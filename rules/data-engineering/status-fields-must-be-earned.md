# A status field is a claim — earn it from evidence, and make it re-checkable

**Task type:** data engineering — manifests, ingest checklists, sync/reconcile jobs, any
`state`/`status` column that records whether work was done.
**Related:** [`completeness-checking`](completeness-checking.md) — this is the specific way a
completeness record lies about itself.

---

## The rule

**Never write a status meaning "this was done" unless something checked that it was done.**

A manifest row, a `state` column, a ✅ in a checklist — each is an assertion about reality, worth
exactly as much as the evidence that produced it. A status derived from an assumption is worse
than no status at all, because it stops anyone from looking.

## The incident

A bulk ingest pulled ~300 datasets from a government portal. Each item required a human action
in a browser before its download unlocked, so the fetch was one long manual session. **Three of
206 items were missed** — an ordinary slip over ten hours of clicking.

The manifest recorded **all 206 as `downloaded`**. The gap went unnoticed for twelve days and had
silently changed an outcome variable for two regions.

## What the manifest already knew

A SHA-256 was computed and stored for every row. Thirty-six file paths were each claimed by two
or three rows — and in **all thirty-six**, every claiming row carried the *identical* hash:

```
region-X  status=downloaded  size=24222512  sha=c540b8bc...  year=NULL
region-X  status=downloaded  size=24222512  sha=c540b8bc...  year=NULL
region-X  status=downloaded  size=24222512  sha=c540b8bc...  year=NULL
```

Three distinct survey years, certified complete by one file's bytes. This query prints the entire
defect:

```sql
SELECT sha256, COUNT(*) FROM requests GROUP BY sha256 HAVING COUNT(*) > 1;
```

Nobody ran it. **Collecting integrity data is not checking it. An unqueried hash is decoration.**
Write the assertion in the same commit as the field.

## The rules that fall out

**Verify at the moment of acquisition, against the source's own statement.** The download page
displayed the expected size before the click. Comparing received bytes to that is free, instant,
and catches a missed or truncated fetch on the spot. Anything checked later is checked against a
memory of what should have happened.

**Uncertainty belongs in the value, not the docstring.** The reconcile function's own docstring
was honest — it said it "best-effort-assigns" and that which row maps to which file is
"arbitrary". The column it wrote said `downloaded`. Every downstream reader sees the column. If a
status is a guess, name it one: `assumed`, `unverified`. Doubt must travel with the data.

**A reconciler must be idempotent and recompute from reality.** This one inflated its own claims
on every run: rows already marked `downloaded` were excluded from the next pass, so the file they
pointed at was never registered as taken and got re-claimed for another row. Reproduced by
resetting one group and re-running:

```
run 1 → 2 of 3 rows marked downloaded   (2 files present)
run 2 → 3 of 3 rows marked downloaded   ← the third row has no file
run 3 → 3 of 3
```

This is "never validate against a previous output" wearing a disguise — the previous output was
its own.

**If the field that makes the check decidable cannot be filled, that is a blocking gap.** The
schema had a `year` column. It was NULL on all 206 rows, because discovery read a list view that
does not expose the year. Without it, matching a request to a file is undecidable — which is
exactly why the function had to guess. The year was available the whole time, on each item's
detail page and inside the delivered filename. Nobody opened one.

**For time-limited sources, record the expiry and watch it.** The ready-date was stored; the
15-day download window was not tracked. Three items reached day 12 of 15 unnoticed and nearly
became unrecoverable.

**Count in the unit of the thing, and prove the mapping is 1:1 first.** The gap was first reported
as *seven* missing items, by counting files. The answer was *three*: one archive named
`2565-2566` satisfies two requests. Wrong by more than double, in the direction of alarm.

## How it was actually caught

No internal check found it. They all compared the pipeline to itself. It surfaced only because a
collaborator held an **independently-produced copy of the same output** and kept asking why it
disagreed.

**An independent copy of your own output is a free audit, and a disagreement with it is a finding,
not a nuisance.** Reconcile it field by field the first time it is offered — not after it has been
raised several times.

## The check to write

For any manifest of fetched artifacts, assert:

- `status = 'downloaded'` implies the recorded path exists **and** its size matches the recorded
  size
- no two rows fulfilled by different logical items share a `sha256`
- every row has the key field that makes row→artifact mapping decidable (here, the version/year)
- the reconcile step is idempotent: running it twice changes nothing

Run it in CI or a pre-commit hook. Each of these is one query, and any one of them would have
caught this on day one.

---

*Earned from:* a manual bulk ingest of 206 items where 3 were missed, every row was recorded as
complete, and the contradicting evidence sat unqueried in the manifest for twelve days.
