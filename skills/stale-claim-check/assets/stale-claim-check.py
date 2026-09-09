#!/usr/bin/env python3
"""Find places that still ASSERT a superseded claim, not places that merely contain the old string.

Why this exists
---------------
On 2026-08-22 this repo produced roughly a dozen retractions. Four of them were
recorded correctly -- a banner at the top of the file, the offending bullet struck
-- and STILL left the original claim standing somewhere else. In the worst case
the survivor was an ADR's own Decision statement, i.e. the single sentence anyone
citing that document would quote.

    A correction lands where you NOTICED the error, not where the claim LIVES.

Search-and-replace covers "every place containing the old string". This covers the
set that actually matters: "every place still ASSERTING it". Those differ, because
a retraction quotes the old value legitimately -- so an occurrence is only a
problem when nothing nearby marks it as superseded.

FALSE POSITIVES ARE EXPECTED AND ARE NOT A BUG. First run: 5 flagged, 1 real.
After widening the registry from 11 to 25 claims and loosening the marker window
from 2 lines to 3, it reports clean -- which is a real result (the day's
corrections DID land) and also the moment to be most suspicious of it: a checker
that returns green is only as good as its registry and its heuristic.
The other 4 were legitimate -- a scope document QUOTING the stale lines it exists
to catalogue, and a table row deliberately reciting "$3M, $100k ARR, $100k profit"
to make a scale-free argument. The marker heuristic is a 2-line window and cannot
read intent. Triage every hit by opening it; a tool that cries wolf and is trusted
blindly is worse than no tool. Report the real/flagged ratio when you cite a run.

Usage:  python3 tools/stale-claim-check.py [--registry ops/superseded-claims.tsv]
Exit 1 if any unqualified survivor is found, so it can gate a commit.
"""
import argparse, pathlib, re, sys

# Words that, near an occurrence, mean it is being discussed rather than asserted.
MARKERS = re.compile(
    r"retract|withdraw|supersed|corrected|struck|~~|no longer|was wrong|"
    r"double-count|formerly|previously|used to|historical|record of|NOT |wrongly|"
    r"refut|falsif|overturn|I asserted|first said|until 20|still reads|still says|"
    r"still asserted|error|defect|mistake|"
    # A claim carrying its OWN qualifier is not an unqualified survivor. Added
    # 2026-09-08: 8 of that run's 83 hits were the 175 THB fee quoted correctly,
    # i.e. next to the words that say it is unverified. A checker that flags the
    # careful phrasing teaches people to ignore it.
    r"second-hand|unconfirmed|widely reported|no amount|not stated|amount is not|"
    # An APPEND-ONLY document carries its own retracted claims by construction -- that is
    # what a revision log IS -- and the convention for marking them is a REVISED/AMENDED
    # banner on the superseded section. Added 2026-09-09 after gamedev-srv ran this against
    # a design document using `> **REVISED -- see 13.7.**` in twelve sections: the tool did
    # not know the word, so every correctly-marked revision read as an unqualified survivor.
    # Either the vocabulary learns the convention or every project changes its convention to
    # suit the tool; the first is obviously right. Append-only documents are this tool's
    # main habitat, not an edge case.
    r"revised|amended|rescinded|see .?[0-9]+\.[0-9]",
    re.I,
)
CONTEXT = 3  # lines either side -- 2 was too tight; a 'refuted' sat just outside it


def load(reg):
    """Returns (rows, malformed). A row is EXACTLY three tab-separated fields.

    `>= 3` used to be the test, and it silently kept the first three fields of a
    longer row. On 2026-09-08 that hid a real failure: three rows had been written
    in a five-column shape (date, who, claim, why, lesson), so field 1 -- the
    regex -- was the literal string "2026-09-08". Each matched every line in the
    repo mentioning that date: 69 of the run's 83 hits, while the three claims
    those rows existed to guard were guarded by nothing at all.

    A malformed row is therefore not a formatting nit. It is a WATCHER THAT IS
    WATCHING NOTHING, and it presents as the tool being noisy rather than as the
    tool being broken. So it is reported and it fails the run.
    """
    rows, malformed = [], []
    for n, line in enumerate(pathlib.Path(reg).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            malformed.append((n, len(parts), parts[0][:60]))
            continue
        rows.append((parts[0], parts[1], parts[2]))
    return rows, malformed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", default="ops/superseded-claims.tsv")
    ap.add_argument("--root", default=".")
    ap.add_argument("--no-default-excludes", action="store_true",
                    help="also scan vendored/build directories (node_modules, vendor, ...)")
    ap.add_argument("--exclude-dir", action="append", default=[],
                    help="additional directory name to skip; repeatable")
    a = ap.parse_args()
    DEFAULT_EXCLUDES = {"node_modules", "vendor", "third_party", ".venv", "venv",
                        "site-packages", "dist", "build", ".next", "target"}
    a.exclude_dirs = set(a.exclude_dir) | (set() if a.no_default_excludes else DEFAULT_EXCLUDES)

    rows, malformed = load(a.registry)
    if malformed:
        print(f"{len(malformed)} MALFORMED REGISTRY ROW(S) -- each is a watcher watching nothing:")
        for n, nf, first in malformed:
            print(f"  line {n}: {nf} tab-separated field(s), expected 3; field 1 = {first!r}")
        print("  Schema is: pattern <TAB> the live value <TAB> why it was superseded.")
        print("  A row in any other shape compiles its FIRST field as the regex, which is")
        print("  usually not the claim -- so the claim it was added for goes unwatched.\n")
    # VENDORED TREES ARE EXCLUDED BY DEFAULT -- added 2026-09-09.
    # A third-party changelog under node_modules cannot ASSERT anything about this project;
    # it is someone else's record of someone else's decision. Every hit there is noise by
    # construction, and noise is how a checker gets ignored -- the failure this file already
    # argues about at length, arriving by a different door. gamedev-srv's first run outside
    # the repo that grew this took SIX OF EIGHT hits from node_modules.
    # Anchoring the registry pattern also fixed their case; that does not make this optional,
    # because the exclusion holds regardless of pattern quality.
    excluded = 0
    def vendored(p):
        return bool(set(p.parts) & a.exclude_dirs)
    files = []
    for p in pathlib.Path(a.root).rglob("*.md"):
        if ".git" in p.parts:
            continue
        if vendored(p):
            excluded += 1
            continue
        files.append(p)
    if excluded:
        # Say what was skipped. A silent exclusion is indistinguishable from a clean tree.
        print(f"({excluded} file(s) in vendored/build directories excluded: "
              f"{', '.join(sorted(a.exclude_dirs))}. Use --no-default-excludes to scan them.)\n")

    # FILE-LEVEL SUPERSEDED BANNER -- added 2026-08-31.
    # A document whose OPENING carries an abandonment/retraction banner is a historical record. Flagging
    # every superseded figure inside it fires dozens of hits on a file that already says, at the top, that
    # it is dead. That is the failure mode this tool exists to avoid causing: "a check that fires every run
    # on the same known-good lines is how a tool gets ignored."
    # Only the FIRST 25 lines count -- a banner buried mid-file does not exempt the document, because a
    # reader quoting line 200 will not have seen it.
    BANNER = re.compile(r"^>?\s*#{0,3}\s*(⛔|⚠️)?\s*\**(ABANDONED|RETRACTED|SUPERSEDED|MOOT)\b", re.I | re.M)
    skipped = []
    live = []
    for f in files:
        try:
            head = "\n".join(f.read_text(encoding="utf-8", errors="replace").splitlines()[:25])
        except Exception:
            live.append(f); continue
        (skipped if BANNER.search(head) else live).append(f)
    files = live
    hits = 0
    for pat, live, why in rows:
        rx = re.compile(pat, re.I)
        for f in files:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            for i, line in enumerate(lines):
                if not rx.search(line):
                    continue
                window = "\n".join(lines[max(0, i - CONTEXT): i + CONTEXT + 1])
                if MARKERS.search(window):
                    continue          # discussed as superseded -- fine
                hits += 1
                print(f"{f}:{i+1}")
                print(f"    asserts : {line.strip()[:96]}")
                print(f"    live    : {live}   ({why})")
    if skipped:
        print(f"({len(skipped)} file(s) skipped -- opening banner marks them ABANDONED/RETRACTED/SUPERSEDED:")
        for f in sorted(skipped)[:8]:
            print(f"    {f.relative_to(a.root)}")
        if len(skipped) > 8:
            print(f"    ... and {len(skipped)-8} more")
        print(" a banner exempts the FILE, not a claim -- if one of these is actually live, remove its banner.)\n")
    if hits:
        print(f"\n{hits} unqualified survivor(s). A correction that has not reached "
              f"the sentence people quote has not landed.")
        return 1
    if malformed:
        print("No unqualified survivors among the rows that PARSED -- but the malformed")
        print("rows above were skipped entirely, so this run checked less than it looks.")
        return 1
    print("No unqualified survivors. (Absence here means the REGISTRY is clean --")
    print("it says nothing about claims nobody has added to it.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
