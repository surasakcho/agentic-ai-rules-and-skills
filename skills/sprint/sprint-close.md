# Closing a sprint

**Two ways to close and both are legitimate: DONE, or ABANDONED against the condition written when
it opened.** A sprint that can only be closed by finishing teaches nothing.

## The close, in order

1. **Move every finished item to `## Done` in `docs/kanban.md`** with the commit that finished it.
2. **Unfinished items go BACK to `docs/backlog.md`**, each with one line on why it did not land.
   **Do not roll them silently into the next sprint** — a task that has failed to land twice is
   telling you something about itself.
3. **Did the abandon condition fire?** If it did and you continued anyway, write down why. That
   sentence is the most valuable thing the sprint produced.
4. **Name the artifact that shipped.** If none did, say so plainly rather than listing activity.
   *Documents produced, checks run and reviews completed are not artifacts.*
5. **Record what you now know that you did not before**, and where it is written down.

## The honesty rule

**Report failures with their evidence, skipped work as skipped, and finished work plainly.** A close
that reads as unbroken success across every item is describing a plan that was never ambitious
enough to be informative.

## Then

Open the next sprint via [`sprint-plan.md`](sprint-plan.md), or stop. **Stopping is a legitimate
outcome** and needs no justification beyond there being nothing worth committing to yet.
