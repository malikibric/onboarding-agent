# Implementation Plan — Altruist Onboarding Agent

**Status:** Build complete. Controlled runtime and fail-closed release gate implemented; structural checks, 128 tests, and the full 46-case behavioural run all pass. Release is blocked only on three human sign-offs (glossary reviewer, quality-sample reviewer, correction-loop owner). Runtime startup requires a pinned model, auth token, correction owner, and backup. See `test-results.md` for the current gate output and `risks-and-next-steps.md` for what is left.
**Build date:** 2026-07-25 to 2026-07-26
**Authority:** `AUDIT_altruist_onboarding_agent.md` (architecture, scope, safety)
**Domain context:** `altruist_onboarding_agent_knowledge.md` (primary), `altruist-knowledge.md` (secondary)

---

## 1. Scope extracted from the audit

### 1.1 Allowed scope (what the agent may do)

From audit §B1/§B2 and §J:

- Explain what Altruist is, who it serves, and its public mission.
- Explain the public product surface at a high level.
- Explain the publicly described customer onboarding journey.
- Explain public Hazel capabilities.
- Explain company values and public culture information.
- Answer beginner-level glossary questions about industry terms (RIA, custodian, ACAT, etc.).
- **Refuse accurately** — the defining behavior. Name what it does not know and what source category would answer it.

### 1.2 Forbidden scope (hard constraints)

From audit §B2 (pack's must-not-pretend list) plus §F4 additions:

- Internal tools, URLs, systems.
- Names of managers, teammates, or any employee.
- Security procedures.
- Internal policies or handbook details.
- Exact first-week meeting schedules.
- Private architecture, prompts, permissions, model stack, evaluation methods, customer data flows.
- Compensation or benefits detail beyond public careers copy.
- **Added in audit §F4:** employment/HR advice, legal advice, immigration/visa, medical/benefits enrollment, performance concerns, anything about specific colleagues.
- **Added in audit §C bucket 4:** naming approvers for compliance-touching changes; asserting regulatory specifics that are not verified; stating Hazel security claims as verified controls rather than public statements.

### 1.3 Architecture constraints

From audit §H and `core/`:

- Five layers, fixed fill order: knowledge → skills → tools → feedback → enforcement.
- Nouns vs verbs: facts live in knowledge; procedures live in skills; never both.
- `core/` stays a blank master. This agent is a deployment copy under `deployments/`.
- One operative `knowledge/CLAUDE.md` on core's 12 sections; reference files behind it.
- Verified public knowledge, quarantined knowledge, and future internal knowledge separate at the directory level.
- No fact is answerable without a source id and a checked date (audit §H3).
- Enforcement must run outside the model (audit §E5).

### 1.4 Core workflows

- `answer-or-refuse` — the defining verb (audit §J item 4).
- `onboard` — the pack's 7-step day-one flow.
- `glossary-lookup` — highest-value knowledge section per `core/`.

### 1.5 Verification expectations

- Refusal suite must pass 20/20 on must-refuse items before ship (audit §J).
- Every answerable fact resolves to a source id and a checked date.
- Knowledge lint exits 0.
- Quality checklist scored and reported honestly, including a weak score.

---

## 2. Phase 0 resolution — blocking questions

The audit §I Phase 0 lists four blocking questions. None can be answered from the documents. The audit pre-authorized a fallback:

> *"If 0.1 is unanswered, build Phase 1 anyway under the most restrictive assumption: hire-deployed, read-only, no internal capture, no PII beyond first name and role."*

**Adopted for this build.** Consequences, all recorded in `assumptions-and-unknowns.md`:

| Question | Fallback taken | Consequence |
|---|---|---|
| 0.1 Operator model | Hire-deployed, self-serve | No PII beyond first name + role; no state persistence in V1 |
| 0.2 Will internal templates be filled | Assume not yet | Templates ship empty; all internal routing degrades to `[MISSING: role]` |
| 0.3 Correction-loop owner | Unassigned | `corrections.md` ships with the owner field blank and marked blocking |
| 0.4 Architecture | Audit §H2 accepted | Built as specified |

---

## 3. Build order

| Phase | Content | Status |
|---|---|---|
| 1 | Fact reconciliation across three documents → tiering | Complete |
| 2 | Knowledge layer (CLAUDE.md, public/, quarantine, registry, internal templates) | Complete |
| 3 | Skills layer (3 skills) | Complete |
| 4 | Tools layer (access policy) | Complete |
| 5 | Feedback layer (corrections log) | Complete |
| 6 | Enforcement layer (gates, rules, runner) | Complete |
| 7 | Verification machinery + tests | Complete |
| 8 | Eval suite (refusal suite) | Complete |
| 9 | Documentation set | Complete |

Fixed order per `core/README.md`. Enforcement is built last and separately because it must hold when everything above it is wrong.

---

## 4. What is deliberately NOT in V1

Per audit §J "Explicitly NOT in V1" and §I Phase 7 gating. Full reasoning in `deferred.md`.

Curriculum, mode system beyond the three skills, stakeholder role-play, meeting prep, workflow tracing, checkpoints, numeric scoring bars, state files, internal-knowledge capture, web search, and every quarantined fact.

---

## 5. Technology decisions

| Decision | Choice | Reason |
|---|---|---|
| Config format | JSON | Matches `core/enforcement/rules.json`; stdlib-only |
| Runtime check dependencies | None (stdlib) | Release gating must never depend on a third-party install |
| Test runner | pytest | Present in environment; standard |
| Language | Python 3 | `core/enforcement/validate.py` is already Python; no reason to add a second runtime |

Full reasoning in `decisions.md`.
