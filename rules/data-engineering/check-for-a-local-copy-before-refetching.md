# Before re-fetching anything, check whether the project already has it

**Task type:** data engineering — any pipeline step that downloads, re-downloads, or
regenerates an input it needs.
**Related:** [`read-the-manual-first`](../how-we-work/read-the-manual-first.md) — the local
copy is usually documented; this is the specific case of not looking.
[`eta-needs-a-denominator`](../how-we-work/eta-needs-a-denominator.md) — a fetch you never
questioned is also a fetch whose size you never measured.

---

## The rule

**A pipeline that fetches remote data must resolve against local copies first, and you must
verify which path it actually uses before letting it run.** "The script downloads its inputs" is
not a fact about the project — it is a fact about one code path, which may be the wrong one.

The dangerous version is not a missing file. It is a project that *deliberately committed a
local copy* — optimised, compressed, LFS-tracked, documented as the committed artifact — while
the pipeline script still points at the gitignored scratch cache nobody updated it away from.
Everything looks correct: the data is in the repo, the download code is legitimate, the run
proceeds. It just re-fetches tens of gigabytes that were already on disk.

## The incident

A geospatial pipeline needed 344 national raster files (43 per year × 8 years). The project had
**already solved this**: a dedicated script produced compressed copies of every one of them into
a separate committed directory, with a docstring explicitly stating they existed to be committed
via Git LFS (3.4 GB against ~38 GB raw) and that the compression had "no material effect on the
statistics the consuming script computes."

The consuming script read from the *other* directory — the raw, gitignored cache — and
re-downloaded all 38 GB from the upstream provider. Nothing had ever wired it to the committed
copies. The two directories sat side by side in the repo, one committed and complete, one
gitignored and empty on a fresh machine.

Over roughly two hours this ran, was killed and restarted twice for unrelated reasons, and was
reported to the user as legitimate slow progress. The user asked the decisive question directly
— **"I thought all data is in repo"** — and a two-minute check confirmed all 344 required
rasters were present, materialised, and readable. A ten-line `resolve_raster()` helper
eliminated the entire download.

**Cost:** hours of wall-clock time and ~38 GB of unnecessary transfer, on data the project had
already gone to deliberate effort to commit so exactly this would not happen.

## Why it survives review

Every individual piece looks right, which is what makes it invisible:

- **The download code is correct.** It fetches the right URLs, retries properly, verifies
  results. Reading it finds no bug, because there isn't one *in it*.
- **The data really is in the repo**, so any check phrased as "do we have this data?" answers
  yes — the question that matters is "does *this code path* find it?", which is different.
- **The gitignore entry justifies itself.** `# ~38GB, re-downloadable by <script>` reads as a
  considered decision rather than a pointer at an unused fallback.
- **Slow is expected.** Large geospatial jobs are legitimately slow, so an unnecessary download
  is indistinguishable from normal cost unless someone checks what it is actually doing.

## Guard

- **Before running any fetching pipeline, grep the repo for a local copy of what it fetches** —
  a sibling directory, a `-compressed`/`-cache`/`-subset` variant, an LFS-tracked path. If one
  exists, confirm the script resolves to it *before* starting the run, not after.
- **When a repo contains both a gitignored cache and a committed copy of the same data, treat
  the committed copy as the source of truth** and make every consumer resolve to it, falling
  back to fetching only when it is genuinely absent. The pattern is small: resolve the preferred
  path, check existence, fetch only on miss.
- **Read the docstring of any script whose output you are about to regenerate.** Here the
  compression script *stated its own purpose* — committed, LFS, safe for these statistics — and
  answered the whole question in its first paragraph.
- **A gitignore comment that says "re-downloadable" is a claim to verify, not a reason to
  re-download.** Check whether an optimised committed form already exists, since committing a
  reduced copy is the standard alternative to excluding large inputs outright.
- **If a job is slow, ask what it is spending the time on before accepting it.** "Large job,
  legitimately slow" and "large job doing entirely unnecessary work" look identical from the
  outside and are distinguished by one cheap check.

---

*Earned from:* a pipeline that re-downloaded ~38 GB of rasters over multiple hours while all 344
of them sat committed in the same repository via Git LFS, in a directory created specifically so
they would not need re-downloading — found only when the data's owner asked why anything was
being downloaded at all.
