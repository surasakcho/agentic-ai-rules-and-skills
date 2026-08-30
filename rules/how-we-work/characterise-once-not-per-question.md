# Characterise the object once — do not investigate question by question

**Task type:** agent workflow — any investigation reported back to someone who will ask
follow-ups.
**Related:** [`close-your-own-gaps`](close-your-own-gaps.md) is what to do when you notice a
gap; this is why you keep not noticing.
[`report-both-sides-of-a-comparison`](../analytics/report-both-sides-of-a-comparison.md) is
the reporting discipline this rule makes possible.

---

## The rule

**Scope the answer to the question. Never scope the investigation to the question.**

When asked "does A match B on X", it is natural to check X, answer, and stop. Each answer is
correct as far as it goes. But the object was never characterised, so the next question
surfaces something that was never looked at — and it looks, every time, like new information
being withheld.

The tell is a session that goes: *"so only X remains?"* → *"...and also Y"* → *"only X and Y?"*
→ *"...and Z"*. From the outside that is indistinguishable from concealment. From the inside
each step felt like answering the question asked.

## The incident

A pipeline output was being reconciled against an independently produced reference file.
Over one session, five separate things were reported and then turned out to be wrong or
incomplete — each surfaced by a follow-up question, none by the investigation itself:

| Reported | Actually |
|---|---|
| "these unmatched rows are the reference file's defect" | **ours** — the pipeline was silently discarding real area at a de-duplication step |
| "this region will drop to 3 unmatched rows" | it stayed at **25**, and was a duplicated text label, not a numeric error |
| "all the boundary variants I tested agree" | there was **another one**, shipped inside a different product's archive, untested until asked about |
| "these 3 rows are an open question" | all three were inside a bucket **already explained** |
| "this is closed, proven" | **three of the supporting claims were false** under recheck |

**Cost:** an entire session spent in a discover-report-discover loop, and a conclusion that had
to be publicly retracted in part after it had already been described as proven.

## The fix is a script, not a resolution

Intent does not survive the next question. Build the thing that characterises the whole object
on every run:

- **Partition every difference by cause**, with a count per bucket.
- **Both directions** — rows only on the left, rows only on the right, counted separately.
- **An explicit `unexplained` bucket that prints as a number.** Anything not matching a named
  cause lands there rather than being rounded into the agreed pile.
- **Name the fields that never differ**, not only the ones that do. "Identity is intact on 5 of
  33 fields" is a finding; silence about them is not.

Once that exists, a scoped question can no longer produce a scoped investigation, because the
report is generated from the whole comparison every time.

The first run of that script immediately surfaced a row in a region nobody had discussed — which
is the point. It was an artefact of running mid-rebuild rather than a real defect, and saying so
took one line. Finding it took zero effort, because the script does not know which question was
asked.

## Corollary: a projection and a measurement must not share a voice

"Should close to 3" was written in the same register as a measured figure. The measurement came
back **25** — wrong by 22 units, and wrong about the *kind* of defect as well.

Either label it (*projected*, *estimated*, *not yet measured*) or measure it. Never let the
second word do the first job. A reader cannot distinguish your confidence from your evidence
unless you mark it, and they will act on the number either way.

## Guard

Before reporting an investigation, ask: **if they ask "is that everything?", can I answer from
what I already ran, or would I have to go and look?** If the second, the investigation is not
finished — regardless of whether the question asked has been answered.
