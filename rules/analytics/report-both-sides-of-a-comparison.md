# Every comparison reports both sides: what matched, and what did not

**Task type:** analytics — any time you compare two datasets, two files, two runs, two versions.
**Related:** [`completeness-checking`](../data-engineering/completeness-checking.md) is how to
find what is missing; this is how to report what you found.

---

## The rule

**When you compare two things, state explicitly what agreed and what disagreed, with counts and
scope for each. Never summarise a comparison with a single adjective, and never let a statement
about one comparison be read as a statement about a different one.**

A comparison has two results, not one. "They match" is not a finding. This is a finding:

> 7,240 of 7,580 rows match on all 33 compared fields; 340 do not; 8 keys exist only on the
> left and 6 only on the right.

The second form is barely longer and cannot be misread.

## What every comparison must state

| Element | Why it is not optional |
|---|---|
| **The two populations and the exact join key** | With counts on each side *before* the join, so rows that fell out are visible rather than silently absent |
| **Matched: how many, of how many possible, on which fields** | "Matched" without a denominator is not a rate |
| **Unmatched: how many, on which fields** | Never "a few", "mostly", "minor differences" |
| **Rows on only one side — both directions, counted separately** | A join reports agreement only for rows that survived it. The ones that did not are the most likely place for the real defect |
| **The tolerance and any normalisation applied** | Equality at 1e-6 relative, with two spellings folded together, is a different claim from byte equality |
| **Fields excluded, and why** | An excluded field is a decision, not an absence |

## Scope the claim to the comparison that produced it

This is the failure that actually happened.

I verified that reordering a table's columns had not altered any value, and reported **"0 values
changed."** True — and a statement about *old file vs new file*. In the same message I had
separately measured *our output vs an external reference* at **95.51%**, i.e. 340 rows
disagreeing. The reader took "changed nothing" to mean "identical to the reference" and asked
directly whether that was what I meant. It was not, and the phrasing invited it.

**Name both sides in the sentence that carries the verdict.** "The reformat changed no value in
our file" and "our file still differs from the reference on 340 rows" are both short, and neither
can be mistaken for the other.

## A percentage is not a conclusion

95.51% agreement is worthless until the 4.49% is partitioned into causes. When that residual was
finally broken down, the largest bucket turned out to be **our own defect** — a set of rows whose
areas were computed in the wrong map projection — which the aggregate figure had been quietly
averaging into a reassuring number.

**Report the residual as a partition with a cause per bucket.** If a bucket is unexplained, say
"unexplained" and give its size, rather than rounding it into the matched pile.

## "Close enough" needs a number attached

Say the measured difference and the threshold you are judging it against. Two things that agree
to 4.9e-05 and two things that agree to 5.6 percentage points are both "close" in prose and are
not remotely the same fact. In the incident above they were the difference between a harmless
projection artefact and two genuinely different source vintages — one to ignore, one to go and
fix.

## The mechanisable part

A comparison report can be generated rather than written. Emit, from code:

- both input row counts, the join key, and the joined count
- per-field mismatch counts at a stated tolerance
- left-only and right-only key counts, separately
- the residual grouped by an assigned cause, with an explicit `unexplained` bucket

Then gate on it: if the bucket counts move between runs, fail, so a change in the residual has
to be explained before it ships rather than being absorbed into a percentage.

---

*Earned from:* a data pipeline compared against an independently-produced reference file. The
headline "95.51% match" concealed that the single largest cause of disagreement was a defect on
our side, and a separately-scoped "0 values changed" was read as a claim of full agreement.
