# Review log

One line per weekly pass, newest first. **An empty pass is a valid outcome and still gets
logged** — three empty passes in a row is a signal worth reading.

Format: `YYYY-MM-DD · what was swept · what was harvested`

Project repos are referred to generically. Naming a private repo here would leak it into a
public one — see [sanitise-before-sharing](../rules/agent-workflow/sanitise-before-sharing.md).

---

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
