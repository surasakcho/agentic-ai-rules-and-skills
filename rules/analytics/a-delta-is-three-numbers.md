# A delta is three numbers — gained, lost, changed. The net is none of them

**Task type:** data engineering, analytics — any rebuild, migration, backfill or source switch
where you compare an output against the version it replaces.
**Related:** [`report-both-sides-of-a-comparison`](report-both-sides-of-a-comparison.md) — the
same discipline applied to a *join* rather than to a *change over time*.
[`completeness-checking`](../data-engineering/completeness-checking.md) — partitioning a gap,
which is what you do once these three numbers disagree.
[`verify-conversions-against-the-original`](../data-engineering/verify-conversions-against-the-original.md)
— the baseline you diff against has to be captured *before* you start.

---

## The rule

**When an output changes, report how many values were newly filled, how many were replaced, and
how many were lost — separately, every time. Never report the net movement.**

A net figure is not merely imprecise. It can be **exactly correct while the composition
underneath it is wrong**, because a loss and a gain of the same size cancel and leave no trace.

## The failure, concretely

A pipeline was migrated from a name-keyed source to a code-keyed one. Coverage went up by 951
rows, and the migration looked clean:

```
coverage: 65,541 -> 66,492   (+951)
```

The first version of that migration also contained a bug that **silently blanked 12 rows** that
previously had values. After the bug was fixed, coverage read:

```
coverage: 65,541 -> 66,492   (+951)
```

**Identical.** The twelve losses were exactly offset by twelve gains elsewhere. The headline was
true both times and told you nothing. Only a row-level diff against a pre-change baseline
separated them:

| | with the bug | after the fix |
|---|---|---|
| newly filled | 963 | **951** |
| **lost** | **12** | **0** |
| net | +951 | +951 |

Had the net been trusted, the dataset would have shipped with twelve entities blanked and the
commit message would have said `+951` — truthfully.

## Why "coverage went up" is the most dangerous kind of true

A net gain reads as unambiguously good news, so it does not invite scrutiny the way a net loss
would. That asymmetry is the trap: **the direction of the headline suppresses the check that
would have found the defect.** A rebuild that reports a net *loss* gets investigated
immediately; one that reports a net gain gets committed.

## Guard

- **Capture the baseline before you start.** You cannot diff against a file you have already
  overwritten. This is one `cp` and it is the whole precondition for the rule.
- **Report the three counts separately**, keyed on the join key, for every changed column:
  `newly_filled`, `replaced`, `lost`.
- **`lost` must be zero, or explained per row.** In a rebuild that is meant to add data, any
  loss is a defect until individually accounted for.
- **Also count what did NOT change**, and which columns were untouched. "0 of 337 unrelated
  columns changed" is what turns a rebuild into a *surgical* rebuild, and it is a stronger claim
  than any figure about the columns you did intend to touch.
- **Never let a net stand alone in a commit message, report or status line.** If it appears, the
  three components appear beside it.

## The specific bug underneath it, worth its own check

The defect was an **inverted lookup table**. A crosswalk mapped `key_a -> key_b`; the migration
applied it in reverse. Both columns were unique — 21 rows, 21 distinct values each — so it
looked like a clean bijection.

It was not safely invertible, because **6 of its target values were themselves legitimate keys**
in the frame being joined to. Reversing the map made those ambiguous, and the ambiguity was
resolved silently in the wrong direction.

**The table was not a rename map, which is what made the inversion look harmless.** The frame
carried two kinds of polygon — the administrative units themselves, and municipality polygons
overlaid on them — each with its own key, and the crosswalk recorded which unit each municipality
belonged to. Both keys in every pair were real frame rows, and **the upstream source published
only one of them**. So reversing the map moved each record off the unit the source names directly
and onto the municipality it never names: the municipality filled, the genuine unit emptied, and
the two cancelled to a net of zero.

**Carry both counts, because they answer different questions.** Six targets intersect the key
space — that is what the guard returns, and the number to assert on. Only **five** could actually
mis-seat: the sixth mapped to *itself*, a leftover identity row, so reversing it is a no-op. The
cheap test deliberately over-counts, and that is correct; what is not correct is quietly reporting
the smaller number as if it were the guard's. Here the write-up drifted to "five" and stayed wrong
for a day.

**Uniqueness on both columns does not make a mapping invertible.** The test is whether the
codomain intersects the domain:

```python
assert not (set(table.target) & set(valid_keys)), \
    "these targets are also valid keys -- inverting this mapping is ambiguous"
```

One set intersection. It prints the answer immediately, and it was not run.

---

*Earned from:* a source migration that reported `+951` coverage with and without a bug that
blanked twelve rows, the loss exactly offset by gains elsewhere. Found only by diffing row by row
against a baseline captured before the rebuild. The underlying defect was a lookup table inverted
without checking that its targets were not also keys — six of them were.
