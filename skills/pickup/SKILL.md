---
name: pickup
description: Pick up where the last session left off by reading the open handoffs. Use at the start of a session before the first task, or when the user says continue, pick up, or "what's next".
---

Pick up the work from the open **handoffs**, the notes `/handoff` leaves for the next session. Treat each one as a claim about the past, and check it against the present before acting on it.

## 1. Find the open handoffs

A handoff is **open** until a later handoff names it in its `**Supersedes:**` line. Usually exactly one is open. Parallel sessions can leave more.

Look in this order, and stop at the first place that has handoffs:

1. `<repo root>/handoffs/`: list every file, then collect the filenames named in all the `**Supersedes:**` lines. The open handoffs are the files that are never named.
2. A `latest-handoff` entry in this directory's memory index. It names an absolute path, usually in another repo's `handoffs/`. Apply rule 1 to that folder.
3. A root `HANDOFF.md`, the older convention, which counts as open.

**Done when:** you hold the list of open handoffs. If there are several, say so: they are parallel threads. If there are none, tell the user there is no handoff and ask what to work on.

## 2. Read them, and the material they point to

Read every open handoff in full. Then open whatever each one tells you to read first: the files, issues and URLs in its "read these" or "state now" sections. A handoff links out on purpose, so the detail lives in those targets.

**Done when:** you have read every pointer marked as must-read.

## 3. Check them against the present

Time has passed since the handoff was written, and other sessions may have moved things. For every item under "State now" and "Next session focus", check the thing itself:

- open, closed, or claimed issues (`gh issue view`)
- commits since the handoff (`git log` after the handoff's own commit)
- files it says exist, or haven't been committed

Mark each item **still true**, **changed** (say what changed), or **uncheckable** (say why).

**Done when:** every state item carries one of those three marks.

## 4. Brief the user

Say what's next, as each open handoff's focus, adjusted for anything that changed. List the standing constraints the next agent must keep, and the items that changed. Keep it short. If several handoffs are open, brief each thread under its own heading. The next `/handoff` merges them.

If the user's opening message already named a task, start on it, and keep the constraints in force. Otherwise, ask the user to confirm the next step, as one question with your recommendation.
