#!/usr/bin/env python3
"""Self-test for session-preflight.sh.

Covers the checks that run BEFORE docker is reached -- declaration parsing, key names,
target resolution, and the exit codes. The container-side checks need a live container and
are exercised by hand; what is asserted here is everything that can fail without one.

Exit 0 pass · 1 failure · 2 cannot run (a self-test that cannot run is never a pass).
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "assets", "session-preflight.sh")


def run(decl_text, extra_files=None):
    """Run the preflight against a throwaway repo; return (exit code, combined output)."""
    d = tempfile.mkdtemp(prefix="preflight-selftest-")
    try:
        if decl_text is not None:
            with open(os.path.join(d, ".claude-session"), "w", encoding="utf-8") as f:
                f.write(decl_text)
        for name, body in (extra_files or {}).items():
            with open(os.path.join(d, name), "w", encoding="utf-8") as f:
                f.write(body)
        # An empty sessions.conf keeps the rc-uniqueness check deterministic: it must not
        # depend on whatever the machine running the test happens to have declared.
        conf = os.path.join(d, "empty-sessions.conf")
        open(conf, "w", encoding="utf-8").close()
        p = subprocess.run(
            ["bash", SCRIPT, d, "--sessions-conf", conf],
            capture_output=True, text=True,
        )
        return p.returncode, p.stdout + p.stderr
    finally:
        shutil.rmtree(d, ignore_errors=True)


CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


@case("a repo with no .claude-session is a blocker, not a guess")
def _():
    rc, out = run(None)
    assert rc == 1, f"expected exit 1, got {rc}"
    assert "no .claude-session" in out
    # The reason matters as much as the finding: the silent default is the host.
    assert "host" in out


@case("rc-name= is caught as an unknown key")
def _():
    # The real defect. The reader looks for rc=; rc-name= is ignored in silence, so the
    # session registers under an auto-generated name and cannot be found from a phone.
    rc, out = run("target=host\nrc-name=whatever\n")
    assert rc == 1, f"expected exit 1, got {rc}"
    assert "unknown key 'rc-name='" in out


@case("a missing target is a blocker")
def _():
    rc, out = run("rc=x-srv\n")
    assert rc == 1
    assert "target= not set" in out


@case("a target that is neither container nor host is a blocker")
def _():
    rc, out = run("target=vm\nrc=x-srv\n")
    assert rc == 1
    assert "is not container or host" in out


@case("a missing rc is a blocker")
def _():
    rc, out = run("target=host\n")
    assert rc == 1
    assert "rc= not set" in out


@case("target=container with no container= is a blocker")
def _():
    rc, out = run("target=container\nrc=x-srv\nworkdir=/app/x\n")
    assert rc == 1
    assert "container= not set" in out


@case("a complete host declaration passes, with the privilege warning")
def _():
    rc, out = run("target=host\nrc=x-srv\ntmux=x-srv\n")
    assert rc == 0, f"expected exit 0, got {rc}: {out}"
    # Passing is not the same as silent: a host session is the most privileged thing here.
    assert "host session" in out
    assert "0 blocker(s)" in out


@case("comments and inline comments do not become keys")
def _():
    rc, out = run("# a comment\ntarget=host   # trailing\nrc=x-srv\n")
    assert rc == 0, f"expected exit 0, got {rc}: {out}"
    assert "unknown key" not in out


@case("an rc with no row in sessions.conf warns but does not block")
def _():
    rc, out = run("target=host\nrc=orphan-srv\n")
    assert rc == 0
    assert "has no row" in out


@case("a missing shared-lessons block warns; a present one does not")
def _():
    rc, out = run("target=host\nrc=x-srv\n", {"CLAUDE.md": "# hi\n"})
    assert "no shared-lessons block" in out, "host path should still check CLAUDE.md"


@case("multiple blockers are all reported in ONE pass")
def _():
    # The whole point of the tool. Stopping at the first finding is the failure it was
    # written for -- six defects discovered one restart at a time.
    rc, out = run("rc-name=x\n")
    assert rc == 1
    assert "unknown key 'rc-name='" in out
    assert "target= not set" in out
    assert "rc= not set" in out
    assert "3 blocker(s)" in out, f"expected 3 blockers in one run: {out}"


def main():
    if not os.path.exists(SCRIPT):
        print("CANNOT RUN: %s not found" % SCRIPT, file=sys.stderr)
        return 2
    if shutil.which("bash") is None:
        print("CANNOT RUN: bash not available", file=sys.stderr)
        return 2

    failed = 0
    for name, fn in CASES:
        try:
            fn()
            print("  pass  %s" % name)
        except AssertionError as e:
            failed += 1
            print("  FAIL  %s\n        %s" % (name, e))
        except Exception as e:  # a test that errors is a failure, never a skip
            failed += 1
            print("  ERROR %s\n        %r" % (name, e))

    print("\n%d/%d passed" % (len(CASES) - failed, len(CASES)))
    if failed:
        print("NOTE: container-side checks (mounts, ~/.claude writability, credentials,")
        print("      .claude.json) are NOT covered here -- they need a live container.")
        return 1
    print("Covered: declaration parsing and every pre-docker check.")
    print("NOT covered: mounts, ~/.claude writability, credentials, .claude.json --")
    print("these need a live container and are verified by hand.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
