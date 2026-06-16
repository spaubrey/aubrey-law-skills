/**
 * _shared.js — Shared branding, helpers, and docx utilities for all PMPS templates.
 * All templates require this file: const shared = require('./_shared');
 */

'use strict';

let docx;
try { docx = require('docx'); }
catch { docx = require('/tmp/npm/lib/node_modules/docx'); }

const {
  BorderStyle, WidthType, ShadingType, AlignmentType,
  VerticalAlign, LevelFormat, PageNumber, Header, Footer,
  ImageRun, Paragraph, TextRun, Table, TableRow, TableCell,
  PageBreak
} = docx;

const fs = require('fs');
const path = require('path');

// ── BRAND CONSTANTS ──────────────────────────────────────────────────────────
const TEAL    = "1A7A6D";
const NAVY    = "1B3A5C";
const L_TEAL  = "E8F5F3";
const L_NAVY  = "EDF0F5";
const GRAY    = "F5F5F5";
const AMBER   = "FFF3CD";
const AMBER_B = "FFC107";

const LOGO_PATH = path.join(__dirname, '..', 'assets', 'aubrey-law-logo.png');

const PAGE_PROPS = {
  page: {
    size: { width: 12240, height: 15840 },
    margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
  }
};

const NUMBERING = {
  config: [
    { reference: "bullets",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 480, hanging: 240 } } } }] },
    { reference: "sub-bullets",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 960, hanging: 240 } } } }] },
    { reference: "numbers",
      levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 480, hanging: 240 } } } }] },
  ]
};

// ── BORDER FACTORIES ─────────────────────────────────────────────────────────
function bdr(color = "CCCCCC", size = 4) {
  return { style: BorderStyle.SINGLE, size, color };
}
function allBorders(color = "CCCCCC") {
  const b = bdr(color);
  return { top: b, bottom: b, left: b, right: b };
}
function noBorders() {
  const nb = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  return { top: nb, bottom: nb, left: nb, right: nb };
}
function thinBorders() { return allBorders("DDDDDD"); }

// ── CELL FACTORIES ───────────────────────────────────────────────────────────
function hdrCell(text, width, bg = NAVY) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { fill: bg, type: ShadingType.CLEAR },
    borders: noBorders(),
    margins: { top: 100, bottom: 100, left: 160, right: 160 },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      children: [new TextRun({ text, font: "Garamond", size: 20, bold: true, color: "FFFFFF" })]
    })]
  });
}

function dataCell(text, width, bg = "FFFFFF", bold = false, color = "333333") {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { fill: bg, type: ShadingType.CLEAR },
    borders: thinBorders(),
    margins: { top: 80, bottom: 80, left: 160, right: 160 },
    children: [new Paragraph({
      children: [new TextRun({ text, font: "Garamond", size: 20, bold, color })]
    })]
  });
}

function totalCell(text, width, bg = TEAL) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { fill: bg, type: ShadingType.CLEAR },
    borders: noBorders(),
    margins: { top: 100, bottom: 100, left: 160, right: 160 },
    children: [new Paragraph({
      children: [new TextRun({ text, font: "Garamond", size: 20, bold: true, color: "FFFFFF" })]
    })]
  });
}

function flagCell(text, width = 9360) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { fill: AMBER, type: ShadingType.CLEAR },
    borders: {
      top: bdr(AMBER_B), bottom: bdr(AMBER_B),
      left: { style: BorderStyle.SINGLE, size: 12, color: AMBER_B },
      right: bdr(AMBER_B)
    },
    margins: { top: 100, bottom: 100, left: 200, right: 200 },
    children: [new Paragraph({
      children: [new TextRun({ text: "⚑  " + text, font: "Garamond", size: 20, color: "856404" })]
    })]
  });
}

// ── PARAGRAPH FACTORIES ──────────────────────────────────────────────────────
function spacer(size = 120) {
  return new Paragraph({ children: [new TextRun("")], spacing: { before: size, after: 0 } });
}

function sectionHdr(text, color = NAVY) {
  return new Paragraph({
    children: [new TextRun({ text, font: "Garamond", size: 28, bold: true, color })],
    spacing: { before: 280, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } }
  });
}

function bodyP(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, font: "Garamond", size: 22, color: "333333", ...opts })],
    spacing: { before: 80, after: 80 }
  });
}

function bulletP(text, bold = false) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    children: [new TextRun({ text, font: "Garamond", size: 22, color: "333333", bold })],
    spacing: { before: 40, after: 40 }
  });
}

function numP(text) {
  return new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    children: [new TextRun({ text, font: "Garamond", size: 22, color: "333333" })],
    spacing: { before: 60, after: 60 }
  });
}

function subBulletP(text) {
  return new Paragraph({
    numbering: { reference: "sub-bullets", level: 0 },
    children: [new TextRun({ text, font: "Garamond", size: 20, color: "555555" })],
    spacing: { before: 20, after: 20 }
  });
}

// ── HEADER / FOOTER ──────────────────────────────────────────────────────────
function makeHeader() {
  const logoData = fs.readFileSync(LOGO_PATH);
  return new Header({
    children: [new Paragraph({
      children: [new ImageRun({
        type: "png", data: logoData,
        transformation: { width: 120, height: 40 },
        altText: { title: "Aubrey Law", description: "Aubrey Law Logo", name: "logo" }
      })],
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: TEAL, space: 4 } }
    })]
  });
}

function makeFooter(docType) {
  return new Footer({
    children: [new Paragraph({
      children: [
        new TextRun({ text: `Aubrey Law  |  scott@aubreylegal.com  |  Needham, MA  |  `, font: "Garamond", size: 16, color: "888888" }),
        new TextRun({ text: docType, font: "Garamond", size: 16, color: "888888", italics: true }),
        new TextRun({ text: "\t", font: "Garamond", size: 16 }),
        new TextRun({ text: "Page ", font: "Garamond", size: 16, color: "888888" }),
        new TextRun({ children: [PageNumber.CURRENT], font: "Garamond", size: 16, color: "888888" }),
      ],
      tabStops: [{ type: "right", position: 9360 }],
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: TEAL, space: 4 } }
    })]
  });
}

// ── TITLE BLOCK ──────────────────────────────────────────────────────────────
function titleBlock(title, subtitle, date) {
  return [
    new Paragraph({
      children: [new TextRun({ text: title, font: "Garamond", size: 40, bold: true, color: NAVY })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 120, after: 60 }
    }),
    new Paragraph({
      children: [new TextRun({ text: subtitle, font: "Garamond", size: 26, color: TEAL, italics: true })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 60 }
    }),
    new Paragraph({
      children: [new TextRun({ text: date, font: "Garamond", size: 20, color: "888888" })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 280 }
    })
  ];
}

// ── CLIENT NAME HELPERS ──────────────────────────────────────────────────────
function clientNames(data) {
  const s1 = data.clients.spouse1.fullName;
  if (data.clients.type === "couple") return `${s1} and ${data.clients.spouse2.fullName}`;
  return s1;
}

function fmt(n) {
  if (n == null || n === 0) return "$0";
  return "$" + Number(n).toLocaleString();
}

// ── EXPORTS ──────────────────────────────────────────────────────────────────
module.exports = {
  docx,
  TEAL, NAVY, L_TEAL, L_NAVY, GRAY, AMBER, AMBER_B,
  PAGE_PROPS, NUMBERING,
  bdr, allBorders, noBorders, thinBorders,
  hdrCell, dataCell, totalCell, flagCell,
  spacer, sectionHdr, bodyP, bulletP, numP, subBulletP,
  makeHeader, makeFooter, titleBlock,
  clientNames, fmt
};
