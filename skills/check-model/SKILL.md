---
name: check-model
description: Report the Claude model active this session, and recommend a different tier when it doesn't match the task's complexity. Use when the user types /check-model, asks which model is running or active, or asks whether to switch models / which model fits the current task.
license: MIT
---

# Check Model

**The live model is fixed for the whole session.** Switching a tier (via `/sonnet`, `/opus`,
`/fable`, or `/model`) changes the *default* for the *next* session, not this one — say so
plainly whenever you recommend a switch.

## 1. Identify the current model

The system prompt for this session states the exact model and ID (e.g. "You are powered by
the model named Sonnet 5..."). Report that verbatim — it is the live, authoritative answer.

If no such line is present, fall back to the `model` / `effortLevel` keys in
`~/.claude/settings.json`, and flag the answer as the *configured default*, not a confirmed
live read.

## 2. Classify the task

Judge the task actually in front of you (or the one the user names) against a tier:

- **Light → Haiku** — search/exploration, formatting, lint, log parsing, background
  subagent grunt work, web search.
- **Standard → Sonnet** — day-to-day coding, refactors, SQL/pipeline scripts, doc drafting,
  routine feature work.
- **Heavy → Opus** (or **Opusplan** for up-front architectural planning) — multi-system
  design, gnarly debugging, edge-case-heavy algorithm work.

A project's or user's own `CLAUDE.md` may declare its own model-routing rules — check for
one first and use it instead of the table above when it exists.

## 3. Recommend

- Tiers match → say so; no action needed.
- Tiers don't match → name the tier that fits and how to reach it: the matching skill if
  loaded (`/sonnet`, `/opus`, `/fable`), else `/model`. Recommend only — never switch on the
  user's behalf. The change only takes effect next session, and a mismatch can be
  deliberate (a stronger model kept on through one small step of a bigger job).
