/* =====================================================================
 * pmps-prep — EMPTY data template (with planStructure fields)
 * ---------------------------------------------------------------------
 * Blank scaffold matching the four-structure schema. Paste into
 * Templates/pmps-data-schema.js as the EMPTY object, then reconcile
 * field names against the real schema before relying on it.
 *
 * Fill every value. Leave `null` where genuinely not applicable
 * (e.g., spouse2 for an individual). Do NOT guess legal figures —
 * use [VERIFY: ...] flags per the skill's guardrails.
 *
 * planStructure controls branching:
 *   "joint_outright" | "joint_disclaimer" | "separate_clayton" | "individual_single"
 * ===================================================================== */

const EMPTY = {
  matter: {
    filePrefix: "",            // client last name(s), e.g. "Smith" or "Miller-Bethlehem"
    outputDir: "",             // matter Intake folder, e.g. "OUTPUTS/Smith/Intake/"
    date: "",                  // e.g. "June 15, 2026"
    attorney: "Scott Aubrey, Esq."
  },

  clients: {
    type: "",                  // "couple" | "individual"
    spouse1: {                 // for an individual, this holds the single client
      firstName: "", lastName: "", fullName: "",
      dob: "", age: null, citizen: null   // citizen: true/false
    },
    spouse2: null,             // couple: {firstName,...}; individual: null
    address: "",
    county: ""                 // e.g. "Norfolk" — drives deed-recording references
  },

  children: [
    // { name: "", dob: "", age: null, isMinor: null, relationship: "" }
  ],

  assets: {
    grossEstate: null,         // raw number
    grossEstateDisplay: "",    // "$0"
    grossEstateApprox: "",     // "$0 million"
    breakdown: [
      // { category: "", value: null, display: "" }
    ]
  },

  plan: {
    planStructure: "",         // REQUIRED — one of the four values above
    hasTrust: null,
    hasCreditShelter: null,    // false for joint_outright and individual_single
    clayton: null,             // true only for separate_clayton
    maQtip: null,              // true for joint_disclaimer and separate_clayton
    hasMinorChildren: null,
    hasRealEstate: null,
    hasLifeInsurance: null,
    hasPets: null,
    documents: [
      // Couple per-spouse doc:   { name: "", category: "", perSpouse: true }
      // Couple joint doc:        { name: "", category: "", joint: true }
      // Spouse-specific trust:   { name: "Revocable Living Trust", category: "core", forSpouse: 1, displayName: "", description: "" }
      // Individual doc:          { name: "", category: "" }
      // categories: "core" | "will" | "incapacity" | "asset" | "guardian"
    ]
  },

  tax: {
    // scenario1 is always the live/baseline result.
    scenario1: {
      label: "",
      firstDeathTax: null, firstDeathTaxDisplay: "",   // null for individual
      survivorEstate: null, survivorEstateDisplay: "", // null for individual
      adjustedTaxableEstate: null,
      grossTax: null, netTax: null,
      secondDeathTax: null, secondDeathTaxDisplay: "", // null for individual
      totalTax: null, totalTaxDisplay: "", totalTaxApprox: ""
    },
    // scenario2: "both $2M preserved; $4M sheltered" for joint_disclaimer / separate_clayton.
    // Set to null for joint_outright and individual_single.
    scenario2: null,
    savings: 0, savingsDisplay: "$0", savingsApprox: "",
    note: ""                   // structure-specific caveat; mark figures as estimates pending verification
  },

  fiduciaries: {
    spouse1: {
      initialTrustee: "", successorTrustees: [],
      personalRep: "", poaPrimary: "", poaSuccessor: "",
      hcpPrimary: "", hcpSuccessor: "", guardian: ""    // guardian null if no minor children
    },
    spouse2: null,             // couple: {...}; individual: null
    notes: [
      // "string" OR { label: "", body: "" }
    ]
  },

  considerations: {
    ilit: null,                // string when recommended; drafting-only framing
    gifting: null,
    beneficiaryDesignations: null,
    anticipatedInheritance: null,
    realEstateTransfer: null,
    lifeInsurance: null,
    youngAdultPlans: null,     // { name: "", age: null, school: "" } for 18+ children
    pets: null, petName: null
  },

  hasLegalPlan: null,          // true => legalPlan block drives pricing; false => flatFee
  flatFee: "",                 // e.g. "$7,000" (core plan) when no legal plan
  legalPlan: {                 // populate only when hasLegalPlan is true
    name: "",                  // "MetLife" | "LegalEASE" | "ARAG" | "Hyatt" | "LegalShield"
    covered: [],               // ["string", ...]
    notCovered: [],            // ["string", ...]
    optionalServices: []       // [{ name, description, fee, status }]
  }
};

module.exports = { EMPTY };
