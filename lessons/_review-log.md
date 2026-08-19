# Review log

One line per weekly pass, newest first. **An empty pass is a valid outcome and still gets
logged** — three empty passes in a row is a signal worth reading.

Format: `YYYY-MM-DD · what was swept · what was harvested`

Project repos are referred to generically. Naming a private repo here would leak it into a
public one — see [sanitise-before-sharing](../rules/agent-workflow/sanitise-before-sharing.md).

---

## 2026-08-19 (sixth) - off-cycle, two rules given directly by the user

Harvested **2 rules**, both `agent-workflow`, both from the same session as the previous entry and
both stated by the user rather than inferred by me.

**`unexpected-means-stop-and-propose.md`** - do the straightforward thing; when the outcome is not
what you expected, stop, report, propose, implement nothing. The tell it names is the sentence
**"I noticed X, so I did Y"** - which reads as diligence and is a decision taken on the user's
behalf, recorded as an observation. The incident: a diff showed 12 values coming back blank, I
formed a theory on the spot, implemented a conditional, verified the 12 returned, and shipped it
inside a defect fix that read as thorough. Every part of the theory was wrong, and the check that
would have collapsed it was one command, run four messages later only after the user rejected the
explanation.

Most of the work in this one is the **boundary against `close-your-own-gaps`**, which says the
opposite in its own domain. The test that separates them: *does the resolution change what the
user receives?* A gap in your own rigour has exactly one right answer, so act. A choice between
defensible readings of the data has more than one, so propose. Without that section the two rules
read as contradictory and the weaker one gets ignored.

**`watch-the-context-budget.md`** - track context continuously, prompt to compact at 40%, state
the number, never compact unilaterally. It replaces the common "suggest compacting after 20-50
prompts" heuristic, which is unusable because turns and context barely correlate: one command in a
large repo can cost more than thirty conversational turns, so a turn-count trigger fires latest in
exactly the tool-heavy sessions that need it earliest. Includes the reason 40% and not 90% (a
compaction near the ceiling happens under pressure and mid-task rather than at a boundary), and
the failure mode it prevents: **degradation is silent and feels exactly like ordinary
confidence** - a model reasoning from a summary experiences recollection, not a gap, so it answers
fluently without re-reading. Same incident, viewed from the other side.

Rules 36 -> 38; links resolve; sanitise scan clean.

## 2026-08-19 (fifth) - off-cycle, user instruction after a four-message wrong diagnosis

Harvested **1 rule**: `rules/data-engineering/never-patch-a-key-to-force-a-join.md`.

**Join on the code as it is. Never invent, rewrite or hand-author a translation table to make a
join succeed.** Three-step escalation: join as-is and count misses both ways; if a lot is missing,
question the KEYS not the rows (same authority? same standard? same granularity? same vintage?);
if a lot is still missing, stop and ask - propose, implement nothing.

The incident is unusually clean. A hand-written, undocumented 21-row table mapped `our_code ->
their_code` and existed only to make one join land. Tested against the issuing authority's own
roster: **their column 21 of 21 valid, our column 1 of 21** - and that one only because an earlier
defect had already corrected it. There was no second numbering system; there were 20 wrong codes
in our frame, and the table was a list of what each should have been. The consumer applied it
backwards, rewriting the authority's correct value into our invalid one so the merge would land.

Costs, all measured: it patched one join out of many, so one unit got its population right and its
economic output **from the wrong province 200 km away, a 17.3% error**; five rows collided with
codes already in the frame as separate zero-overlap polygons (one district had 11 frame rows
against the authority's 10); and my own "fix" - making the rewrite conditional after seeing 12
values go blank - did not repair a mis-seat but changed which half of a split unit got the whole
population, leaving **28 shipped columns in which two blocks from one source disagree**.

The rule carries the correct counter-pattern from the same repo: rewrite YOUR OWN codes, never the
authority's, and propagate the correction through every derived file. A code correction is a frame
rebuild applied everywhere, not a dictionary inside one join.

And the generalisation past codes: **if your join needs a similarity threshold or a manual override
list to succeed, the key is wrong.** Four sibling scripts in the same project forced joins with
difflib and produced the identical defect class - one rural unit receiving a provincial
administration's entire budget.

Worth recording honestly: I defended the patch across four user messages before checking either
column against the issuing authority. The check took one command.

Rules 35 -> 36; links resolve; sanitise scan clean. (Two rules from another session landed on main between the previous pass and this one -- rebased onto them, files disjoint.)

## 2026-08-19 (fourth) · off-cycle, from a retrospective on how four defects hid

Harvested **1 rule**: `rules/analytics/name-the-blind-spot.md`.

Asked how a defect had stayed hidden and what found it, a sweep turned up **four** instances of
one shape in a single project — three from that day, one already written up five days earlier and
never generalised:

| the check reported | the truth |
|---|---|
| "0 corrupt values in any text column" | 164 rows corrupt; the guard tested one codec's byte signature and the other codec's corruption lands inside the target script's own Unicode block |
| "0 of 77 groups match; source B is 1.7-19.1% low" | 77/77 match, max difference 0; it summed 204 detail columns against a total that also covered 12 columns outside them |
| "14,786 name mismatches" | approximately none; the join key had been decoded with the wrong codec |
| "coverage +951" | +951 filled AND 12 silently lost |

The rule: **every check has a null space — the set of data changes that leave its output
unchanged — and you state it before you read the result.** A check's output is a statement about
the *subject*; it has no vocabulary for its own failure, so a broken instrument emits a confident
claim about the data rather than an error. In three of the four the wrong answer arrived with a
corroborating story, and in one the accusation was even partly true.

The observation that makes it bite, and the reason it is a separate rule rather than a line in
`validations-must-fail`: **implausibility is the detector we reach for by default and it is
anti-correlated with harm.** Sorting the four by damage inverts the detection table — the two
caught by "that number looks wrong" were harmless checks that cost hours, while the two that
reached or nearly reached shipped data were found by an outside party and by a structural
partition. A defect big enough to look wrong is a defect too small to ship.

Cross-linked with `validations-must-fail` in both directions — that rule covers a guard that never
fires, this one a guard that fires, returns a number, and is trusted. Honest about coverage: no
single guard catches all four, and the write-up says which catches which.

Rules 32 -> 33; links resolve; sanitise scan clean.

## 2026-08-19 (third) · off-cycle, from a defect introduced while fixing a defect

Harvested **1 rule**: `rules/analytics/a-delta-is-three-numbers.md`.

A source migration reported `coverage 65,541 -> 66,492 (+951)`. The first build of that migration
also silently blanked 12 rows that previously had values. After the bug was fixed, coverage read
**+951 again** — the losses exactly offset by gains elsewhere. The headline was true both times
and distinguished nothing; only a row-level diff against a baseline captured *before* the rebuild
separated 963-filled-12-lost from 951-filled-0-lost.

The rule: report **gained, lost and changed separately, never the net** — a net can be exactly
correct while its composition is wrong. With the observation that makes it bite: a net *gain*
reads as good news and therefore suppresses the very check that would find the defect, where a
net loss would have been investigated at once.

It carries a second, mechanisable guard from the same incident: the bug was an **inverted lookup
table**. Both its columns were unique, so it looked like a clean bijection — but 6 of its target
values were themselves valid keys, making the inverse ambiguous. **Uniqueness on both columns does
not make a mapping invertible**; the test is `set(targets) & set(valid_keys)`, one line, not run.

Deliberately NOT published: a third observation from the same session — that all three of my
errors that day were caught by a check returning something *implausible* (14,786 mismatches,
0 of 77 matching, 12 unexpected losses) rather than by any check passing, and that the most
dangerous of them was the one that arrived with a compelling explanation attached. True, and I
could not reduce it to a guard that runs, so it stays as prose in the project repo rather than
becoming a weak shared rule.

Rules 31 → 32; links resolve; sanitise scan clean.

## 2026-08-19 (later) · correction to the same day's pass

`inspect-what-you-downloaded.md` was published with an incident that said three stub files had
been skipped **silently**. Verified against the source project's code the same day: they were
not. A row-count guard rejected them, the build raised unless the region-period was on an
evidence-bearing allowlist, and the whole case was documented by name in the function's
docstring. The claim had been inferred from the *data* — clustered nulls, files on disk —
without reading the code that handled them.

**The guidance was unaffected and stands**; the incident was rewritten to describe a guard that
worked, which is the more useful story: it now carries the row-count-not-byte-size point, the
earlier version of that check that threw away 15 good regions by sniffing for `404` inside
numeric data, and the third stub that surfaced only after the hard failure was added.

Rule count unchanged at 31. Logged rather than quietly amended, because a rule whose incident
turns out to be wrong is exactly the thing this repo must not accumulate.

## 2026-08-19 · off-cycle, triggered by a silent ingest failure

Harvested **1 new rule** and **strengthened 1 existing** — deliberately not two new rules.

**New:** `rules/data-engineering/inspect-what-you-downloaded.md`. An ingest pulled 693 files
from a government portal; three came back as ~1.3 KB stubs against a median of 83,933 bytes,
served with a normal successful HTTP response. Single header line, no detail rows, name field
mojibaked. Nothing failed — saved, cached, marked fetched, parsed to zero rows, skipped. Two
entire regions lost a year of a demographic block (102 units). A third stub had caused no
damage purely by luck. **The screen that found all three is one sort by file size**, never run
in twelve months of ingests. The rule's core claim: the check is not "did the download succeed"
but "is this the data", and the strongest version counts *records extracted*, not bytes.

**Strengthened:** `completeness-checking.md`. The requester asked for a second rule on
output-vs-input completeness, but that rule already covered detection and already said not to
accept a mismatch as a limitation. Adding a second would have drifted. What it genuinely
lacked, and now has: the **three-outcome decision procedure** after a mismatch (resolved /
explained-and-enumerated / open-with-a-route, and the decision logged), and **Incident D** —
a 3.8% aggregate gap that looked genuine (missing units were tiny islands, median area 1,023
vs 27,087) until partitioned by group × period, at which point 102 of 753 turned out to be two
entire urban regions at 100% in one period. **The aggregate percentage concealed it
completely.** Cross-linked both directions.

Rules 30 → 31; links resolve; sanitise scan clean, plus one judgement the scan cannot make —
a mojibake sample was in the source project's own script and was replaced with a
language-neutral one, since it hinted at the domain.

## 2026-08-18 · off-cycle, triggered by a reader finding an omitted set member

Harvested **1 rule**: `rules/analytics/summaries-must-carry-the-whole-set.md`.

A data-vintage defect affected two groups (48 units with a five-period gap, 88 units with a
one-period gap). Both were reported at discovery and both are in the project's findings log and
task board. **Every summary written afterwards kept the 48 and dropped the 88** — the same-day
impact line, a cost table, the numbered project rule extracted from it, the rule published to
THIS repo, and the defect write-up, which used the 48-unit group as a worked control without
saying a second group existed. The reader found the missing group themselves a day later and
reasonably read it as withheld.

The selection is the finding: summaries keep the most **dramatic** member and drop the
**largest**. Here the dropped group was 1.8x bigger, and lost every retelling because a
one-period gap is undramatic.

Also **corrected the instance in this repo**: `agree-the-output-contract-first.md` carried
"136 units mis-dated, one of them by five periods" in both its cost table and its earned-from
line — the exact indefinite-singular phrasing the new rule prohibits. Both now carry the
cardinality and the split. Fixing the class without fixing the published instance would have
left this repo contradicting its own newest rule.

Rules 29 → 30; links resolve (0 broken); sanitise scan clean — no names, paths, emails or
project-specific terms in the new rule.

## 2026-08-15 · sanitising pass

Audited everything published in the seed pass for information that should not be in a public
repo. Found and removed: a private repo name, a machine username in two skill paths, and a
project-internal defect write-up that carried real variable names and preliminary results
from an unpublished study.

Harvested **1 rule** — [sanitise-before-sharing](../rules/agent-workflow/sanitise-before-sharing.md)
— and mechanised it as a leak scan in `harvest.py --check`, with the self-test extended to
prove the scan fails on seeded leaks.

The seed pass had no such rule and no such check. That is why this was needed.

Also added **`retrieve-lessons`**, closing the loop: until now this repo could publish a lesson
and nothing pulled it into the next project, so each lesson was paid for once and used once.
It adopts by pinned link rather than by copy, and only the categories a repo has evidence for.

And **1 more rule** —
[prompt-and-store-config](../rules/agent-workflow/prompt-and-store-config.md), mechanised as
`lib/skillconfig.py`. The leak scan could say *a hardcoded path is wrong* but gave the value
nowhere to go, so three skills kept theirs as functional defaults. A prohibition with no
supported alternative gets worked around, not followed.

## 2026-08-15 · repo created

Swept one active project repo after a two-day remediation.

Harvested **7 rules** across 6 categories and **2 skills**, from an incident set of 11
self-inflicted defects — see [nine-silent-failures.md](nine-silent-failures.md).

Mechanised: output review → `verify-outputs`; the harvest pass itself → `lesson-review`.
Left as prose (not mechanisable): judging whether an invariant matches the domain, whether a
caption matches its figure, whether a convention is inside its domain.

Not yet harvested, deliberately: that project's board-consistency checker is close to
portable but assumes a specific Kanban markdown shape; revisit if a second project adopts the
same board format.
- 2026-08-15 — published rules/data-engineering/parallel-variants-same-schema.md (parallel measurements of one quantity must share an identical variable set; earned from a two-source age-structure block that differed in names, denominators, coverage and missing-value convention).
- 2026-08-15 — published rules/agent-workflow/close-your-own-gaps.md (a realised omission is work to do, not a question to ask; earned from three self-noticed verification gaps surfaced as caveats rather than closed, whose closure then found six defects no automated check could see). Cross-linked from rules/analytics/review-every-output.md, which describes the same failure one level down. Mechanisable parts extracted as two assertions (a silent skip must be fatal; a stale input must be refused); the disposition itself left as prose rather than shipping a crude proxy. Leak gate clean on the new file. Note for a future pass: `verify-outputs/test_self.py` reports CANNOT RUN under a bare interpreter — it passes 6/6 given matplotlib and pandas, so the harvest report's "cannot run" is an environment gap, not a failing test.
- 2026-08-16 — published five rules from one session. `rules/analytics/report-both-sides-of-a-comparison.md` (state matched AND unmatched, with counts, scope, tolerance and both-direction key gaps; earned from a headline agreement percentage that averaged our own defect into a reassuring number, and a correctly-scoped "0 values changed" that read as a claim of full agreement). `rules/data-engineering/status-fields-must-be-earned.md` (a status is a claim and must come from evidence; earned from a manual bulk ingest where 3 of 206 items were missed, all 206 were recorded complete, and the contradicting duplicate hashes sat unqueried in the manifest for twelve days — includes a reproduced non-idempotent reconciler and four assertions worth writing). `rules/agent-workflow/cannot-is-a-task.md`, `read-the-manual-first.md`, `shut-up-and-work.md` (three agent-behaviour rules from the same incident: declaring a source unobtainable while holding an unused tool; inventing a download route while the written procedure sat unread; and padding that let a scoped claim be misread). Cross-linked: the comparison rule to completeness-checking, the status rule to completeness-checking, cannot-is-a-task to close-your-own-gaps, shut-up-and-work to the comparison rule as the tie-break. Mechanisable parts named in-file rather than shipped as code this pass: a generated comparison report with an explicit `unexplained` bucket, and four manifest invariants (status implies file exists at recorded size; no shared sha256 across distinct items; the row→artifact key field is non-null; reconcile is idempotent). Sanitise pass: leak gate clean on all five new files against project, collaborator, portal and path terms; one flagged hit was the substring 'surin' inside 'reassuring'. Domain identifiers (country, agency, portal, region names) abstracted out — the incidents are told as "a government data portal" and "regions", since the project is a collaborator's unpublished research.
- 2026-08-16 — published rules/data-engineering/adjudicate-with-an-external-source.md (a mismatch between two datasets cannot be settled by those two datasets; go to the issuing authority, a published standard, a genuinely independent third party, or the disputed file's own internal contradiction — and state which tier each answer came from). Earned from resolving a disagreement between two files from one agency by citing this project's own code comment and defect log, i.e. the same claim counted as two sources; asked how it had been confirmed, the honest answer was that it had not. Two traps recorded that are easy to get backwards: a source cached inside the repo can still be external (what matters is who produced it), and a source that looks independent may not be — one candidate was discarded mid-check on discovering its "independent" identifier column was a reformatting of the disputed code itself. Cross-linked to report-both-sides-of-a-comparison (how to report a comparison vs how to settle one) and to completeness-checking (reconcile populations, not just the disputed label). Not mechanised: source-tier judgement is not automatable, and shipping a crude "cite ≥2 URLs" proxy would reward exactly the copy-of-a-copy corroboration the rule exists to catch. Sanitise pass: leak gate clean on the new file and the README row against project, agency, region and path terms; the incident is told as "two boundary files from one agency" and "an administrative code registry", since the source project is a collaborator's unpublished research. Note the check paid for itself — run properly it also surfaced a frame-building defect that had been fusing two distinct entities into one row.
- 2026-08-16 — published two rules and strengthened two, from one reconciliation session. NEW `rules/agent-workflow/characterise-once-not-per-question.md` (scope the answer to the question, never the investigation; earned from five separate things reported and then found wrong or incomplete in one session, every one surfaced by a follow-up question rather than by the investigation — the user's words were "why do you always leave information behind"). The fix shipped as a script that partitions every difference by cause in both directions with an explicit `unexplained` count, not as a resolution; includes the corollary that a projection and a measurement must not share a voice, earned from "should close to 3" that measured 25. NEW `rules/analytics/solve-the-space-not-the-samples.md` (if the explanation space is finite and describable, formulate it as feasibility and solve it exactly — a hypothesis hunt can only ever say "not this one"; earned from hours of variant-testing replaced by a single integer-program infeasibility certificate, bounded by binary search at ~27,000x the match threshold). Its second half is the trap that would have made the solve as weak as the sampling: `success == False` covers infeasible, timeout and numerical failure alike, so a load-bearing negative needs the status code, a tolerance bound, and a positive control that comes back FEASIBLE on the same harness. STRENGTHENED `rules/data-engineering/adjudicate-with-an-external-source.md` with a third trap — two files from the same author are ONE source; independence is a property of authorship, not filename, date or directory. Caught only because the data owner said so; the agreement had been reported as provenance evidence. Plus the self-inflicted twin: a derived statistic presented as corroboration that was arithmetically implied by something already reported. STRENGTHENED `rules/agent-workflow/delegation-and-supervision.md` with "re-derive the load-bearing claim yourself, on a different path" — of three agent claims a conclusion rested on, one was a non-sequitur and one circular, both specific, quantitative and unfalsifiable by anything else in the report; the check that worked was re-implementing the decisive test from scratch against a different input, not re-reading the agent's script. Not mechanised: all four are judgement rules, and the one mechanisable part (the partition-by-cause report) is described in-file since its shape is project-specific. Sanitise pass: leak gate clean on all four files and the two README rows; domain identifiers (country, agency, unit type, region names, the area unit) abstracted to "administrative units", "regions", "area units" and "a reference dataset", since the source project is a collaborator's unpublished research. One exact row-count pair was removed on the second read — it was a measurement of the collaborator's two files rather than a defect count, which is exactly the distinction no scan can make. Pre-existing note: one place name survives in `skills/verify-outputs/SKILL.md` as general geographic knowledge alongside a European port, judged not identifying; `verify-outputs/test_self.py` still reports CANNOT RUN without matplotlib.
- 2026-08-17 — published rules/coding/scratch-code-lives-outside-the-repo.md (scratch/probe code is written outside the repository entirely — a temp directory, a scratchpad, anywhere version control never sees it — not inside the repo's own scratch folder with a "delete it when done" intention). First drafted as "write it in-repo, delete it once it's answered its question," then revised on the spot, on direct project feedback, once it was clear "delete after" is the weaker rule: it depends on a step that gets skipped under load, and it was skipped 150/150 times in the incident that motivated the rule in the first place. Earned from the same reconciliation project's follow-on covariate-frame fix: over 150 ad-hoc probe scripts accumulated in the project's in-repo scratch directory over one session, none deleted, and the one piece of reusable tooling the session actually produced was not promoted from any of them — it was written a second time, from a clean start, and saved properly in the real script directory. Names the concrete risk of leaving probes in-repo: they can be mistaken for the real pipeline, or cited back later as if a considered source, the same failure shape as two-files-one-author in adjudicate-with-an-external-source. Cross-linked to characterise-once-not-per-question (the real script that should exist) and close-your-own-gaps (cleanup deferred is cleanup skipped). Not mechanised: which scripts are disposable vs. load-bearing is a judgement call; the guard is procedural (never write it in-repo to begin with) rather than a check that runs later. Sanitise pass: leak gate clean on the new file and README row; no project-identifying detail beyond the already-public fact that it was a land-use reconciliation task.
- 2026-08-17 — published rules/agent-workflow/known-blast-radius-demands-scoped-fix-everywhere.md (the moment a change's affected set is known precisely, that scoping applies to every downstream artifact the change touches, not only the one under discussion when the question was first asked). Earned from the same project's frame-correction fix: the affected set was ~5 of 7,583 rows, known exactly in advance. For the first of eleven downstream files, a scoped `--only`-rebuild-and-splice pattern was built after being asked directly why a full rebuild was needed for a handful of rows. For the other ten, the same question was never re-asked, so each was simply re-run in full because that was the only mode each script supported — two of them cost over two hours of combined compute recomputing 99.93% of a dataset already known to be unchanged, caught only when the person waiting asked why a five-row fix was taking so long. Cross-linked to characterise-once-not-per-question as the execution-cost twin of the same failure shape (a decision made once for the artifact under discussion, not re-made for every artifact sharing its shape) and to solve-the-space-not-the-samples (this is about cost once the fix itself is already understood, not about proving it). Not mechanised: recognising "same problem shape" across files is a judgement call; the guard is procedural (check the whole downstream list up front, before running any of them). Sanitise pass: leak gate clean on the new file and README row; incident told generically as "administrative units" and "a frame correction," no project-identifying detail. Unrelated to this pass: pulled a concurrent push (skills/scripts/link-skills.sh) that introduced a machine path leak (a username in a path) — not touched here, flagging for whoever owns that file next.
- 2026-08-17 — published rules/agent-workflow/eta-needs-a-denominator.md ("almost done" needs a denominator, not a vibe — before recommending against interrupting a long-running job, compute done/total explicitly, not just recent velocity). Earned minutes after the blast-radius incident above, on the same session: a background rebuild had been running 90+ minutes, reported as "43, then 51, then 74 files touched" with no total, and recommended as "not worth interrupting" alongside a genuinely-close sibling job. Asked "how many total?", a two-minute manifest check showed the real total was ~378 — 74 was about 20% done, not close. The recommendation had used judgement-sounding language ("close enough," "not worth it") without a single measured fraction underneath it. Cross-linked to known-blast-radius-demands-scoped-fix-everywhere as the decision this rule feeds (you can't judge whether a scoped rebuild is worth building without first knowing how far from done the naive one actually is). Not mechanised: recognising when an ETA claim is being made without a denominator is a judgement call on prose, not a pattern a linter catches. Sanitise pass: leak gate clean on the new file and README row; incident told generically, no project-identifying detail.
- 2026-08-17 — published rules/data-engineering/check-for-a-local-copy-before-refetching.md (a pipeline that fetches remote data must resolve against local copies first, and you must verify which path it actually uses before letting it run). Third rule from the same session, and the most expensive: a pipeline re-downloaded ~38 GB of raster inputs over roughly two hours while all 344 required files sat committed in the same repository via Git LFS, in a directory created by a sibling script specifically so they would not need re-downloading — that script's own docstring said so in its first paragraph. The consuming script simply pointed at the other directory (the gitignored raw cache) and nothing had ever wired it across. Documents why it survives review: the download code is correct, the data genuinely is in the repo so "do we have it?" answers yes, the gitignore comment ("~38GB, re-downloadable by <script>") reads as a considered decision, and large geospatial jobs are legitimately slow so unnecessary work is indistinguishable from normal cost. Found only when the data's owner asked "I thought all data is in repo" — a two-minute check confirmed all 344 present, and a ten-line resolve-preferred-path helper eliminated the entire download. Cross-linked to read-the-manual-first (the local copy was documented; nobody looked) and eta-needs-a-denominator (a fetch never questioned is a fetch whose size was never measured). Not mechanised: detecting "this fetch has a local twin" needs repo-specific knowledge of which directories mirror which; the guard is procedural (grep for a sibling/-compressed/-cache/LFS copy before starting any fetching run). Sanitise pass: leak gate clean on the new file and README row; incident told generically as "a geospatial pipeline" and "national raster files", no project-identifying detail.
- 2026-08-17 — published rules/data-engineering/verify-conversions-against-the-original.md (a converted copy is a CLAIM OF EQUIVALENCE; measure it against the original on the statistic the pipeline actually computes, per category, before committing it). Earned the same day: an int-rounding raster compression, committed to make ~38 GB of gitignored source small enough to keep in-repo, whose docstring asserted the rounding "washes out over any unit's worth of pixels (thousands), so it has no material effect on the zonal-stats sums". Nobody measured it. Measured later: total population -0.32%, one sex's total -5.42%, a single age band -87.83% with 6,949 of 7,583 units going to exactly zero. The intuition is backwards — the source held FRACTIONS per pixel, so rounding is not noise around the value but a one-directional floor applied BEFORE the sum, compounding with pixel count instead of averaging away. Records the two-stage danger: the bad copies sat committed and harmless for weeks, then a well-motivated later change (point the consumer at them, skip the download) armed the damage in one line. Surfaced only because an unrelated consumer-side guard fired, and the obvious reading was that the guard was too strict for the small test subset — hence the closing guard, treat a firing check as evidence about the data, not a threshold to relax. Prescribes the specific checks that would have caught it: the downstream aggregate both ways, broken down PER CATEGORY (the grand total looked fine at 0.32% while one slice lost 87.8%), a count of newly-zero entries (6,949 would have screamed), a real checksum where the claim is losslessness, and asking what fraction of values sit below the new dtype's resolution — if most do, the conversion deletes rather than approximates. Cross-linked to check-for-a-local-copy-before-refetching (that rule says prefer the committed copy; this one is why it must be proven equivalent first) and validations-must-fail. Not mechanised: the aggregate to compare is pipeline-specific, so the rule names the checks rather than shipping a generic differ. Sanitise pass: leak gate clean; told generically as "population raster tiles" and "administrative units".
- 2026-08-17 — off-cycle pass, triggered by a defect write-up. Published
  `rules/data-engineering/read-the-authority-never-type-the-table.md`: a hand-typed
  4-region lookup omitted three area codes, silently dropping 3.7% of the frame from
  every regional statistic in a stakeholder handoff, while the authoritative crosswalk
  sat committed in the same repo and was already read by another script. Includes the
  second, harder half — the first fix patched the instance rather than deleting the
  literal. Sanitised: the test statistic and p-value are a collaborator's unpublished
  result and were reduced to magnitudes. Rules 27 → 28; health check green (0 broken
  links, 0 rules without a named incident, all self-tests PASS).
- 2026-08-17 — same pass, second half: published the incident write-up
  `lessons/numbers-that-cannot-fail.md` (four defects, one mechanism: a typed literal has
  nothing to disagree with, so no gate can detect it — and two of them concealed each other,
  because the statistic that would have exposed a bad population was itself hardcoded).
  Added a Lessons section to the README, which had none, and linked both write-ups.
  Sanitise pass also redacted a leaked username in a machine path in
  `skills/scripts/link-skills.sh` — pre-existing, illustrative rather than functional, so
  redacting it broke nothing. Health check now fully clean for the first time: 0 problems,
  0 broken links, 28 rules all with a named incident, all self-tests PASS.
- 2026-08-17 — third off-cycle pass today, user-requested. Published
  `rules/data-engineering/agree-the-output-contract-first.md`: output structure is a
  DECISION, not a fact, so it must be asked rather than checked or assumed — the explicit
  exception to "don't ask what you can check", and the rule states that boundary because
  the two otherwise appear to conflict. Earned from a derived dataset built on four
  unstated structural assumptions, three of which became remediation commits after the
  work was declared finished (including a period-matching rule that mis-dated 136 units,
  one by five periods). Also names the cost that does NOT show up as a rebuild: a column
  layout that shipped as an unagreed guess and was never challenged. Rules 28 → 29;
  health check green.

