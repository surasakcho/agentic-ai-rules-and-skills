# Escalate the blocker before polishing everything around it

**Task type:** agent workflow — any work that has passed through a review naming something you cannot resolve yourself.
**Related:** [`cannot-is-a-task`](cannot-is-a-task.md) is about surfacing what you cannot do;
this is about what happens *after* it is surfaced and then not escalated.
[`close-your-own-gaps`](close-your-own-gaps.md) is the opposite failure — this one is
closing gaps enthusiastically, just never the one that matters.

---

## The rule

**The moment a review names a blocker only the principal can clear, escalate it — before improving anything
else. Refining the unblocked half while the blocker sits in a footnote is not progress. It is displacement,
and it costs more than sunk cost because it looks exactly like diligence.**

Sunk-cost behaviour at least knows what it is pursuing. This does not: every individual round is defensible,
finds real defects, and improves the artifact. The work is good. It is simply spent on the half that could
never have been the constraint.

## The shape

1. Round 2 of a review names something the principal must decide.
2. It is recorded, accurately, in the document — usually in a footer, under a heading like "open questions".
3. **Nobody sends it.** There is no moment where not-sending is a decision; it is just never the next action.
4. Rounds 3 through 9 improve the parts that are not gated, because those are the parts that *can* be improved.
5. The artifact gets genuinely better and remains exactly as unable to start as it was at round 2.

**The tell is that every round ends with a fix list and none ends with a question sent upward.**

## The enabling condition is almost always a stale status line

In the case this rule comes from, the project's dashboard — the file every session reads at start-up — said
**"nothing is owed by the principal."** Three decisions were owed. The sentence had been true when written and
false within the hour.

**The gate looked closed, so work flowed downhill into whatever was not gated.** Nobody chose that. It is what
a stale status line does to a queue.

| | |
|---|---|
| **Whatever your project treats as its status surface must state what is *currently owed*** | A stale "nothing owed" mis-routes an entire session, silently |
| **When a decision is answered, ask what NEW questions it opened** | Answers generate questions. The status line usually records only the closure |
| **Every review round should end by asking "is anything here mine to send, not mine to fix?"** | Fix lists are the default output of review; escalations have to be deliberately looked for |

## What it costs

Measured, in one session: **673,065 tokens of review** on an instrument that a measured build put at
**141,000–177,000 to simply run** — deliberating at roughly **four times the cost of doing the thing**, on a
design that could not legally start until a permission nobody had requested.

And the two checks that could each have killed the design outright — *what does this metric actually count?*
and *put a confidence interval on that estimate* — were **never assigned in nine rounds.** One of them settled
it with a single documentation fetch. **Cheap decisive checks lose to expensive refinement, because refinement
is always available and a decisive check might end the work.**

## Guard

Before dispatching another review round, answer in one line: **what in the last round was mine to send rather
than mine to fix?** If the answer is "nothing", check the status surface actually says what is owed — because
the most common reason nothing looks escalatable is that something already recorded it as closed.
