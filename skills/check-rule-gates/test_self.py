#!/usr/bin/env python3
"""Self-test for check_rule_gates.py.

The cases come in PAIRS -- one that must fire and one that must not -- because
this tool's entire value is discrimination. It has to separate "declares a gate
that was never built" from "declares honestly that it cannot be gated" from
"could not be read", and a checker that cannot tell those apart is noise that
gets switched off.

The green cases matter at least as much as the red ones. A checker only ever
seen failing is as unproven as one only ever seen passing, and anyone adopting
this skill runs it against their own corpus first -- if it cannot demonstrate a
clean pass they will not trust its failures.

Every corpus here is synthetic and built in a temp directory. Nothing reads the
real corpus, so the test does not go green or red because the corpus changed.

Exit 0 pass - 1 failure - 2 cannot run.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.realpath(__file__))
SCRIPT = os.path.join(HERE, "check_rule_gates.py")

CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


def clause(**kv):
    body = "\n".join("%s: '%s'" % (k.replace("__", "_"), v) for k, v in kv.items())
    return "# A rule\n\nProse.\n\n## Enforcement\n\n```yaml\n%s\n```\n" % body


def run(rules, extra_files=(), args=()):
    """Build a throwaway corpus and run the checker over it. -> (rc, output)."""
    root = tempfile.mkdtemp()
    try:
        cdir = os.path.join(root, "rules", "cat")
        os.makedirs(cdir)
        for name, text in rules.items():
            with open(os.path.join(cdir, name), "w", encoding="utf-8") as fh:
                fh.write(text)
        for rel, text in extra_files:
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(text)
        cmd = [sys.executable, "-X", "utf8", SCRIPT,
               "--corpus", os.path.join(root, "rules")] + list(args)
        cmd = [c.replace("@ROOT@", root) for c in cmd]
        r = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
        return r.returncode, r.stdout + r.stderr
    finally:
        shutil.rmtree(root, ignore_errors=True)


def expect(rc, out, want_rc, want=(), unwanted=()):
    if rc != want_rc:
        return "exit %d, expected %d\n%s" % (rc, want_rc, out[-700:])
    for w in want:
        if w not in out:
            return "missing %r\n%s" % (w, out[-700:])
    for u in unwanted:
        if u in out:
            return "unexpected %r\n%s" % (u, out[-700:])
    return None


# --------------------------------------------------------------------------
# GREEN. The whole corpus is gated or honestly unavailable -> exit 0.
# --------------------------------------------------------------------------
@case("green: a resolvable implemented_by path is gated")
def _():
    rc, out = run(
        {"a.md": clause(verdict="deferred", observable="x", trigger="t",
                        check="c", escape="e",
                        implemented_by="tools/real-gate.py")},
        extra_files=[("tools/real-gate.py", "# a gate\n")])
    return expect(rc, out, 0, want=["gated: 1", "UNGATED: 0", "RULE GATES OK"])


@case("green: an irreducible verdict is unavailable, not a gap")
def _():
    rc, out = run({"a.md": clause(verdict="irreducible", observable="-",
                                  trigger="-", check="-", escape="-")})
    return expect(rc, out, 0, want=["unavailable: 1", "UNGATED: 0"])


@case("green: a declared gate id resolves without any file path")
def _():
    reg = "GATES = (\n    ('bulk-stage', f1),\n    ('force-push', f2),\n)\n"
    rc, out = run(
        {"a.md": clause(verdict="interposed", observable="x", trigger="t",
                        check="c", escape="e", implemented_by="bulk-stage")},
        extra_files=[("hooks/g.py", reg),
                     ("gates.conf",
                      "provider hookgates py-tuple hooks/g.py GATES\n")],
        args=["--config", "@ROOT@/gates.conf"])
    return expect(rc, out, 0, want=["gated: 1", "hookgates: bulk-stage"])


# --------------------------------------------------------------------------
# RED. A declared gate with nothing behind it -> exit 1.
# --------------------------------------------------------------------------
@case("red: a gateable verdict with no implemented_by is UNGATED")
def _():
    rc, out = run({"a.md": clause(verdict="interposed", observable="x",
                                  trigger="t", check="c", escape="e")})
    return expect(rc, out, 1, want=["UNGATED: 1", "RULE GATES FAILED"])


@case("red: implemented_by naming a path that does not exist is UNGATED")
def _():
    rc, out = run({"a.md": clause(verdict="deferred", observable="x",
                                  trigger="t", check="c", escape="e",
                                  implemented_by="tools/absent.py")})
    return expect(rc, out, 1, want=["UNGATED: 1", "MISSING"])


@case("a near-miss name is never counted as an implementation")
def _():
    # THE false positive that would matter most: a gate whose name merely looks
    # like the one the rule asks for. 'bulk-stage-v2' must not match the gate
    # 'bulk-stage'.
    #
    # It lands in UNKNOWN rather than UNGATED, and that is the designed answer,
    # not a miss. A bare token that is neither a path nor a DECLARED gate id
    # could be a gate in a source this run was never pointed at, or a typo --
    # undetermined is not absent. What must never happen is `gated`.
    reg = "GATES = (\n    ('bulk-stage', f1),\n)\n"
    rc, out = run(
        {"a.md": clause(verdict="interposed", observable="x", trigger="t",
                        check="c", escape="e",
                        implemented_by="bulk-stage-v2")},
        extra_files=[("hooks/g.py", reg),
                     ("gates.conf",
                      "provider hookgates py-tuple hooks/g.py GATES\n")],
        args=["--config", "@ROOT@/gates.conf"])
    return expect(rc, out, 2, want=["gated: 0", "UNKNOWN: 1"])


# --------------------------------------------------------------------------
# AMBER. Unreadable is its own answer -> exit 2, never folded into clean.
# --------------------------------------------------------------------------
@case("amber: a rule with no Enforcement clause is UNKNOWN, not UNGATED")
def _():
    rc, out = run({"a.md": "# A rule\n\nJust prose, no clause.\n"})
    return expect(rc, out, 2, want=["UNKNOWN: 1", "UNGATED: 0",
                                    "RULE GATES UNKNOWN"])


@case("amber: a prose implemented_by is UNKNOWN, not a false gap")
def _():
    rc, out = run({"a.md": clause(verdict="deferred", observable="x",
                                  trigger="t", check="c", escape="e",
                                  implemented_by="handled by the team")})
    return expect(rc, out, 2, want=["UNKNOWN: 1", "prose, not a locator"])


@case("amber: an unknown verdict word is UNKNOWN, not assumed gateable")
def _():
    rc, out = run({"a.md": clause(verdict="probably-fine", observable="x",
                                  trigger="t", check="c", escape="e")})
    return expect(rc, out, 2, want=["UNKNOWN: 1"])


@case("amber: an unreadable gate provider does not mark rules ungated")
def _():
    rc, out = run(
        {"a.md": clause(verdict="irreducible", observable="-", trigger="-",
                        check="-", escape="-")},
        extra_files=[("gates.conf",
                      "provider broken py-tuple hooks/absent.py GATES\n")],
        args=["--config", "@ROOT@/gates.conf"])
    return expect(rc, out, 2, want=["UNKNOWN: 1", "unreadable"],
                  unwanted=["UNGATED: 1"])


# --------------------------------------------------------------------------
# PRECEDENCE and REGRESSIONS.
# --------------------------------------------------------------------------
@case("a real gap outranks an unreadable one: exit 1, not 2")
def _():
    rc, out = run({"a.md": clause(verdict="interposed", observable="x",
                                  trigger="t", check="c", escape="e"),
                   "b.md": "# no clause\n"})
    return expect(rc, out, 1, want=["UNGATED: 1", "UNKNOWN: 1"])


@case("a configured root never displaces the corpus's own repo")
def _():
    # Regression: configured roots used to REPLACE the default, so declaring an
    # estate root made every in-corpus path dangle -- the run went redder as the
    # config got more complete.
    rc, out = run(
        {"a.md": clause(verdict="deferred", observable="x", trigger="t",
                        check="c", escape="e",
                        implemented_by="tools/real-gate.py")},
        extra_files=[("tools/real-gate.py", "# gate\n"),
                     ("gates.conf", "root estate .\n")],
        args=["--config", "@ROOT@/gates.conf"])
    return expect(rc, out, 0, want=["gated: 1"])


@case("a '#' inside a provider regex is not treated as a comment")
def _():
    # Regression: blanket '#' stripping truncated the one directive most likely
    # to need a '#' -- a regex matching commented gate headers.
    hook = "# GATE 1 -- pin is not stale\nbody\n# GATE 2 -- no survivor\n"
    conf = ("provider commitgates regex hooks/pre-commit "
            r"^#\s+GATE\s+[0-9]+\s+--\s+(.+)$" + "\n")
    rc, out = run(
        {"a.md": clause(verdict="deferred", observable="x", trigger="t",
                        check="c", escape="e",
                        implemented_by="pin is not stale")},
        extra_files=[("hooks/pre-commit", hook), ("gates.conf", conf)],
        args=["--config", "@ROOT@/gates.conf"])
    return expect(rc, out, 0, want=["gated: 1", "commitgates"])


@case("gates nothing claims are reported but never fail the run")
def _():
    reg = "GATES = (\n    ('orphan-gate', f1),\n)\n"
    rc, out = run(
        {"a.md": clause(verdict="irreducible", observable="-", trigger="-",
                        check="-", escape="-")},
        extra_files=[("hooks/g.py", reg),
                     ("gates.conf",
                      "provider hookgates py-tuple hooks/g.py GATES\n")],
        args=["--config", "@ROOT@/gates.conf"])
    return expect(rc, out, 0, want=["orphan-gate", "gates no rule claims"])


def main():
    if not os.path.exists(SCRIPT):
        print("CANNOT RUN: %s not found" % SCRIPT)
        return 2
    failed = 0
    for name, fn in CASES:
        try:
            err = fn()
        except Exception as exc:  # a crashing case is a failure, not a skip
            err = "raised %s: %s" % (type(exc).__name__, exc)
        if err:
            failed += 1
            print("FAIL  %s\n      %s" % (name, err.replace("\n", "\n      ")))
        else:
            print("ok    %s" % name)
    print("\n%d/%d passed" % (len(CASES) - failed, len(CASES)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
