# Quick and dirty is licensed only by a logged experiment — and the licence expires the moment it works

**Task type:** how-we-work — every piece of code written, at the moment you decide how carefully
to write it.
**Related:** [`scratch-code-lives-outside-the-repo`](../coding/scratch-code-lives-outside-the-repo.md) says
*where* a probe goes; this says *what entitles you to write one*.
[`bau-artifacts-are-built-permanent`](../coding/bau-artifacts-are-built-permanent.md) is the
other end of the same pipeline. [`reproducibility`](../research/reproducibility.md) and
[`research-and-qa-logs`](../research/research-and-qa-logs.md) — the log this rule requires.

---

## The rule

**Build for the long term by default. Never write something the quick way merely to make it
work.**

There is exactly one exception, and it is narrow:

> **Quick and dirty is permitted to PROVE A CONCEPT — and only under a written, structured
> experiment plan recorded under `research/` before the code is written.**

Three obligations come with that licence, and none of them is optional:

1. **No floating scratch.** Every throwaway script is accompanied by a log that states what
   question it answers, what was run, and what came back. A probe with no log is not a cheap
   experiment; it is an undocumented artifact whose only record is in one person's head.
2. **Nothing is written as "temporary."** All code has a specific, stated purpose and a full
   trace of what it produced. "Temporary" is a description of intent, never of what actually
   happens to a file.
3. **The licence expires on success.** The moment the concept is proved — *if it works at all* —
   write the permanent implementation immediately, and **prove the permanent one works.** Not the
   next session, not after the next question. The proof obligation transfers: a passing probe is
   not evidence about the code you keep.

**"It works" is the trigger to start building properly, not permission to stop.**

## Disposition — every artifact ends in exactly one of three states

At the end of the work, **nothing is left floating.** Go through the scratch
directory and put each artifact into one of these, explicitly:

| State | What it means | What is left behind |
|---|---|---|
| **Promoted** | it worked and is worth keeping | permanent code in its real home, separately proved, committed |
| **Logged** | it produced a finding but the artifact itself is not worth keeping | the finding recorded; artifact discarded |
| **Superseded** | a permanent version now covers it | nothing; deleted |

A dead end is **Logged**, not Superseded — "tried X, it does not work because Y"
is the finding most likely to be re-derived by someone later.

### Promotion is writing the permanent version — never `git add` on the probe

**Do not commit the scratch directory.** It is a strong temptation at exactly this
point: the work feels valuable, deleting it feels lossy, and committing it looks
like preservation. It is not.

- A probe is shaped by the question that was live when it was written. Committed
  as-is, it enters the repo with no docstring, no entry point, no test, and no
  statement of what it is for — and the next reader cannot tell it from code the
  project depends on.
- A scratch tree usually contains things that must never be committed at all:
  full copies of other repositories, binary intermediates, pickles, fixtures
  captured from a live machine.
- The permanent version is almost never the probe with a better path. In the
  incident below, the reusable tool was written a second time from scratch and
  the 150 probes contributed nothing to it.

**If someone asks you to "commit the scratch", the faithful reading is "make sure
none of this work is lost" — which is served by promoting, logging and deleting,
not by staging a temp directory.** Say what you promoted, what you logged, and
what you deleted, so the decision is visible and reversible.

## The incident

An investigation into why a pipeline's output disagreed with a reference file produced **over 150
ad-hoc scripts** in one session — grid searches, per-region probes, retry variants of the same
check with slightly different parameters. Not one had an accompanying record of what it asked or
what it returned.

The one piece of reusable tooling that came out of that session was **not** produced by promoting
any of the 150. It was written a second time, from scratch, because **nothing in the 150
recorded what any of them had established** — the findings existed only in the investigator's
head, and the scripts were pure liability with no offsetting asset for their entire existence.

A logged plan would have cost minutes per probe and changed both outcomes: each result would have
been recoverable by someone else, and promotion would have been a defined step with a defined
trigger instead of an event that simply never arrived.

**The second half of this rule was earned in the same week, first-hand and smaller.** An agent
ran a probe to confirm that a file-free command produced output identical to a vetted file. It
did — verified, byte-for-byte. The probe was never logged, and the promoted artifact was handed
over *as a chat message*, which is to say it was never written down at all. The concept was
proved and the permanent version was never built; the work survived only as long as the
conversation did.

**Cost:** 150+ undifferentiated files with no recoverable findings, and a reusable tool paid for
twice. In the smaller case, a verified result with no durable home.

## Why this is easy to get wrong

**The quick version is not chosen; it is defaulted into.** Nobody decides "I will write this
badly." The decision that actually happens is *"I just need to check one thing"* — which is true,
and which is also how every one of the 150 began.

And **success is the moment the pressure to promote disappears.** While a probe is failing, it
holds attention. The instant it works, the question it answered stops being interesting and the
next question is already pulling — so the promotion step arrives exactly when motivation for it
is lowest. That is why the trigger has to be mechanical ("it worked → build it now") rather than
a matter of remembering.

## Guard

- **Before writing a probe, write the plan.** A few lines under `research/` naming the question,
  the setup, and what result would settle it. If that feels disproportionate for the probe, the
  probe is small enough that you can answer the question directly instead.
- **Record the result in the same place, including a negative one.** "Tried X, it does not work
  because Y" is a finding, and it is the finding most likely to be re-derived by someone later —
  possibly you.
- **On success, promote before moving on.** Write the permanent implementation from a clean
  start, in its permanent home, and run a check against *that* code. Do not move, rename, or edit
  the probe into place.
- **Prove the permanent version separately.** The probe's passing result says nothing about the
  rewrite. This is where a promotion most often silently fails: the rewrite is assumed correct
  because the thing it was derived from was.
- **A session must not end with a proven concept and no permanent code.** If it has to, that is
  an explicit, recorded debt — named in the log and in the task list — not a silent one.

---

*Earned from:* an investigation that produced 150+ unlogged probe scripts and a reusable tool
that had to be written twice because none of them recorded what it had found — and, in the same
week, a verified experiment whose promoted result was delivered as a chat message and never
written down.
