# A correction lands where you noticed it, not where the claim lives

**Task type:** how-we-work — any project that writes things down and later finds one of
them wrong. Figures, decisions, capabilities, statuses, API contracts, README claims.
**Related:** [`a-correction-is-not-a-control`](a-correction-is-not-a-control.md) — the
adjacent failure: correcting loudly while the object survives unchanged.
[`known-blast-radius-demands-scoped-fix-everywhere`](known-blast-radius-demands-scoped-fix-everywhere.md)
— the same discipline for code.
[`discriminate-by-executing-not-inspecting`](discriminate-by-executing-not-inspecting.md)
— why "I corrected it" is an inspection, and the grep is the execution.
[`register-the-retraction-when-you-make-it`](register-the-retraction-when-you-make-it.md)
— the unguarded flank: this rule reaches every place the claim lives, that one is about
knowing it needs correcting at all.
**Mechanised by:** the [`stale-claim-check`](../../skills/stale-claim-check/SKILL.md) skill.

---

## The rule

> **When you retract a claim, find every place that still ASSERTS it — not every place
> that contains the string.** The correction is not finished at the sentence where you
> spotted the error.

Corrections are written from where attention happened to be. You strike the bullet in
front of you, or put a banner at the top of the file you were reading, and you feel
finished, because the thing you were looking at is now right.

**The claim, however, lives wherever it was ever restated.** A decision record's summary
line. A neighbouring document that quoted the figure. A docstring citing a section that
has since closed. Those copies do not know they are stale, and each one reads as
authoritative to whoever finds it next.

## The worst case is not the obscure copy

It is the **canonical** one. In the incident this rule comes from, four retractions were
recorded correctly — banner at the top, offending bullet struck — and every one still left
the original claim standing elsewhere. In the worst instance the survivor was a decision
record's own **Decision statement**: the single sentence anyone citing that document would
quote. The banner said the figure had changed; three lines down, the Decision still
asserted the old one.

A later instance was a docstring that cited an "unresolved / threshold unset" section as
its authority for a default. That section had been closed hours afterwards by a ruling
setting the number. The code kept the old default for a day, and the citation was what
stopped anyone checking — **a citation that outlives the thing it cites is worse than no
citation.**

## Why it is easy to get wrong

The feeling of having corrected something is produced by the *act* of correcting, and the
act happens in one place. Nothing about it prompts you to ask where else the sentence
went. And the correction is genuinely, visibly there — so anyone auditing your diligence,
including you, sees a retraction and stops.

**Retraction and propagation are different jobs.** Doing the first well produces no
pressure at all to do the second.

## What to do

1. **Register the claim the moment you retract it** — the old pattern, the live value, and
   why it changed. Not later; later is where this fails.
2. **Search for assertions, not occurrences.** A retraction must quote the old value, so
   an occurrence is only a problem when nothing nearby marks it superseded.
3. **Run the check before publishing anything** whose numbers or decisions have moved, and
   let it gate the commit.
4. **Report the real-to-flagged ratio** when you cite a run. A checker that fires on
   careful phrasing gets muted, and a muted checker is worse than none.
5. **Treat a green run as "the registry is clean"**, never as "the repo is clean".

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: deferred
observable: 'files that still ASSERT a retracted claim - the registered pattern present with no supersession marker inside the marker window'
trigger: 'pre-commit'
check: 'for row in registry - hits = grep(row.pattern) minus marked_superseded; any hits -> block'
escape: 'marker vocabulary (superseded, revised, rescinded, no longer) near the figure, or a file-level exempt marker for a file that is the worked example'
implemented_by: 'skills/stale-claim-check/'
note: 'green means the registry is clean, never that the repo is - report coverage, not colour'
```
