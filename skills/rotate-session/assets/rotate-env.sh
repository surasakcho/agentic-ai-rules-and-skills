#!/usr/bin/env bash
# rotate-env.sh — shared helpers + the SELF-TARGET guard for the rotate-session skill.
# Source at the top of every rotate-* script:  source "$(dirname "$0")/rotate-env.sh"
#
# SAFETY CONTRACT (why this file exists):
#   rotate-session refreshes a LIVE Claude session by ending it and letting a same-name successor
#   come up with an empty context window. The sandbox (session-sandbox) is safe because ONLY sbx-*
#   names are targetable. This skill runs against REAL session names in EVERY repo, so that prefix
#   guard is gone. The guarantee here is SELF-ROTATION ONLY:
#     * the only session you may act on is the one you are running inside
#     * rotate_assert_self REFUSES an empty name, an unidentifiable context, or any name != current
#     * there is deliberately NO kill-by-pattern, NO kill-all, NO kill-by-arbitrary-name path.
#       The ONLY kill is rotate_kill <name>, and it calls the guard first.
#   => a typo, a stale config, or a bad env var can never resolve to ANOTHER repo's session:
#      it will not equal the current session name, so the guard refuses.
#
# TWO TOPOLOGIES (2026-09-17). A session runs one of two ways on this estate, and they differ in
# what "the session" even IS:
#
#   MODE=tmux       host session. `claude` is the tmux pane command. Identity = the tmux session
#                   name. Ending it = `tmux kill-session`. The successor is scheduled by us
#                   (systemd-run --user) before the kill.
#
#   MODE=container  container session. The tmux session lives on the HOST, wrapping
#                   `docker exec -it -w <workdir> <container> claude --continue ... --remote-control <rc>`
#                   in a restart loop. INSIDE the container there is no tmux, no systemd and no
#                   docker socket — the host is unreachable except through the shared bind mount.
#                   Identity = the --remote-control name on our OWN claude process. Ending it =
#                   signalling that one pid. The successor is NOT scheduled by us: the host restart
#                   loop already exists and relaunches ~3s after claude exits.
#
#   The container guard is not weaker than the tmux one, it is stronger: the PID namespace means
#   there is no other session's process to reach even if the guard were wrong.

set -euo pipefail

ROTATE_LOG(){ printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S %z')" "$*" >&2; }

# --- mode -------------------------------------------------------------------------------------
# tmux if we are actually inside a tmux session; container if we are inside a container and can
# identify our own claude process. Derived from live state, never configured.
rotate_mode(){
  if [[ -n "$(rotate_tmux_session)" ]]; then echo tmux; return 0; fi
  if rotate_in_container && [[ -n "$(rotate_claude_pid)" ]]; then echo container; return 0; fi
  echo unknown
}

rotate_in_container(){ [[ -f /.dockerenv ]] || grep -qa 'docker\|containerd' /proc/1/cgroup 2>/dev/null; }

rotate_tmux_session(){ command -v tmux >/dev/null 2>&1 && tmux display-message -p '#S' 2>/dev/null || true; }

# --- container identity -----------------------------------------------------------------------
# Our own claude process. $CLAUDE_PID is set by Claude Code itself; it is VALIDATED against
# /proc rather than trusted, and there is a ppid-walk fallback if it is absent.
rotate_claude_pid(){
  local pid="${CLAUDE_PID:-}"
  if [[ -n "$pid" ]] && rotate_is_claude_pid "$pid"; then printf '%s' "$pid"; return 0; fi
  # Fallback: walk up from this shell until a process whose cmdline is the claude CLI.
  pid=$$
  local i=0
  while [[ "$pid" -gt 1 && "$i" -lt 12 ]]; do
    if rotate_is_claude_pid "$pid"; then printf '%s' "$pid"; return 0; fi
    pid="$(awk '{print $4}' "/proc/$pid/stat" 2>/dev/null || echo 1)"
    i=$((i+1))
  done
  return 0   # empty = could not identify; every caller treats that as "refuse"
}

rotate_is_claude_pid(){
  local pid="${1:-}"
  [[ -n "$pid" && -r "/proc/$pid/cmdline" ]] || return 1
  local cmd; cmd="$(tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null || true)"
  [[ "$cmd" == *claude* ]]
}

rotate_cmdline(){
  local pid="${1:?pid}"
  tr '\0' '\n' < "/proc/$pid/cmdline" 2>/dev/null || true
}

# The --remote-control name our own claude process was started with. This is the name the operator
# searches for from a phone, and in container mode it IS the session identity.
rotate_rc_name(){
  local pid; pid="$(rotate_claude_pid)"
  [[ -n "$pid" ]] || return 0
  rotate_cmdline "$pid" | awk '$0=="--remote-control"{getline; print; exit}'
}

# --- the session name this script is running inside (empty if unidentifiable) -------------------
rotate_current_session(){
  local t; t="$(rotate_tmux_session)"
  if [[ -n "$t" ]]; then printf '%s' "$t"; return 0; fi
  rotate_in_container && rotate_rc_name
}

# THE GUARD. Non-zero (aborts `set -e` callers) unless <name> is THIS session — self-rotation only.
rotate_assert_self(){
  local name="${1:-}"
  local current; current="$(rotate_current_session)"
  if [[ -z "$name" ]]; then
    ROTATE_LOG "GUARD: empty target name — refusing."; return 1
  fi
  if [[ -z "$current" ]]; then
    ROTATE_LOG "GUARD: cannot identify the session this is running inside (no tmux session, and no --remote-control name on our own claude process) — refusing '$name'."; return 1
  fi
  if [[ "$name" != "$current" ]]; then
    ROTATE_LOG "GUARD: target '$name' is not the current session '$current' — self-rotation ONLY. REFUSING. Other sessions are unreachable by design."; return 1
  fi
  return 0
}

# The ONLY kill path. Guarded. Mode decides what "end this session" means.
rotate_kill(){
  local name="${1:-}"
  rotate_assert_self "$name" || return 1
  local mode; mode="$(rotate_mode)"
  case "$mode" in
    tmux)
      if tmux has-session -t "$name" 2>/dev/null; then
        tmux kill-session -t "$name"
        ROTATE_LOG "killed session '$name' (self)."
      else
        ROTATE_LOG "no session '$name' to kill (already gone)."
      fi
      ;;
    container)
      # There is no tmux in here. Ending the session means ending OUR OWN claude process: the
      # host's `docker exec` returns, and the host restart loop brings the successor up.
      local pid; pid="$(rotate_claude_pid)"
      if [[ -z "$pid" ]] || ! rotate_is_claude_pid "$pid"; then
        ROTATE_LOG "GUARD: own claude pid not identifiable at kill time — refusing."; return 1
      fi
      ROTATE_LOG "ending own claude process pid=$pid (session '$name'); host restart loop takes it from here."
      # Escalation runs detached so it outlives the process tree we are about to end.
      setsid bash -c "sleep 10; kill -0 $pid 2>/dev/null && kill -9 $pid 2>/dev/null" >/dev/null 2>&1 &
      kill "$pid"
      ;;
    *)
      ROTATE_LOG "GUARD: unknown mode — refusing to end anything."; return 1
      ;;
  esac
}

# --- transcript store -------------------------------------------------------------------------
# Claude Code keeps one conversation transcript per (project dir) under ~/.claude/projects/<slug>/.
# DERIVE the directory from live state (our own session's transcript file) rather than trusting a
# slug-mangling rule; fall back to the '/'->'-' rule only when the env var is unavailable.
rotate_project_dir_from_live(){
  local sid="${CLAUDE_CODE_SESSION_ID:-}"
  [[ -n "$sid" ]] || return 0
  local f; f="$(find "$HOME/.claude/projects" -maxdepth 2 -name "$sid.jsonl" -print -quit 2>/dev/null || true)"
  [[ -n "$f" ]] && dirname "$f"
}

rotate_project_dir_from_cwd(){
  local d="${1:-$PWD}"
  printf '%s/.claude/projects/%s' "$HOME" "$(printf '%s' "$d" | sed 's#/#-#g')"
}

# Per-session launch lock (prevents a duplicate same-name session racing the successor).
rotate_lock_path(){ printf '%s/.cache/claude-rotate-%s.lock' "$HOME" "${1:?name}"; }
