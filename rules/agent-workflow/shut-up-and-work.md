# Shut up and work

**Task type:** agent workflow — how you write every user-facing report.
**Related:** [`report-both-sides-of-a-comparison`](../analytics/report-both-sides-of-a-comparison.md)
— that rule wins wherever the two conflict. Cutting words is right; cutting counts is not.

---

## The rule

**Do the work. Report the result. Skip everything in between.**

No preamble, no narrating what you are about to do, no restating the request, no summarising in a
paragraph what a table shows better, no closing offers of further help nobody asked for. **If a
sentence does not carry a fact the user does not already have, delete it.**

## What survives the cut

- **Measured numbers**, with what was measured and against what
- **What is broken, what is fixed, what is still open** — stated flatly
- **A real question**, when the answer is genuinely the user's to make. One line, not a preamble

## What does not

- "Great question", "You're absolutely right", "Let me go ahead and…", "I'll now…"
- Explaining the plan and then executing the same plan. Just execute it
- Repeating a finding already stated earlier in the same message in different words
- Hedging that adds no information — "it seems", "roughly", "should be fine" — when the thing is
  measurable. Measure it, or say you did not
- Self-congratulation, and equally self-flagellation. Both are noise

## Terseness is not vagueness

This is the failure mode to watch, and it is the more dangerous one.

> "340 rows disagree, all in 4 regions" — short **and** complete.
> "Mostly matches" — short and useless.

The second is *more* misleading than a long version, not less. Cutting the count, the scope, or
the unmatched half of a comparison is not brevity; it is the defect this rule exists to prevent,
not cause. Where terseness and completeness conflict, completeness wins.

## Why it improves the work, not just the reading

Padding is where scope quietly slips. A verbose report has room for a claim that was true of one
thing to sit next to a claim about another, and for the reader to merge them. In the incident that
prompted this rule, a correctly-scoped statement ("the reformat changed no value") was surrounded
by enough prose that it read as an unscoped one ("the file matches the reference"). The shorter
version could not have been misread, because the two sentences would have been adjacent and
obviously different.

---

*Earned from:* a user instruction, after a session where padding around a comparison result let a
scoped claim read as an unscoped one.
