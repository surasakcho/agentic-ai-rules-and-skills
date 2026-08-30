# Record your thinking before complex work — then verify it, then answer

**Task type:** agent workflow — any complex question or multi-step task, before the first
action is taken.
**Related:** [`unexpected-means-stop-and-propose`](unexpected-means-stop-and-propose.md) — both
rules exist to stop a fluent answer from substituting for a checked one.
[`strict-first-then-the-residual`](strict-first-then-the-residual.md) — plan the strict pass
before building around it.

---

## The rule

**Before answering a complex question or doing a complicated task, write a step-by-step plan
into `thinking/thinking-<slug>.md` at the project root. Verify that plan before acting on it —
against the actual files, data, or constraints involved — and only then answer or implement.**

"Complex" means: more than one plausible approach, a claim that would be expensive to retract,
or a task where a wrong first step compounds (schema changes, multi-file refactors, anything
touching shared state). A one-line lookup or a single obvious edit does not need this.

## Why writing it down first, not just thinking it

An unwritten plan is invisible to verification — there is nothing to check it against, and
nothing that survives if the reasoning goes stale mid-task. Writing it to a file:

- forces the steps to be concrete enough to falsify, instead of staying vague enough to feel right
- gives the user something to review if they ask what the approach is
- gives *you* something to re-read after a tool call changes the picture, instead of trusting
  memory of a plan that assumptions have since invalidated

## Why verify before acting, not after

The point of the file is not documentation — it is a checkpoint. "Verify" means confirming the
plan's assumptions against reality before spending effort executing it: does the file this step
assumes exist actually exist, does the API this step assumes have this shape actually have it,
does the number this step depends on actually check out. A plan that looks reasonable and a plan
that is correct are different things, and the gap between them is exactly what silent, confident
mistakes are made of.

## Scope

- One file per task, named for what it's solving, not the date.
- Lives at the project's root under `thinking/`, not in the session scratchpad — it should
  survive the session if the task does.
- Superseded plans stay in the file (or the folder) rather than being deleted; a wrong turn is
  itself useful context for later.

---

*Earned from:* proactive practice, no incident yet — added on user instruction rather than
extracted from a failure. Flagged as a deviation from this repo's normal bar (a rule enters only
after a real incident); revisit this line if/when a concrete incident supersedes it.
