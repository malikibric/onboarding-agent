# Agent Deployment Toolkit

A method and a scaffold for standing up a client-facing AI agent. It splits an agent into five layers built in a fixed order, so that under time pressure nothing gets skipped and every deployment looks the same to whoever maintains it next. Copy `core/` per client; the skill that builds the knowledge layer travels inside it.

## Layout

```
core/                        the five-layer scaffold. Copy it once per client and fill it in.
  README.md                  the method: fill order, nouns vs verbs, the 30-minute version
  EXTENSIONS.md              evals/ and state/ — declared additions, not part of the master
  knowledge/
    CLAUDE.md                the knowledge layer — the file you fill in per client
    dedicated-knowledge/     the skill that builds CLAUDE.md from raw client material
    dedicated-knowledge.skill  packaged install of that skill (for Claude Code)
  skills/                    what the agent does
  tools/                     what it can touch
  feedback/                  how corrections flow back
  enforcement/               what it structurally cannot do

deployments/                 one directory per client. Never edited back into core/.
  altruist-onboarding/       a complete worked deployment — see below
```

## The worked example

`deployments/altruist-onboarding/` is this scaffold carried all the way through for one client: a new-hire onboarding agent built from public documents only, whose defining behaviour is refusing accurately rather than answering fluently.

It is the most useful thing in this repository if you are about to build your first agent, because it shows the parts the method does not: what a filled fact base looks like, how a refusal boundary becomes a testable object, how enforcement gets extended past `validate.py`, and what an honest release status reads like when three of the remaining blockers are human sign-offs nobody has given. Start at its `README.md`.

It also runs. `./check.sh` gates it, 128 tests cover it, and 46 eval cases have been run against a live model with the results checked in.

## The five layers

```
knowledge/    what the agent knows        (nouns — facts about the business)
skills/       what the agent does         (verbs — procedures, step by step)
tools/        what the agent can touch    (physical access; the real control)
feedback/     how the agent improves      (corrections flow back into knowledge)
enforcement/  what the agent cannot do    (structural checks, outside the model)
```

The order is fixed because each layer depends on the one before it:

- **Knowledge before skills** — a procedure written before you understand the business encodes your assumptions instead of theirs.
- **Tools after skills** — you can't decide what access is needed until you know the steps. Deciding access first always over-grants.
- **Enforcement last, and separately** — it's the only layer that must hold when everything above it is wrong.

## Nouns vs verbs

The most common mistake is putting the same rule in both knowledge and skills. Then someone updates one and the agent starts doing two different things.

- "Net 30 for trade accounts" → knowledge. It's a fact about the business.
- "Pull history, check stock, add alternates, generate PDF" → skill. It's a sequence.

If it's a fact, it lives in knowledge and the skill references it. Never both. Same for the knowledge file's own §6 (the process overview): scope, triggers, and handoffs live there; the executable steps live in the skill file.

## Using it

1. **Copy `core/` to the client's workspace.** Don't fill files in place here — this is the blank master.
2. **Build knowledge first.** Run the `dedicated-knowledge` skill — install `core/knowledge/dedicated-knowledge.skill`, or follow `core/knowledge/dedicated-knowledge/SKILL.md` by hand — on whatever raw material the client gave you (transcripts, SOPs, exports). It inventories the sources, extracts against twelve categories, tags every claim (untagged = verified, `[ASSUMED]` = inferred, `[MISSING]` = needed and unknown), writes `knowledge/CLAUDE.md` from `dedicated-knowledge/assets/CLAUDE-template.md`, and scores itself against a checklist. Report the score honestly, including a weak one.
3. **Skills:** one file per procedure, copied from `skills/_TEMPLATE.md`. Reference knowledge sections; restate nothing.
4. **Tools:** fill `tools/access-policy.md` *before* connecting anything. The "worst case if it goes wrong" column is the whole exercise.
5. **Feedback:** `feedback/corrections.md` starts empty and fills from day one. A correction isn't finished until it's in the knowledge.
6. **Enforcement:** fill the gate table in `enforcement/gates.md`, encode the machine-checkable rules in `enforcement/rules.json`, and wire `validate.py` in as a pre-send step. Prompt text is a request; only access, validation, and approval gates are enforcement.

## The 30-minute version

If you have 30 minutes, do this and nothing else:

- Knowledge: the vocabulary and the decision rules only. Skip company background.
- Skills: one procedure, the narrowest useful one.
- Tools: read-only.
- Feedback: just start the log.
- Enforcement: one real rule in `rules.json` that runs. One is enough to prove the pattern.

Narrow and finished beats broad and half-done. You can widen later; you can't un-ship a wrong quote.

## Running the validator

From the client's copy of `core/`:

```
python3 enforcement/validate.py quote.txt --rules enforcement/rules.json
```

Exit 0 = cleared to send. Exit 1 = blocked, with reasons:

```
BLOCKED — not cleared to send

  ✗ [VALUE-001] order value over inside-sales limit: found 61,450.00, limit 50,000.00 — requires Marcus / outside sales
```

A clean pass prints `PASSED — cleared to send`. Add `--json` for a machine-readable result. Things to know:

- A rule that can't be evaluated (bad regex, unparseable number) **fails closed** — it blocks rather than passes.
- A threshold rule that finds no value at all passes with a warning (`no value matched — … not verified`). Treat that warning as "a human checks the number".
- The shipped `rules.json` is a worked example from a fictional client (Meridian Abrasives). Replace every rule; keep the pattern of citing the knowledge section each rule comes from.
- A passing validator is not a reason to stop reading the output. It catches rule violations, not bad judgment.

## What this toolkit does not do

- It doesn't wire anything up. No tool connections, scheduling, hosting, or logging — `validate.py` is the only thing that executes.
- It doesn't make prompts enforceable. Anything the model can be talked out of is a request, not a control; real limits live in withheld access and the validator.
- It doesn't catch output that is valid but commercially stupid. That's what escalation thresholds and human review are for.
- It doesn't maintain itself. The feedback loop is a process the client's process owner must run; if corrections require a developer, they stop the week you leave.
