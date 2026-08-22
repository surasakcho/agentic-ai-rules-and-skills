---
name: launch-session
description: Start a Claude Code session for a repo — in its declared container where one exists, otherwise on the host — as a detached tmux session with remote control enabled. Reads a committed .claude-session file so the choice is made once per repo rather than re-decided each time. Use when the user says "launch session", "start a claude session", "open a tmux claude session", or similar.
---

# launch-session

## Why this is not just a tmux command

A session started on the **host** can read everything the operator can: SSH private
keys, every secrets directory, every repo, with no memory limit. A session started
in a **project container** sees only what that project mounts.

On a machine where containers exist, quietly defaulting to the host hands a session
capabilities the containers were deliberately built to withhold — and nothing warns
you, because both look identical once attached. **So the target is a decision, it is
recorded in the repo, and it is never guessed.**

## 1. Resolve the target — first match wins, do not skip ahead

**a. The repo declares it.** If `<repo>/.claude-session` exists, use it. No prompting.
See the format below.

**b. The host has a managed launcher and knows this repo.** If
`~/projects/zkyhax-host-config/bin/claude-session.sh` exists, run
`claude-session.sh list` and look for a row whose workdir matches this repo. If there
is one, launch with `claude-session.sh start <name>` and stop — that path brings the
memory guard and the container's own mounts, which this skill must not reimplement.

**c. Containers exist but this repo is undeclared.** If `docker info` succeeds AND
`docker image ls` shows a `factory-*` or project image, **ASK the user** before
launching. Give them the real trade-off, not a bare choice:

> This machine runs project containers. A **host** session can read `~/.ssh`, all of
> `~/secrets/` and every repo, with no memory limit. A **container** session sees only
> that project's mounts. Which do you want — and shall I record it in the repo?

**d. No containers.** Host tmux. This is the normal case on a Pi or a laptop, and
needs no prompt.

## 2. Find the repo directory — do not hardcode

Check `~/repos/<repo>` then `~/projects/<repo>`; use whichever exists. Machines differ
(`~/repos` on the Pi, `~/projects` on zkyhax-server) and a hardcoded path fails on a
missing directory rather than falling back.

## 3. Launch

Refuse to overwrite a live session: if `tmux has-session -t <tmux>` exits 0, warn and
get explicit confirmation first.

**Host:**
```bash
tmux new-session -d -s "<tmux>" -c "<repo-dir>" \
  "while true; do claude --continue --model <model> --remote-control '<rc>' [--permission-mode <perm>]; \
   echo '[claude exited -- resuming in 3s]'; sleep 3; done"
```

**Container:**
```bash
tmux new-session -d -s "<tmux>" \
  "while true; do docker exec -it -w '<workdir>' '<container>' \
   claude --continue --model <model> --remote-control '<rc>' [--permission-mode <perm>]; \
   echo '[claude exited -- resuming in 3s]'; sleep 3; done"
```
If the shell predates the `docker` group, wrap the `docker exec` in `sg docker -c "..."`.

Three details, each of which has cost a real session:

- **`--continue`** — a restart must resume the same conversation, not a blank one. It
  exits 0 with no prior conversation, so there is no first-run special case. Without it
  a crash silently loses the work.
- **`--remote-control '<rc>'`** — without it Claude Code still registers, under an
  auto-generated name like `witty-hare`. The session then runs fine and is unfindable
  from a phone, with no error anywhere.
- **tmux on the HOST, never inside the container** — a tmux server inside a container
  dies when the container is recreated, which is routine.

## 4. Record the choice in the repo

If `<repo>/.claude-session` did not exist, write it now and tell the user it is
uncommitted. The point is that the next launch — on any machine, by anyone — does not
re-decide, and that the decision is reviewable in a diff.

```ini
# Where a Claude Code session for this repo should run.
# Read by the launch-session skill. Committed on purpose.
target=container          # container | host
container=yf-agent        # required when target=container
workdir=/app/youtube-factory   # path INSIDE the container
model=opus
rc=youtube-srv            # remote-control name; keep stable, you search by it
tmux=youtube-srv
permission_mode=          # optional: acceptEdits, etc.
```

For `target=host`, omit `container`/`workdir` and set `workdir` to the repo path, or
leave it unset to use the repo directory.

## 5. Report back

Attach command · remote-control name · repo path · model · **and whether it is running
on the host or in a container**. That last line is the one the user cannot see from the
tmux pane, and it is the one that determines what the session can reach.
