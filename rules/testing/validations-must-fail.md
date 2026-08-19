# A validation you have never seen fail is untested

**Task type:** testing — guards, gates, assertions, acceptance checks.
**Related:** [`name-the-blind-spot`](../analytics/name-the-blind-spot.md) — the mirror case. This rule is about a check that never fires; that one is about a check that *does* fire, returns a plausible number, and is believed.

---

## The rule

Run every new validation against input you **know** is broken, and confirm it fails. A check
that only ever passes is worthless, and worse than worthless: it produces the *feeling* of
verification without the substance.

Three corollaries, each earned:

### 1. Prove the branch fires

If you write `if X: do_important_thing`, you owe a check that **X is ever true**.

> **Incident.** A custom colour scale was registered under
> `if "flag" not in matplotlib.colormaps: register(...)`. `flag` is a matplotlib **builtin**,
> so the condition was always false, the registration never ran, and 30 figures silently drew
> with the wrong scale — inverted, so the rare class each figure existed to show became
> invisible. No error. The code reads correctly.
>
> **Cost:** 30 wrong figures, shipped, until someone looked at one.

A defensive branch with no evidence it fires is not defence.

### 2. Build the failure before you guard against it

> **Incident.** A download-completeness guard rejected any file whose first 400 characters
> contained `"404"`. The files were pipe-delimited population counts, so a row containing
> `|4046|` matched. It threw away **15 of 77 provinces** — files up to 300 KB with 451
> complete rows. The docstring justifying the rule described an error-page shape observed
> once, for a different kind of bad request, and generalised from it.
>
> **Cost:** a blocked pipeline and 15 provinces of good data discarded. Producing all four
> real failure modes took four requests and two minutes, and yielded a rule separating every
> bad case from every good one by a factor of 69.

### 3. Every treatment needs a null case

> **Incident.** A new measure was compared against an existing column to quantify an
> adjustment. The two came from different source rasters on different grids; the "+5.7%
> effect" was the baseline mismatch. It was caught only because a control existed — the
> subpopulation where the adjustment does nearly nothing, which *must* show nearly nothing.
> With a like-for-like baseline the same check reads **+0.11%**.

Find the subpopulation where the treatment does approximately nothing and confirm the
measurement shows approximately nothing. If it does not, the **baseline** is wrong, and no
conclusion about the treatment is worth reading yet.

## When an invariant fails at scale, suspect the invariant

> **Incident.** A validation asserted that no unit may be closer to a deep-sea port than to
> the coastline. It failed for **3,091 units** — and the data was right. Bangkok Port is a
> genuine international gateway 18 km up a river, as are Hamburg, Antwerp and Rotterdam.

Prefer invariants on the **small curated set** over the large derived one. The useful test
here was on the 8 ports (all within 18.3 km of the coast, against 243 km and 760 km for the
two river ports that had to be excluded), not on 7,586 units.

## The asymmetry underneath all of this

**Loud failure is cheap; silent success is expensive.** The bad `"404"` guard failed loudly
and cost twenty minutes. The unregistered colormap succeeded silently and shipped thirty
inverted figures.

Prefer code that crashes to code that quietly does the wrong thing — and be **most suspicious
of the parts that never complain**.
