#!/usr/bin/env python3
"""Self-test for stale-claim-check.py.

Every case below pins a regression this tool's own docstring records as having really
happened. The checker's whole value is discrimination — flagging an ASSERTION while leaving a
DISCUSSION alone — so the tests come in pairs: one that must fire and one that must not.

Exit 0 pass · 1 failure · 2 cannot run.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.realpath(__file__))
SCRIPT = os.path.join(HERE, "assets", "stale-claim-check.py")

CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


def run(files, registry_rows, *extra):
    """Build a throwaway tree and run the checker over it. Returns (exit code, output)."""
    d = tempfile.mkdtemp(prefix="scc-selftest-")
    try:
        for rel, body in files.items():
            path = os.path.join(d, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(body)
        reg = os.path.join(d, "registry.tsv")
        with open(reg, "w", encoding="utf-8") as f:
            f.write("\n".join(registry_rows) + "\n")
        p = subprocess.run(
            [sys.executable, "-X", "utf8", SCRIPT, "--registry", reg, "--root", d, *extra],
            capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr
    finally:
        shutil.rmtree(d, ignore_errors=True)


ROW = "5632m\t21290m derived from /proc/meminfo\thardcoded before the RAM upgrade"


# ---------------------------------------------------------------- the core discrimination

@case("an unqualified survivor is flagged, and named with its line")
def _():
    rc, out = run({"doc.md": "# Doc\n\nThe ceiling is 5632m.\n"}, [ROW])
    assert rc == 1, out
    assert "doc.md:3" in out, out
    assert "asserts" in out and "live" in out, out


@case("a marked survivor is NOT flagged — a retraction may quote the old value")
def _():
    rc, out = run({"doc.md": "# Doc\n\nThis was retracted: the ceiling is 5632m.\n"}, [ROW])
    assert rc == 0, out


# ---------------------------------------------------------------- the 3-line marker window

@case("a marker exactly 3 lines away exempts the occurrence")
def _():
    # CONTEXT = 3. Two lines was too tight once -- a 'refuted' sat just outside it.
    body = "the claim was refuted\nfiller\nfiller\nThe ceiling is 5632m.\n"
    rc, out = run({"doc.md": body}, [ROW])
    assert rc == 0, out


@case("a marker 4 lines away does NOT exempt it")
def _():
    # The window must be a window. If distance never mattered, a real survivor sitting near
    # any unrelated retraction would go unflagged.
    body = "the claim was refuted\nfiller\nfiller\nfiller\nThe ceiling is 5632m.\n"
    rc, out = run({"doc.md": body}, [ROW])
    assert rc == 1, out


# ---------------------------------------------------------------- append-only conventions

@case("a REVISED banner beside the figure exempts it")
def _():
    # gamedev-srv, 2026-09-09: a design document used `> **REVISED -- see 13.7.**` in twelve
    # sections and every correctly-marked revision read as an unqualified survivor.
    body = "# Doc\n\n> **REVISED — see 13.7.**\n\nThe ceiling is 5632m.\n"
    rc, out = run({"doc.md": body}, [ROW])
    assert rc == 0, out


@case("a bare section reference 'see 13.7' also exempts")
def _():
    body = "# Doc\n\nsee 13.7\n\nThe ceiling is 5632m.\n"
    rc, out = run({"doc.md": body}, [ROW])
    assert rc == 0, out


# ---------------------------------------------------------------- file-level banner

@case("an OPENING banner exempts the whole file")
def _():
    body = "# ⛔ SUPERSEDED\n\n" + "The ceiling is 5632m.\n" * 3
    rc, out = run({"dead.md": body}, [ROW])
    assert rc == 0, out
    assert "skipped" in out, out


@case("a banner BELOW line 25 does not exempt the file")
def _():
    # A reader quoting line 200 never saw a banner buried mid-file. The claim is kept far
    # from the banner on purpose: within 3 lines the MARKER window would exempt it, and the
    # test would silently be checking the wrong mechanism.
    body = "The ceiling is 5632m.\n" + "filler\n" * 40 + "# SUPERSEDED\n"
    rc, out = run({"doc.md": body}, [ROW])
    assert rc == 1, out


# ---------------------------------------------------------------- the malformed-row ratchet

@case("a 5-field registry row fails the run and is named")
def _():
    # 2026-09-08: three rows written in a five-column shape compiled '2026-09-08' as the
    # regex and matched 69 of that run's 83 hits, while the three claims they existed to
    # guard were watched by nothing. A watcher watching nothing presents as noise.
    bad = "2026-09-08\tme\t5632m\twhy it changed\tthe lesson"
    rc, out = run({"doc.md": "nothing relevant here\n"}, [bad])
    assert rc == 1, out
    assert "MALFORMED" in out, out
    assert "2026-09-08" in out, out


@case("a malformed row makes an otherwise-clean run fail, saying it checked less")
def _():
    bad = "a\tb\tc\td"
    rc, out = run({"doc.md": "nothing relevant\n"}, [ROW, bad])
    assert rc == 1, out
    assert "checked less than it looks" in out, out


# ---------------------------------------------------------------- vendored trees

@case("vendored trees are excluded by default, and the count is printed")
def _():
    # A third-party changelog cannot assert anything about your project. Six of eight hits in
    # one real run came from node_modules. A SILENT exclusion would be indistinguishable from
    # a clean tree, so the count must appear.
    rc, out = run({"node_modules/pkg/CHANGELOG.md": "The ceiling is 5632m.\n"}, [ROW])
    assert rc == 0, out
    assert "excluded" in out, out


@case("--no-default-excludes scans them anyway")
def _():
    rc, out = run({"node_modules/pkg/CHANGELOG.md": "The ceiling is 5632m.\n"}, [ROW],
                  "--no-default-excludes")
    assert rc == 1, out


@case("--exclude-dir adds a directory of your own")
def _():
    rc, out = run({"fixtures/old.md": "The ceiling is 5632m.\n"}, [ROW],
                  "--exclude-dir", "fixtures")
    assert rc == 0, out


# ---------------------------------------------------------------- green is the dangerous colour

@case("a clean run says the REGISTRY is clean, never that the repo is")
def _():
    rc, out = run({"doc.md": "nothing relevant here\n"}, [ROW])
    assert rc == 0, out
    assert "REGISTRY is clean" in out, out


def main():
    if not os.path.exists(SCRIPT):
        print("CANNOT RUN: %s not found" % SCRIPT, file=sys.stderr)
        return 2

    failed = 0
    for name, fn in CASES:
        try:
            fn()
            print("  pass  %s" % name)
        except AssertionError as e:
            failed += 1
            print("  FAIL  %s\n        %s" % (name, str(e)[:400]))
        except Exception as e:
            failed += 1
            print("  ERROR %s\n        %r" % (name, e))

    print("\n%d/%d passed" % (len(CASES) - failed, len(CASES)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
