# Retrieve the shared lessons weekly, and log every retrieval

**Task type:** agent workflow — keeping a project's adopted rules in step with the shared repo.
**Related:** [`publish-lessons-weekly`](publish-lessons-weekly.md) is the other half of the same
cycle — that one pushes what a project learned out; this one pulls what other projects learned
in. The skill that does the work is `retrieve-lessons`.

---

## The rule

**Run the retrieval pass at least once a week, and append what it found to a
`retrieved-lesson.md` in the repo — including the passes that found nothing.**

Publishing without retrieving is a one-way cycle: every project pays for its own mistakes and
learns nothing from the others. The publish rule already has a weekly cadence and a review log.
This is the same cadence and the same log discipline pointed the other way, and it exists
because the two halves decay differently — a missed *publish* loses one lesson, a missed
*retrieve* keeps repeating N of them.

## Why the log file, and not just the CLAUDE.md block

The `retrieve-lessons` skill writes a **pinned** block of links into `CLAUDE.md`: links rather
than copies, pinned to a shared-repo commit so `--check` can tell you the source moved. That
block answers *"what does this repo currently follow?"*

It does not answer the question that actually matters over time:

> **When was this last checked, what changed since, and did anyone read the change?**

A pin that is six months stale looks exactly like a pin that was verified this morning. The log
is what distinguishes them. `retrieved-lesson.md` records, per pass: the date, the shared-repo
commit before and after, which rules were **added, changed or removed**, and — the entry that is
easiest to skip and most worth writing — **what the reader decided to do about each change.**

**Adopting a rule is not the same as reading it.** A new rule arriving in the pinned block
changes nothing about how the project works until somebody looks at it and either applies it or
records why it does not apply here. The log is where that judgement lands.

## What a pass looks like

1. **Check the pin.** `retrieve.py --repo <repo> --check` exits non-zero when the shared repo has
   moved past the pinned commit. That failure is the trigger to read, not an error to silence.
2. **Diff the source.** Between the pinned commit and the current one: which rule files are new,
   which changed, which were deleted. A *deleted* rule matters as much as a new one — the shared
   repo deletes rules that later experience contradicted, and a project still following one is
   following something known to be wrong.
3. **Read the new and changed ones.** Not the titles. The incident is the part that transfers.
4. **Re-run the write** so the pin advances: `retrieve.py --repo <repo> --write`.
5. **Append to `retrieved-lesson.md`**: date, old pin → new pin, the added/changed/removed list,
   and one line per item on what it means here — *applied*, *already covered by our rule N*, or
   *not applicable because …*.

## An empty pass still gets logged

If the shared repo has not moved, write that down with the date and the commit. Two lines. The
value is entirely in being able to answer "when did we last check?" without guessing — and three
empty passes in a row is a real signal, either that the other projects are quiet or that nobody
is publishing.

## Guard

- **A stale pin is a defect, not a state.** If `--check` has been failing for weeks, the repo is
  following a snapshot nobody has looked at.
- **Never advance the pin without reading the diff.** Re-running `--write` to make the check pass
  is the retrieval equivalent of deleting a failing test.
- **Log the decision, not just the delta.** "3 rules added" is a changelog. "3 rules added; two
  applied, one not applicable because this repo has no web layer" is a record someone can trust
  later.

---

*Earned from:* a repo that had published nine rules outward over two days and never once run the
retrieval in the other direction — the consuming half existed as a skill, with no cadence
attached to it and nowhere to record that it had been run.
