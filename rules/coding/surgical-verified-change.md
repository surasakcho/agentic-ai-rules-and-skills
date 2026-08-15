# Surgical, verified change

**Task type:** coding — modifying an existing system.

---

## The rule

**Touch only what you must; clean up only your own mess.** Every changed line should trace
directly to the request.

- Don't "improve" adjacent code, comments or formatting.
- Don't refactor what isn't broken. Match the existing style even where you'd do it
  differently.
- If you notice unrelated dead code, **mention it, don't delete it**.
- Do remove imports, variables and functions that *your* change made unused.

## Verify before, and after

Turn the task into a verifiable goal before starting: "add validation" becomes "write tests
for invalid inputs, then make them pass"; "fix the bug" becomes "write a test that reproduces
it, then make it pass". Strong success criteria let you work independently; weak ones ("make
it work") need constant clarification.

Commit after each verified milestone. A committed checkpoint is cheap; losing verified work
is not.

## The remediation paradox

> **Incident.** A remediation fixed 15 audited findings and **introduced 11 new defects doing
> so**. Six surfaced only when someone asked whether the outputs had been reviewed. Two were
> the *same mistake made twice on the same day*.

Fixing is when defects are introduced, because the fixer is moving fast through code they
have just understood for the first time. The countermeasures:

- **After each fix, check what the fix touched** — not just whether the original symptom is
  gone.
- **Watch for the same mistake twice.** If two defects share a mechanism, the mechanism is the
  bug, and a third instance is probably already written.
- **A fix that moves the metric the wrong way is information.** Enumerate candidate mechanisms
  and measure to discriminate before changing anything again.

## Two mistakes worth memorising

**"This run's list" is not "everything that exists."** Any code that deletes or overwrites
based on a computed set must know whether that set is complete or partial. Full run → replace.
Partial run → merge, or refuse.

> Cost, in one project, on one day: a cleanup deleted **317 files**; the same shape truncated
> a **321-row** metadata table to **5 rows**. Both were written and tested on a full run,
> where "this run's list" and "everything" happen to coincide.

**Write the partial case first.** It is the one that loses data.

**A convention needs a stated domain.** A rule that is right inside its domain becomes a
defect outside it — a fixed 0–1 display scale, correct for variables spanning that range,
wasted half the range on variables topping out at 0.449 and hid the study's main gradient.
