---
name: rotate-session
description: Refresh (rotate) the CURRENT Claude session in place — hand off, wrap, then replace this session with a fresh same-name successor that has an empty context window. Works for a host tmux session and for a container session whose tmux lives on the host. Only rotates the session you are inside, and only in a repo that has opted in with a committed .claude/rotate.conf.
argument-hint: "What should the next (fresh) session focus on?"
disable-model-invocation: true
---

# rotate-session — refresh the current session in place

Rotate the **current** Claude session: preserve continuity to disk, then replace this
session with a fresh same-name successor (empty context window). Continuity is
reconstructed from committed, pushed files — not from the discarded conversation.

The guard is **self-rotation only** — the sole session this skill can ever end is the one it
is running inside. A typo or a bad config cannot reach another repo's session.

## Two topologies — the skill detects which, you do not configure it

|  | **MODE=tmux** (host session) | **MODE=container** (container session) |
|---|---|---|
| what runs `claude` | the tmux pane, on the host | `docker exec` from a tmux pane **on the host** |
| identity of "this session" | the tmux session name | the `--remote-control` name on our own claude process |
| ending it | `tmux kill-session` | signal our own claude pid; the `docker exec` returns |
| who starts the successor | **we do** — `systemd-run --user`, scheduled before the kill | **the host restart loop** — already running, relaunches ~3s later |
| what could silently fail | the successor is never scheduled | the successor comes up **resuming this same conversation** |

**Inside a container there is no tmux, no systemd and no docker socket.** The host is
unreachable except through the shared bind mount. That is why the tmux-only version of this
skill refused outright from a container session, and why the container path is built
differently rather than by relaxing the guard.

### The container problem, and the actual fix

The host loop is (see the `launch-session` skill):

```sh
while true; do docker exec -it -w <workdir> <container> \
  claude --continue --model <model> --remote-control '<rc>' ...; sleep 3; done
```

So a container session **already has a successor** — ending `claude` brings one back in ~3s.
What it does **not** have is a *fresh* one: `--continue` is baked into that command line, on
the host, where we cannot edit it. Left alone, a rotation ends the session, the loop resumes
**this same saturated conversation**, and the rotation has accomplished nothing while
appearing to work.

`--continue` resumes **the most recent conversation for that project directory**. So the fix
is to control what there is to continue:

1. **Seed** a fresh, near-empty conversation for the workdir (`claude -p <bootstrap>`), run
   with this session's `CLAUDE_CODE_*` variables stripped so it is genuinely a new one.
2. **Archive** every other conversation out of `~/.claude/projects/<slug>/` (moved, never
   deleted — a rotation that goes wrong must be recoverable).
3. **Verify** exactly one conversation remains and it is the seed.
4. **Only then** end our own claude process.

**Leaving it zero conversations is worse than leaving it the old one.** Interactive
`claude --continue` with nothing to continue prints `No conversation found to continue` and
**exits** — and the 3-second restart loop then spins forever. That is why step 3 is a hard
gate and why the seed is created *before* anything is moved.

The bootstrap prompt lands **inside the seed**, so the successor opens with it already in
history — it does not need to be passed on a command line we do not control.

## Activation (why it may refuse)

A repo rotates **only** if it contains a committed `.claude/rotate.conf` whose `SESSION`
equals the live session name. Absent that file, the skill hard-refuses.

`.claude/rotate.conf` fields:

```sh
SESSION=ebiz                 # REQUIRED: tmux session name (host) or --remote-control name (container)
SUCCESSOR=host-restart-loop  # REQUIRED IN CONTAINER MODE — see below
MODEL=opus                   # tmux mode: --model for the successor
EFFORT=high                  # tmux mode: --effort for the successor
RC_NAME=Factory-$(hostname)  # tmux mode: --remote-control name (default: SESSION)
PERMISSION_MODE=acceptEdits  # tmux mode: --permission-mode for the successor
DELAY=60                     # tmux mode: seconds until the successor launches (default 60)
SEED_MODEL=haiku             # container mode: model used to seed the fresh conversation
```

**`SUCCESSOR=host-restart-loop` is an assertion the operator makes, not a check the skill can
run.** A container session cannot see the host, so it cannot confirm a restart loop exists —
and ending a session that has none kills it permanently. Verify it on the **host**, once:

```sh
tmux list-panes -a -F '#{session_name} :: #{pane_start_command}' | grep '<SESSION>'
```

The pane command must be a `while true; do docker exec ... claude ...; sleep 3; done` loop.
If it is a bare `docker exec`, **do not assert it** — relaunch through `claude-session.sh`
first. Until the line is present, preflight refuses and says exactly this.

## Steps (run in this order)

Run from **inside** the session you want to refresh, from its workdir.

1. **Preflight — refuse early if not permitted.** `assets/rotate.sh --preflight`. It resolves
   the mode; verifies `.claude/rotate.conf` is present and its `SESSION` is the current session
   (the self-target guard); checks `systemd-run` (tmux mode) or the successor assertion, the
   `claude` CLI and the transcript store (container mode); and warns if the repo is not clean
   and pushed. On `PREFLIGHT FAIL`, print the reason and STOP — change nothing.
   `assets/rotate.sh --dry-run <sha>` prints the whole plan without touching anything.
2. **Handoff note (inlined).** Write the deliberate `## Next Session` note (from the focus
   argument) into the repo's committed handoff file (CONTEXT.md / HANDOFF.md / TODO.md) and
   commit + push just that file. This is the `/handoff` action performed **inline**: `handoff`
   is a user-invoked skill and, per this repo's `docs/invocation.md`, a user-invoked skill
   (this one) can never invoke another user-invoked skill — so do the note yourself rather
   than calling `/handoff`.
3. **`/wrap`** — invoke the `/wrap` skill (it is model-invoked, so this user-invoked skill may
   call it). It summarises, updates project logs, and commits **and pushes** everything.
   Capture the resulting commit SHA (the successor verifies it).
4. **Rotate** — run `assets/rotate.sh <pushed_sha>`.
5. **Report** — the session drops now and reappears fresh under the same name (~`DELAY`s in
   tmux mode, ~3s in container mode). The successor reads the committed handoff and confirms
   the predecessor SHA before acting.

**The clean, pushed repo is a hard gate in the script, not a habit.** `rotate.sh` refuses to
rotate with uncommitted changes or unpushed commits — the conversation is about to be
discarded, so the repo must already hold everything. This is deliberately checked by the
script rather than left to whoever is driving it.

## Recovery — what to do if the successor does not appear

Nothing is deleted. In container mode the archive directory holds the old conversations and a
`rotate.log` with the exact restore command:

```sh
mv ~/.claude/rotate-archive/<slug>/<stamp>/*.jsonl ~/.claude/projects/<slug>/
```

Then relaunch on the **host** (`claude-session.sh start <name>`) and `--resume <uuid>` the
conversation you want. Pick it by size: a real session is megabytes.

## Assets

- `assets/rotate-env.sh` — mode detection, identity, and the self-target guard
  (`rotate_assert_self`, `rotate_kill`). Source first.
- `assets/rotate.sh` — `--preflight` / `--dry-run` checks; else the irreversible half.
- `assets/rotate-launch.sh` — tmux mode: launch a same-name successor on a real TTY
  (`tmux pipe-pane` logging).
- `assets/rotate-status.sh` — read-only: is the session on a TTY and relay-connected?
- `assets/selftest-guard.sh` — proves the guard accepts only the current session; run it anywhere.

## Notes

- Adding this skill is a global `~/.claude` change → file the FYI issue your project requires.
- v1 is manual only. Auto-firing at a context ceiling (~30%) is a separate, later change.
- The sandbox `sbx-*` scripts are NOT modified — they remain the isolated dev harness.
- **A cleaner container fix exists and is not built here:** the host launcher could honour a
  rotate-request file dropped on the shared mount and relaunch without `--continue`. That is a
  change to `claude-session.sh`, which a container session cannot reach. The seed-and-archive
  route above is the version that needs **no host change**.
