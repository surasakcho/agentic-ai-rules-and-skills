# A report past twenty lines ends with a TL;DR — under eight bullets, or it is not a summary

**Task type:** how-we-work — every user-facing report long enough that the reader must choose
what to read.
**Related:** [`shut-up-and-work`](shut-up-and-work.md) — cut the report to what carries facts;
this governs what remains once the cut still leaves something long.
[`default-to-silence`](default-to-silence.md) — whether to send at all.
[`open-decisions-go-in-the-tracker`](open-decisions-go-in-the-tracker.md) — the open ask
belongs in the TL;DR *and* in the tracker; the summary is not a substitute for the record.

---

## The rule

**If a report runs past roughly twenty lines, it ends with a TL;DR of fewer than eight
bullets.** Not a restatement, not a closing paragraph — the short list a reader could act on
having read nothing above it.

Three constraints, and the count is the load-bearing one:

1. **Under eight bullets.** A summary that grows with the report is not a summary; it is the
   report again. The cap forces a ranking, and the ranking is the actual work.
2. **Anything still waiting on the reader appears in it.** An open decision that exists only in
   the body has been buried by the same length the TL;DR exists to fix.
3. **It is not a licence to write long.** The cut comes first. This applies to what survives
   the cut, never as permission to skip it.

## The incident

A long working session produced report after report in the twenty-to-sixty-line range — tables
of verified state, commit references, competing recommendations, and several genuine questions
for the operator. Each was individually defensible: the facts were checked, the tables were
dense, nothing was padding.

The operator read them and **answered the last thing mentioned.** Not because the earlier
material was unimportant, but because a sixty-line report with six sections and two embedded
questions offers no ranking, and a reader supplies their own — usually recency.

Over the session that produced this rule, at least six blocking questions were asked in prose
inside long reports. Most were never answered. The information was present, accurate, and
well organised. **It was also unranked, and unranked is unread.**

**Cost:** decisions never made, presented as decisions not needed — and the reader doing the
summarising work that the writer declined to do, every single time.

## Why this is easy to get wrong

**Thoroughness feels like the safe direction.** Every additional verified fact seems to reduce
risk, so the report grows, and each individual addition is justified. The cost is invisible to
the writer, who already knows which three things mattered, and lands entirely on the reader,
who does not.

It also gets worse exactly when it matters most. A session that found seven real problems
produces a longer report than one that found none — so **the reports most worth reading
carefully are the ones least likely to be**.

And a long report *looks* diligent. It is the same shape as a log that records a failure in
correct English into a file nobody reads: the information exists, and existing is being
mistaken for arriving.

## Guard

- **Count before sending.** Past ~20 lines, the TL;DR is not optional. Under it, do not add one
  — a summary of five lines is noise.
- **Cap it at eight bullets and hold the cap.** If eight will not fit, the report is carrying
  more than one subject and should be split, not summarised harder.
- **Lead each bullet with the outcome, not the activity.** "X is broken, fix is Y" over "looked
  into X".
- **Every open ask gets a bullet**, phrased as the decision, not as background.
- **Write it last, from the finished report** — a TL;DR drafted first describes what you meant
  to say rather than what you said.
- **Never introduce a fact that appears only in the TL;DR.** If it is new there, it belongs in
  the body too; a reader who read the body must not be missing something.

---

*Earned from:* a session of dense, accurate, twenty-to-sixty-line reports in which six separate
blocking questions were raised and mostly never answered — not because the reader was careless,
but because nothing in the reports said which of six sections to act on first.
