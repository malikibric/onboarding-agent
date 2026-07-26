# HarperOS Altruist Onboarding Agent — Finished Audit

**Review date:** 26 July 2026  
**Reviewer stance:** Production-readiness audit; no code changes made.

## 1. Executive Verdict

This is **not production-ready**. It is a disciplined safety prototype and a reasonably good knowledge-governance package, but it is not a deployable agent system. The repository is strongest where it constrains and documents what the model should not know; it is weakest where production requires actual enforcement, observability, source verification, runtime integration, and trustworthy evaluation.

The current release signal is also misleading: the live result has 12 errored answer cases, `gate_met` is false, yet [check.sh](deployments/altruist-onboarding/check.sh#L54-L61) exits successfully because it only warns about the failed behavioral gate.

Honest classification: **useful for controlled experimentation, unsafe to represent as production-ready, and not yet close enough for unsupervised internal onboarding.**

## 2. What Is Genuinely Strong

- The repository understands the difference between documentation and enforcement. It explicitly admits that the build-time validator does not inspect live model output.
- The absence-of-access posture is real. There is no web, CRM, HRIS, email, calendar, write, or internal-system access. This limits the worst case to a wrong sentence rather than an unauthorized action.
- The old strategic plan is not trusted by default. `PLAN` cannot promote claims into the answerable fact set, including through source laundering. The invariant is implemented in [checks.py](deployments/altruist-onboarding/verification/agentcheck/checks.py#L47-L69).
- The fact/quarantine distinction is structurally clear. The system distinguishes answerable claims, quarantined claims, repository provenance, and external verification.
- The boundary inventory is comprehensive for the stated scope: internal tools, org structure, onboarding logistics, compensation, HR, immigration, investment advice, architecture, approvals, quarantined facts, and Hazel security assurance.
- The test suite tests many validator failure paths rather than only happy paths. It covers malformed facts, duplicate IDs, missing routes, unknown cases, stale facts, unsupported sources, and missing boundary coverage.
- The prompt is generated from structured artifacts in [build_prompt.py](deployments/altruist-onboarding/runtime/build_prompt.py#L80-L125), reducing one class of prompt/knowledge drift.
- The repository documents known risks instead of hiding them: no external verification, no conversation logging, no correction owner, no per-turn interception, and an unreviewed glossary.
- The refusal suite includes useful adversarial shapes: guess requests, hypothetical framing, false authority, roleplay, and leading quarantined numbers.

## 3. What Is Weak or Broken

### Critical

#### 3.1 The release gate does not gate the behavioral gate

The current result contains:

- 32/32 refusal cases graded;
- 1/13 answer cases graded;
- 12 answer cases errored due to the spend limit;
- `gate_met: false`.

This is visible in [results.json](deployments/altruist-onboarding/runtime/results.json#L1-L25).

However, [check.sh](deployments/altruist-onboarding/check.sh#L36-L61) prints a warning and still exits zero. It does not set a failure status when `gate_met` is false or `errored` is nonempty.

**Consequence:** CI can receive a successful exit code after only one of thirteen answer cases has actually run. The release control is broken.

#### 3.2 There is no production runtime

There is no application server, chat loop, authentication, session handling, model configuration, deployment target, logging, redaction, retention policy, or runtime output filter.

The “runtime” is an evaluation harness invoking the external `claude` CLI in a subprocess, not a production agent. [architecture.md](deployments/altruist-onboarding/docs/architecture.md#L76-L84) explicitly admits this.

**Consequence:** production behavior is not demonstrated outside the benchmark harness. The system cannot currently support authenticated users, audit trails, tenant boundaries, or operational incident response.

#### 3.3 The strongest safety control is prompt compliance

There is no runtime interception between model output and the user. The model receives facts, quarantined claims, boundary descriptions, route labels, and internal implementation details, then is instructed not to reveal them.

The grader can detect some leaks after the fact, but no production pre-send blocker exists.

**Consequence:** an unusual prompt, context interaction, model update, or inherited instruction can produce an unreviewed false claim or internal metadata leak.

#### 3.4 No source is externally verified

Every fact has `external_verified: false`, and the supplied source documents contain no resolvable external URLs. This is explicit in [factbase.json](deployments/altruist-onboarding/knowledge/factbase.json#L1-L48).

The system allows P1 and P2 claims to be stated plainly even though “primary source” means primary repository input, not an authoritative external source.

**Consequence:** a wrong statement in the initial knowledge pack becomes a confident onboarding lesson. Quarantine catches some unsupported claims, but not errors inside the answerable set.

#### 3.5 The correction loop is not operational

The owner is unassigned. [corrections.md](deployments/altruist-onboarding/feedback/corrections.md#L5-L47) defines a good ownership requirement but does not provide an accountable person, intake channel, SLA, approval workflow, or change audit.

**Consequence:** the system can remain exactly as wrong six months later. A correction is not guaranteed to become a fact-base change, regression case, prompt rebuild, and approved deployment.

### High

#### 3.6 The behavioral grader is too weak to support production safety claims

The grader in [grader.py](deployments/altruist-onboarding/runtime/grader.py#L1-L180) relies heavily on regex and keyword heuristics:

- finite refusal phrases;
- hardcoded tools, teams, approval phrases, and names;
- a manually duplicated quarantine string list;
- no semantic grounding check;
- no contradiction detector;
- no factuality grader for answer cases;
- no validation that required attribution applies to the correct claim;
- no scope or usefulness assessment.

It is a smoke test, not a safety proof.

#### 3.7 `must_answer` grading is shallow

Answer cases pass when expected substrings appear. The grader does not establish that the answer covers the required fact, omits unsupported details, applies attribution correctly, distinguishes marketing from verified behavior, or remains useful and in scope.

The `expect_absent` logic is globally hedged: a refusal marker anywhere can make a banned phrase acceptable. See [grader.py](deployments/altruist-onboarding/runtime/grader.py#L245-L264).

#### 3.8 Behavioral coverage is single-turn and narrow

The 45 fixed questions do not test multi-turn persistence, repeated blocked questions, prompt injection, fake user-provided documents, mixed answerable/forbidden questions, paraphrases, typos, multilingual inputs, long context, malicious quoted instructions, conflicting assertions, or model pressure after refusal.

**Consequence:** the agent may pass the benchmark and fail the natural-language variants actual hires use.

#### 3.9 The prompt contains internal machinery and depends on the model not exposing it

The generated prompt contains fact IDs, quarantine IDs, route labels, internal paths, policy text, and evaluator-oriented instructions. The model is told not to leak them, but the production runtime has no actual output sanitizer.

Earlier runs already produced internal file paths, fact codes, and meta-commentary, as recorded in [behavioural-results.md](deployments/altruist-onboarding/docs/behavioural-results.md#L5-L19).

#### 3.10 The prompt artifact can drift from source artifacts

[run_eval.py](deployments/altruist-onboarding/runtime/run_eval.py#L185-L201) requires an existing `system-prompt.txt` but does not rebuild it or verify its hash against the current source artifacts.

The release script checks knowledge-file timestamps but not prompt freshness or prompt/source equivalence.

**Consequence:** a maintainer can change the fact base and run evaluation against stale prompt content.

#### 3.11 The repeated-question rule is not implemented

The policy says that after the same blocked question is asked three times, the agent should issue a terminal refusal. The current runtime is stateless and has no repetition counter, normalization, or session store.

**Consequence:** this behavior is specified but not operational.

### Medium

#### 3.12 Documentation and implementation are already out of sync

The repository reports conflicting test counts:

- [README.md](deployments/altruist-onboarding/README.md#L24-L46) says 95 tests;
- [AGENT.md](deployments/altruist-onboarding/AGENT.md#L58-L73) says 101 tests in one place and 95 in another;
- [test-strategy.md](deployments/altruist-onboarding/docs/test-strategy.md#L80-L89) says 95 tests;
- the actual test run produced **104 passed**.

Behavioral documentation also describes the answer gate as met while the current recorded result has 12 errored answer cases and `gate_met: false`.

**Consequence:** reviewers receive inconsistent release signals.

#### 3.13 Staleness warnings do not enforce freshness

Facts older than 180 days warn but do not block. Product capabilities, security messaging, regulatory descriptions, onboarding timelines, and tax-related features should not be treated as evergreen.

#### 3.14 Internal routes are technically present but practically useless

Route slots resolve to empty templates. The model can only provide generic pointers such as “your recruiter or HR” or “the right internal team.” This is safe but not useful for the questions new hires actually need answered.

#### 3.15 The glossary is not domain-reviewed

Financial-services definitions such as SIPC, wash sales, ACATs, and custody are generated from general knowledge without financial-services subject matter review. A subtle error could be confidently repeated to every new hire.

## 4. Hidden Risks

- **P1 looks externally authoritative but is not.** The labels create an appearance of source rigor while all claims remain externally unverified.
- **The system is overengineered around static governance and underbuilt around runtime reality.** It has extensive schemas, policies, gates, graders, and documentation, but no production request path, audit log, output interceptor, model pinning, or owner.
- **Policy and quarantine data are duplicated.** Quarantined strings exist in the fact base, grader, prose, eval cases, and boundaries. New claims can be blocked in one layer but missed in another.
- **The evaluator is not hermetic.** The `claude` CLI inherits operator configuration and ambient instructions. Results are not reliably reproducible across machines.
- **A safe refusal can still be practically useless.** Generic routing will cause users to abandon the assistant for the questions they most need answered.
- **Hazel security messaging remains a dangerous answerable surface.** The distinction between marketing and assurance is conceptually correct but still prompt-dependent.
- **Absence of access limits actions, not misinformation.** A wrong regulatory, security, tax, or product statement can still be repeated by a new hire.

## 5. Biggest Gap to Production

The biggest missing capability is **a real controlled runtime with a hard release contract**.

That requires:

1. a production request path;
2. a pinned model and runtime configuration;
3. current-artifact verification;
4. pre-send output inspection;
5. conversation logging with retention and access rules;
6. session-aware behavior;
7. CI failure when behavioral results are incomplete or stale;
8. an accountable correction owner.

Without this, the repository evaluates a model invocation rather than operating an agent.

The most urgent immediate defect is narrower: [check.sh](deployments/altruist-onboarding/check.sh#L36-L61) must fail when `runtime/results.json` has `gate_met: false` or any errored cases.

## 6. Recommended Next Moves

### 1. Repair the release gate and status claims

- Make [check.sh](deployments/altruist-onboarding/check.sh#L36-L61) exit nonzero when `gate_met` is false, cases are errored, results are stale, or the prompt hash does not match current artifacts.
- Do not call a run a pass if 12 answer cases were not executed.
- Regenerate the result after a complete run.
- Correct all test counts in the README, agent entry point, and test strategy.

### 2. Build a real runtime boundary

Create an actual service or adapter with authenticated users, explicit sessions, model and prompt version identifiers, timeout and retry handling, no-tools enforcement, pre-send policy checks, structured internal metadata kept out of user output, and fail-closed error handling.

The evaluator should call this same runtime rather than a separate subprocess path.

### 3. Replace regex-only grading with structured evaluation

Keep regex as a cheap first pass, but add semantic refusal review, assertion-versus-disclaimer classification, answer grounding against allowed fact IDs, mandatory attribution validation, contradiction tests, multi-turn tests, prompt-injection tests, paraphrase variants, and human review sampling.

### 4. Make provenance semantics honest

Externally verify the facts against authoritative sources, or treat all current facts as attributed claims rather than ordinary facts. Do not call repository documents “primary sources” when they have no external citations.

Regulatory, security, tax, and product capability claims need the strictest treatment.

### 5. Operationalize ownership, logging, and correction

Assign a content owner, compliance reviewer, backup, correction intake channel, review cadence, retention policy, and transcript access policy. Then add CI checks for the operational process.

## 7. Final Score

| Area | Score | Assessment |
|---|---:|---|
| Architecture | **6/10** | Clean declarative separation and good artifact discipline, but no production runtime and too much duplicated policy machinery. |
| Safety | **4/10** | Strong refusal philosophy and least-privilege posture, but live safety is prompt-dependent and all factual claims are externally unverified. |
| Evaluation quality | **4/10** | Good negative testing of validators; weak semantic grading, narrow single-turn coverage, incomplete current run, and no grounding verification. |
| Documentation honesty | **5/10** | Frequently candid about risks, but undermined by stale counts, contradictory behavioral claims, and a successful shell exit despite an incomplete behavioral gate. |
| Production readiness | **2/10** | Suitable for a controlled prototype or evaluation exercise. Not suitable for real internal onboarding without runtime, observability, ownership, verified sources, and corrected release gating. |

## Bottom Line

This is not fake rigor; much of the static governance is real and thoughtfully designed. But it is still static governance around an unequipped model invocation. The repository has done more work proving that it knows its limitations than proving that it can safely operate in production.
