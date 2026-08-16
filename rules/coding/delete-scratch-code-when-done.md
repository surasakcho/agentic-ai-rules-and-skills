# Never leave scratch code behind — write it, use it, delete it

**Task type:** coding — any investigation, probe, or one-off check written to answer a question
rather than to ship.
**Related:** [`surgical-verified-change`](surgical-verified-change.md) is about changes to real
code; this is about code that was never meant to become real code.
[`characterise-once-not-per-question`](../agent-workflow/characterise-once-not-per-question.md)
— the fix for a scoped investigation is a real, saved script; this rule is what happens to
everything that isn't that script.

---

## The rule

**A script written to answer one question, during one investigation, gets deleted the moment
it has answered that question.** If the investigation turns up something worth keeping — a
reusable check, a documented derivation — that gets written as real code, saved in the
project's normal code location, and committed. It does not get produced by leaving the scratch
version lying around.

There are exactly two end states for a script: **deleted**, or **real code**. "Still sitting in
a scratch folder, maybe useful later" is not a third state — it is the first state, deferred.

## The incident

One reconciliation investigation — root-causing why a pipeline's output disagreed with a
reference file for several regions — produced **over 150 ad-hoc Python scripts** in a scratch
directory over the course of one session: grid searches, per-region probes, one-off geometry
scans, retry variants of the same check with slightly different parameters. None were deleted.

By the end of the session, the directory listing itself carried no information: nothing
distinguished a script that had answered its question and could be thrown away from one that
encoded a check worth keeping. The one piece of real, reusable tooling that came out of the
session — a full reconciliation script that partitions every disagreement by cause with an
explicit "unexplained" bucket — was **not** produced by promoting any of the 150 scratch
scripts. It was written a second time, from a clean start, and saved properly in the project's
real script directory. The scratch scripts contributed nothing to it except the understanding
already in the investigator's head — which means they were pure liability with no offsetting
asset once that understanding existed.

**Cost:** 150+ files of undifferentiated signal, all of it now permanent unless someone does an
audit pass later to sort disposable from load-bearing — an audit that has to re-derive, file by
file, a judgement the original author already made once and simply didn't act on.

## Why this is worse than it looks

A pile of undeleted probes isn't neutral clutter — it actively misleads:

- **It can be mistaken for the real pipeline.** Nothing in a filename says "this was a
  hypothesis test that failed" versus "this is what actually produced the shipped number."
- **It can get cited back as evidence.** A later session (or a later question in the same
  session) reading a scratch script's output can treat it as a source, the same failure mode as
  [two files from one author counting as two
  sources](../data-engineering/adjudicate-with-an-external-source.md) — except here the second
  "source" is not even a considered result, it's a discarded intermediate step that happened to
  still be readable.
- **It defeats the reproducibility guarantee.** A project rule that "every output must be
  regenerable from code kept in the repo" is only meaningful if the repo distinguishes code
  that regenerates a real output from code that was a rabbit hole. A scratch folder that never
  gets pruned makes that distinction unrecoverable from the repo alone.

## Guard

At the moment a scratch script has done its job — the question is answered, the hypothesis is
confirmed or refuted — that is the moment to act, not later:

- **Answer not worth keeping the method for?** Delete the script now, in the same turn. Don't
  leave it "just in case."
- **Answer worth keeping the method for?** Don't edit the scratch file into shape in place.
  Write it as real code — proper docstring, no hardcoded scratch paths, wired into whatever
  makes the project's outputs reproducible — save it in the project's real code location, and
  *then* delete the scratch original. The real version earns its place by being written
  properly, not by being promoted.

If a session is about to end (or hand off) with scratch scripts still present, that is the
signal the cleanup pass was skipped, not evidence that the scripts might be needed — per
[`close-your-own-gaps`](../agent-workflow/close-your-own-gaps.md), noticing this is the same
turn as fixing it.

---

*Earned from:* a land-use reconciliation investigation that produced 150+ uncommitted, undeleted
scratch scripts, none of which turned out to be the reusable artifact the investigation actually
needed — that was written separately and properly instead.
