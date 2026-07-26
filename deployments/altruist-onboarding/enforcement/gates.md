# Enforcement

Boundaries that hold regardless of what the model decides.

## The distinction, applied to this agent

`core/enforcement/gates.md`: *"if the agent can be talked out of it, it isn't enforcement."*

The old build plan filed a list of behavioural rules under the heading "Enforcement". Every one was prompt text. That list now lives in `policy/behavioral-rules.md`, correctly labelled as requests. What follows is what actually holds.

## The structural problem this deployment had to solve

`core`'s validator checks **a file before it is sent**. This agent's output is **conversational** — there is no pre-send artifact to gate. The audit flagged that neither input document noticed this, and that left unaddressed the agent would ship with prose guardrails only.

Resolution: **gate the knowledge base at build time instead of the conversation at runtime.** This agent's dominant failure mode is knowledge-borne, not phrasing-borne — it says wrong things because it *knows* wrong things, or because a boundary was never declared. Both are catchable before anyone talks to it.

## Gates for this deployment

| # | Rule | Enforced by | Blocks or warns |
|---|---|---|---|
| 1 | The agent has no credential to reach any internal system, send anything, or write to its own knowledge | **Absence of access** — `tools/access-policy.md` | block (structural) |
| 2 | `new-agent.md` can never make a claim answerable | `agentcheck` FB007 | block |
| 3 | Every answerable fact has a tier, a source, and a checked date | `agentcheck` FB001–FB009 | block |
| 4 | A fact marked sensitive cannot exist without its mandatory attribution | `agentcheck` FB006 | block |
| 5 | No fact may claim external verification without recording the source | `agentcheck` FB013 | block |
| 6 | Prose cannot cite an unknown or quarantined claim as fact | `agentcheck` CI001–CI003 | block |
| 7 | Every refusal boundary routes to a slot that exists on disk | `agentcheck` BD002 | block |
| 8 | Every declared boundary has at least one refusal test | `agentcheck` EV003 | block |
| 9 | At least 20 must-refuse cases exist | `agentcheck` EV006 | block |
| 10 | Published fact counts match the fact base | `agentcheck` RG001 | block |
| 11 | Public knowledge files contain no manager reference, team routing, entitlement promise, internal tool name, competitor name, or security assurance | `validate.py` + `rules.json` | block |
| 12 | Facts older than 180 days are surfaced | `agentcheck` FB010 | warn |

Gate 1 is the strongest and the cheapest, and it is the only one that operates at runtime. Everything the agent could do that would be genuinely dangerous — reading an internal system and paraphrasing it, writing an unreviewed fact into its own knowledge, mailing something to a colleague, storing employee data — is prevented by not existing.

## Running it

```
./check.sh                     # both gates
cd verification && python3 -m agentcheck          # structural only
cd verification && python3 -m agentcheck --strict # warnings block too
python3 enforcement/validate.py knowledge/public/01-company-and-mission.md --rules enforcement/rules.json
```

Exit 0 = clear. Exit 1 = blocked, with reasons. A rule that cannot be evaluated **fails closed** — `validate.py` blocks rather than passes, and `agentcheck` refuses to report success on a deployment it could not load.

## What these rules cannot do

Stated plainly, because overclaiming here would be the same error the agent exists to prevent.

- **This layer does not inspect live answers.** The shared runtime boundary in `runtime/agent_runtime.py` performs pre-send checks; this build-time layer remains responsible for artifact integrity and release status.
- **Regex cannot tell quotation from assertion.** `rules.json` is scoped to `knowledge/public/*.md` and deliberately excludes `CLAUDE.md` and `skills/`, both of which quote forbidden phrasings as worked counterexamples. A file that says *"never say 'you get benefits from day one'"* is indistinguishable to the linter from one that asserts it. This is why the scope is narrow rather than the rules being weak.
- **A known miss:** the entitlement rule matches `you'll receive` / `you will receive` but not the bare `you get`, because the counterexample in `05-culture-and-values.md` uses that phrasing to teach against it. The rule is a floor, not a ceiling.
- **They cannot check that a claim without a citation should have had one.** `FACT-001` requires *at least one* citation per file; it cannot detect the third paragraph that quietly asserts something unsourced. That is a human review job, listed as test gap TG-02.
- **They do not verify anything against the world.** Every fact carries `external_verified: false`. These gates enforce internal consistency and provenance discipline, not truth.

Don't let a passing gate become a reason to stop reading the output.
