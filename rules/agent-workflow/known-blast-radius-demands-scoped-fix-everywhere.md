# A known, small blast radius demands a scoped fix everywhere it applies — not just where you were first asked about it

**Task type:** agent workflow — any time a correction's affected set is known precisely and
touches more than one downstream artifact.
**Related:** [`characterise-once-not-per-question`](characterise-once-not-per-question.md) is
about not leaving gaps in an *investigation*; this is the execution-cost twin — not leaving
gaps in how a *known* fix gets applied. [`solve-the-space-not-the-samples`](../analytics/solve-the-space-not-the-samples.md)
is about proof; this is about cost once the fix itself is already understood.

---

## The rule

**The moment a change's affected set is known precisely — not estimated, enumerated — that
scoping applies to every artifact the change touches, not only the one under discussion when
someone first asked "why rebuild everything for a handful of rows."** If you already built a
scoped/incremental rebuild for one file with this exact problem shape, the same pattern is owed
to every other file with the same shape, before any of them gets run.

A script's default invocation being "recompute everything" is an accident of how it happens to
be written. It is not evidence that full recomputation is the right cost for a change already
known to touch 5 rows out of 7,583.

## The incident

A frame correction changed the identity of roughly 5 of 7,583 tambons (administrative units) in
one project — about 0.07% of the total. The affected codes were enumerable directly from the
correction's own definition, known exactly before any downstream file was touched.

Eleven downstream files derived from that frame needed rebuilding. For the **first** one, the
question "why rebuild everything, can't you just rebuild the defective items" was asked
directly, and the answer was to build a `--only` flag: recompute just the touched deliveries,
splice the unaffected rows back in from the previous committed output.

For the other **ten**, the same question was never re-asked, so it was never re-answered. Each
was simply re-run in full — the only mode each script's `__main__` supported — because
"rebuild file X" defaulted to whatever X already did. **Two of the ten took over two hours of
combined wall-clock/CPU time** computing national, multi-year zonal statistics for 7,578 tambons
whose values were already known to be unchanged, to produce output that differed from the
previous version at fewer than 5 rows — confirmed **after the fact** by a diff against the
previous committed version, when the diff's shape had already been fully known **before** either
job was started.

**Cost:** two-plus hours of compute spent recomputing 99.93% of a national geospatial dataset
that provably had not changed, running concurrently with unrelated background work, discovered
only when the person waiting on it asked why a five-row fix was taking this long.

## Why it happened

The scoped-rebuild pattern was built once, in response to being asked about it once, for the one
script that happened to be the subject of the conversation at that moment. It was not
generalised to the other ten scripts sharing the identical shape — same corrected frame, same
known small blast radius, same "full rebuild" default — because nothing prompted revisiting the
decision for each of them individually. Each got dispatched as "just rerun this script," and
"just rerun this script" silently inherited whatever cost that phrase happened to imply for that
particular script.

This is the same failure shape as scoping an *investigation* to the question asked instead of the
whole object — except here the object is a decision about **how expensive to make a fix**, made
once, then quietly not re-made for every artifact that needed the same decision.

## Guard

Before dispatching "rebuild file X" for any file downstream of a change with a known, precisely
enumerable affected set:

- **Ask whether X's affected surface is the same known small set** as the one you already built
  a scoped rebuild for. If the answer is yes for one file, it is yes for all of them — check the
  whole list up front, not file by file as each one happens to come up.
- **Build (or reuse) the splice-with-previous-output pattern before running anything**, not after
  discovering the naive rebuild is slow. The pattern is always the same shape: load the previous
  output, recompute only the rows in the known affected set, splice the rest back in unchanged,
  and verify row-for-row that nothing outside the known set moved.
- **A script's lack of a scoped mode is a gap to fix, not a constraint to accept.** If ten
  scripts share one frame and one correction, the scoped-rebuild capability is a property of the
  *situation*, and it is cheaper to add it to all ten once than to eat full recomputation cost on
  each ten separate times this same class of frame correction happens again.
- **"Old output + a known small diff-set + a way to compute values for just that diff-set" is
  always cheaper to splice than to recompute from scratch.** Treat that as the default plan the
  instant the diff-set is known, not as an optimisation to reach for only after someone asks why
  it's taking so long.

---

*Earned from:* a frame correction affecting ~5 of 7,583 rows, where a scoped-rebuild pattern
built for one downstream file was not applied to ten others sharing the identical problem shape,
costing over two hours of full-national recomputation that a five-row splice would have replaced
in minutes — caught only when asked directly why a small fix was taking this long.
