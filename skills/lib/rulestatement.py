#!/usr/bin/env python3
"""The ONE parser for a rule's quotable statement. Import it; never re-implement it.

A rule states itself in one line, in a fixed place: the first non-empty line beneath the
`## The rule` heading, as a blockquote (`>`) or a bold statement (`**`). Two shapes are
accepted because the corpus genuinely uses both; a third is drift.

`extract` returns the flattened statement, or None. **None means REFUSE** -- never fall
back to emitting a bare link, because a silent fallback is how an all-URL block
accumulates without anyone deciding to have one.

See rules/how-we-work/a-rule-states-itself-in-one-line.md

    python3 rulestatement.py <file.md>     # print the statement, exit 1 if absent
"""
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^##\s+The rule\s*$", re.M)


def extract(text: str):
    """The statement as one flat line, or None if the rule does not carry one."""
    m = HEADING.search(text)
    if not m:
        return None
    body = text[m.end():]
    lines = body.split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return None
    first = lines[i].strip()
    if not (first.startswith(">") or first.startswith("**")):
        return None
    out = []
    while i < len(lines) and lines[i].strip():
        out.append(lines[i].strip().lstrip(">").strip())
        i += 1
    return " ".join(out).strip() or None


def extract_path(path) -> "str | None":
    return extract(Path(path).read_text(encoding="utf-8"))


def title(text: str, fallback: str = "") -> str:
    for line in text.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    st = extract_path(sys.argv[1])
    if st is None:
        print("no extractable statement: %s" % sys.argv[1], file=sys.stderr)
        sys.exit(1)
    print(st)
