# Gateability — what each rule can be reduced to, and what it cannot

**A rule is not inherently gateable or ungateable. It becomes gateable when you find the
observable artifact it implies.** You cannot gate a judgement. You can very often gate the
*trace* that the judgement happened, or the *specific failure shape* the rule was written
about — and because every rule here names a real incident, the incident tells you what
observable would have caught it.

This document is the reduction pass over `rules/how-we-work/` (45 rules) and `rules/coding/`
(11 rules). Every rule gets a verdict. **Six do not reduce, and that is recorded as a finding
rather than papered over** — a gate that is easy to satisfy without doing the thing is worse
than the prose it replaced, because it converts a practice into a ritual and then reports
green.

---

## The four layers, and the one that is empty

| Layer | What it means | Count |
|---|---|---|
| **structural** | the capability does not exist — nothing to enforce | **0** |
| **interposed** | `permissions.deny`, or a `PreToolUse` / `Stop` hook that inspects tool input and refuses | **11** |
| **deferred** | pre-commit hook, `--check` exit code, CI, scheduled audit | **18** |
| **narrowed** | a real gate that covers the incident but **not** the rule's full intent — prose stays alongside | **21** |
| **irreducible** | no artifact; judgement, tone, or disposition | **6** |

**50 of 56 reduce to something mechanical; 29 of those at full strength.** The prior
assessment put it at roughly 15 of 45.

**The structural row is empty, and that is informative rather than a gap.** A structural gate
removes a capability — no credential mounted, no socket exposed. `how-we-work` rules govern
*conduct*, and conduct cannot be removed from an agent that is still able to work. Structural
gates belong to the infrastructure layer, not the rules layer; expecting them here is a
category error.

## The verdict is not the whole answer — the firing moment is

[`a-gate-that-fires-at-commit-time-is-not-a-gate`](../rules/coding/a-gate-that-fires-at-commit-time-is-not-a-gate.md)
is the rule this document is most accountable to. A control that catches "do not start X
without Y" at commit time does not prevent the work — it prevents the work from *landing*,
after it has been paid for. That rule's own incident measured ~130k tokens spent on a feature
that could never merge.

So **`trigger` is a mandatory field**, and any clause whose trigger is later than the moment
its rule names carries `fires_late: true`. That flag is the honest admission, and it is
machine-readable so the gap can be counted rather than forgotten.

**This cuts both ways.** For a rule about a claim *landing* — a retraction, a published figure
— commit time IS the moment the rule names, and a pre-commit gate is a full-strength gate, not
a late one. `fires_late` marks a mismatch, not a layer.

---

## The clause format, and why a trailing section rather than frontmatter

Every reduced rule gains a `## Enforcement` section at the end of its file, carrying a fenced
YAML block:

```yaml
verdict: interposed
observable: what a machine looks at
trigger: PreToolUse(Bash)
check: the predicate
escape: how a legitimate case gets through
narrows: what the gate does NOT cover   # only when verdict is narrowed
fires_late: true                        # only when the trigger is later than the rule's moment
implemented_by: skills/<name>/          # only when it already runs
```

**Why not YAML frontmatter:**

- **Nothing in the corpus uses it.** All 80 rule files open with `# Title` then bold-label
  lines (`**Task type:**`, `**Related:**`, `**Mechanised by:**`). Frontmatter would push the
  H1 down and risk the extractors that read these files — `rules_in_force.py` keys on a
  `## The rule` heading, `harvest.py --check` greps each rule for a named incident.
- **Frontmatter is invisible in the rendered file.** The firing moment is something a *human*
  reading the rule needs to see, because `a-gate-that-fires-at-commit-time-is-not-a-gate`
  demands the moment be stated. A control nobody can read is back to being remembered.
- **The pattern already exists.**
  [`prompt-and-store-config`](../rules/how-we-work/prompt-and-store-config.md) carries a
  "What is gated and what is not" section written by hand. This format generalises what that
  rule already did rather than inventing a convention.
- A fenced block is exactly parseable while still rendering as visible text.

**A rule judged irreducible gets no clause. Its absence is the finding** — an empty
`## Enforcement` section asserting "nothing here" would be indistinguishable from one nobody
has written yet.

---

## how-we-work

| Rule | Verdict | Observable | Trigger | Check sketch | False positives / escape | Cost |
|---|---|---|---|---|---|---|
| a-bot-check-is-a-full-stop | interposed | stealth/spoof signatures in tool input: `puppeteer-extra-plugin-stealth`, `playwright-stealth`, `undetected-chromedriver`, `navigator.webdriver` patches, a browser UA passed to a scripted client, a session cookie imported into automation | PreToolUse(Bash/Write/Edit) + `permissions.deny` on the installs | `argv or file body matches STEALTH_SIGNATURES -> deny` | An API that *requires* a UA header. Escape: allowlist non-browser UA strings; operator confirm for the rest | trivial |
| a-correction-is-not-a-control | narrowed | retraction-registry rows added in a window, against objects actually ended (a doc deleted or marked superseded) | scheduled audit + Stop advisory | `rows_added(window) >= N and objects_ended(window) == 0 -> report the ratio` | Never refuses. A genuinely correct object attracts corrections. | state |
| a-correction-lands-where-you-noticed-it | deferred | files still ASSERTING a retracted claim — the old pattern present with no supersession marker within the marker window | pre-commit | `for row in registry: hits = grep(row.pattern) - marked_superseded; hits -> block` | A file quoting the old value as a worked example. Escape: marker vocabulary (superseded/revised/rescinded/no longer), or a file-level exempt marker | implemented |
| a-finding-is-scoped-to-what-you-checked | narrowed | a universal quantifier (every/all/none/always) in a written finding with no count in the same sentence | pre-commit on findings + Stop advisory | `claim =~ /\b(every|all|none)\b/ and not adjacent_count -> flag` | A claim about a set enumerated elsewhere. Escape: put the count in the sentence — which is the rule's own prescription | parser |
| a-pr-nobody-is-asked-to-review-is-invisible | interposed | `gh pr create` argv without `--reviewer` and `--assignee`; plus open PRs with empty `reviewRequests` and `assignees` | PreToolUse(Bash) + scheduled sweep | `gh pr create without both flags -> deny`; sweep `gh search prs --state open` and read both fields back | Solo repo. Escape: `--assignee @me`. Exit 0 is not evidence — read the state back | trivial |
| a-task-in-one-place-vanishes | deferred | task-shaped lines (`- [ ]`, decision rows, "TODO") in a document being restructured or deleted, absent from the declared tracker | pre-commit | `deleted_task_lines - tracker_entries -> block` | A task legitimately completed. Escape: present as done in the tracker, or an explicit dropped note | parser + declared tracker path |
| board-for-state-sprint-for-commitment | deferred | the WIP limit declared on the board, and the card count in the in-progress column; at sprint close, every unfinished card labelled carried/split/dropped | pre-commit on the board file | `in_progress_count > wip_limit -> block`; `sprint_closed and unlabelled_cards -> block` | Mid-move overshoot. Escape: an explicit override with a reason | parser + board format |
| cannot-is-a-task | **irreducible** | — | — | — | see Irreducibles | — |
| characterise-once-not-per-question | narrowed | a reconciliation/comparison report lacking an explicit `unexplained` count, or reporting only one direction | pre-commit / CI on the report artifact | `report lacks unexplained:N or lacks both directions -> block` | Escape: none needed; the fields are cheap. **Cannot compel the investigation** — only refuse a report that hides its residual | report-format convention |
| close-your-own-gaps | narrowed | (a) a silent skip inside a verification loop — `if x not in y: continue`; (b) a step reading an artifact another step produces without asserting they agree on population | pre-commit lint + Stop advisory on hedge phrases | `AST: continue-on-missing inside a verify loop -> block`; `summary =~ /could verify|shall I look/ -> advise` | A deliberate optional field. Escape: assert the expected count instead. **The rule says itself this is mostly not mechanisable** | parser |
| default-to-silence | **irreducible** | — | — | — | see Irreducibles | — |
| delegation-and-supervision | narrowed | a diff that weakens an existing test — assertion deleted, tolerance raised, `assertEqual` loosened to approx | PreToolUse(Edit) on test paths + pre-commit | `diff on tests weakens an assertion -> deny` | A genuinely wrong assertion. Escape: change it in a commit that says so, not inside a delegated task | parser |
| derive-from-state-not-invocation-count | deferred | a numeric literal in an accumulation call equal to a schedule period declared elsewhere in the repo; a constant beside a comment asserting a capacity | pre-commit lint | `literal in accrue/credit call == cron_period(repo) -> block` | A real constant. Escape: annotate as derived, or read it from state | parser + schedule inventory |
| discard-secret-output-never-filter-it | interposed | a secret-resolving command piped into anything but `/dev/null` — `compose config`, `docker inspect`, `env`, `printenv`, `terraform show`, `kubectl get secret -o yaml`, `git config --list` | PreToolUse(Bash) | `cmd in SECRET_RENDERERS and has_pipe_or_no_redirect -> deny` | Value-free subcommands (`config --services`, `inspect -f` on a non-env field). Escape: allowlist those; otherwise redirect and test the exit code | trivial |
| discriminate-by-executing-not-inspecting | narrowed | for a named flag or metric: `lift = P(flag \| fact) − P(flag \| not fact)`, and whether every non-positive row is named with a reason | scheduled audit (CI over telemetry) | `lift <= 0 and row unexplained -> fail` | A deliberately retired mechanic reads dead and is correct. Escape: name the reason — the gate is "every failing row is explained", never "the table is green" | state |
| escalate-the-blocker-before-polishing-the-rest | deferred | the status surface asserting nothing is owed while the tracker holds open owner-blocked items | pre-commit on the status file + session-start advisory | `status asserts "nothing owed" and open_owner_blocked > 0 -> block` | None. Escape: update the line — which is the fix | declared tracker |
| eta-needs-a-denominator | narrowed | a proximity claim (almost done / not worth interrupting / nearly there) with no done/total pair in the same message | Stop | `msg =~ PROXIMITY and not =~ /\d+\s*(of|\/)\s*\d+/ -> refuse` | Qualitative progress talk. Escape: state the fraction, or say the total is unknown — which the rule also accepts | trivial |
| find-the-route-or-name-what-you-need | narrowed | the rule's own named tells — an imperative aimed at the user, a duration estimate for *their* work, the same refusal restated across turns | Stop | `msg has imperative_to_user and duration_estimate -> refuse`; `refusal repeated in >1 turn -> refuse` | A genuine one-step requisition. Escape: phrase as resource + who supplies it | trivial |
| grill-for-reasoning-before-complex-tasks | **irreducible** | — | — | — | see Irreducibles | — |
| known-blast-radius-demands-scoped-fix-everywhere | narrowed | capability asymmetry among sibling rebuild scripts — one supports a scoped `--only` mode, its siblings do not | pre-commit / CI | `siblings(frame) and any(has_only_flag) and not all -> block` | Scripts that are siblings by name only. Escape: declare the family. **Does not decide when to scope** — it removes the excuse that the script cannot | parser + declared family |
| long-reports-end-with-a-tldr | interposed | prose line count of the outgoing message; presence and bullet count of the TL;DR; whether each open ask appears in it | Stop | `prose_lines > 20 and (no TLDR or bullets >= 8 or open_ask not in TLDR) -> refuse` | Tables and code blocks inflating length. Escape: count prose lines only. **The rule states its own thresholds** — the gate is faithful, not invented | trivial |
| monitor-the-number-not-just-the-job | deferred | every scheduled unit discovered from the filesystem/config, mapped to a registered reconciler; and OK/DIVERGED/UNKNOWN with UNKNOWN carrying the worst exit code | CI + scheduled | `units = discover(); unmapped -> UNKNOWN -> nonzero`; `reconciler unscheduled -> fail` | Jobs producing an artifact but no value. Escape: declare `value: none`. Never hand-list the units — discovery is the point | state |
| nothing-leaves-git-without-permission | interposed | tool input matching an exclusion verb — a `.gitignore` write, `git rm --cached`, `--assume-unchanged`, `--skip-worktree` | PreToolUse(Bash/Write/Edit) | `cmd or edit matches EXCLUSION_VERBS -> deny, ask the operator` | A new repo needing an ignore file — still asks, per the rule (propose, do not apply). Escape: the operator's own confirmation | trivial |
| one-writer-per-shared-artifact | deferred | a script writing a declared shared artifact with no owner guard; a fixed `.tmp` name in a read-modify-write | pre-commit lint | `writes(shared_artifact) and not has_host_guard -> block`; `fixed .tmp in RMW -> block` | Single-host scripts. Escape: declare the owner in the artifact's vicinity, which the rule already requires | parser + artifact registry |
| open-decisions-go-in-the-tracker | interposed | a question put to the human in the outgoing message with no tracker entry written in the same turn | Stop | `msg has question_to_user and not tracker_written(turn) -> refuse` | Rhetorical questions. Escape: write the entry — ten seconds, per the rule | declared tracker |
| phrase-narrow-rules-as-prohibitions | **irreducible** | — | — | — | see Irreducibles | — |
| prompt-and-store-config | deferred | absolute paths, usernames and emails in a shared artifact; a git-tracked or un-ignored `.env`; a real value in `.env.example` | `--check` exit code | `harvest.py --check` and `skillconfig.py check` | Placeholder segments are deliberately not hits. **Whether a skill *asks* rather than defaults is not gated** — the rule says so itself | implemented |
| propose-xml-schema-before-strict-output | narrowed | a strict-format output file whose schema/skeleton sibling does not exist earlier in the log | pre-commit | `strict_output added and schema absent or newer -> block` | Escape: commit the skeleton first. **Does not capture that the user confirmed it** — only that a shape was fixed before the fill | trivial |
| publish-lessons-weekly | deferred | the newest date in `lessons/_review-log.md` against now | `--check` exit code | `age(max(dates)) > 7 -> problem` | An empty pass is valid and still logged. Escape: log it | implemented |
| quick-and-dirty-needs-a-logged-experiment | narrowed | a probe path being staged; any tracked file under a declared scratch directory; a probe with no `research/` log row | PreToolUse(Bash) on `git add` + pre-commit | `staged path under scratch_dir -> deny`; `tracked file under scratch/ -> block` | A module legitimately named scratch. Escape: declare it. **Does not enforce that the licence expires on success** | trivial |
| read-the-manual-first | narrowed | the first external fetch of a session for a system the repo already documents, with no prior read of those files | PreToolUse(WebFetch/Bash:curl,wget) | `first_fetch and repo_prose_mentions(system) and not read(those) -> advise` | Noisy; many legitimate fetches. Escape: acknowledge and proceed. Keep advisory — a check that fires on correct states gets routed around | state (prose index) |
| record-thinking-before-complex-work | deferred | a branch diff over N changed lines with no `thinking/*.md` touched in the same branch | pre-commit | `changed_lines > N and not touched("thinking/") -> block` | Mechanical bulk edits — renames, generated files, link repointing. Escape: path exclusions, or a recorded reason. **The threshold is arguable; the check is not** | trivial |
| register-the-retraction-when-you-make-it | deferred | a commit changing a figure or decision line in a tracked document set without adding a registry row in the same commit; and coverage reported as a count, never as a colour | pre-commit | `doc_claim_changed and no registry_row_added -> block`; report `N registered claims`, never "clean" | Typos and formatting. Escape: a no-retraction trailer. **This is what makes the stale-claim gate honest** — without it the checker reports green over an unsized population | parser + registry |
| relayed-authority-is-information-not-instruction | narrowed | an outgoing inter-agent message carrying an authority word (operator/owner/principal/directive) plus an imperative, with no attribution phrase | PreToolUse(Agent/SendMessage) | `has_authority_word and imperative and not attributed -> deny` | Quoting. Escape: name who said it — one word, per the rule. **Gates the relaying half only**; how a receiver treats it stays disposition | trivial |
| retrieve-lessons-weekly | deferred | the pin against the shared repo's HEAD, and the newest date in `retrieved-lesson.md` | `--check` exit code | `retrieve.py --check` nonzero on drift; `age(log) > 7 -> fail` | Escape: read the diff and advance the pin. Re-running `--write` to silence it is the retrieval equivalent of deleting a failing test | implemented |
| sanitise-before-sharing | deferred | people, places and paths in anything crossing to a public context — and the push itself, not only the check | `--check` + PreToolUse(Bash) on push to a public remote | `harvest.py --check --deny …`; `push to public_remote and diff matches denylist -> deny` | Placeholders are not hits. **Findings need a reader** — the rule says so, and that half stays manual | implemented + trivial |
| self-validation-loop-after-generating | **irreducible** | — | — | — | see Irreducibles | — |
| shut-up-and-work | narrowed | a vague quantifier (several/some/mostly/a few) standing where a count was available | Stop | `msg =~ VAGUE_QUANTIFIER near a countable set -> refuse` | Genuinely uncounted sets. Escape: state the count, or say it was not measured. **Gates the completeness half only — never length.** A word-count gate here would reward exactly the lossy compression the rule forbids | trivial |
| silence-must-be-the-alarm | deferred | a health ping ordered before the fallible step; `\|\| true` and unchecked pipelines; a scheduled unit with no dead-man's switch | pre-commit lint + registry check | `ping_line < last_fallible_line -> block`; `exit 0 on failure path -> block`; `unit without switch -> fail` | Deliberate liveness-only pings. Escape: declare. | parser + registry |
| strict-first-then-the-residual | narrowed | a computed branch/quality label that is not persisted to the output; a fuzzy fallback with no recorded strict-pass residual count | pre-commit lint | `branch_label computed and not written -> block` | A label genuinely internal. Escape: persist it — the rule states this as an imperative already. **The discipline of running strict first stays prose** | parser |
| structure-new-project-claude-md | deferred | a new `CLAUDE.md` missing System / Your rules / Project brief, in that order | pre-commit on added files | `new CLAUDE.md and headings != expected -> block` | Existing files. Escape: applies to newly added ones only | trivial |
| unexpected-means-stop-and-propose | narrowed | the rule's own named construction — "I noticed X, so I did Y" — in an outgoing message, and a fix committed in the same turn as a discovered anomaly with no ask | Stop | `msg =~ /noticed .{0,80}(so|therefore) I/ -> refuse` | The rule's own boundary table: closing a gap in your own rigour is correct and looks identical. Escape: a one-line justification naming which side of the boundary it is | trivial |
| watch-the-context-budget | interposed | context usage as a percentage of the window | per-turn hook / PreCompact | `usage > 0.40 and not prompted_this_session -> prompt with the number` | None. Escape: the user declines — the rule forbids compacting unilaterally anyway | trivial if the harness exposes usage |
| write-in-fragments-not-sentences | **irreducible** | — | — | — | see Irreducibles | — |
| write-it-down-when-you-read-it | narrowed | a turn that received substantive input and produced no durable write; a capture file that is untracked rather than committed | Stop | `user_turn carried items and no tracked_write(turn) -> refuse`; `capture_file untracked -> block` | Pure questions. Escape: classify, or write the file. **"Durable means in the repo" gates cleanly; "worth keeping" is judgement** | trivial |

## coding

| Rule | Verdict | Observable | Trigger | Check sketch | False positives / escape | Cost |
|---|---|---|---|---|---|---|
| a-fix-that-cannot-reach-the-artifact-is-not-a-fix | narrowed | a test environment disabling a constraint production enables (foreign keys off, pragmas relaxed); a migration or backfill with no test seeded from the defective population | pre-commit / CI | `test disables constraint enabled in prod -> block`; `migration without a polluted-state fixture -> block` | Fixtures that legitimately need constraints off. Escape: declare per file. **Cannot verify the fix reaches the running row** — only that the check and the artifact are not different objects | parser |
| a-gate-that-fires-at-commit-time-is-not-a-gate | deferred | every rule's declared `trigger` against the moment its own statement names | CI over this repo | `rule says "before X starts" and trigger is commit-time and not fires_late -> fail` | Rules where commit time IS the named moment. Escape: `fires_late: true`, which is the admission the rule demands | trivial |
| a-repo-split-kills-relative-links-silently | deferred | relative links resolving outside the repo root; an ignore file absent on first run; the test suite not run standalone in the new repo | `--check` exit code | already in `harvest.py`: `root not in dest.parents -> problem` | None material. Escape: rewrite to absolute URLs in the same commit as the split | implemented |
| ask-before-overwriting-uncommitted-work | narrowed | `git status --porcelain <target>` for a direct write; for a command, the dirty/untracked set under its output directory before it runs | PreToolUse(Write/Edit/Bash) | `status(target) in {"??", " M"} -> deny`; for generator/build verbs, snapshot dirty+untracked files aside first | **The incident was a Bash build command whose write target is not in the tool input** — that case does not gate, so the reduction is a snapshot that makes the damage recoverable rather than a refusal | trivial (direct) / parser (side effect) |
| bau-artifacts-are-built-permanent | interposed | the filesystem type behind any path handed over or referenced by a recurring command — the rule gives the command: `findmnt -no FSTYPE,OPTIONS <path>` | Stop + PreToolUse(Bash) on schedule installs | `outgoing msg references scratchpad path -> refuse`; `cron/systemd unit references tmpfs path -> deny` | Legitimately naming a temp artifact. Escape: say it is temporary and not for reuse | trivial |
| mock-the-screen-before-you-build-it | deferred | a commit touching UI files with no mockup artifact committed earlier in the branch; whether three states were rendered | pre-commit | `ui_files_changed and no mockup in branch history -> block` | Small UI fixes. Escape: a threshold and a declared exemption. **`fires_late: true`** — the rule's moment is before the build | trivial |
| sanity-check-test-cases | narrowed | surviving mutants on the changed logic — the mechanical form of "the tests encode the same blind spot as the code" | CI | `mutation_score(changed) < threshold -> fail` | Slow; equivalent mutants. Escape: a baseline ratchet. **Hand-tracing a sample has no artifact and stays prose** | needs a tool + CI time |
| scratch-code-lives-outside-the-repo | interposed | a staged path under a scratch directory; any tracked file inside one | PreToolUse(Bash) on `git add` + pre-commit | `staged path under scratch_dir -> deny`; `tracked file under scratch/ -> block` | A module legitimately named scratch. Escape: declare it | trivial |
| shell-expansion-silently-deletes-published-content | interposed | an unquoted heredoc, or a double-quoted `--body`/`-m` whose text contains `` ` ``, `$(`, or `\` | PreToolUse(Bash) | `publish_cmd and body is double-quoted and body =~ /[\`$]/ -> deny, require --body-file or <<'EOF'` | Short bodies with no metacharacters. Escape: allow when the body contains none. Verify the published artifact with a canary — absence of visible damage proves nothing | trivial |
| surgical-verified-change | narrowed | formatting-only hunks in files whose functional lines are unchanged; a delete or overwrite driven by a computed set with no full-vs-partial declaration | pre-commit | `hunk is whitespace-only and file otherwise unchanged -> flag`; `delete_by_computed_set and no completeness flag -> block` | Deliberate reformatting. Escape: do it in its own commit. **"A convention needs a stated domain" does not reduce** | parser |
| write-the-prd-before-the-code | interposed | an edit to an implementation path while no PRD or named reproduced defect is referenced | PreToolUse(Write/Edit) with pre-commit backstop | `edit(impl_path) and no PRD referenced -> deny before the first line is written` | A one-line fix; a reproduced defect. Escape: name the defect, or write the paragraph — the rule says length is not the deliverable | trivial |

---

## Priority — the eight to build first

Ordered by **the damage actually recorded in the rule files**, not by how easy each is. The
ranking principle: *irreversible* beats *expensive*, and *undetectable* beats *loud*.

**1. `shell-expansion-silently-deletes-published-content`** — interposed, trivial.
A financial threshold was **deleted** from a message to a decision-maker, inside a comment
whose purpose was correcting an earlier understatement. The command exited 0. The deletion is
invisible in the source and exists only in what other people read, so no amount of care
afterwards finds it. Highest damage-to-cost ratio in the corpus: one regex over publish
commands.

**2. `nothing-leaves-git-without-permission` + `ask-before-overwriting-uncommitted-work`** —
interposed pair.
The only agent action with **no undo inside git at all**. The recorded incident destroyed the
user's only copy of a problem they had spent days solving, recovered only because the folder
happened to sit in a service with version history. Build them together: the first removes the
exclusion decision from the agent, the second catches the write. Note the honest gap — the
incident's actual mechanism was a *build command*, so the snapshot-aside mitigation is the
part that would have saved it, not the refusal.

**3. `discard-secret-output-never-filter-it`** — interposed, trivial.
A one-way door. By the time a filter drops a line the producing command has already written
every byte into a transcript on disk. The incident put an API key into a 23 MB session log,
and a peer session using the same key stayed clean purely by accident of style. Rotation is
the only remedy after the fact, which is why this belongs before the call rather than after.

**4. `write-the-prd-before-the-code`, moved to `PreToolUse`** — interposed.
This is the highest-leverage *relocation* in the document. The rule was tested with blind
agents and worked — it refused the right commit — and still let a full feature be built first,
at ~130k tokens in a repo charging compute against a cash ceiling. The corpus already contains
the rule explaining why (`a-gate-that-fires-at-commit-time-is-not-a-gate`). Fixing the firing
moment costs nothing and recovers the whole point of the rule.

**5. `register-the-retraction-when-you-make-it` — before, or with, `a-correction-lands-where-you-noticed-it`** — deferred pair.
`stale-claim-check` already exists, and **that is exactly the risk.** A week produced at least
sixteen retractions; a sweep from memory registered six; the run came back green over roughly
a third of the population. One stale sentence was wired into a release gate, telling it to log
an exception. Shipping the checker without gating registration ships a green light over an
unsized sample — the precise failure mode this whole document is meant to avoid.

**6. `monitor-the-number-not-just-the-job` + `silence-must-be-the-alarm`** — deferred pair,
needs a job registry.
The most expensive class here: **green while wrong**. 59 consecutive days of flawless runs
booking one eighth of the income, which made the most profitable strategy look like the least
and nearly got it deprioritised on its own broken accounting. Alongside it, three nights of
configuration silently unbacked-up while the job logged its own remedy in plain English. One
registry of scheduled units serves both checks, which is why they are built together.

**7. `derive-from-state-not-invocation-count`** — deferred, needs a parser.
Falsified **twice in this estate**: an accrual job crediting a flat period per invocation, in
the number a real-capital decision rested on; and a hardcoded ceiling that rationed a 23 GiB
machine as a 7 GiB one for thirteen days. The lint is a literal compared against the schedule
the repo itself declares. Both incidents are the same signature and it is greppable.

**8. `a-pr-nobody-is-asked-to-review-is-invisible`** — interposed, trivial.
A reviewed, mergeable contribution stalled indefinitely because two flags were missing, and
the sweep it prompted found a **third party's** PR lost the same way in another repo. One flag
in one command, and the sweep finds the ones already lost.

**Deliberately not in the top eight:** `record-thinking-before-complex-work` and
`long-reports-end-with-a-tldr` are both trivial and both worth building — but their recorded
cost is wasted effort and unread reports, not destroyed or corrupted artifacts.

---

## The irreducibles — six, with reasons

**These get no `## Enforcement` clause.** The absence is deliberate and is itself the record.

| Rule | Why it does not reduce | Weaker instrument still available |
|---|---|---|
| **cannot-is-a-task** | The deliverable is "a route or a requisition", and the difference between a route genuinely searched for and one asserted is *effort*, which leaves no artifact. Detecting the phrase "not possible" would gate the wording and reward silence instead. | A `Stop` advisory: when the outgoing message asserts a blocker, print the rule's own checklist — tools you already hold, alternatives named individually, the indirect route, narrowing the ask. Informs; never refuses. Its sibling `find-the-route` *does* gate the tells, and covers part of the same ground. |
| **default-to-silence** | This is a routing decision about whether a message should exist. Every mechanical proxy is a length or count gate, and the rule's own stated failure mode is that **compression drops set sizes** — so a length gate would push directly against the rule while reporting compliance. Requiring the agent to name one of the four reasons is a one-word ritual, satisfiable without the judgement. | A periodic human audit: messages sent against decisions actually requested. The incident was six long reports on one four-word decision — a ratio a person can see at a glance and no checker can. |
| **grill-for-reasoning-before-complex-tasks** | "Complex" is the judgement, and the deliverable is the *quality* of the questions. Counting questions asked would be satisfied by three bad ones. Proactive practice with no incident, so there is not even a failure shape to gate. | The `grilling` skill, invoked deliberately. A checklist item at task start. |
| **phrase-narrow-rules-as-prohibitions** | Gating this needs a machine judgement of whether a rule is *narrow*, which is the whole content of the rule. A lint on "always/every" in rule statements would misfire on the many correctly prescriptive broad rules — the rule explicitly protects those. | The contributing checklist in `README.md`; a review prompt when a rule is added. |
| **self-validation-loop-after-generating** | The four checks are real, and whether they were run leaves no trace. A declaration that the loop ran is exactly the "easy to satisfy without doing the thing" failure. | A `Stop` advisory that prints the four checks. Its named consequences are gated elsewhere — format strictness under `propose-xml-schema`, contradictions under `a-correction-lands`. |
| **write-in-fragments-not-sentences** | Texture of output. A sentence-count or word-count gate is actively harmful here for the same reason as `default-to-silence`: the rule's own boundary section says cutting facts is the wrong cut, and a length gate rewards precisely that. | The completeness half is gated under `shut-up-and-work` (vague quantifier where a count was available) — which is the *inverse* of the naive gate, and the safe one. |

**The pattern worth noticing:** four of the six are about the *texture or effort* of output,
and in three of those the obvious mechanical proxy would push against the rule rather than
toward it. That is not a coincidence — it is what separates a rule that can be gated from one
that can only be read.

---

## Narrowing register — 21 rules whose gate is smaller than the rule

Each of these carries `narrows:` in its clause, stating what the gate does **not** cover. The
prose stays alongside and stays binding. The ones where the gap is widest, and worth reading
before trusting the green light:

- **`ask-before-overwriting-uncommitted-work`** — gates the direct write; the incident was a
  *command whose write was a side effect*. The mitigation is a snapshot, not a refusal.
- **`characterise-once-not-per-question`** — gates the shape of the report; cannot compel the
  investigation that should have produced it.
- **`discriminate-by-executing-not-inspecting`** — gates lift for named flags in telemetry;
  the general discipline ("would this have shown anything if the claim were false?") is prose.
- **`known-blast-radius-demands-scoped-fix-everywhere`** — gates capability parity between
  sibling scripts; does not decide when scoping is owed.
- **`shut-up-and-work`** — gates only the completeness half. **Never gate length here.**
- **`propose-xml-schema-before-strict-output`** — gates that a shape was fixed first; not that
  anyone confirmed it.
- **`write-it-down-when-you-read-it`** — gates that a durable, *tracked* write happened; not
  whether what was written was worth keeping.

---

## Found while reading — stale, contradictory, or already falsified

1. **The README's rule table is 15 rules out of date.** 80 rule files exist; the table carries
   72 rows, and 15 files are not linked from it at all — including five of the eleven `coding`
   rules (`write-the-prd-before-the-code`, `a-gate-that-fires-at-commit-time-is-not-a-gate`,
   `a-repo-split-kills-relative-links-silently`, `mock-the-screen-before-you-build-it`,
   `a-fix-that-cannot-reach-the-artifact-is-not-a-fix`) and nine of `how-we-work`.
   `CADENCE.md`'s own "done" checklist requires *"README.md's rule table matches what is
   actually in rules/"*, so the cadence is passing a check it is failing. **This is gateable
   and is not gated:** `for f in rules/*/*.md: f linked from README -> else fail` is three
   lines in `harvest.py --check`, and it would have refused the last several passes.

2. **"About half of what is written down can be mechanised" is now an understatement.** It
   appears in `README.md` and in `publish-lessons-weekly`. This pass finds 50 of 56 reducible,
   29 at full strength. The figure was true when written and nothing tied it to the corpus —
   which is exactly the pattern `derive-from-state-not-invocation-count` names: *a number that
   describes the system belongs in the system, derived rather than transcribed.* It should be
   computed from the `verdict:` fields, not restated.

3. **A resolved tension, worth stating so it is not read as a contradiction.**
   `a-gate-that-fires-at-commit-time-is-not-a-gate` says a commit-time control is not a gate;
   `a-correction-lands-where-you-noticed-it` instructs you to *"let it gate the commit"*. Both
   are right. The test is not the layer but the match: for a rule about work *starting*,
   commit time is late; for a rule about a claim *landing*, commit time is the named moment.
   Hence `fires_late` marks a mismatch rather than a layer.

4. **A rule that already does what this document proposes.**
   `prompt-and-store-config` carries an explicit "What is gated and what is not" section, and
   is the only rule that does. It is the precedent the clause format generalises — worth
   keeping as the worked example for anyone writing a new rule.

5. **Two rules are already fully mechanised and say so; three more are mechanised without
   saying so.** `a-correction-lands` and `register-the-retraction` name `stale-claim-check` in
   a `**Mechanised by:**` line. But `a-repo-split-kills-relative-links-silently`,
   `sanitise-before-sharing` and `publish-lessons-weekly` are all enforced today by
   `harvest.py --check` and none of them says which check enforces it. The `implemented_by`
   field closes that gap — a rule and its enforcement drifting apart is the failure this whole
   format exists to prevent.
