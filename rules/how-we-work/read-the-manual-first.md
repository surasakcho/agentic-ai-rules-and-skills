# Search for the existing manual before inventing a new way

**Task type:** agent workflow — any task that resembles something the project has done before.
**Related:** [`research-and-qa-logs`](../research/research-and-qa-logs.md) is why the manual
exists; this is the obligation to read it.

---

## The rule

**If the task looks like something this project has done before, find the written procedure
first. Read it, follow it, and only then consider a different route — saying explicitly why the
documented one does not apply.**

The repo is the manual. Before proposing an approach, grep for it: research logs, defect
write-ups, Q&A logs, lessons files, the board, and the docstrings of any script that already
touches the same system.

**A procedure that exists and is ignored is worse than no procedure**, because the documented one
usually encodes failures that were paid for once already.

## What the existing log contains that a fresh attempt will not

| | Cost of not reading it |
|---|---|
| **The route already rejected, and why** | You re-spend the original cost of discovering it fails |
| **The blocker three steps in** | Invisible from outside; it decides whether the approach is viable at all |
| **Which steps are the user's, not yours** | Logins, approvals, anything expressing their identity or opinion |
| **Mechanical quirks** | The click that silently no-ops, the field that must be set first, the id that is stable versus the one that is only a display position |

## A different route is allowed; an uninformed one is not

If the documented method is slower or blocked, say so *against the log* and propose the
alternative on the record. What is not allowed is discovering a new path and acting on it while a
written procedure for the same task sits unread in the repo.

## The incident

Asked to fetch a missing dataset, I searched the web, found a second download portal for the same
agency, and clicked download on it.

Meanwhile the repo held a research log for exactly this task, documenting:

- the agreed method and why it was chosen
- a security control that blocks scripted access, and the explicit decision never to evade it
- a **per-item human gate** that only the user can pass
- the file-naming and manifest conventions the download must land in
- and — the detail that then blocked me — that the specific page I needed **had never been
  confirmed to work**

I read it only after the user asked whether I still remembered how we did this. The user's
reaction to the unsanctioned download was not enthusiasm.

## The cheap habit that prevents it

Before the first tool call on a task that smells familiar, one search across the repo's prose for
the system you are about to touch. It costs seconds. In this case it would have replaced a wrong
portal, a tripped security control, and an annoyed user with a five-step checklist that already
existed.

---

*Earned from:* proposing and acting on a new download route while the project's own written
procedure for that exact task — including the gate that would block me — sat unread in the repo.
