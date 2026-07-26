# Decisions

Each entry: what was decided, why, what was given up, and what would reverse it.

---

## D-01 — `core/` is the architectural authority; the deployment lives outside it

**Decision.** Build under `deployments/altruist-onboarding/`, leaving `core/` a blank master. Five layers in `core`'s fixed order.

**Why.** Three competing folder structures existed (core's, the knowledge pack's twelve files, the old plan's ten-plus-state-plus-evals). The audit resolved this in favour of core. Filling `core/` in place would destroy the master for the next deployment.

**Given up.** The knowledge pack's numbered-file layout, which was more browsable but bypassed core's quality checklist — that checklist is written against the `CLAUDE.md` template, so loose files are unaudited by construction.

**Reversed by.** A decision that this repository serves one client only, making the master pointless.

---

## D-02 — `new-agent.md` carries no authority

**Decision.** The old plan is not a source. It can move a claim **into** quarantine; it can never move one into the answerable set. Enforced mechanically (`agentcheck` FB007), tested twice, and reflected in the access policy by not granting the agent read access to it.

**Why.** ~40 specific claims, zero URLs, zero per-fact dates, tiers applied to paragraphs rather than facts. The audit found its detail to be presentational rather than evidentiary. Allowing it as a weak source would mean its precision quietly outcompetes the primary pack's hedged, sourced statements — which is exactly how the specificity inflation happened in the first place.

**Given up.** ~40 claims that are probably mostly true, including some a new hire would genuinely find useful (entity structure, funding, Hazel timeline). They are recoverable via `validation-backlog.md` at the cost of actually verifying them.

**Reversed by.** Per-fact external sourcing. Not by the plan being detailed, and not by it being mostly right.

---

## D-03 — The secondary knowledge file is a second document, not a second source

**Decision.** `altruist-knowledge.md` promotes some claims to tier P3 and corroborates others, but never converts a claim into "verified". Everything keeps `external_verified: false`.

**Why.** It cites no URLs either. Two documents agreeing is corroboration between unverified secondary artifacts. Describing that as confirmation would be the precise error the agent exists to prevent in a new hire, committed by the system itself.

**Given up.** A much larger answerable fact base, and the comfortable feeling that agreement means truth.

**Reversed by.** Resolvable sources on the underlying claims.

**Notable outcome.** The secondary file corroborated the *primary pack* against the old plan on office locations, and corroborated only the *narrow* form of the regulatory claim — which is how the dangerous specifics (entity structure, Lloyd's, Customer Protection Rule) stayed quarantined while the useful narrow claim became answerable as `ALT-027`.

---

## D-04 — Tiers record document provenance, not verification

**Decision.** P1 / P2 / P3 describe which document a claim came from and how it corroborates. A separate boolean, `external_verified`, records verification and is `false` everywhere. A fact claiming `external_verified: true` without recording its source is a blocking error.

**Why.** The old plan's A/B/C/D tiers looked like an audit trail and had nothing behind them. A confidence marker with no resolvable source suppresses a reader's scepticism without earning it — worse than no tiering.

**Given up.** The simpler single-axis system.

---

## D-05 — Facts and boundaries are machine-readable; prose cites them

**Decision.** `factbase.json` and `boundaries.json` are the single authorities. Prose in `knowledge/public/` cites ids and establishes nothing. Skills reference boundaries and restate none.

**Why.** core's repeated warning about the same rule living in two places. It also makes the safety properties *countable* and *testable* — 15 boundaries, all covered; 32 facts, all cited; published counts proven against the fact base.

**Given up.** Some readability. A reviewer must hold two files open. Mitigated by keeping prose the human-facing surface.

---

## D-06 — The "name who would approve" rule is deleted, not deferred

**Decision.** Deleted from the behavioural rules. Boundary `B-13` refuses approval questions. Three eval cases, including a false-authority adversarial case.

**Why.** The audit's second-most-critical finding. With `10-internal-org-chart.TEMPLATE.md` empty, the rule could only be satisfied by fabrication — and a rule that cannot be followed truthfully will be followed falsely.

**Given up.** A genuinely valuable habit to teach, once the org chart exists.

**Reversed by.** A filled org chart *with* approval chains, plus a deliberate revisit. Recorded in the template itself so the reversal condition sits where someone filling it will see it.

---

## D-07 — No internal-knowledge capture path exists

**Decision.** The old plan's loop — the hire writes internal learnings into `knowledge/internal/` — is not built. Not gated, not stubbed. No write path exists.

**Why.** Unclassified internal-data capture in a regulated firm, authorized by nobody, with the confidentiality policy template itself empty. The audit's third critical finding. Building it behind a flag would still mean the path exists.

**Given up.** The compounding-knowledge property, which was the old plan's most attractive idea.

**Reversed by.** A written data-classification policy and a named approver.

---

## D-08 — Read-only, no state, no web search

**Decision.** The agent reads `knowledge/`, `skills/`, `policy/`. Nothing else. No persistence, no retrieval, no send capability.

**Why.** Operator model is undecided (U-01), so PII rules are unknown; live retrieval would inject untiered claims straight into answers, bypassing the entire fact discipline; and absence of access is the only control that holds at runtime when there is no output gate.

**Given up.** Currency — the fact base is frozen and dated. Personalization. Cross-session memory.

**Reversed by.** For web search: a rule assigning a tier to retrieved content and a disclosure requirement. For state: an answer to U-01 and a retention policy.

---

## D-09 — Enforcement gates the knowledge base, not the conversation

**Decision.** Repoint `core`'s `validate.py` at `knowledge/public/*.md` at build time; add `agentcheck` for structural checks; treat absence of access as the runtime control. `validate.py` is copied unmodified and a test enforces byte-equality with `core`'s.

**Why.** The audit's structural finding: no pre-send artifact exists for a conversational agent. Forking the validator would have drifted the deployment from the scaffold; pretending prompt rules are enforcement is the error the old plan made.

**Given up.** Any runtime interception. Documented as risk R-01 and gap TG-01 rather than papered over.

**Superseded in part (2026-07-26).** Runtime interception was subsequently built —
`validate_output` in `runtime/agent_runtime.py` runs a fail-closed pre-send check shared by the
evaluator and the HTTP adapter. The decision above still holds for the *build-time* layer, which
remains the primary control and is unchanged; what changed is that "no runtime interception" is
no longer accurate. It does not cover the interactive `/onboard` path. See `docs/deferred.md`
DF-10 for what was built and which of the predicted false-positive problems actually occurred.

---

## D-10 — Three skills, not six modes

**Decision.** `answer-or-refuse`, `onboard`, `glossary-lookup`. Meeting prep, stakeholder role-play, and workflow tracing are deferred with written gate conditions.

**Why.** The audit's V1 specified one skill; two more were added because both are 100% pack-supported and the glossary is core's highest-value section. The other three each require internal knowledge that does not exist — role-play in particular would have the agent improvising internal culture that a new hire cannot distinguish from information.

**Given up.** Most of the old plan's richness.

---

## D-11 — Profile capture is limited to first name and role, persisted nowhere

**Decision.** `onboard.md` asks role once, optionally. It does not ask for manager, start date, or stakeholders.

**Why.** The old plan captured five fields including manager and stakeholders. Capturing from the user is legitimate — the risk is storage, not fabrication — but storing employee-relationship data creates an obligation nobody has accepted, and the operator model is undecided.

**Given up.** Role-adaptive content, which is deferred anyway for lack of role-specific material.

---

## D-12 — Competitive comparison is stripped from an otherwise answerable fact

**Decision.** `ALT-031` carries the neutral reason-list and is marked sensitive; the source's comparison framing is dropped and competitor names are quarantined (`ALT-Q19`).

**Why.** The secondary document phrases the positioning partly as comparing favourably to named competitors. A new hire repeating a competitive claim carries reputational risk, and the claim is unverified. The neutral form loses nothing a day-one hire needs.

**Notable.** The knowledge-base linter caught the residue of this decision — an instruction *not* to compare, containing competitor names, sitting in a knowledge file. That was a real layering violation (a rule in a facts file), and fixing it moved the rule to `CLAUDE.md` §10 where it belonged.
