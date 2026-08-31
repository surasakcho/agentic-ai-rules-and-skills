# Monitoring that the job ran does not monitor that the number is right

**Task type:** operations — scheduled jobs, pipelines, accruals, anything unattended that
produces a *value* rather than just an artifact.
**Related:** [`silence-must-be-the-alarm`](silence-must-be-the-alarm.md) — that rule covers a job
that **failed** and nobody noticed. This one covers a job that **succeeded**, on time, every
time, and was wrong throughout. The success report was present, truthful, and useless.
[`a-pr-nobody-is-asked-to-review-is-invisible`](a-pr-nobody-is-asked-to-review-is-invisible.md)
— "verify the effect, not the exit status" is this rule at the scale of a single command.

---

## The rule

**Liveness and correctness are different properties, and every cheap monitor measures the first
one.** A ping, an exit code, a heartbeat, a "last run" timestamp — each answers *did this
execute?* None answers *is the output right?*

To monitor the number you need a **second, independent derivation** of it. That is genuinely
more expensive than a ping, which is why it is almost never built. It is also the only thing
that catches this class of failure, which by construction produces no error at all.

## The incident

A delta-neutral trading strategy accrued funding income every 8 hours on a cron. It ran for
**59 consecutive days without a single failure**: no exceptions, no missed runs, no gaps in the
log, and a green dead-man's switch throughout.

It booked **one eighth** of the income it had earned.

The cause was one line: a resampler emitted the *in-progress* period as though it were complete,
so reading the last element returned a partial sum. The job fired 5 minutes into each period, so
"partial" meant one payment out of eight.

Every monitor in the system was satisfied, and every monitor was *correct*. The job had run. It
had not errored. It had written its log and pushed its state. The monitoring answered its
question accurately; the question was the wrong one.

**It was found only when someone asked a different question** — not "did it run?" but "does what
it booked match what the exchange actually paid?" That took a new tool, and the tool refuted the
first confident explanation of the bug within an hour of existing.

**Cost:** 59 days of a live sleeve's returns understated by ~8×, which made the most profitable
strategy in the book look like the least — and nearly caused it to be deprioritised on the
strength of its own broken accounting.

## Why this survives so long

- **It produces no error, ever.** There is nothing to catch, log, retry or alert on. Every
  failure mode the system was designed to handle is *absent*.
- **The wrong number is plausible.** `$0.00625` looks exactly as reasonable as `$0.05000` when
  nothing sits beside it. Magnitude errors hide in artifacts that carry no benchmark.
- **Reliability compounds the blindness.** A job with a perfect uptime record is the last place
  anyone looks, and its green history is offered as evidence that it is fine.
- **The obvious check is self-referential.** Comparing the booked figure against the value the
  job itself computed will always agree. See
  [`a-check-that-shares-a-source-is-not-a-check`](../testing/a-check-that-shares-a-source-is-not-a-check.md).

## Guard

- **For any job that produces a number that matters, build a reconciler**: derive the expected
  value from a source *outside* the job — the vendor's record, the venue's settlement history,
  the invoice — and alert when booked and expected diverge beyond a band. Set the band wide. It
  exists to catch structural loss, not to police rounding; a tight band produces noise, gets
  ignored, and becomes the next thing nobody reads.
- **Report three states, not two: OK / DIVERGED / UNKNOWN.** "I could not check" must never be
  encoded as "fine." Give UNKNOWN the *worst* exit code, so a run that could not fully check
  itself cannot be mistaken for ordinary noise.
- **Enumerate what to reconcile; never hand-list it.** Discover the units from the filesystem or
  the config, and report anything without a reconciler as UNKNOWN. In this incident a correct
  validation harness already existed — and had been pointed at a *different* sleeve for 37 days.
  The tool that would have found this in one run sat unused beside it.
- **Log the expectation next to the value.** An 8× gap is invisible in an artifact carrying only
  the booked figure. Write `expected` alongside `actual` and the discrepancy becomes readable by
  eye, by anyone, without running anything.
- **Schedule the reconciler.** An unscheduled detector is how the harness above went unused. If
  it only runs when someone remembers, it will be forgotten exactly when it matters.

## The question that finds it

For every unattended job, ask both, separately:

1. *If this stopped running, what would tell me, and when?* — the liveness question, usually
   answered.
2. ***If this ran perfectly and produced a wrong number, what would tell me, and when?*** — the
   correctness question. If the honest answer is "nothing, until someone reconciled it by hand,"
   then the number is unmonitored no matter how green the dashboard is.

---

*Earned from:* a funding-accrual job that ran flawlessly for 59 days, pinged green throughout,
and booked one eighth of what it had earned — discovered only by deriving the expected income
from the exchange's own settlement record rather than from the code that booked it.
