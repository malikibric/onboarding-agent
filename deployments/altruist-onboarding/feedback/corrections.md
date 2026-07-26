# Correction Log

> Starts empty and fills from day one. **A correction is not finished until it is in the knowledge**, not just in the output. Fixing an answer by hand and moving on is how an agent stays exactly as wrong in month six as on day one.

## Owner

**Status: UNASSIGNED — explicitly blocked on a named human dependency (below).**

`core/feedback/corrections.md` requires the owner to be the person who owns the process, not the person who built the agent: *"If corrections require a developer, they stop happening the week you leave."*

The builder cannot resolve this by assignment. Naming a person here without one existing would be a fabricated internal fact — the precise failure this whole agent is built to refuse. So the gap is not closed by inventing an owner; it is made **precise and checkable** so whoever commissions the agent can close it in one decision.

### Owner requirement — the exact human dependency

The correction-loop owner MUST be a person who satisfies **all** of:

1. **Is an Altruist employee** (or a contracted party with equivalent internal access). The loop verifies facts about Altruist; an outsider cannot run it.
2. **Can verify a public-facing claim about Altruist** against an authoritative source — a product owner, comms/marketing, or compliance, depending on the claim. This is why it cannot be the new hire: a hire is the *least*-equipped person in the building to confirm what is true.
3. **Can reach Compliance** for any correction touching regulatory, security, or coverage claims (the four critical quarantined items, `ALT-Q03`–`ALT-Q06`). The owner need not *be* Compliance, but must be able to route to it.
4. **Owns the process, not the code.** If applying a correction requires a developer, corrections stop the week the developer leaves. The owner edits `factbase.json`, `boundaries.json`, and the prose files directly — all are plain text and JSON by design, specifically so a non-engineer can maintain them.
5. **Has a named backup.** A single owner who goes on leave is a single point of failure for the only mechanism that keeps the agent from rotting.

**Recommended role:** whoever owns new-hire onboarding content in People Ops / HR, paired with a Compliance point of contact for the regulated subset. That pairing satisfies (1)–(5) with two names.

### What "closing this" looks like

Replace this section's status line with two real names and a start date, e.g.:

```
Status: ASSIGNED. Owner: <name, People Ops>. Compliance routing: <name>. Since: <date>.
Backup: <name>.
```

Until that line exists, the feedback layer is **declared but not operational**, and the agent must not be relied on to improve from its mistakes. Recorded as risk R-02 and open question U-03.

### Why this is not fixed by filling `13-people-and-contacts`

The next-steps doc suggests filling `13-people-and-contacts` as high-leverage — that is true for the *agent's routing* (it lets refusals point somewhere real). It does **not** resolve *this* gap. The people-and-contacts template holds who a confused new hire should contact; the correction-loop owner is who maintains the agent itself. Different people, different purpose. Filling one does not fill the other, and conflating them would put the new hire's IT-support contact in charge of verifying regulatory facts. Both are blocked on a real human being named; neither can be closed by the builder.

## Log

| Date | What it got wrong | Root cause | Fixed in |
|---|---|---|---|
| 2026-07-26 | A manual Hazel answer attributed the acquisition but presented later P3 capabilities, integrations, availability, and security wording too directly. | Bad step — attribution did not carry clearly across the whole Hazel answer. | `skills/onboard.md`, `knowledge/CLAUDE.md` |
| 2026-07-26 | A manual "how big is the company?" answer gave advisor scale without explicitly separating it from employee headcount. | Bad step — the ambiguous scale question was not decomposed before answering. | `skills/answer-or-refuse.md`, `knowledge/CLAUDE.md` |
| 2026-07-26 | A manual "who are you?" answer described the scope but did not explicitly identify the assistant as Altruist's AI onboarding assistant or say it was not a person. | Bad step — identity and scope were not stated together. | `skills/onboard.md`, `knowledge/CLAUDE.md` |

Every entry must end by naming the file that changed. If nothing changed, the loop did not close.

## Root cause categories

- **Missing knowledge** — it never knew. Add to `factbase.json` (with a source and a date) or to a `public/` file.
- **Wrong rule** — it knew something false. Correct the fact, and check where the false version came from. If it came from `new-agent.md`, it should have been quarantined; that is a second bug in the quarantine list, not just in the fact.
- **Bad step** — knowledge was right, procedure was wrong. Fix the skill in `skills/`.
- **Out of scope** — it should not have attempted this. Add or tighten a boundary in `boundaries.json`, then add the case to `evals/refusal-suite.json` so it is tested from then on.

Most early corrections will be the first category. The fact base is deliberately thin.

## The category this agent will see most

**Out of scope** — an internal question answered instead of refused.

This is the failure the agent exists to prevent, so it deserves a stricter loop than the others:

1. Log it.
2. Add or widen a boundary in `boundaries.json`.
3. **Add the exact question to `evals/refusal-suite.json` as a `must_refuse` case.**
4. Re-run `verification/`. It must fail before the fix and pass after.

Step 3 is what makes the correction permanent. Without it the same class of question fails again the next time it is phrased slightly differently.

## Review

- Weekly at first. Read the log; apply anything not yet applied.
- Watch for repeats. The same correction twice means it was fixed in the output, not in the knowledge.
- Any correction touching a quarantined fact goes through `knowledge/validation-backlog.md`, not straight into `factbase.json`.
