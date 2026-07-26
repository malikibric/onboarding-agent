# Feedback Loop

Two loops. Almost everyone builds the first and forgets the second, which is why most agents are exactly as good in month six as on day one.

## Loop 1 — within a run

The agent checks its own output before it leaves: validation, format checks, a second pass. Cheap and mechanical. Handled in `enforcement/`.

## Loop 2 — across runs

A human corrects the agent. That correction goes back into knowledge or skills, so it never has to be made again.

This is the loop that matters, and it's a process problem more than a technical one. The failure mode is silent: someone fixes the output by hand, ships it, and never tells anyone. The agent stays wrong. Nobody notices because the work got done.

**So the rule is: a correction isn't finished until it's in the knowledge.** Fixing the output is treating the symptom.

## Correction log

Every entry ends by naming the file that changed. If nothing changed, the loop didn't close.

| Date | What it got wrong | Root cause | Fixed in |
|---|---|---|---|
| | | missing knowledge / wrong rule / bad step / out of scope | knowledge §X |

### Root cause categories

- **Missing knowledge** — it never knew. Add to knowledge.
- **Wrong rule** — it knew something false. Correct knowledge, and check where the false version came from.
- **Bad step** — knowledge was right, procedure was wrong. Fix the skill.
- **Out of scope** — it shouldn't have attempted this. Tighten scope or add a stop condition.

Most early corrections are the first category. If you're still seeing lots of them after a few weeks, discovery was too shallow — go back and interview.

## Review

- Weekly at first: read the log, apply anything not yet applied.
- Watch for repeats. The same correction twice means it was fixed in the output, not in the knowledge.

## Who owns it

The person who owns the process, not the person who built the agent. If corrections require a developer, they stop happening the week you leave.
