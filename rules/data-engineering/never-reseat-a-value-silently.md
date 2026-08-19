# Never reseat a value silently — moving a row is a decision, and it needs consent

**Task type:** data engineering — any join, merge, remap, override or correction that can change
*which row* a value lands on.
**Related:** [`never-patch-a-key-to-force-a-join`](never-patch-a-key-to-force-a-join.md) — says
don't build the remap. This says: when one exists anyway, it must be visible.
[`unexpected-means-stop-and-propose`](../agent-workflow/unexpected-means-stop-and-propose.md) —
fires on surprise; **this one fires when nothing is surprising at all**, which is the gap it
fills.
[`a-delta-is-three-numbers`](../analytics/a-delta-is-three-numbers.md) — a reseat is a loss and a
gain that cancel.

---

## The rule

**Any operation that changes which row a value lands on must be surfaced before it ships, with
the source row, the destination row, and the value named — and it must be approved, not
announced.**

Not "logged". Not "counted". **Named, and consented to.**

## Why the other guards do not catch this

The usual triggers all depend on something looking wrong:

- an exception — there is none; the join succeeds
- a null — there is none; every row has a value
- an unexpected result — nothing is unexpected; the remap did exactly what it was written to do
- a total that does not reconcile — it reconciles perfectly, because a reseat is a **loss and a
  gain of the same value**

A reseat is invisible to every check that looks for failure, because **it is not a failure.** It
is a *decision about attribution*, executing silently inside code that was written to make a join
work.

And attribution is exactly the thing the person who owns the data must decide. Which of two rows
is the real one is a question about the world, not about the merge.

## The shape it takes

Two rows hold the same number in different columns, and both look defensible:

| row | `population` | `no_coverage` flag | `pop_from_other_block` |
|---|---|---|---|
| the unit the **source** names | NULL | **True** | **149,645** |
| the unit the **remap** points to | **149,645** | False | NULL |

The value is byte-identical in both places. That identity is the proof it is one record seated
two ways — and it is also why no reconciliation catches it. **The flag is worse than the null:**
`no_coverage = True` on a unit the source plainly publishes is not missing data, it is a
fabricated assertion, and it is the column analysts filter on.

## Guard

- **Enumerate every reseat, every run.** `source_key → destination_key`, the column, the value.
  A count is not enough — the count is what let this survive. **Name the rows.**
- **A remap that runs and prints nothing is the defect**, independent of whether its mapping is
  right.
- **Emit the reseat list as a reviewable artifact** and diff it between runs. A *new* reseat
  appearing should fail the build until someone acknowledges it.
- **Assert the two sides never both hold the value.** If the source row and the destination row
  are both in your frame, exactly one may end up populated, and which one is a decision — so the
  assertion should force the question rather than pick.
- **Never let a remap flip a coverage or quality flag.** If a value moved, the flag on the vacated
  row is now a claim nobody made.
- **Apply it everywhere or nowhere.** A remap applied in one join and not its sibling produces
  two blocks from one source that contradict each other in the same output.

## The incident

A hand-written crosswalk reseated demographic records from the code the issuing authority
publishes onto a different code in our frame. It ran unconditionally, in two sibling scripts,
producing no warning and no null.

One script was later given a guard; **the other was not**. The two blocks then disagreed in the
shipped dataset: **12 unit-years carried a fabricated `no_coverage = True` while the sibling
block held real published population for the same units — 557,132 people flagged as having no
coverage.** The values were byte-identical across the two rows.

The only check written to compare the two blocks filtered to rows where **both** were populated.
These rows have exactly one populated on each side, so they were structurally invisible to the
one guard aimed at them.

**Nobody was ever asked** whether a population should be attributed to the unit the authority
names or to the polygon our frame invented. That question was answered, for months, by a
dictionary lookup.

---

*Earned from:* the user, on being shown the two-row table above — *"this kind of matching must
send me a prompt."*
