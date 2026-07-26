# Enforcement

Boundaries that hold regardless of what the model decides.

## The distinction that matters

Writing "never send without approval" in a prompt is not enforcement. It's a request. The model will usually comply, and "usually" isn't a control.

**Test: if the agent can be talked out of it, it isn't enforcement.**

Real enforcement lives outside the model:

| Prompt (a request) | Enforcement (structural) |
|---|---|
| "Never send without approval" | No credential to send. It can't. |
| "Always include the expiry date" | Validator rejects output missing it |
| "Don't quote outside the territory" | Check runs against the order before it can leave |
| "Escalate deals over $50k" | Value check halts the run |

## The four kinds

1. **Absence of access** — strongest. Covered in `tools/access-policy.md`. What it can't reach, it can't break.
2. **Validation** — output checked against rules before release. `validate.py` here.
3. **Approval gates** — a human clicks. Use for anything irreversible or leaving the company.
4. **Audit trail** — doesn't prevent anything, but makes failure visible fast. Log what ran, on what, with what result.

## Gates for this deployment

| # | Rule | Enforced by | Blocks or warns |
|---|---|---|---|
| 1 | | validate.py / access / approval | block |
| 2 | | | |

Blocking rules should be few and genuinely absolute. If everything blocks, people route around the system and you've enforced nothing.

## Running it

```
python enforcement/validate.py <output-file> --rules enforcement/rules.json
```

Exit 0 = passes. Exit 1 = blocked, with reasons. Wire it in as a pre-send step so nothing reaches a customer unchecked.

## What this layer can't do

Enforcement catches rule violations, not bad judgment. It'll stop a quote missing an expiry date; it won't stop a quote that's technically valid and commercially stupid. That's what escalation thresholds and human review are for.

Don't let a passing validator become a reason to stop reading the output.
