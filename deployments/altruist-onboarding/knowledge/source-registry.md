# Source Registry

> **Canonical machine-readable authority: `factbase.json`.** This file explains the scheme and records the honest state of sourcing. It deliberately does not restate facts — two authorities drift.

## The headline, stated plainly

**Not one fact in this system is externally verified.**

All three input documents — the primary knowledge pack, the secondary knowledge file, and the old build plan — assert facts about Altruist without citing a single resolvable URL, retrieval date, or primary source. The audit flagged this as gap F2 and it remains open.

Consequently every entry in `factbase.json` carries `external_verified: false`. The tier system records **document provenance inside this repository**, not verification against the world.

**Two of these documents agreeing is corroboration between unverified secondary artifacts.** It raises confidence a little. It is not proof, and it must never be described as confirmation. This is the exact failure mode the agent exists to prevent in a new hire, so the system must not commit it itself.

## Documents

| Id | Path | Role | Authority | Cites external sources |
|---|---|---|---|---|
| `PACK` | `altruist_onboarding_agent_knowledge.md` | Primary grounding document | Highest | No |
| `SEC` | `altruist-knowledge.md` | Secondary domain context | Supporting | No |
| `PLAN` | `new-agent.md` | Old strategic draft | **None** | No |

`PLAN` carries no authority by decision, not by oversight. It can move a claim *into* quarantine; it can never move one into the answerable set. See `docs/decisions.md` D-02.

## Tiers

| Tier | Answerable | Meaning | Required hedge when speaking |
|---|---|---|---|
| `P1` | Yes | Stated in `PACK`. | None. |
| `P2` | Yes | Stated in `SEC`, and `PACK` states a compatible overlapping or weaker form. | State plainly; flag promotional claims as positioning. |
| `P3` | Yes | Stated in `SEC` only; `PACK` silent. `PLAN` agreement adds nothing. | **Attribute:** "Altruist's public materials describe…" |
| `Q` | **No** | `PLAN`-only, contradicted across documents, or a specific figure inflating a vaguer sourced claim. | Not answerable. Route to `validation-backlog.md`. |

Additionally, facts with `sensitive: true` carry a mandatory `attribution` string that must be delivered *with* the fact. Currently: `ALT-011` (careers/benefits messaging), `ALT-027` (regulatory), `ALT-028` (Hazel security), `ALT-031` (competitive positioning).

## Current counts

| Tier | Count |
|---|---|
| P1 | 12 |
| P2 | 2 |
| P3 | 18 |
| **Answerable total** | **32** |
| Quarantined | 19 |

Counts are asserted by `verification/agentcheck` at lint time and will fail the build if this table drifts from `factbase.json`.

## How a fact gets promoted

Quarantine → answerable requires **all** of:

1. A resolvable external source (URL or document reference) recorded on the fact.
2. A retrieval date.
3. For anything regulatory, financial, or security-related: confirmation from an internal owner, not just a public page.
4. An entry in `feedback/corrections.md` naming what changed.

Promotion is a deliberate act by a named human. Nothing promotes automatically, and no agent may promote a fact about itself.

## How a fact goes stale

The release gate now enforces freshness: `check.sh` runs `agentcheck --strict`, so the old plan's "refresh the fact base monthly" is backed by a blocking 180-day window. What exists instead:

- Every fact carries `checked`.
- Lint warns on any fact whose `checked` date exceeds the staleness window (default 180 days).
- In normal inspection the check remains a warning; the release gate promotes it to blocking and requires an explicit refresh before shipping.

This is a known weak point, recorded as risk R-04.
