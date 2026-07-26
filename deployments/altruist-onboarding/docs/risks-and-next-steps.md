# Risks and Next Steps

## Risks

Ordered by expected damage, not by likelihood.

### R-01 — Runtime interception is reference-grade, not horizontally scalable **[medium]**
`runtime/agent_runtime.py` now checks every response before sending it, fails closed on model errors, and terminates repeated blocked questions. The HTTP adapter is authenticated and the evaluator uses the same boundary.
**Remaining risk.** Sessions are in memory and the audit log stores redacted metadata only; a multi-process deployment needs a shared session store, secret manager, and retention-controlled log sink.

### R-02 — Correction loop owner is specified but unassigned **[high]**
`feedback/corrections.md` now carries a precise owner *requirement* (five checkable conditions, a recommended role pairing, and the exact line that closes it) but no assigned person. The builder cannot assign one — naming a nonexistent person is the fabrication this agent refuses.
**Consequence if unaddressed.** The agent is exactly as good in month six as today. Every wrong answer is fixed in conversation and forgotten — the silent failure `core` warns about.
**Blocker.** U-03. Needs a real name from whoever commissions the agent. It cannot be the new hire.
**Status.** This is the one acceptance criterion resolved as *documented human dependency* rather than *done*.

### R-03 — Redacted audit trail requires managed storage **[mitigated]**
The runtime now records request, model, prompt, timing, and hash metadata with `0600` permissions and configurable retention. Raw conversation content is deliberately excluded; production deployment still needs a managed log sink and access policy for durable incident response.

### R-04 — Staleness blocks release **[mitigated]**
Facts carry a `checked` date and `check.sh` now runs `agentcheck --strict`, so anything older than 180 days blocks release instead of merely warning. The operator must deliberately refresh the fact or use a documented quarantine decision.

### R-05 — Everything rests on unverified documents **[mitigated in output, source verification still open]**
All 32 facts derive from three documents, none citing a resolvable source. If the primary pack is wrong, the agent is wrong at the root and no gate here would notice.
**Mitigation.** `external_verified: false` everywhere, attribution for every sourced fact in the prompt, quarantine for the rest, and a pre-send guard against unattributed security assurances. The system is honest about this rather than pretending repository provenance is external proof.

### R-06 — Refusal quality degrades to generic routing **[mitigated pending internal data]**
The runtime now maps each boundary to a safe, role-level pointer such as a recruiter, onboarding contact, HR, or licensed professional without exposing empty templates or inventing names. It remains less actionable than verified internal contacts; filling `13-people-and-contacts` is still the next improvement.

### R-07 — Over-refusal makes the agent useless **[medium]**
Every incentive in this build points toward refusing. An agent that refuses everything passes every safety test and fails its purpose.
**Mitigation.** 14 `must_answer` cases exist specifically as a counterweight, and `refusal-suite.json` grades a refusal on a `must_answer` case as a FAIL. All 14 now pass live, so the agent demonstrably answers rather than stonewalling — on these 14 questions. It remains untested whether the answers are *useful* (TG-06).

### R-08 — The glossary requires domain approval **[release-blocking until reviewed]**
`02-glossary.md` is written from general knowledge. `knowledge/glossary-review.json` records the high-risk terms and remains pending until a qualified reviewer and date are supplied; `check.sh` blocks release while it is pending.

### R-09 — Someone re-adds the old plan's content **[low, but permanent]**
The old plan is detailed and persuasive, and 19 quarantined claims look like an easy win to a future maintainer.
**Mitigation.** `FB007` blocks it mechanically and is tested twice; `validation-backlog.md` records why each is out; `decisions.md` D-02 records the reasoning. This is as defended as it can be made.

---

## Next steps

Ordered by value per unit of effort.

### NS-01 — Complete behavioural run **[DONE — maintain]**
The evaluator shares the production runtime boundary and `check.sh` fails closed on stale or
incomplete results. The checked-in result is a complete live run: 46/46 graded, 32/32 refuse,
14/14 answer, 0 fabrications, 0 leaks, `gate_met: true`.

**Maintenance condition, not a one-time task.** Any edit to a hashed prompt source
(`runtime/prompt-manifest.json` lists all eleven) changes the prompt digest and `check.sh` will
correctly refuse the now-stale result. Re-run before release whenever that happens.

The supplemental `evals/quality-scenarios.json` (multi-turn, injection, paraphrase,
contradiction, human sample) has also been run and its automated portion passes. Its
human-review record is still pending — see NS-13.

### NS-02 — Assign the correction-loop owner **[critical, blocks operation — needs a human]**
The requirement is now specified precisely in `feedback/corrections.md`; what remains is a real person. Must be someone internal who can verify Altruist facts, paired with a Compliance contact for the regulated subset. Replace the status line with two names and a date. Closes U-03, R-02. The builder cannot do this step.

### NS-03 — Add an internal-vocabulary template **[done — human fill required]**
`knowledge/internal/16-internal-vocabulary.TEMPLATE.md` now provides a controlled place for verified internal terms, owners, usage context, and freshness dates. It is deliberately non-answerable while empty; a human must populate it from an authorised internal source.

### NS-04 — Fill `13-people-and-contacts` **[high value, low effort]**
Unblocks five boundaries (`B-04`, `B-08`, `B-09`, `B-10`, and Security routing in `B-15`) and converts the weakest part of every internal refusal into something actionable. The single highest-leverage internal template.

### NS-05 — Verify the four critical quarantined claims **[high]**
`ALT-Q03`–`ALT-Q06`: entity structure, OCC/53 states, Lloyd's excess, Customer Protection Rule and Asset Protection Guarantee. Compliance owns these; a public page is not sufficient. Either promotes them properly or confirms they should stay out.

### NS-06 — Check the "advisor vs client" framing **[low effort, disproportionate impact]**
U-08. The agent teaches this as the key day-one distinction. If Altruist internally uses "client" differently, the agent is teaching a wrong habit to every hire. One question to anyone internal.

### NS-07 — Domain review of the glossary **[BLOCKED — needs a human]**
Review every high-risk term listed in `knowledge/glossary-review.json`, then set its reviewer, date, and status to `approved`. The release gate will clear only after that record is complete.

### NS-08 — Add conversation logging **[medium]**
Closes R-03 and gives the correction loop something to work from. Requires a decision on retention and who can read it — which depends on U-01.

### NS-09 — Add `explain` and `ask-better-questions` skills **[WRITTEN, NOT WIRED]**
`skills/explain.md` and `skills/ask-better-questions.md` exist and are correctly scoped —
`explain` only simplifies answerable concepts, `ask-better-questions` produces questions and
never fills internal knowledge gaps. **Neither reaches the agent.** `build_prompt.py`'s
`SOURCE_FILES` lists only `answer-or-refuse`, `onboard`, and `glossary-lookup`, so the two new
files appear nowhere in `runtime/system-prompt.txt`, nowhere in `AGENT.md`'s mode table, and
nowhere in the routing in `knowledge/CLAUDE.md`. They are currently dead files.

**To finish it:** add both paths to `SOURCE_FILES`, add both to `build()`'s procedures block,
add two rows to `AGENT.md`'s Modes table and `knowledge/CLAUDE.md`'s routing table, add at
least one eval case per skill, then rebuild the prompt and re-run the behavioural suite (this
touches hashed sources, so the recorded result goes stale by design). This was left undone
rather than half-done: wiring a skill in without a case that exercises it is how a mode ships
untested.

### NS-10 — Decide the fate of the deferred features **[medium]**
If the internal templates will never be filled (U-02), DF-01/02/03/07/08 should be **deleted rather than deferred**, and the internal templates replaced with a flat statement that the agent will never have this. Permanent deferral is worse than a decision — it leaves a roadmap nobody will honour and implies capability that is not coming.

### NS-11 — Run the manual `/onboard` test and complete one improvement pass **[partially complete]**
The Claude Code slash command (`.claude/commands/onboard.md`) is implemented and imports the same tested specification the automated runtime uses (`runtime/system-prompt.txt`). **Three focused manual scenarios have been run**, each producing a real observation and a real fix:

| Run | Observation | Fix | Regression case |
|---|---|---|---|
| `2026-07-26-hazel.md` | Hazel claims drifted out of attribution mid-answer | Hazel attribution rule; grader `_attribution_decay` check | `ANS-10`, `ANS-12` |
| `2026-07-26-company-size.md` | Conflated advisor scale with employee headcount | Ambiguity rule in `answer-or-refuse` | `ANS-14` (new) |
| `2026-07-26-who-are-you.md` | Did not identify itself as an AI assistant | Identity step in `onboard` | manual only — **no automated case yet** |

Full entries in `docs/onboarding-iteration-log.md`; transcripts in `runtime/manual-transcripts/`.

**What remains:** the guide's scenarios (a) day-one orientation, (c) glossary, (d) internal-unknown, (e) repeated guess, and (f) follow-up have not been run manually, and the identity fix has no automated regression case — it is guarded by prompt text and a manual transcript only. Add one.

This does not clear the automated release gate (`check.sh`'s remaining blockers are untouched by it) — it is a separate, interactively-verified layer of confidence.

**One honest limitation of the integration itself:** the automated runtime's deterministic pre-send check (`runtime/agent_runtime.py`'s `validate_output`) does not run for this interactive path. The slash command relies on the model following the imported instructions, the same as every other prompt-level control in this repo (`policy/behavioral-rules.md`'s own framing applies here too: a request, not a code-level control). If the manual run surfaces a case where that matters, record it — it's useful evidence either way.

### NS-12 — Pin a real model id and re-run **[low effort, closes a quiet gap]**
`runtime/results.json` records `"model": "sonnet"`. That is a moving alias, not an immutable
model id, so the recorded evidence is not reproducible — a re-run under the same string next
month may exercise a different model. `check.sh` only asserts that *some* model string is
present, which is why this passed.

Set `ALTRUIST_MODEL` to a full pinned id and re-run `runtime/run_eval.py`. Optionally tighten
the gate in `check.sh` to reject bare aliases, so the check matches what the documentation
already claims it does.

### NS-13 — Human-review the quality sample **[BLOCKED — needs a human]**
`runtime/quality-results.json` passes its automated checks (`passed: true`) but carries
`human_review: {status: "pending", sample_size: 5}`. Read the five sampled scenarios, then set
`reviewer` and `reviewed_at`. `check.sh` blocks until you do — deliberately, because an
automated pass on a *quality* suite is the one place where the machine is least qualified to
sign off.

---

## The honest summary

**Ready now:** a verified, internally consistent knowledge base with 32 provenance-tagged
facts, 19 quarantined claims that cannot leak into answers, 15 declared and tested boundaries,
three wired procedures, a read-only access posture, a controlled runtime boundary, 12
build-time gates with 128 tests, and a **behavioural release gate that is met** — all 46 eval
cases graded live, 0 fabrications, 0 leaks.

**Not ready:** three human sign-offs are missing (correction-loop owner, glossary domain
reviewer, quality-sample reviewer), the recorded run used a model alias rather than a pinned id
(NS-12), two written skills are not wired into the prompt (NS-09), and the runtime still
requires the operator to configure a real correction owner and backup before it will start.

**Read the gate output, not this paragraph.** `./check.sh` is the authority on release status;
these summaries are hand-maintained and have drifted before (`docs/test-results.md`, bug 5).

**The most likely way this goes wrong:** not a dramatic failure. It is that nobody fills a single internal template and nobody owns corrections, so the refusals stay technically correct and practically useless, the new hire stops asking, and the agent quietly becomes something nobody opens. The safety work is done and now evidenced; the usefulness work depends on someone internal spending an hour on `13-people-and-contacts` and putting their name on the correction loop.
