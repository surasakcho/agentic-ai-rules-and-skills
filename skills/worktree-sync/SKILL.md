---
name: worktree-sync
description: Give a second concurrent session its own git worktree so two sessions cannot silently overwrite each other, and keep the branches from diverging automatically. Use when two Claude sessions work on one repo, when a side session must not disturb a main one, when edits mysteriously vanish or a patch reports success while applying nothing, or when asked to set up a worktree, stop sessions clobbering each other, or keep a branch merged with main.
license: MIT
---

# Worktree sync — two sessions, one repo, no silent overwrites

## The problem this exists for

**Two agent sessions in one working directory are not isolated by git.** There is one set of files
on disk. Git mediates nothing, because there are never two versions to merge — the last write wins,
with no conflict, no marker and no prompt.

**Committed work is not at risk.** It is in history, and an edit to the same lines shows in a diff.
**Uncommitted work is**, and it fails in a way that is hard to see:

- A **whole-file write** replaces whatever the other session had not committed.
- A **targeted edit** silently does not apply when the other session already changed the text it
  matched on — and a script that does not check reports success.
- **`git add <file>`** stages whatever is on disk at that moment, so one session's commit can carry
  the other's half-finished work under a message that does not describe it.

**The shape is a lost update.** Both sessions read → think → write, and thinking takes minutes. Read
at 10:00, the other session writes at 10:01, write at 10:02 from what was read at 10:00 — their
change is gone.

*Observed, not theorised: a patch reported four fixes applied while the commit contained none of
them, because every anchor string had moved underneath it; and two sessions independently issued the
same identifier in one document.*

## Install

```sh
skills/worktree-sync/assets/install.sh        # copies the scripts, installs the hook
git worktree add -b side/<topic> ~/worktrees/<name> origin/main
```

Two directories, two checkouts, one repository, one history. **Neither session can touch the other's
files.** Git only allows a branch to be checked out in one worktree at a time — that restriction is
the safety, not an inconvenience.

## What it does after every commit

**On a side branch:** fetch, rebase onto `origin/main`, push the branch, fast-forward `origin/main`.
Divergence is bounded at one commit.

**On `main`:** pull, but only through four gates — clean working tree, nothing staged, no rebase in
progress, no merge or cherry-pick in progress. Fast-forward when there are no local commits; rebase
and push when there are. **If any gate fails it warns and does nothing.** Post-commit is the safe
moment by construction: a commit just succeeded, so the tree is normally clean.

> **Never rebase a session that may have uncommitted work under it.** A refused push is a loud, safe
> failure; a surprise rewrite is a silent, unsafe one.

## What it does when a rebase conflicts

1. **Aborts and restores the exact starting commit.** No half-finished rebase, no lost commit.
2. **Gets the work onto the remote anyway** — pushing a branch is always a fast-forward and cannot
   conflict, so it happens regardless. Side branches go to `origin/<branch>`; local commits on main
   are parked on a timestamped `rescue/main-<date>`. **A conflict can sit unresolved for hours; that
   is the wrong moment for the only copy to be on one disk.**
3. **Records it on `main` as an open task** — `ops/open-conflicts.md`, written with git plumbing on
   top of `origin/main` so no checkout is needed. It names the branch, the worktree, how many commits
   are waiting, which files conflicted and how to resolve. **The entry clears itself when the sync
   next succeeds.** Every session reads main, so the conflict is found rather than announced.
4. **Retries on every later commit and keeps failing loudly** until someone resolves it. That noise
   is deliberate.

**The resolution is always a person's.** A conflict means both sessions genuinely edited the same
lines and no script should pick a winner.

## Deliberately NOT included

- **No `-X ours` / `-X theirs`.** Silently discarding one session's work is the exact failure this
  prevents.
- **No union merge driver.** It resolves conflicts nobody decided. Lossless, but it can interleave
  two edits into nonsense with no one asked to look.
- **No `git rerere`.** It replays *your own* resolution, so it is not a guess — but from the second
  occurrence onward nobody is told, and here the repeats are only our own hook retrying. **Suppressing
  noise we generate ourselves hides the signal that two sessions are writing the same file.**

## Two traps that cost real time

- **Worktrees share ONE hooks directory** (`git rev-parse --git-common-dir`), so a hook installed for
  one fires in all of them. **Put the branch guard in the script, not the hook** — a future hook edit
  would drop it.
- **Hooks run with `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` set**, and those confuse `rebase`
  across worktrees. Clear them first.
- **A tool that writes git state must never touch the real index.** An early version ran `git
  read-tree` against the live index before switching to a temporary one; it silently replaced the
  session's staging area, left the working tree dirty and blocked every later rebase — with the
  symptom (*"cannot rebase: you have unstaged changes"*) two steps from the cause. Build in a
  temporary `GIT_INDEX_FILE` and nothing else.

## Checking

```sh
tools/worktree-sync.sh --check    # N ahead, M behind; exits non-zero when diverged
tools/worktree-sync.sh            # sync now
```

`--check` exits non-zero on purpose, so it can gate other things. **"No output" and "in sync" must
not look the same.**

## What it does not fix

One writer per file is still the first rule — this stops silent clobbering, not conflicts. Two
sessions can still both invent the same identifier in a shared document, because neither is wrong
locally. And verifying that an edit actually landed is a separate habit: report which anchors matched
and which did not, rather than assuming a patch applied.
