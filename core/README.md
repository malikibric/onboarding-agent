# Deployment Scaffold

One copy per client. The method, the nouns/verbs rule, and the 30-minute version live in the toolkit README one level up — this file is just the map.

```
knowledge/CLAUDE.md                   what the agent knows — the file you fill in per client
knowledge/dedicated-knowledge/        the skill that builds CLAUDE.md from raw client material
knowledge/dedicated-knowledge.skill   packaged install of that skill (for Claude Code)
skills/_TEMPLATE.md                   one file per procedure; reference knowledge, restate nothing
tools/access-policy.md                decide access before connecting anything
feedback/corrections.md               starts empty; fills from day one
enforcement/gates.md                  the gate table, and how the layers differ from prompt text
enforcement/rules.json                machine-checkable rules — replace the fictional example set
enforcement/validate.py               pre-send check; exit 0 = clear, exit 1 = blocked
```

Fill in that order: knowledge → skills → tools → feedback → enforcement.

**Knowledge first.** Run the skill in `knowledge/dedicated-knowledge/` (see its `SKILL.md`) against the client's raw material. It writes `knowledge/CLAUDE.md` from `dedicated-knowledge/assets/CLAUDE-template.md`.

**Then make at least one enforcement rule actually run** before the agent touches anything real:

```
python3 enforcement/validate.py <output-file> --rules enforcement/rules.json
```
