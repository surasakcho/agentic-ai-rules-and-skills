# A realised omission is work to do, not a question to ask

**Task type:** agent workflow — any task where you report on work you did yourself.
**Related:** [`review-every-output`](../analytics/review-every-output.md) is what to check;
this is what to do the moment you notice you did not check it.

---

## The rule

**The moment you notice you skipped something you should have done, do it.** Do not report it,
do not ask permission, do not offer it as an option. The realisation and the fix belong in the
same turn.

This is not about scope changes — those still get discussed. It is about one specific,
recurring move: noticing your own gap and then handing it back.

| What you notice | What to do |
|---|---|
| "I only checked the summary totals, not the per-row values" | Check them |
| "I looked at one of N artifacts and called it reviewed" | Screen all N, eyeball the sample |
| "That check skipped a fifth of its columns on a name mismatch" | Fix it and re-run |
| "I verified the output but not that its population matches the input" | Verify it |

## Why asking is the wrong move here

The question has exactly one defensible answer, so putting it to the user costs a round-trip
to hear "yes".

Worse, it **launders an incomplete job into an approved one**. Once the user says "that's
fine", the gap becomes *their* decision rather than your omission, and it stops being tracked
by either party. A gap you name and close is finished work. A gap you name and hand over is
unfinished work wearing a status update.

The asymmetry is the point: closing the gap costs minutes, and the answer is always the same.
So the expected value of asking is negative in every branch.

## What still gets reported

Doing it silently is not the goal. The goal is that the report says **"this was wrong and is
now fixed, here is the evidence"** rather than **"this might be wrong, shall I look?"**

If the fix turns up something material, that is a finding, and it goes to the user with the
same weight as any other defect. In the incident below, closing three such gaps surfaced six
real defects that no automated check could see.

## The corollary that catches most of it

**Never let "I could verify this further" sit in a summary as a caveat.**

Either it was not worth doing — in which case do not mention it — or it was worth doing, in
which case it should already be done by the time the summary is written. A caveat listing your
own unfinished verification is a to-do list you have delegated to the reader.

The honest version of that caveat is different and still required: **state what you screened
versus what you actually inspected.** "I reviewed them" when you screened them is a false claim
about your own work. "I screened all N programmatically for these failure classes and inspected
these twelve by eye" is true, useful, and not a to-do list.

## What it looks like in practice

Three gaps were surfaced as caveats rather than closed, in one session:

1. **A column rename verified only by summary statistics.** Totals matching cannot detect a
   per-row shuffle. Diffing the pre- and post-rename files row by row took one command.
2. **A gallery of several hundred generated images "verified" after looking at one.** Writing a
   screen for the failure classes that had actually occurred in that project — blank output,
   no colour variation, orphaned files, missing entries, both directions of a completeness
   check — took twenty minutes and covered all of them.
3. **A cross-check that silently skipped a fifth of its columns** because it looked for a
   suffix spelled `sd` while the data used `std`. Caught only because the comparison count did
   not divide evenly by the number of statistics. The skip was `if name not in columns:
   continue` — the classic silent pass. Making it fatal took one line.

All three took minutes once actually attempted. Then, prompted to finish the job properly, a
full inspection of the documentation deck found **four stale numbers** that every automated
check had passed: a section describing a schema by its pre-rename names (invisible to the name
checker because the names were written as brace templates, which contain no bare identifier); a
stale intermediate file that made one slide state three different totals at once, each
individually "measured" but from two different vintages; a magic constant in a chart that made
its slices sum to neither total printed beside them; and a hardcoded count that had drifted.

**Both mistakes made while closing the gaps were caught by testing rather than assumed away** —
the silent skip above, and a freshness guard that compared against the data *after* a derived
column was added, so it would have fired on a correct input. A guard that cries wolf gets
switched off, which is worse than no guard.

## Mechanisable? Mostly not — and say so

The rule itself is behavioural and cannot be a test. Two of its consequences can be:

- **A silent skip must be fatal.** Any `if x not in y: continue` inside a verification loop is
  a place the check can pass by not running. Assert the expected count instead.
- **A stale input must be refused.** A step that reads an artifact another step produces should
  assert the two agree on the population they describe, and name the command to re-run. Reading
  a stale input is indistinguishable from reading a correct one unless something checks.

The rest is a disposition, and the honest thing is to write it as prose rather than ship a
crude proxy and call it enforcement.

---

*Earned from:* a data-preparation handoff, 2026-08. The user's reply to the third caveat was
**"Do it then"** — which is the only reply such a caveat can ever get, and the reason this rule
exists.
