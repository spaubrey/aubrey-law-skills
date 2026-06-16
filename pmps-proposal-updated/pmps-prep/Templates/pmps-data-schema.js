/**
 * pmps-data-schema.js
 * Full data schema definition for all PMPS templates.
 * Copy and populate this object, then pass to each template function.
 *
 * Usage:
 *   const schema = require('./pmps-data-schema');
 *   // Inspect schema.SAMPLE for a fully-populated example
 *   // Inspect schema.EMPTY for a blank template
 */

'use strict';

const SAMPLE = {
  matter: {
    date: "May 2, 2026",          // Display date string
    filePrefix: "Smith",           // Prefix for output filenames (e.g. "Smith" → Smith_Agenda.docx)
    outputDir: "/path/to/OUTPUTS/Smith_PMPS/"  // Absolute path; must already exist
  },

  clients: {
    type: "couple",               // "couple" | "individual"
    spouse1: {
      firstName: "David",
      lastName: "Chen",
      fullName: "David Chen",
      dob: "March 15, 1975",      // Display string; optional
      age: 51,
      citizenship: "US"
    },
    spouse2: {                    // SET TO null FOR INDIVIDUAL CLIENTS
      firstName: "Maria",
      lastName: "Santos-Chen",
      fullName: "Maria Santos-Chen",
      dob: "August 22, 1978",
      age: 47,
      citizenship: "US"
    },
    address: "45 Maple Street, Wellesley, MA 02481",
    county: "Norfolk County",
    marriedSince: "June 2005"     // optional; display string
  },

  children: [
    // Each child: { name, dob (optional), age, isMinor }
    { name: "Sophia Chen", dob: "January 10, 2012", age: 14, isMinor: true },
    { name: "Lucas Chen",  dob: "May 3, 2016",       age: 9,  isMinor: true }
  ],

  hasMinorChildren: true,
  hasLegalPlan: false,            // true = MetLife/ARAG; false = flat fee
  legalPlan: null,                // if hasLegalPlan: { name: "MetLife", type: "MetLife Legal Plans" }
  flatFee: "$4,500",              // if !hasLegalPlan: fee for the plan (ask Scott if unknown)

  hasTrust: true,
  hasCreditShelter: true,         // couples only; false for individuals
  hasRealEstate: true,
  hasLifeInsurance: true,
  hasAnticipatedInheritance: true,
  hasPets: true,

  assets: {
    grossEstate: 4300000,
    grossEstateDisplay: "$4,300,000",
    grossEstateApprox: "$4.3 million",
    breakdown: [
      // Each item: { category, value, display }
      { category: "Primary Residence (net of mortgage)", value: 1520000, display: "$1,520,000" },
      { category: "401(k) — David",                      value: 850000,  display: "$850,000"   },
      { category: "Brokerage Account",                    value: 620000,  display: "$620,000"   },
      { category: "Savings",                              value: 95000,   display: "$95,000"    },
      { category: "Life Insurance (face value)",          value: 500000,  display: "$500,000"   }
    ]
  },

  tax: {
    // Couples: both scenario1 and scenario2
    // Individuals: scenario1 only; set scenario2 = null, savings = 0
    scenario1: {
      label: "Without Planning",
      taxableEstate: 4300000,
      adjustedTaxableEstate: 4240000,   // taxableEstate - 60000
      bracketFloor: 4040000,
      bracketCeiling: 5040000,
      bracketRate: 0.112,               // as decimal
      baseTax: 290800,
      excess: 200000,                   // adjustedTaxableEstate - bracketFloor
      taxOnExcess: 22400,               // excess * bracketRate
      grossTax: 313200,                 // baseTax + taxOnExcess
      unifiedCredit: 99600,
      netTax: 213600,                   // grossTax - unifiedCredit
      netTaxDisplay: "$213,600",
      netTaxApprox: "~$214,000"
    },
    scenario2: {                        // null for individuals
      label: "With Credit Shelter Trust",
      firstDeath: {
        bypassAmount: 2000000,
        grossTax: 99600,
        credit: 99600,
        netTax: 0
      },
      secondDeath: {
        taxableEstate: 2300000,         // grossEstate - bypassAmount
        adjustedTaxableEstate: 2240000,
        bracketFloor: 2040000,
        bracketCeiling: 2540000,
        bracketRate: 0.08,
        baseTax: 106800,
        excess: 200000,
        taxOnExcess: 16000,
        grossTax: 122800,
        unifiedCredit: 99600,
        netTax: 23200
      },
      totalNetTax: 23200,               // firstDeath.netTax + secondDeath.netTax
      netTaxDisplay: "$23,200",
      netTaxApprox: "~$23,000"
    },
    savings: 190400,                    // scenario1.netTax - scenario2.totalNetTax; 0 for individuals
    savingsDisplay: "$190,400",
    savingsApprox: "~$190,000"
  },

  plan: {
    type: "Trust-Based with Credit Shelter",  // Display string for plan type
    documents: [
      // Each document: { name, joint (bool), perSpouse (bool) }
      // joint=true → one copy labeled "Joint"
      // perSpouse=true + couple → two copies, one per spouse
      // perSpouse=true + individual → one copy
      { name: "Joint Revocable Living Trust (with Credit Shelter)", joint: true,  perSpouse: false },
      { name: "Pour-Over Will",                                      joint: false, perSpouse: true  },
      { name: "Durable Power of Attorney",                           joint: false, perSpouse: true  },
      { name: "Health Care Proxy",                                   joint: false, perSpouse: true  },
      { name: "HIPAA Authorization",                                 joint: false, perSpouse: true  },
      { name: "Advance Health Directive (Living Will)",              joint: false, perSpouse: true  }
    ]
  },

  fiduciaries: {
    // For couples: both spouse1 and spouse2
    // For individuals: spouse1 = the client's appointments; spouse2 = null
    notes: null,   // optional: string note (e.g. non-resident fiduciary warning)
    spouse1: {
      trustee:       "Maria Santos-Chen, then Ana Santos, then James Chen",
      personalRep:   "Maria Santos-Chen, then Ana Santos",
      poaAgent:      "Maria Santos-Chen, then James Chen",
      hcpAgent:      "Maria Santos-Chen, then James Chen",
      guardian:      "Ana Santos (primary), James Chen (backup)"   // omit if no minor children
    },
    spouse2: {      // null for individual clients
      trustee:       "David Chen, then Ana Santos, then James Chen",
      personalRep:   "David Chen, then Ana Santos",
      poaAgent:      "David Chen, then Ana Santos",
      hcpAgent:      "David Chen, then Ana Santos",
      guardian:      "Ana Santos (primary), James Chen (backup)"
    }
  },

  considerations: {
    // All optional; set to null or omit if not applicable
    pets:                 "Golden retriever named Bear — discuss pet trust provisions.",
    lifeInsurance:        "David's $500K term policy (Northwestern Mutual) — consider ILIT to remove from taxable estate.",
    anticipatedInheritance: "Maria's mother may leave ~$400K — discuss estate growth implications.",
    realEstateTransfer:   "Primary residence to be transferred into trust via quitclaim deed ($350 + $280 recording fee).",
    beneficiaryDesignations: "Review 401(k) beneficiary designations to align with trust plan.",
    youngAdultPlans:      null,  // { name, age, school } if any child is 18+
    ilit:                 true,  // flag: recommend ILIT discussion
    gifting:              false  // flag: recommend gifting discussion
  },

  flags: []   // Additional attorney flags; array of strings displayed in Agenda flags section
};

const EMPTY = {
  matter: { date: null, filePrefix: null, outputDir: null },
  clients: {
    type: null,
    spouse1: { firstName: null, lastName: null, fullName: null, dob: null, age: null, citizenship: null },
    spouse2: null,
    address: null, county: null, marriedSince: null
  },
  children: [],
  hasMinorChildren: false,
  hasLegalPlan: null, legalPlan: null, flatFee: null,
  hasTrust: null, hasCreditShelter: null, hasRealEstate: null,
  hasLifeInsurance: null, hasAnticipatedInheritance: null, hasPets: null,
  assets: { grossEstate: null, grossEstateDisplay: null, grossEstateApprox: null, breakdown: [] },
  tax: { scenario1: null, scenario2: null, savings: 0, savingsDisplay: "$0", savingsApprox: "$0" },
  plan: { type: null, documents: [] },
  fiduciaries: { notes: null, spouse1: null, spouse2: null },
  considerations: { pets: null, lifeInsurance: null, anticipatedInheritance: null,
    realEstateTransfer: null, beneficiaryDesignations: null,
    youngAdultPlans: null, ilit: false, gifting: false },
  flags: []
};

module.exports = { SAMPLE, EMPTY };
