# A repo split kills relative links, silently

**Task type:** coding — extracting a directory into its own repository, or moving one between repos.
**Related:** [`known-blast-radius-demands-scoped-fix-everywhere`](../how-we-work/known-blast-radius-demands-scoped-fix-everywhere.md)
— the general discipline; a split has a knowable radius and it is the link graph.
[`a-task-in-one-place-vanishes`](../how-we-work/a-task-in-one-place-vanishes.md) — the same class of
loss, for work rather than references.

---

## The rule

> **Before splitting a directory out of a repo, enumerate every relative link that escapes it, and
> rewrite those to absolute URLs in the same commit as the split.**

A relative path that climbs above the new root does not error at split time, at commit time, or at
push time. **It fails when a human clicks it, weeks later, and the failure looks like a typo rather
than a structural consequence.**

## What escapes, and it is more than documentation

- **Markdown links** reaching `../../docs`, `../../ops`, `../../tools`.
- **Imports and config paths** that climbed out of the directory. *If the code imports shared
  infrastructure by relative path, the split is not clean and should be stopped until it is.*
- **Machinery the documents assume exists**: the agent definitions the review process needs, the
  tools the docs cite by path, the registries a checker reads.

**The last one is the trap.** A split that carries the documents and leaves the machinery produces
a repo that reads correctly and cannot actually run its own process. One extraction moved every
document faithfully and left behind the agent definitions the assurance chain depends on, so the
chain was intact on paper and unrunnable in fact.

## Also decide, out loud, what does NOT move

**Shared, cross-venture state should stay in one place even when that place is now inconvenient.** A
retraction registry, a knowledge base, a spend ledger: **a split registry is worse than one registry
somewhere awkward**, because a retraction filed in one half is invisible to the other and nothing
reports the gap. Cite it by absolute URL from the new repo and say in the new repo's instructions
that this was deliberate.

## Guard

- **Grep for escaping relative paths and drive the count to zero** before pushing. It is mechanical;
  do it rather than trusting a read-through.
- **Add the ignore file before the first run, not after.** A freshly split application repo with no
  ignore rules will offer its database and user uploads for commit the first time it runs.
- **Run the test suite in the new repo, standalone**, to prove the extraction is self-contained.
- **Do not delete the original until the new one is verified.** Keeping both briefly costs nothing;
  the delete is the only step with no undo.
- **If the split is not the project's lifecycle graduation, say so in the new repo.** Otherwise the
  move itself gets cited later as evidence of maturity it does not represent.

---

*Earned from:* extracting a venture into its own repository on 2026-09-11. The code was cleanly
decoupled, and four documents still carried links that climbed above the new root; the first pass
also left behind the sixteen agent definitions the repo's own review process requires.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: deferred
observable: 'relative links that resolve outside the repo root, an ignore file absent on the first run, and the test suite never run standalone in the new repo'
trigger: 'check exit code, in the same commit as the split'
check: 'dest resolves outside root -> problem; drive the escaping-link count to zero before pushing'
escape: 'rewrite escaping links to absolute URLs in the split commit'
implemented_by: 'skills/lesson-review/harvest.py'
```
