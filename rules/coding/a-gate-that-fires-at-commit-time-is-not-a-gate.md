# A gate that fires at commit time is not a gate

**Task type:** coding — any process control meant to stop work from starting, as opposed to stopping
it from landing.
**Related:** [`a-correction-is-not-a-control`](../how-we-work/a-correction-is-not-a-control.md) — the
general form; this is the specific one that bites process rules written as prose.
[`write-the-prd-before-the-code`](write-the-prd-before-the-code.md) — the rule this was discovered
while testing.
[`validations-must-fail`](../testing/validations-must-fail.md) — why the test that found it had to
run in both directions.

---

## The rule

> **A rule that says "do not start X without Y" must be checked BEFORE X starts. If the only thing
> that catches it is review or commit, the rule does not prevent the work — it prevents the
> work from landing, after it has already been paid for.**

State which moment a control fires at, and if that moment is later than the one the rule names, say
so rather than counting it as enforcement.

## Why: the rule was tested, and it half-worked

A repo adopted *"no implementation without a PRD"* and wrote it at the top of the instructions file
every session loads. It was then tested with two agents, neither told the rule existed: one given a
new feature (the rule must fire), one given an already-reproduced defect fix (the rule must not).

**The discrimination worked perfectly.** The feature agent found the rule unprompted, read its
carve-out correctly, judged that a new feature did not qualify, and refused to commit. The control
agent proceeded and shipped. **A rule that fires on everything is not a control, and this one did
not.**

**But the feature agent implemented the entire feature first** — code, template, three tests — and
only *then* read the instructions and stopped itself. Roughly 130k tokens, in a repo whose own
policy charges compute against a cash ceiling, spent producing something that could never land.

**The instruction had been "all code is suspended". What actually happened is that code was written,
run and tested, then held at the door.** From the inside, that is indistinguishable from the rule
working — the agent reported a clean refusal, and the refusal was genuine.

## The ladder

`prose < checklist < test < gate`

**Prose at the top of a context file is the weakest rung**, because it competes with everything else
in that file and is read once, at a moment when there is no work to apply it to. It relies on the
agent remembering at the right instant, which is the definition of a control that fails silently
under load.

**Move it down the ladder as far as the rule allows.** For "no code without a PRD", the mechanical
form is a pre-commit hook refusing a diff that touches implementation files without a referenced
requirements document or a named reproduced defect. That converts *"the agent remembered"* into
*"the repo refused"*.

## Guard

- **Name the firing moment when you write the rule.** "Before starting" and "before merging" are
  different rules; pick one deliberately.
- **Test the control with an agent that was not told about it.** A control you have to point at is
  already relying on memory.
- **Test both directions.** One case that must fire, one that must not.
- **Count the cost of a late catch.** Work done and discarded is not free, and treating a late
  refusal as a success hides the bill.
- **Building the mechanical gate is usually itself governed by the rule.** That is correct, not a
  paradox — write its requirements down like anything else.

---

*Earned from:* testing a newly-adopted PRD rule on 2026-09-11 with two blind agents. It blocked the
right one and cleared the right one, and still let a full feature be built before it spoke.
