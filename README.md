# Agentic AI — Rules and Skills

Portable working rules and executable skills for AI-assisted engineering, extracted from
real projects and organised by the kind of task they apply to.

**Everything here has to have earned its place.** A rule enters this repo only after a real
incident showed it was needed, and every rule names that incident. Advice without a scar is
just opinion, and there is enough of that already.

---

## Layout

```
rules/            portable rules
  how-we-work/      MANDATORY — every project, every session. How the work is conducted,
                    and how what it leaves behind behaves once nobody is watching.
  analytics/        producing figures, tables and reported numbers
  research/         reproducibility, logging, provenance
  coding/           writing and changing code
  testing/          validations, gates and checkers
  data-engineering/ ingestion, encoding, completeness
skills/           executable Claude Code skills (rules that can run) —
                  ~/.claude/skills points HERE, so discovery stays flat
  lib/              helpers skills call (skillconfig.py); inside skills/ deliberately,
                    because `..` from a junction escapes the link, not the repo
lessons/          incident write-ups the rules were extracted from
CADENCE.md        how this repo stays alive
```

**`how-we-work/` is first because it is the only category nobody may opt out of.** The other five
are *domains* — a repo that produces no figures genuinely does not need the analytics rules, and
selecting it anyway is the noise that stops a `CLAUDE.md` being read. `how-we-work/` is not a
domain. It covers conduct and operation, which every project has, so evidence-based selection can
only ever fail it: the first cron entry, the first background task, the first delegation all
arrive long after the repo was characterised.

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
| [how-we-work](rules/how-we-work/) | [Quick and dirty needs a logged experiment](rules/how-we-work/quick-and-dirty-needs-a-logged-experiment.md) | 150+ unlogged probes and a reusable tool written twice; plus a verified experiment promoted only as a chat message |
| [how-we-work](rules/how-we-work/) | [Derive from state, not invocation count](rules/how-we-work/derive-from-state-not-invocation-count.md) | An accrual job crediting a flat 8h per run because it was scheduled every 8h — short on every missed run |
| [how-we-work](rules/how-we-work/) | [Silence must be the alarm](rules/how-we-work/silence-must-be-the-alarm.md) | A nightly backup that failed three nights running, logged its own remedy each time, and was found by accident |
| [how-we-work](rules/how-we-work/) | [One writer per shared artifact](rules/how-we-work/one-writer-per-shared-artifact.md) | Four uncoordinated-writer defects in one system; one rewrote a config backup backwards, 226 lines → 174 |
| [how-we-work](rules/how-we-work/) | [Delegation and supervision](rules/how-we-work/delegation-and-supervision.md) | Agent findings taken at face value and later disproved |
| [how-we-work](rules/how-we-work/) | [An open decision lives in the tracker](rules/how-we-work/open-decisions-go-in-the-tracker.md) | Six blocking questions asked in prose; a bare "yes" resolved only the newest and silently dropped the rest |
| [how-we-work](rules/how-we-work/) | [Long reports end with a TL;DR](rules/how-we-work/long-reports-end-with-a-tldr.md) | Dense, accurate 20-60 line reports whose unranked open questions went unanswered — unranked is unread |
| [how-we-work](rules/how-we-work/) | [A PR nobody is asked to review is invisible](rules/how-we-work/a-pr-nobody-is-asked-to-review-is-invisible.md) | A bot-authored PR its owner could not find; a sweep then found an outside contributor's PR lost the same way |
| [how-we-work](rules/how-we-work/) | [Unexpected means stop and propose](rules/how-we-work/unexpected-means-stop-and-propose.md) | "I noticed X, so I did Y" -- a wrong fix shipped because a one-command check was never run |
| [how-we-work](rules/how-we-work/) | [Strict first, then the residual](rules/how-we-work/strict-first-then-the-residual.md) | A fallback built before the strict pass ever ran, so nobody learned how big the problem was |
| [how-we-work](rules/how-we-work/) | [Watch the context budget](rules/how-we-work/watch-the-context-budget.md) | Post-compaction, four messages spent defending a table that had never been re-read |
| [how-we-work](rules/how-we-work/) | [Publish lessons weekly](rules/how-we-work/publish-lessons-weekly.md) | Eleven reusable lessons that would have stayed in one repo |
| [how-we-work](rules/how-we-work/) | [Retrieve lessons weekly](rules/how-we-work/retrieve-lessons-weekly.md) | Nine rules published outward, the retrieval never once run inward |
| [how-we-work](rules/how-we-work/) | [Sanitise before sharing](rules/how-we-work/sanitise-before-sharing.md) | This repo's own seed pass published a collaborator's name and unpublished results |
| [how-we-work](rules/how-we-work/) | [Prompt for machine-specific values](rules/how-we-work/prompt-and-store-config.md) | Four skills hardcoding a username and another private repo's name |
| [how-we-work](rules/how-we-work/) | ["I can't" is a task](rules/how-we-work/cannot-is-a-task.md) | A dataset declared unobtainable while an unused tool sat in the session |
| [how-we-work](rules/how-we-work/) | [Read the manual first](rules/how-we-work/read-the-manual-first.md) | A new download route invented while the written procedure sat unread |
| [how-we-work](rules/how-we-work/) | [Shut up and work](rules/how-we-work/shut-up-and-work.md) | Padding that let a correctly-scoped claim read as an unscoped one |
| [how-we-work](rules/how-we-work/) | [Default to silence](rules/how-we-work/default-to-silence.md) | Six long process reports in a day on one four-word decision, burying the three questions only the user could answer |
| [how-we-work](rules/how-we-work/) | [Characterise the object once](rules/how-we-work/characterise-once-not-per-question.md) | Five findings surfaced by follow-up questions, none by the investigation |
| [how-we-work](rules/how-we-work/) | [Known blast radius demands a scoped fix everywhere](rules/how-we-work/known-blast-radius-demands-scoped-fix-everywhere.md) | Two-plus hours recomputing 99.93% of a dataset already known to be unchanged |
| [how-we-work](rules/how-we-work/) | [A correction is not a control unless something can fail it](rules/how-we-work/a-correction-is-not-a-control.md) | Twelve retractions, zero changes of direction — and the anti-drift instruments had all drifted |
| [how-we-work](rules/how-we-work/) | [Escalate the blocker before polishing everything around it](rules/how-we-work/escalate-the-blocker-before-polishing-the-rest.md) | Nine review rounds refining the half that was never the constraint, at 4× the cost of doing the thing |
| [how-we-work](rules/how-we-work/) | [A finding is scoped to what you checked](rules/how-we-work/a-finding-is-scoped-to-what-you-checked.md) | A verified omission in one model, written up as "absent from every model" and applied to a second that already carried it — a published double-count |
| [how-we-work](rules/how-we-work/) | ["Almost done" needs a denominator](rules/how-we-work/eta-needs-a-denominator.md) | "Not worth interrupting" said about a job that was 20% done, not checked until asked |
| [how-we-work](rules/how-we-work/) | [Nothing leaves git without permission](rules/how-we-work/nothing-leaves-git-without-permission.md) | A file gitignored as "build output" was the user's only copy of a GUI fix; an unasked verification rebuild destroyed it |
| [how-we-work](rules/how-we-work/) | [Record your thinking before complex work](rules/how-we-work/record-thinking-before-complex-work.md) | Proactive practice, no incident yet — added on user instruction |
| [how-we-work](rules/how-we-work/) | [Phrase a narrow rule as a prohibition](rules/how-we-work/phrase-narrow-rules-as-prohibitions.md) | Proactive practice, no incident yet — added on user instruction |
| [how-we-work](rules/how-we-work/) | [Propose the XML schema before strict output](rules/how-we-work/propose-xml-schema-before-strict-output.md) | Proactive practice, no incident yet — added on user instruction |
| [how-we-work](rules/how-we-work/) | [Grill for reasoning before complex tasks](rules/how-we-work/grill-for-reasoning-before-complex-tasks.md) | Proactive practice, no incident yet — added on user instruction |
| [how-we-work](rules/how-we-work/) | [Structure a new project's CLAUDE.md as System / Rules / Brief](rules/how-we-work/structure-new-project-claude-md.md) | Proactive practice, no incident yet — added on user instruction |
| [how-we-work](rules/how-we-work/) | [Run a self-validation loop after generating](rules/how-we-work/self-validation-loop-after-generating.md) | Proactive practice, no incident yet — added on user instruction |
| [analytics](rules/analytics/) | [Review every output](rules/analytics/review-every-output.md) | Six defects found in the first fourteen figures ever examined |
| [research](rules/research/) | [Reproducibility](rules/research/reproducibility.md) | Outputs that could not be regenerated after the source moved |
| [research](rules/research/) | [Research and Q&A logs](rules/research/research-and-qa-logs.md) | The same dead-end source evaluated twice |
| [research](rules/research/) | [External sources only are primary](rules/research/external-sources-only-are-primary.md) | Most internally-"VERIFIED" ledger entries had no external link a human could check |
| [testing](rules/testing/) | [Validations must be able to fail](rules/testing/validations-must-fail.md) | A guard that never fired, silently, for its whole life |
| [data-engineering](rules/data-engineering/) | [Text encoding](rules/data-engineering/text-encoding.md) | 164 mojibake labels from a locale-codec fallback |
| [data-engineering](rules/data-engineering/) | [Completeness checking](rules/data-engineering/completeness-checking.md) | A whole province silently locked in as "done" by a caching bug |
| [data-engineering](rules/data-engineering/) | [Check for a local copy before re-fetching](rules/data-engineering/check-for-a-local-copy-before-refetching.md) | ~38 GB re-downloaded while all of it sat committed in the same repo |
| [data-engineering](rules/data-engineering/) | [Verify conversions against the original](rules/data-engineering/verify-conversions-against-the-original.md) | A compression that destroyed 87.8% of a data slice, committed on an unmeasured claim |
| [data-engineering](rules/data-engineering/) | [Read the authority, never type the table](rules/data-engineering/read-the-authority-never-type-the-table.md) | A typed region list omitted 3 codes, silently dropping 3.7% of the frame, while the crosswalk sat committed nearby |
| [data-engineering](rules/data-engineering/) | [Agree the output contract first](rules/data-engineering/agree-the-output-contract-first.md) | Four unstated assumptions about an output table's shape; three became remediation commits after the work was called done |
| [coding](rules/coding/) | [Surgical, verified change](rules/coding/surgical-verified-change.md) | Fixes that introduced more defects than they closed |
| [coding](rules/coding/) | [Scratch code lives outside the repo](rules/coding/scratch-code-lives-outside-the-repo.md) | 150+ undeleted probe scripts, none of them the reusable tool the task actually needed |
| [coding](rules/coding/) | [Sanity-check test cases, hand-traced](rules/coding/sanity-check-test-cases.md) | Proactive practice, no incident yet — added on user instruction |
| [coding](rules/coding/) | [BAU artifacts are built permanent](rules/coding/bau-artifacts-are-built-permanent.md) | A live host's cron rewrite *and its rollback* both staged in a `tmpfs` scratchpad |
| [analytics](rules/analytics/) | [Report both sides of a comparison](rules/analytics/report-both-sides-of-a-comparison.md) | A "95.51% match" whose largest residual bucket was our own defect |
| [data-engineering](rules/data-engineering/) | [Status fields must be earned](rules/data-engineering/status-fields-must-be-earned.md) | 206 items recorded as fetched; 3 never were, and the manifest's own hashes proved it |
| [analytics](rules/analytics/) | [Solve the space, don't sample it](rules/analytics/solve-the-space-not-the-samples.md) | Hours of variant-testing replaced by one infeasibility certificate |
| [data-engineering](rules/data-engineering/) | [Adjudicate with an external source](rules/data-engineering/adjudicate-with-an-external-source.md) | A repo's own comment and defect log cited as two sources for one claim |
| [data-engineering](rules/data-engineering/) | [Never patch a key to force a join](rules/data-engineering/never-patch-a-key-to-force-a-join.md) | A hand-written crosswalk whose own code column was 1-of-21 valid against the issuing authority |
| [data-engineering](rules/data-engineering/) | [Never reseat a value silently](rules/data-engineering/never-reseat-a-value-silently.md) | 557,132 people flagged "no coverage" while a sibling block held their real published population |
| [data-engineering](rules/data-engineering/) | [Match exactly, on a complete key](rules/data-engineering/exact-match-on-a-complete-key.md) | 142 of 153 wrong seats per year were EXACT matches on an under-specified key |
| [analytics](rules/analytics/) | [Summaries must carry the whole set](rules/analytics/summaries-must-carry-the-whole-set.md) | A two-group defect whose larger group was dropped from every summary after the first |
| [data-engineering](rules/data-engineering/) | [A successful download is not data](rules/data-engineering/inspect-what-you-downloaded.md) | Three 1.3 KB stubs served with HTTP 200, cached as good, costing two regions a whole year |
| [analytics](rules/analytics/) | [A delta is three numbers](rules/analytics/a-delta-is-three-numbers.md) | `+951` reported identically with and without a bug that blanked twelve rows |
| [analytics](rules/analytics/) | [Name the check's blind spot](rules/analytics/name-the-blind-spot.md) | A codec guard testing the wrong byte range certified 164 corrupt rows as clean |
| [coding](rules/coding/) | [Ask before overwriting uncommitted work](rules/coding/ask-before-overwriting-uncommitted-work.md) | A build re-run "to verify" overwrote an untracked file; `git status` on it would have printed `??` |

## Lessons

The incident write-ups the rules were extracted from. Longer and more narrative than a rule:
they exist so the *mechanism* survives, not just the instruction.

| Lesson | The mechanism |
|---|---|
| [Nine silent failures](lessons/nine-silent-failures.md) | Every defect that mattered was invisible in the source and obvious in the rendered output; a remediation of 15 findings introduced 11 new defects |
| [The numbers that cannot fail](lessons/numbers-that-cannot-fail.md) | Four defects sharing one mechanism — a typed literal has nothing to disagree with, so no gate can detect it. Two of them concealed each other |

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
