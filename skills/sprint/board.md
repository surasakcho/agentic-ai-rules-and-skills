# The two files, and how to migrate into them

**Every task in a repo lives in `docs/kanban.md` or `docs/backlog.md`. There is no third place.**

| file | holds | rule |
|---|---|---|
| `docs/kanban.md` | **the current sprint only** | committed work, in progress, done. Nothing speculative |
| `docs/backlog.md` | **everything else** | ranked. Anything not committed to a sprint |

## Why two and not one

A single list makes "what am I doing now" and "what might we do" the same question, and the second
always crowds out the first. **The kanban is short on purpose — if it is long, the sprint was not a
commitment.**

## `docs/kanban.md`

```markdown
# Sprint — <goal as an outcome>

**Abandon if:** <written when the sprint opened, not now>
**Ships:** <the artifact that exists when this succeeds>

## Committed
- [ ] **<id>** <task> — owner: <who> — blocked by: <what, or nothing>

## In progress
## Done
- [x] **<id>** <task> — <commit>
```

## `docs/backlog.md`

Ranked. Each row: a stable id, the task in one line, **who owns it**, **what blocks it**, and a
pointer to where the detail lives. **The blocker column is the one that earns its keep** — a board
where everything says "nothing" is not being read honestly.

## Migrating a repo that has tasks scattered

**This is the real work and it is not mechanical.**

1. **Sweep everywhere tasks hide**, not just the obvious file: plans with `owed` columns, decision
   rows flagged for review, ADR follow-ups, dashboards with "waiting on" prose, parked knowledge-base
   entries with revive conditions, open tracker issues, and `TODO`/`FIXME` in code.
2. **For each, judge three things**: is it still open, is it a duplicate of another row, and does it
   exist in only ONE place. **That last one is why a reorganisation loses work** — a task recorded
   once, in a file being restructured, disappears silently.
3. **Contradictions are findings, not noise.** Two files disagreeing about a task's status means at
   least one is lying to every session that reads it. Resolve it against evidence and say which was
   wrong.
4. **Leave a pointer where you took it from**, so the next reader is not told two different things.
5. **Anything that looks done but was never marked done** — verify and close it. Stale open rows are
   how a board stops being read.

## Keeping it honest

**A board is state, not commitment.** The kanban carries commitment; the backlog carries state.
**Never reorder the backlog silently on someone else's behalf** — ranking is a judgement its owner
makes when they look at it.
