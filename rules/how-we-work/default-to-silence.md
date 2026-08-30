# Default to silence — a message needs a reason to exist

**Task type:** agent workflow — deciding **whether to send** a message to the person you work for.
**Related:** [`shut-up-and-work`](shut-up-and-work.md) governs **how to write** a report once you have
decided to send one; this decides whether it should exist at all. Its caveat carries over intact — cutting
words is right, cutting counts is not.
[`research-and-qa-logs`](../research/research-and-qa-logs.md) is where the unsent material goes instead.
[`close-your-own-gaps`](close-your-own-gaps.md) — silence must never become a way to sit on a gap.

---

## The rule

**Default is silence. Do the work.** A message needs **one of four reasons** to exist:

1. **A decision only they can make.**
2. **A result that changes what happens next.**
3. **A blocker only they can clear.**
4. **A correction to something wrong they were already told.**

**Carrying none of the four is not a short message. It is a message that should not be sent.** Write it to
the record instead.

## The record is not the report

This is the mechanism, and it is worth stating plainly because it is counter-intuitive: **the material that
feels most worth sending is usually the material you have just written down.** You finish a careful piece of
work, commit the document that explains it, and then narrate that same document into a message — because it is
fresh, because it was hard, and because reporting it feels like the responsible end of the task.

It is not. It is the same content twice, and the second copy is the one that cannot be searched, cannot be
corrected in place, and arrives whether or not it is wanted. **If it is committed, it has been reported.** A
link and one line of what changed is the whole message.

## What does not earn a message

- **Progress and status.** "Now doing X", "X is done, starting Y."
- **Method.** What you checked, what you verified it against, what tool you used. This belongs in the log.
- **Self-assessment in either direction.** A defect confession with no decision attached is not
  accountability — it is asking the reader to do something with information they cannot act on. Write the
  defect into the record where the next person will actually hit it.
- **Restating a linked document.** If they can click it, do not summarise it in three paragraphs.
- **Asking for permission you already have**, or re-confirming a decision already made.

## Two failure modes silence can cause — guard both, they are opposite

**1. Sitting on a decision that is theirs.** This rule is *not* "ask less". A genuine decision — one where
proceeding under either assumption would waste real work or be unsafe — goes up **immediately**, in one line,
with the options. Suppressing that is the more expensive error, because the work gets done wrong rather than
merely narrated.

**2. Dropping counts to be brief.** Compression is where set sizes disappear. "Several issues" instead of
"6 issues, 2 unresolved" is not brevity. Where terseness and completeness conflict, **completeness wins** —
same tie-break as [`shut-up-and-work`](shut-up-and-work.md).

## The incident

An agent ran a multi-day task for one principal. Over a single working day it sent **six** substantial
messages — several hundred words each — about **one four-word decision** the principal had made. The content
was: what had been verified and how, which of its own earlier claims it had retracted, what its process
failures had been, and what it planned next.

Every one of those facts was **already committed** to the project's own record — an architecture decision file,
a handoff note, and a tracked issue — in more durable and more precise form than the messages restated them.

The principal's instruction, which is where this rule comes from: *only things that matter should reach me;
otherwise work with yourself and your team.*

**Cost:** the genuinely decision-relevant items — three open questions the principal alone could answer — were
distributed across those six messages, each surrounded by process narration. **Volume did not merely waste the
reader's attention; it hid the part that needed it.** That is the real damage, and it is why this is a routing
rule rather than a style preference.

## Guard

Before sending, name which of the four reasons applies — **in one word**. If you cannot, the message is a
progress report wearing a result's clothes. Commit it and move on.

A useful second check: **would this message still be worth sending if they had already read the commit?** If
not, the commit was the message.

---

*Earned from:* a direct user instruction, after a day in which six long process reports on a single four-word
decision buried the three open questions only that user could answer.
