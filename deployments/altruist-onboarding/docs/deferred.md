# Deferred

What was not built, why, and the condition that would unblock it. Each has a written gate — "later" without a gate is how deferred work becomes permanently forgotten or silently re-added.

---

## DF-01 — Curriculum (day 1 / 30 / 60 / 90)
**Gate:** verified role-specific content exists (DF-02) **and** an answer to U-01 (a curriculum implies persistence).
**Why deferred.** The old plan's four-week curriculum is mostly structure — the clock and the sequencing are reasonable. The *content* for weeks 2–4 requires knowledge of Altruist's actual products, workflows, and failure modes at a depth the fact base does not have. Building it now would fill four weeks with industry-generic material presented as Altruist onboarding.
**What is reusable.** The clock keyed to start date, and the week-1 shape. Not the milestone claims ("Day 30: sit in a cross-functional meeting and ask a question that moves it forward") which are unmeasurable.

## DF-02 — Role-specific branches
**Gate:** `knowledge/internal/15-role-specific-ramps.TEMPLATE.md` filled by someone internal.
**Why deferred.** With the template empty, role branches could only be generic engineering/ops/support advice presented as Altruist expectations. `onboard.md` still asks the role once, which is a judgment call flagged in that file — if it starts creating an expectation the agent cannot meet, cut the question.

## DF-03 — Stakeholder role-play
**Gate:** internal norms documented, **plus** a persistent simulation banner in the interface.
**Why deferred.** Playing "compliance partner" or "staff engineer" requires internal norms marked unknown. The agent would improvise internal culture, and a new hire cannot distinguish simulation from information — the failure is invisible at the moment it happens and surfaces weeks later when they repeat it. Decision rule 9 currently refuses role-play outright.

## DF-04 — Industry failure-modes primer
**Gate:** an explicit framing that survives contact with a reader — a header alone is not enough.
**Why deferred.** The old plan's failure-mode list (ACAT rejects, corporate actions mid-rebalance, T+1 settlement breaks, sweep reconciliation, fee-billing error replication, RMD deadlines, wash sales, performance disagreement) is credible *industry* material and genuinely valuable for an engineer. Presented in an Altruist onboarding agent it reads as a claim about Altruist's systems.
**Partially delivered.** The concepts that are pure vocabulary (wash sale, settlement, cost basis, sweep, partial transfer) are in `02-glossary.md` as definitions, which is the safe half. What is deferred is the "here is what breaks and who gets hurt" framing.
**Note.** This is the most valuable deferred item for an engineering hire specifically.

## DF-05 — State layer (`profile` / `progress` / `gap-log`)
**Gate:** U-01 answered **and** a retention/access policy written.
**Why deferred.** `core` has no state layer; the old plan correctly identified the gap. But storing role, manager, stakeholders, and progress creates a data-handling obligation nobody has accepted, and the confidentiality policy template is itself empty. Running stateless costs a returning hire a repeated introduction; storing employee-relationship data with no policy costs more.
**Designed, not built.** `core/EXTENSIONS.md` records the intended shape so this is an addition rather than a retrofit.

## DF-06 — Checkpoint assessments with numeric bars
**Gate:** real scoring data from at least five hires.
**Why deferred.** The old plan's bars (day 7 ≥ 3.0; day 30 ≥ 4.0 with no axis below 3) are invented numbers on an uncalibrated scale. The *format* — strong / vague / unsafe assumption / missed stakeholder / stronger rewrite / harder follow-up — is well engineered and is preserved in `policy/behavioral-rules.md` rule 6 as the correction style. The scoring is what is deferred.

## DF-07 — Meeting preparation
**Gate:** calendar access granted through a completed access policy.
**Why deferred.** Requires calendar access (withheld, with reasoning) and knowledge of internal meeting norms (unknown). Calendar access would also expose internal meeting titles and attendees — internal information the agent is deliberately built not to have.

## DF-08 — Internal-knowledge capture loop
**Gate:** a written data-classification policy **and** a named approver. See D-07.
**Why deferred.** Not merely deferred — no write path exists at all. The old plan's most attractive idea (knowledge compounds with each hire) is also its most dangerous: it asks a brand-new employee to decide what internal information is safe to write into a file store, in a regulated firm, with no policy and no gate.
**Status:** blocked on `14-policies-and-compliance.TEMPLATE.md`, which is empty.

## DF-09 — Live web search
**Gate:** a tier-assignment rule for retrieved content **and** a disclosure requirement in answers.
**Why deferred.** The reasoning for it is sound — Altruist ships fast and a frozen fact base goes stale. But the entire fact discipline rests on `factbase.json`, and live retrieval injects unclassified claims straight into answers, bypassing tiers, attribution, and quarantine in one step. The old plan granted this in a single line with no worst-case analysis.

## DF-10 — Runtime interception of answers **[BUILT — the original doubt was well-founded]**
**Original gate:** a runtime that exposes a pre-delivery hook, plus a workable definition of a checkable violation in conversational text.
**Why it was deferred.** Honestly: this may not be buildable well. Regex over conversational output produces false positives on legitimate discussion (the agent must be able to say "I can't tell you who approves that" without tripping an approver rule).

**What was built.** `validate_output` in `runtime/agent_runtime.py` runs before every response ships, fails closed, and is shared by the evaluator and the HTTP adapter so a benchmark cannot take a safer path than production. It checks four things: leaked internals, fabrications, unattributed security assurances, and attribution decay.

**The predicted problem happened, repeatedly, and is worth reading before trusting this layer.** Every false-positive class the deferral warned about showed up live and is now documented in the code as a comment on the pattern it forced: `re.I` on the name detector matched "is **t**he right person"; a bare `\bboundary\b` matched "that's a boundary I have to hold"; the attribution-decay check went through three wrong formulations before the fourth matched the real transcript. Each fix is locked by a regression test built from an actual observed answer (`test_grader.py`). The layer works, but it was calibrated by finding its own false positives in production output — treat a future pattern addition the same way.

**Still true:** this does not run on the interactive `/onboard` path, only the automated one. Absence of access remains the control that holds when this one is wrong. Risk R-01.

## DF-11 — `explain` and `ask-better-questions` skills **[WRITTEN, NOT WIRED]**
Both files exist in `skills/` and are correctly scoped — `explain` only simplifies answerable
concepts, `ask-better-questions` produces questions rather than internal answers.

**Neither reaches the agent.** They are absent from `build_prompt.py`'s `SOURCE_FILES`, so they
appear nowhere in `runtime/system-prompt.txt`, nowhere in `AGENT.md`'s mode table, and nowhere
in `knowledge/CLAUDE.md`'s routing. Writing the file is the easy half; wiring it in changes the
prompt digest and invalidates the recorded behavioural run, which is why it stopped here. Steps
to finish in `docs/risks-and-next-steps.md` NS-09.

---

## Not deferred — deliberately discarded

These are not coming back without a fresh argument.

| Item | Why discarded |
|---|---|
| "Name who would approve" rule | Mandates fabrication with an empty org chart. D-06. |
| §5D "internalize the moat sentence in week one" | Converts a labelled inference into taught conviction. |
| Hazel architecture inference | Explicitly forbidden by the primary pack. `ALT-Q18`, permanently quarantined. |
| "3–6 months → 30 days" ramp claim | Unsourced at both ends, no measurement instrument. |
| Hour estimates on build tasks | False precision. |
| Day-90 "onboard the next hire" | Assumes org practice the agent cannot know. |
| Competitor comparison framing | D-12. |
