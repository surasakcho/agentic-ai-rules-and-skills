# Agentic AI — Rules and Skills

Portable working rules and executable skills for AI-assisted engineering, extracted from
real projects and organised by the kind of task they apply to.

**Everything here has to have earned its place.** A rule enters this repo only after a real
incident showed it was needed, and every rule names that incident. Advice without a scar is
just opinion, and there is enough of that already.

---

## Layout

```
skills/           every skill — ~/.claude/skills points HERE, so discovery stays flat
  lib/              helpers skills call (skillconfig.py); inside skills/ deliberately,
                    because `..` from a junction escapes the link, not the repo
rules/            portable rules, by task type
  analytics/        producing figures, tables and reported numbers
  research/         reproducibility, logging, provenance
  coding/           writing and changing code
  testing/          validations, gates and checkers
  data-engineering/ ingestion, encoding, completeness
  agent-workflow/   delegating to and supervising AI agents
skills/           executable Claude Code skills (rules that can run)
lessons/          incident write-ups the rules were extracted from
CADENCE.md        how this repo stays alive
```

## The ranking that governs everything here

> **Prose < checklist < test < gate.**
>
> A lesson that cannot fail is a document, and documents drift. Whenever a rule *can* be
> made executable, it belongs in `skills/` as code, not in `rules/` as text.

About half of what is written down can be mechanised. The other half — judging whether an
invariant matches the domain, whether a caption matches its figure — needs a human or an
agent that actually looks. Both halves are here. Neither pretends to be the other.

## Rules by task type

| Category | Rule | Earned from |
|---|---|---|
| [analytics](rules/analytics/) | [Review every output](rules/analytics/review-every-output.md) | Six defects found in the first fourteen figures ever examined |
| [research](rules/research/) | [Reproducibility](rules/research/reproducibility.md) | Outputs that could not be regenerated after the source moved |
| [research](rules/research/) | [Research and Q&A logs](rules/research/research-and-qa-logs.md) | The same dead-end source evaluated twice |
| [testing](rules/testing/) | [Validations must be able to fail](rules/testing/validations-must-fail.md) | A guard that never fired, silently, for its whole life |
| [data-engineering](rules/data-engineering/) | [Text encoding](rules/data-engineering/text-encoding.md) | 164 mojibake labels from a locale-codec fallback |
| [data-engineering](rules/data-engineering/) | [Completeness checking](rules/data-engineering/completeness-checking.md) | A whole province silently locked in as "done" by a caching bug |
| [data-engineering](rules/data-engineering/) | [Check for a local copy before re-fetching](rules/data-engineering/check-for-a-local-copy-before-refetching.md) | ~38 GB re-downloaded while all of it sat committed in the same repo |
| [data-engineering](rules/data-engineering/) | [Verify conversions against the original](rules/data-engineering/verify-conversions-against-the-original.md) | A compression that destroyed 87.8% of a data slice, committed on an unmeasured claim |
| [coding](rules/coding/) | [Surgical, verified change](rules/coding/surgical-verified-change.md) | Fixes that introduced more defects than they closed |
| [coding](rules/coding/) | [Scratch code lives outside the repo](rules/coding/scratch-code-lives-outside-the-repo.md) | 150+ undeleted probe scripts, none of them the reusable tool the task actually needed |
| [agent-workflow](rules/agent-workflow/) | [Delegation and supervision](rules/agent-workflow/delegation-and-supervision.md) | Agent findings taken at face value and later disproved |
| [agent-workflow](rules/agent-workflow/) | [Publish lessons weekly](rules/agent-workflow/publish-lessons-weekly.md) | Eleven reusable lessons that would have stayed in one repo |
| [agent-workflow](rules/agent-workflow/) | [Sanitise before sharing](rules/agent-workflow/sanitise-before-sharing.md) | This repo's own seed pass published a collaborator's name and unpublished results |
| [agent-workflow](rules/agent-workflow/) | [Prompt for machine-specific values](rules/agent-workflow/prompt-and-store-config.md) | Four skills hardcoding a username and another private repo's name |
| [analytics](rules/analytics/) | [Report both sides of a comparison](rules/analytics/report-both-sides-of-a-comparison.md) | A "95.51% match" whose largest residual bucket was our own defect |
| [data-engineering](rules/data-engineering/) | [Status fields must be earned](rules/data-engineering/status-fields-must-be-earned.md) | 206 items recorded as fetched; 3 never were, and the manifest's own hashes proved it |
| [agent-workflow](rules/agent-workflow/) | ["I can't" is a task](rules/agent-workflow/cannot-is-a-task.md) | A dataset declared unobtainable while an unused tool sat in the session |
| [agent-workflow](rules/agent-workflow/) | [Read the manual first](rules/agent-workflow/read-the-manual-first.md) | A new download route invented while the written procedure sat unread |
| [agent-workflow](rules/agent-workflow/) | [Shut up and work](rules/agent-workflow/shut-up-and-work.md) | Padding that let a correctly-scoped claim read as an unscoped one |
| [agent-workflow](rules/agent-workflow/) | [Characterise the object once](rules/agent-workflow/characterise-once-not-per-question.md) | Five findings surfaced by follow-up questions, none by the investigation |
| [agent-workflow](rules/agent-workflow/) | [Known blast radius demands a scoped fix everywhere](rules/agent-workflow/known-blast-radius-demands-scoped-fix-everywhere.md) | Two-plus hours recomputing 99.93% of a dataset already known to be unchanged |
| [agent-workflow](rules/agent-workflow/) | ["Almost done" needs a denominator](rules/agent-workflow/eta-needs-a-denominator.md) | "Not worth interrupting" said about a job that was 20% done, not checked until asked |
| [analytics](rules/analytics/) | [Solve the space, don't sample it](rules/analytics/solve-the-space-not-the-samples.md) | Hours of variant-testing replaced by one infeasibility certificate |
| [data-engineering](rules/data-engineering/) | [Adjudicate with an external source](rules/data-engineering/adjudicate-with-an-external-source.md) | A repo's own comment and defect log cited as two sources for one claim |

## Skills

| Skill | What it does |
|---|---|
| [verify-outputs](skills/verify-outputs/) | Screens rendered figures and tables for the defect classes that survive code review. Exit 1 to gate a commit. Needs [requirements.txt](skills/verify-outputs/requirements.txt). |
| [lesson-review](skills/lesson-review/) | Runs the periodic review in [CADENCE.md](CADENCE.md): finds lessons stranded in project repos, publishes the portable ones here, and scans this repo for leaked paths, emails and private names. |
| [retrieve-lessons](skills/retrieve-lessons/) | The other direction: adopts these rules into a repo that lacks them. Selects only the categories with evidence behind them, links rather than copies, and pins the commit so drift fails a check instead of going unnoticed. |

Run both self-tests, and the health check, with an interpreter that has the requirements
installed — a self-test that cannot run exits **2** and is reported as `CANNOT RUN`, never as
a pass.

```bash
python -X utf8 skills/lesson-review/harvest.py --shared . --check --deny "private-repo-name,collaborator"
```

## Using these in a project

Use the [retrieve-lessons](skills/retrieve-lessons/) skill — it detects what the repo actually
does, adopts only the categories with evidence behind them, and writes **links pinned to a
commit** into the repo's `CLAUDE.md`:

```bash
python -X utf8 skills/retrieve-lessons/retrieve.py --repo <target-repo>          # preview
python -X utf8 skills/retrieve-lessons/retrieve.py --repo <target-repo> --write  # adopt
python -X utf8 skills/retrieve-lessons/retrieve.py --repo <target-repo> --check  # gate drift
```

Reference the rules, never copy them — a copied rule drifts out of agreement with its source
and looks exactly as authoritative as the original while doing it. And adopt selectively: a
`CLAUDE.md` carrying nine rules where two apply teaches the reader that most of it is
skippable.

## Installing the skills

This repo is the single source of truth for both the rules and the skills, so nothing is
copied — **point `~/.claude/skills` at `skills/`** and the agent reads them in place:

```bash
# macOS / Linux
ln -sfn /path/to/agentic-ai-rules-and-skills/skills ~/.claude/skills

# Windows (directory junction — no admin needed)
cmd /c mklink /J "%USERPROFILE%\.claude\skills" "C:\path\to\agentic-ai-rules-and-skills\skills"

pip install -r skills/verify-outputs/requirements.txt
```

The link points one level *into* the repo, not at its root. That is what lets Claude Code's
flat discovery (`<name>/SKILL.md` directly under the skills dir) coexist with `rules/`,
`lessons/` and `lib/` — they sit outside the link and are never mistaken for skills.

### The bar for a skill here

`skills/` holds working tools, not only exemplars, so the standard is scoped to what can
actually fail: **a skill that ships executable code carries a self-test.** Prose-only skills
have nothing to test and are exempt. Code-bearing skills that lack one are declared in
[`skills/_no-selftest.txt`](skills/_no-selftest.txt), which `harvest.py --check` treats as a
ratchet — a new one cannot land without either a test or an explicit line, and a line that is
no longer needed fails the check so the list can only shrink.

## Contributing a rule

1. Name the incident. What broke, how much did it cost, and how was it caught?
2. Say whether it can be mechanised. If yes, it belongs in `skills/`.
3. Put it under the task type someone would be doing when they need it — not the one it
   was discovered in.
