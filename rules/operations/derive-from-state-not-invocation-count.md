# Derive from state, never from how many times you ran

**Task type:** operations — anything scheduled, retried, or run unattended, especially where each
run accumulates a value.
**Related:** [`validations-must-fail`](../testing/validations-must-fail.md) — the same disease in
guards rather than accumulators. [`status-fields-must-be-earned`](../data-engineering/status-fields-must-be-earned.md)
— a recorded status that outran what actually happened.

---

## The rule

**Never compute a quantity from how many times your code ran. Compute it from what the world
says.**

Any value derived from invocation count carries a silent assumption: *my scheduler is perfect,
has always been perfect, and always will be.* Miss a run and the value is short with no
catch-up. Repeat a run and it double-counts. Neither raises an error, because from the code's
point of view nothing went wrong — it did exactly what it was told, the right number of times
minus one.

The replacement is a **watermark**: record when you last did the thing, and at each run compute
the elapsed span from the recorded mark to now.

## The incident

An unattended job accrued interest on idle capital. It ran on an eight-hour schedule, so it
credited a flat eight hours per invocation:

```python
accrue_idle_yield(state, hours=8.0)
```

Correct on average, and correct on every run anyone ever watched. Wrong the moment the schedule
was not honoured — a host reboot, a fencing guard holding the job back, a failover, an
operator's maintenance window. A missed run silently under-credited a full period with no
mechanism to notice or catch up; a re-run double-credited.

The direct money was trivial: four missed cycles across two strategies, about eleven cents. **The
cost was not the money.** That accumulated value was the equity curve against which a
go/no-go decision to deploy real capital was measured. A small hole, pointed in an unknown
direction, in the one number the decision depended on.

The same system carried a second instance of the identical assumption: scheduled jobs whose hour
fields were written to mean "five minutes after settlement" but evaluated by the scheduler in a
different timezone, so they fired an hour and five minutes late — for months, correctly, exactly
as configured, and not as intended. The code assumed a property of its scheduler that nobody had
ever checked.

## Why this is easy to get wrong

**It reads as a simplification, not an assumption.** `hours=8.0` in a job that runs every eight
hours looks like a constant being passed to a function. It is actually a claim about
infrastructure, embedded in arithmetic, with no comment marking it as such and nothing that
fails when it stops being true.

And it is *correct in testing*, permanently. No test run misses a cron fire. The failure only
appears in production, only when something else has already gone wrong, and it appears as a
number that is slightly off rather than as an error — so it is discovered, if ever, long after
the state that produced it is unrecoverable.

## Guard

- **Grep your own code for constants that equal your schedule period.** A literal matching your
  cron cadence, sitting in an accumulation call, is the signature of this bug. It will look
  deliberate, because it was.
- **Replace with a watermark, and give it its own field.** Not the general-purpose
  `last_updated` a save routine stamps — that is written on paths that have nothing to do with
  the accumulation, and a crash between accruing and saving will re-credit the same span. A
  dedicated mark means one thing: *credited through here*.
- **Then clamp, because unbounded elapsed time is worse than a fixed constant.** A restored
  backup, a clock skew, or a long outage will otherwise invent value out of arithmetic:
  - elapsed negative → credit zero, warn;
  - elapsed beyond a stated maximum → credit the cap, warn **loudly**, and say the gap needs
    investigating before the output is trusted.
  Prefer under-crediting to inventing. "Never silently invent" beats "always be exact".
- **Advance the watermark on every exit path** — including the clamped path and the path where
  there was nothing to do. A path that returns early without advancing re-processes the same
  span forever.
- **Make the operation idempotent**, so a duplicate run is a no-op rather than a double-count,
  and say so where it is scheduled.
- **Where the value cannot be reconstructed from elapsed time** — a missed reading of something
  that only existed at that instant — a watermark is not enough and you need real backfill from
  a historical source. Say which of the two you have; do not let the elapsed-time fix imply
  coverage it does not provide.

---

*Earned from:* an unattended accrual job that credited a fixed period per invocation because it
was scheduled at that period, quietly under-counting every missed run — in a system where that
accumulated number was the evidence for a decision to commit real capital.
