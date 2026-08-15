# Every output must be reproducible from code in the repo

**Task type:** research — anything that will be cited, published, or handed to someone else.

---

## The rule

Every output file — table, figure, model, panel — must be regenerable by running a script
committed to the repo. No manual, undocumented or one-off steps. If a figure was exported by
hand, add a script that regenerates it, so it cannot drift from the data.

## Commit the raw inputs, not just the URL

**A source URL is not a durable substitute for the bytes.** Portals go stale, snapshots age
out, corporate proxies start blocking a host that worked last session. "The script can
re-fetch it" is not reproducibility if the thing it fetches from disappears.

If a file is too large to commit as-is, **do not gitignore it as the default move** — optimise
first: large-file storage, a compressed or subset form, or trimming to the slice the pipeline
actually uses. Only exclude once those are genuinely exhausted, and say so in the ignore
comment.

Always log the **source URL, download date, format, size and licence** — and, for anything
that lives only on local disk, **which machine it is on**. An uncommitted file's location is
otherwise undiscoverable from the repo itself.

## Delete stale intermediates when inputs change

Cached artifacts must never silently outlive the inputs they were derived from. When an input
changes, delete the cache so it rebuilds.

## Version changes are findings, not housekeeping

> **Incident.** A rainfall series was migrated from one release of a global product to the
> next, to gain a missing year. The migration was not a level shift: **2023 and 2024 national
> means moved by +14.6% and +11.1%**, against −0.5% to +3.6% for earlier years — and it
> **reordered** provinces, one moving from rank 16 to 24 on dryness, another from 7 to 20.
>
> A pre-registered geographic prior that had passed on the old version now failed. It was left
> failing, with the cause documented, rather than retuning the threshold — **retuning a test
> to accommodate new data is fitting the test to the thing it is supposed to check.**

When a source version changes, publish a **per-period delta table** alongside the new data, so
anyone comparing against an earlier vintage can tell a reprocessing from a real change.

## State what was measured versus what was assumed

Mark measured numbers as measured and say what was run to get them. If a source was cited but
not read, say so. **Never present an inferred figure in the same voice as a measured one.**

A useful discipline: never state a number you did not measure. Recalled figures, plausible
round numbers and "roughly X" are guesses wearing the costume of evidence. If an unverified
figure must be used, label it unverified **in the same sentence**.
