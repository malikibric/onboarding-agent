# [Company] — [Domain] Agent Knowledge

> Dedicated knowledge layer. Last updated: [date]. Source material: [what this was built from].
> Confidence tags: untagged = verified from source · `[ASSUMED]` = inferred, needs confirmation · `[MISSING]` = required and not yet known.

---

## 1. What this company does

[Two to four sentences. What they sell, to whom, how revenue works. Enough context for the agent to understand what is at stake in its work. Not marketing copy.]

## 2. Vocabulary

| Term | Means | Not to be confused with |
|---|---|---|
| | | |

[Every internal term, code, abbreviation, and system nickname. Err heavily toward including too much.]

## 3. People and authority

**Roles and decision rights**

| Decision | Who decides | Threshold / condition |
|---|---|---|

**Routing** — [which kinds of question go to which role]

[Where current names live: point to the system rather than hardcoding, unless the roster is genuinely stable.]

## 4. Products and services

[Catalog structure and the logic underneath it — how items are grouped, coded, bundled, substituted. The pattern, not a full dump. Point to the live catalog for current items and prices.]

## 5. Customers and segments

| Segment | Definition | What changes operationally |
|---|---|---|

[Only segments that actually drive different behaviour.]

## 6. The process this agent owns

**Scope:** [one sentence — where this process starts and stops]

**Step 1 — [name]**
- Trigger:
- Action:
- Done when:
- Hands off to:

[Repeat per step. Encode the real process, noting where it diverges from the documented one. If this file is deployed alongside a separate skills layer, keep this section to scope, triggers, and handoffs and put the step-by-step procedure in the skill file — the same steps in two places will drift.]

## 7. Decision rules

- If [condition], then [action].
- If [condition], then [action], unless [exception], in which case [action].

[Every threshold and branch point, stated so it can be executed rather than interpreted.]

## 8. Sources of truth

| Fact type | Authoritative system | Notes / conflict resolution |
|---|---|---|

[Where two systems disagree, state explicitly which wins.]

## 9. Output standards

**Format rules:** [naming conventions, numbering, required fields, subject line patterns]

**Worked example — [artifact type]**

```
[A real, approved output pasted verbatim. This teaches more than any description of tone.]
```

[One example per artifact type the agent produces.]

## 10. Hard constraints — never do

- Never [absolute prohibition].
- Never [absolute prohibition].

[No hedging, no interpretive room. Regulatory limits, commitments the agent cannot make, data it cannot expose, claims it cannot state.]

## 11. Escalate to a human when

- [Specific condition — value threshold, unrecognised entity, conflicting data, irreversible action, external commitment]

[Each entry must have a checkable trigger. "When unsure" is not a trigger.]

## 12. Open questions

Prioritized by consequence if the gap goes unfilled.

1. **[Question]** — needed for: [what breaks without it]. Ask: [who].
2. **[Question]** — needed for: [what breaks without it]. Ask: [who].

---

*Assumptions in this file are tagged `[ASSUMED]` and should be confirmed or corrected by someone who owns the process. Every correction made here compounds — it improves this agent and every agent built on this knowledge afterward.*
