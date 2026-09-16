---
name: pickup
description: Pick up where the last session left off by reading the newest handoff. Use at the start of a session before the first task, or when the user says continue, pick up, or "what's next".
---

Pick up the work from the newest **handoff**, the note `/handoff` leaves for the next session. Treat the handoff as a claim about the past, and check it against the present before acting on it.

## 1. Find the newest handoff

Look in this order and take the first hit:

1. `<repo root>/handoffs/`: the newest file. Filenames are `YYYY-MM-DD-HHMM.md` (older ones may be `YYYY-MM-DD-am`/`-pm`), so they sort by name.
2. A `latest-handoff` entry in this directory's memory index. It names an absolute path, usually in another repo.
3. A root `HANDOFF.md`, the older convention.

**Done when:** you hold one path. If nothing turns up, tell the user there is no handoff and ask what to work on.

## 2. Read it, and the material it points to

Read the whole handoff. Then open whatever it tells you to read first: the files, issues and URLs in its "read these" or "state now" sections. A handoff links out on purpose, so the detail lives in those targets.

**Done when:** you have read every pointer marked as must-read.

## 3. Check it against the present

Time has passed since the handoff was written, and other sessions may have moved things. For every item under "State now" and "Next session focus", check the thing itself:

- open, closed, or claimed issues (`gh issue view`)
- commits since the handoff (`git log` after the handoff's own commit)
- files it says exist, or haven't been committed

Mark each item **still true**, **changed** (say what changed), or **uncheckable** (say why).

**Done when:** every state item carries one of those three marks.

## 4. Brief the user

Say what's next, as the handoff's focus, adjusted for anything that changed. List the standing constraints the next agent must keep, and the items that changed. Keep it short.

If the user's opening message already named a task, start on it, and keep the constraints in force. Otherwise, ask the user to confirm the next step, as one question with your recommendation.
