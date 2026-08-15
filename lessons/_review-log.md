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
