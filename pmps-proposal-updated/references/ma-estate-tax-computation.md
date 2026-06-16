# Massachusetts Estate Tax Computation Reference

## Overview

Massachusetts imposes an estate tax using the former IRC §2011 credit for state death taxes table (as in effect December 31, 2000). The key rules:

1. **Exemption**: $2,000,000 per person. If gross estate ≤ $2M, no tax.
2. **Cliff effect**: If over $2M, the **entire estate** is taxed — there is no subtraction of the $2M.
3. **Adjusted taxable estate** = taxable estate − $60,000 (statutory adjustment).
4. **No portability**: Massachusetts does NOT allow spouses to share unused exemptions. Each spouse's $2M exemption is "use it or lose it."
5. **Unified credit**: $99,600 — offsets tax on exactly $2M (so a $2M estate pays $0).
6. **Credit shelter trust**: The only way to preserve the first-to-die's exemption is by funding a bypass trust at death.

## Rate Table (21 Brackets)

| Floor | Ceiling | Base Tax | Rate |
|-------|---------|----------|------|
| $0 | $40,000 | $0 | 0.0% |
| $40,000 | $90,000 | $0 | 0.8% |
| $90,000 | $140,000 | $400 | 1.6% |
| $140,000 | $240,000 | $1,200 | 2.4% |
| $240,000 | $440,000 | $3,600 | 3.2% |
| $440,000 | $640,000 | $10,000 | 4.0% |
| $640,000 | $840,000 | $18,000 | 4.8% |
| $840,000 | $1,040,000 | $27,600 | 5.6% |
| $1,040,000 | $1,540,000 | $38,800 | 6.4% |
| $1,540,000 | $2,040,000 | $70,800 | 7.2% |
| $2,040,000 | $2,540,000 | $106,800 | 8.0% |
| $2,540,000 | $3,040,000 | $146,800 | 8.8% |
| $3,040,000 | $3,540,000 | $190,800 | 9.6% |
| $3,540,000 | $4,040,000 | $238,800 | 10.4% |
| $4,040,000 | $5,040,000 | $290,800 | 11.2% |
| $5,040,000 | $6,040,000 | $402,800 | 12.0% |
| $6,040,000 | $7,040,000 | $522,800 | 12.8% |
| $7,040,000 | $8,040,000 | $650,800 | 13.6% |
| $8,040,000 | $9,040,000 | $786,800 | 14.4% |
| $9,040,000 | $10,040,000 | $930,800 | 15.2% |
| $10,040,000 | ∞ | $1,082,800 | 16.0% |

## Computation Algorithm

### For a given taxable estate amount:

```
function computeMATax(taxableEstate):
    if taxableEstate <= 2,000,000:
        return { netTax: 0 }
    
    adjustedTaxableEstate = taxableEstate - 60,000
    
    Find the bracket where: floor <= adjustedTaxableEstate < ceiling
    
    excess = adjustedTaxableEstate - bracket.floor
    taxOnExcess = excess * bracket.rate
    grossTax = bracket.baseTax + taxOnExcess
    netTax = grossTax - 99,600  (unified credit)
    
    return { adjustedTaxableEstate, bracket, excess, taxOnExcess, grossTax, netTax }
```

### Scenario 1: Without Planning (couple)

All assets pass to surviving spouse at first death (unlimited marital deduction = $0 tax). At second death, the full combined estate is taxed. First spouse's $2M exemption is wasted.

- taxableEstate = grossEstate (full combined value)
- Compute tax on full amount

### Scenario 2: With Credit Shelter Planning (couple)

At first death, $2M goes to bypass trust (uses first spouse's exemption). Remainder goes to surviving spouse.

**First death:**
- taxableEstate = $2,000,000 (bypass amount)
- grossTax = $99,600 (exactly equals unified credit)
- netTax = $0

**Second death:**
- taxableEstate = grossEstate − $2,000,000 (bypass amount already sheltered)
- Compute tax on this reduced amount

**Savings** = Scenario 1 netTax − Scenario 2 total netTax

### Individual (no spouse)

Only Scenario 1 applies — compute tax on the full estate. Scenario 2 (credit shelter) is not applicable. Set savings to $0 and note that credit shelter planning requires a spouse.
