/**
 * pmps-proposal.js — Estate Plan Proposal (Client-facing)
 * Usage: require('./pmps-proposal')(data)
 */
'use strict';
const path = require('path');
const shared = require('./_shared');
const {
  docx, TEAL, NAVY, L_TEAL, L_NAVY, GRAY,
  PAGE_PROPS, NUMBERING, noBorders, thinBorders, hdrCell, dataCell, totalCell,
  spacer, sectionHdr, bodyP, bulletP, numP,
  makeHeader, makeFooter, titleBlock, clientNames, fmt
} = shared;

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, WidthType, ShadingType, BorderStyle
} = docx;
const fs = require('fs');

module.exports = function generateProposal(data) {
  const isCouple = data.clients.type === "couple";
  const s1 = data.clients.spouse1;
  const s2 = isCouple ? data.clients.spouse2 : null;
  const names = clientNames(data);
  const hasCreditShelter = isCouple && data.hasCreditShelter;
  const s1tax = data.tax && data.tax.scenario1;
  const s2tax = data.tax && data.tax.scenario2;
  const fid1 = (data.fiduciaries && data.fiduciaries.spouse1) || {};
  const fid2 = (data.fiduciaries && data.fiduciaries.spouse2) || {};
  const cons = data.considerations || {};

  // ── ESTATE OVERVIEW ─────────────────────────────────────────────────────────
  const estateBody = isCouple
    ? `Based on the information you have shared, your combined taxable estate is approximately ${data.assets.grossEstateApprox || data.assets.grossEstateDisplay}. As a married couple with an estate of this size, Massachusetts estate tax planning is an important component of your estate plan.`
    : `Based on the information you have shared, your taxable estate is approximately ${data.assets.grossEstateApprox || data.assets.grossEstateDisplay}.`;

  const maBody = hasCreditShelter
    ? "Massachusetts does not allow spouses to share unused estate tax exemptions — a concept known as portability. Each spouse has a $2,000,000 exemption that is use-it-or-lose-it. Without proactive planning, the first spouse's exemption is typically wasted, and the entire estate is taxed at the second death."
    : (isCouple
        ? "Massachusetts does not allow spouses to share unused estate tax exemptions. Each spouse has a $2,000,000 exemption. Your combined estate is currently below the threshold where tax planning provides immediate benefit, but we recommend monitoring as your estate grows."
        : (s1tax && s1tax.taxableEstate > 2000000
            ? "Your estate exceeds the Massachusetts $2,000,000 estate tax exemption. Unlike federal law, Massachusetts does not allow portability, and the tax applies to your entire estate — not just the amount above the exemption."
            : "Your estate is currently below the $2,000,000 Massachusetts estate tax exemption. No estate tax is due at this time, but we recommend monitoring as your estate grows."));

  const csBody = hasCreditShelter
    ? "A Credit Shelter Trust (also called a Bypass Trust) is the most effective tool to preserve both spouses' exemptions and significantly reduce the estate tax your family will owe."
    : null;

  // ── TAX SUMMARY TABLE ────────────────────────────────────────────────────────
  let taxTable = null;
  if (s1tax && isCouple) {
    const rows = [
      new TableRow({ children: [hdrCell("", 4680), hdrCell("Without Planning", 2340), hdrCell(hasCreditShelter ? "With Credit Shelter" : "Current Plan", 2340)] }),
      new TableRow({ children: [
        dataCell("Combined Estate", 4680, L_NAVY),
        dataCell(fmt(s1tax.taxableEstate), 2340, L_NAVY),
        dataCell(fmt(s1tax.taxableEstate), 2340, L_NAVY),
      ]}),
    ];
    if (hasCreditShelter && s2tax) {
      rows.push(new TableRow({ children: [
        dataCell("First Spouse's Exemption Used", 4680),
        dataCell("❌ Wasted", 2340),
        dataCell("✓ $2,000,000", 2340),
      ]}));
      rows.push(new TableRow({ children: [
        dataCell("Estate Taxed at Second Death", 4680, L_NAVY),
        dataCell(fmt(s1tax.taxableEstate), 2340, L_NAVY),
        dataCell(fmt(s2tax.secondDeath ? s2tax.secondDeath.taxableEstate : 0), 2340, L_NAVY),
      ]}));
    }
    rows.push(new TableRow({ children: [
      dataCell("MA Estate Tax Due", 4680),
      dataCell(fmt(s1tax.netTax), 2340),
      dataCell(hasCreditShelter && s2tax ? fmt(s2tax.totalNetTax) : fmt(s1tax.netTax), 2340),
    ]}));
    if (hasCreditShelter && s2tax && data.tax.savings > 0) {
      rows.push(new TableRow({ children: [
        totalCell("Tax Savings with Credit Shelter", 4680),
        new TableCell({ columnSpan: 2, width: { size: 4680, type: WidthType.DXA },
          shading: { fill: TEAL, type: ShadingType.CLEAR }, borders: noBorders(),
          margins: { top: 100, bottom: 100, left: 160, right: 160 },
          children: [new Paragraph({ children: [new TextRun({ text: fmt(data.tax.savings), font: "Garamond", size: 22, bold: true, color: "FFFFFF" })] })]
        })
      ]}));
    }
    taxTable = new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: [4680, 2340, 2340], rows });
  } else if (s1tax && !isCouple) {
    const rows = [
      new TableRow({ children: [hdrCell("", 4680), hdrCell("Your Estate", 4680)] }),
      new TableRow({ children: [dataCell("Taxable Estate", 4680, L_NAVY), dataCell(fmt(s1tax.taxableEstate), 4680, L_NAVY)] }),
      new TableRow({ children: [dataCell("MA Exemption", 4680), dataCell("$2,000,000", 4680)] }),
      new TableRow({ children: [dataCell("MA Estate Tax Due", 4680, L_NAVY), dataCell(fmt(s1tax.netTax), 4680, L_NAVY, true)] }),
    ];
    taxTable = new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: [4680, 4680], rows });
  }

  // ── DOCUMENT LIST TABLE ──────────────────────────────────────────────────────
  const docColWidths = data.hasLegalPlan ? [5760, 2000, 1600] : [7360, 2000];
  const docHdrs = data.hasLegalPlan
    ? [hdrCell("Document", 5760), hdrCell("Coverage", 2000), hdrCell("MetLife Code", 1600)]
    : [hdrCell("Document", 7360), hdrCell("For", 2000)];

  function metlifeCode(name) {
    if (/trust/i.test(name)) return "260";
    if (/will/i.test(name)) return "200";
    if (/power of attorney|dpoa|poa/i.test(name)) return "220";
    if (/health care proxy|hcp/i.test(name)) return "220";
    if (/hipaa/i.test(name)) return "220";
    if (/living will|advance health/i.test(name)) return "220";
    if (/affidavit|certificate of trust/i.test(name)) return "65";
    return "—";
  }

  const docRows = [(new TableRow({ children: docHdrs }))];
  let rowIdx = 0;
  (data.plan.documents || []).forEach(doc => {
    const bg = rowIdx % 2 === 0 ? L_TEAL : GRAY;
    const forLabel = doc.joint ? "Joint" : (isCouple && doc.perSpouse ? "Each Spouse" : s1.firstName);
    if (data.hasLegalPlan) {
      docRows.push(new TableRow({ children: [
        dataCell(doc.name, 5760, bg, doc.joint),
        dataCell(data.legalPlan ? "Member & Spouse" : "Covered", 2000, bg),
        dataCell(metlifeCode(doc.name), 1600, bg),
      ]}));
    } else {
      docRows.push(new TableRow({ children: [
        dataCell(doc.name, 7360, bg, doc.joint),
        dataCell(forLabel, 2000, bg),
      ]}));
    }
    rowIdx++;
  });

  // Pricing total row
  if (data.hasLegalPlan) {
    // Rough MetLife estimate
    const hasTrust = (data.plan.documents || []).some(d => /trust/i.test(d.name));
    const willDoc = (data.plan.documents || []).find(d => /will/i.test(d.name) && !/trust/i.test(d.name));
    const livingWill = (data.plan.documents || []).find(d => /advance health|living will/i.test(d.name));
    let est = 0;
    if (hasTrust) est += isCouple ? 400 : 325;
    if (willDoc) est += isCouple ? 185 : 150;
    est += isCouple ? 255 : 135; // 3 POA types (couple=$85×3, individual ~$135)
    if (livingWill) est += isCouple ? 65 : 45;
    docRows.push(new TableRow({ children: [
      totalCell("Estimated MetLife Total", 5760, NAVY),
      new TableCell({ width: { size: 2000, type: WidthType.DXA }, shading: { fill: NAVY, type: ShadingType.CLEAR }, borders: noBorders(), margins: { top: 100, bottom: 100, left: 160, right: 160 }, children: [new Paragraph({ children: [new TextRun({ text: "", font: "Garamond", size: 20, color: "FFFFFF" })] })] }),
      totalCell(`~$${est}*`, 1600, TEAL),
    ]}));
  } else {
    docRows.push(new TableRow({ children: [
      totalCell("Plan Total (Flat Fee)", 7360, NAVY),
      totalCell(data.flatFee || "[confirm]", 2000, TEAL),
    ]}));
  }
  const docTable = new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: docColWidths, rows: docRows });

  // ── FIDUCIARY TABLE ──────────────────────────────────────────────────────────
  function fidRow(role, v1, v2) {
    const bg = ["Trustee", "Personal Representative", "Health Care Proxy Agent"].includes(role) ? L_TEAL : GRAY;
    const bold = ["Trustee", "Personal Representative", "Health Care Proxy Agent"].includes(role);
    if (isCouple) {
      return new TableRow({ children: [dataCell(role, 2600, bg, bold), dataCell(v1 || "[To be determined]", 3380), dataCell(v2 || "[To be determined]", 3380)] });
    }
    return new TableRow({ children: [dataCell(role, 3360, bg, bold), dataCell(v1 || "[To be determined]", 6000)] });
  }

  const fidColWidths = isCouple ? [2600, 3380, 3380] : [3360, 6000];
  const fidHdrs = isCouple
    ? [hdrCell("Role", 2600), hdrCell(s1.firstName, 3380), hdrCell(s2.firstName, 3380)]
    : [hdrCell("Role", 3360), hdrCell("Your Appointments", 6000)];

  const fidRows = [
    new TableRow({ children: fidHdrs }),
    fidRow("Trustee", fid1.trustee, fid2.trustee),
    fidRow("Successor Trustee", fid1.successorTrustee || fid1.trustee, fid2.successorTrustee || fid2.trustee),
    fidRow("Personal Representative", fid1.personalRep, fid2.personalRep),
    fidRow("DPOA Agent", fid1.poaAgent, fid2.poaAgent),
    fidRow("Health Care Proxy Agent", fid1.hcpAgent, fid2.hcpAgent),
    ...(data.hasMinorChildren ? [fidRow("Guardian (minor children)", fid1.guardian, fid2.guardian)] : [])
  ];
  const fidTable = new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: fidColWidths, rows: fidRows });

  // ── ADDITIONAL CONSIDERATIONS ────────────────────────────────────────────────
  const consItems = [];
  if (data.hasMinorChildren) consItems.push("Minor beneficiary provisions: your trust holds any child's inheritance until a responsible age you specify (e.g., distributing at ages 25 and 30). This prevents a minor inheriting outright at 18.");
  if (cons.beneficiaryDesignations) consItems.push(cons.beneficiaryDesignations);
  if (cons.realEstateTransfer) consItems.push(cons.realEstateTransfer);
  if (cons.lifeInsurance || cons.ilit) consItems.push((cons.lifeInsurance || "") + (cons.ilit ? " Consider an Irrevocable Life Insurance Trust (ILIT) to remove the death benefit from your taxable estate." : ""));
  if (cons.anticipatedInheritance) consItems.push(cons.anticipatedInheritance);
  if (cons.pets) consItems.push(cons.pets);
  if (cons.gifting) consItems.push("Annual gifting: $18,000/year per recipient reduces your taxable estate without gift tax implications.");
  if (cons.youngAdultPlans) {
    const y = cons.youngAdultPlans;
    consItems.push(`Young Adult Estate Plan for ${y.name || "your adult child"}${y.age ? ` (age ${y.age})` : ""}${y.school ? ` at ${y.school}` : ""}: Once a child turns 18, parents lose automatic legal authority over medical, financial, and educational decisions. We recommend a package of Health Care Proxy, Durable Power of Attorney, Education Power of Attorney, Living Will, and HIPAA Authorization.`);
  }

  // ── ASSEMBLE CHILDREN ──────────────────────────────────────────────────────
  const children = [
    sectionHdr("About Your Estate"),
    bodyP(estateBody),
    bodyP(maBody),
    ...(csBody ? [bodyP(csBody)] : []),
  ];

  if (taxTable) {
    children.push(spacer(120));
    children.push(sectionHdr("MA Estate Tax Summary"));
    if (isCouple) children.push(bodyP("The table below compares two scenarios for your estate:"));
    children.push(spacer(80));
    children.push(taxTable);
    children.push(spacer(60));
    children.push(bodyP("* Tax estimates are based on current Massachusetts law and are provided for planning purposes only.", { italics: true, size: 18, color: "888888" }));
  }

  children.push(spacer(120));
  children.push(sectionHdr("Our Recommended Plan"));
  children.push(bodyP(`Based on your goals and the size of your estate, we recommend ${isCouple ? "a " : "an "}${data.plan.type || "estate plan"} including the following documents:`));
  children.push(spacer(80));
  children.push(docTable);
  if (data.hasLegalPlan) {
    children.push(spacer(60));
    children.push(bodyP("* MetLife/ARAG billing estimate. Coverage for credit shelter / tax-planning trusts may require case manager review.", { italics: true, size: 18, color: "888888" }));
  }

  if (data.hasTrust) {
    children.push(spacer(120));
    children.push(sectionHdr("About Your Trust"));
    const trustDesc = isCouple
      ? `Your Revocable Living Trust will hold your assets during your lifetime and distribute them according to your wishes at death — without going through the Massachusetts probate process, which typically takes 9 to 18 months.${hasCreditShelter ? ` Your trust includes Credit Shelter provisions. At the death of the first spouse, up to $2,000,000 passes into a Bypass Trust, capturing that spouse's exemption completely free of estate tax. The surviving spouse receives income from the Bypass Trust for life and may access principal for health, education, maintenance, and support. At the second death, the Bypass Trust distributes to your named beneficiaries.` : ""}`
      : `Your Revocable Living Trust will hold your assets during your lifetime and distribute them according to your wishes at death — without going through the Massachusetts probate process, which typically takes 9 to 18 months.`;
    children.push(bodyP(trustDesc));
    if (data.hasMinorChildren) {
      children.push(bodyP("Because you have minor children, your trust will include provisions to hold and manage any inheritance for a minor beneficiary until they reach ages you specify — for example, distributing at ages 25 and 30."));
    }
  }

  children.push(spacer(120));
  children.push(sectionHdr("Fiduciary Appointments"));
  children.push(bodyP("One of the most important decisions in your estate plan is choosing who will act on your behalf. These appointments will be confirmed during your planning session."));
  children.push(spacer(80));
  children.push(fidTable);

  if (consItems.length > 0) {
    children.push(spacer(120));
    children.push(sectionHdr("Additional Considerations"));
    consItems.forEach(item => children.push(bulletP(item.trim())));
  }

  children.push(spacer(120));
  children.push(sectionHdr("Next Steps"));
  children.push(numP("Sign the Engagement Agreement — we will email it to you after today's meeting."));
  children.push(numP("Complete the design phase — we will gather your fiduciary appointments and document preferences."));
  children.push(numP("Receive draft documents for your review within 2–3 weeks of engagement."));
  children.push(numP("Attend your signing ceremony — in-person, with attorney, notary, and two witnesses."));
  children.push(numP("Receive your Funding Roadmap and complete trust funding (including any real property transfers)."));

  children.push(spacer(160));
  children.push(new Paragraph({
    children: [new TextRun({ text: "Aubrey Law  |  1329 Highland Avenue, Suite 1A, Needham, MA 02492  |  scott@aubreylegal.com", font: "Garamond", size: 18, color: "888888", italics: true })],
    alignment: AlignmentType.CENTER
  }));

  const doc = new Document({
    numbering: NUMBERING,
    sections: [{
      properties: PAGE_PROPS,
      headers: { default: makeHeader() },
      footers: { default: makeFooter("Estate Plan Proposal") },
      children: [
        ...titleBlock("ESTATE PLAN PROPOSAL", `Prepared for ${names}`, `Aubrey Law  |  ${data.matter.date}`),
        ...children
      ]
    }]
  });

  const outFile = path.join(data.matter.outputDir, `${data.matter.filePrefix}_Proposal.docx`);
  return Packer.toBuffer(doc).then(buf => { fs.writeFileSync(outFile, buf); console.log(`✓ ${path.basename(outFile)}`); });
};
