# Fundamental engine v0.8

The engine converts a canonical CVM accounting snapshot plus shares, market price and payout assumptions into the indicators used by the Excel methodology.

## Rules
- LPA = attributable net income / applicable shares.
- VPA = equity attributable to common shareholders / applicable shares.
- DPA = LPA × expected payout.
- 5-year CAGR is only emitted when valid positive endpoints are exactly five years apart.
- Graham, Bazin, Gordon and projective ceilings use the methodology parameters supplied to the calculation.
- Banks/financial institutions do not receive a Debt/EBITDA score; the field is explicitly not applicable rather than zero debt.
- Missing shares prevent LPA/VPA instead of silently substituting a denominator.
- Quality flags are preserved with the calculation output.

## Important limitation
Shares are deliberately supplied as an explicit input in v0.8. The next ingestion milestone will populate the applicable share count from official CVM/FCA/capital-structure data and corporate-action adjustments.
