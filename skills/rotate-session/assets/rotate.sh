#!/usr/bin/env bash
# rotate.sh --preflight          -> run all safety checks, print PASS/FAIL, take NO action
# rotate.sh --dry-run <sha>      -> print exactly what the real run would do; change nothing
# rotate.sh <predecessor_sha>    -> make the successor come up FRESH, then guarded self-end
#
# The Claude-driven steps (handoff note -> /wrap) run BEFORE this script, from SKILL.md. This script
# is ONLY the irreversible mechanical half.
#
# ORDER IS THE CORRECTNESS GUARANTEE. It differs by mode, and in both the rule is the same: the
# successor's path must be secured BEFORE the predecessor is ended, so a failure leaves the
# predecessor alive rather than opening a coverage gap.
#
#   MODE=tmux       schedule the successor (systemd-run --user, detached so it survives our death),
#                   THEN self-kill.
#
#   MODE=container  the successor is ALREADY guaranteed: the host restart loop relaunches
#                   `docker exec ... claude --continue ...` ~3s after claude exits. What is NOT
#                   guaranteed is that it comes up FRESH — `--continue` is baked into the host
#                   loop's command line and we cannot change it from in here. Left alone, a rotation
#                   would resume this same saturated conversation and silently accomplish nothing.
#                   So the container work is: seed a fresh, near-empty conversation for this project
#                   dir, move the old transcripts out of the way so `--continue` cannot reach them,
#                   verify, THEN end our own process. If the seed fails, nothing is moved and
#                   nothing is killed.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/rotate-env.sh"

REPO_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
CONF="$REPO_DIR/.claude/rotate.conf"
MODE="$(rotate_mode)"
CURRENT="$(rotate_current_session)"

fail(){ ROTATE_LOG "PREFLIGHT FAIL: $*"; exit 1; }

# --- activation gate: a committed .claude/rotate.conf is what activates a repo ---
[[ -f "$CONF" ]] || fail "no .claude/rotate.conf in $REPO_DIR — rotation NOT activated for this repo (only activated repos rotate)."
# shellcheck disable=SC1090
source "$CONF"
: "${SESSION:?rotate.conf missing SESSION}"
MODEL="${MODEL:-}"; EFFORT="${EFFORT:-}"; RC_NAME="${RC_NAME:-$SESSION}"
PERMISSION_MODE="${PERMISSION_MODE:-}"; DELAY="${DELAY:-60}"; BOOTSTRAP_EXTRA="${BOOTSTRAP_EXTRA:-}"
SUCCESSOR="${SUCCESSOR:-}"; SEED_MODEL="${SEED_MODEL:-haiku}"
REPO_DIR="${REPO_DIR_OVERRIDE:-$REPO_DIR}"

[[ "$MODE" != "unknown" ]] || fail "cannot tell what kind of session this is — no tmux session, and not a container session with an identifiable claude process. Rotation needs to know what 'this session' means before it ends anything."

# --- THE GUARD: the config's SESSION must be THIS live session (self-rotation only) ---
rotate_assert_self "$SESSION" || fail "config SESSION='$SESSION' is not the current session '$CURRENT' — refusing."
[[ "$DELAY" =~ ^[0-9]+$ ]] || fail "DELAY '$DELAY' is not an integer."

# --- mode-specific preconditions --------------------------------------------------------------
PROJ_DIR=""; LIVE_JSONL=""
if [[ "$MODE" == "tmux" ]]; then
  command -v tmux >/dev/null 2>&1        || fail "tmux missing."
  command -v systemd-run >/dev/null 2>&1 || fail "systemd-run missing (needed to detach the successor)."
else
  # A container session cannot start its own successor. It relies on the host restart loop, which
  # it cannot see from in here. So the operator ASSERTS it, once, in a committed file — and we
  # refuse until they have. An unasserted rotation here is not a rotation, it is a session that
  # ends and never comes back.
  [[ "$SUCCESSOR" == "host-restart-loop" ]] || fail \
"this is a CONTAINER session and rotate.conf does not assert SUCCESSOR=host-restart-loop.
    Nothing in here can see the host, so the restart loop cannot be verified from inside the
    container — and ending this session without one kills it permanently.
    Verify it on the HOST, once:
        tmux list-panes -a -F '#{session_name} :: #{pane_start_command}' | grep '$SESSION'
    The pane command must be a 'while true; do docker exec ... claude ...; sleep 3; done' loop.
    Then set SUCCESSOR=host-restart-loop in $CONF and commit it."
  command -v claude >/dev/null 2>&1 || fail "the 'claude' CLI is not on PATH — needed to seed the successor's fresh conversation."
  # The transcript store, derived two independent ways; they must agree.
  PROJ_DIR="$(rotate_project_dir_from_live)"
  local_from_cwd="$(rotate_project_dir_from_cwd "$REPO_DIR")"
  [[ -n "$PROJ_DIR" ]] || fail "could not locate this session's own transcript under ~/.claude/projects (CLAUDE_CODE_SESSION_ID=${CLAUDE_CODE_SESSION_ID:-unset})."
  [[ "$PROJ_DIR" == "$local_from_cwd" ]] || fail \
"transcript-store mismatch: this session's transcripts live in '$PROJ_DIR' but the repo '$REPO_DIR' maps to '$local_from_cwd'.
    The host restart loop launches with -w <workdir>, so it will read '$local_from_cwd'. Run this from the session's own workdir."
  [[ -w "$PROJ_DIR" ]] || fail "transcript store '$PROJ_DIR' is not writable."
  LIVE_JSONL="$PROJ_DIR/${CLAUDE_CODE_SESSION_ID:-nonexistent}.jsonl"
  [[ -f "$LIVE_JSONL" ]] || fail "this session's own transcript '$LIVE_JSONL' not found — refusing to touch a store I cannot account for."
fi

# --- the repo is the memory: it must be committed AND pushed before the conversation is discarded
git_state_ok(){
  local why="" dirty
  dirty="$(git -C "$REPO_DIR" status --porcelain 2>/dev/null)"
  if [[ -n "$dirty" ]]; then
    # Name the files. A gate that fires without saying what tripped it gets worked around rather
    # than fixed, and an untracked machine-local file (.claude/settings.local.json and friends)
    # will otherwise block every rotation with an error that sounds like lost work.
    why="uncommitted changes: $(printf '%s' "$dirty" | awk '{printf "%s%s", sep, $0; sep="; "}' | cut -c1-300)"
  fi
  local ahead; ahead="$(git -C "$REPO_DIR" rev-list --count '@{upstream}..HEAD' 2>/dev/null || echo unknown)"
  if [[ "$ahead" == "unknown" ]]; then why="${why:+$why; }no upstream branch to compare against"
  elif [[ "$ahead" != "0" ]]; then why="${why:+$why; }$ahead commit(s) not pushed"; fi
  [[ -z "$why" ]] || { printf '%s' "$why"; return 1; }
  return 0
}

if [[ "${1:-}" == "--preflight" ]]; then
  if [[ "$MODE" == "tmux" ]]; then
    tmux has-session -t "$SESSION" 2>/dev/null || ROTATE_LOG "note: 'tmux has-session $SESSION' false (unexpected while inside it)."
    loginctl show-user "$USER" 2>/dev/null | grep -q 'Linger=yes' \
      || ROTATE_LOG "WARN: user linger is OFF — a successor scheduled near logout may not fire (loginctl enable-linger $USER)."
  else
    ROTATE_LOG "note: container mode — successor is the host restart loop (asserted in rotate.conf, not verifiable from in here)."
    ROTATE_LOG "note: transcript store $PROJ_DIR ($(ls -1 "$PROJ_DIR"/*.jsonl 2>/dev/null | wc -l) conversation(s)); live = $(basename "$LIVE_JSONL")."
  fi
  if ! reason="$(git_state_ok)"; then
    ROTATE_LOG "WARN: repo not clean/pushed ($reason). The real run will REFUSE — the conversation is discarded, so the repo must already hold everything."
  fi
  ROTATE_LOG "PREFLIGHT PASS: self-rotation of '$SESSION' permitted (mode=$MODE, repo=$REPO_DIR, rc=$RC_NAME)."
  exit 0
fi

DRY=0
if [[ "${1:-}" == "--dry-run" ]]; then DRY=1; shift; fi
SHA="${1:-unknown}"

# 1. Successor bootstrap — SHA dual-check per e-biz-factory/docs/auto-resume-design.md.
BOOTSTRAP="You are the REFRESHED successor for session '$SESSION'. Read the committed handoff note (CONTEXT.md or HANDOFF.md '## Next Session', or TODO.md). Run 'git fetch' and CONFIRM predecessor commit $SHA is present before proceeding. Then reply in ONE short line confirming you are the fresh successor and stating the next step. Do nothing else until instructed.${BOOTSTRAP_EXTRA:+ $BOOTSTRAP_EXTRA}"

# 2. The repo must already hold the work. Checked here, not left to the model.
#    A dry run REPORTS the refusal instead of exiting on it — the point of a dry run is to show the
#    whole plan, and a dirty tree at planning time is normal.
if ! reason="$(git_state_ok)"; then
  if [[ "$DRY" == "1" ]]; then
    ROTATE_LOG "DRY-RUN: the real run would REFUSE here — $reason in $REPO_DIR. Continuing the plan anyway."
  else
    ROTATE_LOG "FATAL: $reason in $REPO_DIR. The conversation is about to be discarded and the repo is the only memory. Commit and push first — NOT rotating."
    exit 1
  fi
fi

if [[ "$MODE" == "tmux" ]]; then
  # --- host session: schedule the successor (detached; survives our death), then self-kill -------
  LAUNCH="$HERE/rotate-launch.sh"
  UNIT="claude-rotate-succ-${SESSION}-$(date +%s)"
  if [[ "$DRY" == "1" ]]; then
    ROTATE_LOG "DRY-RUN: would schedule unit '$UNIT' (+${DELAY}s) -> $LAUNCH '$SESSION' '$REPO_DIR' '$MODEL' '$EFFORT' '$RC_NAME' '$PERMISSION_MODE' <bootstrap>"
    ROTATE_LOG "DRY-RUN: would then kill tmux session '$SESSION'. Nothing changed."
    exit 0
  fi
  if systemd-run --user --setenv=PATH="$PATH" --on-active="${DELAY}s" --unit="$UNIT" \
       "$LAUNCH" "$SESSION" "$REPO_DIR" "$MODEL" "$EFFORT" "$RC_NAME" "$PERMISSION_MODE" "$BOOTSTRAP" >/dev/null 2>&1; then
    ROTATE_LOG "successor scheduled: unit '$UNIT' fires in ${DELAY}s -> rotate-launch '$SESSION'."
  else
    ROTATE_LOG "FATAL: could not schedule successor (systemd --user / linger?) — NOT killing predecessor."
    exit 1
  fi
  ROTATE_LOG "killing predecessor '$SESSION' now (successor appears in ~${DELAY}s)."
  rotate_kill "$SESSION"
  ROTATE_LOG "rotation initiated. Watch: claude.ai/code -> '$SESSION' reappears fresh in ~${DELAY}s."
  exit 0
fi

# --- container session --------------------------------------------------------------------------
# The host loop will relaunch `claude --continue`. `--continue` resumes the most recent conversation
# FOR THIS PROJECT DIR. So "come up fresh" means: leave it exactly one conversation to continue, and
# make that one brand new. Both halves matter — leaving it ZERO is worse than leaving it the old
# one, because interactive `claude --continue` with nothing to continue prints
# "No conversation found to continue" and EXITS, and the 3-second restart loop then spins forever.

STAMP="$(date +%Y%m%d-%H%M%S)"
ARCHIVE="$HOME/.claude/rotate-archive/$(basename "$PROJ_DIR")/$STAMP"
before="$(ls -1 "$PROJ_DIR"/*.jsonl 2>/dev/null | sort || true)"

if [[ "$DRY" == "1" ]]; then
  ROTATE_LOG "DRY-RUN: mode=container session='$SESSION' pid=$(rotate_claude_pid) repo=$REPO_DIR"
  ROTATE_LOG "DRY-RUN: would seed a fresh conversation:  (cd $REPO_DIR && claude -p --model $SEED_MODEL <bootstrap>)"
  ROTATE_LOG "DRY-RUN: bootstrap = $BOOTSTRAP"
  ROTATE_LOG "DRY-RUN: would then move these transcript(s) to $ARCHIVE :"
  printf '%s\n' "$before" | sed 's/^/                                   /' >&2
  ROTATE_LOG "DRY-RUN: would verify the seed is the ONLY conversation left, then end pid $(rotate_claude_pid)."
  ROTATE_LOG "DRY-RUN: nothing changed."
  exit 0
fi

# 3. Seed the successor's fresh conversation. This runs as a separate, non-nested claude: the
#    CLAUDE_CODE_* variables of THIS session must not leak into it or it will not be a new one.
ROTATE_LOG "seeding a fresh conversation for '$PROJ_DIR' (model=$SEED_MODEL)..."
seed_out="$(cd "$REPO_DIR" && env -u CLAUDE_CODE_SESSION_ID -u CLAUDE_CODE_CHILD_SESSION \
      -u CLAUDE_CODE_BRIDGE_SESSION_ID -u CLAUDE_CODE_MESSAGING_SOCKET -u CLAUDE_CODE_MESSAGING_TOKEN \
      -u CLAUDECODE -u CLAUDE_PID \
      timeout 180 claude -p --model "$SEED_MODEL" "$BOOTSTRAP" 2>&1 | tail -3 || true)"

after="$(ls -1 "$PROJ_DIR"/*.jsonl 2>/dev/null | sort || true)"
SEED="$(comm -13 <(printf '%s\n' "$before") <(printf '%s\n' "$after") | head -1)"
if [[ -z "$SEED" || ! -f "$SEED" ]]; then
  ROTATE_LOG "FATAL: seeding produced no new conversation in $PROJ_DIR — NOT archiving, NOT ending this session."
  ROTATE_LOG "       claude -p said: $seed_out"
  exit 1
fi
ROTATE_LOG "seed = $(basename "$SEED") ($(wc -c < "$SEED") bytes). The successor's --continue will land here."

# 4. Move every OTHER conversation out of reach of --continue. Archived, not deleted: a rotation
#    that goes wrong must be recoverable, and the old conversation is the only copy of it.
mkdir -p "$ARCHIVE"
moved=0
for f in "$PROJ_DIR"/*.jsonl; do
  [[ -e "$f" ]] || continue
  [[ "$f" == "$SEED" ]] && continue
  mv "$f" "$ARCHIVE/" && moved=$((moved+1))
done
ROTATE_LOG "archived $moved conversation(s) -> $ARCHIVE"

# 5. Verify: exactly one conversation left, and it is the seed. This is the last point of no return.
left="$(ls -1 "$PROJ_DIR"/*.jsonl 2>/dev/null | wc -l)"
if [[ "$left" != "1" || ! -f "$SEED" ]]; then
  ROTATE_LOG "FATAL: after archiving, $PROJ_DIR holds $left conversation(s), expected exactly 1 (the seed) — NOT ending this session."
  ROTATE_LOG "       restore with: mv '$ARCHIVE'/*.jsonl '$PROJ_DIR'/"
  exit 1
fi

# The rotation log survives us; the pane output does not (we are about to end the process writing it).
{
  echo "rotated:        $STAMP"
  echo "session:        $SESSION   (mode=container, rc=$RC_NAME)"
  echo "repo:           $REPO_DIR"
  echo "predecessor sha:$SHA"
  echo "seed:           $SEED"
  echo "archived:       $moved conversation(s) in $ARCHIVE"
  echo "restore:        mv '$ARCHIVE'/*.jsonl '$PROJ_DIR'/    # then relaunch and --resume <uuid>"
  echo "if no successor appears: the host restart loop was not there. Relaunch on the HOST with"
  echo "                claude-session.sh start $SESSION"
} > "$ARCHIVE/rotate.log"
ROTATE_LOG "wrote $ARCHIVE/rotate.log (recovery instructions survive this session)."

# 6. Guarded self-end LAST (irreversible). The successor is the host loop, already running.
#    Final sweep: our own claude may have appended to its transcript path since step 4.
for f in "$PROJ_DIR"/*.jsonl; do
  [[ -e "$f" && "$f" != "$SEED" ]] && mv "$f" "$ARCHIVE/" 2>/dev/null || true
done
ROTATE_LOG "ending '$SESSION' now; the host loop relaunches it in ~3s, fresh."
rotate_kill "$SESSION"
