# Check completeness against the source, never against a previous output

**Task type:** data engineering — ingestion, joins, aggregation.
**Related:** [`inspect-what-you-downloaded`](inspect-what-you-downloaded.md) — the acquisition-side failure that produces most clustered gaps.

---

## The rule

Enumerate what the output *should* contain from the **source of truth** — the raw inputs, the
authoritative entity list, the spec — and prove every expected item is present.

**Never validate completeness against a previous output.** A prior run cannot reveal something
that was never ingested; if the last version was missing a province, comparing against it
certifies the same gap as correct.

Check **both directions**: expected items absent from the output, and output items with no
source counterpart. Check at every level that can silently lose data — whole files or groups,
entities within a group, fields within an entity.

## Missing data rarely looks missing

It arrives as a plausible zero, an empty string, a default, or a dropped row that nothing
counts. Verify counts against the source; never infer completeness from the absence of nulls
or errors.

Treat a silent skip as a defect. Warnings that nothing fails on, `try/except` that continues,
a glob that quietly matches nothing — all should become hard failures.

## A whole-group gap is a bug until proven otherwise

When the output population does not match the input's, **do not report it as an accepted
limitation yet**. A mismatch is far more often a fixable processing failure than genuine
absence.

> **Incident A.** A pipeline reported 132 "missing" units as an accepted limitation. **125 of
> them were an entire province**, silently locked in as "done" by a caching bug that checked
> whether a cached file *existed* but never whether it was *good*. The source data was live
> and downloadable the whole time.

> **Incident B.** An audit of the same dataset identified two provinces with a genuine
> upstream gap. A third province had the identical gap and nobody had noticed — it surfaced
> only once the silent skip was converted into a hard failure. **The audit had found two of
> three.**

Genuine absence is normally scattered — a few tiny islands. Clustered absence — an entire
province, an entire delivery batch — is a strong signal to investigate rather than report.

**Read any "we checked and found N" claim as a lower bound.**

## Cache validity is part of completeness

A cache check that tests existence rather than integrity will serve a truncated download
forever. Verify cached artifacts against a checksum or the source's reported content length,
not `size > 0`.

## Every pipeline compares its output population to its input population

Not "does the output look plausible" — **count the input's units, count the output's, and state
both.** Whatever the natural unit is (records, entities, files, deliveries), the comparison runs
on every build, and **an exact match is the expectation most of the time**. Where it is not, say
in advance why not, so a shortfall is measured against a stated expectation rather than a
feeling.

## When they do not match: three outcomes, and only three

A mismatch is never left as a number in a report. It resolves to exactly one of these, and the
choice is written down:

1. **Resolved.** The cause was found and fixed, the counts now reconcile. State the cause, not
   just the new number.
2. **Explained and accepted.** The gap is genuine, the reason is understood and evidenced, and
   the affected units are **enumerated** — not summarised as a count. An accepted gap with no
   list of what is in it cannot be re-checked later.
3. **Open, with a proposed route.** You could not resolve it. Then the deliverable is the
   *route*: what you tried, what it would cost, and the single thing you need from someone else.
   Never a shrug.

**"Investigated, cause unknown, size N" is a legitimate outcome. "Roughly matches" is not.**

The decision, whichever it is, goes in the log with its evidence — because the next person to
see the same shortfall will otherwise re-derive it from scratch, or worse, assume someone
already decided it was fine.

## The gap's SHAPE tells you which outcome you are in

This is the cheapest discriminator available, and it works before you know anything about the
cause:

- **Scattered** — a few units here and there, unrelated, each tiny. Usually genuine absence.
- **Clustered** — an entire group, an entire batch, an entire period, all-or-nothing within it.
  **Almost always a defect.** Real-world absence does not respect your grouping keys.

> **Incident D.** A demographic block was missing for 753 of ~20,000 unit-periods, ~3.8%, and
> the profile looked convincingly genuine: the missing units were overwhelmingly tiny islands,
> median area 1,023 against 27,087 for the population as a whole, and the same units recurred
> every period.
>
> Partitioning by group and period broke it in two. **651 were genuine.** The other **102 were
> two entire regions, in one specific period, at 100%** — dense urban regions with no islands
> at all, whose units carried every *other* variable in the dataset including a sibling block
> from the same agency. Adjacent periods were complete.
>
> The cause was three ~1.3 KB stub files served with a successful HTTP response and cached as
> good (see [`inspect-what-you-downloaded`](inspect-what-you-downloaded.md)). **The aggregate
> 3.8% concealed it completely** — it was visible only once the gap was partitioned by group ×
> period and the shape of each bucket examined.

**Never report a completeness figure as a single percentage.** Partition it, give a cause per
bucket, and if a bucket is unexplained say "unexplained" and give its size.

## Derived identifiers must follow the identity

When a record's key is corrected, every column derived from that key must be recomputed.

> **Incident C.** A unit's code was corrected from one province to another. The correction was
> applied to the key everywhere — but a *derived* `province_code` column kept the old value,
> and a province-level economic variable was joined through it. The unit continued to receive
> the wrong province's figure, **a 23% error**, which is precisely the defect the correction
> existed to fix.
