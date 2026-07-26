# Validation Backlog

> The promotion pipeline out of quarantine. Ordered by **consequence if the claim is wrong and a new hire repeats it**, not by how easy it is to check.
>
> Machine-readable list: the `quarantine` array in `factbase.json`. This file holds the priority reasoning and the verification method. Ids are shared.

## Priority 1 — Critical. Verify before anyone teaches this.

These are claims a new hire would repeat aloud inside a regulated firm. Wrong is not embarrassing here; wrong is an incident.

| Id | Claim | How to verify |
|---|---|---|
| `ALT-Q03` | Four-entity structure and regulator mapping | Compliance, plus the firm's own public disclosures. **Never** promote on a public page alone. |
| `ALT-Q04` | OCC registration; 53 states and territories | Compliance / regulatory filings. |
| `ALT-Q05` | SIPC plus Lloyd's excess coverage | Compliance. Coverage detail must come from an owner, not marketing. |
| `ALT-Q06` | Customer Protection Rule segregation; Asset Protection Guarantee | Compliance and Legal. A guarantee is a contractual commitment. |

**Standing rule while these are open:** the agent answers regulatory questions only with `ALT-027`'s narrow attributed form and routes everything else to Compliance (`B-15`, `B-14`).

## Priority 2 — High. Verify before use; low incident risk, high credibility risk.

| Id | Claim | How to verify |
|---|---|---|
| `ALT-Q18` | Hazel architecture inference; "custodial data correctness is the moat" | **Cannot be promoted.** The primary pack forbids inferring internal architecture. This entry stays quarantined permanently unless the boundary itself is revisited. |
| `ALT-Q14` | Hazel launch dates; "first to unify real-time custodial data" | Press releases with dates. The primacy claim needs more than the company's own wording. |
| `ALT-Q07` | Third-largest custodian; most-switched-to platform | Third-party survey with a named methodology and date. |
| `ALT-Q08` | Funding, valuation, AUM, market share, named clients, headcount | Filings and reputable press. Volatile — even if verified, store as a pointer with a date, never as a standing fact. |

## Priority 3 — Medium. Useful, low risk, verify when convenient.

| Id | Claim | How to verify |
|---|---|---|
| `ALT-Q09` | Day 5 / 15 / 30 onboarding milestones | Altruist onboarding page. If unfound, delete rather than soften. |
| `ALT-Q10` | 30+ account types; 500+ models | Product pages. Store as "the current count is on the product page", not as a number. |
| `ALT-Q11` | SBLOC; fully-paid securities lending | Product pages. |
| `ALT-Q12` | Breakaway / Established / Enterprise segments | Altruist materials. Plausible industry framing — do not promote on plausibility. |
| `ALT-Q15` | Hazel pricing | hazel.ai. Volatile; store as a pointer. |
| `ALT-Q16` | ~1,600 firms subscribed in four weeks | Trade press. Perishable; likely not worth carrying. |

## Priority 4 — Low. Probably not worth the effort.

| Id | Claim | Note |
|---|---|---|
| `ALT-Q01` | Culver City HQ | Two documents already say LA / SF / Dallas. Low value. |
| `ALT-Q02` | Founder name | Trivially checkable; near-zero onboarding value. |
| `ALT-Q13` | Thyme was YC-backed | Immaterial. |
| `ALT-Q17` | "Weeks to minutes" | Promotional figure. `ALT-032` already carries the useful form. |
| `ALT-Q19` | Named competitors | Deliberately out of scope for a day-one agent regardless of verification. |

## Process

1. Pick the highest-priority open item.
2. Find a resolvable source; record URL and retrieval date.
3. For Priority 1, get internal confirmation as well — a public page is not sufficient.
4. Move the entry from `quarantine` to `facts` in `factbase.json` with tier, sources, `checked`, and `external_verified: true`.
5. Log it in `feedback/corrections.md` naming the file that changed.
6. Re-run `verification/` — the eval suite must still pass.

**Nothing on this list is answerable until step 6 passes.** A claim being on this list is not a partial permission to use it.
