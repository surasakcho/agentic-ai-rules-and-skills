---
name: check-rule-gates
description: Report which rules in this corpus declare an enforcement gate that does not actually exist — parsing each rule's `## Enforcement` clause, resolving the implementation it names against the places gates really live, and separating "no gate was built" from "the linkage could not be read". Use when adopting or auditing the rules corpus, before trusting a rule's enforcement block as coverage, after a reduction pass assigns verdicts, or when asked which rules are gated / ungated / unenforced.
license: MIT
---

# Check Rule Gates

**A verdict is a classification, not an implementation.**

Every reduced rule here ends with a machine-readable clause naming what it *could* be
reduced to:

```yaml
verdict: interposed
observable: '...'
trigger: 'PreToolUse(Bash) on git add, plus pre-commit'
check: '...'
escape: '...'
```

That is a judgement a reader made once, in a reduction pass. **Nothing has ever checked
whether the gate it describes was then built.** This does.

```bash
python -X utf8 check_rule_gates.py                          # the corpus this ships with
python -X utf8 check_rule_gates.py --corpus <dir>           # somebody else's corpus
python -X utf8 check_rule_gates.py --config <file>          # + where your gates live
python -X utf8 check_rule_gates.py --quiet                  # worklist only
```

## Why a declared-but-absent gate is worse than an honest blank

A rule carrying `verdict: interposed` with no gate deployed reads, to anyone skimming, as
coverage. The block *looks* like enforcement and is prose. A rule that says plainly it
cannot be gated is more useful, because nobody mistakes it for a control.

So the report has **four** states, not two:

| | meaning |
|---|---|
| **gated** | a gateable verdict, and the implementation it names exists |
| **UNGATED** | a gateable verdict, and no implementation found — **the work queue** |
| **unavailable** | honestly declares it cannot be gated (`irreducible`, `structural`) |
| **UNKNOWN** | no clause, an unparseable one, or a linkage that cannot be resolved |

**Exit codes are three states, not two.** `0` clean · `1` at least one UNGATED · `2` no
UNGATED but something unreadable. An unread corpus is not a clean one, and folding UNKNOWN
into "fine" is how a checker starts lying.

## The linkage design, and what it cannot see

**`implemented_by` is the link. It was not invented here** — the corpus's own clause format
already specifies it, and the reduction pass that introduced it says why: *"a rule and its
enforcement drifting apart is the failure this whole format exists to prevent."* Adding a
second key for the same job would create exactly that drift.

Resolution uses **two matchers, both exact**:

1. A **path-like token** (it contains `/`) must exist on disk under a declared root.
2. A **declared gate identifier** must appear in the value as a complete, bounded token —
   so `bulk-stage` never matches inside `bulk-stage-v2`.

There is deliberately **no inference from rule slug to gate name**. It is the obvious
shortcut and it is the one that breaks the tool. A rule called
`nothing-leaves-git-without-permission` sits near a gate called `bulk-stage`; any heuristic
confident enough to link those is confident enough to invent links that are wrong — and a
wrong link reports coverage that does not exist, which is the exact defect this checker was
built to find. An unresolvable linkage is handed to a person as UNKNOWN.

### Failure modes, stated rather than discovered

**False positives (reports "gated" when nothing is enforced) — the one that matters.**

- **Existence is not wiring.** The checker proves the named file or gate id *exists*. It does
  **not** prove it is installed, registered, reachable, or has ever fired. A gate script
  present in a repo but never invoked reports as gated. This is the single largest gap and
  no amount of static checking closes it.
- A rule may name a real implementation that enforces **something else**. The link is
  asserted by the rule's author and taken at face value.

**False negatives (reports UNGATED when a gate does exist).**

- A gate enforced somewhere the caller never declared as a root or provider is invisible.
  The `gates no rule claims` group exists partly to surface this: if a gate you know about
  is listed there, some rule should be naming it.
- A clause whose `implemented_by` is prose is reported **UNKNOWN, not UNGATED** — deliberately.
  Undetermined is not absent.
- Same for a **bare identifier matching no declared provider** — a typo'd or misremembered gate
  name (`bulk-stage-v2` against a real `bulk-stage`) reports UNKNOWN, so it surfaces at exit 2
  rather than exit 1. It is never reported as gated, which is the property that matters; but it
  is a softer signal than a missing *path*, which is definite and reports UNGATED.

**Structural is a judgement call, and it is flagged rather than buried.** `structural`
(the capability is removed, so there is no rule-layer mechanism to point at) is classified
`unavailable`. The corpus this was written against contains **zero** structural clauses, so
that branch has never run against real data. Moving it into the gateable set is one line.

## Nothing about any particular estate is written down here

Gates live somewhere different in every estate: a deny list in a settings file, a table of
handlers in a hook, a labelled block in a commit hook, a script in a tools directory. **None
of that is universal, so none of it is hardcoded.** Paths are arguments; a machine path baked
into a shared skill publishes a username and a directory layout.

Without a config, the only resolution root is the corpus's own repo — which makes a corpus
whose clauses name in-repo paths **go green with no configuration at all**. That default is
load-bearing: someone adopting this runs it against their own corpus first, and a tool that
cannot demonstrate a clean pass does not get trusted when it starts failing.

A config declares the rest. Relative paths resolve against the config file's own directory,
so it can sit beside the estate it describes:

```
# roots -- where a path in implemented_by may resolve
root estate ..

# providers -- enumerate gate identifiers that actually exist
provider hook-gates    py-tuple   ../hooks/gates.py GATES
provider deny-list     json-list  ../settings.json permissions.deny
provider commit-gates  regex      ../githooks/pre-commit ^#\s+GATE\s+[0-9]+\s+--\s+(.+)$
provider check-scripts tree       ../bin *.sh
```

| kind | reads |
|---|---|
| `json-list` | entries of a list at a dotted key in a JSON file |
| `py-tuple` | first string of each entry in a module-level tuple — via `ast`, never imported |
| `regex` | capture group 1 of every match in a text file |
| `tree` | every file under a directory matching a glob |

A provider that will not parse is **UNKNOWN**, never a silent zero — nothing is concluded
from a source that could not be read.

`py-tuple` parses with `ast` and never imports or execs. A gate registry is precisely the
file an attacker would want a checker to import.

## What one run looks like

The reasoning lives on the **group**, not on each finding. An early draft repeated a
seven-line rationale under all 45 ungated rules — 315 lines with the worklist buried in it.
Each finding is now one line, and the report is read on a phone.

```
=== UNGATED -- declares a gate, none found ===
  Each declares a gateable verdict and names no implementation,
  ...
UNGATED   coding/bau-artifacts-are-built-permanent          interposed
UNGATED   how-we-work/open-decisions-go-in-the-tracker      interposed

gated: 7   UNGATED: 45   unavailable: 0   UNKNOWN: 30
```

**A dated measurement, not a fact about the corpus.** On 2026-09-12 this corpus scored
7 gated · 45 UNGATED · 0 unavailable · 30 UNKNOWN over 82 rules. It is quoted here only to
show the shape of the gap; the tool recomputes it, and a number that describes the system
belongs in the system rather than transcribed into prose.

**`unavailable: 0` is itself a finding.** Irreducibility is recorded by *omitting* the clause,
so the six rules judged irreducible are indistinguishable, in the files, from rules a
reduction pass never reached. Both land in UNKNOWN. Making that difference visible needs a
clause that says so — `verdict: irreducible` written down — which is a change to the corpus,
not to this checker.

## Read-only, always

It opens files and parses them. It never writes, chmods, renames, or touches git. Safe from
cron, from CI, or against a live tree.

## Self-test

```bash
python -X utf8 test_self.py
```

Cases come in pairs — one that must fire, one that must not — over synthetic corpora built in
a temp directory. Nothing reads the real corpus, so the tests do not change colour when the
corpus does. **The green cases matter as much as the red ones:** a checker only ever seen
failing is as unproven as one only ever seen passing.
