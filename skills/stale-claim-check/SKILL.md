---
name: stale-claim-check
description: Find places that still ASSERT a claim you have already retracted, rather than places that merely contain the old string. Use after correcting a published figure or decision, before citing a document you have amended, as a pre-commit gate on a docs tree, or when asked whether a retraction actually landed everywhere.
---

# Stale claim check — did the correction reach the sentence people quote?

## The problem this exists for

> **A correction lands where you NOTICED the error, not where the claim LIVES.**

One repo produced roughly a dozen retractions in a day. Four were recorded *correctly* — a banner at
the top of the file, the offending bullet struck through — and still left the original claim standing
somewhere else. In the worst case the survivor was an ADR's own **Decision** statement: the single
sentence anyone citing that document would quote.

Search-and-replace covers *every place containing the old string*. That is the wrong set. The set
that matters is **every place still asserting it** — and the two differ, because a retraction quotes
the old value legitimately. An occurrence is only a problem when nothing nearby marks it as
superseded.

## Use it

```sh
python3 assets/stale-claim-check.py --registry ops/superseded-claims.tsv --root .
```

Exit 1 on any unqualified survivor, so it can gate a commit. The registry is a TSV, exactly three
tab-separated fields:

```
pattern <TAB> the live value <TAB> why it was superseded
```

Nothing else is repo-specific — both paths are flags.

## How it decides

- **Marker window.** An occurrence within 3 lines of `retract`, `supersed`, `~~`, `no longer`,
  `formerly`, `unconfirmed`, `revised`, `amended` and friends is being *discussed*, not asserted, and
  is not flagged. Two lines was too tight: a `refuted` sat just outside it.
- **`REVISED` / `AMENDED` are in the vocabulary because append-only documents are this tool's main
  habitat, not an edge case.** A revision log carries its own retracted claims by construction, and
  the convention for marking one is a banner on the superseded section — `> **REVISED — see §13.7.**`.
  A tool that does not know the word turns every correctly-marked revision into an unqualified
  survivor, which forces the project to change its convention to suit the checker. That is backwards.
- **Vendored trees are skipped by default** — `node_modules`, `vendor`, `third_party`, `.venv`,
  `site-packages`, `dist`, `build`, `.next`, `target`. **A third-party changelog cannot assert
  anything about your project**; it is someone else's record of someone else's decision, so every hit
  there is noise by construction. The count of skipped files is printed, because a silent exclusion
  is indistinguishable from a clean tree. `--no-default-excludes` scans them anyway;
  `--exclude-dir NAME` adds more.
- **File-level banner.** A document whose first 25 lines carry an `ABANDONED` / `RETRACTED` /
  `SUPERSEDED` / `MOOT` banner is a historical record and is skipped whole. Only the first 25 lines
  count — a banner buried mid-file does not exempt the document, because a reader quoting line 200
  never saw it.
- **Malformed rows fail the run.** A registry row that is not exactly three fields has its *first*
  field compiled as the regex, which is usually not the claim. The claim it was added to guard is
  then guarded by nothing, while the tool looks merely noisy.

## Read the output, do not trust the colour

**False positives are expected and are not a bug.** First run: 5 flagged, 1 real. First run
*outside* the repo that grew this (2026-09-09): 8 flagged, 1 real — **six of the eight came from
`node_modules`** and the eighth was a properly-marked `REVISED` section. Both are now excluded by
construction rather than by triage, which is where an exclusion belongs once you can name the class. The other four were
legitimate — a scope document quoting the stale lines it exists to catalogue, and a table row
deliberately reciting old figures to make a scale-free argument. The marker heuristic cannot read
intent. **Triage every hit by opening it, and report the real/flagged ratio when you cite a run.** A
tool that cries wolf and is trusted blindly is worse than no tool.

**And green is the more dangerous colour.** "No unqualified survivors" means the *registry* is clean.
It says nothing whatever about claims nobody has added to it, which is why the tool prints that
caveat rather than a tick.

## Why the malformed-row check earns its place

It is the part that has actually caught something. Three rows had been written in a five-column shape
— date, who, claim, why, lesson — so field 1, the regex, was the literal string `2026-09-08`. It
matched every line in the repo mentioning that date: **69 of that run's 83 hits**, while the three
claims those rows existed to guard were watched by nothing at all.

The tool reported 83 problems and the repo had none. **A watcher watching nothing presents as noise,
not as breakage** — which is why the check fails the run rather than warning, and why the summary
says a green result "checked less than it looks" whenever any row was skipped.

## The registry's own `live` field is a claim, and nothing checks it

**The row says what is true now. Nothing verifies that.** The tool compiles field 1 as a pattern and
prints field 2 as the answer — so a `live` value that has itself been superseded is handed to
every future run as the truth, by the instrument whose entire job is catching exactly that.

**Observed 2026-09-09, and it is the sharpest instance this tool has produced.** A row guarding a
deadlock claim carried, as its live value, *"the live build 97c9933 predates the flock and has no
seedlock.py — it cannot deadlock."* That sentence had been falsified empirically the same evening —
the build does deadlock, and the mechanism was known. So the **registry of superseded claims was
itself asserting a superseded claim**, and would have kept answering the question correctly-shaped
and wrongly for as long as anyone asked.

**It was found by running the tool, not by reading the file** — the pattern still matched and no
marker cleared it. The registry is part of the tree, so it is subject to its own check; that is
worth knowing, because the instinct is to treat the registry as the reference rather than as input.

**And the field has a shelf life, not just a truth value — a line number is the shortest.** The same
row, rewritten to fix the error above, was about to go stale a second time within the hour: it cited
`main.py` lines 664/675/691, true at `97c9933` and meaningless at HEAD, because the fixing commit
moved everything (664 is now an unrelated guard, 675 the middle of a docstring). **That is a
different failure from a wrong claim — it is a true claim decaying into a false citation**, and it
needs no one to be mistaken about anything.

The fix is to pin rather than to re-derive: the row carries **the command that reproduces it**
(`git show 97c9933:./app/app/main.py`), the commit the numbers are true at, and an explicit note
that they do not hold at HEAD. *A citation that says where to stand beats one that assumes the
reader is already standing there.*

**The general shape: correct behaviour, wrong object, silent.** The tool has no way to learn that
its own expectation went stale, and it reports clean the entire time. So when a claim is corrected
twice, **update the row as well as the documents** — and write the row to record the correction,
not the half of it you were sure of at the time.

## Related

[`a-correction-lands-where-you-noticed-it`](../../rules/how-we-work/a-correction-lands-where-you-noticed-it.md)
— the rule this skill mechanises. Read it first; the tool is step 2 of its five.
[`a-correction-is-not-a-control`](../../rules/how-we-work/a-correction-is-not-a-control.md) — a
retraction the object absorbs and survives is an output, not a control. This is what gives one an
off-switch.
[`discriminate-by-executing-not-inspecting`](../../rules/how-we-work/discriminate-by-executing-not-inspecting.md)
— run the checker over the tree; do not read the retraction and conclude it landed.

Originally built in the e-biz factory repo (`tools/stale-claim-check.py`) and published here
unchanged.
