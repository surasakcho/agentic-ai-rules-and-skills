# A finding is a set — every retelling carries its size, not just its worst member

**Task type:** analytics, reporting, review — any time a finding is written down more than once.
**Related:** [`report-both-sides-of-a-comparison`](report-both-sides-of-a-comparison.md) — a
comparison has two results; this is the same discipline applied across *retellings* rather than
across *sides*. [`review-every-output`](review-every-output.md) — the compressed artifacts are
the ones to review. [`shut-up-and-work`](../how-we-work/shut-up-and-work.md) — terseness is
right; dropping a set member is not the way to get it.

---

## The rule

**When a finding has more than one member — two regions, three failing files, four affected
customers — every later mention of it must carry the count. Drop the members if space demands
it. Never drop the fact that there were N of them.**

## This is not concealment, and it does not happen at discovery

The first report is usually complete. The failure happens on the **second** telling, and every
telling after that. The finding gets compressed — into a status line, a cost table, a commit
message, a slide bullet, a rule write-up — and the summary keeps **one** member as the
illustration.

Which one it keeps is not random. **It keeps the most dramatic and drops the largest.**

The member that makes the best sentence is the one with the biggest per-unit effect: the
five-period gap, the 90% error, the customer who lost the most. The member with the biggest
*total exposure* is duller per unit and loses every retelling. So the surviving example is
reliably **not** the one that matters most in aggregate, and a reader who trusts the summary
believes the small vivid thing is the whole story.

## The phrasing that does the damage

The indefinite singular:

> "136 units mis-dated, **one** by five periods"

Every word is true. It reads as *one notable case and 135 minor ones*. The truth was **two
groups, of 48 and 88** — and the 88 was the omitted one. Compare:

> "136 units mis-dated **across 2 groups** — 48 by five periods, 88 by one"

Same length. Cannot be misread.

## Guard

- **Name every member.** Two or three almost always fit; it costs a handful of words.
- **If they truly do not fit, carry the cardinality** — "across 2 groups", "in 3 of the 17
  files". The count is what tells the reader something was elided.
- **Never write a bare indefinite singular** — *"one of them"*, *"the worst case"*, *"notably
  X"* — without the count beside it. That construction actively implies the rest are
  unremarkable.
- **When the set is uneven, say which way.** If one member is nearly twice another, the reader
  needs the ordering, because the vivid member answers "how bad is this really?" wrongly.
- **Audit where compression happens**, not where detail lives. The long log is almost always
  correct. Check status lines, cost tables, commit messages, slide bullets, and rule write-ups —
  including this one.

**Corollary: a worked example is not a population claim, and must say so.** Using one member as
a control or illustration is legitimate. Writing it up so the reader cannot tell whether it was
the *only* member is not. One clause fixes it: "of the 2 affected groups, this section works
through one".

## Why it costs more than it looks

A correct detailed record does not save you. Readers consult the summary — that is what a
summary is for — and form their belief there. When they later find a member that appeared in no
summary, the damage is not confined to that finding. **They must now re-audit everything else
you reported**, because nothing tells them which other summaries dropped a member. One elided
item converts a body of verified work back into unverified work, and that conversion is far more
expensive than the finding itself.

---

*Earned from:* a data-vintage defect affecting **two** groups — one with 48 units and a
five-period gap, one with 88 units and a one-period gap. Both were reported at discovery, three
separate times in conversation, and both appear in the project's findings log and task board.
**Every subsequent summary kept the 48 and dropped the 88** — the same-day impact line, a cost
table, the numbered project rule written from it, the rule published to this repo, and the
defect write-up, which used the 48-unit group as a worked control without noting a second group
existed. The reader found the missing group themselves a day later and reasonably concluded it
had been withheld. **The dropped group was the larger by 1.8x.** It lost every retelling because
a one-period gap is undramatic — while the covariates it governed moved on 88 of 88 rows, which
was the entire reason the defect mattered.
