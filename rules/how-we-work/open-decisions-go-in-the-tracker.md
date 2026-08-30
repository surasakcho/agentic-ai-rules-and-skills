# An open decision lives in the tracker, not in the last message that mentioned it

**Task type:** how-we-work — any time work stops and waits on a human's answer.
**Related:** [`escalate-the-blocker-before-polishing-the-rest`](escalate-the-blocker-before-polishing-the-rest.md)
— raising it at all; this is what happens to it after it is raised.
[`silence-must-be-the-alarm`](silence-must-be-the-alarm.md) — the unattended twin: there,
nobody reads the log; here, nobody re-reads the scrollback.

---

## The rule

**Every question put to a human that blocks or shapes work gets written into the project's
durable tracker at the moment it is asked** — the file, board, or issue that outlives the
conversation. Asking in prose is how you raise it. Writing it down is how it survives.

The tracker entry records what is being decided, what is blocked on it, and what the default
is if no answer comes. A question with no default is a question that can only stall.

**Answering is what removes it, not asking again.** An ask repeated in a later message is
still one open decision, not two, and it still needs exactly one durable entry.

## The incident

One long session put at least six decisions to its operator, inline, in prose: whether to
query a peer machine for facts that could not be observed locally; whether a blocked service
should be re-tried against corrected numbers; where a newly cloned repository should run;
whether a config file's drift should be resolved toward the repo or the machine; whether to
schedule a recurring sync; and when to schedule a rehearsal that required deliberately
stopping a production job.

**Each was asked once, clearly, and then buried by the next unit of work.** The peer-machine
question was raised twice across two separate sessions and never answered either time — it
survived only because it happened to be written into a handoff file, which is the mechanism
this rule generalises.

The failure mode is specific and worth naming: the operator answers with a bare **"yes"**,
which resolves *the most recent* ask. Every earlier open ask is silently dropped, and nothing
anywhere records that it was dropped. Both sides then proceed believing the queue is empty.
The agent has no list to re-read, and the human has no list to answer.

**Cost:** decisions that were never actually made, presented as decisions that were not needed
— which is indistinguishable from progress right up until the un-made decision matters.

## Why this is easy to get wrong

**Asking feels like handing it over.** The question was clear, it was specific, it named the
trade-off — so it gets mentally filed as "with the operator now." It is not with anyone. It
is in a transcript, and a transcript's access pattern is "scroll back, usually because
something already went wrong."

It gets worse exactly as the work gets better. A productive session generates more asks and
buries them faster, because each new result pushes the last question further up. **The more
useful the session, the more reliably its open questions are lost.**

And a buried decision does not announce itself. Unlike a failed command, an unanswered
question produces no output at all. The next session inherits a system with several unmade
decisions in it and no way to tell which parts of the design were chosen versus defaulted.

## Guard

- **Write the entry when you ask, not when you finish.** If it is worth interrupting a human
  for, it is worth ten seconds in the tracker. Deferring the write to end-of-session is how
  it gets lost, because end-of-session is exactly when context is thinnest.
- **Record the default alongside the question.** "If no answer, I will do X" turns an
  indefinite stall into a decision with a deadline, and lets a human resolve it by silence
  when that is genuinely fine.
- **Treat a bare "yes"/"no" as resolving one ask — the most recent.** Say which one you took
  it to mean, and re-surface the others. Never let an ambiguous affirmative silently close a
  queue.
- **Re-read the open list before reporting progress**, and state what is still waiting. A
  status report that omits the open questions is a status report that is wrong.
- **One entry per decision, updated — not appended per re-ask.** Re-raising a question in
  conversation must not create a second tracker item; it should bump the one that exists.
- **On handoff, open decisions are the first section, not a footnote.** The next session
  cannot infer which choices were made deliberately and which were merely never made.

**Where the tracker lives is per-project and must be stated in that project's own
configuration** — an issue tracker, a board, a `TODO.md`, a handoff file. The rule is that
one exists and is written to at ask-time; naming a specific location here would publish one
machine's layout into every project that adopts this.

---

*Earned from:* a session that asked its operator six separate blocking questions in prose,
had one answered by a bare "yes" that resolved only the most recent, and left the rest
undetected — including one that had already gone unanswered across two prior sessions and
survived only because a handoff file happened to capture it.
