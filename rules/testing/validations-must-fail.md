# A validation you have never seen fail is untested

**Task type:** testing — guards, gates, assertions, acceptance checks.
**Related:** [`name-the-blind-spot`](../analytics/name-the-blind-spot.md) — the mirror case. This rule is about a check that never fires; that one is about a check that *does* fire, returns a plausible number, and is believed.

---

## The rule

Run every new validation against input you **know** is broken, and confirm it fails. A check
that only ever passes is worthless, and worse than worthless: it produces the *feeling* of
verification without the substance.

Six corollaries, each earned:

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

### 4. A passing case does not tell you which branch passed it

Corollary 1 says prove the branch fires. This is its twin, and it is the one nobody checks:
**prove that the branch you believe is covering a case is the branch actually covering it.**

A green result reports an outcome. It says nothing about the mechanism, so coverage can rest on
an accident — and the accident is invisible in exactly the artifact people read to decide whether
something is covered.

> **Incident.** A guard protecting a set of control files had two independent arms: a
> subcommand-aware arm for the version-control operations that rewrite a tree, and a generic
> verb-list arm. `git rm <protected>` and `git mv <protected>` were refused, so the case looked
> handled. **Neither is in the subcommand arm.** They were caught because the generic list contains
> the bare verbs `rm` and `mv`, and the segment happens to contain one with a space in front of it
> — a pattern that is not looking at version control at all.
>
> The consequence is the dangerous part: **someone tightening the generic list to fix a false
> positive would silently uncover `git rm`, without ever touching the arm they believed owned it.**
> The test stays green until the day it does not, and the change that breaks it looks unrelated.

**The mechanical form is per-arm mutation, and it is a small extension of guard removal.** Disable
*the arm you believe covers this case* — not the whole guard — and re-run. If the case still
passes, your coverage is attributed to the wrong mechanism and your map of the system is wrong in
a way no amount of green will tell you.

Ask it of any control with more than one path to the same verdict: *which line refused this, and
is it the one I would have named?*

### 5. Ask what would still be green if it were already broken

The general form of this rule, and the cheapest question in it. Take any check, dashboard,
health signal, status field or passing test, assume the thing it watches is **already broken**,
and ask what it would be showing right now.

> **Incident.** Two assertions in a new test suite read `check("watermark written", "key" in
> state)` against a fixture that already set that key. Both passed against an implementation
> that never wrote the watermark at all — proved by patching it out and re-running. They had
> been written minutes earlier, by an author who knew the rule on this page.

Whenever the honest answer is *"green"*, the signal is decoration. This is the shared shape
behind a guard that never fires, a health ping emitted before the fallible step, a drill that
exercises a retired code path, and a status field set from intent rather than outcome:
**the success signal is not attached to the thing it reports.** See
[`silence-must-be-the-alarm`](../how-we-work/silence-must-be-the-alarm.md) for the unattended
case, where the answer is "green" for as long as nobody happens to look.

## The boundary: when running the test IS the harm

This rule says prove the guard fires. There is one class where you may not, and it has to be stated
here or the rule argues for the wrong thing: **a control whose only direct test is performing the
act it prevents.**

> **Incident.** A credential gate was found to miss a path-qualified reader verb. The open question
> was whether the layer beneath it independently caught the same command — and the only way to
> answer it directly was to attempt to read a live private key. Nobody ran it. *A test whose
> failure mode is a private key in a transcript is not a test worth running*, because the failure
> case is unrecoverable: a key that has been printed is rotated, not un-printed.

The discriminator is **whether the failing run is reversible.** A guard that might fail to stop a
file write can be tested against a scratch file. A guard that might fail to stop an exfiltration
cannot be tested by exfiltrating, because the test *is* the incident.

What to do instead, in order:

1. **Test the predicate, not the effect.** Evaluate the matcher against the command string as data
   — every finding in that incident came from calling the classifier on strings, never from running
   one of them.
2. **Substitute a decoy with the same shape.** A file at the same path pattern, containing nothing.
   This works when the control keys on the path and not on the content.
3. **Have it answered from outside a session** by whoever owns the system, where the answer costs
   nothing.
4. **Record it as unverified, with the reason.** An honest "not tested, because the test is the
   harm" is a finding. A green light produced by never having looked is
   [`absence-is-not-compliance`](absence-is-not-compliance.md).

**Never resolve this by deciding the control is probably fine.** The point of the boundary is that
the evidence is genuinely unavailable by the direct route, which makes routes 1 to 3 mandatory
rather than optional.

### 6. A check that has never passed is as untested as one that has never failed

**The mirror of corollary 1, and the half nobody runs.** That corollary says prove the failing branch
fires. This one says **prove the passing branch fires, on real input** — because both ends of the
range are untested, and the all-red end does not look like a defect. It looks like diligence.

> **Incident.** An audit compared each repository's recorded pin for **equality** against the newest
> commit touching `rules/`. The tool that writes those pins records the clone's remote HEAD instead,
> so the two coincide only when HEAD happens to be a `rules/` commit. Result across 24 repositories:
> **0 current, 13 stale.** Every row of the worklist it produced was unearned, and it had been that
> way for four days.
>
> The proof was the auditing repo itself, reported stale at a pin **newer** than the newest `rules/`
> commit — the correct state for anything repinned after a skills-only change. An independent
> checker on the same repo at the same moment: *"pin is behind but NO RULE MOVED — holding is
> correct"*, exit 0.

**The tell is not a colour, it is a denominator nothing can move.** Corollary 5 asks what would still
be green if the subject were already broken; here the honest answer was *"nothing is green"*, which
reads as the check working hard. **`0 of 24` is not a measurement, it is a constant** — and a rate
that no state of the world could change is reporting on the checker, not the subject.

**A denominator that CAN move is allowed to sit at zero, and that is the false-positive shape of
this corollary.** Not every all-red reading is a broken check — sometimes everything really is stale.
The discriminator is not the number, it is whether any state of the world would change it.

> **Demonstrated within the hour, by this corollary's own publication.** The rule file was committed,
> which touched `rules/`, which made the auditing repo's pin genuinely stale. The audit printed the
> same headline as the defect — `0 of 24 current` — about a completely different object: before the
> repair it was a constant nothing could move; now it was a reading that happened to be zero because
> a rule had moved an hour earlier. Repinning made it `1 of 24`.
>
> **Same number, same tool, same day, one broken and one correct.** So do not read a count and
> conclude anything. Ask what would have to be true for it to differ, and then go and make one row
> differ.

**The fix is a different predicate, not a better measurement.** The object was right and the baseline
was one the other end never writes. That distinguishes this from
[`discriminate-by-executing-not-inspecting`](../how-we-work/discriminate-by-executing-not-inspecting.md),
which is a true number about an *adjacent* object.

**Validate by join, not by argument.** The repaired check was confirmed by running an independent
implementation over the same 13 repositories and comparing: **13 agree, 0 disagree.** Before the
repair, the single disagreement *was* the entire "current" column — so the join found it where
re-reading the code had not, for four days.

And this class costs other people rather than you: see
[`a-pinned-reference-is-checked-at-its-pin`](../how-we-work/a-pinned-reference-is-checked-at-its-pin.md)
on why a loud check is obeyed and a silent one is audited.

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

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: deferred
observable: 'for every guard, assertion or acceptance check that is added or changed: whether the test suite contains a case that makes it FAIL, proven by removing the guard body and observing a test go red; and for every defensive branch, whether any test makes its condition true'
trigger: 'pre-commit on changed guard paths, plus CI over the whole guard set'
check: 'for each changed guard: delete its body, run the suite - if nothing goes red, block; a check whose pass branch is exercised by no test case, or whose live run has never returned a pass for any subject, -> block: a rate no state of the world can move is reporting on the checker; a conditional whose true branch is never entered under the suite -> block; and for a guard with more than one arm reaching the same verdict, disable each arm separately - a case that survives removal of the arm believed to cover it is covered by accident, and the report names which arm actually fired'
escape: 'a guard genuinely impossible to exercise in test declares itself unexercised with a reason, and that declaration is counted and reported rather than hidden'
narrows: 'guard-removal proves the check CAN fail, and per-arm removal proves WHICH line does the work. It does not prove the check fails on the RIGHT input - a guard written against an imagined failure shape passes its own removal test while missing every real defect, which is why a-check-that-shares-a-source-is-not-a-check sits beside this one and is recorded there as irreducible'
```
