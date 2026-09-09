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
  `formerly`, `unconfirmed` and friends is being *discussed*, not asserted, and is not flagged. Two
  lines was too tight: a `refuted` sat just outside it.
- **File-level banner.** A document whose first 25 lines carry an `ABANDONED` / `RETRACTED` /
  `SUPERSEDED` / `MOOT` banner is a historical record and is skipped whole. Only the first 25 lines
  count — a banner buried mid-file does not exempt the document, because a reader quoting line 200
  never saw it.
- **Malformed rows fail the run.** A registry row that is not exactly three fields has its *first*
  field compiled as the regex, which is usually not the claim. The claim it was added to guard is
  then guarded by nothing, while the tool looks merely noisy.

## Read the output, do not trust the colour

**False positives are expected and are not a bug.** First run: 5 flagged, 1 real. The other four were
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

## Related

[`a-correction-is-not-a-control`](../../rules/how-we-work/a-correction-is-not-a-control.md) — a
retraction the object absorbs and survives is an output, not a control. This is what gives one an
off-switch.
[`discriminate-by-executing-not-inspecting`](../../rules/how-we-work/discriminate-by-executing-not-inspecting.md)
— run the checker over the tree; do not read the retraction and conclude it landed.

Originally built in the e-biz factory repo (`tools/stale-claim-check.py`) and published here
unchanged.
