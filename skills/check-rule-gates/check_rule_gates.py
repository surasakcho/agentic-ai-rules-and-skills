#!/usr/bin/env python3
"""Which rules declare a gate that does not exist?

WHAT THIS IS FOR. Every rule in this corpus ends with a machine-readable
`## Enforcement` clause carrying a `verdict:` -- interposed, deferred, narrowed,
irreducible. **A verdict is a classification, not an implementation.** It records
what the rule COULD be reduced to, decided by a reader once, in a reduction pass.
Nothing has ever checked whether the gate it describes was then built.

That gap is worse than an honest blank. A rule declaring `verdict: interposed`
with no gate deployed reads, to anyone skimming the corpus, as coverage -- the
block looks like enforcement and is prose. A rule that says plainly it cannot be
gated is more useful, because nobody mistakes it for a control.

So this reports four states, never two:

  gated        a gateable verdict, and the implementation it names EXISTS
  UNGATED      a gateable verdict, and no implementation found -- the real gap
  unavailable  honestly declares it cannot be gated (irreducible / structural)
  UNKNOWN      no clause, an unparseable one, or a linkage that cannot be read

Exit codes -- three states, not two:

  0   clean: nothing UNGATED, nothing UNKNOWN
  1   at least one UNGATED. This is a gate; a declared-but-absent gate is a gap
  2   no UNGATED, but at least one UNKNOWN

UNGATED vs UNKNOWN, and why the distinction is load-bearing. If a clause will not
parse, or names its implementation in prose this script cannot resolve, the
answer is UNKNOWN and the reason is printed. Reporting "UNGATED" for a rule whose
linkage merely could not be READ would be a false alarm, and false alarms are how
checks get switched off. An unread corpus is not a clean one -- hence exit 2
rather than exit 0.

READ-ONLY, ALWAYS. It opens files and parses them. It never writes, chmods,
renames, or touches git. Safe from cron, from CI, or against a live tree.

PATHS ARE ARGUMENTS, NEVER LITERALS. A machine path baked into a shared skill
publishes a username and a directory layout. The corpus root is an argument; so
is every place a gate might live. Nothing about any particular estate is written
down here -- see `--config` and `SKILL.md`.
"""
import argparse
import ast
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# The verdict vocabulary, and the one judgement call in it.
#
# `interposed`, `deferred` and `narrowed` all name a mechanism that someone has
# to build, so each OWES an implementation and is UNGATED without one.
#
# `irreducible` means no artifact exists to look at -- judgement, tone,
# disposition. Nothing is owed and the rule is `unavailable`, which is a clean
# state, not a failure.
#
# `structural` is the contestable one, and it is flagged rather than quietly
# decided. It means the capability itself is removed -- no credential mounted,
# no socket exposed -- so there is no rule-layer mechanism to point at, and it is
# classified `unavailable` here. The corpus this was written against contains
# ZERO structural clauses, so that branch has never been exercised against real
# data. If structural rules ever appear and an estate wants them to owe an
# implementation, move the name into GATEABLE -- one line, stated here so the
# choice is visible rather than buried.
# ---------------------------------------------------------------------------
GATEABLE = {"interposed", "deferred", "narrowed"}
UNAVAILABLE = {"irreducible", "structural"}
KNOWN_VERDICTS = GATEABLE | UNAVAILABLE

# The linkage key. NOT invented here -- the corpus's own clause format already
# specifies `implemented_by`, and the reduction pass that introduced it says why:
# "a rule and its enforcement drifting apart is the failure this whole format
# exists to prevent". Adding a second key for the same job would create exactly
# the drift it names.
LINK_KEY = "implemented_by"

# A token is path-like if it contains a separator. Anything else is tried only as
# an EXACT provider identifier -- see resolve(). Loose matching is the failure
# mode that matters most here: a wrong link reports a gate that does not exist,
# which is the very thing this script was written to detect.
PATH_TOKEN = re.compile(r"[A-Za-z0-9_.~-]+(?:/[A-Za-z0-9_.~-]*)+")

ENFORCEMENT_HEAD = re.compile(r"^##\s+Enforcement\s*$", re.M)
YAML_FENCE = re.compile(r"^```ya?ml\s*$(.*?)^```\s*$", re.M | re.S)


def istty():
    try:
        return sys.stdout.isatty()
    except Exception:
        return False


def paint(code, text):
    return f"\033[{code}m{text}\033[0m" if istty() else text


red = lambda s: paint("31", s)
amber = lambda s: paint("33", s)
green = lambda s: paint("32", s)


# ---------------------------------------------------------------------------
# Clause parsing.
#
# Hand-parsed, not via PyYAML, and that is deliberate on two counts. No skill in
# this repo takes a third-party import, and a skill that cannot run on a bare
# interpreter is a skill that reports CANNOT RUN instead of an answer. The clause
# grammar is also provably flat -- every clause in the corpus is single-line
# `key: value` pairs with no block scalars, no nesting and no lists -- so a real
# YAML parser would buy nothing and cost a dependency.
#
# Anything this parser cannot make sense of becomes UNKNOWN with its reason
# printed. It never guesses.
# ---------------------------------------------------------------------------
def parse_clause(text):
    """(fields, error). fields is None when there is nothing parseable."""
    head = ENFORCEMENT_HEAD.search(text)
    if not head:
        return None, "no '## Enforcement' section"
    fence = YAML_FENCE.search(text, head.end())
    if not fence:
        return None, "'## Enforcement' section with no ```yaml block"

    fields = {}
    for raw in fence.group(1).splitlines():
        line = raw.split("#", 1)[0].rstrip() if not raw.strip().startswith("#") else ""
        if not line.strip():
            continue
        if ":" not in line:
            continue
        if line[:1].isspace():
            # Indentation means nesting or a list, which this grammar does not
            # have. Refuse rather than silently flatten it.
            return None, "clause is nested or a list; this parser reads flat keys only"
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "'\"":
            val = val[1:-1]
        fields[key] = val
    if not fields:
        return None, "```yaml block is empty"
    return fields, None


# ---------------------------------------------------------------------------
# Providers -- how "does this gate exist?" is answered without hardcoding one
# estate's layout.
#
# A gate lives somewhere different in every estate: a deny list in a settings
# file, a table of handlers in a hook, a labelled block in a commit hook, a
# script in a tools directory. None of that is universal, so none of it is
# written down here. A provider is DECLARED by the caller and enumerates the gate
# identifiers it can see. The checker then asks one exact question: does the
# string this rule names appear among them?
# ---------------------------------------------------------------------------
def provider_json_list(path, arg):
    """Entries of a list at a dotted key in a JSON file (e.g. permissions.deny)."""
    with open(path, "r", encoding="utf-8") as fh:
        node = json.load(fh)
    for part in arg.split("."):
        node = node[part]
    if not isinstance(node, list):
        raise ValueError(f"{arg} is not a list")
    return [str(x) for x in node]


def provider_py_tuple(path, arg):
    """First string of each entry in a module-level tuple/list named `arg`.

    Parsed with `ast`, never imported and never exec'd: reading a file must not
    be able to run it. A gate registry is exactly the file an attacker would
    want a checker to import.
    """
    tree = ast.parse(open(path, "r", encoding="utf-8").read())
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if arg not in names:
            continue
        if not isinstance(node.value, (ast.Tuple, ast.List)):
            continue
        for elt in node.value.elts:
            if isinstance(elt, (ast.Tuple, ast.List)) and elt.elts:
                first = elt.elts[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    out.append(first.value)
            elif isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                out.append(elt.value)
    if not out:
        raise ValueError(f"no string entries found in tuple '{arg}'")
    return out


def provider_regex(path, arg):
    """Group 1 of every match of `arg` in a text file. For labelled blocks."""
    rx = re.compile(arg, re.M)
    body = open(path, "r", encoding="utf-8", errors="replace").read()
    out = [m.group(1).strip() for m in rx.finditer(body) if m.lastindex]
    if not out:
        raise ValueError("regex matched nothing")
    return out


def provider_tree(path, arg):
    """Every file under a directory matching a glob; id is the relative path."""
    import fnmatch
    pat = arg or "*"
    out = []
    for base, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if fnmatch.fnmatch(f, pat):
                out.append(os.path.relpath(os.path.join(base, f), path).replace(os.sep, "/"))
    return out


PROVIDERS = {
    "json-list": provider_json_list,
    "py-tuple": provider_py_tuple,
    "regex": provider_regex,
    "tree": provider_tree,
}


# ---------------------------------------------------------------------------
# Config. Line-oriented, '#' comments, two directives:
#
#   root     <label> <path>
#   provider <label> <kind> <path> [arg]
#
# Relative paths resolve against the CONFIG FILE's directory, so a config can sit
# beside the estate it describes and travel with it.
# ---------------------------------------------------------------------------
def read_config(path):
    roots, provs, errs = [], [], []
    base = os.path.dirname(os.path.abspath(path))
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for n, raw in enumerate(fh, 1):
            # A '#' only starts a comment at the start of a line or after
            # whitespace. A blanket split would truncate a provider regex such
            # as '^#\s*GATE' at its first character -- the config directive most
            # likely to need one.
            line = re.split(r"(?:^|\s)#", raw, maxsplit=1)[0].strip()
            if not line:
                continue
            parts = line.split(None, 3)
            kind = parts[0]
            if kind == "root" and len(parts) >= 3:
                roots.append((parts[1], os.path.normpath(os.path.join(base, parts[2]))))
            elif kind == "provider" and len(parts) >= 4:
                label, pkind, ppath = parts[1], parts[2], parts[3]
                arg = ""
                if " " in ppath:
                    ppath, arg = ppath.split(None, 1)
                if pkind not in PROVIDERS:
                    errs.append(f"line {n}: unknown provider kind '{pkind}'")
                    continue
                provs.append((label, pkind, os.path.normpath(os.path.join(base, ppath)), arg))
            else:
                errs.append(f"line {n}: unrecognised directive '{line[:40]}'")
    return roots, provs, errs


# ---------------------------------------------------------------------------
# Resolution -- the hard part, and the part most likely to lie.
#
# TWO MATCHERS, BOTH EXACT. Nothing fuzzy, nothing by similarity of name.
#
#   1. A path-like token (contains '/') must EXIST on disk under a declared root.
#   2. A provider identifier must appear in the value as a complete token --
#      bounded, so 'bulk-stage' never matches inside 'no-bulk-stage-yet'.
#
# There is deliberately NO rule-slug-to-gate-name inference. It is the obvious
# shortcut and it is the one that breaks the tool: a rule named
# `nothing-leaves-git-without-permission` sits near a gate named `bulk-stage`,
# and any heuristic confident enough to link those is confident enough to invent
# links that are wrong. A wrong link reports coverage that does not exist, which
# is precisely the defect this checker exists to find -- so an unresolvable
# linkage is reported as UNKNOWN and handed to a person.
# ---------------------------------------------------------------------------
def resolve(value, roots, ids):
    """(status, evidence).  status in {'hit','dangling','unreadable'}"""
    tokens = PATH_TOKEN.findall(value)

    for pid, owner in ids.items():
        if re.search(r"(?<![A-Za-z0-9_./-])" + re.escape(pid) + r"(?![A-Za-z0-9_./-])", value):
            return "hit", f"{owner}: {pid}"

    if not tokens:
        return "unreadable", ""

    for tok in tokens:
        for label, root in roots:
            if os.path.exists(os.path.join(root, tok)):
                return "hit", f"{label}/{tok}"
    return "dangling", ", ".join(tokens[:3])


# ---------------------------------------------------------------------------
# Report buffering. Every finding is filed under a group and printed at the end,
# so one run produces a grouped worklist rather than an interleaved trace.
# Detail lines are kept narrow on purpose: this gets read on a phone.
# ---------------------------------------------------------------------------
GROUP_ORDER = [
    "corpus",
    "UNGATED -- declares a gate, none found",
    "UNKNOWN -- could not be determined",
    "gated",
    "unavailable",
    "gates no rule claims",
]

# The reasoning belongs to the GROUP, not to each finding. The first draft
# repeated a seven-line rationale under all 45 ungated rules -- 315 lines of
# identical text with the worklist buried in it, which is the interleaved trace
# this report format exists to avoid. Said once per group, each finding stays one
# line and the whole thing fits on a phone.
PREAMBLE = {
    GROUP_ORDER[1]: [
        "Each declares a gateable verdict and names no implementation,",
        "so the clause reads as coverage and nothing was shown to",
        "enforce it.",
        "'-> MISSING' instead marks a clause that DOES name one which",
        "no declared root contains: a broken link, not a gate.",
        "fix, per rule: build it and add",
        "    implemented_by: <path or declared gate id>",
        "  -- or change the verdict to say it cannot be gated. An",
        "  honest 'irreducible' is a cleaner state than a",
        "  classification standing in for a control.",
    ],
    GROUP_ORDER[2]: [
        "Not judged ungated -- judged unreadable, which is a different",
        "answer and is why this exits 2 rather than 0. A rule with no",
        "clause is either irreducible BY DESIGN (the reduction pass",
        "records the absence as the finding) or was never assessed at",
        "all. The file does not say which, so neither is assumed.",
    ],
    GROUP_ORDER[3]: [
        "The named implementation EXISTS. That is the whole claim --",
        "not that it is installed, wired up, or has ever fired.",
    ],
    GROUP_ORDER[5]: [
        "Gates that exist and that no rule names. Never a failure -- a",
        "gate may enforce something written down elsewhere, or nowhere.",
        "Listed so the inverse gap is visible too.",
    ],
}


class Report:
    def __init__(self):
        self.buf = {}
        self.ungated = 0
        self.unknown = 0

    def _file(self, group, sev, head, details):
        text = "%-9s %s\n" % (sev, head)
        for d in details:
            if d:
                text += "          %s\n" % d
        self.buf.setdefault(group, "")
        self.buf[group] += text

    def ungate(self, head, *d):
        self._file(GROUP_ORDER[1], "UNGATED", head, d)
        self.ungated += 1

    def unk(self, head, *d):
        self._file(GROUP_ORDER[2], "UNKNOWN", head, d)
        self.unknown += 1

    def ok(self, group, head, *d):
        self._file(group, "ok", head, d)

    def note(self, group, head, *d):
        self._file(group, "note", head, d)


def main():
    ap = argparse.ArgumentParser(
        description="Report which rules declare a gate that does not exist.")
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument(
        "--corpus",
        default=os.environ.get("RULE_GATES_CORPUS",
                               os.path.normpath(os.path.join(here, "..", "..", "rules"))),
        help="directory of rule .md files (searched recursively). "
             "Default: the rules/ dir of the repo this skill ships in.")
    ap.add_argument(
        "--config", default=os.environ.get("RULE_GATES_CONFIG"),
        help="estate config declaring roots and gate providers. "
             "Without one, the only root is the corpus's parent directory.")
    ap.add_argument("--root", action="append", default=[], metavar="LABEL=PATH",
                    help="extra resolution root; repeatable.")
    ap.add_argument("--quiet", action="store_true",
                    help="omit the gated/unavailable groups; show only the worklist.")
    args = ap.parse_args()

    rep = Report()
    corpus = os.path.abspath(args.corpus)

    # Roots. The default is the corpus's PARENT, which makes a corpus whose
    # clauses name in-repo paths resolve with no configuration at all. That
    # matters more than it looks: someone adopting this skill runs it first
    # against their own corpus, and a tool that cannot demonstrate a clean pass
    # does not get trusted when it starts failing.
    roots, provs, cfg_errs = [], [], []
    if args.config:
        if not os.path.isfile(args.config):
            rep.unk("config file does not exist", os.path.basename(args.config),
                    "No roots or providers were declared, so every",
                    "linkage below was resolved against the default",
                    "root alone.")
        else:
            roots, provs, cfg_errs = read_config(args.config)
            for e in cfg_errs:
                rep.unk("config line not understood", e)
    for spec in args.root:
        if "=" in spec:
            lbl, _, p = spec.partition("=")
            roots.append((lbl, os.path.abspath(p)))
    # The corpus's own repo is ALWAYS a root, never replaced by a configured
    # one. Clauses name in-repo paths (`skills/...`), so dropping it the moment
    # an estate declares a root of its own would make every one of those dangle
    # -- the run would go REDDER as the configuration got more complete, which is
    # the wrong direction for a checker to move.
    default_root = ("corpus-repo", os.path.dirname(corpus))
    if default_root[1] not in [r for _, r in roots]:
        roots.append(default_root)

    # Providers enumerate the gate identifiers that actually exist.
    ids, prov_counts = {}, []
    for label, kind, path, arg in provs:
        if not os.path.exists(path):
            rep.unk("gate provider '%s' is unreadable" % label,
                    "declared %s, which does not exist" % kind,
                    "Gate identifiers from this source are unread, so a",
                    "rule naming one of them cannot be confirmed as",
                    "gated. This is not evidence that it is ungated.")
            continue
        try:
            found = PROVIDERS[kind](path, arg)
        except Exception as exc:
            rep.unk("gate provider '%s' would not parse" % label,
                    "%s: %s" % (kind, str(exc)[:60]),
                    "Nothing is concluded from this source.")
            continue
        prov_counts.append((label, len(found)))
        for f in found:
            ids.setdefault(f, label)

    # Corpus.
    if not os.path.isdir(corpus):
        rep.unk("corpus directory does not exist",
                "Nothing was read. This is NOT a clean corpus --",
                "it is an unmeasured one.",
                "fix: pass --corpus <dir>")
        files = []
    else:
        files = []
        for base, dirs, names in os.walk(corpus):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for n in sorted(names):
                if n.endswith(".md") and not n.startswith("_") and n != "README.md":
                    files.append(os.path.join(base, n))
        files.sort()

    gated = unavailable = 0
    claimed = set()

    for path in files:
        slug = os.path.splitext(os.path.basename(path))[0]
        cat = os.path.basename(os.path.dirname(path))
        name = "%s/%s" % (cat, slug)
        try:
            body = open(path, "r", encoding="utf-8", errors="replace").read()
        except Exception as exc:
            rep.unk("%s is unreadable" % name, str(exc)[:60])
            continue

        fields, err = parse_clause(body)
        if fields is None:
            # The commonest UNKNOWN, and the most informative. It covers two
            # different situations that look identical in the file: a rule
            # judged irreducible (whose clause is omitted BY DESIGN -- the
            # reduction pass records that as "its absence is the finding"), and
            # a rule from a category the reduction pass never reached. Neither
            # is distinguishable from the other without reading the pass's own
            # notes, so neither is guessed at here.
            rep.unk("%-52s %s" % (name, err))
            continue

        verdict = fields.get("verdict", "").strip()
        if not verdict:
            rep.unk("%s: clause has no verdict" % name)
            continue
        if verdict not in KNOWN_VERDICTS:
            rep.unk("%s: unknown verdict '%s'" % (name, verdict[:24]),
                    "Not in the vocabulary, so nothing is concluded.")
            continue

        if verdict in UNAVAILABLE:
            unavailable += 1
            rep.ok("unavailable", "%s (%s)" % (name, verdict),
                   "Declares it cannot be gated. Nothing is owed.")
            continue

        link = fields.get(LINK_KEY, "").strip()
        if not link:
            rep.ungate("%-52s %s" % (name, verdict))
            continue

        status, evidence = resolve(link, roots, ids)
        if status == "hit":
            gated += 1
            claimed.add(evidence.split(": ", 1)[-1])
            late = "  fires_late" if fields.get("fires_late", "").lower() == "true" else ""
            rep.ok("gated", "%-52s %s%s" % (name, evidence, late))
        elif status == "dangling":
            rep.ungate("%-52s %s -> MISSING %s" % (name, verdict, evidence[:34]))
        else:
            rep.unk("%-52s %s is prose, not a locator" % (name, LINK_KEY))

    # The inverse gap: gates that exist and that no rule points at. Reported as a
    # note, never a failure -- a gate may legitimately exist for a reason outside
    # this corpus, and failing on that would punish having built one.
    for pid, owner in sorted(ids.items()):
        if pid not in claimed:
            rep.note(GROUP_ORDER[5], "%s: %s" % (owner, pid[:52]),
                     "Exists, and no rule names it. Not a failure --",
                     "possibly enforcing something written down",
                     "elsewhere, or nowhere.")

    rep.note("corpus", "%d rule file(s) read" % len(files),
             "roots: " + ", ".join(l for l, _ in roots),
             ("providers: " + ", ".join("%s=%d" % p for p in prov_counts))
             if prov_counts else "providers: none declared")

    # ----------------------------------------------------------------- report
    print("rule-gate check -- %d rule(s)" % len(files))
    skip = set()
    if args.quiet:
        skip = {"gated", "unavailable", "gates no rule claims"}
    for g in GROUP_ORDER:
        if g not in rep.buf or g in skip:
            continue
        print("\n=== %s ===" % g)
        for line in PREAMBLE.get(g, []):
            print("  " + line)
        if g in PREAMBLE:
            print("")
        for line in rep.buf[g].rstrip("\n").split("\n"):
            if line.startswith("UNGATED"):
                print(red(line))
            elif line.startswith("UNKNOWN"):
                print(amber(line))
            elif line.startswith("ok"):
                print(green(line))
            else:
                print(line)

    print("\ngated: %d   UNGATED: %d   unavailable: %d   UNKNOWN: %d"
          % (gated, rep.ungated, unavailable, rep.unknown))
    if rep.ungated:
        print(red("RULE GATES FAILED -- %d rule(s) declare a gate that does not exist"
                  % rep.ungated))
        print(red("Each names its own fix. Nothing was changed."))
        return 1
    if rep.unknown:
        print(amber("RULE GATES UNKNOWN -- 0 ungated, but %d thing(s) unread"
                    % rep.unknown))
        print(amber("An unread corpus is not a gated one. Fix the reads, re-run."))
        return 2
    print(green("RULE GATES OK -- every gateable rule names an implementation that exists"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
