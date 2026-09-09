#!/usr/bin/env bash
# Keep a side worktree's branch from diverging from main.
#
# Two modes:
#   --check   report divergence and exit non-zero if the branch is behind or ahead. Read-only.
#   (none)    fetch, rebase onto origin/main, push the branch, fast-forward origin/main.
#
# Safe to run from anywhere and safe to run repeatedly. It NEVER leaves a rebase half-finished:
# on conflict it aborts, restores the branch, and tells you what to do. A conflict means both
# sessions really did change the same lines, and that is a decision for a person.
set -uo pipefail

MAIN_BRANCH="${MAIN_BRANCH:-main}"
cd "$(git rev-parse --show-toplevel)" || exit 1
BRANCH="$(git rev-parse --abbrev-ref HEAD)"

# Guard: worktrees SHARE .git/hooks, so a post-commit hook installed for the side worktree also
# fires in the main one. Refuse to act on the main branch -- there is nothing to sync there.
if [ "$BRANCH" = "$MAIN_BRANCH" ]; then
  # On main there is nothing to push -- side branches land here directly. What main can be is
  # BEHIND. Bring it up to date, but ONLY when doing so cannot destroy anything. Post-commit is
  # the safe moment by construction: a commit just succeeded, so the tree is usually clean.
  git fetch -q origin "$MAIN_BRANCH" 2>/dev/null || exit 0
  behind=$(git rev-list --count "HEAD..origin/$MAIN_BRANCH" 2>/dev/null || echo 0)
  ahead=$(git rev-list --count "origin/$MAIN_BRANCH..HEAD" 2>/dev/null || echo 0)

  if [ "${behind:-0}" -eq 0 ]; then
    [ "${1:-}" = "--check" ] && echo "on $MAIN_BRANCH, up to date with origin/$MAIN_BRANCH."
    exit 0
  fi

  # --- the safety gates. Any one of them failing means WARN, never act. ---
  unsafe=""
  git diff --quiet            || unsafe="uncommitted changes in the working tree"
  git diff --cached --quiet   || unsafe="staged changes not yet committed"
  gd=$(git rev-parse --git-dir)
  [ -d "$gd/rebase-merge" ] || [ -d "$gd/rebase-apply" ] && unsafe="a rebase is already in progress"
  [ -f "$gd/MERGE_HEAD" ]     && unsafe="a merge is in progress"
  [ -f "$gd/CHERRY_PICK_HEAD" ] && unsafe="a cherry-pick is in progress"

  if [ -n "$unsafe" ]; then
    echo "SYNC: $behind commit(s) behind origin/$MAIN_BRANCH -- NOT pulling: $unsafe."
    echo "      Pull deliberately when ready: git pull --rebase --autostash"
    exit 0
  fi

  # Hooks run with git env vars set, which confuse rebase across worktrees. Clear them.
  unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_PREFIX

  if [ "${ahead:-0}" -eq 0 ]; then
    # Nothing local to replay: a fast-forward, which cannot conflict and cannot lose a commit.
    if git merge -q --ff-only "origin/$MAIN_BRANCH"; then
      echo "SYNC: fast-forwarded $MAIN_BRANCH $behind commit(s) to $(git rev-parse --short HEAD)."
    else
      echo "SYNC: fast-forward refused unexpectedly -- pull by hand."
    fi
    exit 0
  fi

  # Local commits exist AND we are behind: replay them onto origin/main.
  before=$(git rev-parse HEAD)
  if git rebase -q "origin/$MAIN_BRANCH"; then
    echo "SYNC: rebased $ahead local commit(s) onto origin/$MAIN_BRANCH ($(git rev-parse --short HEAD))."
    git push -q origin "HEAD:$MAIN_BRANCH" \
      && echo "SYNC: pushed to origin/$MAIN_BRANCH." \
      || echo "SYNC: rebased, but the push was refused -- origin moved again. Re-run."
  else
    git rebase --abort 2>/dev/null
    echo "SYNC: CONFLICT rebasing $MAIN_BRANCH onto origin/$MAIN_BRANCH -- aborted, restored to $before."
    # Cannot push to main (it would be rejected anyway), but the commits must not live only on
    # this disk. Park them on a rescue branch -- always a fast-forward, cannot conflict.
    rescue="rescue/$MAIN_BRANCH-$(date +%Y%m%d-%H%M%S)"
    if git push -q origin "HEAD:refs/heads/$rescue"; then
      echo "      The commits are SAFE on origin/$rescue -- nothing is only on this disk."
    else
      echo "      !! AND THE RESCUE PUSH FAILED -- these commits exist only on this disk."
    fi
    echo "      Both sessions changed the same lines. Resolve deliberately:"
    echo "        git pull --rebase origin $MAIN_BRANCH"
  fi
  exit 0
fi

git fetch -q origin "$MAIN_BRANCH" || { echo "SYNC: fetch failed -- offline? nothing changed."; exit 2; }

counts=$(git rev-list --left-right --count "origin/$MAIN_BRANCH...HEAD")
behind=${counts%%	*}; ahead=${counts##*	}

if [ "${1:-}" = "--check" ]; then
  printf '%s: %s ahead, %s behind origin/%s\n' "$BRANCH" "$ahead" "$behind" "$MAIN_BRANCH"
  if [ "$ahead" -eq 0 ] && [ "$behind" -eq 0 ]; then echo "in sync"; exit 0; fi
  echo "DIVERGED -- run tools/worktree-sync.sh"
  exit 1
fi

if [ "$ahead" -eq 0 ] && [ "$behind" -eq 0 ]; then echo "SYNC: already in sync."; exit 0; fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "SYNC: refusing -- uncommitted changes present. Commit them first."; exit 3
fi

before=$(git rev-parse HEAD)
if ! git rebase -q "origin/$MAIN_BRANCH"; then
  conflicted=$(git diff --name-only --diff-filter=U 2>/dev/null | tr '\n' ' ')
  git rebase --abort 2>/dev/null
  echo "SYNC: CONFLICT rebasing onto origin/$MAIN_BRANCH -- aborted, branch restored to $before."
  # The work cannot land on main, but it MUST NOT be left only on this disk. Pushing the branch
  # is always a fast-forward and cannot conflict, so it is safe to do even now.
  if git push -q -u origin "$BRANCH"; then
    echo "      The commits are SAFE on origin/$BRANCH -- they just cannot land on $MAIN_BRANCH yet."
  else
    echo "      !! AND THE BRANCH PUSH FAILED -- these commits exist only on this disk. Push by hand."
  fi
  echo "      Both sessions changed the same lines. Resolve deliberately:"
  echo "        git rebase origin/$MAIN_BRANCH   # then fix, git add, git rebase --continue"
  # Record it ON MAIN, so the conflict is an open task every session sees rather than a line of
  # output in one session's scrollback.
  [ -x tools/conflict-record.sh ] && tools/conflict-record.sh open "$BRANCH" "$(pwd)" $conflicted
  exit 4
fi

git push -q --force-with-lease -u origin "$BRANCH" || { echo "SYNC: branch push failed."; exit 5; }

if git push -q origin "HEAD:$MAIN_BRANCH"; then
  echo "SYNC: $BRANCH rebased and landed on origin/$MAIN_BRANCH ($(git rev-parse --short HEAD))."
  [ -x tools/conflict-record.sh ] && tools/conflict-record.sh clear "$BRANCH"
else
  echo "SYNC: branch pushed, but origin/$MAIN_BRANCH moved again -- re-run to land it."
  exit 6
fi
