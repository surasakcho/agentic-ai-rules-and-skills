# Register the retraction in the commit that makes it

**Task type:** any project that keeps a registry of superseded claims, or any long-lived document
set that accumulates corrections — design docs, ADRs, runbooks, incident logs.
**Related:** [`a-correction-lands-where-you-noticed-it`](a-correction-lands-where-you-noticed-it.md)
— this is its unguarded flank: that rule gets the correction to every place the claim lives, this
one is about knowing the claim needs correcting at all.
[`discriminate-by-executing-not-inspecting`](discriminate-by-executing-not-inspecting.md)
— the same denominator problem, one level up.
**Mechanised by:** the [`stale-claim-check`](../../skills/stale-claim-check/SKILL.md) skill —
which reads this registry, and can therefore only ever be as good as it.

---

## The rule

**A retraction is registered by the commit that makes it, not by a sweep afterwards.**

A sweep's denominator is your memory. A commit's denominator is the log.

When you correct a figure, overturn a decision, or discover that a claim was never true, you hold
three things at that instant and only at that instant: **the old claim in its exact wording, the
new value, and why it changed.** An hour later you hold the new value. A day later you hold only
the new value, and the old claim survives in whatever documents quoted it — silently, because
nothing in a document announces that it is out of date.

So the registry row is not paperwork appended when someone remembers to audit. It is part of the
change, in the same commit, or it does not reliably exist.

## The incident

A week of intense correction produced **at least sixteen retractions**: measured figures that moved,
a diagnosis that was overturned, a metric that turned out to measure the wrong object, a mechanic
retired after being specified.

Afterwards, someone swept the tree with a stale-claim checker and registered the retractions they
could recall: **six rows.** The run came back with one real survivor and read as broadly clean.

A second pass by a different role registered **ten more** — and reported that **two of those ten
were noticed only because they went looking to register them.** Nobody had forgotten them
carelessly; they simply were not the ones that came to mind, because the mind that recalls
retractions recalls the dramatic ones.

**So the first "clean" run was checking roughly a third of the population and reporting a colour
about the whole tree.** The registry was the sample, and nobody had computed its coverage.

The survivor it did catch is worth stating, because it shows what the uncovered two-thirds could
have been hiding. (The claim quoted next is **superseded** — reproduced here as the worked example,
not asserted.) A design document asserted *"the endpoint is undeployed"* — and that sentence sat
in the section that **instructs the release gate how to record the telemetry row.** It did not
merely sit there being wrong; it told the gate to log an exception. It had been false for a week,
and it is most of the reason that gate row looked impossible to satisfy. One stale sentence, wired
into a control.

## Why a sweep cannot close the gap

**Green is the dangerous colour, and an incomplete registry produces exactly the same green as a
clean tree.** There is no signal that distinguishes them, which is what makes this different from
an ordinary miss: the tool is working perfectly, over a population nobody sized.

Three properties make sweeping structurally lossy:

- **Recall is biased toward drama.** The retraction that cost three days is remembered. The one
  that was a quiet correction in passing is not, and it is equally capable of sitting in a control.
- **The wording is gone.** Registering a claim requires the *pattern* that matches how it was
  originally phrased. That phrasing is in front of you while you edit it and nowhere afterwards.
- **The reason evaporates fastest of all.** "Why was this superseded" is the field that makes a
  future reader trust the row, and it is the first thing that decays into "we changed it."

## Applying it

At the moment a change supersedes a claim, the same commit adds the row: **the pattern that matches
the old wording, the value that replaced it, and why.** If a project has no registry yet, that
commit creates it — a one-row registry that grows with the log is worth more than a twenty-row one
assembled from memory a week later.

**And the row is a claim like any other, so it ages like any other.** Registering on time is
necessary and not sufficient: when something is corrected a *second* time, the row is one of the
places that correction has to land. Two independent repos hit this on the same evening — in one, a
row was wrong before the day it was written correctly had ended; in the other, two of ten rows had
gone stale within a day, and both were moved by rulings the same person made *after* registering
them. **The live value is most perishable in exactly the rows an active decision-maker just wrote**,
because those are the ones still being ruled on.

A checker cannot save you here, and this is the trap: the pattern column guards the *old* values, so
**nothing watches the live field**, and the registry is read as the reference rather than as input.
**A stale guard is worse than a missing one, because it produces the same colour as a correct one.**
In one of the two incidents, correcting a single rotted row immediately exposed a real survivor in a
design document that had been invisible behind it the whole time.

The repair is cheap and is the same operation as any other retraction: **the dead live value moves
into the pattern column.** A figure superseded twice is then watched at both stages rather than
replaced and forgotten. Which is this rule reaching one level further in — register the retraction
when you make it, *including the retraction of your own replacement*.

Two supporting habits, both cheap:

**Mark the figure where it stands, not where the section starts.** A checker's marker window is a
few lines wide, so a banner at the head of a revision section does not qualify a number thirty lines
below it — demonstrated three times in one evening on an append-only document, where a file-level
banner was not an option either because it would have skipped the only live sections. A retraction
stated without a marker — *superseded*, *revised*,
*rescinded*, *no longer* — cannot be distinguished from an assertion by a tool, and cannot be
distinguished by a human skimming either. In the incident above, one flagged hit was a correctly
written retraction that simply never said so; the reader's eye lands on the stale number.

**Report coverage, not colour.** "No unqualified survivors across N registered claims" is a
statement someone can evaluate. "Clean" is not. If the registry has six rows and the week had
sixteen retractions, the honest summary says so.
