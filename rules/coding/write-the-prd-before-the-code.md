# Write the PRD before the code

**Task type:** coding — any implementation beyond a one-line fix: a feature, a service, a tool, a
schema, a script someone else will run.
**Related:** [`agree-the-output-contract-first`](../data-engineering/agree-the-output-contract-first.md)
— the same discipline for a pipeline's output, and the narrower case this generalises.
[`record-thinking-before-complex-work`](../how-we-work/record-thinking-before-complex-work.md) — a
plan for how you will work; a PRD is a statement of what is being built and for whom, and they are
not substitutes.
[`open-decisions-go-in-the-tracker`](../how-we-work/open-decisions-go-in-the-tracker.md) — where the
questions a PRD surfaces go while they are unanswered.

---

## The rule

> **No implementation begins without a written PRD: what is being built, for whom, what it must do,
> and what would make it done.**

It is written down, in the repo, before the first line of implementation — not reconstructed
afterwards from what got built, which is a description rather than a requirement.

**Four things, and a PRD missing any of them is not one:**

1. **The user and the problem.** Who has it, and what they do today instead.
2. **What it must do** — the behaviour, in terms a non-implementer can check.
3. **What it explicitly will NOT do.** The out-of-scope list is the half that survives contact with
   a deadline, and the half nobody writes.
4. **Done.** The condition under which this ships. Not "it works" — a statement someone else could
   evaluate without asking you.

**Scope it to the work.** A PRD for a small tool is a paragraph and a bullet list. The rule is that
it exists and is agreed before code, not that it is long. Length is not the deliverable.

## Why: this fails in both directions, and most rules only guard one

**Building with no PRD.** A studio's own charter assigned design, implementation, grading and
outreach to four separate roles. **Three games were built single-handed before anyone noticed the
charters were unused** — not by decision, by drift. Nothing was written down that anyone could have
checked the build against, so there was no moment at which the divergence became visible. **A rule
living only in someone's head cannot be violated, because there is nothing to compare against.**

**And the opposite, which a PRD rule can cause.** An incubator in the same estate produced
**8,093 lines of design documents and zero shipped listings**; one document took **seven review
rounds costing roughly four times what running the experiment it described would have cost**, and
every round found real defects while the design never changed shape. A separate assessment measured
that operation at **1,879 lines of code, zero tests, and nothing ever shipped.**

**So a PRD that cannot end is not a PRD, it is displacement activity onto the tractable** — and it
is indistinguishable from rigour from the inside, because every individual round is defensible.

## The stop condition is part of the rule, not an exception to it

**A PRD is written once and reviewed once.** A second round names what would make you abandon the
document rather than revise it. There is no third round without a stated reason that is not "it
could be better."

**Write the ship condition in the same breath as the requirement.** If no outcome of the PRD would
license writing code, the document is not deciding anything.

**A PRD is not a design, an architecture, or a schedule.** It says *what* and *for whom*. The moment
it starts specifying *how*, it has become the implementation in prose — slower to write, impossible
to run, and now a second thing to keep in agreement with the code.

**Questions it surfaces go to the tracker, not into the document as open threads.** A PRD carrying
six unresolved questions is a meeting agenda; a PRD carrying six links to tracked decisions is a
requirement with known gaps.

## Guard

- **Written and in the repo before implementation** — a PRD agreed verbally is a memory, and the
  code will be the only surviving record of what was agreed.
- **The out-of-scope list is mandatory.** A PRD with no exclusions has not been thought about.
- **"Done" must be checkable by someone who did not build it.**
- **One round, then a stated stop condition.** Round two names the abandon criterion.
- **If the PRD changes after code exists, change the PRD** — and say so in the commit. A silently
  amended requirement is how the implementation becomes its own specification.
- **Do not write *how*.** If it specifies functions, tables or endpoints, it stopped being a PRD.

---

*Earned from:* an operator directive, 2026-09-10, grounded in the same estate failing both ways —
three games built with no written design because charters existed and were never read, and an
incubator that produced 8,093 lines of documents, a seven-round review costing four times the
experiment it described, and nothing shipped at all.
