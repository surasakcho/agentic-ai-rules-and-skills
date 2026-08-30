# Phrase a narrow rule as a prohibition, not a prescription

**Task type:** agent workflow — writing or extracting a new rule for this repo.
**Related:** [`record-thinking-before-complex-work`](record-thinking-before-complex-work.md) —
another rule-about-rules added on direct instruction rather than a named incident.

---

## The rule

**When a rule is very specific — scoped to one situation, one kind of mistake, one narrow
context — state it as a prohibition ("never do X") rather than a prescription ("always do Y").
Leave the fix open.**

## Why the direction matters at narrow scope

A broad rule can safely prescribe, because the positive instruction *is* the generalisation —
"verify every reported number against its source" holds regardless of what the number is. A
narrow rule doesn't have that luxury: it was extracted from one specific incident, and a
prescription written at that scope tends to just describe the fix that happened to work that one
time.

A prohibition ages better than a prescription at narrow scope, for two reasons:

- **A ban is falsifiable in a way a prescribed procedure isn't.** "Never do X" is checked by
  asking "did X happen?" — binary. "Always do Y" is checked by asking "was Y done well enough?" —
  which quietly invites judgment calls that dilute the rule over time.
- **A ban doesn't overfit to today's fix.** The situation that produced the rule might have three
  valid fixes; prescribing one forecloses the other two for every future case, even ones where
  they'd be the better choice. Prohibiting the failure mode leaves the actual remedy to context.

## What this doesn't change

This is about phrasing at narrow scope, not a blanket preference for negative rules everywhere.
Broad, procedural rules in this repo are correctly prescriptive (e.g. "verify conversions against
the original") — prescribing there *is* the generalisation, not a narrowing of it. Apply this
when a rule is being written specifically enough that the alternative would be enumerating one
situation.

---

*Earned from:* proactive practice, no incident yet — added on user instruction rather than
extracted from a failure, consistent with
[`record-thinking-before-complex-work`](record-thinking-before-complex-work.md).
