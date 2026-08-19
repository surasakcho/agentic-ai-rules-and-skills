# Do the straightforward thing — and when it turns out unexpected, stop and propose

**Task type:** agent workflow — any task where the result can disagree with what you expected.
**Related:** [`never-patch-a-key-to-force-a-join`](../data-engineering/never-patch-a-key-to-force-a-join.md)
— the same escalation for one specific case.
[`close-your-own-gaps`](close-your-own-gaps.md) — the **boundary case**, and the one most easily
confused with this rule; read the boundary section below.
[`cannot-is-a-task`](cannot-is-a-task.md) — exhaust the routes *before* escalating, so what you
bring back is a choice and not a shrug.
[`agree-the-output-contract-first`](../data-engineering/agree-the-output-contract-first.md) — the
same principle applied before the work starts instead of during it.

---

## The rule

**Do the straightforward thing. When the outcome is not what you expected, stop, report it, and
propose — implement nothing.** Never assume, and never quietly decide the resolution yourself.

Two halves, and both matter:

- **Straightforward first.** No pre-emptive cleverness, no workaround built in advance of a
  problem, no defensive special case for a situation you have not actually observed. The plain
  implementation is what makes a surprise *visible*; every accommodation you build in advance is
  a place a surprise can hide.
- **Surprise is a full stop.** A count that does not reconcile, values that disappear, a join
  that misses more rows than it should, a figure an order of magnitude off — that is the end of
  your autonomy on that thread, not an obstacle to route around.

## The sentence that gives it away

If you can write **"I noticed X, so I did Y"** — you should have written **"I noticed X. Here are
the options."**

That construction is the whole failure. It reads as diligence. It is a decision taken on the
user's behalf, recorded as an observation.

## Why silent resolution is worse than the problem it hides

- **The surprise was the finding.** Twelve values disappearing was not an obstacle in front of
  the task; it was the single most informative thing the task produced. Resolving it quietly
  spends the finding and returns nothing.
- **Your explanation is untested.** You resolve it against the story you have in your head. In
  the incident below, that story was wrong, and one command against the authoritative source
  would have shown it — but the fix had already shipped, so nobody ran the command.
- **A silent fix is unreviewable.** It arrives as a design decision, indistinguishable from
  everything else you did deliberately. Nobody knows to question it, because nobody knows a
  question was ever asked.
- **It launders a guess into an approved decision.** Once it is in the deliverable under a
  confident commit message, it stops being provisional.

## The boundary — and it is the part people get wrong

This rule does **not** say "ask before doing things." A rule that fires on everything gets
ignored, and its sibling rule [`close-your-own-gaps`](close-your-own-gaps.md) says the opposite
in its own domain: a gap in *your own verification* is work to do, not a question to ask.

**The test: does the resolution change what the user receives?**

| situation | do it | ask |
|---|---|---|
| You skipped a check you should have run | **run it** | — |
| Your screen covered 1 of 341 artifacts | **screen all 341** | — |
| Your comparison used the wrong column | **redo it correctly** | — |
| The corrected result disagrees with the source | — | **ask** |
| Rows vanished and you have a theory why | — | **ask** |
| Two defensible options exist and you prefer one | — | **ask** |

Closing a gap in your own rigour has exactly one right answer, so asking wastes a round-trip.
Choosing between defensible readings of the *data* has more than one, so deciding wastes the
user's authority. **One right answer: act. More than one: propose.**

## What a proposal owes

Escalating is not stopping. Bring: what you observed with numbers, what you have already ruled
out and how, the options with their costs, your recommendation and why — and everything that does
**not** depend on the answer already finished.

## The incident

A rebuild's row-level diff showed **12 values that previously had data coming back blank**. I
formed a theory on the spot — the code-remapping step must be wrong — implemented a conditional
to stop it, verified the 12 came back, and shipped it inside a defect fix that read as thorough.

I never said "12 values went blank, here is what I think is happening, which do you want?"

Every part of the theory was wrong. The remapping was the *intended* use of that table — a
sibling script had applied it that way for months. The 12 values had not been lost; they had
moved onto the row that sibling seats them on. And the underlying reality was a **split unit**:
one source population row covering two separate polygons, so both my version and the original
were assigning a whole population to one half. My conditional did not fix a mis-seat. It changed
which half won, and left **28 columns across 5 pairs, from one source, disagreeing with each
other in shipped output**.

The check that would have collapsed the theory — testing both code columns against the issuing
authority's roster — was **one command**, and it was run four user messages later, only after the
user rejected the explanation outright.

**Cost:** a wrong fix shipped, a wrong write-up published to two repos, an inconsistency
introduced into a dataset that did not have one, and four rounds of a person's time spent
dismantling a confident explanation of something that had never been checked.

---

*Earned from:* user instruction, immediately after the above — *"always do things straightforward.
When things turned out unexpected, prompt and propose a solution. Never assume or implicitly
decide any solution on your own."*
