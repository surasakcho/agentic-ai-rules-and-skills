#!/usr/bin/env bash
# Record (or clear) an unresolved-conflict marker ON MAIN, without checking main out.
#
#   conflict-record.sh open  <branch> <worktree> <files...>
#   conflict-record.sh clear <branch>
#
# Uses git plumbing to build a commit on top of origin/<MAIN_BRANCH> and push it, so it works from
# any worktree and never touches either working tree. The marker file is the point: every session
# reads main, so an unresolved conflict becomes an open task nobody has to be told about.
set -uo pipefail
MAIN_BRANCH="${MAIN_BRANCH:-main}"
FILE="ops/open-conflicts.md"
HEADER="# Unresolved conflicts

**Written and cleared automatically by \`tools/worktree-sync.sh\`. Do not hand-edit.**
An entry here means a worktree has commits that cannot land on \`$MAIN_BRANCH\` until someone
resolves them. **The entry disappears on its own once the sync succeeds.**
"
mode="${1:?open|clear}"; branch="${2:?branch}"; shift 2 || true

git fetch -q origin "$MAIN_BRANCH" 2>/dev/null || exit 0
base=$(git rev-parse "origin/$MAIN_BRANCH") || exit 0

current=$(git show "$base:$FILE" 2>/dev/null || printf '%s' "$HEADER")
# drop any existing section for this branch (from its heading to the next heading or EOF)
stripped=$(printf '%s\n' "$current" | awk -v b="## $branch" '
  $0==b {skip=1; next}
  skip && /^## / {skip=0}
  !skip {print}')

if [ "$mode" = "open" ]; then
  wt="${1:-unknown}"; shift || true
  body="$stripped

## $branch

- **detected:** $(date -u '+%Y-%m-%d %H:%M UTC')
- **worktree:** \`$wt\`
- **commits waiting:** $(git rev-list --count "origin/$MAIN_BRANCH..HEAD" 2>/dev/null || echo '?') — safe on \`origin/$branch\`, not on \`$MAIN_BRANCH\`
- **conflicting files:** ${*:-（not captured）}
- **resolve:** \`cd $wt && git rebase origin/$MAIN_BRANCH\` → fix → \`git add\` → \`git rebase --continue\`

**This entry clears itself when the sync next succeeds.**"
else
  body="$stripped"
fi

# nothing changed? do not make an empty commit
if [ "$(printf '%s' "$body")" = "$(printf '%s' "$current")" ]; then exit 0; fi

blob=$(printf '%s\n' "$body" | git hash-object -w --stdin) || exit 1
# Build the new tree in a TEMPORARY index. Never run read-tree/update-index against the real
# index -- it silently overwrites the session's staging area with main's tree, which leaves the
# working tree dirty and blocks every later rebase. (That bug was here, and it did exactly that.)
export GIT_INDEX_FILE
GIT_INDEX_FILE=$(mktemp) || exit 1
git read-tree "$base" || { rm -f "$GIT_INDEX_FILE"; exit 1; }
git update-index --add --cacheinfo 100644,"$blob","$FILE" || { rm -f "$GIT_INDEX_FILE"; exit 1; }
newtree=$(git write-tree) || { rm -f "$GIT_INDEX_FILE"; exit 1; }
rm -f "$GIT_INDEX_FILE"; unset GIT_INDEX_FILE

if [ "$mode" = "open" ]; then msg="conflict: $branch cannot land on $MAIN_BRANCH"
else msg="conflict resolved: $branch landed on $MAIN_BRANCH"; fi
commit=$(git commit-tree "$newtree" -p "$base" -m "$msg

Written automatically by tools/worktree-sync.sh. See ops/open-conflicts.md.") || exit 1
git push -q origin "$commit:refs/heads/$MAIN_BRANCH" 2>/dev/null \
  && echo "      Recorded on $MAIN_BRANCH: ops/open-conflicts.md" \
  || echo "      (could not record on $MAIN_BRANCH -- it moved; will retry next commit)"
