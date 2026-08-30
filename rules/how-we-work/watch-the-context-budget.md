# Watch the context budget — prompt to compact at 40%, and say the number

**Task type:** agent workflow — every session, continuously.
**Related:** [`unexpected-means-stop-and-propose`](unexpected-means-stop-and-propose.md) — a
degraded context is where confident wrong explanations come from.
[`characterise-once-not-per-question`](characterise-once-not-per-question.md) — the cheapest way
to spend less context in the first place.

---

## The rule

**Track context usage continuously. When it passes 40%, tell the user the number and ask whether
to compact. Do not wait to be asked, and do not compact unilaterally.**

## Why a turn count is not a measure

The common version of this — *"suggest compacting after 20–50 prompts"* — is unusable, because
turns and context have almost no relationship:

- one `git status` in a large repo can cost more than thirty conversational turns
- reading a wide CSV header, a long log, or a directory listing can cost more than an hour of
  discussion
- a subagent's report arrives as one turn and can be enormous

**Measure the thing you are managing.** If a turn count is your trigger, you will compact far too
late in exactly the sessions that need it early — the tool-heavy ones.

## Why 40%, and not 90%

Because a compaction near the ceiling is a compaction under pressure. It has to discard more, it
has less room to preserve detail, and it lands mid-task rather than at a boundary. At 40% you can
still choose *when* — and finishing the current thread first is almost always the right answer,
because a summary written at a natural boundary keeps what matters and a summary written mid-diff
does not.

## Prompt — never compact on your own

Compaction is lossy and irreversible within the session. The user knows which thread they are
still holding; you know only what is in front of you. **Say the number and let them decide.**

> Context is at 43%. Want me to `/compact` before the next task?

State the percentage rather than a vague warning. "Getting long" is not actionable; a number is.

## The failure mode you are actually preventing

**Degradation is silent, and it feels exactly like ordinary confidence.** A model reasoning from
a compacted summary does not experience a gap where the detail used to be — it experiences a
recollection. So it answers from the summary instead of re-reading the file, and it answers
fluently.

The tell is a claim about a *specific artifact* — what a table contains, which direction a
mapping runs, what a script does — offered without a fresh read. **After any compaction, re-read
before asserting.** The summary is a map of the territory, and it was compressed by something
that could not know which detail you would later need.

## The incident

A long tool-heavy session compacted mid-work. Afterwards I explained, over four user messages,
what a 21-row lookup table meant and why a join behaved as it did — reconstructing it from the
summarised account rather than opening the file and the script that consumed it.

The explanation was wrong at the root: I had the table's purpose backwards, I had never read the
sibling script that had been consuming it for months, and I had never tested either of its columns
against the authority that issues those codes. That last check was **one command**. It ran only
after the user rejected the explanation outright, and it inverted the conclusion completely.

**Cost:** a wrong fix shipped, a wrong write-up published to two repositories, and four rounds of
a person's time spent dismantling a fluent reconstruction of something that had never been read.

---

*Earned from:* user instruction — *"always monitor percent of context. If exceed 40%, prompt for
compact."* — given at the end of the session described above.
