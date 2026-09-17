#!/usr/bin/env bash
# rotate-status.sh [session]   (default: the session this is running inside)
# Read-only: is claude on a real TTY, and does it hold an established Anthropic relay connection
# (160.79.104.0/22)? Never kills or changes anything. Works in both topologies:
#   tmux mode      — resolve the claude pid through the tmux pane
#   container mode — resolve it as our own claude process (there is no tmux in here)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/rotate-env.sh"

MODE="$(rotate_mode)"
s="${1:-$(rotate_current_session)}"
[[ -n "$s" ]] || { echo "(no session given, and this context has no identifiable session)"; exit 0; }

cl_pid=""
if [[ "$MODE" == "tmux" ]]; then
  tmux has-session -t "$s" 2>/dev/null || { echo "$s (not running)"; exit 0; }
  pane_pid="$(tmux list-panes -t "$s" -F '#{pane_pid}' 2>/dev/null | head -1)"
  cl_pid="$(pgrep -P "$pane_pid" -f 'claude' 2>/dev/null | head -1)"
  [[ -z "$cl_pid" ]] && cl_pid="$(pgrep -f -- "remote-control $s" 2>/dev/null | head -1)"
else
  # Container: the only session reachable from in here is our own, so a name that is not ours
  # cannot be reported on — say so rather than printing a misleading "(not running)".
  if [[ "$s" != "$(rotate_current_session)" ]]; then
    echo "$s (not reachable from inside this container — only this session is)"; exit 0
  fi
  cl_pid="$(rotate_claude_pid)"
fi

tty="$(readlink /proc/${cl_pid:-0}/fd/1 2>/dev/null || true)"
is_tty="no"; [[ "$tty" == /dev/pts/* ]] && is_tty="YES"
# Count established relay connections. grep -c exits 1 on zero matches, so tolerate it under pipefail.
relay=0
if [[ -n "$cl_pid" ]]; then
  relay="$(ss -tnp 2>/dev/null | { grep -w "pid=${cl_pid}" || true; } | { grep ESTAB || true; } | grep -Ec '160\.79\.10[4-7]\.' || true)"
  [[ -z "$relay" ]] && relay=0
fi
printf "%-16s mode=%-9s claude_pid=%-8s on_TTY=%-3s relay_conns=%s\n" "$s" "$MODE" "${cl_pid:-none}" "$is_tty" "$relay"
