---
name: new-repo-session
description: Stand up a Claude Code session for a repo that has never had one — clone location, container vs host, the stack, the declaration, authentication, shared rules — and verify it WORKS rather than that it started. Use when a repo is new to this machine, when "launch session" fails on a repo with no session yet, or when a session starts and then sits on a prompt nobody expected.
---

# new-repo-session — from a repo URL to a session that actually works

**[`launch-session`](../launch-session/SKILL.md) starts a session a repo has already declared.
This is the step before it, and it exists because that step has no owner.** When it is skipped,
the defects are found one restart at a time.

## The failure this is built from

One repo, 2026-09-12. Six defects, discovered **serially** — each invisible until the previous
one was fixed, each costing a restart:

| # | defect | how it presented |
|---|---|---|
| 1 | `.claude-session` used the key `rc-name=` where the reader looks for `rc=` | nothing. The key is ignored silently |
| 2 | the rc name it declared belonged to a **live** session | would have collided at launch |
| 3 | `workdir=` pointed at a path mounted nowhere | nothing, until the session starts in the wrong place |
| 4 | docker created the home mount, so `~/.claude` inside was **root-owned** while the container runs as uid 1000 | session parks on the login picker forever, nothing in any log |
| 5 | no `.credentials.json` | login picker |
| 6 | no `.claude.json`, so no `oauthAccount` | **login picker again — after the credential was in place** |

**#6 is the one worth remembering.** The credential file alone does not authenticate a
container. The picker is driven by `oauthAccount` / `hasCompletedOnboarding` in `.claude.json`;
the token lives in `.credentials.json`. A fresh home needs **both**, and only one of them is
the obvious half — so "I supplied the credential" produces a session that looks exactly as
broken as it did before.

**The through-line: the launcher reports *started*, and nobody measures *works*.** Every one of
those six is checkable before launch. None of them was checked.

## Run the preflight first — all blockers in one pass

```sh
assets/session-preflight.sh <repo-dir> [--sessions-conf <file>]
```

Exit 0 launchable · 1 blockers present · 2 cannot check. Read-only: it never fixes, launches,
or recreates anything.

It reports **every** blocker in a single run rather than stopping at the first, because serial
discovery is the failure it was written for. Verified both directions: against a working
session it exits 0 over 13 checks; against a declaration carrying defects #1, #2 and #3 it
names all three and exits 1.

**Container-side facts are checked by executing inside the container, never inferred from host
ownership bits.** The `~/.claude` writability probe is a real `touch`, and it has been shown to
return non-zero on a root-owned directory and zero on a writable one — the estate's standing
lesson is that a plausible host-side check is precisely how this class of bug stays hidden.

## The order, and why each step is where it is

### 1. Ask WHERE before cloning — four things are decided by it

Container or host · does it need `git-lfs` · is that path backed up · how big is it. **A host
session reads the operator's SSH keys, every secrets directory and every repo, uncapped.** If
the answer is host, say what that grants rather than letting it be the default nobody chose.

### 2. Clone, then verify the clone

On a machine without `git-lfs`, an LFS repo checks out as ~132-byte pointer stubs that keep the
real filename and extension — silent now, loud much later. Check for stubs before moving on.

### 3. The stack, if it is a container session

Judgement, not template-filling, and the skill does not automate it:

- **Reuse an existing agent image** unless this repo needs something it lacks. Derive a new one
  the day it does, not before.
- **Its own single-member network** if it publishes anything. A published port binds the
  container's `eth0` — docker never forwards to container loopback — so on a shared network
  that bind is reachable by every other container on it.
- **Publish to host loopback only**, never `0.0.0.0` and not a tailnet address.
- **`mem_limit` strictly below `memswap_limit`.** Equal values mean zero swap, so hitting the
  cap can only end in an OOM kill; a gap buys slow instead of dead.
- **No SSH mount.** Push as a bot over HTTPS from a token file.

### 4. ⚠️ Create the container's home directory BY HAND, before the first `up`

**This is the step that has no natural prompt and breaks everything downstream.** If the bind
mount's source does not exist, docker creates it **as root**. A container running as a normal
uid then cannot write its own `~/.claude`, and the session parks on the login picker with
nothing logged anywhere. It cannot be repaired by logging in — there is nowhere to write the
credential.

```sh
mkdir -p <host-home>/.claude     # as the operator, BEFORE docker ever sees the path
```

Nested mountpoints docker creates *inside* that directory may stay root-owned; that is
harmless. The directory itself must not be.

### 5. Write `.claude-session`, and get the key names right

```ini
target=container          # container | host
container=<name>          # required when target=container
workdir=/app/<repo>       # the path INSIDE the container
model=opus
rc=<repo>-srv             # remote-control name; keep stable, you search by it
tmux=<repo>-srv
permission_mode=          # optional
```

**`rc=`, not `rc-name=`.** An unknown key is ignored in silence. And the rc name must be
unique across live sessions and the launcher's own config — a name two sessions answer to is a
session you cannot address.

### 6. Authenticate — and know which file does what

A fresh home has neither file. **Preferred: log in once through `tmux attach`.** The home is a
bind mount, so it survives container recreation, and nothing is propagated between containers.

If a credential is placed by hand instead, that is **the operator's decision, never the
agent's** — and it is only half the job:

| file | carries | symptom when missing |
|---|---|---|
| `~/.claude/.credentials.json` | the token | login picker |
| `~/.claude.json` | `oauthAccount`, `hasCompletedOnboarding` | login picker, *even with the token present* |

⚠️ **Two containers sharing one credential share one refresh token.** Whichever refreshes first
may invalidate the other's copy. A per-container login avoids this entirely.

### 7. Adopt the shared rules BEFORE the first launch, not after

Run [`retrieve-lessons`](../retrieve-lessons/SKILL.md) against the repo while the session is
still down. A session already running holds the context it started with, so rules pulled
mid-conversation do not reach it until it restarts — adopting after launch buys nothing until
the next rotation.

### 8. Launch, then verify the SESSION, not the launcher

Hand off to [`launch-session`](../launch-session/SKILL.md) or the estate's managed launcher.
Then look at the pane. First run walks theme → login → trust folder, and a session sitting on
any of those is not running, however healthy the container looks.

**Finally, confirm it registered under the name you chose.** Without `--remote-control`, Claude
Code registers under an auto-generated name, runs perfectly, and is invisible from a phone with
no error anywhere.

## What "done" looks like

Preflight exits 0 · the pane shows a prompt rather than a picker · the session appears in the
peer list under its declared rc name · `CLAUDE.md` carries a current shared-lessons block.

**Anything short of all four is a session that started, not one that works.**

## Related

[`launch-session`](../launch-session/SKILL.md) — the next step; it assumes everything here.
[`retrieve-lessons`](../retrieve-lessons/SKILL.md) — step 7.
[`discriminate-by-executing-not-inspecting`](../../rules/how-we-work/discriminate-by-executing-not-inspecting.md)
— why the preflight execs into the container instead of reading ownership bits.
[`escalate-the-blocker-before-polishing-the-rest`](../../rules/how-we-work/escalate-the-blocker-before-polishing-the-rest.md)
— an unauthenticated session is a blocker; say so before reporting the launch a success.

[`PRD.md`](PRD.md) — what the preflight is for, and the four things it deliberately will not do.
