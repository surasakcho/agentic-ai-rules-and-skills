#!/usr/bin/env python3
"""SessionStart hook — put the repo's rules in context before the first reply.

Wire it in settings.json:

    "hooks": { "SessionStart": [ { "hooks": [ {
        "type": "command",
        "command": "<this file>",
        "timeout": 20 } ] } ] }

WHY A HOOK AND NOT A HABIT. The adopted block in CLAUDE.md is a list of links, and a rule that
is a URL is not in front of you at the moment it applies. Measured in this estate: a rule was
adopted, pinned, read during retrieval and quoted back to the operator, and was then broken in
the very repo whose CLAUDE.md links it. Reading the digest ON DEMAND requires remembering to,
which is the thing that already failed. `prose < checklist < test < gate`.

NEVER BLOCKS. Every failure path prints valid JSON and exits 0. A hook that can stop a session
starting is worse than a session that starts without its rules in context.
"""
import json
import os
import subprocess
import sys

# realpath: this is invoked through ~/.claude/skills/<skill>/assets/, a symlink.
HERE = os.path.dirname(os.path.realpath(__file__))
DIGEST = os.path.join(HERE, "..", "rules_in_force.py")

# Roughly 4 chars per token. The full digest measured 12-19 KB on real repos (~3-4.6k tokens,
# about 1% of a 400k window) -- affordable, and the whole point is the statements rather than
# the names. The cap exists for the repo that adopts far more than any seen so far.
MAX_CHARS = 60000


def emit(context):
    """The only exit path. Anything else would risk blocking a session start."""
    if context:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }))
    else:
        print("{}")
    sys.exit(0)


def find_repo(start):
    """Nearest ancestor holding a CLAUDE.md; fall back to the git root."""
    d = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(d, "CLAUDE.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    r = subprocess.run(["git", "-C", start, "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        payload = {}

    cwd = payload.get("cwd") or os.getcwd()
    repo = find_repo(cwd)
    if not repo:
        emit(None)

    if not os.path.isfile(DIGEST):
        emit(None)

    try:
        p = subprocess.run([sys.executable, "-X", "utf8", DIGEST, "--repo", repo],
                           capture_output=True, text=True, timeout=15)
    except Exception:
        emit(None)

    out = (p.stdout or "").strip()

    # Exit 1 means "nothing adopted" -- a real state, and worth saying once rather than
    # injecting silence. A repo bound by nothing written down should say so at the top of the
    # session, not be indistinguishable from one whose rules simply failed to load.
    if p.returncode == 1:
        emit("This repo has no adopted shared-rules block in CLAUDE.md. "
             "Consider running the retrieve-lessons skill before starting work.")

    if p.returncode != 0 or not out:
        emit(None)

    if len(out) > MAX_CHARS:
        out = out[:MAX_CHARS] + (
            "\n\n[TRUNCATED — this digest exceeded the injection cap. Run "
            "rules-in-force yourself for the rest; do NOT assume the remainder is empty.]")

    emit(
        "The working rules in force for this repo, injected at session start because a rule "
        "that is only a URL in CLAUDE.md is not in front of you at the moment it applies. "
        "Each statement below is verbatim from its rule file at the commit this repo pinned. "
        "Local rules win on conflict with shared ones. Follow these; do not merely cite them.\n\n"
        + out
    )


if __name__ == "__main__":
    main()
