# A blocked list is a fact about a moment — re-check it, and work everything else

**Task type:** how we work — any session holding work it cannot finish. Every project, every
session.
**Mechanised by:** [`skills/unblocked-loop`](../../skills/unblocked-loop/) — the timer, the
re-check, and the filing step.
**Related:**
[`a-remembered-claim-is-not-a-checked-one`](a-remembered-claim-is-not-a-checked-one.md) — this is
that rule pointed at your own backlog, and the same discriminator applies: name the check that
says it is still blocked.
[`open-decisions-go-in-the-tracker`](open-decisions-go-in-the-tracker.md) — where a surviving
blocker goes. This rule is why there should be fewer of them than you think.
[`escalate-the-blocker-before-polishing-the-rest`](escalate-the-blocker-before-polishing-the-rest.md)
— the opposite failure, and both are live: that rule stops you burying a blocker under finished
work; this one stops you stopping because one exists.
[`cannot-is-a-task`](cannot-is-a-task.md) — a blocker is a deliverable with a route or a
requisition attached, never a full stop.

---

## The rule

> **Work everything that is not blocked, and re-check what is. A blocker is a fact about a moment,
> not a property of the work — so it is established by a check you can name, never by recalling
> what the list said last time.**

## Why the list rots in the direction of stopping

Blockers expire silently and **nothing tells you.** The operator answered in an issue you have not
opened; a peer finished the thing you were waiting on; the container came back; the artifact was
published somewhere you can now reach. None of those events arrive as a notification, and every one
of them turns a blocked item into an unblocked one while you are looking elsewhere.

So the error is asymmetric and always in the same direction: **the remembered list is longer than
the real one.** A session working from memory stops for reasons that have already gone away, and
the longer it waits the more of its list is stale.

There is a second source of the same error, worth naming separately: **an item that was never
blocked at all**, inferred from one failure and never retried.

## The forbidden output

> **A correct, well-organised list of the decisions you need from someone else is not work.**

It is a status report on your own idleness, and it is convincing precisely because writing one
well is genuinely difficult. It reads as diligence, it is accurate, and the turn produced nothing.

Three outcomes, and only one of them is forbidden:

| outcome | verdict |
|---|---|
| work moved | good |
| genuinely blocked, named precisely, filed where it can be answered | **good — naming it is the work** |
| a tidy list of what other people owe you, offered as the turn's output | **forbidden** |

## ⚠️ The boundary — this never licenses working past a refusal

**A refusal is an answer, not an obstacle.** A gate that refuses, a denied path, a permission the
user declined, a confinement the repo documents as deliberate — these are blockers, and the correct
response is to name them and file them. **Never re-spell the command, split the write, switch tools,
or reach the same effect another way.**

This boundary is load-bearing rather than decorative: a rule that says *keep moving* is exactly the
rule a session will cite while routing around a control. Working around a refusal is not unblocking
yourself, and because the session that does it quietly leaves no trace, it is also invisible to
whoever owns the control — see
[`a-verb-list-is-not-a-boundary`](../testing/a-verb-list-is-not-a-boundary.md) on silent
accommodation.

## The cost of asking, which is what makes the re-check worth running

Every question spends the attention of someone with other things to do, and a question about
something the session could have settled itself spends it on nothing. **Two things genuinely need a
person:** a decision only they can make, and an action only they can take. Everything else is a
check not yet run.

## Guard

- **Re-check every blocker before reporting it**, and name the check. "Still waiting" is not a
  check; "the issue is still open, read just now" is.
- **Never let a turn end with only a list of what others owe you.** If that is all there is, the
  blockers have not been re-checked — a list that long is rarely all true at once.
- **File a surviving blocker where it can be answered**, not in chat. A question that exists only
  in a transcript cannot be searched, assigned, or found by the person who would answer it.
- **A refusal is filed, never routed around.**
- **Re-arm the timer at session start.** A reminder that depends on remembering to re-read it is
  the weakest instrument there is, and a scheduled job does not survive the session that made it.

---

*Earned from:* an operator directive — *"for anything unblocked, keep doing it; remind yourself
every 30 minutes"* — issued after a session repeatedly ended turns with well-organised lists of
decisions owed by the operator, while work it could have done sat untouched. The same day, five
blockers that had been carried as current were settled or filed in a single pass once each was
actually re-checked.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'the turn itself: whether a durable write or a tracker entry was produced; whether the outgoing message is composed mainly of requests directed at the user; whether a recurring check is scheduled in this session; and whether each blocker named in the message was read from the tracker during this session'
trigger: 'Stop, plus a session-start check that the timer is armed'
check: 'msg is majority requests-to-the-user and the turn produced no durable write and no tracker entry -> refuse; a blocker named in the message with no read of the tracker this session -> advise, naming the item; no recurring job scheduled in this session -> advise once at session start'
escape: 'a turn whose honest output IS a filed blocker passes - the tracker entry is the durable write the check looks for. A session with genuinely nothing unblocked says so with the count it re-checked'
assisted_by: 'skills/unblocked-loop/ - a checklist, NOT an implementation. It is prose: it cannot refuse, so it cannot discharge this clause however faithfully it is followed. Withdrawn from implemented_by on 2026-09-13, hours after being claimed there, because a skill that cannot refuse reported as a gate is the exact defect a-classification-is-not-a-gate names'
narrows: 'gates the SHAPE of an idle turn and the presence of the timer. It cannot tell a re-checked blocker from a remembered one unless the check happened to touch the tracker in the same session, and it cannot see the failure this rule most cares about - a session that quietly works around a refusal instead of filing it, which produces a turn that looks productive by every observable here'
```
