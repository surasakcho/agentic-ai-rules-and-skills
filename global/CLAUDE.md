# Global rules — every machine, every project

**This file is the SOURCE. It is copied verbatim into a machine's `~/.claude/CLAUDE.md` by the
[`refresh-rules`](../skills/refresh-rules/) skill, which then appends a generated machine block
below it.** Edit it here; never edit the copy on a machine, because the next refresh overwrites it.

**Everything here is true on every machine.** Anything naming a host, a path, a container, a
credential or an employer belongs in that machine's own block or in a private repo — this file is
public.

---

## How to reply

> **A little context, then ASD-STE100 Simplified Technical English, in the ubiquitous language
> from `CONTEXT.md`. Fragments over sentences. Lead with the verdict.**

Copy identifiers, error text and numbers exactly — `--flag`, a sha, a path, a count. **Precision
wins over plainness**; when they pull apart the sentence gets longer, never vaguer.
→ [`write-in-fragments-not-sentences`](../rules/how-we-work/write-in-fragments-not-sentences.md)

## Before you assert it

> **Never assume. Check first.** The discriminator: can you name the check you ran?

When the check is genuinely unavailable, say **UNVERIFIED and why** — never resolve it by deciding
the thing is probably fine. Binds claims someone will act on, not ordinary reasoning out loud.
→ [`a-remembered-claim-is-not-a-checked-one`](../rules/how-we-work/a-remembered-claim-is-not-a-checked-one.md)

## When something blocks

> **Work everything that is not blocked, and re-check the rest by a check you can name.**

A remembered blocked-list is always longer than the real one. A status report is not a gate: a
decision only the owner can make is theirs; the session's own restart is not.
→ [`a-blocked-list-is-a-fact-about-a-moment`](../rules/how-we-work/a-blocked-list-is-a-fact-about-a-moment.md)

## Delegation

> **Match effort to failure mode: expensive reasoning for silent failures, cheap execution for
> loud ones.**

Delegate execution against a known plan. Keep novel algorithmic work, architecture spanning
modules, and **any edit to an existing test's assertions or tolerances**. Agent output is evidence
to check, never a result to relay.
→ [`delegation-and-supervision`](../rules/how-we-work/delegation-and-supervision.md)

## Assets and inputs

> **Find it free, then generate it, then ask.**

"Free" on a page is a price, not a licence, and the licence is read against the actual use. A
recognisable person needs a release; a trademark survives any file licence.
→ [`find-free-then-generate-then-ask`](../rules/how-we-work/find-free-then-generate-then-ask.md)

## Before you destroy anything

> **Before any write that destroys existing content, look at what is there.**

→ [`ask-before-overwriting-uncommitted-work`](../rules/coding/ask-before-overwriting-uncommitted-work.md)
· [`nothing-leaves-git-without-permission`](../rules/how-we-work/nothing-leaves-git-without-permission.md)

## Text encoding

> **Make encoding explicit as the code is written.** Windows Python uses the locale codec
> (cp1252, or cp874 on a Thai-locale machine); Linux and macOS use UTF-8.

`open(...)` takes `encoding="utf-8"` unless the mode is binary. This one is machine-dependent in
its *symptom* and machine-independent in its *fix*, so it lives here rather than in a machine block.
→ [`text-encoding`](../rules/data-engineering/text-encoding.md)

---

## What is NOT in this file

- **Anything machine-specific** — it is generated into the machine block below this, by
  `refresh-rules`, from state rather than from anyone's memory.
- **Anything project-specific** — that belongs in the project's own `CLAUDE.md`, adopted by
  [`retrieve-lessons`](../skills/retrieve-lessons/).
- **Any secret, host name, container name or private path.** This file is public.
