# Structure a new project's CLAUDE.md as System / Rules / Brief

**Task type:** agent workflow — initialising a new project's `CLAUDE.md`.
**Related:** [`prompt-and-store-config`](prompt-and-store-config.md) — both are about getting a
project's persistent context right before work starts, not patched in after.

---

## The rule

**When starting a new project's `CLAUDE.md`, use three sections, in this order:**

```markdown
## System
You are <role — the persona/expertise this project needs, not a generic assistant>.

## Your rules
- <constraint>
- <constraint>
- ...

## Project brief
<what the project is, what it's for, and any context needed to work on it>
```

## Why this order, and why these three

**System first** — the role sets how everything after it should be read. "You are a data
pipeline engineer" and "You are drafting marketing copy" make the same rule mean different
things.

**Rules second, as constraints, not as a task list.** This section is boundaries — what must
never happen, what must always be true, what's off-limits — not a to-do list for the current
piece of work. Task-specific instructions belong in the conversation, not in a file that persists
across every future session.

**Brief last.** Once the role and the constraints are set, the brief only has to convey what the
project *is* — the reader already knows how to act on it.

## Why not one undifferentiated block

A `CLAUDE.md` that mixes role, constraints, and background in prose makes each one harder to
find and easier to silently drop during an edit. Three named sections mean a new constraint gets
added to "Your rules" without disturbing the brief, and the brief gets extended without touching
the constraints — instead of every edit risking the other two.

---

*Earned from:* proactive practice, no incident yet — added on user instruction rather than
extracted from a failure, consistent with
[`record-thinking-before-complex-work`](record-thinking-before-complex-work.md).
