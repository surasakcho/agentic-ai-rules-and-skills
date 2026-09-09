#!/usr/bin/env bash
# Install the worktree sync into a repo: copy the scripts, install the shared-safe post-commit hook.
# Idempotent. Run from inside the repo (any worktree).
set -euo pipefail
root=$(git rev-parse --show-toplevel)
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$root/tools"
cp "$here/worktree-sync.sh" "$here/conflict-record.sh" "$root/tools/"
chmod +x "$root/tools/worktree-sync.sh" "$root/tools/conflict-record.sh"
hooks="$(git rev-parse --git-common-dir)/hooks"
mkdir -p "$hooks"
cat > "$hooks/post-commit" <<'HOOK'
#!/usr/bin/env bash
# Keeps worktrees from diverging. Worktrees SHARE this hooks directory, so the script itself
# decides what to do based on the current branch -- do not put that guard here.
root=$(git rev-parse --show-toplevel)
[ -x "$root/tools/worktree-sync.sh" ] && "$root/tools/worktree-sync.sh" || true
HOOK
chmod +x "$hooks/post-commit"
echo "installed: tools/worktree-sync.sh, tools/conflict-record.sh, $hooks/post-commit"
