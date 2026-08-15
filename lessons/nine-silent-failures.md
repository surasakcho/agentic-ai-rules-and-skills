# Nine silent failures

*Shareable write-up · 2026-08-15 · drawn from a large sub-national geospatial panel —
thousands of areal units, several survey waves, a few hundred variables. The study itself is
unpublished and is not identified here: every lesson below is about **process**, and none of
them needs the findings to make sense.*

**A pipeline that runs is not a pipeline that is right.** Every defect that mattered here was
invisible in the source code and obvious in the rendered output, and none of them threw an
error.

---

## The setup

A data audit found fifteen problems in a research panel. Fixing them took two days and
produced 321 maps, nine tables and a set of stylised facts. The work was verified: unit
tests, a completeness audit, an acceptance gate at 26/26, and 24 of 26 pre-registered
geographic priors passing.

Then someone asked whether the figures had actually been looked at. The honest answer was no
— they had been generated, listed and reported.

**Reviewing them found six distinct defects in the first fourteen figures examined.**

The arithmetic worth sitting with: the remediation fixed 15 audited findings and
**introduced 11 new defects doing so**.

---

## The nine mechanisms

### 1. The conditional that never fires

A custom colour scale was registered under `if "flag" not in colormaps: register(...)`. But
`flag` is a **builtin** name in the plotting library, so the condition was always false and
the custom scale was never once used. Every binary map drew with the builtin — low values
bright red, high values black, exactly inverted.

**Cost:** 30 maps inverted; the 44 units each flag existed to identify were invisible.

**Guard:** if you write `if X: do_important_thing`, you owe a check that **X is ever true**.
A defensive branch with no evidence it fires is not defence.

### 2. "This run's list" treated as "everything that exists"

A cleanup step removed artifacts whose source column no longer existed. Run against a
four-variable subset, it concluded every other artifact was orphaned. The same mistake, the
same day, truncated a 321-row metadata table to 5 rows.

**Cost:** 633 artifacts destroyed across two instances of one mistake.

**Guard:** anything that deletes or overwrites from a computed set must know whether that set
is **complete or partial**. Write the partial case first; it is the one that loses data.

### 3. Masked values that render as missing

A log scale masks non-positive values, and a colour map's "bad" colour is transparent by
default. Every zero drew as blank — pixel-identical to no-data — beneath a panel title
reading "0 units no data" and a caption claiming the zeros were "drawn at the floor".

**Cost:** 39,829 values rendered invisible across 16 maps. In the worst case *the prevalence
of true zeros* **was the finding**, and the map showed it as absence.

**Guard:** a claim in your own comment or caption is a **hypothesis you wrote down**, not
evidence.

### 4. A guard written from a guess about the failure

A completeness check rejected any downloaded file containing `"404"` in its first 400
characters. The files were pipe-delimited population counts, so a row containing `|4046|`
matched. The docstring justifying the rule described an error-page shape observed once, for a
*different* kind of bad request.

**Cost:** 15 of 77 provinces of good data discarded — files up to 300 KB with 451 complete
rows.

**Guard:** **produce the failure and look at it** before writing the guard against it. Four
requests, two minutes, and a rule that separates every bad case from every good one by a
factor of 69.

### 5. Comparing against the wrong baseline

A new measure was compared against an existing column to quantify an adjustment. The two came
from different source rasters on different grids.

**Cost:** a "+5.7% effect" that was entirely baseline mismatch. The true value was +0.11%.

**Guard:** **every treatment needs a null case.** Find the subpopulation where the treatment
does approximately nothing and confirm the measurement shows approximately nothing. That
control is the only reason this was caught rather than published.

### 6. An invariant from intuition, not from the domain

A validation asserted that no unit may be closer to a deep-sea port than to the coastline. It
failed for **3,091 units** — and the data was right. Bangkok Port is a genuine international
gateway 18 km up a river, as are Hamburg, Antwerp and Rotterdam.

**Guard:** when an invariant fails at scale, the first hypothesis is that **the invariant is
wrong**. Prefer invariants on the small curated set (8 ports) over the large derived one
(7,586 units).

### 7. A convention applied outside its domain

A fixed 0–1 colour scale made share variables comparable across maps. Correct for land-use
shares, which span 0.83–1.00 of that range. Wrong for demographic ratios, which top out at
0.449.

**Cost:** 9 of 25 maps using under 40% of their colour range — including the study's main
regressor, whose spatial gradient was flattened into a uniform pale wash.

**Guard:** a convention needs a **stated domain**.

### 8. A headline number that counts threshold crossings

"Nine of eighteen relationships change sign between the pooled and within estimator" was
accurate — and knife-edge. One pair scored "no change" only because its pooled correlation
landed at **+0.0017** rather than −0.0017.

**Guard:** when a headline is a count of threshold crossings, report the **magnitude of
movement** alongside it, and how many cases sit near the threshold.

### 9. Fixing a symptom before understanding the mechanism

Masking buildings out of a surface model to recover bare-earth slope made the number *worse*.
Slope is computed on a 3×3 kernel, so masking a footprint removes the flat roof interior and
keeps the steep ground-to-roof ring.

**Guard:** when a fix moves the metric the wrong way, that is **information about the
mechanism**. Enumerate candidate causes and measure to discriminate before changing anything.

---

## Why fourteen figures found six defects

Defects do not live in artifacts. They live in the **shared policy code** that produces
artifacts — a colour rule, a normalisation rule, a scale rule — so a single defect lands on
every artifact that policy touches, four to thirty at a time.

The fourteen figures were chosen to span different policies: one per colour family, one per
transform type, one per data family. **Random sampling of fourteen out of 321 would likely
have found one or two.**

> Sample across **mechanisms**, not at random. If two artifacts came from the same code path,
> reviewing both tells you almost nothing the first did not.

---

## Two asymmetries

**Loud failure is cheap; silent success is expensive.** The bad `"404"` guard failed loudly
and cost twenty minutes. The unregistered colour map succeeded silently and shipped thirty
inverted figures. Be most suspicious of the code that never complains.

**A check you have never seen fail is untested.** An acceptance gate was deliberately run
against known-bad input and failed 17 of 19 criteria — that is what established it could fail
at all.

---

## What to actually do

1. **Recompute, don't read.** Verify a table by recomputing it from source.
2. **Predict, then look.** Say what the output should show before opening it.
3. **Open the image.** Can the thing it exists to show be seen? Does the caption match what
   the figure draws?
4. **Screen the rendered artifact, not the code** — then eyeball everything flagged, plus a
   mechanism-spanning sample.
5. **Say what you eyeballed versus what you screened.** "I reviewed them" when you screened
   them is a false claim about your own work.

Rules extracted from this: [review-every-output](../rules/analytics/review-every-output.md),
[validations-must-fail](../rules/testing/validations-must-fail.md),
[surgical-verified-change](../rules/coding/surgical-verified-change.md).
Mechanised as [verify-outputs](../skills/verify-outputs/).

*The full write-up, with the real variable names and counts, stays in the originating project
repo. Only this de-identified version is published — see
[sanitise-before-sharing](../rules/agent-workflow/sanitise-before-sharing.md).*
