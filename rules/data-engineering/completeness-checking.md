# Check completeness against the source, never against a previous output

**Task type:** data engineering — ingestion, joins, aggregation.

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

## Derived identifiers must follow the identity

When a record's key is corrected, every column derived from that key must be recomputed.

> **Incident C.** A unit's code was corrected from one province to another. The correction was
> applied to the key everywhere — but a *derived* `province_code` column kept the old value,
> and a province-level economic variable was joined through it. The unit continued to receive
> the wrong province's figure, **a 23% error**, which is precisely the defect the correction
> existed to fix.
