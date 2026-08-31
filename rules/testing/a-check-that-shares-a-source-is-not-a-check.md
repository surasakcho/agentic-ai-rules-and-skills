# A check that shares a source with its subject is not a check

**Task type:** testing — validators, guards, reconcilers, and the fixtures that exercise them.
**Related:** [`validations-must-fail`](validations-must-fail.md) — run a check against input you
know is broken. This rule is the next question: *who decided what "broken" looks like?* If the
answer is "the same person who wrote the bug," the check inherits the bug and passes.
[`a-pr-nobody-is-asked-to-review-is-invisible`](../how-we-work/a-pr-nobody-is-asked-to-review-is-invisible.md)
— "verify the effect, not the exit status" is the same distrust aimed one layer lower: at what a
command *reports*, rather than at where a check gets its expectation.

---

## The rule

**A check must derive its expectation from somewhere other than the thing it is checking.**
Not a different function in the same module — a different *source*: the vendor's own record, a
second implementation, a figure computed months earlier by someone else, the real broken input.

An expectation derived from the buggy path agrees with itself and reports green. This is not a
failure of diligence. It is what happens by default, because the blind spot travels from the
implementation to the checker through the author's model of the problem, and **synthetic test
input is its main vector.**

## The incidents

All four are from a single day, in a codebase whose author was actively trying to prevent
exactly this.

### A guard that passed against the very defect it was written for

A live trading strategy computed a market signal over a rolling 30-day window. Its price history
was assembled by concatenating stored files with a live API call, and nothing checked that the
two **met**. They did not: the files ended 8 weeks before the API window began. The resampler
silently dropped the empty periods, so the 90-bucket window spanned 84 calendar days instead of
30 and **87% of the signal was two months stale.**

A guard was written to refuse a signal computed across a hole. It scanned the gaps *between* the
rows inside the window — and against the real 54-day hole it saw nothing but clean 1-hour steps,
and **passed.** The hole was at the window's *left edge*: the data simply did not reach back far
enough. An interior scan cannot look there.

The guard would have passed a synthetic test too, because the author would have generated an
interior hole — that being the author's model of what a hole is. It was caught only by running
it against production data.

**Cost:** nearly shipping a guard whose sole purpose was to catch a defect it demonstrably did
not catch.

### A fixture that back-filled the bug

A test pinned the invariant "the booked rate is a full 8-hour period, never a partial." Its
synthetic price series was generated from a fixed start to a fixed end, and `now` was set
*inside* that range — so the "still open" period was fully populated with data that, in reality,
had not happened yet. The pre-fix implementation therefore looked **correct** under test.

Caught only because the test also replayed the old implementation and asserted it booked exactly
0.125 of a period. That assertion failed, which is how the fixture's error surfaced.

### A checker that reproduced its own target bug

A tool was written to stop "I did not check X" being reported as "X does not exist." While being
written, it reported a repository as backed-up on the grounds that the files were *tracked* —
without checking they had been **pushed**. It committed the precise error it existed to prevent,
one layer up.

### A mechanism inferred from the code, refuted by the venue

A sleeve was under-booking income by ~8×. Reading the code produced a confident mechanism:
"it misses 7 of 8 payments." A reconciler that derived expected income from the **exchange's own
settlement history** — deliberately not from the code path under suspicion — refuted it within
the hour: payment counts matched exactly (26 venue, 24 booked). The entire gap was in *rate
magnitude*, not payment count.

The cause turned out to be adjacent to the guess, but the *symptom* was wrong, and a fix built
on it would have been confidently wrong. **The refutation was only possible because the
expectation came from outside the code.**

## Why the obvious defences do not work

- **"I tested it."** Against input you constructed from the model that produced the bug.
- **"I reviewed it."** With the mind that wrote it.
- **"The check failed correctly when I broke it."** You broke it *the way you imagine it
  breaks*. Real defects are shaped by the thing you did not think of — that is why they are
  defects.

## Guard

- **Name the source of the expectation, out loud, before writing the check.** If it is "the same
  module," "my understanding of the format," or "a fixture I wrote," you have a consistency
  check, not a verification. Those are useful, but they cannot find a wrong *model*.
- **Run every new checker against the real defect, in production data, before believing it.**
  Not a reconstruction of the defect. The reconstruction is the thing under suspicion.
- **Replay the broken implementation inside the test** and assert it goes red — including the
  specific wrong value it produces. This catches fixtures that have quietly encoded the bug, and
  it is the only check on this page that costs almost nothing.
- **Prefer an external record over a second opinion.** A vendor's API, an invoice, a number
  derived independently months earlier. When a conversion reproduced a figure written into a
  project's docs long before, that agreement meant something no internal check could have
  established.
- **When a checker and its subject disagree, do not assume the subject is wrong.** Half the time
  this session it was the checker.

## The tell

Ask: **if my understanding of this problem is wrong, would this check still pass?**

For a check that shares its source with its subject, the answer is always yes — and that is
precisely the case you need it for. A check exists to catch what you did not think of. One built
from what you did think of cannot.

---

*Earned from:* a continuity guard that passed against the 54-day hole it was written to catch; a
test fixture that generated data past `now` and made the pre-fix implementation look correct; a
backup-coverage tool that reproduced its own target bug while being written; and a confidently
reasoned failure mechanism refuted in under an hour by an expectation derived from the exchange
instead of from the code.
