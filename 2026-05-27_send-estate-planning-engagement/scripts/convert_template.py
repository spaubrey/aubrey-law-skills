#!/usr/bin/env python3
"""
convert_template.py — Convert the Mustache-syntax engagement agreement
template from SharePoint into the Jinja2 + DocuSeal-marker template the
skill uses at runtime.

Usage:
    python3 convert_template.py \
        --source path/to/engagement_template_source.docx \
        --out    assets/engagement_template.docx

Run this once at skill setup, and re-run whenever the SharePoint canonical
template is updated. Output is committed alongside the skill.

The script depends on `/mnt/skills/public/docx/scripts/office/unpack.py` and
`pack.py` (Cowork's docx skill) for the run-merging unpack step. If those
are not available, the script falls back to a plain zip extract/repack but
may fail on templates where Mustache tags are split across runs by Word.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

# DocuSeal placeholder vars — these become literal DocuSeal field markers
# (wrapped in {% raw %} so Jinja2 doesn't try to render them).
DOCUSEAL_FIELDS = {
    "client_sig": "{{Client Signature;type=signature;role=Client;required=true}}",
    "client_date": "{{Client Date;type=date;role=Client;required=true}}",
    "spouse_sig": "{{Spouse Signature;type=signature;role=Spouse;required=true}}",
    "spouse_date": "{{Spouse Date;type=date;role=Spouse;required=true}}",
    "credit_shelter_election": "{{CST Election;type=checkbox;role=Client;required=false}}",
}

# Variables that pass through as Jinja2 substitutions
DATA_VARS = {
    "client_name", "spouse_name",
    "flat_fee_amount", "legal_plan_name",
    "trust_label", "trust_label_lp",
}


def paragraph_only_contains_tag(xml_text: str, tag_start: int, tag_end: int) -> bool:
    """Is this Mustache tag the only text content in its <w:p> paragraph?"""
    p_open_a = xml_text.rfind("<w:p ", 0, tag_start)
    p_open_b = xml_text.rfind("<w:p>", 0, tag_start)
    p_open = max(p_open_a, p_open_b)
    if p_open == -1:
        return False
    p_close = xml_text.find("</w:p>", tag_end)
    if p_close == -1:
        return False
    paragraph_xml = xml_text[p_open:p_close + len("</w:p>")]
    text_chunks = re.findall(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>", paragraph_xml)
    full_text = "".join(text_chunks)
    matched = xml_text[tag_start:tag_end]
    return full_text.replace(matched, "", 1).strip() == ""


def convert_document_xml(xml_text: str) -> str:
    """Convert Mustache control flow to Jinja2; wrap DocuSeal markers in raw blocks."""
    tag_re = re.compile(r"\{\{([#^/])?([A-Za-z_][A-Za-z0-9_]*)?\}\}")
    section_stack: list[str] = []
    out_parts: list[str] = []
    last_end = 0

    for m in tag_re.finditer(xml_text):
        prefix, name = m.group(1), m.group(2)
        out_parts.append(xml_text[last_end:m.start()])
        is_alone = paragraph_only_contains_tag(xml_text, m.start(), m.end())

        if prefix == "#" and name:
            section_stack.append(name)
            out_parts.append(f"{{%p if {name} %}}" if is_alone else f"{{% if {name} %}}")
        elif prefix == "^" and name:
            section_stack.append(name)
            out_parts.append(f"{{%p if not {name} %}}" if is_alone else f"{{% if not {name} %}}")
        elif prefix == "/":
            if not section_stack:
                raise ValueError(f"Unmatched closing tag at position {m.start()}")
            section_stack.pop()
            out_parts.append("{%p endif %}" if is_alone else "{% endif %}")
        elif name:
            if name in DOCUSEAL_FIELDS:
                out_parts.append(f"{{% raw %}}{DOCUSEAL_FIELDS[name]}{{% endraw %}}")
            elif name in DATA_VARS:
                out_parts.append(f"{{{{ {name} }}}}")
            else:
                # Unknown variable — pass through; will error at render time if not provided
                out_parts.append(f"{{{{ {name} }}}}")
        else:
            out_parts.append(m.group(0))
        last_end = m.end()

    out_parts.append(xml_text[last_end:])
    if section_stack:
        raise ValueError(f"Unclosed sections: {section_stack}")
    return "".join(out_parts)


def unpack_with_run_merge(source: Path, out_dir: Path) -> bool:
    """Use Cowork's docx unpack (merges adjacent runs). Returns True if used."""
    unpack_script = Path("/mnt/skills/public/docx/scripts/office/unpack.py")
    if not unpack_script.exists():
        return False
    subprocess.run(
        ["python3", str(unpack_script), str(source), str(out_dir)],
        check=True,
    )
    return True


def unpack_plain(source: Path, out_dir: Path) -> None:
    """Fallback: plain zip extraction."""
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source) as z:
        z.extractall(out_dir)


def pack_with_validation(unpacked: Path, output: Path, original: Path) -> bool:
    pack_script = Path("/mnt/skills/public/docx/scripts/office/pack.py")
    if not pack_script.exists():
        return False
    subprocess.run(
        ["python3", str(pack_script), str(unpacked), str(output),
         "--original", str(original), "--validate", "false"],
        check=True,
    )
    return True


def pack_plain(unpacked: Path, output: Path) -> None:
    """Fallback: plain zip repackage."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
        for p in unpacked.rglob("*"):
            if p.is_file():
                z.write(p, p.relative_to(unpacked))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", required=True, help="Source Mustache .docx")
    p.add_argument("--out", required=True, help="Output Jinja2 .docx")
    args = p.parse_args()

    source = Path(args.source)
    output = Path(args.out)
    if not source.exists():
        print(f"ERROR: source not found: {source}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp:
        unpacked = Path(tmp) / "unpacked"
        if not unpack_with_run_merge(source, unpacked):
            print("Note: Cowork docx unpack not found; using plain zip extract", file=sys.stderr)
            unpack_plain(source, unpacked)

        doc_xml = unpacked / "word" / "document.xml"
        original_xml = doc_xml.read_text()
        converted = convert_document_xml(original_xml)
        doc_xml.write_text(converted)

        if not pack_with_validation(unpacked, output, source):
            print("Note: Cowork docx pack not found; using plain zip repackage", file=sys.stderr)
            pack_plain(unpacked, output)

    print(f"Converted -> {output}")


if __name__ == "__main__":
    main()
