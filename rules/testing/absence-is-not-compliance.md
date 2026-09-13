# An absent subject is not a passing check — "nothing found" and "nothing looked at" are different answers

**Task type:** testing — checkers, audits, coverage reports, guards, and any status a machine
derives from them.
**Related:**
[`validations-must-fail`](validations-must-fail.md) — *"ask what would still be green if it were
already broken"*. This rule is the commonest concrete answer to that question: **green, because
the thing it inspects was not there.**
[`status-fields-must-be-earned`](../data-engineering/status-fields-must-be-earned.md) — a status
derived from an assumption rather than an outcome. An absent subject is the assumption that
writes itself.
[`completeness-checking`](../data-engineering/completeness-checking.md) — the population count
this rule needs; without it, a check cannot tell an empty scan from a clean one.
[`name-the-blind-spot`](../analytics/name-the-blind-spot.md) — *"treat an exoneration as the
weakest result a check can return."* This is the mechanism behind that advice.
[`a-classification-is-not-a-gate`](../how-we-work/a-classification-is-not-a-gate.md) — the same
species one level up: a declared control that does not exist reads as coverage.

---

## The rule

> **A check must never return its passing value because its subject was absent. Report three
> states — passed, failed, and not examined — and make "not examined" carry the failing exit
> code.**

Every check contains an implicit universal: *for every X, P(X) holds.* A universal over an empty
set is **true**. So the instant the population goes to zero — no credential configured, no file
present, no rows matched, no rules parsed — the check returns the same value it returns for a
subject it examined and approved, and nothing in the output distinguishes them.

This is not a bug in any particular checker. It is the default behaviour of the shape, and it
arrives for free in every language.

## The discriminator: absence of the DEFECT, or absence of the SUBJECT

These look identical in the code and are opposites in meaning. **Getting this backwards produces a
check that fires on correct rows, which is the other way a guard dies.**

| the check asks | an empty population means | passing is |
|---|---|---|
| "does this diff contain a secret?" | no secret in the diff | **correct** — absence of the *defect* is the thing being certified |
| "is the configured credential valid?" | nothing is configured | **wrong** — the *subject* is missing, and nothing was certified |
| "does every rule's declared gate exist?" | no rule declared one | **wrong** — unless the check also says how many rules it read |

The test that separates them, and it is one sentence:

> **Is the passing branch reachable with zero subjects examined — and if it is, does the output
> say so?**

A defect-hunter may pass on an empty population. A property-verifier may not. And **either one may
report a count**, which is why the count is the fix that works for both: a checker that prints
*"0 violations in 0 files"* has not lied, and one that prints *"clean"* has.

## The incidents

### A credential check that passed an agent wired to no credential

A verifier confirmed that an agent's configured credential was present, well-formed and accepted
by the service. Run against an agent whose configuration **named no credential at all**, it
returned success. The loop that validated each configured entry had nothing to iterate, and the
function fell through to its return-true.

The agent was not partly wired. It was not wired. The check that existed to catch exactly that
state reported the same green as a correctly provisioned peer.

### A checker that accepted a regular file where a symlink was required

The requirement was a **relationship**: a path that must be a symlink pointing at a specific
target, so that edits made in one place are visible in the other. The check tested the path.

A regular file at that path satisfies "exists", "is readable", and "has the right name" — and
satisfies **none** of the requirement. The link was the whole point; the file was a copy that would
silently diverge on the first edit. The check was written against the object and the requirement
was about the edge, so the failure mode the requirement existed to prevent was the one state the
check could not see.

**When a requirement is a relationship, a check on the endpoint is not a check.**

### This corpus, measured against its own convention

This repo's reduction pass established that a rule which genuinely cannot be gated carries **no
enforcement clause at all**, on the reasoning that *"the absence is the finding — an empty block
asserting 'nothing here' would be indistinguishable from one nobody has written yet."*

The argument is half right and inverted. Run the corpus's own gate checker:

```
gated: 7   UNGATED: 44   unavailable: 0   UNKNOWN: 30
```

**`unavailable` — the bucket meaning "honestly declares it cannot be gated" — was empty in a corpus
that had already decided six rules were irreducible.** Those six sat in `UNKNOWN` beside 24 rules
nobody had triaged yet, under one undifferentiated reason: *no `## Enforcement` section*. The
convention made a deliberate finding **indistinguishable from an omission**, which is precisely
what it was written to avoid.

**Cost:** six recorded judgements unreadable by the only thing that reads them, and a
worklist 30 long of which 6 were already done. The fix is the one this rule states: the
irreducible verdict is written down as a verdict, and absence goes back to meaning *not yet
examined*.

## Why it survives review

- **It passes.** Nobody investigates a green result, and the green is produced by the same line
  that produces a legitimate green.
- **It is correct code.** There is no exception, no null, no wrong branch. Reading the function
  finds no bug, because the bug is in what the function was asked.
- **It is most likely to fire exactly when it matters.** A subject is absent when something was
  never set up, was removed, or failed earlier — the states a check is for. **The check is
  weakest at the moment it is most needed.**
- **The population is usually invisible.** A checker prints its findings, not its denominator, so
  "0 findings over 0 subjects" and "0 findings over 400 subjects" render identically.

## Guard

- **Size the population before you judge it, and print the size.** *"N examined, M failed"* — never
  a colour, never a bare "clean". This single change makes the failure visible without deciding
  anything else.
- **Three states, minimum**, and the third is not a pass: `passed` · `failed` · `not examined`.
  Give `not examined` the same exit code as `failed`, or worse. Folding it into success is how a
  checker starts lying; folding it into failure at least gets it read.
- **Derive the expected population from a source the scan does not produce.** A count the checker
  computes from its own scan cannot detect that the scan found nothing — see
  [`a-check-that-shares-a-source-is-not-a-check`](a-check-that-shares-a-source-is-not-a-check.md).
- **Write the absence case into the self-test.** Delete the subject, run the check, and assert it
  does **not** pass. This is the cheapest test on this page and it is the one that is never
  written, because the absent case does not feel like a case.
- **When the requirement is a relationship, assert the relationship.** `is_symlink()` and
  `readlink() == target`, not `exists()`. Presence of an endpoint is not presence of an edge.
- **An empty configuration is a finding about the configuration.** Nothing to check is an answer
  about your wiring, and it is the answer nobody ever returns.

## The tell

You are reading a passing result and you cannot say, from the output alone, **how many things it
looked at.** That is the whole diagnosis — and if the answer turns out to be zero, the check has
been reporting on nothing for as long as it has existed.

---

*Earned from:* two checkers found on one day — a credential verifier that passed an agent
configured with no credential, and a link checker that accepted a regular file where a symlink was
the entire requirement — and this corpus's own irreducible convention, which recorded six
deliberate "cannot be gated" judgements as an absence its own checker could not tell from the 24
rules nobody had looked at.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: deferred
observable: 'for each checker in the repo: whether its passing branch is reachable with an empty population, whether it prints the size of the population it examined, and whether its self-test contains a case that removes the subject and asserts a non-pass'
trigger: 'pre-commit on checker paths, plus CI over the checker suite'
check: 'AST: a function returning a pass value from a path where the iterated population is empty, with no separate not-examined state -> block; a checker whose output carries no examined-count -> block; a checker whose tests contain no subject-absent case -> block'
escape: 'a defect-hunter whose correct answer on an empty population IS pass - declare it (a marker naming the population as the defect set, not the subject set), and it still owes the examined-count'
narrows: 'gates the shape, not the semantics - whether a given population is the defect set or the subject set is a judgement the marker records rather than proves. And no lint can tell that a check asserted the wrong property (existence where a symlink was required); only the subject-absent self-test catches that, and the gate can compel the test to exist, not to be correct'
```
