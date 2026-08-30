# For unattended work, silence is the alarm — a logged failure is an undetected failure

**Task type:** operations — scheduled jobs, backups, collectors, sync tasks, anything that runs
with nobody watching.
**Related:** [`validations-must-fail`](../testing/validations-must-fail.md) — a guard that cannot
fire; this is a guard that fires into a void.
[`status-fields-must-be-earned`](../data-engineering/status-fields-must-be-earned.md) — the same
decoupling between a success marker and the work it claims.

---

## The rule

**For anything that runs unattended, the absence of a success report is the alarm.** A failure
that only writes to a log is not detected, because **logs are pull and nobody pulls.**

Two orderings follow directly, and both are violated constantly:

1. **Do the work, then report success.** A success ping emitted before the fallible step reports
   that the *scheduler* fired, not that the *job* worked.
2. **Alert on absence, not on error.** Something outside the job must notice "this has not
   reported success in N periods." Errors can be logged; absence must page.

## The incident

A nightly backup job copied a machine's configuration into a repository and pushed. A second
host began writing to the same branch, so the push started failing — a plain non-fast-forward
rejection. The job logged it in full, including the standard remedy text naming the exact fix,
and exited.

**It ran that way three consecutive nights and nothing noticed.** The failure was found only
because somebody opened the repository for an unrelated reason and happened to compare it
against the remote. For three days the backup had silently stopped being a backup, while the job
continued to run on schedule, on time, every night.

Nothing was missing that a monitor could have seen. The evidence was complete, correct,
timestamped, and written in English — into a file that has no reader.

The same system carried the ordering error too: a runner pinged its healthcheck endpoint
**before** performing the step that could fail. Every run reported healthy whether or not the
work that followed succeeded. The health signal was structurally incapable of reporting the
failure it existed to catch.

**Cost:** three nights of configuration silently unbacked-up, and a health channel that had been
reporting the scheduler's liveness while appearing to report the job's.

## Why this is easy to get wrong

Writing the error to the log *feels like handling it*. The information exists, it is accurate,
and producing it took real care — so the failure gets mentally filed as "reported." It is not
reported. It is stored, in a place whose access pattern is "someone goes looking, usually
because something else already went wrong."

The gap widens with reliability. A job that has succeeded for months trains everyone,
correctly, not to check it. **The better a job's track record, the less anyone reads its log, and
the longer its silent failure will last.**

## Guard

- **Order the ping after the work.** If a job reports health, that report must come after every
  step that can fail, and must not be emitted at all on the failure path.
- **Exit non-zero on failure.** A job that logs an error and exits 0 is invisible to every
  supervisor, wrapper and scheduler above it. This is one line and it is skipped constantly,
  especially in shell, where `|| true` and unchecked pipelines swallow status by default.
- **Install a dead-man's switch for anything that matters** — a check that fires when a success
  marker is *older than expected*, not when an error appears. It is the only mechanism that
  catches a job that stopped running entirely, which no amount of in-job error handling can.
- **Ask of every unattended job: if this failed tonight, what would tell me, and when?** If the
  honest answer is "the log would say so," it is undetected. If the answer is "nothing, until
  someone needed the output," it is worse than undetected — the first symptom will be a missing
  artifact at the moment it is required.
- **Nothing that runs unattended may have "someone reads the log" as its only detection path.**
  Logs are for diagnosing a failure you already know about. They are not a detection mechanism
  and were never one.

---

*Earned from:* a nightly backup that failed on three consecutive nights, logged the rejection and
its own remedy in plain English each time, and was discovered only by accident — alongside a
health ping emitted before the step it was meant to be reporting on.
