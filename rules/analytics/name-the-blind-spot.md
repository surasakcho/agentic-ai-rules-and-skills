# Name the check's blind spot before you read its answer

**Task type:** analytics, data engineering — any measurement, audit, reconciliation or diff
whose number you intend to act on.
**Related:** [`validations-must-fail`](../testing/validations-must-fail.md) — a guard that never
fires. This is its mirror: a check that *does* fire, returns a number, and is believed.
[`a-delta-is-three-numbers`](a-delta-is-three-numbers.md) — one instance of the null space, and
the most common one.
[`report-both-sides-of-a-comparison`](report-both-sides-of-a-comparison.md) — the reporting
discipline once the check is trustworthy.

---

## The rule

Every check has a **null space**: the set of changes to the data that leave its output
unchanged. **Write that sentence down before you read the result.** If the defect you actually
care about lives in the null space, the check is not evidence about it — no matter what number
it returns, and no matter how reassuring the number is.

## Why a broken check hides a defect instead of revealing one

A check's output is a statement **about the subject**. It has no vocabulary for its own failure.
So when the instrument is wrong, you do not get silence, an exception, or a null. You get a
confident, well-formed claim about the data.

Four incidents from one project, four different mechanisms, one shape:

| the check reported | the truth | what it was actually measuring |
|---|---|---|
| "0 corrupt values in any text column" | 164 rows corrupt across 15 values | the guard tested one codec's byte signature; the *other* codec's corruption lands inside the target script's own Unicode block and passes cleanly |
| "0 of 77 groups match; source B is 1.7–19.1% low" | 77/77 match, max absolute difference **0** | it summed the 204 single-year age columns on one side against a grand total that also includes 12 supplementary columns sitting outside them |
| "14,786 name mismatches" | approximately none | the names had been decoded with the wrong codec; the corruption entered a *matcher*, where "no match" is indistinguishable from legitimate absence |
| "coverage +951" | +951 filled **and 12 silently lost** | a net is `gained − lost`, and subtraction cannot show cancellation |

Not one of them said *"I might be broken."* Every one blamed the data.

## The concealment mechanism, stated precisely

**The check's wrong answer landed inside the range its correct answer was expected to occupy** —
and in three of the four, arrived with a corroborating story:

- *"B is low, worst in border and highland groups"* is exactly the gradient a genuine
  definitional difference would produce.
- *"the names are corrupt"* was **partly true** — an independent audit later found 100 genuinely
  corrupt names. The instrument was lying and the accusation was real.
- *"coverage improved by 951"* was the migration's stated purpose. It hit its target.

A defect that produces an absurd number is a defect that gets fixed in ten minutes. The ones that
survive are the ones that produce the number you were expecting.

## Detection: what actually found each of them

| # | found by | works when |
|---|---|---|
| 2, 3 | **implausible magnitude** — a perfect `0 of 77`, a count larger than the population could support | the defect is large |
| 1, and a fifth (100 corrupt names) | **an independent method disagreeing** — a second auditor, a document parsed for an unrelated purpose | someone else is looking |
| 4 | **a structural partition run unconditionally** against a baseline captured before the change | always |

**Now sort the same four by harm.** The two caught by implausibility were harmless: they were
checks, they cost hours, they were loud. The two that reached or nearly reached shipped data —
the corruption certified clean, and the twelve blanked rows — were the quiet ones, and **neither
was caught by looking at the number.** One was caught by an outsider; one by structure.

**Implausibility is the detector we reach for by default, and it is anti-correlated with harm.**
Its sensitivity scales with the size of the defect, while a data defect's damage scales with how
far it travels — and travelling far requires looking normal. A defect big enough to look wrong is
a defect too small to ship.

## Guard

1. **State the null space in one sentence, before reading the result.** Literally: *"what could
   change without moving this number?"* `net = +951` → *a loss offset by a gain*. `0 corrupt
   found` → *any corruption outside the byte range I tested*. `sum(A) vs total(B)` → *any column
   inside B's total but outside A's sum*.
2. **Raise the resolution until the defect leaves the null space.** A scalar in which two errors
   can cancel is not a check; it is a summary. Partition it — gained/lost/changed/unchanged,
   per group, per column.
3. **Validate each side against itself before comparing sides.** An internal identity within one
   source — details plus supplements equal the stated total — needs no second source, and it is
   the only thing that catches an extraction error before it is misread as a disagreement.
4. **Run a positive control in the same invocation as the real check.** A deliberately corrupted
   string through the corruption guard; a deliberately blanked row through the delta. A check
   validated on a separate occasion is a check whose current wiring is unverified.
5. **Treat an exoneration as the weakest result a check can return.** "Nothing found" is the one
   answer consistent with both a clean subject and a dead instrument. Never report it without
   saying what would have had to be true for the check to see something.

---

*Earned from:* four checks in one project that each returned a well-formed, plausible number
about the data while actually reporting their own defect — a codec guard testing the wrong byte
range and certifying 164 corrupt rows as clean, a reconciliation summing 204 detail
columns against a total that also covered 12 columns outside them, and concluding two identical
sources disagreed, a mis-decoded join key
producing 14,786 phantom mismatches, and a net coverage figure that read `+951` identically with
and without a bug that blanked twelve rows. The two loudest were harmless. The two that shipped
were found by an outside party and by a structural partition, not by anyone judging whether the
number looked right.
