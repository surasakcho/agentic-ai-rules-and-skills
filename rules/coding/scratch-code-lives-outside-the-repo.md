# Scratch code lives outside the repo — never in it, not even in a scratch folder

**Task type:** coding — any investigation, probe, or one-off check written to answer a question
rather than to ship.
**Related:** [`surgical-verified-change`](surgical-verified-change.md) is about changes to real
code; this is about code that was never meant to become real code.
[`characterise-once-not-per-question`](../agent-workflow/characterise-once-not-per-question.md)
— the fix for a scoped investigation is a real, saved script; this rule is what happens to
everything that isn't that script.

---

## The rule

**A script written to answer one question, during one investigation, is written outside the
repository entirely — a system temp directory, a scratchpad path, anywhere version control
never sees it.** If the investigation turns up something worth keeping — a reusable check, a
documented derivation — that gets written as real code, from a clean start, in the project's
normal code location, and committed.

**"Write it in the repo's `scratch/` folder, then delete it when done" is not this rule — it is
the weaker version this rule replaced, and it fails the same way "remember to clean up later"
always fails: the deleting step gets skipped under load.** The fix is not better discipline
about deleting; it is removing the option to forget. Code that was never inside the repo cannot
accumulate in it, cannot get accidentally `git add`ed, and cannot get mistaken for something the
project depends on — no matter how the investigation ends or how the session gets cut off.

There are exactly two end states for a probe script: **it never touches the repo**, or it
becomes **real code**, written properly the first time it's saved inside the repo. There is no
third state where it sits in an in-repo scratch directory "for now."

## The incident

One reconciliation investigation — root-causing why a pipeline's output disagreed with a
reference file for several regions — produced **over 150 ad-hoc Python scripts** inside the
project's own `scratch/` directory over the course of one session: grid searches, per-region
probes, one-off geometry scans, retry variants of the same check with slightly different
parameters. The project's own convention at the time was "write it in `scratch/`, delete it when
you're done" — and none were deleted, because "when you're done" never arrived as a distinct,
remembered step; the investigation just moved on to the next question.

The one piece of real, reusable tooling that came out of the session — a full reconciliation
script that partitions every disagreement by cause with an explicit "unexplained" bucket — was
**not** produced by promoting any of the 150 scratch scripts. It was written a second time, from
a clean start, and saved properly in the project's real script directory. The scratch scripts
contributed nothing to it except the understanding already in the investigator's head — pure
liability, no offsetting asset, the whole time they existed.

**Cost:** 150+ files of undifferentiated signal, now permanent inside the repository unless
someone runs an audit pass to sort disposable from load-bearing — an audit that has to
re-derive, file by file, a judgement the original author already made once and simply never
acted on.

## Why "delete it after" isn't enough

The first version of this rule said: write scratch code in the repo, delete it once it's
answered its question. That is strictly worse than never writing it in the repo at all, for one
structural reason — **deleting is a step that can be skipped, and a directory that can be
skipped will be, at volume, under time pressure, across a long session.** 150 scripts and zero
deletions is not 150 individual lapses of discipline; it is one systemic fact about how "clean
up when done" behaves when "done" is fuzzy and the next question is already pulling attention
forward.

Writing outside the repo removes the failure mode instead of asking for better compliance with
it:

- **Nothing to `git add -A` by accident.** A probe script sitting in `/tmp` or a session
  scratchpad cannot end up in a commit, no matter how broad the staging command.
- **Nothing for the next reader to misjudge.** A script that was never in the repo cannot be
  mistaken for the real pipeline, and cannot get cited back as evidence the way [two files from
  one author get counted as two
  sources](../data-engineering/adjudicate-with-an-external-source.md) — there is no second
  artifact sitting around to be misread as a considered result.
- **Nothing to prune later.** The reproducibility guarantee — every output regenerable from code
  kept in the repo — stops needing a periodic audit to hold, because the repo only ever
  contained the code that was meant to regenerate something.

## Guard

Before writing a script whose only purpose is to answer a question you're holding right now:

- **Put it in a temp directory outside the repository** — the OS temp dir, a session scratchpad,
  anywhere that is not tracked and not inside the project tree. Many agent environments already
  provide exactly this (a scratchpad path separate from the working repo) for precisely this
  purpose — use it by default, don't reach for the repo's own directories out of habit.
- **If the answer turns out to be worth keeping the method for, don't move or edit the temp
  file into the repo.** Write the real version from scratch in the project's real code location
  — proper docstring, no scratch-path artifacts, wired into whatever makes the project's outputs
  reproducible — and let the temp original expire wherever it was written.
- **If a session is about to end with scratch code sitting inside the repo tree**, that's the
  signal the rule was skipped this time, not evidence the code might be needed — per
  [`close-your-own-gaps`](../agent-workflow/close-your-own-gaps.md), noticing this is the same
  turn as moving it out or deleting it.

---

*Earned from:* a land-use reconciliation investigation that produced 150+ scratch scripts inside
a project's own repo-tracked `scratch/` directory under a "delete when done" convention that
predictably did not get followed — revised, on the same project's direct feedback, to keep
scratch code out of the repository in the first place rather than trust it to be deleted.
