---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.

---

*Adopted from upstream at `3cca18b`, 2026-09-13, as the invoker wayfinder's Research ticket type
calls by name. One addition on adoption, recorded in [`UPSTREAM.md`](../UPSTREAM.md):* this corpus
holds three rules that bind the same work and say more than the three steps above —
[`external-sources-only-are-primary`](../../rules/research/external-sources-only-are-primary.md)
(a repo file is a lead, not evidence, and so is an owner describing their own system),
[`research-and-qa-logs`](../../rules/research/research-and-qa-logs.md) (the log records sources
**rejected** and negative results, access status verified from this machine, and the licence of
every source at the moment it is evaluated), and
[`a-faithful-relay-loses-the-clause-that-matters`](../../rules/how-we-work/a-faithful-relay-loses-the-clause-that-matters.md)
(read the primary, not a summary of it). **Those bind the findings file; this skill only spawns the
agent that writes it.**
