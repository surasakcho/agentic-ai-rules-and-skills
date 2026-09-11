#!/usr/bin/env python
"""Self-test: prove retrieve.py detects, discriminates, and can FAIL.

The interesting property is not that it finds categories -- it is that it does NOT find the
ones with no evidence. A detector that selects everything is the same as no detector.

    python -X utf8 test_self.py
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
SCRIPT = HERE / "retrieve.py"


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                          encoding="utf-8", errors="replace")


def build_shared(root: Path):
    """A miniature of the shared repo, as a real git repo so --shared can be pinned."""
    for cat in ("analytics", "testing", "coding", "research", "data-engineering",
                "how-we-work"):
        d = root / "rules" / cat
        d.mkdir(parents=True)
        (d / f"{cat}-rule.md").write_text(f"# {cat}\n\n## The incident\n\nCost: real.\n",
                                          encoding="utf-8")
        # A SECOND rule per category, so declining one rule leaves the category populated.
        # With one rule each, "decline a rule" and "decline the category" are the same act
        # and the distinction the selection record exists for cannot be tested at all.
        (d / f"{cat}-rule-two.md").write_text(f"# {cat} two\n\n## The incident\n\nReal.\n",
                                              encoding="utf-8")
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "t@t.t")
    git(root, "config", "user.name", "t")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "seed")
    return root


def build_target(root: Path):
    """A repo that plots and tests, but does NO research and has NO data pipeline."""
    (root / "src").mkdir(parents=True)
    (root / "tests").mkdir(parents=True)
    (root / "figures").mkdir(parents=True)
    (root / "src" / "app.py").write_text("print('hi')\n", encoding="utf-8")
    (root / "tests" / "test_app.py").write_text("def test_x(): assert True\n", encoding="utf-8")
    (root / "requirements.txt").write_text("matplotlib\npytest\n", encoding="utf-8")
    return root


def build_vendored_target(root: Path):
    """A prose repo whose ONLY code is a downloaded dependency.

    An Obsidian vault ships every installed plugin as a built main.js. Nothing here was
    written by the repo's authors, so "coding" is evidence they cannot act on.
    """
    (root / ".obsidian" / "plugins" / "obsidian-reminder-plugin").mkdir(parents=True)
    (root / ".obsidian" / "plugins" / "obsidian-reminder-plugin" / "main.js").write_text(
        "'use strict';var e=require('obsidian');\n", encoding="utf-8")
    (root / "notes").mkdir(parents=True)
    (root / "notes" / "a-note.md").write_text("# a note\n", encoding="utf-8")
    return root


def run(target, shared, *extra):
    r = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), "--repo", str(target),
                        "--shared", str(shared), *extra],
                       capture_output=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout + r.stderr


def main():
    failures = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        shared = build_shared(tmp / "shared")
        target = build_target(tmp / "target")

        code, out = run(target, shared, "--json")
        try:
            data = json.loads(out)
        except Exception:
            print(out[-800:])
            print("\nSELF-TEST FAILED: --json did not produce JSON")
            return 1
        sel = set(data["selected"])

        checks = {
            "selects analytics from matplotlib + figures/": "analytics" in sel,
            "selects testing from pytest + tests/": "testing" in sel,
            "selects coding from src/": "coding" in sel,
            "does NOT select research (no evidence)": "research" not in sel,
            "does NOT select data-engineering (no evidence)": "data-engineering" not in sel,
            "records a pin": bool(data["sha"]),
            # The target repo has no scheduler, no .claude/ and no CLAUDE.md -- how-we-work is
            # adopted on the mandatory rule alone. Empty MANDATORY, or bolt a detector onto
            # this category, and these go red.
            "MANDATORY: how-we-work adopted with zero evidence": "how-we-work" in sel,
            # .get(), not [] -- if MANDATORY is emptied this must report a red check, not raise
            # a KeyError that aborts the run before the other checks are even reached.
            "MANDATORY marker is the reason recorded, not a detector hit":
                data["selected"].get("how-we-work") == ["mandatory for every project"],
        }

        # A repo whose only code is vendored must not adopt the coding rules.
        vendored = build_vendored_target(tmp / "vault")
        _, vout = run(vendored, shared, "--json")
        vsel = set(json.loads(vout)["selected"])
        checks["does NOT select coding from a vendored .obsidian plugin"] = "coding" not in vsel
        checks["still adopts the mandatory category in a prose-only repo"] = (
            "how-we-work" in vsel)

        # --check must FAIL before anything is written.
        code, _ = run(target, shared, "--check")
        checks["--check fails when no block exists"] = code == 1

        code, _ = run(target, shared, "--write")
        cm = (target / "CLAUDE.md").read_text(encoding="utf-8")
        checks["--write creates the block"] = "shared-lessons:begin" in cm
        checks["links point at the shared repo"] = "rules/analytics/analytics-rule.md" in cm
        checks["does not link an unselected category"] = "rules/research/" not in cm
        checks["the mandatory category is linked"] = "rules/how-we-work/" in cm
        checks["the mandatory category is listed FIRST"] = (
            "**how-we-work**" in cm and "**analytics**" in cm
            and cm.index("**how-we-work**") < cm.index("**analytics**"))

        code, _ = run(target, shared, "--check")
        checks["--check passes once pinned"] = code == 0

        # Idempotent: writing twice must not duplicate the block.
        run(target, shared, "--write")
        cm2 = (target / "CLAUDE.md").read_text(encoding="utf-8")
        checks["--write is idempotent"] = cm2.count("shared-lessons:begin") == 1

        # Move the shared repo on: the pin is now stale and --check must say so.
        (shared / "rules" / "coding" / "another.md").write_text(
            "# another\n\n## The incident\n\nCost: real.\n", encoding="utf-8")
        git(shared, "add", "-A")
        git(shared, "commit", "-q", "-m", "move on")
        code, out = run(target, shared, "--check")
        checks["--check detects a stale pin"] = code == 1 and "pinned at" in out

        # Preserves surrounding content.
        (target / "CLAUDE.md").write_text(
            "# My rules\n\nKeep me.\n\n" + cm2, encoding="utf-8")
        run(target, shared, "--write")
        cm3 = (target / "CLAUDE.md").read_text(encoding="utf-8")
        checks["--write preserves existing CLAUDE.md content"] = "Keep me." in cm3

        # A shared repo missing a category must be a hard error, not a silent skip.
        import shutil
        shutil.rmtree(shared / "rules" / "analytics")
        git(shared, "add", "-A")
        git(shared, "commit", "-q", "-m", "drop analytics")
        code, out = run(target, shared, "--write")
        checks["errors when the shared repo drops a category"] = (
            code != 0 and "no rules/analytics" in out)

        for label, ok in checks.items():
            print(f"  [{'ok' if ok else 'MISS'}] {label}")
            if not ok:
                failures.append(label)

        # ---- re-pin: the SHA advances, the categories do not ----------------------
        # Each case below is checked in BOTH directions where it can be: the hold case
        # asserts the file was not rewritten, not merely that the exit code was 0.
        rp_shared = tmp / "rp_shared"
        rp_shared.mkdir()
        build_shared(rp_shared)
        rp_target = tmp / "rp_target"
        rp_target.mkdir()
        build_target(rp_target)
        run(rp_target, rp_shared, "--offline", "--write")
        cm = rp_target / "CLAUDE.md"
        pinned_once = cm.read_text(encoding="utf-8")

        # A commit that touches only skills/ must NOT make a consumer stale. This is the
        # false alarm that cost 78 links of churn for no behavioural difference.
        (rp_shared / "skills").mkdir(exist_ok=True)
        (rp_shared / "skills" / "s.md").write_text("# skill\n", encoding="utf-8")
        git(rp_shared, "add", "-A"); git(rp_shared, "commit", "-q", "-m", "skills only")
        code, out = run(rp_target, rp_shared, "--offline", "--check")
        for label, ok in [
            ("--check holds through a skills-only commit", code == 0 and "NO RULE MOVED" in out),
        ]:
            print(f"  [{'ok' if ok else 'FAIL'}] {label}")
            if not ok:
                failures.append(label)

        code, out = run(rp_target, rp_shared, "--offline", "--repin")
        unchanged = cm.read_text(encoding="utf-8") == pinned_once
        for label, ok in [
            ("--repin holds, and does not rewrite the file", code == 0 and unchanged),
        ]:
            print(f"  [{'ok' if ok else 'FAIL'}] {label}")
            if not ok:
                failures.append(label)

        # A commit that DOES touch rules/ must fire, and --repin must then write.
        (rp_shared / "rules" / "how-we-work" / "new-rule.md").write_text(
            "# new\n", encoding="utf-8")
        git(rp_shared, "add", "-A"); git(rp_shared, "commit", "-q", "-m", "a rule moved")
        code_check, out_check = run(rp_target, rp_shared, "--offline", "--check")
        code_pin, out_pin = run(rp_target, rp_shared, "--offline", "--repin")
        after = cm.read_text(encoding="utf-8")
        cats_before = set(re.findall(r"/rules/([a-z-]+)/", pinned_once))
        cats_after = set(re.findall(r"/rules/([a-z-]+)/", after))
        for label, ok in [
            ("--check fires when a rule moves, and names it",
             code_check == 1 and "new-rule.md" in out_check),
            ("--repin writes when a rule moved", code_pin == 0 and after != pinned_once),
            ("--repin does NOT change the category set", cats_before == cats_after),
            ("--repin picks up a new rule in an adopted category",
             "new-rule.md" in after),
        ]:
            print(f"  [{'ok' if ok else 'FAIL'}] {label}")
            if not ok:
                failures.append(label)

        # A linked rule that VANISHED must stop the run. verify_links cannot catch this --
        # it checks the links about to be written, and a deleted rule just stops being one.
        git(rp_shared, "rm", "-q", str(rp_shared / "rules" / "how-we-work" / "how-we-work-rule.md"))
        git(rp_shared, "commit", "-q", "-m", "delete an adopted rule")
        before_del = cm.read_text(encoding="utf-8")
        code, out = run(rp_target, rp_shared, "--offline", "--repin")
        for label, ok in [
            ("--repin refuses when an adopted rule was deleted",
             code != 0 and "no longer exist" in out
             and cm.read_text(encoding="utf-8") == before_del),
        ]:
            print(f"  [{'ok' if ok else 'FAIL'}] {label}")
            if not ok:
                failures.append(label)

        # First-time adoption is judgement and must not be invented by --repin.
        fresh = tmp / "fresh"
        fresh.mkdir()
        build_target(fresh)
        code, out = run(fresh, rp_shared, "--offline", "--repin")
        for label, ok in [
            ("--repin refuses a repo with no block, and points at --write",
             code != 0 and "--write" in out),
        ]:
            print(f"  [{'ok' if ok else 'FAIL'}] {label}")
            if not ok:
                failures.append(label)

        # ---- selection record: review, decline, manual adopt ----------------------------
        # PRD docs/prd/retrieve-lessons-review-and-declines.md -- all five "done" checks.
        sel = tmp / "sel"
        sel.mkdir()
        build_target(sel)

        code, out = run(sel, rp_shared, "--offline", "--review")
        cm_absent = not (sel / "CLAUDE.md").exists()
        code_d1, _ = run(sel, rp_shared, "--offline",
                         "--decline", "testing", "--reason", "no suite anyone runs")
        code_d2, _ = run(sel, rp_shared, "--offline",
                         "--decline", "coding/coding-rule.md", "--reason", "does not fit")
        code_w, _ = run(sel, rp_shared, "--offline", "--write")
        block = (sel / "CLAUDE.md").read_text(encoding="utf-8")
        rec = (sel / ".claude" / "lessons-selection.tsv").read_text(encoding="utf-8")

        code_r2, out_r2 = run(sel, rp_shared, "--offline", "--review")
        code_ra, out_ra = run(sel, rp_shared, "--offline", "--review", "--all")

        # a category with NO detector evidence, adopted by hand, must survive --write
        run(sel, rp_shared, "--offline", "--adopt", "research", "--reason", "we publish findings")
        run(sel, rp_shared, "--offline", "--write")
        block2 = (sel / "CLAUDE.md").read_text(encoding="utf-8")
        run(sel, rp_shared, "--offline", "--write")
        block3 = (sel / "CLAUDE.md").read_text(encoding="utf-8")

        code_chk, _ = run(sel, rp_shared, "--offline", "--check")

        for label, ok in [
            ("--review writes nothing", code == 0 and cm_absent),
            ("--decline records a category and a single rule",
             code_d1 == 0 and code_d2 == 0
             and "testing" in rec and "coding/coding-rule.md" in rec
             and "no suite anyone runs" in rec),
            ("a declined CATEGORY is absent from the written block",
             code_w == 0 and "rules/testing/" not in block),
            ("a declined RULE is absent, but its category survives",
             "rules/coding/coding-rule.md)" not in block
             and "rules/coding/coding-rule-two.md" in block),
            ("declines persist: --review no longer offers them as new",
             code_r2 == 0 and "declined" in out_r2.lower()),
            ("--review --all re-presents declines WITH their reasons",
             code_ra == 0 and "no suite anyone runs" in out_ra),
            ("a hand-adopted category with no evidence reaches the block",
             "rules/research/research-rule.md" in block2),
            ("...and SURVIVES a second --write (the analytics drift bug)",
             "rules/research/research-rule.md" in block3),
            ("--check stays non-interactive and passes after all of it", code_chk == 0),
        ]:
            print(f"  [{'ok' if ok else 'FAIL'}] {label}")
            if not ok:
                failures.append(label)

    if failures:
        print("\nSELF-TEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nself-test passed: detection discriminates, the pin catches drift, "
          "and a reorganised shared repo fails loudly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
