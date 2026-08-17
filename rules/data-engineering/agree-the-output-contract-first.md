# Agree the output table's structure before building it — never assume the shape

**Task type:** data engineering — writing or changing any pipeline that produces a table, file
or dataset somebody else will consume.
**Related:** [`completeness-checking`](completeness-checking.md) — what to assert once the
contract exists. [`parallel-variants-same-schema`](parallel-variants-same-schema.md) — keeping
two outputs' shapes identical once agreed.
[`report-both-sides-of-a-comparison`](../analytics/report-both-sides-of-a-comparison.md) — the
row-count question is where most comparison failures start.
[`read-the-authority-never-type-the-table`](read-the-authority-never-type-the-table.md) — the
mirror image: *reference data* must be read, never typed; *structure* must be asked, never
derived.

---

## The rule

**Before building a data-preparation pipeline, ask the consumer what the output should look
like: file format, what exactly one row represents, which rows are included, the row order, the
column set, the column order, and the naming. Structure is a decision, not a fact.**

It cannot be measured, inferred from the inputs, or read off a previous output. There is no
correct answer to discover — only a preferred one to be told.

## Why this is the exception to "check, don't ask"

A good general rule says: *don't ask what you can check.* Most questions that feel like
judgement calls are actually facts sitting in the repo, and asking wastes a round-trip on
something a `grep` would settle in seconds.

Output structure is the exception, and the boundary is the point:

> **Checking is for facts. Asking is for preferences. Assuming is for neither.**

No amount of measuring the inputs reveals whether the consumer wants one row per unit or one
row per unit-period, columns in source order or grouped by family, CSV or Parquet, edge cases
kept or folded away. Guessing here is not a routine judgement call — it is **inventing a
requirement and then building on it**, which is the most expensive kind of wrong because
everything downstream inherits it.

The tell that you are about to do this: you are about to write `to_csv(...)` and you have not
been told what the file should look like.

## What to ask about

Each of these has independently cost a rebuild:

- **File format**, and one file or many. Per group, or a single table?
- **Granularity** — what does exactly one row represent? **The most expensive thing to get
  wrong**, because it fixes the row count and every join downstream.
- **Which rows** — the full population, a filter, a latest-N slice? And **are edge, fragment or
  incomplete rows kept, dropped, or aggregated into a parent?**
- **Row order** — source order, sorted by key, unspecified? *"Unspecified" is a valid answer,
  but it has to be given rather than assumed.*
- **Column set and column order.** Keys first? Grouped how? Must an upstream file's own column
  order be preserved verbatim?
- **Naming** — file name, folder, and the column-naming convention (prefixes, suffixes, case).
- **Missing-value convention** — empty, `NA`, `NULL`, a sentinel? Never a fabricated `0`, which
  passes every null check and lands in the mean.
- **Precision, units, encoding and line endings** — anything downstream that reads bytes rather
  than parsed values will notice.

## Mechanise it: propose the contract, do not describe it

Do not ask the questions in prose and hope. **Print the intended output and get agreement on
it**: the header in order, the row count, what one row is, the sort key, the format. A
`--dry-run` / `--check` mode that emits exactly that and writes nothing turns a paragraph of
questions into something reviewable in seconds, and it keeps paying off on every later change.

Then put the agreed contract in the script's docstring, so the next reader sees what was
**decided** instead of inferring what was **intended**.

**And once agreed, assert it.** Row count, column order, key uniqueness, sort order. A contract
that a rebuild can silently break is not a contract.

## The incident

A consumer asked for a second dataset: *"our covariates, but the outcome variable from my own
file."* Two structural choices were put to them — whether the result should be a panel or a
cross-section, and how to handle edge rows that existed in their file but not in ours. **The
rest was assumed.** Every assumption was wrong or had to be redone:

| assumed | had to be redone as | cost |
|---|---|---|
| covariates from each unit's **latest** period | each unit's **source-matched** period | **136 units mis-dated**, one by five periods; full rebuild |
| the file written with the platform-default line ending | explicit LF, plus an attribute pinning it | committed bytes ≠ working-tree bytes, so a quoted hash described neither; two commits |
| one combined documentation package covering both datasets | **one package per dataset** | a 400-line generator refactored after the fact |
| column layout chosen by the implementer | survived — but was never agreed | an unverified guess that happened to be acceptable |

**Three of the four became their own remediation commits *after* the deliverable had been
declared ready.** None was hard to fix; all were avoidable. The two questions that *were* asked
took one round-trip and settled the two biggest decisions — which is exactly the evidence that
asking the other six would have been cheap.

**The subtler cost is the one that does not show up as a rebuild.** The column layout was never
agreed and never challenged, so it shipped as a guess. It may be fine. Nobody knows, including
the person who chose it — and "the consumer did not complain" is not the same as "the consumer
wanted this."

## Guard

- About to write an output file with a shape nobody specified? Stop and ask.
- Ask by **showing the proposed header, row count and granularity**, not by describing them.
- Record the agreed contract where the code lives.
- Assert the contract, so a rebuild that breaks it fails instead of shipping.
- "Unspecified" is an answer. Absence of an answer is not.

---

*Earned from:* a derived dataset built on four unstated structural assumptions, three of which
became remediation commits after the work was declared finished — including a period-matching
rule that mis-dated 136 units, one of them by five periods. The two structural questions that
were actually asked were each settled in a sentence.
