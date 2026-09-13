# Cadence — how this repo stays alive

**Review and publish at least once a week.**

A lessons repo decays in a specific, predictable way: the lessons keep being *learned* in
project repos and stop being *extracted*. Six months later the shared repo describes a way of
working nobody follows any more, and the real knowledge is scattered across a dozen
`LESSONS.md` files nobody outside that project will ever open.

The weekly pass exists to stop that, and it is deliberately small.

---

## The rule

> **Once a week, sweep the active project repos for lessons, rules and skills that are
> portable, and publish them here. Then check that what is already here is still true.**

Run it with the [`lesson-review`](skills/lesson-review/) skill, which does the mechanical
parts — finding candidates, detecting drift, checking links — and leaves the judgement to you.

```bash
# from any machine, with the project repos checked out
/lesson-review
```

## What the pass covers

**1. Harvest.** Look in each active project for knowledge that is stranded there:

- `LESSONS.md`, `DEFECTS.md`, `Q-and-A.md`, `research/*.md`
- new numbered rules in a project `CLAUDE.md`
- new scripts under `scripts/` that are repo-agnostic checkers rather than pipeline steps
- commit messages describing a defect *class* rather than a single fix

**2. Filter.** Most of it should stay where it is. A lesson belongs here only if it is true
outside the project that produced it. Ask:

- Would this still be true with different data, a different domain, a different language?
- Does it name a real incident with a cost?
- Is it already covered by an existing rule here? (Then strengthen that rule, don't add one.)

**Expect the answer to be yes, and expect the strengthening to be a cross-reference.** The corpus
is now large enough that the same failure reaches two categories from two directions, and a
candidate that feels new usually is the *other end* of something already written. Four candidates
in one evening resolved that way — a split needing a partition check, already in
`parallel-variants-same-schema`; a grouping key that is null, already in
`read-the-authority-never-type-the-table`; and two more one category over.

**So the corpus's gap is navigation before it is coverage.** A rule nobody can find from where they
are standing is as absent as one nobody wrote — and adding the second copy is worse than either,
because the two then drift. When a candidate resolves to an existing rule, **put the pointer where
the person who raised it was looking**, not only in the rule that already knew.

**3. Mechanise what can fail.** Before writing a rule as prose, ask whether it can be a
check. `prose < checklist < test < gate`. If it can run, it goes to `skills/`.

**4. Verify what is already here.** Rules rot:

- Do the linked incidents still resolve?
- Do the skills still run? (`lesson-review` executes each skill's self-test.)
- Has a rule been contradicted by later experience? **Contradicted rules get deleted, not
  hedged.** Git keeps the history.

**5. Sanitise — blocking, and it happens last.** Portability and disclosure are different
questions that feel like one. Before anything is pushed, scan for **people, places, paths and
findings**: see [sanitise-before-sharing](rules/how-we-work/sanitise-before-sharing.md).
The first three are gated by `harvest.py --check --deny …`; the fourth needs a reader.

**6. Publish.** Commit and push. A weekly pass that ends on an unpushed branch has not
happened.

> **The commit convention changed on 2026-09-13, and the history is deliberately not
> consistent.** Commits **before** that date carry a `Claude-Session:` trailer and name the
> machine they were written on. Commits **after** it carry neither: this is a public repo, and a
> session URL and a host name are exactly the people-and-places the sanitise step above exists to
> keep out.
>
> **Do not "fix" the old commits.** Rewriting the published history of a public repo is
> destructive, it breaks every commit link anyone has ever quoted, and the exposure is already
> indexed — so the rewrite costs more than it recovers. It is the operator's call and nobody
> else's. The inconsistency is the record of a decision, not an oversight.
>
> Keep `Co-Authored-By:` — it names an author, not a place.

## What "done" looks like

A pass is complete when:

- [ ] every active project has been swept since the last pass
- [ ] every new rule names its incident and its cost
- [ ] anything mechanisable is in `skills/`, not `rules/`
- [ ] every skill's self-test passes (`CANNOT RUN` is not a pass)
- [ ] `README.md`'s rule table matches what is actually in `rules/`
- [ ] the leak scan is clean, and nothing published carries someone else's unpublished results
- [ ] the work is pushed

## The honest failure mode

The most likely way this rule dies is not that a week gets skipped — it is that the pass
becomes a ritual that touches nothing. **A pass that harvests nothing is a valid outcome and
should be recorded as such**, in `lessons/_review-log.md`, with a date and one line. Three
empty passes in a row is a signal worth reading: either the projects are quiet, or nobody is
writing lessons down where the sweep can find them.
