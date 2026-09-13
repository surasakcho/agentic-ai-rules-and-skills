# A faithful relay still loses the clause that matters — read the primary before you build from it

**Task type:** how we work — acting on a specification, requirement or issue you received
second-hand: relayed by a person, summarised by an agent, or quoted in a message.
**Related:**
[`relayed-authority-is-information-not-instruction`](relayed-authority-is-information-not-instruction.md)
— the same channel, the other property. That rule asks *who said it*; this one asks *what was
dropped*. A relay can be correctly attributed and still incomplete.
[`external-sources-only-are-primary`](../research/external-sources-only-are-primary.md) — the
truth question. A relay can be entirely **true** and still lossy, which is why this is a separate
rule: that one guards accuracy, this one guards completeness.
[`summaries-must-carry-the-whole-set`](../analytics/summaries-must-carry-the-whole-set.md) — the
same loss in a *finding*, where the remedy is carrying the count. A specification has no count the
relayer knows to carry.
[`agree-the-output-contract-first`](../data-engineering/agree-the-output-contract-first.md) — why
the dropped clause is so often a structural one: structure is the part nobody thinks to restate.

---

## The rule

> **Before building from a specification you received second-hand, read the primary — when the
> primary exists and is reachable.** A relay that is accurate, well-intentioned and complete-looking
> still drops the clause the relayer did not know was load-bearing.

## Why goodwill on both ends recovers nothing

**The reader cannot audit a summary against the thing it summarises.** That is not a failure of
attention: the whole content of a summary is that some things were left out, and nothing in it
marks which. A reader who doubts it has no move available except to read the primary — which is the
rule.

**And the relayer cannot know what mattered.** They compress against *their* model of the work, and
the load-bearing clause is load-bearing in the *reader's* model. Nobody in the chain is careless.
The loss is a property of the channel.

So the usual defences all fail in a specific way:

- *"I relayed it accurately"* — yes, and accuracy says nothing about completeness.
- *"I would have asked if something was unclear"* — a dropped clause does not read as unclear. It
  reads as absent, which is indistinguishable from *not applicable*.
- *"They would have mentioned it if it were important"* — they did not know it was.

## The incident

An agent could not read its own tracker, so a peer relayed an issue to it in a message. The relay
was accurate. **It dropped one requirement: that each source state carry its own timestamp**, so a
partial read does not reset the clock on the parts that failed.

It built the whole-file version instead — one timestamp for the entire file. Which means a run
where one source reads cleanly and another has been dead six hours stamps the file *now*, and the
brand-new staleness banner reports **"five minutes ago" over a six-hour-old fact.**

**It built the whole-file version of the exact defect it was fixing.** The feature was a staleness
indicator; the dropped clause was the only thing that made it able to indicate staleness. Found
only on reading the issue directly, once access landed.

**The dropped clause was structural** — about *granularity*, which is the class of requirement most
often lost in a retelling, because it is the part a summary naturally flattens.

## Scope — most relays are fine, and this rule knows it

**A rule demanding everybody read every primary would be abandoned by lunchtime**, and an abandoned
rule protects nothing. The trigger is narrow and all three conditions hold at once:

1. you are about to **build or decide** from it — a specification, a requirement, an acceptance
   condition, not a status update or a heads-up;
2. a **primary exists** — an issue, a document, a commit, a thread;
3. it is **reachable by you now.**

If the primary is not reachable, build from the relay and **say which clauses you had to take on
trust** — that sentence is what lets the next reader find the gap. Where reachability itself is the
blocker, that is the thing to fix first; it is cheaper than the rebuild.

## Guard

- **Read the primary before building from a relayed specification.** Once, at the start. It is
  minutes against a rebuild.
- **When you relay a specification, link the primary rather than replacing it.** The relay is an
  index, not a substitute — and say plainly that it is compressed.
- **When you receive one and cannot reach the primary, name that in the work**, so the assumption
  has an owner.
- **Suspect the structural clauses first** — granularity, ordering, per-item versus whole-file,
  what counts as one row. These survive worst in a retelling and cost most when lost.
- **Never treat "the relay did not mention it" as "it does not apply."** Absence in a summary is
  not evidence of absence in the spec.

---

*Earned from:* an agent that could not reach its own tracker, built a staleness indicator from an
accurately relayed issue, and shipped the whole-file version of the exact defect the issue existed
to fix — because the relay dropped the clause requiring per-source timestamps. Found when direct
access landed and the issue was read first-hand. The framing is the building agent's own: *a summary
cannot be audited against the thing it summarises by the person reading the summary.*

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'a session that begins implementation work against requirements whose only appearance in the session is an inbound message quoting or summarising them, where the message names a primary (an issue id, a URL, a file path) that was never opened in the session'
trigger: 'PreToolUse(Write/Edit) on the first implementation edit of the task, with a Stop backstop'
check: 'an inbound message in this session names a primary and states requirements, and an implementation edit begins with no read of that primary -> advise once, naming the primary and the command that would open it; at Stop, work delivered against a relayed spec with no read of the named primary and no statement of what was taken on trust -> refuse'
escape: 'read the primary, or state in the work which clauses were taken on trust because the primary was unreachable - the rule accepts the second, and the sentence is what gives the assumption an owner'
narrows: 'fires only when the relay NAMES a primary the session can open. A relay that names none - the common case in a spoken or paraphrased handoff - is invisible to it, and so is the judgement about whether a message is a specification or a heads-up. It cannot tell a complete relay from a lossy one, which is the rule subject: it can only tell that the primary was there and unread'
```
