---
name: sprint
description: The engineering process for this estate - PRD before code, goal-based sprints, mockups before UI, and two task files per repo. A thin router; invoke it whenever engineering work is starting, being planned, being reviewed, or when someone asks where a task lives.
---

# The engineering process

**A router. It holds the four things that must always be true and sends you to ONE file for the
rest.** Load only the branch you need — that is the whole point of the shape.

## The four invariants

1. **No implementation without a PRD.**
   [`write-the-prd-before-the-code`](https://github.com/surasakcho/agentic-ai-rules-and-skills/blob/3901f3a/rules/coding/write-the-prd-before-the-code.md)
   is the rule; read it rather than working from any summary. **Binding, not advisory.**
   *One carve-out, narrow on purpose: a fix to a defect that is already found, already written down
   and already reproduced is not new engineering. If you are arguing that something is "really just
   a fix", it is not.*
2. **No UI built before a mockup the owner has seen.** Screens are mocked in the browser, brand
   assets in Canva. Two different branches below, and the split is deliberate.
3. **Every task lives in exactly two files, per repo:** `docs/kanban.md` (the current sprint) and
   `docs/backlog.md` (everything else). **A task recorded anywhere else does not exist.** Find one
   in a plan, an ADR or a decision row: move it, leave a pointer.
4. **A sprint is a goal, not a date.** It ends when its committed list is done, or when it is
   declared failed. Never on a calendar.

## ⚠️ The stop condition belongs to every branch, and is not an exception to any of them

> **Written once, reviewed once. Round two of ANY document must name what would make you ABANDON it
> rather than revise it. There is no round three without a reason that is not "it could be better."**

**This is load-bearing.** The PRD rule cites this estate by number as the cautionary case for the
*opposite* failure: thousands of lines of design documents, a seven-round review costing roughly
four times the experiment it described, and nothing shipped at all. **A process that can only
produce documents is the failure it was built to prevent, wearing a new name.**

**The test, at any moment: name the artifact that ships if the next check comes back positive.**
No such artifact means the process has stopped converging.

## Branches — read ONE, not all

| you are… | read |
|---|---|
| about to build something | [`prd.md`](prd.md) |
| starting or planning a sprint | [`sprint-plan.md`](sprint-plan.md) |
| finishing or abandoning a sprint | [`sprint-close.md`](sprint-close.md) |
| about to build or change a **screen** | [`mock-screen.md`](mock-screen.md) |
| making a **logo, social image or brand asset** | [`mock-brand.md`](mock-brand.md) |
| tidying, merging or migrating tasks | [`board.md`](board.md) |

## A repo that has neither file yet

Create `docs/kanban.md` and `docs/backlog.md`, version-controlled. `board.md` carries the templates
and the migration procedure. **Do not create them empty and call the repo compliant** — the tasks
already exist, scattered across plans and decision rows, and finding them IS the migration.
