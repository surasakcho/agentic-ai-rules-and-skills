# Never commit a compressed or converted copy without checking it against the original

**Task type:** data engineering — compressing, re-encoding, downsampling, or converting a data
file into another format, especially to make it small enough to commit.
**Related:** [`check-for-a-local-copy-before-refetching`](check-for-a-local-copy-before-refetching.md)
— that rule tells you to prefer the committed copy; this one is why the committed copy has to be
proven equivalent first. [`validations-must-fail`](../testing/validations-must-fail.md) — the
aggregate check below is only worth writing if it can fail.

---

## The rule

**A converted copy is a claim of equivalence. Measure it before committing, on the statistic the
pipeline actually computes, against the original — and include at least one total that would
change if data were lost.**

Not "it opened fine." Not "the dtype looks right." Not a spot-check of one cell. **Recompute the
downstream aggregate from both copies and compare the totals.** Loss shows up in a sum long
before it shows up in an eyeball.

Write the measurement into the converter's own docstring, with numbers. A conversion script that
asserts equivalence in prose and never measured it is worse than one that says nothing, because
the prose is what the next reader trusts.

## The incident

A pipeline needed ~38 GB of population raster tiles that were gitignored as "re-downloadable."
A sibling script converted them to a committed form — rounding each pixel to a 32-bit integer,
which compressed to 3.4 GB (9% of the original) because integers repeat and most of each tile
was a constant nodata sentinel.

Its docstring stated: *"Rounding error washes out over any unit's worth of pixels (thousands),
so it has no material effect on the zonal-stats sums the consumer actually computes."*

**Nobody measured that.** Measured later, comparing zonal sums over ~7,600 administrative units:

| raster | loss vs original |
|---|---:|
| total population | **−0.32%** |
| one sex's total | **−5.42%** |
| a single age band | **−87.83%** — 6,949 of 7,583 units went to **exactly zero** |

**Why the "washes out" intuition is exactly backwards.** The source held *fractions of a person
per pixel*. Rounding to an integer is not noise scattered around the true value — it is a
**one-directional floor applied before the sum**. Almost every pixel floors to 0, and a sum of
zeros is zero. So the error **compounds with pixel count instead of averaging away**: the bigger
the unit, the more it loses. The intuition only holds where values sit comfortably above 1,
which is why the total-population raster survived and the age bands were annihilated.

**Cost, and how narrowly it was avoided.** The converted copies sat committed and unread for
weeks — harmless. The damage was armed later, by a *different, well-motivated* change: pointing
the consumer at the committed copies to avoid the 38 GB download. That single line would have
rewritten the entire age-sex block with near-zero counts on the next rebuild.

It surfaced only because the consumer had an unrelated internal guard — *"a unit with population
> 0 must not have an age-sex total of 0"* — which aborted a test run. **The obvious reading was
that the guard was too strict** for the small subset being tested. The guard was right and the
data source was wrong.

## What to actually check

- **The downstream aggregate, both ways.** Whatever the pipeline computes — a zonal sum, a row
  count, a group-by total — compute it from the original and from the conversion, and report the
  relative difference. This is the check that catches loss.
- **Per-category, not just the grand total.** The grand total here lost 0.32% and looked fine;
  a single age band lost 87.8%. **An aggregate over everything can hide a catastrophe in one
  slice.** Break it down by whatever dimension the data is used along.
- **A count of newly-zero / newly-null entries.** "How many units went from a positive value to
  exactly zero?" is a single number that would have screamed here: 6,949.
- **A checksum or hash where the conversion claims to be lossless.** If the claim is *exact*
  round-trip — a container change, a re-encode at the same precision — then prove it exactly:
  convert back and compare digests, or hash the decoded arrays. A lossless claim deserves a
  byte-level check, not a tolerance.
- **The range that survives the type.** Before rounding or narrowing a dtype, ask what fraction
  of the values are *below the new resolution*. If most of the data is smaller than one unit of
  the target type, the conversion does not lose precision — it deletes the data.

## Guard

Before committing a converted copy, or pointing anything at one:

1. Recompute the pipeline's own statistic from both copies.
2. Report the difference **per category**, plus a count of values that became zero or null.
3. Put those numbers in the converter's docstring. If you cannot state the measured loss, you
   have not verified the conversion.
4. Treat any downstream guard that fires on the converted data as **evidence about the data**,
   not as a guard that needs relaxing.

---

*Earned from:* an int-rounding raster compression whose docstring asserted the error "washes out
over thousands of pixels," which destroyed up to 87.8% of a population age band because the
per-pixel values were fractions of a person. Committed unmeasured; caught only when an unrelated
consumer-side guard aborted, and only after that abort was nearly dismissed as a too-strict
threshold.
