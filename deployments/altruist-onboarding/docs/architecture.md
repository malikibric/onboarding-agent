# Architecture

## Position in the repository

```
harperOS/
├─ core/                          blank master scaffold — NOT filled in place
│  └─ EXTENSIONS.md               documents evals/ and state/ as sanctioned additions
└─ deployments/
   └─ altruist-onboarding/        this agent — a deployment copy
```

`core/README.md` step 1: *"Copy `core/` to the client's workspace. Don't fill files in place here — this is the blank master."* Followed.

## The five layers, plus two

`core`'s fixed fill order is knowledge → skills → tools → feedback → enforcement, because each depends on the one before. This deployment adds `evals/` and (deferred) `state/`, declared as extensions in `core/EXTENSIONS.md` rather than folded in silently — otherwise the next deployment inherits an undocumented divergence from the master.

```
AGENT.md                identity, scope, mode routing, layer index. No facts.
check.sh                the release gate

knowledge/              WHAT IT KNOWS (nouns)
  CLAUDE.md               operative layer on core's 12 sections
  factbase.json           ← single authority for facts, tiers, provenance
  boundaries.json         ← single authority for what it refuses and where that routes
  public/*.md             human-readable prose; cites fact ids, establishes nothing
  quarantine (in factbase) unverified claims — present, indexed, NOT answerable
  validation-backlog.md   the promotion pipeline out of quarantine
  source-registry.md      the scheme, and the honest state of sourcing
  internal/               seven empty templates
  glossary-review.json    human approval record for high-risk definitions

skills/                 WHAT IT DOES (verbs)
  answer-or-refuse.md     the defining procedure          ← in the prompt
  onboard.md              day-one orientation             ← in the prompt
  glossary-lookup.md      define a term                   ← in the prompt
  explain.md              simplify an answerable concept  — NOT wired (DF-11)
  ask-better-questions.md turn a vague ask into questions — NOT wired (DF-11)

tools/access-policy.md  WHAT IT CAN TOUCH — read-only; the runtime control
feedback/corrections.md HOW IT IMPROVES — owner and backup required at runtime startup
policy/                 requests, honestly labelled (not enforcement)
evals/                  refusal suite (46 cases) + quality scenarios — evaluates the AGENT
enforcement/            gates.md, rules.json, validate.py (unmodified from core)
runtime/                prompt builder, shared runtime boundary, HTTP adapter, evaluators
verification/           agentcheck package + 128 tests
docs/                   this set
```

**A file in `skills/` is not a capability.** Only the three marked "in the prompt" are listed in
`build_prompt.py`'s `SOURCE_FILES`; the other two are inert. `SOURCE_FILES` — not the directory
listing — is the authority on what the agent actually has.

## Three design decisions that shape everything

### 1. One authority per fact

`factbase.json` is the only place a fact's tier and provenance are established. Prose in `public/` cites ids (`[ALT-003]`) and never re-establishes them. `agentcheck` proves every citation resolves to an answerable fact, and that the counts published in `source-registry.md` still match.

This exists because `core` warns repeatedly about the same information living in two places: *"someone updates one and the agent starts doing two different things."* The knowledge pack proposed twelve loose files and the old plan proposed ten more; either would have put the same fact in several files with no mechanism to keep them consistent.

### 2. Refusal is declared data, not prose

`boundaries.json` holds 15 boundaries. `skills/answer-or-refuse.md` references it and restates none of it. The eval suite proves every boundary has at least one test.

The alternative — a prose list of forbidden topics inside the skill — is what both input documents did, and it cannot be tested or counted.

### 3. Enforcement gates both the knowledge base and the conversation

`core`'s `validate.py` gates a file before it is sent, while `runtime/agent_runtime.py` applies a separate pre-send policy to live responses. The evaluator and HTTP adapter share this runtime boundary, so benchmark behavior cannot silently use a safer path than production.

The remaining risk is bounded by no-tools execution, bearer authentication, pinned model configuration, session-aware terminal refusals, redacted audit metadata, and fail-closed output checks.

## Data flow

```
altruist_onboarding_agent_knowledge.md ─┐
altruist-knowledge.md ──────────────────┼─> hand reconciliation ─> factbase.json ─┐
new-agent.md ───────────────────────────┘         (PLAN → quarantine only)        │
                                                                                   ↓
AUDIT_...md ─> boundaries.json ─> skills/ ────────────────────────────> the agent's answers
                     │                                                             ↑
                     └─> evals/refusal-suite.json ─> verification/ ─> gates ────────┘
```

The one-way arrow that matters: `new-agent.md` can put a claim **into** quarantine and can never put one into the answerable set. Enforced by `agentcheck` FB007 and tested twice.

## The prompt chain, and why editing certain files invalidates evidence

The system prompt is **built, not written**. This is the mechanic that surprises people, so it
is stated once here in full:

```
11 hashed source files ──build_prompt.py──> system-prompt.txt ──> the agent
        │                                          │
        └──> source_digest ──┐        ┌── prompt_digest
                             ↓        ↓
                      prompt-manifest.json          results.json.prompt_digest
                             └────── check.sh compares all three ──────┘
```

The eleven sources are listed in `runtime/prompt-manifest.json`: `AGENT.md`, five files under
`knowledge/`, `knowledge/public/02-glossary.md`, the three wired skills, and
`policy/behavioral-rules.md`.

**The consequence:** editing any one of them — even a typo fix — changes `prompt_digest`, and
`check.sh` then refuses the recorded behavioural result as "produced with a different prompt".
That is correct behaviour, not a bug: the evidence describes a prompt that no longer exists.
The cost is that a one-word documentation fix inside `AGENT.md` and a genuine safety change to
a boundary are indistinguishable to the gate, and both require a full live re-run (~46 model
calls). Budget accordingly, and batch prompt-source edits rather than trickling them.

Everything outside those eleven files — `docs/`, both `README.md`s, `runtime/*.py`, `check.sh`,
`verification/`, the two unwired skills — can be edited freely without touching the gate.
`check.sh` separately blocks if *any* file under `knowledge/` is newer than `results.json` —
including the unhashed ones — so that whole directory is effectively frozen between runs.

## Why Python, JSON, and no dependencies

- **Python** — `core/enforcement/validate.py` is already Python. Adding a second runtime for a system this small would be complexity for its own sake.
- **JSON** — matches `core/enforcement/rules.json`. Stdlib parsing, no install. YAML would be friendlier to hand-edit and would add a dependency to the release gate; declined.
- **No third-party deps in the runtime checks** — release gating must never break because an install is missing. `pytest` is used for tests only, where an install is a reasonable expectation.

## What this architecture does not do

- It does not provide cloud deployment, a database-backed session store, or a production secret manager. The stdlib HTTP adapter is a controlled reference boundary; deploy it behind an authenticated reverse proxy, provide an isolated `CLAUDE_CONFIG_DIR`, and replace in-memory sessions before horizontal scaling.
- It does not verify facts against the world. It enforces provenance discipline.
- It does not persist conversation content. It persists only redacted hashes and metrics for audit correlation, with `0600` permissions and configurable retention.
