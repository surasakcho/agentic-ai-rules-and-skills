# Write it down when you read it

**Task type:** how-we-work — every session that receives information it did not generate:
brainstorms, requirements, corrections, preferences, decisions given in passing.
**Related:** [`open-decisions-go-in-the-tracker`](open-decisions-go-in-the-tracker.md) — the same
failure for questions rather than statements.
[`silence-must-be-the-alarm`](silence-must-be-the-alarm.md) — why nobody notices: a lost idea
produces no output at all.
[`board-for-state-sprint-for-commitment`](board-for-state-sprint-for-commitment.md) — where the
captured item goes once it is a task.

---

## The rule

> **Anything worth keeping is written to a durable file at the moment it is received — not at the
> end of the burst, not when the session wraps, and never when someone asks whether you kept it.**

Acknowledging is not capturing. A one-line "noted" is a reply, and a reply lives in a transcript.

**The durable write happens before the next reply goes out.** If ten items arrive in ten messages,
that is ten writes, or ten appends to one file — but the file is current after each one, never only
after the tenth.

**Capture is separate from evaluation.** Write it verbatim first, attributed, undecided, marked as
undecided. Judging it, scheduling it, or reconciling it against something it contradicts are later
acts, and none of them is a precondition for writing it down.

**Contradictions get recorded as contradictions.** Two items that cannot both be true are two
records plus a note, not one record and a silent choice. Resolving on the fly is how the losing half
disappears without anyone deciding it should.

## The incident

An operator opened with *"I will throw some ideas here. I don't have time to make decision. Just
take all notes."* Nine ideas followed across nine messages — an event format, a logo concept, a
process change, and a chain of six that escalated into a complete reimagining of the product's
interface.

**Each was acknowledged in one line. None was written anywhere.** The session's own standing
instruction — recorded, in its own memory, from an earlier correction by the same operator — said
*"commit after every substantive message, do not batch."* It was not followed.

The items were finally written to a file only after the operator asked: **"Did you take note for all
these ideas?"** Nothing had been lost, because nothing had gone wrong yet. **That is the whole
problem: this failure is invisible while it is happening and total when it triggers.**

The operator's response was the rule: *"Do not wait until I ask. Write everything once you read
it."*

## Why this is easy to get wrong

**"Just take notes" sounds like permission to hold them.** It is the opposite instruction —
*notes* means *written down*. Being told not to analyse gets heard as being told to do less, and the
part that gets dropped is the durable write rather than the analysis.

**A fluent transcript feels like storage.** Everything is right there, in order, easy to re-read. It
is not storage: it is one compaction, crash, context rotation or session end away from gone, and
none of those announce themselves.

**Batching feels tidier and is strictly worse.** One clean file at the end reads better than ten
appends — but it only exists if the session survives to write it, and the whole burst is staked on
that. **The tidiness is bought with a single point of failure.**

**Acknowledging discharges the feeling of having handled it.** "Noted" is a real reply and it
satisfies the conversational obligation completely, which is exactly why the durable write stops
feeling urgent.

**And the person who gave it will not notice it missing.** They said it once, they moved on, and
they are relying on you. When an idea is lost, nobody reports a bug — the idea simply never comes up
again.

## Guard

- **Write before you reply.** The append and the acknowledgement are one action, in that order.
- **Verbatim first, judgement later.** Quote what was said. Paraphrase is where meaning quietly
  shifts, and the shift is undetectable once the original is gone.
- **"Noted" is not a capture** unless a file changed. If nothing was written, nothing was noted.
- **Mark items as undecided rather than holding them until decided.** An unanalysed record beats an
  analysed memory.
- **Record conflicts as conflicts.** Never resolve two incompatible items into one on the fly.
- **Keep your own un-answered suggestions too.** Un-answered is not declined, and the asymmetry —
  keeping theirs, dropping yours — silently loses half the conversation.
- **Never answer "did you record that?" by recording it then.** If that question can be triggered
  by anything other than curiosity, the rule is already broken.

---

*Earned from:* nine ideas delivered in nine messages, each acknowledged in one line and none written
down, against a standing instruction from the same operator that said not to batch — captured only
when they asked whether they had been, and followed by *"Do not wait until I ask. Write everything
once you read it."*
