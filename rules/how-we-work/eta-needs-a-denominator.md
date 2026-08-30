# "Almost done" needs a denominator, not a vibe

**Task type:** agent workflow — deciding whether to let a long-running job keep going or
interrupt it.
**Related:** [`known-blast-radius-demands-scoped-fix-everywhere`](known-blast-radius-demands-scoped-fix-everywhere.md)
is the decision this rule feeds — you cannot judge whether a scoped rebuild is worth building
without first knowing how far from done the current run actually is.

---

## The rule

**Before recommending "let it keep running, not worth interrupting," compute done/total
explicitly.** Recent progress velocity ("it went from 43 to 51 to 74") tells you the job is
alive. It tells you nothing about how close it is to finishing unless you also know the
denominator. Reporting steady progress and reporting proximity to completion are two different
claims, and only one of them was checked.

If the total isn't known, *that* is the finding — "I don't know the total, so I can't say
whether this is close" — not grounds for a confident recommendation in either direction.

## The incident

A background job had been running for over 90 minutes. Asked for a progress update twice, the
answer given each time was a raw count of files touched (43, then 51, then 74) with no total
attached. On the strength of that trend, plus a *different* nearby job genuinely being close to
its end, the recommendation was: not worth killing and rewriting this one, let it finish.

The user asked one question — "how many total?" — and a two-minute check of the job's own
input manifest (a directory listing of what it needed to fetch) showed the real total was
**roughly 378 files for the full run**. 74 was **about 20% done**, not "almost done." The
recommendation to keep waiting had been made without ever computing that fraction, extrapolated
instead from three points on a curve whose end was never looked up.

**Cost:** the user had to explicitly demand the denominator before the true scope was checked.
Had they not asked, the session would have kept waiting — potentially hours longer — on advice
that sounded calibrated ("steady progress, don't interrupt") but rested on a number that was
never gathered.

## Why this is an easy mistake to make

A rising counter *feels* like evidence of imminent completion, especially alongside a sibling
job that genuinely is close. But "rising" and "close to the end" are independent facts. A
counter can rise steadily for 20% of a job exactly as it rises steadily for 95% of one — the
shape of early progress carries no information about the total unless the total is known.

The tell, in hindsight: the recommendation used words like "close enough" and "not worth it"
without a single number that had a total on the other side of it — a direct instance of stating
a judgement that sounds quantitative while resting on nothing that was actually measured.

## Guard

- **Before saying a job is close to done, find its total.** For a download loop, check the
  manifest or file count it's working from. For a per-year or per-batch loop, check how many
  batches the job's own code iterates over. This is almost always a fast, cheap lookup — the
  same two minutes it took here, once someone finally asked for it.
- **State the fraction, not just the trend.** "74 of ~378 (about 20%)" is a claim someone can
  act on. "It's been climbing steadily" is not — it is consistent with both 20% done and 95%
  done, and the reader cannot tell which.
- **If asked "how much longer / how many total" and you don't know, say so and go find out
  before answering** — don't reach for the confident-sounding phrase ("should be close," "not
  much left") as a placeholder for a number you have not looked up.
- **A prior "not worth interrupting" recommendation is void the moment the real denominator
  changes the picture.** Re-evaluate immediately rather than defending the earlier call — the
  earlier call was made on incomplete information, and sunk time spent giving that advice is not
  a reason to keep giving it.

---

*Earned from:* recommending against interrupting a 90-minute background job on the strength of a
rising file count, without ever checking the job's own total — reversed within minutes once the
user asked "how many total" and the real fraction turned out to be about 20% done, not "almost
done."
