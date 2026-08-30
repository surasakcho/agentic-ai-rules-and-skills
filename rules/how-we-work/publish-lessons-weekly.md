# Publish Portable Lessons — Review Weekly

**Task type:** agent workflow — keeping shared knowledge alive across projects.

Canonical cadence: [CADENCE.md](../../CADENCE.md). Executed by [lesson-review](../../skills/lesson-review/).

---

**Lessons, rules and reusable checkers that are true outside this project belong in the
shared repo, not stranded here.** Review and publish **at least once a week**.

**Shared repo:** <https://github.com/surasakcho/agentic-ai-rules-and-skills>
**Skill:** `lesson-review` — runs the harvest and the health check.

The decay mode is specific and predictable: lessons keep being *learned* in project repos
and stop being *extracted*. Six months later the shared repo describes a way of working
nobody follows, and the real knowledge sits in a dozen `LESSONS.md` files nobody outside
each project will open.

**The weekly pass:**

1. **Harvest.** Sweep for knowledge stranded in this repo — `LESSONS.md`, `DEFECTS.md`,
   `Q-and-A.md`, `research/*.md`, new numbered rules in `CLAUDE.md`, and scripts under
   `scripts/` that are repo-agnostic checkers rather than pipeline steps.
2. **Filter.** Most stays. A lesson goes to the shared repo only if it holds with different
   data, a different domain, a different language — **and names a real incident with a
   cost.** Advice without a scar is opinion. If an existing shared rule covers it,
   *strengthen that rule* rather than adding a second one that will drift.
3. **Mechanise what can fail.** `prose < checklist < test < gate`. If a rule can be a check
   that runs, it ships as code with a self-test, not as prose. About half can be; be honest
   about the other half rather than writing a crude proxy and calling it enforcement.
4. **Verify what is already shared.** Skills' self-tests must pass, links must resolve,
   every rule must still be true. **A rule contradicted by later experience gets deleted,
   not hedged** — git keeps the history, and a hedged rule is one nobody can act on.
5. **Publish and log.** Push, then append one line to the shared `lessons/_review-log.md`.

**An empty pass is a valid outcome and still gets logged.** Three empty passes in a row is
a signal worth reading: either the projects are genuinely quiet, or lessons are not being
written down anywhere the sweep can find them — which is the more serious problem.

**When to run it off-cycle:** at the end of a phase or remediation, and whenever a task
produces a defect write-up or a checker that would work in another repo. That is when the
detail is still in reach; a month later only the headline survives.

## The incident

This rule was written the day a two-day remediation produced eleven reusable lessons and two repo-agnostic checkers, all of which would have stayed in one project repo. The cost of *not* having it is invisible by construction: you never see the second team hitting the defect the first team already solved.
