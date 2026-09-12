# PRD — new-repo-session

**Status:** agreed
**Owner:** the operator of the estate that runs container-backed Claude Code sessions.

*Filed inside the skill directory rather than `docs/prd/` because this repo has no `docs/`
tree and skills here are self-contained. Same document, different shelf.*

## The user and the problem

**The operator, standing up a Claude Code session for a repo that has never had one.**

What they do today instead: clone, hand-write a compose file by copying a neighbouring
project's, add a `sessions.conf` row, run the launcher, and then discover — one symptom at a
time, over several restart cycles — what was missing. The launcher reports **started** and the
session is unusable, because *started* and *works* are different conditions and only the first
one is measured.

Observed 2026-09-12 on a single repo, in this order: a `.claude-session` with the wrong key
name, an rc name already held by a live session, a workdir mounted nowhere, a container home
directory created by docker and therefore owned by **root** while the container runs as uid
1000, a missing credential, and finally a missing `.claude.json` — each found only after the
previous one was fixed and the session restarted. **Six serial round trips for one repo.**

Every one of them is checkable before launch. None of them was checked.

## What it must do

- Given a repo, report **every** blocker between its current state and a working session, in
  one pass — not the first one it hits.
- Distinguish **blocker** (the session cannot work) from **warning** (it will work, something
  is unusual). Exit non-zero only for blockers, so it can gate a launch.
- Prove writability and mounts **by executing inside the container**, never by inferring from
  host-side ownership bits. The estate's standing lesson is that a plausible-looking host-side
  check is exactly how this class of failure stays hidden.
- Be safe to run against a live session: read-only, no restarts, no container recreation.
- Say what to DO about each finding, not only that it is wrong.
- Take the repo as an argument. No machine-specific paths written into the tool.

## What it will NOT do

- **Not fix anything.** No chown, no credential copy, no compose edits, no file creation. The
  credential step in particular is the operator's decision and is refused by the permission
  layer in any case; a tool that quietly did it would be routing around that.
- **Not launch the session.** `launch-session` and the estate's own launcher already own that,
  including the memory ceiling. This runs before them and hands back a verdict.
- **Not scaffold a compose stack.** Choosing an image, a memory limit, a network and a port is
  judgement with a security boundary attached; the skill documents the decisions, the tool does
  not make them.
- **Not validate the repo's contents** — no build, no tests, no lint. It checks the session
  plumbing only.
- **Not manage credentials, rotate them, or report their contents.** It answers *present or
  absent* and nothing further.

## Done

**A person who did not build it can point it at a repo with no session and, from that one
run, know every step still required — with no restart cycle used to discover any of them.**

Concretely: run against a repo mid-setup, and each of the six failures listed above is named
in the first pass, each labelled blocker or warning, each with the next action. Run it against
a working session and it exits 0.

**Stop condition:** this is written once and reviewed once. Round two must name what would
make me abandon the tool rather than revise it — the likely candidate being that the checks
turn out to be estate-specific enough that `claude-session.sh` should absorb them directly, in
which case the skill keeps its prose and loses its script.

## Open questions

- Whether these checks ultimately belong in the estate's `claude-session.sh` as a launch
  precondition rather than in a separate tool. Tracked on the host Kanban under the
  new-container auth item; it does not block writing this.
