# Parallel variants must share an identical variable set

**Task type:** data engineering — multi-source ingestion, benchmark/cross-check datasets,
A/B variants of a derived measure.

---

## The rule

When the same quantity is measured from more than one source, or produced in more than one
variant, **every variant ships the same set of variables** — same names modulo the source
prefix, same derivations, same units, same missing-value convention.

A variant that carries a column its sibling lacks is not a richer variant. It is a broken
comparison.

The whole reason to carry two measurements of one quantity is to check them against each
other. That check silently fails when the two are different shapes — and it fails in the
direction that looks like a **finding** rather than a defect. The analyst reads a definitional
gap as a data discrepancy and writes it up.

## Enforce it by construction, not by discipline

Put the derivation in **one function that takes the source prefix**, and have every variant
call it:

```python
def derive(df, prefix):
    """Given {prefix}_count_{a}_{b} and {prefix}_total_{b}, add every derived column."""
    ...

df = derive(df, "source_a")
df = derive(df, "source_b")
```

Two implementations that agree today are two implementations that will disagree after the next
edit. The shared function is also where the missing-value convention lives, so that cannot
diverge either. A change to the denominator rule then lands on **both variants or neither**.

## The four ways variants drift

All four of these were present in a single block of one real panel, discovered together:

| Drift | What it looked like |
|---|---|
| **Names** | `count_senior_male` sitting beside `srcb_count_senior_male` — no prefix on one of them |
| **Coverage** | One source published only a share-of-total; the other published share-of-total *and* within-group. The missing pair was computable from columns already shipped |
| **Denominators** | Two columns with parallel names whose denominators differed by ~2×, and nothing in either name to say so |
| **Missing values** | One wrote `0` where the denominator was zero; the other wrote NULL |

**The fabricated `0` is the dangerous one.** A 0% share on a unit with no population is a value
nobody measured. It passes every null check, survives every `dropna`, and lands in the mean.
In the incident below, 1,209 such rows had been inflating a published correlation from
**+0.23 to +0.34**; removing them changed the headline number.

A share is undefined when its denominator is zero. Write NULL.

## Check it

- **Assert the schemas are identical modulo prefix**, in the same self-test that asserts
  anything else about the block. Then a new variant fails loudly instead of shipping
  half-formed.
- **Assert that any classifier or grouping over the columns covers all of them.** After a
  rename, twelve columns fell into an `unclassified` bucket and were invisible — caught only
  because a downstream consumer required its groups to *partition* the column set, not merely
  to match most of it.
- **Never address parallel records by list position.** A caption that quoted example `[1]` from
  a results list kept rendering after a rename, with the right format and the wrong pair. Look
  up by name and raise when the name is absent.

## Migrating an existing pair

The measured quantity is usually the raw counts; everything else is a pure function of them.
So the migration needs no re-ingestion — rename the counts, drop the derived columns, and
re-derive through the shared function.

**Prove the equivalence rather than asserting it:** check that each re-derived column
reproduces the value the old code wrote, everywhere the old code wrote a defined one. In the
incident below that came out at 4.4e-14, which is what made the rename safe to ship.

---

*Earned from:* two independent measurements of the same population structure — one modelled
from raster, one from an administrative register — shipped side by side for months so they
could be benchmarked against each other, while differing in names, denominators, coverage and
missing-value convention. Nobody had compared them, because comparing them did not work.
