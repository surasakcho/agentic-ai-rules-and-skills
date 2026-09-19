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


# --- adoption policy shared by every adopter -------------------------------------
# A block of ~90 URLs was adopted, pinned, quoted back, and did not fire. Volume is
# part of that failure: attention thins across the excess. The ceiling is therefore
# a REFUSAL, never a silent truncation -- which of N rules to keep is a judgement,
# and slicing an alphabetical list makes it for nobody.
RULE_CEILING = 25


MANDATORY_CATEGORY = "how-we-work"


def over_ceiling(counts: dict, ceiling: int = RULE_CEILING):
    """A refusal message when the OPTIONAL selection is too big, or None.

    The ceiling binds the domain categories only. `how-we-work` is mandatory and is
    54 rules on its own, so a ceiling counting it would refuse every repo forever --
    "adopt it always" and "cap at 25" can only both hold if the cap binds what is
    optional. ASSUMPTION, recorded here so it can be overruled in one place.
    """
    total = sum(n for c, n in counts.items() if c != MANDATORY_CATEGORY)
    if total <= ceiling:
        return None
    lines = ["REFUSED -- %d rules selected from domain categories, ceiling is %d."
             % (total, ceiling), "",
             "  (%s is mandatory and is not counted against the ceiling)"
             % MANDATORY_CATEGORY, ""]
    for cat in sorted(counts, key=lambda c: -counts[c]):
        lines.append("  %-22s %d" % (cat, counts[cat]))
    lines += ["",
              "Narrow the categories and run again. Truncating for you would pick which",
              "rules bind this repo by filename order, which is a judgement nobody made.",
              "See rules/how-we-work/a-rule-states-itself-in-one-line.md"]
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    st = extract_path(sys.argv[1])
    if st is None:
        print("no extractable statement: %s" % sys.argv[1], file=sys.stderr)
        sys.exit(1)
    print(st)
