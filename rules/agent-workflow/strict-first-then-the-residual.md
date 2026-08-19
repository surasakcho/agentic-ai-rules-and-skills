# Strict first, even when it hurts — then propose what to do with the residual

**Task type:** universal. Every project, every language, every domain — any task where a general
solution will not cover every case.
**Related:** [`unexpected-means-stop-and-propose`](unexpected-means-stop-and-propose.md) — what to
do when the strict pass surprises you.
[`exact-match-on-a-complete-key`](../data-engineering/exact-match-on-a-complete-key.md) — this
rule applied to one domain.
[`close-your-own-gaps`](close-your-own-gaps.md) — the boundary: closing your own rigour gap is
phase 1, not phase 2.

---

## The rule

**Build the strict, exact, straightforward solution first — even when you can already see it will
not cover everything, and even when the difficulty is the reason you want to avoid it.**

**Then treat what it does not cover as a separate, second phase: enumerate the residual, and
propose a disposition for each item.** Never assume one. Never skip phase 1 because you expect it
to be hard. Never merge phase 2 into phase 1 by building the accommodation in advance.

## Why the accommodation must not be built first

The tempting move is to foresee the difficulty and handle it up front — a fallback branch, a
tolerance, a default, a retry, a special case, a `try/except` that continues. It feels like
competence. It destroys three things at once:

- **The residual becomes unmeasurable.** If the fallback absorbs the hard cases, you never learn
  how many there were. *How many* is the single most useful number the task can produce, and it
  only exists between phase 1 and phase 2.
- **An accommodation built in advance is indistinguishable from a requirement.** Six months on,
  nobody can tell whether the tolerance was necessary or merely precautionary — so nobody removes
  it, and nobody trusts the strict path either.
- **Difficulty is information, not an obstacle.** The strict pass failing on 755 items is a
  measurement of the real problem. Softening the pass does not reduce the difficulty; it moves it
  inside the output where nobody can see it.

## It is universal, not a data rule

| domain | phase 1 (strict) | phase 2 (residual, proposed) |
|---|---|---|
| joins / lookups | exact key equality only | unmatched rows, each with a decision |
| parsing | strict parse, reject on anything unexpected | the rejects — which are the spec's real edge cases |
| migration / refactor | move everything that maps cleanly | what does not map; usually the actual project |
| types | strictest types the compiler allows | each escape hatch, named and justified |
| dependencies | exact pins | each range, with the reason it must float |
| tests | assert the exact expected value | each loosened assertion, with why |
| performance | plain correct implementation | optimisation — and the plain version stays as the oracle |
| error handling | let it raise | each swallowed error, with what is known to be safe |

In every row, the phase-2 column is a **list you can hand to someone.** That is the test of
whether you did this correctly.

## Never bypass — the three bypasses, by name

- **Pre-emptive tolerance.** Writing the fuzzy fallback, the `± epsilon`, or the `or default`
  before the strict version has ever been run. You do not yet know it is needed.
- **The absorbing fallback.** A chain — `strict → loose → looser` — where the output records only
  the value and not which branch produced it. Three qualities of result in one column, and no way
  to audit any of them. **If a branch label is computed, it must be persisted.**
- **The silent phase-merge.** Doing phase 2 in your head while writing phase 1, so the residual
  never becomes a list and never reaches the person who should decide it.

## What phase 2 owes

- **Enumerated, not counted.** "17 unresolved" is a status; the 17 rows are a deliverable.
- **A proposed disposition per item**, with evidence — and an explicit *"this one is yours"* label
  for the cases that genuinely cannot be settled without the owner's judgement. That label is the
  point of the exercise; everything else you can resolve yourself.
- **Its cost.** What each disposition would take, so the owner can decide what is worth doing.
- **Everything that does not depend on the answer, already finished.** Escalating is not stopping.

## The incident

A matcher was written with a similarity fallback so that a name-based lookup would "work". It did
work — every row got a value, nothing raised, totals reconciled. The strict version was never run,
so the residual was never measured.

An audit years later ran the strict pass for the first time: **~154 rows per year had been landing
on the wrong entity**, the total silently inflated wherever a correct row arrived too, and a
sibling consumer had placed **20% of its reference locations** by the same fallback with no guard
at all. None of it was visible, because the accommodation had been built before anyone found out
how large the problem actually was.

**The strict pass would have been harder on day one and correct ever since.**

---

*Earned from:* user instruction — *"Do all things straightforward and exact solution first even if
it will lead to difficulty. Then handle what remains later by propose me sound solution. Never
assume or bypass these steps."*
