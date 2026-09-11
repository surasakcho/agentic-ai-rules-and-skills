#!/usr/bin/env python
"""Pull the shared rules into a repo -- by reference, pinned, never by copy.

A copied rule drifts silently and nobody notices until it contradicts the source. This links
to the shared repo and records the commit it was read at, so drift becomes detectable instead
of invisible.

    python -X utf8 retrieve.py --repo DIR                      # detect + recommend
    python -X utf8 retrieve.py --repo DIR --write              # write the CLAUDE.md block
    python -X utf8 retrieve.py --repo DIR --check              # exit 1 if the pin is stale
    python -X utf8 retrieve.py --repo DIR --shared DIR --write # use an existing clone

Exit 1 when --check finds drift or a missing block, so it can gate a commit.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SHARED_URL = "https://github.com/surasakcho/agentic-ai-rules-and-skills.git"
SHARED_WEB = "https://github.com/surasakcho/agentic-ai-rules-and-skills/blob"
BEGIN = "<!-- shared-lessons:begin -->"
END = "<!-- shared-lessons:end -->"

# Each category is selected only on evidence. A rule nobody needs is noise, and noise is how
# a CLAUDE.md stops being read.
#
# EXCEPT how-we-work. A category in MANDATORY is adopted by every project regardless of what
# the detectors find, and is listed first.
#
# The evidence rule is right for DOMAIN categories -- analytics, data-engineering, research,
# testing, coding all describe what a repo PRODUCES, and a repo that produces none of them
# genuinely does not need those rules. `how-we-work` is not a domain. It is the constant
# underneath every project: how the work is conducted, and how what it leaves behind behaves
# once nobody is watching. Two independent reasons it can never be evidence-selected:
#
#   - The operational half leaves nothing to detect. A job that keeps reporting success after
#     it stopped working does not announce itself in a dependency list or a directory name, and
#     the first cron entry, retry loop or background task arrives long AFTER the repo was
#     characterised -- by which time retrieval has already run and concluded it was irrelevant.
#   - The conduct half is circular to detect. Globbing for CLAUDE.md to decide whether agents
#     work here is checking for evidence of something the act of running this script already
#     proves -- and it failed precisely where it mattered most, denying a fresh repo with no
#     CLAUDE.md yet the rule on how to structure a new CLAUDE.md.
MANDATORY = ("how-we-work",)

DETECTORS = {
    "how-we-work": {
        "why": "every project has conduct and operation — how the work is done, and how what "
               "it leaves behind behaves once nobody is watching",
        "deps": (),
        "paths": (),
        "globs": (),
    },
    "analytics": {
        "why": "produces figures, tables or reported numbers",
        "deps": ("matplotlib", "seaborn", "plotly", "ggplot2", "altair", "bokeh", "d3"),
        "paths": ("figures", "figs", "plots", "charts", "reports"),
        "globs": ("**/*.ipynb",),
    },
    "data-engineering": {
        "why": "ingests or transforms data",
        "deps": ("pandas", "polars", "dbt", "pyarrow", "sqlalchemy", "duckdb", "geopandas"),
        "paths": ("data", "etl", "pipelines", "ingest", "warehouse"),
        "globs": ("**/*.csv", "**/*.parquet", "**/*.sql"),
    },
    "research": {
        "why": "carries research output that must stay reproducible",
        "deps": (),
        "paths": ("research", "papers", "literature", "notebooks"),
        "globs": ("**/*.bib", "**/Q-and-A.md", "**/LESSONS.md"),
    },
    "testing": {
        "why": "has a test suite whose checks must be able to fail",
        "deps": ("pytest", "vitest", "jest", "unittest", "rspec", "junit"),
        "paths": ("tests", "test", "spec", "__tests__"),
        "globs": ("**/test_*.py", "**/*.test.ts", "**/*.spec.ts"),
    },
    "coding": {
        "why": "contains source code that gets changed",
        "deps": (),
        # bin/ and *.sh matter: an ops repo whose entire content is shell scripts is
        # a repo that contains code, and omitting them made such repos adopt no coding
        # rules at all -- including one whose own headline defect was a hardcoded
        # constant, which is exactly what those rules cover.
        "paths": ("src", "lib", "app", "scripts", "pkg", "bin"),
        "globs": ("**/*.py", "**/*.ts", "**/*.js", "**/*.go", "**/*.rs", "**/*.java",
                  "**/*.sh", "**/*.bash"),
    },
}
# Directories holding code the repo did not write. Vendored bundles look exactly like
# first-party source to a glob, so every one of them has to be named here or the detector
# reports evidence the repo's authors have never edited and cannot act on.
# .obsidian: an Obsidian vault ships each installed plugin as a built main.js. A vault of
# pure prose matched "coding" on a downloaded reminder plugin -- same class as node_modules.
SKIP = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".next",
        ".obsidian", "site-packages", ".mypy_cache", ".pytest_cache"}


def run(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, encoding="utf-8",
                          errors="replace")


def default_branch(shared: Path) -> str:
    """The remote's default branch. Never assume 'main' -- ask the remote."""
    head = run("git", "-C", str(shared), "symbolic-ref", "--short", "-q",
               "refs/remotes/origin/HEAD").stdout.strip()
    return head.split("/", 1)[1] if "/" in head else "main"


def published_sha(shared: Path) -> str:
    """The SHA to pin: the remote's, or local HEAD when there is no remote at all.

    Preferring `origin/<default>` is the whole point -- a consumer must never be
    pinned to a commit only one machine has. But a clone with NO origin (a test
    fixture, or a deliberately local `--shared` checkout) has no published SHA, and
    there local HEAD is the only truth available. Falling back is correct there and
    nowhere else.
    """
    remote = run("git", "-C", str(shared), "rev-parse", "--short",
                 f"origin/{default_branch(shared)}")
    if remote.returncode == 0 and remote.stdout.strip():
        return remote.stdout.strip()
    return run("git", "-C", str(shared), "rev-parse", "--short", "HEAD").stdout.strip() or "HEAD"


def sync_shared(shared: Path) -> str:
    """Fetch, MERGE, push back -- then report the REMOTE's SHA, never the local one.

    Three properties, each closing a distinct way this went wrong in practice:

    1. MERGE, not `pull --ff-only`. A clone carrying local commits -- which is what
       happens the moment someone drafts a rule in it -- could not fast-forward, so
       the old code printed a WARNING and carried on against a silently stale
       mirror. Merging keeps both sides.
    2. PUSH BACK when the merge leaves us ahead. Otherwise a lesson written locally
       is stranded in a cache directory nobody backs up, which is the opposite of
       sharing it.
    3. PIN FROM THE REMOTE, after the push. The old code read the SHA from local
       HEAD, so a clone sitting on a branch pinned consumers to a commit that
       existed only on that machine, with rule links that 404 for everyone else --
       while both --check and --write reported success. Reading `origin/<default>`
       makes that structurally impossible: if the push fails, the pin falls back to
       the last genuinely published commit rather than an unreachable one.
    """
    branch = default_branch(shared)
    if run("git", "-C", str(shared), "fetch", "--quiet", "origin").returncode != 0:
        print("  WARNING: fetch failed; working from the cached copy")
        return published_sha(shared)

    cur = run("git", "-C", str(shared), "symbolic-ref", "--short", "-q", "HEAD").stdout.strip()
    if cur != branch:
        if run("git", "-C", str(shared), "status", "--porcelain").stdout.strip():
            raise SystemExit(
                f"ERROR: shared clone at {shared} is on '{cur or 'detached HEAD'}' with "
                f"uncommitted changes.\n       Commit or stash them, then re-run.")
        run("git", "-C", str(shared), "checkout", "--quiet", branch)

    m = run("git", "-C", str(shared), "merge", "--no-edit", "--quiet", f"origin/{branch}")
    if m.returncode != 0:
        raise SystemExit(
            f"ERROR: merging origin/{branch} into the shared clone conflicted.\n"
            f"       Resolve it in {shared}, then re-run.\n"
            f"       {m.stderr.strip().splitlines()[-1] if m.stderr.strip() else ''}")

    ahead = run("git", "-C", str(shared), "rev-list", "--count",
                f"origin/{branch}..HEAD").stdout.strip()
    if ahead and ahead != "0":
        print(f"  shared clone is {ahead} commit(s) ahead of origin -- pushing back")
        if run("git", "-C", str(shared), "push", "--quiet", "origin", branch).returncode != 0:
            print(f"  WARNING: push failed, so those {ahead} commit(s) stay local.\n"
                  f"           Pinning to the last PUBLISHED commit instead -- a consumer must\n"
                  f"           never be pinned to a commit only this machine has.")
        else:
            run("git", "-C", str(shared), "fetch", "--quiet", "origin")

    return published_sha(shared)


def ensure_shared(shared: Path, url: str, offline: bool) -> Path:
    """Clone the shared repo if it is absent. Syncing is sync_shared()'s job."""
    if shared.exists() and (shared / ".git").exists():
        return shared
    if offline:
        raise SystemExit(f"ERROR: no shared repo at {shared} and --offline was given")
    shared.parent.mkdir(parents=True, exist_ok=True)
    print(f"  cloning {url}")
    r = run("git", "clone", "--quiet", url, str(shared))
    if r.returncode != 0:
        raise SystemExit(f"ERROR: clone failed: {r.stderr.strip()}")
    return shared


def verify_links(shared: Path, sha: str, rules) -> None:
    """Every linked rule must exist at the SHA being written. Cheap, and it is the
    last line of defence: it catches a bad pin even if the sync above is bypassed."""
    missing = [f"rules/{cat}/{name}" for cat in rules for name in rules[cat]
               if run("git", "-C", str(shared), "cat-file", "-e",
                      f"{sha}:rules/{cat}/{name}").returncode != 0]
    if missing:
        raise SystemExit(
            f"ERROR: {len(missing)} rule file(s) do not exist at {sha} -- refusing to write "
            f"links that 404:\n" + "\n".join(f"         {m}" for m in missing))


def dep_text(repo: Path) -> str:
    """Everything a dependency could be declared in, concatenated and lowercased."""
    names = ("requirements.txt", "pyproject.toml", "setup.py", "environment.yml",
             "package.json", "Gemfile", "go.mod", "Cargo.toml", "DESCRIPTION")
    out = []
    for n in names:
        p = repo / n
        if p.exists():
            out.append(p.read_text(encoding="utf-8", errors="replace").lower())
    return "\n".join(out)


def detect(repo: Path):
    """Return {category: [evidence, ...]}: every MANDATORY category, plus any other category
    with actual evidence."""
    deps = dep_text(repo)
    dirs = {p.name.lower() for p in repo.rglob("*")
            if p.is_dir() and not any(s in p.parts for s in SKIP)}
    found = {}
    for cat, spec in DETECTORS.items():
        evidence = []
        for d in spec["deps"]:
            if re.search(rf"\b{re.escape(d)}\b", deps):
                evidence.append(f"dependency '{d}'")
        for d in spec["paths"]:
            if d.lower() in dirs:
                evidence.append(f"{d}/ directory")
        for g in spec["globs"]:
            hit = next((p for p in repo.glob(g)
                        if not any(s in p.parts for s in SKIP)), None)
            if hit:
                evidence.append(f"{hit.relative_to(repo).as_posix()}")
        if evidence:
            found[cat] = evidence[:3]
    # Mandatory categories are adopted whether or not anything was detected. Any evidence that
    # WAS found is kept after the marker -- informative, but never load-bearing.
    for cat in MANDATORY:
        found[cat] = ["mandatory for every project"] + found.get(cat, [])[:2]
    return found



# ---------------------------------------------------------------------------------------
# The selection record. Declines and hand-adoptions are properties of the CONSUMING repo,
# not of the shared rules, so they live with the repo and are version-controlled.
#
# Two failures this exists for, both observed:
#   - A category the detectors miss must be adoptable BY HAND and must survive --write.
#     `analytics` was hand-added OUTSIDE the generated block precisely because --write would
#     wipe it, and then drifted two pins behind while the managed block moved twice.
#   - A rule considered and rejected left no trace, so the same judgement was re-made from
#     nothing at every retrieval. Declined and never-seen looked identical.
#
# Resurfacing is MANUAL and that is a ruling, not an oversight: "I will ask to review all
# rules again." No timer, no repo-state trigger. Do not add one because it seems helpful.
SELECTION = Path(".claude") / "lessons-selection.tsv"
SEL_HEADER = "# verb\tscope\tdate\tsha\treason\n"


def sel_path(repo: Path) -> Path:
    return repo / SELECTION


def read_selection(repo: Path):
    """-> (declined:set[str], adopted:dict[str,str], rows:list[tuple]).

    A scope is a category ("testing") or one rule inside it ("coding/foo.md").
    A malformed row is NAMED and fatal, never silently skipped -- a selection file that
    quietly drops a row would re-adopt something a human had declined.
    """
    p = sel_path(repo)
    declined, adopted, rows = set(), {}, []
    if not p.exists():
        return declined, adopted, rows
    for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 5:
            raise SystemExit(f"ERROR: {p}:{i} has {len(parts)} fields, expected 5 "
                             f"(verb/scope/date/sha/reason). Refusing to guess which "
                             f"rules were declined.")
        verb, scope, date, at, reason = (x.strip() for x in parts)
        if verb == "DECLINE":
            declined.add(scope)
        elif verb == "ADOPT":
            adopted[scope] = reason
        else:
            raise SystemExit(f"ERROR: {p}:{i} unknown verb {verb!r} (expected DECLINE/ADOPT)")
        rows.append((verb, scope, date, at, reason))
    return declined, adopted, rows


def write_selection(repo: Path, verb: str, scope: str, sha: str, reason: str):
    p = sel_path(repo)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(SEL_HEADER, encoding="utf-8")
    if "\t" in reason or "\n" in reason:
        raise SystemExit("ERROR: a reason may not contain a tab or a newline")
    if not reason:
        raise SystemExit(f"ERROR: --{verb.lower()} needs --reason. A decision with no reason "
                         f"is one nobody can review later, which is the whole failure this "
                         f"record exists to fix.")
    date = subprocess.run(["date", "-u", "+%Y-%m-%d"], capture_output=True,
                          encoding="utf-8").stdout.strip()
    with p.open("a", encoding="utf-8") as f:
        f.write(f"{verb}\t{scope}\t{date}\t{sha}\t{reason}\n")


def apply_selection(selected, rules, declined, adopted, shared):
    """Remove declined scopes; add hand-adopted categories. Returns (selected, rules)."""
    for cat in list(selected):
        if cat in declined:
            if cat in MANDATORY:
                raise SystemExit(f"ERROR: {cat} is mandatory for every project and cannot be "
                                 f"declined. Remove the row from {SELECTION.as_posix()}.")
            selected.pop(cat, None)
            rules.pop(cat, None)
    for cat, reason in adopted.items():
        if cat in selected:
            continue
        d = shared / "rules" / cat
        if not d.exists():
            raise SystemExit(f"ERROR: {SELECTION.as_posix()} adopts rules/{cat}, which does "
                             f"not exist in the shared repo.")
        selected[cat] = [f"adopted by hand -- {reason}"]
        rules[cat] = sorted(p.name for p in d.glob("*.md"))
    for cat in list(rules):
        rules[cat] = [n for n in rules[cat] if f"{cat}/{n}" not in declined]
        if not rules[cat]:
            selected.pop(cat, None)
            rules.pop(cat, None)
    return selected, rules


def rules_for(shared: Path, cats):
    """Every rule file under each selected category. Missing category = hard error: it means
    the shared repo moved and this skill is pointing at nothing."""
    out = {}
    for cat in cats:
        d = shared / "rules" / cat
        if not d.exists():
            raise SystemExit(f"ERROR: shared repo has no rules/{cat} -- it has been "
                             f"reorganised and this skill is out of date")
        out[cat] = sorted(p.name for p in d.glob("*.md"))
    return out


def build_block(shared: Path, sha: str, selected, rules):
    lines = [BEGIN,
             "",
             "## Shared working rules",
             "",
             f"Adopted from [agentic-ai-rules-and-skills]({SHARED_WEB.rsplit('/blob', 1)[0]}) "
             f"at `{sha}`. **Linked, not copied** — a copied rule drifts out of agreement with "
             f"its source and nobody notices. Refresh with `/retrieve-lessons`.",
             ""]
    # Mandatory categories lead, in declared order; detected ones follow alphabetically.
    order = ([c for c in MANDATORY if c in rules]
             + sorted(c for c in rules if c not in MANDATORY))
    for cat in order:
        if cat in MANDATORY:
            lines.append(f"**{cat}** — **mandatory, adopted by every project**: "
                         f"{DETECTORS[cat]['why']}.")
        else:
            lines.append(f"**{cat}** — selected because this repo {DETECTORS[cat]['why']} "
                         f"({', '.join(selected[cat])}).")
        lines.append("")
        for name in rules[cat]:
            title = name[:-3].replace("-", " ")
            lines.append(f"- [{title}]({SHARED_WEB}/{sha}/rules/{cat}/{name})")
        lines.append("")
    lines += ["*The pin is the point: if the shared repo has moved on, "
              "`retrieve.py --check` fails and you re-read what changed.*", "", END]
    return "\n".join(lines)


def rules_changed(shared: Path, old_sha: str, new_sha: str):
    """Which rule files differ between two SHAs. Empty list = the pin is behind but
    NOTHING A CONSUMER LINKS TO has moved.

    This distinction is the whole point and it was learned the expensive way. `--check`
    used to compare repo HEAD, so a commit touching only `skills/` marked every consumer
    stale -- and the remedy it recommended was provably a no-op, because skills reach
    sessions by symlink and are live on pull regardless of any pin. One observed case:
    78 links would have been rewritten to say nothing different.

    A checker whose recommended fix changes nothing is how a checker gets muted, and a
    muted checker misses the commit that DID move a rule.
    """
    r = run("git", "-C", str(shared), "diff", "--name-only",
            f"{old_sha}..{new_sha}", "--", "rules/")
    if r.returncode != 0:
        # An unknown SHA is not "no change" -- it is "cannot tell", and those must not
        # look the same. Returning None forces the caller to say so.
        return None
    return [l for l in r.stdout.splitlines() if l.strip()]


def parse_block(text: str):
    """The categories and rule files a CLAUDE.md block ALREADY links, read back out of it.

    This is what makes re-pinning separable from re-detecting. `detect()` asks "what should
    this repo adopt?", which is judgement and is wrong in both directions today. This asks
    "what did someone already decide it adopts?", which is a fact recorded in the file.
    Advancing a SHA over a set a human chose is mechanical; re-running detection under a
    cron job is not, and conflating them is why nothing could be automated at all.
    """
    m = re.search(re.escape(BEGIN) + r"(.*?)" + re.escape(END), text, re.S)
    if not m:
        return None
    body = m.group(1)
    out = {}
    for cat, name in re.findall(r"/rules/([a-z-]+)/([a-z0-9-]+\.md)\)", body):
        out.setdefault(cat, set()).add(name)
    if not out:
        return None
    # The evidence string a human reviewed when the category was adopted, kept verbatim.
    # Re-deriving it here would be detection by the back door, and detection is the half
    # that needs judgement.
    ev = {c: [e.strip() for e in m2.split(",")]
          for c, m2 in re.findall(r"\*\*([a-z-]+)\*\* — selected because this repo [^(]*\(([^)]*)\)", body)}
    return {"rules": {c: sorted(v) for c, v in out.items()}, "evidence": ev}


def read_pin(text: str):
    m = re.search(re.escape(BEGIN) + r".*?at `([0-9a-f]{6,40})`", text, re.S)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="the repo adopting the rules")
    ap.add_argument("--shared", help="path to an existing clone (default: a local cache)")
    ap.add_argument("--url", default=SHARED_URL)
    ap.add_argument("--write", action="store_true", help="write the block into CLAUDE.md")
    ap.add_argument("--check", action="store_true", help="exit 1 if the pin is stale/missing")
    ap.add_argument("--offline", action="store_true", help="never touch the network")
    ap.add_argument("--json", action="store_true", help="machine-readable detection output")
    ap.add_argument("--repin", action="store_true",
                    help="advance the SHA over the categories ALREADY in the block; never "
                         "re-runs detection. No-op unless a rule actually moved (--force overrides)")
    ap.add_argument("--review", action="store_true",
                    help="show what WOULD be adopted, with evidence and any prior decisions, "
                         "and write nothing. The review step before --write")
    ap.add_argument("--all", action="store_true",
                    help="with --review: re-present previously declined scopes too, with the "
                         "reasons given. Resurfacing declines is MANUAL and this is the way")
    ap.add_argument("--decline", metavar="SCOPE",
                    help="record a decline: a category ('testing') or one rule "
                         "('coding/foo.md'). Needs --reason")
    ap.add_argument("--adopt", metavar="CATEGORY",
                    help="adopt a category the detectors did not find. Needs --reason")
    ap.add_argument("--reason", default="", help="why, in your own words -- recorded verbatim")
    ap.add_argument("--force", action="store_true",
                    help="with --repin: rewrite the block even when no rule changed")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.exists():
        raise SystemExit(f"ERROR: no such repo: {repo}")
    shared = Path(args.shared).resolve() if args.shared else \
        Path.home() / ".claude" / "cache" / "agentic-ai-rules-and-skills"
    shared = ensure_shared(shared, args.url, args.offline or bool(args.shared))
    # The pin is the REMOTE's SHA, never local HEAD -- see sync_shared().
    sha = published_sha(shared) if (args.offline or bool(args.shared)) \
        else sync_shared(shared)

    if args.decline or args.adopt:
        if args.decline and args.adopt:
            raise SystemExit("ERROR: --decline and --adopt in one run; do them separately so "
                             "each lands as its own reviewable row")
        verb, scope = ("DECLINE", args.decline) if args.decline else ("ADOPT", args.adopt)
        if verb == "ADOPT" and "/" in scope:
            raise SystemExit("ERROR: --adopt takes a CATEGORY, not a rule. A category is "
                             "adopted whole; decline the rules inside it that do not fit.")
        if verb == "DECLINE" and scope in MANDATORY:
            raise SystemExit(f"ERROR: {scope} is mandatory for every project.")
        write_selection(repo, verb, scope, sha, args.reason.strip())
        print(f"recorded: {verb} {scope} -- {args.reason.strip()}")
        print(f"  in {sel_path(repo)}")
        print(f"  run --write to apply it to the block")
        return 0

    # --repin runs BEFORE detect() is ever called, and that placement is the guarantee.
    # "Never re-runs detection" is a structural property here, not a promise in a docstring:
    # there is no detection result in scope to use by accident.
    if args.repin:
        cm = repo / "CLAUDE.md"
        existing = cm.read_text(encoding="utf-8", errors="replace") if cm.exists() else ""
        parsed = parse_block(existing)
        if parsed is None:
            raise SystemExit(
                f"ERROR: no shared-lessons block in {cm} -- nothing to re-pin.\n"
                f"       First-time adoption chooses CATEGORIES, which is judgement. "
                f"Run --write and read what it proposes.")
        pin = read_pin(existing)
        old_rules, evidence = parsed["rules"], parsed["evidence"]

        if pin == sha and not args.force:
            print(f"already pinned at {sha} -- nothing to do")
            return 0
        changed = rules_changed(shared, pin, sha) if pin else None
        if pin and changed is None and not args.force:
            raise SystemExit(f"ERROR: cannot read the diff {pin}..{sha} -- refusing to re-pin "
                             f"on an unverifiable comparison. Use --force only if you know why.")
        if pin and not changed and not args.force:
            print(f"held at {pin} (shared repo {sha}): no rule moved, so re-pinning would "
                  f"rewrite {sum(len(v) for v in old_rules.values())} links to say nothing "
                  f"different")
            return 0

        new_rules = rules_for(shared, sorted(old_rules))
        # A rule that VANISHED is the one case a human must see. verify_links cannot catch
        # it -- that checks the links about to be written, and a deleted rule simply stops
        # being in the list. A rule is deleted when later experience contradicted it, so a
        # disappearance can mean this repo is currently doing something now known to be wrong.
        vanished = {c: [n for n in names if n not in new_rules.get(c, [])]
                    for c, names in old_rules.items()}
        vanished = {c: v for c, v in vanished.items() if v}
        if vanished:
            raise SystemExit(
                "ERROR: rule(s) this repo links no longer exist at {}:\n{}\n"
                "       A rule contradicted by later experience is DELETED, not hedged -- so\n"
                "       this can mean something this repo does is now known to be wrong.\n"
                "       Read the deletion, then re-run with --write.".format(
                    sha, "\n".join(f"         rules/{c}/{n}" for c, v in vanished.items() for n in v)))

        added = {c: [n for n in new_rules[c] if n not in old_rules[c]] for c in old_rules}
        added = {c: v for c, v in added.items() if v}
        verify_links(shared, sha, new_rules)
        block = build_block(shared, sha, evidence, new_rules)
        new = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), block, existing, flags=re.S)
        cm.write_text(new, encoding="utf-8")
        n_links = sum(len(v) for v in new_rules.values())
        print(f"re-pinned {cm} {pin} -> {sha} "
              f"({len(new_rules)} categories, {n_links} links, categories unchanged)")
        for c, v in added.items():
            for n in v:
                print(f"  new rule in an adopted category: rules/{c}/{n}")
        return 0

    selected = detect(repo)
    # No "nothing matched" path any more: MANDATORY is non-empty, so `selected` never is. The
    # old early return here could not fire once operations/agent-workflow became mandatory, and
    # a branch that cannot fire is exactly what rules/testing/validations-must-fail.md is about.
    # Assert the invariant instead of pretending to handle its negation.
    assert selected, "MANDATORY is empty -- every project must adopt at least the mandatory rules"
    rules = rules_for(shared, selected)
    declined, adopted, sel_rows = read_selection(repo)
    selected, rules = apply_selection(selected, rules, declined, adopted, shared)
    verify_links(shared, sha, rules)

    if args.review:
        print(f"\nshared repo at {sha}\n")
        print("WOULD ADOPT:")
        for cat in ([c for c in MANDATORY if c in selected]
                    + sorted(c for c in selected if c not in MANDATORY)):
            print(f"  {cat:18} {', '.join(selected[cat])}")
            for name in rules[cat]:
                print(f"      - {name}")
        skipped = [c for c in DETECTORS
                   if c not in selected and c not in declined
                   and (shared / "rules" / c).exists()]
        if skipped:
            print("\nNOT ADOPTED -- no evidence found. Adopt by hand with "
                  "--adopt CAT --reason ...:")
            for c in skipped:
                print(f"  {c:18} {DETECTORS[c]['why'][:70]}")
        if declined:
            print("\nPREVIOUSLY DECLINED -- not offered again unless you ask:")
            for verb, scope, date, at, reason in sel_rows:
                if verb != "DECLINE":
                    continue
                if args.all:
                    print(f"  {scope:34} {date}  {reason}")
                else:
                    print(f"  {scope:34} {date}  (--review --all shows why)")
        print("\nNothing was written. --write applies this; "
              "--decline SCOPE --reason ... changes it.")
        return 0

    if args.json:
        print(json.dumps({"sha": sha, "selected": selected, "rules": rules}, indent=2))
        return 0

    print(f"\nshared repo at {sha}\n")
    for cat in ([c for c in MANDATORY if c in selected]
                + sorted(c for c in selected if c not in MANDATORY)):
        print(f"  {cat:18} {', '.join(selected[cat])}")
        for name in rules[cat]:
            print(f"      - {name}")

    cm = repo / "CLAUDE.md"
    existing = cm.read_text(encoding="utf-8", errors="replace") if cm.exists() else ""
    pin = read_pin(existing)

    if args.check:
        if BEGIN not in existing:
            print(f"\nPROBLEM: no shared-lessons block in {cm.name}. Run --write.")
            return 1
        if pin == sha:
            print(f"\nPin is current ({sha}).")
            return 0
        changed = rules_changed(shared, pin, sha)
        if changed is None:
            # Cannot tell is not the same as no change, and they must not print the same.
            print(f"\nPROBLEM: pinned at {pin}, shared repo is at {sha}, and the diff "
                  f"between them could not be read (unknown SHA? shallow clone?). "
                  f"Unverifiable is not verified -- resolve it rather than assuming.")
            return 1
        if not changed:
            print(f"\nPin is behind ({pin} -> {sha}) but NO RULE MOVED -- holding is correct.\n"
                  f"  Re-pinning would rewrite every link in the block to say nothing "
                  f"different. Skills are not pinned: they reach sessions by symlink and "
                  f"are already live.")
            return 0
        print(f"\nPROBLEM: pinned at {pin}, shared repo is at {sha}, "
              f"and {len(changed)} rule file(s) moved:")
        for f in changed:
            print(f"         {f}")
        print("\n  Read what changed, then --repin (same categories) or --write (re-detect).")
        return 1

    block = build_block(shared, sha, selected, rules)
    if not args.write:
        print(f"\n--- would write into {cm.name} (pass --write) ---\n")
        print(block)
        return 0

    if BEGIN in existing and END in existing:
        new = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), block, existing, flags=re.S)
        action = f"refreshed (was {pin})"
    else:
        new = (existing.rstrip() + "\n\n" + block + "\n") if existing else block + "\n"
        action = "added"
    cm.write_text(new, encoding="utf-8")
    print(f"\n{action} the shared-lessons block in {cm} -- pinned at {sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
