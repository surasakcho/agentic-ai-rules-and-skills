# Handoff

## Next Session

### What this session was

The Rules Sector office, working the appointment brief and then a long run of
incident-driven authoring with the Core session. **65 commits, all pushed, working tree
clean.** Corpus went 81 → 92 rules and 66 → 68 skills.

State at handoff, measured rather than recalled:

```
rules: 92   skills: 68   leaks: 0   broken links: 0   duplicate slugs: 0
gated: 8   UNGATED: 77   unavailable: 7   UNKNOWN: 0
```

**Read `gated: 8` narrowly.** It asserts the named implementation *exists* — not that anything
invokes it. **Nothing in this repo invokes any of the eight**: `core.hooksPath` is unset, there is
no hooks directory, `.git/hooks` holds only samples. Every clause now carries `invoked_by:` saying
so.

---

### ⚠️ READ FIRST: replacing this corpus with upstream as master

A directive is reported to be in flight to **replace the forked `skills/` with
`mattpocock/skills` as master**. Before that happens, read
[`skills/UPSTREAM.md`](skills/UPSTREAM.md) — it exists to answer exactly this, and it was written
from a measurement, not a preference.

**`skills/` is already a fork of that repository.** Its `package.json` still carries the upstream
name, URL and MIT licence, and upstream's `LICENSE` is vendored beside it. So this is not an
adoption question, it is **how a fork takes upstream changes** — and the measured sets are:

| | |
|---|---|
| ours | **68** |
| upstream (at pin `3cca18b`) | 37 |
| in both — the decision set | **26** |
| upstream-only | 13 |
| ours-only | **42** |

**What a wholesale replacement discards:** 42 skills that exist only here, and our side of 26
overlaps — including `tdd`, which is **38 lines upstream and 108 here**. That is a rewrite somebody
did for a reason, and an installer resolves it by overwrite, in install order, reporting what it
installed rather than what it replaced.

**The recommendation on record is lossless-by-default**, and it is the operator's own constraint
that produced it — *"I want the better one to win, but we cannot tell that right away."* Keep ours,
date every per-skill verdict with a reason, and re-ask when evidence arrives. **Four of the 13
upstream-only skills are in upstream's own `in-progress/`.**

If the decision is nevertheless to take upstream wholesale, **it is a decision and not a
housekeeping step** — say so, record which 42 + 26 are being dropped, and do not let an installer
make it silently.

---

### Open, and none of it this office's to move

All with the operator, filed on `zkyhax-empire` by the Core:

- **the gate-debt charter defect** — this office publishes clauses it structurally cannot
  discharge, so `a-classification-is-not-a-gate` is unsatisfiable here by construction. The only
  thing keeping that honest is `skills/check-rule-gates/` exiting non-zero.
- **the tamper-gate fix** (`#5`), the **locality `known_gap` verdict value**, **`#11`** (the
  auditor's own charter), **`#17`** (containers serving a stale `~/.claude/CLAUDE.md`).
- **`#14`** — nine repos with no declared owning session; declaring one is a capability grant, so
  it is not backlog.

### Recorded debt, with counts

- **77 rules classified gateable and ungated.** Deliberate: the clause is safe to publish *only
  because* `check-rule-gates` counts it as a gap and exits 1. **If that checker is ever removed,
  77 rules silently become documented controls that do not exist.**
- **17 of 34 tracked shebang files are `100644`.** Not 17 defects — this corpus documents its tools
  interpreter-prefixed, so `100644` is right — but **not one says so in itself**, and the work owed
  is a line per file. See `rules/testing/what-the-harness-supplies-it-cannot-test.md`. **Do not fix
  this with a bulk `chmod`**; that asserts an executable interface these files do not have.

### Caveat on anything read from host rules this session

`~/.claude/CLAUDE.md` inside this container was **frozen ~28 hours** by a single-file bind
mount that captured the inode at container start. Confirmed by execution: zero occurrences of any
marker written on 2026-09-13. Every governance ruling acted on this session arrived **by peer relay
and was treated as a relay** — see the second precondition in
`rules/how-we-work/relayed-authority-is-information-not-instruction.md`, which is about exactly
this: a corroborating artifact can be stale without saying so, and its silence is
indistinguishable from the relay having been invented.

### Suggested skills for the next session

`rules-in-force` at start · `check-rule-gates` before trusting any coverage number ·
`ship-a-rule` when authoring · `lesson-review` for the actual weekly pass, which this session
was **not**.
