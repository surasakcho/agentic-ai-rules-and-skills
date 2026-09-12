#!/usr/bin/env bash
# session-preflight.sh -- everything between "the launcher said started" and "the session works".
#
# Reports EVERY blocker in one pass. The failure this exists for is serial discovery: six
# defects found one restart at a time, each invisible until the previous was fixed.
#
# Read-only. Never fixes, never launches, never recreates a container.
#
#   session-preflight.sh <repo-dir> [--sessions-conf <file>]
#
# Exit 0 = launchable (warnings may still be printed). Exit 1 = at least one blocker.
# Exit 2 = cannot check (bad arguments, no .claude-session).
set -uo pipefail

BLOCKERS=0
WARNINGS=0
CHECKED=0

red()  { printf '\033[31m%s\033[0m\n' "$*"; }
ylw()  { printf '\033[33m%s\033[0m\n' "$*"; }
grn()  { printf '\033[32m%s\033[0m\n' "$*"; }

block() { red   "  BLOCKER  $1"; [ -n "${2:-}" ] && printf '           → %s\n' "$2"; BLOCKERS=$((BLOCKERS+1)); }
warn()  { ylw   "  warning  $1"; [ -n "${2:-}" ] && printf '           → %s\n' "$2"; WARNINGS=$((WARNINGS+1)); }
ok()    { grn   "  ok       $1"; }
note()  { printf '           %s\n' "$1"; }
count() { CHECKED=$((CHECKED+1)); }

finish() {
  echo
  printf 'checked %d · %d blocker(s) · %d warning(s)\n' "$CHECKED" "$BLOCKERS" "$WARNINGS"
  if [ "$BLOCKERS" -gt 0 ]; then
    echo "NOT launchable. Fix the blockers above -- all of them, in one pass."
    exit 1
  fi
  echo "launchable. Warnings are not gates; read them anyway."
  exit 0
}

# Applies to host and container sessions alike. A session already running holds the context
# it started with, so rules adopted after launch do not reach it until it restarts.
check_shared_rules() {
  count
  if grep -q 'shared-lessons:begin' "$REPO/CLAUDE.md" 2>/dev/null; then
    ok "CLAUDE.md carries a shared-lessons block"
  else
    warn "no shared-lessons block in $REPO/CLAUDE.md" \
         "run retrieve-lessons BEFORE the session starts, so it opens with the rules in context"
  fi
}

REPO=""
SESSIONS_CONF="${HOME}/projects/zkyhax-svr-config/claude/sessions.conf"
while [ $# -gt 0 ]; do
  case "$1" in
    --sessions-conf) SESSIONS_CONF="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) REPO="$1"; shift ;;
  esac
done

[ -n "$REPO" ] || { echo "usage: session-preflight.sh <repo-dir> [--sessions-conf <file>]" >&2; exit 2; }
REPO="${REPO%/}"
[ -d "$REPO" ] || { echo "no such directory: $REPO" >&2; exit 2; }

DECL="$REPO/.claude-session"
echo
echo "session preflight: $REPO"
echo

# ---------------------------------------------------------------- 1. the declaration
# A repo that does not declare its target gets one guessed, and the guess is the host --
# which is the most privileged thing on the machine. That decision is never implicit.
if [ ! -f "$DECL" ]; then
  count; block "no .claude-session in $REPO" \
    "decide container vs host WITH the operator, then write it. A missing declaration defaults to the host by accident."
  echo; echo "cannot check further without a declaration."; exit 1
fi
count; ok ".claude-session present"

# Parse conservatively: KEY=VALUE, ignore comments and inline trailing comments.
declare -A D=()
while IFS= read -r line; do
  line="${line%%#*}"
  line="$(printf '%s' "$line" | sed 's/[[:space:]]*$//; s/^[[:space:]]*//')"
  [ -z "$line" ] && continue
  case "$line" in *=*) D["${line%%=*}"]="${line#*=}" ;; esac
done < "$DECL"

# ---------------------------------------------------------------- 2. key names
# A typo'd key is silent: the launcher reads nothing and the session registers under an
# auto-generated name that cannot be found from a phone.
for wrong in rc-name rc_name remote-control tmux-name workdir-path; do
  if [ -n "${D[$wrong]:-}" ]; then
    count; block "unknown key '$wrong=' in .claude-session" \
      "the reader looks for rc=/tmux=/workdir=. An unknown key is ignored SILENTLY -- nothing errors."
  fi
done

TARGET="${D[target]:-}"
RC="${D[rc]:-}"
TMUXN="${D[tmux]:-$RC}"
CONTAINER="${D[container]:-}"
WORKDIR="${D[workdir]:-}"

count
case "$TARGET" in
  container|host) ok "target=$TARGET" ;;
  "") block "target= not set" "container | host. This decides what the session can read." ;;
  *)  block "target='$TARGET' is not container or host" "container | host" ;;
esac

count
if [ -z "$RC" ]; then
  block "rc= not set" "without --remote-control the session registers as e.g. 'witty-hare' and is unfindable from a phone"
else
  ok "rc=$RC"
fi

# ---------------------------------------------------------------- 3. name collisions
# An rc name already in use is the failure that looks like "it never started".
if [ -n "$RC" ]; then
  count
  if tmux has-session -t "$TMUXN" 2>/dev/null; then
    warn "tmux session '$TMUXN' is already live" "launching again would overwrite it; stop it first or confirm deliberately"
  else
    ok "tmux name '$TMUXN' is free"
  fi

  if [ -f "$SESSIONS_CONF" ]; then
    count
    # Pipe-delimited rows: name | compose | service | container | profile | workdir | model | rc | perm
    # Count rows whose rc FIELD equals this rc -- not rows merely CONTAINING the string, which
    # matches the session's own row and reports every correct config as a collision.
    hits="$(awk -F'|' -v rc="$RC" '
        /^[[:space:]]*#/ {next} NF < 8 {next}
        { gsub(/^[[:space:]]+|[[:space:]]+$/, "", $8); gsub(/^[[:space:]]+|[[:space:]]+$/, "", $1)
          if ($8 == rc) print $1 }' "$SESSIONS_CONF" | sort -u)"
    n="$(printf '%s' "$hits" | grep -c . || true)"
    if [ "$n" -gt 1 ]; then
      warn "rc name '$RC' is claimed by $n rows: $(echo "$hits" | tr '\n' ' ')" \
           "two sessions answering to one name is a session you cannot address"
    elif [ "$n" -eq 1 ]; then
      ok "rc name '$RC' is declared once (row '$hits')"
    else
      warn "rc name '$RC' has no row in $(basename "$SESSIONS_CONF")" \
           "the managed launcher will not know this session; add a row"
    fi
  fi
fi

# ---------------------------------------------------------------- 4. host target
if [ "$TARGET" = "host" ]; then
  count; warn "host session -- reads ~/.ssh, all of ~/secrets/ and every repo, uncapped" \
    "confirm this is intended; a container session sees only its own mounts"
  check_shared_rules
  finish
fi

# An UNRESOLVED target is not a container target. Falling through to the container checks
# reports "container= not set" as though container had been chosen -- a second finding
# manufactured by the first, which is how a blocker list stops being trustworthy.
if [ "$TARGET" != "container" ]; then
  check_shared_rules
  note "target unresolved -- container checks skipped. Fix target= and run again."
  finish
fi

# ---------------------------------------------------------------- 5. container exists
count
if [ -z "$CONTAINER" ]; then
  block "target=container but container= not set" "name the container the session execs into"
  check_shared_rules; finish
fi

DOCKER="docker"
if ! docker info >/dev/null 2>&1; then
  if sg docker -c 'docker info' >/dev/null 2>&1; then
    DOCKER="sg docker -c"
  else
    echo "  cannot reach docker; skipping every container-side check." >&2
    echo; printf 'checked %d · %d blocker(s) · %d warning(s) · CONTAINER CHECKS SKIPPED\n' "$CHECKED" "$BLOCKERS" "$WARNINGS"
    exit 2
  fi
fi
dex() { if [ "$DOCKER" = "docker" ]; then docker "$@"; else sg docker -c "docker $*"; fi; }

if ! dex ps --format '{{.Names}}' 2>/dev/null | grep -qx "$CONTAINER"; then
  block "container '$CONTAINER' is not running" "start the stack first; every check below needs it up"
  check_shared_rules; finish
fi
ok "container '$CONTAINER' is up"

# The uid the session actually runs as. Everything below is judged against THIS, not against
# whoever owns the files on the host.
UID_IN="$(dex exec "$CONTAINER" id -u 2>/dev/null | tr -d '\r')"
[ -n "$UID_IN" ] || UID_IN=0
note "container runs as uid $UID_IN"

# ---------------------------------------------------------------- 6. the workdir is mounted
# A workdir that exists in the declaration and nowhere in the container is the defect that
# presents as the session starting in the wrong place, or not at all.
count
if [ -z "$WORKDIR" ]; then
  block "target=container but workdir= not set" "the path INSIDE the container, e.g. /app/<repo>"
elif dex exec "$CONTAINER" test -d "$WORKDIR" 2>/dev/null; then
  ok "workdir $WORKDIR exists in the container"
  count
  if dex exec "$CONTAINER" test -e "$WORKDIR/.claude-session" 2>/dev/null; then
    ok "workdir is this repo (its .claude-session is visible inside)"
  else
    warn "$WORKDIR is mounted but does not look like this repo" \
         "no .claude-session inside -- check the bind mount points at $REPO"
  fi
else
  block "workdir $WORKDIR does not exist inside '$CONTAINER'" \
        "add a bind mount for this repo, or fix workdir=. Declared-but-unmounted is silent at launch."
fi

# ---------------------------------------------------------------- 7. HOME and its ownership
HOME_IN="$(dex exec "$CONTAINER" sh -c 'echo $HOME' 2>/dev/null | tr -d '\r')"
[ -n "$HOME_IN" ] || HOME_IN="/home/app"
note "container HOME is $HOME_IN"

# THE check this tool exists for. Docker creates a missing bind-mount source as ROOT; a
# container running as 1000 then cannot write its own ~/.claude, and Claude Code parks on the
# login picker forever with nothing in any log. Ownership bits on the host are NOT the test --
# the mount, the uid and the mode all have to line up, so execute it.
count
if dex exec "$CONTAINER" sh -c "touch $HOME_IN/.claude/.preflight-probe 2>/dev/null && rm -f $HOME_IN/.claude/.preflight-probe" 2>/dev/null; then
  ok "$HOME_IN/.claude is writable by uid $UID_IN"
else
  block "$HOME_IN/.claude is NOT writable by uid $UID_IN" \
        "usually docker created the home mount itself, so it is root-owned. Pre-create the host directory as the operator BEFORE the first up, then recreate."
  note "this one cannot be fixed by logging in -- there is nowhere to write the credential"
fi

# ---------------------------------------------------------------- 8. authentication
# Two files, and only the first is obvious. The credential alone still lands on the login
# picker, because the picker is driven by oauthAccount/hasCompletedOnboarding in .claude.json.
count
if dex exec "$CONTAINER" test -s "$HOME_IN/.claude/.credentials.json" 2>/dev/null; then
  ok "credential present"
else
  block "no $HOME_IN/.claude/.credentials.json -- this home is unauthenticated" \
        "log in once via tmux attach (survives container recreation), or have the operator place one. Never copy one yourself."
fi

count
if dex exec "$CONTAINER" test -s "$HOME_IN/.claude.json" 2>/dev/null; then
  if dex exec "$CONTAINER" grep -q '"oauthAccount"' "$HOME_IN/.claude.json" 2>/dev/null; then
    ok ".claude.json carries oauthAccount"
  else
    block ".claude.json has no oauthAccount -- the session will show the LOGIN PICKER" \
          "a credential file alone is not enough; the picker is driven by this file, not that one"
  fi
else
  warn "no $HOME_IN/.claude.json" "first run will show onboarding (theme, then login, then trust)"
fi

# ---------------------------------------------------------------- 9. --continue safety
# --continue with nothing to continue prints "No conversation found to continue" and EXITS,
# which a restart loop then retries every few seconds forever.
count
SLUG="$(printf '%s' "$WORKDIR" | sed 's|/|-|g')"
if dex exec "$CONTAINER" sh -c "ls $HOME_IN/.claude/projects/$SLUG/*.jsonl >/dev/null 2>&1" 2>/dev/null; then
  ok "prior conversation exists -- --continue is safe"
else
  note "no prior conversation for $WORKDIR; the launcher must start FRESH, not --continue"
fi

# ---------------------------------------------------------------- 10. shared rules
check_shared_rules

finish
