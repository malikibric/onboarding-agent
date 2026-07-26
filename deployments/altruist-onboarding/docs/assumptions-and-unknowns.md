# Assumptions and Unknowns

Everything the build could not verify. Assumptions are things acted on anyway, with the fallback stated. Unknowns are things left open.

---

## Assumptions acted on

### A-01 — Tier reflects document provenance, not external verification
**Assumed.** The three input documents describe Altruist accurately enough to be worth encoding, even though none cites a resolvable source.
**Basis.** The audit designates the primary pack as the grounding document; the task designates the secondary file as domain context.
**Risk if wrong.** Every answerable fact is wrong at the root. Contained by: `external_verified: false` on all 32 facts, attribution required on P3, the whole quarantine mechanism, and `validation-backlog.md`.
**How to close.** Source the facts. Nothing else closes it.

### A-02 — Operator model: hire-deployed, self-serve
**Assumed.** The new hire runs this themselves.
**Basis.** Audit §I Phase 0: *"If 0.1 is unanswered, build Phase 1 anyway under the most restrictive assumption: hire-deployed, read-only, no internal capture, no PII beyond first name and role."* Explicitly pre-authorized.
**Consequences.** No state layer, no PII beyond first name and role, no internal capture, read-only access.
**Risk if wrong.** If HR-deployed, state and personalization become reasonable and the build is more restrictive than necessary — a recoverable error. If manager-deployed, the correction-loop owner may already exist. Both are cheaper to fix than the reverse.

### A-03 — The seven internal templates are not filled and may never be
**Assumed.** No internal content is coming in the near term.
**Basis.** Six are marked "unknown externally" in the primary pack and nobody has been named to fill them; the seventh (`16-internal-vocabulary`) was added later by NS-03 as a controlled slot and is empty for the same reason.
**Consequences.** Every internal route points at an empty slot; the agent must say so. Curriculum and role branches deferred.
**Risk if wrong.** If they are filled next week, the deferred features become buildable and the refusal routing needs revisiting (NS-04). Note that filling any of them invalidates the recorded behavioural run, since `check.sh` blocks when anything under `knowledge/` is newer than `results.json`.

### A-04 — Industry vocabulary definitions are safe general knowledge
**Assumed.** Defining RIA, ACAT, custodian, SIPC, wash sale etc. is general financial-industry knowledge, not a claim about Altruist, and is within scope.
**Basis.** The primary pack explicitly requests a glossary and lists the terms.
**Consequences.** `02-glossary.md` is the richest file in the knowledge base and carries no fact ids for its definitions.
**Risk if wrong.** A definition could be subtly wrong or could differ from Altruist's internal usage. Contained by: `glossary-lookup.md` step 1 routes anything that might be internal jargon to a refusal, and the file states its provenance at the top.
**Known limitation.** The definitions were written from general knowledge and have not been reviewed by anyone with financial-services expertise. Recorded as TG-03.

### A-05 — "About 30 days" may be stated; day-numbered milestones may not
**Assumed.** The primary pack's hedged claim is answerable; the old plan's day-5/15/30 overlay is not.
**Basis.** Specificity inflation — a precise-looking overlay on a vaguer sourced claim.
**Consequence.** Eval case ANS-09 requires the hedged answer; REF-32 requires refusing the specific one even when the question supplies the numbers.

### A-06 — Attribution wording is a design choice, not a sourced requirement
**Assumed.** "Altruist's public materials describe…" is an adequate attribution formula.
**Basis.** Nothing. It is a judgment about what makes provenance audible to a listener.
**Risk if wrong.** Too weak and a hire hears it as fact; too heavy and every answer is caveat. Untested with real users — TG-04.

---

## Unknowns — open, blocking where noted

### U-01 — Who operates this agent? **[blocking for state, PII, tools]**
Hire, HR, or manager. Determines whether state, personalization, and internal routing are appropriate at all.
**Ask:** whoever commissioned the agent. **Currently:** A-02 fallback.

### U-02 — Will the internal templates be filled, by whom, under what classification? **[blocking for curriculum, role branches]**
If never, the deferred features should be deleted rather than deferred, and the internal templates should be replaced with a flat statement that the agent will never have this.
**Ask:** HR / People Ops owner.

### U-03 — Who owns the correction loop? **[blocking for the feedback layer to function]**
`core` requires the process owner, not the builder. It cannot be the new hire — they cannot verify Altruist facts and are the least-equipped person to run the loop.
**Ask:** the process owner. **Currently:** unassigned; feedback layer declared but not operational. Risk R-02.

### U-04 — Can any quarantined claim be externally verified, and by whom?
19 claims, 4 rated critical (entity structure, OCC/53 states, Lloyd's excess, Customer Protection Rule / Asset Protection Guarantee).
**Ask:** Compliance for the critical four; anyone with source access for the rest. **Currently:** `validation-backlog.md`.

### U-05 — Is live web search permitted?
Blocked in V1 because retrieved content carries no tier. Needs a tier-assignment rule and a disclosure requirement before it could be granted.
**Ask:** deployment owner.

### U-06 — What is the agent's actual runtime?
Claude Project, Claude Code with files, something else. The build is runtime-agnostic — a knowledge base, procedures, and gates — but nothing has been wired to an interface, so the agent has never actually run.
**Consequence.** The behavioural eval pass cannot be executed until this is answered. TG-01.

### U-07 — Does Altruist have internal vocabulary a new hire needs?
Almost certainly yes, and it is arguably higher-value than the org chart — `core` calls vocabulary the highest-value section and this agent has only the industry half. The controlled `knowledge/internal/16-internal-vocabulary.TEMPLATE.md` now captures it, but remains empty until an authorised internal source is provided. NS-03.

### U-08 — Is the "advisor vs client" framing correct in Altruist's own usage?
The build treats "client" as the advisor's end investor and Altruist's customer as the advisory firm, and teaches this as the key day-one distinction. Both source documents support it, but if Altruist internally says "client" to mean the advisory firm, the agent is teaching the wrong habit.
**Ask:** anyone internal. Cheap to check, disproportionately damaging if wrong.

### U-09 — Are there onboarding topics nobody has thought to ask about?
The boundary list was derived from the primary pack's must-not-pretend list plus the audit's additions. It is 15 boundaries covering the anticipated questions. A real cohort will ask things nobody predicted.
**Mitigation.** `feedback/corrections.md` has a stricter loop for out-of-scope failures, requiring a new eval case for each. This is the mechanism by which the boundary list grows.
