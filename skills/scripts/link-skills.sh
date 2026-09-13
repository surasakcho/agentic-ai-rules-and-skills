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

  # PRUNE. Linking is only half of a sync: this loop walks what the repo HAS, so a
  # renamed or deleted skill leaves its old link behind forever. Observed live -- a
  # rename produced `to-spec`/`to-tickets` on the next run and left `to-prd`/`to-issues`
  # dangling in BOTH farms; a deletion produces only the dangling half and nothing
  # announces it at all.
  #
  # BOTH CONDITIONS ARE REQUIRED, and the second is what keeps this safe: remove a link
  # only if it points INTO this repo's skills/ AND no longer resolves. Sweeping every
  # broken link in the farm would delete links another repo owns -- these directories are
  # shared, which is the whole reason they are a farm.
  pruned=0
  for target in "$DEST"/*; do
    [ -L "$target" ] || continue
    [ -e "$target" ] && continue                      # resolves: not ours to judge
    raw="$(readlink "$target")"
    case "$raw" in
      /*) abs="$raw" ;;
      *)  abs="$(cd "$DEST" 2>/dev/null && printf '%s/%s' "$(pwd -P)" "$raw")" ;;
    esac
    # Normalise without requiring existence -- the target is broken by definition here.
    abs="$(printf '%s' "$abs" | awk -F/ '{n=0; for(i=1;i<=NF;i++){ if($i==""||$i==".") continue;
          if($i==".."){ if(n>0) n--; continue } a[++n]=$i } s=""; for(i=1;i<=n;i++) s=s"/"a[i];
          print (s==""?"/":s) }')"
    case "$abs" in
      "$REPO/skills/"*) rm -f "$target"; pruned=$((pruned+1));
                        echo "pruned $(basename "$target") (was $raw)" ;;
    esac
  done
  [ "$pruned" -eq 0 ] || echo "pruned $pruned dangling link(s) in $DEST"
done
