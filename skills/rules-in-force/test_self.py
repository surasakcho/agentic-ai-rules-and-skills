#!/usr/bin/env python3
"""Self-test for rules_in_force.py.

The properties that matter are not "it printed something" -- they are that the statement is
the file's own, that it is read at the PIN rather than HEAD, and that the count reconciles so
a dropped rule cannot hide.

Exit 0 pass · 1 failure · 2 cannot run.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "rules_in_force.py")
sys.path.insert(0, HERE)

CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


# ---------------------------------------------------------------- extraction

@case("a blockquote statement is extracted")
def _():
    from rules_in_force import statement
    got = statement("# t\n\n## The rule\n\n> **Do the thing.**\n\nprose after\n")
    assert got == "Do the thing.", repr(got)


@case("a bold-paragraph statement is extracted too")
def _():
    # The corpus uses BOTH shapes. An earlier version handled only the blockquote and
    # reported 6 of 10 coding rules as unextractable -- the reader was wrong, not the corpus.
    from rules_in_force import statement
    got = statement("## The rule\n\n**Run `git status` first.**\n\nprose\n")
    assert got == "Run `git status` first.", repr(got)


@case("a multi-line statement is joined, not truncated")
def _():
    from rules_in_force import statement
    got = statement("## The rule\n\n> **Before any write that\n> destroys content, stop.**\n\nx\n")
    assert got == "Before any write that destroys content, stop.", repr(got)


@case("prose after the blank line is NOT swept into the statement")
def _():
    from rules_in_force import statement
    got = statement("## The rule\n\n**Short.**\n\nThis explanatory sentence must not appear.\n")
    assert "explanatory" not in got, repr(got)


@case("a file with no '## The rule' returns None rather than guessing")
def _():
    from rules_in_force import statement
    assert statement("# t\n\n**Task type:** coding\n\nsome prose\n") is None


@case("statement() never invents text for empty input")
def _():
    from rules_in_force import statement
    assert statement("") is None
    assert statement(None) is None


# ---------------------------------------------------------------- block parsing

BLOCK = """# Repo

## Local thing

<!-- shared-lessons:begin -->

## Shared working rules

Adopted from [x](https://github.com/o/r) at `abc1234`. Linked, not copied.

**how-we-work** — mandatory:

- [alpha rule](https://github.com/o/r/blob/abc1234/rules/how-we-work/alpha.md)
- [beta rule](https://github.com/o/r/blob/abc1234/rules/how-we-work/beta.md)

**coding** — evidence:

- [gamma rule](https://github.com/o/r/blob/abc1234/rules/coding/gamma.md)

<!-- shared-lessons:end -->

## Another local thing
"""


@case("the pin is read from the block")
def _():
    from rules_in_force import parse_block
    pin, _ = parse_block(BLOCK)
    assert pin == "abc1234", pin


@case("every rule is attributed to the heading above it")
def _():
    from rules_in_force import parse_block
    _, rules = parse_block(BLOCK)
    assert len(rules) == 3, rules
    cats = [r[0] for r in rules]
    assert cats == ["how-we-work", "how-we-work", "coding"], cats


@case("the path comes from the URL, not the prettified link text")
def _():
    from rules_in_force import parse_block
    _, rules = parse_block(BLOCK)
    assert rules[0][2] == "rules/how-we-work/alpha.md", rules[0]


@case("local headings are collected, and the block's own heading is not")
def _():
    from rules_in_force import local_rules
    got = local_rules(".", BLOCK)
    assert "Local thing" in got and "Another local thing" in got, got
    assert "Shared working rules" not in got, got


@case("a repo with no block yields no rules and no pin")
def _():
    from rules_in_force import parse_block
    pin, rules = parse_block("# plain\n\n## heading\n")
    assert pin is None and rules == []


# ---------------------------------------------------------------- end to end

def real_repo_run(*extra):
    """Run against this very repo, which carries a real corpus."""
    shared = os.path.abspath(os.path.join(HERE, "..", ".."))
    d = tempfile.mkdtemp(prefix="rif-selftest-")
    try:
        head = subprocess.run(["git", "-C", shared, "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
        names = subprocess.run(
            ["git", "-C", shared, "ls-tree", "--name-only", f"{head}", "rules/how-we-work/"],
            capture_output=True, text=True).stdout.split()
        picks = [n for n in names if n.endswith(".md")][:3]
        lines = "\n".join(
            f"- [{os.path.basename(p)[:-3]}](https://github.com/o/r/blob/{head}/{p})"
            for p in picks)
        body = (f"# t\n\n<!-- shared-lessons:begin -->\n\n## Shared working rules\n\n"
                f"Adopted at `{head}`.\n\n**how-we-work** — mandatory:\n\n{lines}\n\n"
                f"<!-- shared-lessons:end -->\n")
        with open(os.path.join(d, "CLAUDE.md"), "w", encoding="utf-8") as f:
            f.write(body)
        p = subprocess.run([sys.executable, "-X", "utf8", SCRIPT, "--repo", d,
                            "--shared", shared, *extra], capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr, len(picks)
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


@case("end to end: the count reconciles")
def _():
    rc, out, n = real_repo_run()
    assert rc == 0, out
    m = re.search(r"(\d+) rule\(s\) adopted · (\d+) statement\(s\) shown · "
                  r"(\d+) not extracted · (\d+) filtered out", out)
    assert m, out
    adopted, shown, missed, filtered = (int(g) for g in m.groups())
    assert adopted == n, f"expected {n} adopted, got {adopted}"
    # The reconciliation is the whole guarantee: a dropped rule cannot hide in the total.
    assert shown + missed + filtered == adopted, out


@case("end to end: --category filters, and says how many it filtered out")
def _():
    rc, out, n = real_repo_run("--category", "coding")
    assert rc == 0, out
    m = re.search(r"(\d+) rule\(s\) adopted · (\d+) statement\(s\) shown · "
                  r"(\d+) not extracted · (\d+) filtered out", out)
    assert m, out
    _, shown, _, filtered = (int(g) for g in m.groups())
    assert shown == 0 and filtered == n, out


@case("end to end: a repo with no CLAUDE.md cannot run, and says so")
def _():
    d = tempfile.mkdtemp(prefix="rif-selftest-empty-")
    try:
        p = subprocess.run([sys.executable, SCRIPT, "--repo", d], capture_output=True, text=True)
        assert p.returncode == 2, p.returncode
        assert "no CLAUDE.md" in (p.stdout + p.stderr)
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


@case("end to end: a repo with a CLAUDE.md but no block exits 1, not 0")
def _():
    d = tempfile.mkdtemp(prefix="rif-selftest-noblock-")
    try:
        with open(os.path.join(d, "CLAUDE.md"), "w", encoding="utf-8") as f:
            f.write("# plain repo\n")
        shared = os.path.abspath(os.path.join(HERE, "..", ".."))
        p = subprocess.run([sys.executable, SCRIPT, "--repo", d, "--shared", shared],
                           capture_output=True, text=True)
        # Adopting nothing is a real state and must not read as a clean digest.
        assert p.returncode == 1, p.returncode
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def main():
    if not os.path.exists(SCRIPT):
        print("CANNOT RUN: %s not found" % SCRIPT, file=sys.stderr)
        return 2
    shared = os.path.abspath(os.path.join(HERE, "..", ".."))
    if not os.path.isdir(os.path.join(shared, ".git")):
        print("CANNOT RUN: %s is not a git clone" % shared, file=sys.stderr)
        return 2

    failed = 0
    for name, fn in CASES:
        try:
            fn()
            print("  pass  %s" % name)
        except AssertionError as e:
            failed += 1
            print("  FAIL  %s\n        %s" % (name, e))
        except Exception as e:
            failed += 1
            print("  ERROR %s\n        %r" % (name, e))

    print("\n%d/%d passed" % (len(CASES) - failed, len(CASES)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
