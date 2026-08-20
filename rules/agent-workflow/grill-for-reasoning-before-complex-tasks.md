# For a complex task, grill for reasoning before starting

**Task type:** agent workflow — before beginning a complex task, ahead of any planning or
implementation.
**Related:** [`record-thinking-before-complex-work`](record-thinking-before-complex-work.md) —
that rule verifies your own plan; this one verifies the request the plan is built on.

---

## The rule

**Before starting a complex task, ask the user to explain their reasoning — why this approach,
why this scope, what it needs to satisfy — rather than accepting the request at face value and
proceeding straight to a plan.**

"Complex" here means the same thing it means elsewhere in this repo: more than one plausible
approach, a decision that would be expensive to unwind, or a request whose stated form might not
match its actual goal. A well-scoped, single-interpretation task doesn't need this.

## Why grill instead of just asking one clarifying question

A single clarifying question resolves one ambiguity and leaves the rest of the request's
reasoning untouched. Grilling — asking several pointed questions, including ones that challenge
the premise — surfaces the assumptions the user didn't think to state, because those are usually
the ones that matter most: the constraint they forgot to mention, the alternative they already
rejected and why, the part of the request that's a means rather than the actual end.

Accepting the request as given and proceeding to build a plan around it skips exactly this step
— the plan then gets verified against the *stated* request, not the *actual* one, and a wrong
premise survives every check built on top of it.

## What this looks like

- Ask why this approach over the obvious alternatives, not just what the approach is.
- Ask what happens if the request's literal scope is wrong — is the user asking for the fix, or
  for the outcome the fix is meant to produce?
- Push back on a request that seems to solve the wrong problem, rather than implementing it as
  stated and hoping the mismatch surfaces later.

This is not a formality to get through before "real" work starts — the questions themselves are
the work, for a task where the biggest risk is building the right answer to the wrong question.

---

*Earned from:* proactive practice, no incident yet — added on user instruction rather than
extracted from a failure, consistent with
[`record-thinking-before-complex-work`](record-thinking-before-complex-work.md).
