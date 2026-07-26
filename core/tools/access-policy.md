# Tool Access

Fill this in **before** connecting anything. Access decided after the fact is always too wide.

This is the only layer that's physical. Knowledge, skills and enforcement-as-prose are all text the model can misread. Access is binary — it either has the credential or it doesn't. That makes it the strongest control available, so spend the thought here.

## Granted

| Tool | Mode | Why it's needed | Worst case if it goes wrong |
|---|---|---|---|
| | read / write | | |

The last column is the whole exercise. If you can't fill it in, don't grant the access yet.

## Explicitly withheld

| Tool | Why not | What the agent does instead |
|---|---|---|
| | | escalates to [who] |

Writing down what you *didn't* grant is as useful as what you did — it tells the next person the omission was a decision, not an oversight.

## Rules

- **Read before write.** An agent that only reads cannot cause damage. Start there and widen once it's proven on real cases.
- **Least privilege.** Narrowest scope that finishes the job. Not "the whole CRM" but the objects it actually needs.
- **Irreversible needs a human.** Anything that can't be undone — sending, paying, deleting, publishing, committing — goes through approval until there's evidence to remove it.
- **External needs a human.** Anything leaving the company is irreversible in practice, whatever the API says.

## Credentials

- Who owns them:
- Scope:
- How they're revoked:
- Logged where:

If nobody can answer how to turn it off in thirty seconds, it isn't ready to be on.
