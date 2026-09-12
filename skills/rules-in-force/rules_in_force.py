#!/usr/bin/env python3
"""rules-in-force -- what a repo is actually bound by, in one pass.

A repo's adopted block is a list of LINKS. In one real case: 97 lines, ~90 URLs, zero
sentences of rule text. Nobody opens ninety links, so the rules end up known by reputation --
and a rule that is a URL rather than text is not in front of you at the moment it applies.

This prints each rule's own statement, VERBATIM, grouped by category, read at the commit the
repo actually pinned.

  python3 rules_in_force.py --repo <repo> [--shared <clone>] [options]

Never modifies anything. Never fetches. Exit 0 digest printed · 1 nothing to read · 2 cannot run.
"""
import argparse
import os
import re
import subprocess
import sys

BEGIN = "<!-- shared-lessons:begin -->"
END = "<!-- shared-lessons:end -->"

# The adopted block writes one bullet per rule, linking a blob URL that carries both the pin
# and the path. Parsing the URL rather than the link text is deliberate: the text is a
# prettified slug, the URL is the address of the actual file.
LINK = re.compile(r"\[([^\]]+)\]\(https?://[^)]*?/blob/([0-9a-f]{6,40})/(rules/[^)#]+\.md)\)")
CATEGORY = re.compile(r"^\*\*([a-z0-9-]+)\*\*\s*(?:—|--)", re.M)
PIN = re.compile(r"at `([0-9a-f]{6,40})`")


def run(*args):
    return subprocess.run(args, capture_output=True, text=True)


def read_at(shared, sha, path):
    """A rule file as it was at the pinned commit -- not as it reads today."""
    r = run("git", "-C", shared, "show", f"{sha}:{path}")
    return r.stdout if r.returncode == 0 else None


def statement(text):
    """The rule's own statement, verbatim.

    Convention across the corpus: a `## The rule` heading, then the statement as the first
    block under it. That block is a BLOCKQUOTE in some files and a BOLD PARAGRAPH in others --
    an early version of this function handled only the blockquote and silently reported 6 of
    10 coding rules as unextractable. The corpus was fine; the reader was wrong.

    Emphasis markers are stripped for legibility. Nothing else is altered: no rewording, no
    truncation, no summarising.
    """
    if not text:
        return None
    m = re.search(r"^##\s+The rule\s*$", text, re.M)
    if not m:
        return None

    lines = []
    for line in text[m.end():].splitlines():
        s = line.strip()
        if not s or s == "---":
            if lines:
                break          # blank line ends the statement
            continue           # leading blanks before it
        if s.startswith("#"):
            break              # ran into the next heading without finding one
        lines.append(s.lstrip(">").strip())

    if not lines:
        return None
    out = re.sub(r"\s+", " ", " ".join(lines)).strip()
    out = re.sub(r"\*\*(.+?)\*\*", r"\1", out)
    return out or None


def task_type(text):
    if not text:
        return None
    m = re.search(r"^\*\*Task type:\*\*\s*(.+?)(?:\s*$)", text, re.M)
    return m.group(1).strip() if m else None


def parse_block(claude_md):
    """Pin, and [(category, name, path)] in document order."""
    if BEGIN not in claude_md:
        return None, []
    block = claude_md.split(BEGIN, 1)[1].split(END, 1)[0]
    pm = PIN.search(block)
    pin = pm.group(1) if pm else None

    # Walk the block so every bullet is attributed to the heading above it.
    cat = "(uncategorised)"
    rules, seen = [], set()
    for line in block.splitlines():
        cm = CATEGORY.match(line.strip())
        if cm:
            cat = cm.group(1)
            continue
        lm = LINK.search(line)
        if lm:
            path = lm.group(3)
            if path in seen:
                continue
            seen.add(path)
            rules.append((cat, lm.group(1), path, lm.group(2)))
    return pin, rules


def local_rules(repo, claude_md):
    """The repo's OWN headings, outside the adopted block. These win on conflict."""
    outside = claude_md
    if BEGIN in claude_md:
        head, rest = claude_md.split(BEGIN, 1)
        outside = head + (rest.split(END, 1)[1] if END in rest else "")
    heads = [h.strip() for h in re.findall(r"^#{2,3}\s+(.+?)\s*$", outside, re.M)]
    return [h for h in heads if h.lower() not in ("shared working rules",)]


def main():
    ap = argparse.ArgumentParser(description="Print the rules a repo is currently bound by.")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--shared", help="local clone of the shared rules repo "
                                     "(default: the repo this script lives in)")
    ap.add_argument("--category", action="append", help="limit to a category; repeatable")
    ap.add_argument("--brief", action="store_true", help="names only, no statements")
    ap.add_argument("--drift", action="store_true",
                    help="also report rules whose text changed between the pin and HEAD")
    a = ap.parse_args()

    cmd = os.path.join(a.repo, "CLAUDE.md")
    if not os.path.isfile(cmd):
        print(f"no CLAUDE.md in {a.repo}", file=sys.stderr)
        return 2
    claude_md = open(cmd, encoding="utf-8").read()

    # realpath, not abspath: this skill is normally reached through a symlink in
    # ~/.claude/skills/, and abspath would resolve the shared clone to ~/.claude.
    here = os.path.dirname(os.path.realpath(__file__))
    shared = a.shared or os.path.abspath(os.path.join(here, "..", ".."))
    if not os.path.isdir(os.path.join(shared, ".git")):
        print(f"not a git clone: {shared}  (pass --shared)", file=sys.stderr)
        return 2

    pin, rules = parse_block(claude_md)
    local = local_rules(a.repo, claude_md)

    print()
    print(f"rules in force — {os.path.basename(os.path.abspath(a.repo))}")
    if pin:
        print(f"shared rules pinned at {pin}")
    print()

    if not rules and not local:
        print("no adopted block and no local rules. This repo is bound by nothing written down.")
        print("→ run retrieve-lessons to adopt the shared rules.")
        return 1

    if local:
        print("LOCAL — this repo's own rules. These win on conflict with anything below.")
        for h in local:
            print(f"  · {h}")
        print()

    if not rules:
        print("no shared-lessons block — nothing adopted from the shared repo.")
        return 1

    wanted = set(a.category) if a.category else None
    missing, shown, skipped_cat = [], 0, 0
    drifted = []

    cats = []
    for cat, name, path, sha in rules:
        if not cats or cats[-1][0] != cat:
            cats.append((cat, []))
        cats[-1][1].append((name, path, sha))

    for cat, items in cats:
        if wanted and cat not in wanted:
            skipped_cat += len(items)
            continue
        print(f"{cat.upper()}  ({len(items)})")
        for name, path, sha in items:
            text = read_at(shared, sha, path)
            if text is None:
                missing.append((path, f"not present at {sha}"))
                print(f"  · {name}")
                print(f"    ! could not read {path} at {sha}")
                continue
            if a.brief:
                print(f"  · {name}")
                shown += 1
                continue
            st = statement(text)
            if st is None:
                tt = task_type(text)
                missing.append((path, "no '## The rule' section"))
                print(f"  · {name}")
                print(f"    ! no rule statement in the file{f' — task type: {tt}' if tt else ''}")
                continue
            print(f"  · {name}")
            print(f"    {st}")
            shown += 1
            if a.drift:
                head = read_at(shared, "HEAD", path)
                if head is not None and head != text:
                    drifted.append(path)
        print()

    total = len(rules)
    print("─" * 76)
    print(f"{total} rule(s) adopted · {shown} statement(s) shown · "
          f"{len(missing)} not extracted · {skipped_cat} filtered out")

    # The count must reconcile. A digest that quietly drops a rule reproduces, inside the
    # tool, the exact failure it was built to fix.
    if missing:
        print("\nNOT EXTRACTED — read these files directly:")
        for path, why in missing:
            print(f"  {path}  ({why})")

    if a.drift:
        if drifted:
            print(f"\nDRIFT — {len(drifted)} rule(s) differ between the pin and HEAD:")
            for p in drifted:
                print(f"  {p}")
            print("These are NOT the rules in force; the pin is. Re-pin with retrieve-lessons "
                  "after reading the diff.")
        else:
            print("\nno drift: every adopted rule is identical at the pin and at HEAD.")

    print("\nVerbatim from the rule files at the pinned commit. Nothing here is paraphrased.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
