/* =====================================================================
 * pmps-prep — SAMPLE data objects, one per planStructure
 * ---------------------------------------------------------------------
 * Paste into Templates/pmps-data-schema.js (or reference from it).
 *
 * NEW FIELD: data.plan.planStructure  (string, required)
 *   "joint_outright"    — Joint Trust, Outright to Spouse (baseline / minimal)
 *   "joint_disclaimer"  — Joint Trust, Disclaimer Planning
 *   "separate_clayton"  — Separate Revocable Trusts + Credit Shelter + Clayton Election
 *   "individual_single" — Individual Trust for a single person
 *
 * RELATED FLAGS the templates branch on:
 *   plan.hasTrust, plan.hasCreditShelter, plan.clayton (bool),
 *   plan.maQtip (bool), clients.type ("couple" | "individual")
 *
 * TAX NOTE: all `tax` numbers below are ILLUSTRATIVE estimates pending
 * attorney verification against the M-706 process. The "both exemptions
 * preserved" scenarios shelter $4,000,000 (NOT $2,000,000) — fixing the
 * prior bug where the column sheltered only $2M while the text claimed $4M.
 * Figures use a $14,391,911 gross estate for the couple samples so they
 * tie to the worked example in ma-estate-tax-computation.md.
 * ===================================================================== */

/* ---------------------------------------------------------------------
 * SHARED building blocks reused across samples (children, assets, etc.)
 * ------------------------------------------------------------------- */
const SAMPLE_CHILDREN = [
  { name: "Sawyer James Sample", dob: "April 28, 2016",   age: 10, isMinor: true,  relationship: "Son" },
  { name: "Oliver Grey Sample",  dob: "March 20, 2019",   age: 7,  isMinor: true,  relationship: "Son" },
  { name: "Jack Riley Sample",   dob: "February 23, 2022", age: 4, isMinor: true,  relationship: "Son" }
];

const SAMPLE_ASSET_BREAKDOWN = [
  { category: "Real Estate (primary residence, net of mortgage)", value: 1398131, display: "$1,398,131" },
  { category: "Bank Accounts",                                    value: 99183,   display: "$99,183" },
  { category: "Retirement Accounts",                              value: 421632,  display: "$421,632" },
  { category: "Brokerage / Investment Accounts",                  value: 3402309, display: "$3,402,309" },
  { category: "Cryptocurrencies",                                 value: 93000,   display: "$93,000" },
  { category: "Life Insurance (term)",                            value: 1000000, display: "$1,000,000" },
  { category: "Business Interests",                               value: 8030000, display: "$8,030,000" },
  { category: "Vehicles (net of loan)",                           value: -56000,  display: "($56,000)" }
];
// Gross = 14,391,911

/* =====================================================================
 * 1) JOINT TRUST — OUTRIGHT TO SPOUSE   (baseline / minimal planning)
 * ===================================================================== */
const SAMPLE_JOINT_OUTRIGHT = {
  matter: {
    filePrefix: "SampleOutright",
    outputDir: "OUTPUTS/SampleOutright/Intake/",
    date: "June 15, 2026",
    attorney: "Scott Aubrey, Esq."
  },
  clients: {
    type: "couple",
    spouse1: { firstName: "Matt", lastName: "Sample", fullName: "Matt Sample",
               dob: "January 10, 1985", age: 41, citizen: true },
    spouse2: { firstName: "Julie", lastName: "Sample", fullName: "Julie Sample",
               dob: "February 22, 1986", age: 40, citizen: true },
    address: "19 Sample Ave, Needham, MA 02492",
    county: "Norfolk"
  },
  children: SAMPLE_CHILDREN,
  assets: {
    grossEstate: 14391911,
    grossEstateDisplay: "$14,391,911",
    grossEstateApprox: "$14.4 million",
    breakdown: SAMPLE_ASSET_BREAKDOWN
  },
  plan: {
    planStructure: "joint_outright",
    hasTrust: true,
    hasCreditShelter: false,   // no bypass funded — assets pass outright
    clayton: false,
    maQtip: false,
    hasMinorChildren: true,
    hasRealEstate: true,
    hasLifeInsurance: true,
    hasPets: false,
    documents: [
      { name: "Joint Revocable Living Trust", category: "core", joint: true,
        displayName: "Joint Revocable Living Trust",
        description: "A single joint trust holding the couple's assets. At the first death, assets remain available to the surviving spouse outright; no credit shelter trust is funded." },
      { name: "Pour-Over Will", category: "will", perSpouse: true },
      { name: "Durable General Power of Attorney", category: "incapacity", perSpouse: true },
      { name: "Health Care Proxy", category: "incapacity", perSpouse: true },
      { name: "HIPAA Authorization", category: "incapacity", perSpouse: true },
      { name: "Living Will (Advance Health Directive)", category: "incapacity", perSpouse: true },
      { name: "Assignment of Personal Property", category: "asset", perSpouse: true },
      { name: "Certificate of Trust", category: "asset", joint: true },
      { name: "Quitclaim Deed", category: "asset", joint: true },
      { name: "Parental Appointment of Guardian", category: "guardian", joint: true },
      { name: "Temporary Delegation of Parental Powers", category: "guardian", joint: true }
    ]
  },
  tax: {
    // Scenario 1 (baseline) = the live result for this structure.
    scenario1: { label: "Outright to Spouse (one exemption used)",
      firstDeathTax: 0, firstDeathTaxDisplay: "$0",
      survivorEstate: 14391911, survivorEstateDisplay: "$14,391,911",
      adjustedTaxableEstate: 14331911,
      grossTax: 1769506, netTax: 1769506,
      secondDeathTax: 1769506, secondDeathTaxDisplay: "$1,769,506",
      totalTax: 1769506, totalTaxDisplay: "$1,769,506", totalTaxApprox: "$1.77 million" },
    scenario2: null,            // no planning scenario to compare against
    savings: 0, savingsDisplay: "$0",
    note: "This structure does not preserve the first spouse's $2M Massachusetts exemption. Compare against the disclaimer and separate-trust structures to see the potential savings."
  },
  fiduciaries: {
    spouse1: { initialTrustee: "Matt (self)", successorTrustees: ["Julie", "[To be determined]"],
               personalRep: "Julie", poaPrimary: "Julie", poaSuccessor: "[To be determined]",
               hcpPrimary: "Julie", hcpSuccessor: "[To be determined]", guardian: "[To be determined]" },
    spouse2: { initialTrustee: "Julie (self)", successorTrustees: ["Matt", "[To be determined]"],
               personalRep: "Matt", poaPrimary: "Matt", poaSuccessor: "[To be determined]",
               hcpPrimary: "Matt", hcpSuccessor: "[To be determined]", guardian: "[To be determined]" },
    notes: [ { label: "Successor fiduciaries pending", body: "Successor trustees, POA/HCP successors, and backup guardians to be finalized at the design meeting." } ]
  },
  considerations: {
    realEstateTransfer: "Transfer the residence into the joint trust via quitclaim deed.",
    beneficiaryDesignations: "Review retirement and life insurance beneficiary designations to coordinate with the trust.",
    lifeInsurance: "Existing $1,000,000 term policy; discuss whether an ILIT is warranted given estate size.",
    ilit: null
  },
  hasLegalPlan: false,
  flatFee: "$5,000"
};

/* =====================================================================
 * 2) JOINT TRUST — DISCLAIMER PLANNING
 * ===================================================================== */
const SAMPLE_JOINT_DISCLAIMER = {
  matter: {
    filePrefix: "SampleDisclaimer",
    outputDir: "OUTPUTS/SampleDisclaimer/Intake/",
    date: "June 15, 2026",
    attorney: "Scott Aubrey, Esq."
  },
  clients: {
    type: "couple",
    spouse1: { firstName: "Matt", lastName: "Sample", fullName: "Matt Sample",
               dob: "January 10, 1985", age: 41, citizen: true },
    spouse2: { firstName: "Julie", lastName: "Sample", fullName: "Julie Sample",
               dob: "February 22, 1986", age: 40, citizen: true },
    address: "19 Sample Ave, Needham, MA 02492",
    county: "Norfolk"
  },
  children: SAMPLE_CHILDREN,
  assets: {
    grossEstate: 14391911,
    grossEstateDisplay: "$14,391,911",
    grossEstateApprox: "$14.4 million",
    breakdown: SAMPLE_ASSET_BREAKDOWN
  },
  plan: {
    planStructure: "joint_disclaimer",
    hasTrust: true,
    hasCreditShelter: true,    // available IF survivor disclaims
    clayton: false,
    maQtip: true,              // MA-only QTIP can apply to disclaimed share
    hasMinorChildren: true,
    hasRealEstate: true,
    hasLifeInsurance: true,
    hasPets: false,
    documents: [
      { name: "Joint Revocable Living Trust", category: "core", joint: true,
        displayName: "Joint Revocable Living Trust with Disclaimer Provisions",
        description: "A single joint trust. At the first death, the surviving spouse may disclaim assets into a credit shelter (bypass) trust within 9 months to preserve the first spouse's $2M Massachusetts exemption." },
      { name: "Pour-Over Will", category: "will", perSpouse: true },
      { name: "Durable General Power of Attorney", category: "incapacity", perSpouse: true },
      { name: "Health Care Proxy", category: "incapacity", perSpouse: true },
      { name: "HIPAA Authorization", category: "incapacity", perSpouse: true },
      { name: "Living Will (Advance Health Directive)", category: "incapacity", perSpouse: true },
      { name: "Assignment of Personal Property", category: "asset", perSpouse: true },
      { name: "Certificate of Trust", category: "asset", joint: true },
      { name: "Quitclaim Deed", category: "asset", joint: true },
      { name: "Parental Appointment of Guardian", category: "guardian", joint: true },
      { name: "Temporary Delegation of Parental Powers", category: "guardian", joint: true }
    ]
  },
  tax: {
    scenario1: { label: "Without Planning (no disclaimer made)",
      firstDeathTax: 0, firstDeathTaxDisplay: "$0",
      survivorEstate: 14391911, survivorEstateDisplay: "$14,391,911",
      adjustedTaxableEstate: 14331911,
      grossTax: 1769506, netTax: 1769506,
      secondDeathTax: 1769506, secondDeathTaxDisplay: "$1,769,506",
      totalTax: 1769506, totalTaxDisplay: "$1,769,506", totalTaxApprox: "$1.77 million" },
    scenario2: { label: "With Disclaimer (both $2M exemptions preserved; $4M sheltered)",
      firstDeathTax: 0, firstDeathTaxDisplay: "$0",
      survivorEstate: 10391911, survivorEstateDisplay: "$10,391,911",
      adjustedTaxableEstate: 10331911,
      grossTax: 1129506, netTax: 1129506,
      secondDeathTax: 1129506, secondDeathTaxDisplay: "$1,129,506",
      totalTax: 1129506, totalTaxDisplay: "$1,129,506", totalTaxApprox: "$1.13 million" },
    savings: 640000, savingsDisplay: "$640,000", savingsApprox: "$640,000",
    note: "Savings depend on the surviving spouse making a valid, timely disclaimer (within 9 months, without having accepted benefits). If the disclaimer is not made or is defective, the result reverts to Scenario 1. Figures are estimates pending attorney verification."
  },
  fiduciaries: {
    spouse1: { initialTrustee: "Matt (self)", successorTrustees: ["Julie", "[To be determined]"],
               personalRep: "Julie", poaPrimary: "Julie", poaSuccessor: "[To be determined]",
               hcpPrimary: "Julie", hcpSuccessor: "[To be determined]", guardian: "[To be determined]" },
    spouse2: { initialTrustee: "Julie (self)", successorTrustees: ["Matt", "[To be determined]"],
               personalRep: "Matt", poaPrimary: "Matt", poaSuccessor: "[To be determined]",
               hcpPrimary: "Matt", hcpSuccessor: "[To be determined]", guardian: "[To be determined]" },
    notes: [
      { label: "Disclaimer dependency", body: "Discuss with clients that this structure relies on the surviving spouse affirmatively disclaiming within 9 months; consider whether the separate-trust/Clayton structure is preferable for reliability." }
    ]
  },
  considerations: {
    realEstateTransfer: "Transfer the residence into the joint trust via quitclaim deed.",
    beneficiaryDesignations: "Review beneficiary designations to coordinate with the trust and the potential disclaimer trust.",
    lifeInsurance: "Existing $1,000,000 term policy; ILIT optional (see below).",
    ilit: "Optional ILIT to remove life insurance from the taxable estate; drafting-only, one-time first-year Crummey notices. New policy owned by the ILIT from inception avoids the IRC §2035 three-year lookback."
  },
  hasLegalPlan: false,
  flatFee: "$5,500"
};

/* =====================================================================
 * 3) SEPARATE REVOCABLE TRUSTS + CREDIT SHELTER + CLAYTON ELECTION
 * ===================================================================== */
const SAMPLE_SEPARATE_CLAYTON = {
  matter: {
    filePrefix: "SampleClayton",
    outputDir: "OUTPUTS/SampleClayton/Intake/",
    date: "June 15, 2026",
    attorney: "Scott Aubrey, Esq."
  },
  clients: {
    type: "couple",
    spouse1: { firstName: "Matt", lastName: "Sample", fullName: "Matt Sample",
               dob: "January 10, 1985", age: 41, citizen: true },
    spouse2: { firstName: "Julie", lastName: "Sample", fullName: "Julie Sample",
               dob: "February 22, 1986", age: 40, citizen: true },
    address: "19 Sample Ave, Needham, MA 02492",
    county: "Norfolk"
  },
  children: SAMPLE_CHILDREN,
  assets: {
    grossEstate: 14391911,
    grossEstateDisplay: "$14,391,911",
    grossEstateApprox: "$14.4 million",
    breakdown: SAMPLE_ASSET_BREAKDOWN
  },
  plan: {
    planStructure: "separate_clayton",
    hasTrust: true,
    hasCreditShelter: true,
    clayton: true,
    maQtip: true,
    hasMinorChildren: true,
    hasRealEstate: true,
    hasLifeInsurance: true,
    hasPets: false,
    documents: [
      { name: "Revocable Living Trust", category: "core", forSpouse: 1,
        displayName: "Matt Sample Revocable Trust",
        description: "Holds Matt's assets; includes credit shelter provisions and a Clayton election so his fiduciary can optimize the credit-shelter / marital (QTIP) division at the first death." },
      { name: "Revocable Living Trust", category: "core", forSpouse: 2,
        displayName: "Julie Sample Revocable Trust",
        description: "Mirror trust for Julie with the same credit shelter and Clayton-election provisions." },
      { name: "Pour-Over Will", category: "will", perSpouse: true },
      { name: "Durable General Power of Attorney", category: "incapacity", perSpouse: true },
      { name: "Health Care Proxy", category: "incapacity", perSpouse: true },
      { name: "HIPAA Authorization", category: "incapacity", perSpouse: true },
      { name: "Living Will (Advance Health Directive)", category: "incapacity", perSpouse: true },
      { name: "Assignment of Personal Property", category: "asset", perSpouse: true },
      { name: "Certificate of Trust", category: "asset", perSpouse: true },
      { name: "Quitclaim Deed", category: "asset", joint: true },
      { name: "Parental Appointment of Guardian", category: "guardian", joint: true },
      { name: "Temporary Delegation of Parental Powers", category: "guardian", joint: true }
    ]
  },
  tax: {
    scenario1: { label: "Without Planning",
      firstDeathTax: 0, firstDeathTaxDisplay: "$0",
      survivorEstate: 14391911, survivorEstateDisplay: "$14,391,911",
      adjustedTaxableEstate: 14331911,
      grossTax: 1769506, netTax: 1769506,
      secondDeathTax: 1769506, secondDeathTaxDisplay: "$1,769,506",
      totalTax: 1769506, totalTaxDisplay: "$1,769,506", totalTaxApprox: "$1.77 million" },
    scenario2: { label: "With Credit Shelter + Clayton Election (both $2M preserved; $4M sheltered)",
      firstDeathTax: 0, firstDeathTaxDisplay: "$0",
      survivorEstate: 10391911, survivorEstateDisplay: "$10,391,911",
      adjustedTaxableEstate: 10331911,
      grossTax: 1129506, netTax: 1129506,
      secondDeathTax: 1129506, secondDeathTaxDisplay: "$1,129,506",
      totalTax: 1129506, totalTaxDisplay: "$1,129,506", totalTaxApprox: "$1.13 million" },
    savings: 640000, savingsDisplay: "$640,000", savingsApprox: "$640,000",
    note: "The Clayton election is fiduciary-controlled (not survivor-dependent), and a Massachusetts state-only QTIP election can defer tax on the marital share. Coordinate the federal and MA elections deliberately (see Shaffer). Figures are estimates pending attorney verification."
  },
  fiduciaries: {
    spouse1: { initialTrustee: "Matt (self)", successorTrustees: ["Julie", "[To be determined]"],
               personalRep: "Julie", poaPrimary: "Julie", poaSuccessor: "[To be determined]",
               hcpPrimary: "Julie", hcpSuccessor: "[To be determined]", guardian: "[To be determined]" },
    spouse2: { initialTrustee: "Julie (self)", successorTrustees: ["Matt", "[To be determined]"],
               personalRep: "Matt", poaPrimary: "Matt", poaSuccessor: "[To be determined]",
               hcpPrimary: "Matt", hcpSuccessor: "[To be determined]", guardian: "[To be determined]" },
    notes: [
      { label: "Business interest", body: "Closely held / illiquid business interests require a successor trustee capable of overseeing them; review for out-of-state situs (2025 Mass. Acts Ch. 9, §35)." },
      { label: "Election coordination", body: "Document intended federal vs. MA-only QTIP elections; a federal QTIP pulls property into the survivor's MA estate at the second death (Shaffer, SJC-12812 (2020))." }
    ]
  },
  considerations: {
    realEstateTransfer: "Transfer the residence into the trusts via quitclaim deed.",
    beneficiaryDesignations: "Review and update beneficiary designations to coordinate with the trusts.",
    lifeInsurance: "Recommend ILIT(s); drafting-only, one-time first-year Crummey notices; new ILIT-owned policy from inception avoids the IRC §2035 three-year lookback.",
    ilit: "One ILIT for Matt now ($3,500), optional second ILIT for Julie concurrently ($2,500; reverts to $3,500 if deferred). Insurance procurement and ongoing annual Crummey notices excluded."
  },
  hasLegalPlan: false,
  flatFee: "$7,000"   // core plan; ILITs quoted separately as line items
};

/* =====================================================================
 * 4) INDIVIDUAL TRUST — SINGLE PERSON
 * ===================================================================== */
const SAMPLE_INDIVIDUAL_SINGLE = {
  matter: {
    filePrefix: "SampleSingle",
    outputDir: "OUTPUTS/SampleSingle/Intake/",
    date: "June 15, 2026",
    attorney: "Scott Aubrey, Esq."
  },
  clients: {
    type: "individual",
    spouse1: { firstName: "Denise", lastName: "Sample", fullName: "Denise Sample",
               dob: "March 3, 1968", age: 58, citizen: true },
    spouse2: null,                 // individual — no spouse stub
    address: "42 Single Lane, Needham, MA 02492",
    county: "Norfolk"
  },
  children: [
    { name: "Ava Sample", dob: "September 1, 2004", age: 21, isMinor: false, relationship: "Daughter" }
  ],
  assets: {
    grossEstate: 4250000,
    grossEstateDisplay: "$4,250,000",
    grossEstateApprox: "$4.25 million",
    breakdown: [
      { category: "Real Estate (primary residence, net of mortgage)", value: 1100000, display: "$1,100,000" },
      { category: "Bank Accounts",                                    value: 150000,  display: "$150,000" },
      { category: "Retirement Accounts",                              value: 1300000, display: "$1,300,000" },
      { category: "Brokerage / Investment Accounts",                  value: 1500000, display: "$1,500,000" },
      { category: "Vehicles",                                         value: 200000,  display: "$200,000" }
    ]
  },
  plan: {
    planStructure: "individual_single",
    hasTrust: true,
    hasCreditShelter: false,   // requires a spouse — N/A
    clayton: false,
    maQtip: false,
    hasMinorChildren: false,
    hasRealEstate: true,
    hasLifeInsurance: false,
    hasPets: false,
    documents: [
      { name: "Revocable Living Trust", category: "core",
        displayName: "Denise Sample Revocable Trust",
        description: "Holds and manages Denise's assets during her lifetime, avoids probate, and controls distribution at death. No marital or credit shelter provisions (single person)." },
      { name: "Pour-Over Will", category: "will" },
      { name: "Durable General Power of Attorney", category: "incapacity" },
      { name: "Health Care Proxy", category: "incapacity" },
      { name: "HIPAA Authorization", category: "incapacity" },
      { name: "Living Will (Advance Health Directive)", category: "incapacity" },
      { name: "Assignment of Personal Property", category: "asset" },
      { name: "Certificate of Trust", category: "asset" },
      { name: "Quitclaim Deed", category: "asset" }
    ]
  },
  tax: {
    // Single scenario only — tax at the individual's death.
    scenario1: { label: "At Death (single individual; one $2M exemption)",
      firstDeathTax: null,
      survivorEstate: null,
      adjustedTaxableEstate: 4190000,
      grossTax: 306800, netTax: 306800,
      secondDeathTax: null,
      totalTax: 306800, totalTaxDisplay: "$306,800", totalTaxApprox: "$307,000" },
    scenario2: null,            // not applicable for an individual
    savings: 0, savingsDisplay: "$0",
    note: "Credit shelter / Clayton / QTIP planning requires a spouse and does not apply. The worksheet still shows the computation so the individual's MA exposure and strategies (gifting, charitable, ILIT) can be discussed. Figures are estimates pending attorney verification."
  },
  fiduciaries: {
    spouse1: { initialTrustee: "Denise (self)", successorTrustees: ["Ava Sample", "[To be determined]"],
               personalRep: "[To be determined]", poaPrimary: "[To be determined]", poaSuccessor: "[To be determined]",
               hcpPrimary: "[To be determined]", hcpSuccessor: "[To be determined]", guardian: null },
    spouse2: null,
    notes: [ { label: "Single-person fiduciaries", body: "Naming reliable successor trustees and agents is critical for a single client; finalize at the design meeting." } ]
  },
  considerations: {
    realEstateTransfer: "Transfer the residence into the trust via quitclaim deed.",
    beneficiaryDesignations: "Review beneficiary designations on retirement accounts to coordinate with the trust.",
    youngAdultPlans: { name: "Ava Sample", age: 21, school: "[school if known]" },
    ilit: null
  },
  hasLegalPlan: false,
  flatFee: "$4,000"
};

module.exports = {
  SAMPLE_JOINT_OUTRIGHT,
  SAMPLE_JOINT_DISCLAIMER,
  SAMPLE_SEPARATE_CLAYTON,
  SAMPLE_INDIVIDUAL_SINGLE
};
