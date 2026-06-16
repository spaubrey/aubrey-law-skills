/**
 * pmps-tax-worksheet.js — MA Estate Tax Worksheet (Attorney-only)
 * Usage: require('./pmps-tax-worksheet')(data)
 */
'use strict';
const path = require('path');
const shared = require('./_shared');
const {
  docx, TEAL, NAVY, L_TEAL, L_NAVY, GRAY,
  PAGE_PROPS, NUMBERING, noBorders, hdrCell, dataCell, totalCell,
  spacer, sectionHdr, bodyP,
  makeHeader, makeFooter, titleBlock, clientNames, fmt
} = shared;

const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, WidthType, ShadingType } = docx;
const fs = require('fs');

module.exports = function generateTaxWorksheet(data) {
  const isCouple = data.clients.type === "couple";
  const names = clientNames(data);
  const s1tax = data.tax && data.tax.scenario1;
  const s2tax = data.tax && data.tax.scenario2;
  const hasCreditShelter = isCouple && data.hasCreditShelter && s2tax;

  function wRow(label, value, bg = "FFFFFF", bold = false) {
    return new TableRow({ children: [
      dataCell(label, 5760, bg, bold, bold ? NAVY : "444444"),
      dataCell(value, 3600, bg, bold, bold ? NAVY : "333333"),
    ]});
  }
  function wHdr(l1, l2) { return new TableRow({ children: [hdrCell(l1, 5760), hdrCell(l2, 3600)] }); }
  function wTotal(label, value, bg = TEAL) {
    return new TableRow({ children: [totalCell(label, 5760, bg), totalCell(value, 3600, bg)] });
  }

  function computationTable(tax, title) {
    if (!tax) return [];
    return [
      new Paragraph({ children: [new TextRun({ text: title, font: "Garamond", size: 24, bold: true, color: NAVY })], spacing: { before: 80, after: 80 } }),
      new Table({
        width: { size: 9360, type: WidthType.DXA }, columnWidths: [5760, 3600],
        rows: [
          wHdr("Computation Step", "Amount"),
          wRow("Gross / Taxable Estate", fmt(tax.taxableEstate), L_NAVY),
          wRow("Less: Statutory Adjustment", "−$60,000"),
          wRow("= Adjusted Taxable Estate", fmt(tax.adjustedTaxableEstate), L_NAVY, true),
          wRow("Rate Bracket Floor", fmt(tax.bracketFloor)),
          wRow("Base Tax at Bracket Floor", fmt(tax.baseTax), L_NAVY),
          wRow("Excess Above Floor", fmt(tax.excess)),
          wRow("Rate on Excess", (tax.bracketRate * 100).toFixed(1) + "%", L_NAVY),
          wRow("Tax on Excess", fmt(tax.taxOnExcess)),
          wRow("= Gross Tax", fmt(tax.grossTax), L_NAVY, true),
          wRow("Less: Unified Credit", "−$99,600"),
          wTotal("= Net MA Estate Tax", fmt(tax.netTax)),
        ]
      }),
      spacer(120)
    ];
  }

  // Key facts table
  const keyFacts = new Table({
    width: { size: 9360, type: WidthType.DXA }, columnWidths: [5760, 3600],
    rows: [
      wRow("Gross / Taxable Estate", data.assets.grossEstateDisplay || fmt(s1tax ? s1tax.taxableEstate : 0), L_NAVY, true),
      wRow("MA Exemption per Person", "$2,000,000"),
      wRow("Portability", isCouple ? "None — use it or lose it per spouse" : "N/A — individual client"),
      wRow("Unified Credit", "$99,600"),
      wRow("Statutory Adjustment", "−$60,000 from taxable estate"),
      wRow("Planning Recommendation", hasCreditShelter ? "Credit Shelter Trust — recommended" : (isCouple ? "Monitor estate growth" : "Revocable Trust — no credit shelter applicable"), L_TEAL, true),
    ]
  });

  const body = [
    sectionHdr("Key Facts"),
    keyFacts,
    spacer(200),
  ];

  if (s1tax) {
    if (isCouple) {
      body.push(sectionHdr("Scenario 1: Without Credit Shelter Planning"));
      body.push(bodyP("All assets pass to surviving spouse at first death (unlimited marital deduction → $0 tax at first death). First spouse's $2M exemption is wasted. At second death, the full estate is taxed."));
      body.push(spacer(80));
      body.push(...computationTable(s1tax, "Second Death — Full Estate Taxed"));
    } else {
      body.push(sectionHdr("Estate Tax at Death"));
      body.push(bodyP("The following computation shows your Massachusetts estate tax exposure based on the current value of your estate."));
      body.push(spacer(80));
      body.push(...computationTable(s1tax, "Tax at Death"));
    }
  }

  if (hasCreditShelter && s2tax) {
    body.push(sectionHdr("Scenario 2: With Credit Shelter Trust"));
    body.push(bodyP("At first death, $2,000,000 passes to a Bypass Trust. The unified credit fully offsets the tax on $2M, resulting in $0 tax at first death. Only the remaining estate is taxed at the second death."));
    body.push(spacer(80));

    // Step A — First death
    body.push(new Paragraph({ children: [new TextRun({ text: "Step A — First Death (Bypass Trust Funding)", font: "Garamond", size: 22, bold: true, color: NAVY })], spacing: { before: 80, after: 60 } }));
    body.push(new Table({
      width: { size: 9360, type: WidthType.DXA }, columnWidths: [5760, 3600],
      rows: [
        wHdr("Computation Step", "Amount"),
        wRow("Amount to Bypass Trust", fmt(s2tax.firstDeath.bypassAmount), L_NAVY),
        wRow("Gross Tax on $2,000,000", fmt(s2tax.firstDeath.grossTax)),
        wRow("Less: Unified Credit", "−$99,600", L_NAVY),
        wTotal("= Net MA Estate Tax (First Death)", fmt(s2tax.firstDeath.netTax)),
      ]
    }));
    body.push(spacer(120));

    // Step B — Second death
    body.push(new Paragraph({ children: [new TextRun({ text: "Step B — Second Death (Surviving Spouse's Estate)", font: "Garamond", size: 22, bold: true, color: NAVY })], spacing: { before: 80, after: 60 } }));
    body.push(...computationTable(s2tax.secondDeath, ""));
  }

  // Comparison summary (couples only)
  if (s1tax && isCouple) {
    body.push(sectionHdr("Comparison Summary"));
    const savingsGreen = "1A6B30";
    body.push(new Table({
      width: { size: 9360, type: WidthType.DXA }, columnWidths: [5760, 3600],
      rows: [
        wHdr("", "MA Estate Tax"),
        wRow(hasCreditShelter ? "Scenario 1: Without Credit Shelter" : "Current Estate Tax Exposure", fmt(s1tax.netTax), L_NAVY),
        ...(hasCreditShelter && s2tax ? [
          wRow("Scenario 2: With Credit Shelter Trust", fmt(s2tax.totalNetTax)),
          new TableRow({ children: [
            totalCell("Tax Savings with Credit Shelter Planning", 5760, savingsGreen),
            totalCell(fmt(data.tax.savings), 3600, savingsGreen),
          ]})
        ] : [])
      ]
    }));
  }

  body.push(spacer(200));
  body.push(new Paragraph({
    children: [new TextRun({ text: "CONFIDENTIAL — ATTORNEY USE ONLY  |  Tax computations reflect current MA law. For planning purposes only; not legal or tax advice.", font: "Garamond", size: 16, color: "AAAAAA", italics: true })],
    alignment: AlignmentType.CENTER
  }));

  const doc = new Document({
    numbering: NUMBERING,
    sections: [{
      properties: PAGE_PROPS,
      headers: { default: makeHeader() },
      footers: { default: makeFooter("MA Estate Tax Worksheet — Confidential") },
      children: [
        ...titleBlock("MA ESTATE TAX WORKSHEET", `${names}  |  ${data.matter.date}`, "Confidential — Attorney Use Only"),
        ...body
      ]
    }]
  });

  const outFile = path.join(data.matter.outputDir, `${data.matter.filePrefix}_TaxWorksheet.docx`);
  return Packer.toBuffer(doc).then(buf => { fs.writeFileSync(outFile, buf); console.log(`✓ ${path.basename(outFile)}`); });
};
