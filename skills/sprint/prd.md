# Writing the PRD

**Read the rule first:**
[`write-the-prd-before-the-code`](https://github.com/surasakcho/agentic-ai-rules-and-skills/blob/3901f3a/rules/coding/write-the-prd-before-the-code.md).
This file is the local procedure, not a replacement for it.

## Before you write: grill the requester

**A PRD built on an unexamined request verifies the stated ask, never the actual one.** Ask, one at
a time, and stop when the answers stop changing anything:

- Why this approach rather than the obvious alternative?
- Is the request the fix, or the outcome the fix is meant to produce?
- What would make this NOT worth building?
- What did you already consider and reject, and why?

**Push back on a request that solves the wrong problem** instead of building it and hoping the
mismatch surfaces later.

## The file

`docs/prd/<slug>.md`. **Scope it to the work — a small tool's PRD is a paragraph and a bullet list.
Length is not the deliverable.**

```markdown
# PRD — <what this is>

**Status:** draft | agreed | superseded by <link>
**Owner:** <who decides it is done>

## The user and the problem
Who has it. What they do today instead. *If you cannot name a person or a role, stop.*

## What it must do
Behaviour, in terms someone who will not build it can check.

## What it will NOT do
<!-- MANDATORY. A PRD with no exclusions has not been thought about. -->

## Done
A condition someone who did not build it could evaluate. Not "it works".

## Open questions
Links to tracked decisions only. <!-- Six unresolved questions here = a meeting agenda, not a PRD -->
```

## Four hard checks before it is agreed

1. **The out-of-scope list is not empty.** It is the half that survives contact with a deadline and
   the half nobody writes.
2. **"Done" is checkable by a stranger.**
3. **It does not say HOW.** The moment it names functions, tables or endpoints it has become the
   implementation in prose — slower to write, impossible to run, and now a second artifact to keep
   in agreement with the code.
4. **Open questions are links, not threads.** Unanswered questions go to the tracker.

## Rounds

**One round. Then one review.** Round two opens only by writing down **what would make you abandon
this document rather than revise it**. If no outcome of the review would license writing code, the
document is not deciding anything and should be abandoned now.

## After code exists

**If the requirement changes, change the PRD, and say so in the commit.** A silently amended
requirement is how the implementation quietly becomes its own specification.
