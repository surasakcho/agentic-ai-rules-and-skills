---
name: unblocked-loop
description: Re-check what is actually blocked and work everything that is not, on a timer. Use at session start, every 30 minutes during long work, when a session has been waiting on someone, or when a turn is about to end with a list of things you need from other people.
---

# Unblocked loop

**A blocked list is a fact about a moment, not a property of the work.** Things get unblocked while
you are not looking — an operator answers, a peer finishes, a container comes back — and a session
that remembers what was blocked an hour ago stops working for reasons that no longer exist.

So this runs on a timer, and it **re-checks** rather than recalls. It is
[`a-remembered-claim-is-not-a-checked-one`](../../rules/how-we-work/a-remembered-claim-is-not-a-checked-one.md)
pointed at your own backlog.

## 1. Arm the timer — at session start, before anything else

Schedule this skill to fire every 30 minutes for the rest of the session.

**Re-arm it at the start of every session.** Scheduled jobs in Claude Code are session-scoped: they
die with the session that created them and expire on their own after 7 days. A timer you armed
yesterday is not running. **Do not assume it survived — check that it is scheduled, or schedule it
again.** Checking costs one command.

**Completion criterion:** a recurring job exists in *this* session, confirmed by listing them, not
by remembering that you armed one.

**There is no pause — only arm and delete.** Stopping this loop deletes the job, so it is
destructive to the schedule, and re-arming means invoking this skill again rather than resuming
anything. Say that out loud whenever you stop, because a reader who thinks they paused it will wait
for a firing that is never coming.

## 2. Enumerate the open work from the tracker, not from memory

Read the tracker itself. Whatever the repo declares — an issue list, a board file, a task file.
**Never work from your recollection of what was open**, which is the failure this skill exists to
interrupt.

**Completion criterion:** every open item is listed, with a count.

## 3. For each item, check whether the blocker still holds

This is the step that makes the skill worth running, and it is the one that gets skipped.

For every item you believe is blocked, **name the check that establishes it is still blocked** — and
run it. Not "still waiting on the operator": *the issue is still open, checked just now*.

Blockers that expire quietly, all of which have happened:

- the person you asked has answered — in an issue, a comment, a message you have not read
- a peer finished the thing you were waiting on
- a container, mount or service came back
- the artifact you needed was published somewhere you can now reach
- the thing was never actually blocked; you inferred it from one failure and never retested

**Completion criterion:** every item is either *moving* or has a **named, freshly-checked** blocker.
"I think that is still blocked" is not a state this step may end in.

## 4. Work everything that can move

Do the work. Not a plan for the work.

Order by what is cheapest to finish, not by what is most interesting — a finished small thing
changes the state for everyone waiting on it; a half-explored large thing changes nothing.

**Completion criterion:** no item remains that could have been advanced this turn.

## 5. For what is genuinely blocked, file it — do not raise it in chat

For each blocker that survived step 3, write it into the declared tracker. One decision per entry:

- **the decision or action needed**, stated so it can be answered yes/no or with one choice
- **why it cannot be settled without them** — the specific thing you lack
- **what it blocks**, named
- **what it costs to leave it**, including "nothing yet, but X on <date>"

**Chat is not a tracker.** A question asked only in a transcript cannot be searched, assigned,
reopened, or found from a phone, and it is compacted away. If it matters enough to ask, it matters
enough to file. See
[`open-decisions-go-in-the-tracker`](../../rules/how-we-work/open-decisions-go-in-the-tracker.md).

**Where it goes is configuration, never a literal in this file.** Read the tracker location from the
repo — its `CLAUDE.md`, its session declaration, or its issue host. If no tracker is declared, ask
once and record the answer where the next session will find it; do not invent a destination and do
not hardcode one estate's repository into a shared skill.

**Completion criterion:** every surviving blocker has an entry, and you can name its id.

## 6. Report three things, in this order

1. **What moved** — finished work, named.
2. **What is blocked** — with the check that established it, and the entry id where it is filed.
3. **What you are doing next**, which is the unblocked item you are returning to.

## 7. Stop on an unchanged streak — never on a single blocked reading

**A fully-blocked sweep is a normal result. The same fully-blocked sweep N times is a finding**, and
it is the one this step exists for: six consecutive firings once produced a byte-identical reading
— same tracker comment, same patches applying, same counts, same two peers already relayed to —
while every remaining item needed an act only the operator could take. **Six firings, one result,
zero state change: the loop was spending attention to re-print a constant.**

**Compare the SIGNALS, not the verdict.** Record what each check returned this sweep — the newest
tracker timestamp, the counts, the peer states, the pin — and compare against the last sweep's
record. *"Still blocked"* is a verdict and it is the same sentence every time; the readings behind
it are what tell you whether anything moved.

- **Any signal differs** → the streak resets to zero. Something moved, even if nothing unblocked.
- **Every signal identical** → the streak increments, and **the interval doubles.**
- **The interval reaches its ceiling** → stop, and say so in the terms below.

**Back off before you stop, and stop only at the ceiling.** A bare stop on the first blocked reading
contradicts this skill's own premise — blockers expire while you are not looking, and a loop that
deleted itself at 22:00 cannot notice the answer that arrives at 02:00. Doubling keeps an observer
alive at a cost that halves each time, so the founding premise survives and the constant stops being
re-printed.

### The stop is LOUD, or it is indistinguishable from a crash

**A loop that goes quiet and a loop that died look identical from outside**, which is this estate's
signature failure — see
[`silence-must-be-the-alarm`](../../rules/how-we-work/silence-must-be-the-alarm.md). So the final
turn carries four things and is not finished without them:

1. **that it stopped, and after how many identical sweeps**
2. **the constant reading** — the signals that did not change, in full
3. **the one command that re-arms it**, said plainly, with the note that this was a delete and not a
   pause
4. **the acts that would change any signal** — which is the list of what is owed and by whom

**Completion criterion:** a reader who sees only your last message can tell the loop stopped on
purpose, what it was seeing when it did, and what to do about it.

## The one forbidden output

> **A correct, well-organised list of the decisions you need from someone else is not a turn's
> work.** It is a status report on your own idleness, and producing it feels productive because it
> is genuinely difficult to write well.

**Unless you re-checked and nothing moved — then it is the answer.** Three outcomes, and only the
middle one is forbidden:

| what you produced | verdict |
|---|---|
| the list, having **re-checked** the signals this sweep | **correct** — and if the signals are unchanged, it is step 7's input |
| the list, **without** re-checking, because it was true last time | **forbidden** — this is the idleness report |
| work moved, or a blocker newly named and filed | good |

**The discriminator is whether the re-check happened, not how the answer looks.** Earlier wording
sent a blocked turn back to step 3 unconditionally, which told a session that had done the work
correctly to disbelieve a true answer and do it again — right most of the time, and wrong exactly
when the estate is genuinely and completely blocked, which is the moment the instruction matters.

## ⚠️ Boundary — "keep going" never means working past a refusal

**A refusal is an answer, not an obstacle.** This is the sentence that keeps this skill from being
dangerous, and it is not negotiable:

- a gate that refuses a command
- a denied tool or path
- a confinement the repo documents as deliberate
- a permission the user declined

None of those are blockers to route around. **Do not re-spell the command, split the write, switch
tools, or find another path to the same effect.** Fix the underlying thing if it is yours to fix;
otherwise name it, file it per step 5, and move to the next unblocked item.

**Working around a refusal is not unblocking yourself. It is the failure the refusal exists to
prevent**, and a session that does it quietly leaves no trace that the control was ever wrong —
see [`a-verb-list-is-not-a-boundary`](../../rules/testing/a-verb-list-is-not-a-boundary.md) on
silent accommodation.

## The cost of asking

Every question spends the attention of someone who has other things to do, and a question about
something you could have settled yourself spends it on nothing. Two things genuinely need them:

- **a decision only they can make** — a preference, a priority, a risk they own
- **an action only they can take** — placing a credential, editing a file your own guards deny

Anything else is a check you have not run yet.
