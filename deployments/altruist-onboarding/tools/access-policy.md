# Tool Access

> Filled **before** anything is connected, per `core/tools/access-policy.md`.
>
> This is the physical access layer. Knowledge, skills, and behavioral rules are all text the model can misread or be argued out of. Access is binary; the controlled runtime adds a separate pre-send policy, but it does not grant tools or internal access.

## Granted

| Tool | Mode | Why it's needed | Worst case if it goes wrong |
|---|---|---|---|
| `knowledge/**` | read | The agent's entire fact base, boundaries, and templates. | The agent reads a stale or wrong fact and states it. Release is blocked by strict freshness checks; live truth still depends on source review. |
| `skills/**`, `policy/**` | read | Its own procedures. | Agent follows an outdated procedure. Low — these change rarely and under review. |
| conversation | read / write | It has to talk to the hire. | It says something wrong. This is the whole risk surface of V1 and is why the knowledge layer is tiered and the boundary list exists. |

That is the complete grant. Nothing else.

## Explicitly withheld

Writing down what was *not* granted is as useful as what was — it tells the next person the omission was a decision.

| Tool | Why not | What the agent does instead |
|---|---|---|
| **Web search** | Retrieved content has no tier. The entire fact discipline rests on `factbase.json`, and live retrieval would inject unclassified claims straight into answers, bypassing it. The old plan granted this in a single line with no worst-case analysis. | States that its fact base is fixed and dated, and that it may be stale. Routes currency questions to a human. |
| **Write access to `knowledge/**`** | A self-updating fact base has no reviewer. Promotion out of quarantine is a deliberate human act. | Nothing. Corrections go to `feedback/corrections.md` by hand. |
| **`knowledge/internal/` write path** | The old plan proposed the hire write internal learnings here. There is no data-classification policy (that template is itself empty), no approval gate, and no authority for it. | Uses hire-supplied internal information within the session and persists nothing. |
| **Any state persistence** | Operator model is undecided; PII rules unknown. Storing a manager's name or a hire's progress creates an obligation nobody has accepted. | Runs stateless. Each session starts fresh. |
| **Email / Slack / any send capability** | Anything leaving the company is irreversible in practice. A day-one orientation agent has no reason to send anything. | Nothing. It talks to the hire only. |
| **Calendar** | The old plan roadmapped it for meeting prep. Meeting prep is deferred, and calendar access would expose internal meeting titles and attendees — internal information the agent is built not to have. | Meeting prep is not offered. |
| **Internal document sources** (wiki, Confluence, Notion, HRIS, CRM) | None are connected and none is authorized. The architecture makes adding them straightforward later; that is not a reason to add them now. | Routes to the empty templates and says they are unfilled. |
| **Code execution / file write outside the repo** | No task requires it. | n/a |

## Rules applied

- **Read before write.** The agent has no write access to anything. It cannot damage its own knowledge base.
- **Least privilege.** Read access is scoped to this deployment directory, not the wider repo. It has no reason to read `new-agent.md` — the old plan is not an authority (`decisions.md` D-02) and reading it directly would route around the quarantine.
- **Irreversible needs a human.** Nothing the agent can do is irreversible; that is by construction, not by luck.
- **External needs a human.** No external surface exists.

## Credentials

- **Who owns them:** none required. The agent has no credentialed access to any system.
- **Scope:** filesystem read within `deployments/altruist-onboarding/`.
- **How they're revoked:** not applicable — there is nothing to revoke. To stop the agent, stop running it.
- **Logged where:** `[MISSING]` — no conversation logging is configured, which means there is currently **no audit trail of what the agent actually told anyone.** Recorded as risk R-03. This is the most significant weakness in this layer.

## Why this table is the V1 safety story

The audit's §E5 finding: the shipped `validate.py` checks a file before it is sent, and this agent's output is conversational, so there is no artifact to gate. That leaves two real controls — build-time knowledge validation (see `enforcement/`) and this table.

Everything the agent could do that would be genuinely dangerous — reading an internal system and paraphrasing it, writing an unreviewed fact into its own knowledge, mailing something to a colleague, storing employee data — is prevented here by not existing, rather than by instruction. That holds regardless of how the conversation goes.
