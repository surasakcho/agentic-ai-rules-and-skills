#!/usr/bin/env bash
set -euo pipefail

# Links all skills in the repository into the local skill directories used by
# each agent harness:
#   - ~/.claude/skills  — Claude Code
#   - ~/.agents/skills  — pi and other Agent-Skills-standard harnesses
# Each entry is a symlink into this repo, so a `git pull` is all that's needed
# to keep installed skills up to date.

# Walk up to the nearest ancestor that actually contains a skills/ directory,
# rather than assuming a fixed depth. This script is committed at
# <repo>/skills/scripts/, so the previous "$(dirname "$0")/.." resolved REPO to
# <repo>/skills and then searched <repo>/skills/skills -- which does not exist,
# so find errored and the script linked nothing while still exiting 0 through
# the pipeline. Walking up works from either location.
REPO="$(cd "$(dirname "$0")" && pwd)"
while [ "$REPO" != "/" ] && [ ! -d "$REPO/skills" ]; do
  REPO="$(dirname "$REPO")"
done
[ -d "$REPO/skills" ] || { echo "error: no skills/ dir found above $0" >&2; exit 1; }
DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")

# Collect the repo's skills once, link into every destination.
names=()
srcs=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names+=("$(basename "$src")")
  srcs+=("$src")
done < <(find "$REPO/skills" -name SKILL.md -not -path '*/node_modules/*' -not -path '*/deprecated/*' -print0)

for DEST in "${DESTS[@]}"; do
  # If $DEST is a symlink that resolves into this repo, we'd end up writing the
  # per-skill symlinks back into the repo's own skills/ tree. Detect and bail
  # out instead of polluting the working copy.
  if [ -L "$DEST" ]; then
    resolved="$(readlink -f "$DEST")"
    case "$resolved" in
      "$REPO"|"$REPO"/*)
        echo "error: $DEST is a symlink into this repo ($resolved)." >&2
        echo "Remove it (rm \"$DEST\") and re-run; the script will recreate it as a real dir." >&2
        exit 1
        ;;
    esac
  fi

  mkdir -p "$DEST"

  for i in "${!names[@]}"; do
    name="${names[$i]}"
    src="${srcs[$i]}"
    target="$DEST/$name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
      rm -rf "$target"
    fi

    # RELATIVE (-r), not absolute, so the same farm resolves inside a container.
    # An absolute link hardcodes this machine's $HOME -- e.g.
    # /home/<user>/projects/... -- and a container has no such directory, so
    # every link dangles and the harness reports no error, it just sees zero
    # skills. A relative link resolves against wherever the farm itself is
    # mounted, so bind-mounting this repo at <container-home>/projects/<repo>
    # is enough. Verified both ways: 57/57 resolve on the host and 57/57 in a
    # container; with absolute links the container resolves 0.
    ln -sfnr "$src" "$target"
    echo "linked $name -> $(readlink "$target") ($DEST)"
  done
done
