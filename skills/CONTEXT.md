# Matt Pocock Skills

A collection of agent skills (slash commands and behaviors) loaded by Claude Code. Skills are organized into buckets and consumed by per-repo configuration emitted by `/setup-matt-pocock-skills`.

## Language

**Issue tracker**:
The tool that hosts a repo's issues — GitHub Issues, Linear, a local `.scratch/` markdown convention, or similar. Skills like `to-tickets`, `to-spec`, `triage`, and `qa` read from and write to it.
_Avoid_: backlog manager, backlog backend, issue host

**Issue**:
A single tracked unit of work inside an **Issue tracker** — a bug, task, PRD, or slice produced by `to-tickets`.
_Avoid_: ticket (use only when quoting external systems that call them tickets)

**Triage role**:
A canonical state-machine label applied to an **Issue** during triage (e.g. `needs-triage`, `ready-for-afk`). Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

## Relationships

- An **Issue tracker** holds many **Issues**
- An **Issue** carries one **Triage role** at a time

## Flagged ambiguities

- ⚠️ **UNRESOLVED, 2026-09-13: "ticket" is both forbidden and shipped.** The **Issue** entry above
  says *avoid: ticket*, and names `to-tickets` as the skill that produces one. The skill was renamed
  from `to-issues` on the operator's own wording for the chain — *grill-with-docs (or wayfinder) →
  to-spec → to-tickets → implement* — so the vocabulary decision has been made for the **skill
  names** and not for the **domain term**. Upstream carries the same contradiction: it ships
  `to-tickets` under a domain model that avoids the word.

  Left as an ambiguity rather than settled here, because a ubiquitous language reaches further than
  two filenames and nothing in the operator's message touched it. **The two coherent answers are
  "ticket is the artifact and the entry is stale" and "the skill name is a verb, the artifact is
  still an Issue" — and only the operator can pick.**

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
