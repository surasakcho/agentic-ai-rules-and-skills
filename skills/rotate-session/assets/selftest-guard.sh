#!/usr/bin/env bash
# selftest-guard.sh — prove the self-target guard accepts ONLY the current session.
# Safe: it only exercises rotate_assert_self (which returns a status); it NEVER ends anything.
# Run from inside any session, host or container. Exit 0 = all assertions held; 1 = a guard failure.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/rotate-env.sh"

MODE="$(rotate_mode)"
CUR="$(rotate_current_session)"
if [[ "$MODE" == "unknown" || -z "$CUR" ]]; then
  echo "SKIP: no identifiable session here (not inside tmux, and not a container session with a --remote-control name)."; exit 0
fi
echo "mode=$MODE  current=$CUR"

fails=0
ok(){ printf 'PASS  %s\n' "$1"; }
bad(){ printf 'FAIL  %s\n' "$1"; fails=$((fails+1)); }

# ACCEPT: the current session name (the one legitimate self-rotation target).
if rotate_assert_self "$CUR" 2>/dev/null; then ok "accept current session '$CUR'"; else bad "should ACCEPT current '$CUR'"; fi

# REFUSE: every OTHER live tmux session (host mode only — a container has none), plus synthetic
# edge cases. Any candidate that happens to equal the current session is skipped (it would be a
# legitimate accept, not a refuse case).
others=""
[[ "$MODE" == "tmux" ]] && others="$(tmux ls -F '#{session_name}' 2>/dev/null | grep -vxF "$CUR" || true)"
for bogus in $others "" "SBX-1" "${CUR}x" "x${CUR}" "$CUR; rm -rf /" "*" "nonexistent-repo" "ebiz-svr" "youtube-svr"; do
  [[ "$bogus" == "$CUR" ]] && continue
  if rotate_assert_self "$bogus" 2>/dev/null; then bad "should REFUSE '$bogus'"; else ok "refuse '$bogus'"; fi
done

# Container mode only: the kill path resolves to OUR OWN pid and nothing else.
if [[ "$MODE" == "container" ]]; then
  pid="$(rotate_claude_pid)"
  if [[ -n "$pid" ]] && rotate_is_claude_pid "$pid"; then ok "own claude pid resolves and validates ($pid)"; else bad "own claude pid unresolvable — kill path would refuse"; fi
  rc="$(rotate_rc_name)"
  if [[ "$rc" == "$CUR" ]]; then ok "identity comes from our own --remote-control name ('$rc')"; else bad "rc name '$rc' != current '$CUR'"; fi
  live="$(rotate_project_dir_from_live)"; fromcwd="$(rotate_project_dir_from_cwd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")"
  if [[ -n "$live" && "$live" == "$fromcwd" ]]; then ok "transcript store agrees from both derivations ($live)"
  else bad "transcript store disagrees: live='$live' from-cwd='$fromcwd' (rotation would refuse)"; fi
fi

echo "----"
if [[ "$fails" -eq 0 ]]; then echo "GUARD OK — self-rotation only."; exit 0
else echo "GUARD BROKEN — $fails assertion(s) failed."; exit 1; fi
