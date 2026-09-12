# A fix that cannot reach the artifact is not a fix

**Task type:** coding — shipping any remediation: a migration, a backfill, a seed, a corrected
message, a guard over existing state.
**Related:** [`discriminate-by-executing-not-inspecting`](../how-we-work/discriminate-by-executing-not-inspecting.md)
— the nearest neighbour, and the difference matters: that rule is about a CHECK that reads
something adjacent to the thing. This one is about a FIX whose coverage structurally excludes the
population it was written for. Both produce green.
[`known-blast-radius-demands-scoped-fix-everywhere`](../how-we-work/known-blast-radius-demands-scoped-fix-everywhere.md)
— once the affected set is enumerated, the fix is owed to all of it.
[`a-correction-is-not-a-control`](../how-we-work/a-correction-is-not-a-control.md) — a correction
the object absorbs and survives.

---

## The rule

> **Name the artifact the fix has to reach — the page, the row, the running database — and verify
> THAT. Not the function, not the test, not the build.** A remediation whose coverage excludes the
> state that has the defect has not fixed anything, and it reports success the whole time.

## The incident

**Seven instances in one day, in one application, all the same shape.** Every one: tests passed,
deploy succeeded, defect still visible.

| the fix | why it could not land |
|---|---|
| a unique index closing a credit-minting hole | `CREATE UNIQUE INDEX` **raises** on a database that already holds duplicates — precisely the databases the bug had polluted. It applied everywhere except where it was needed |
| an upload rejection message | the reason was written to a request-scoped attribute and **read by nothing**. A user who attached a screenshot was told to attach a screenshot |
| a pluralisation fix in the demo seed | the text is **stored**, and the seed does not top up an existing database. Correct code, green tests, successful rebuild, bug still on screen |

**Then it happened twice more inside the fix for it.** A guard written to make a destructive
rebuild safe asked about **names** while the thing it deleted was **rows** — a name is a guess
about a row's origin, not a fact about it, and a genuine review written under a seeded login was
deleted while the guard reported everything fine. And the stamping mechanism built to prevent
exactly that **could not reach the one database it existed for**, because that database was
created before the stamp existed and so took the never-touch branch forever.

**And once in the instrument.** The test for the first instance ran the migration with foreign
keys OFF while production runs them ON, against a fixture inventing rows whose parents did not
exist. Green for weeks, about a database the engine would never have allowed the app to create.

## Why it is easy to get wrong

**Every one of these is correct code.** The function returns the right string; the migration is
valid SQL; the seed produces good text. Nothing is wrong with the change — the change simply
cannot arrive where the damage is.

**The common tell: the check and the artifact were different objects.** A test proving a function
returns the right string says nothing about whether anyone renders it. A migration that applies to
a fresh database says nothing about the one in production. A seed that produces good text says
nothing about text written last week.

**First deployments are usually outside the coverage of anything that manages existing state.**
The oldest data is the data that predates the mechanism, and it is also the data that has the
defect.

## Guard

- **Write down the artifact before writing the fix.** If you cannot name the row, page or file
  that must change, you cannot tell whether it did.
- **Verify against the affected population, not a fresh one.** A migration is tested on a database
  that already holds the bad rows; a seed on a database that already holds the bad text.
- **When you ship a mechanism that manages existing state, ask immediately whether the existing
  state is inside its coverage.** It usually is not, and that gap is silent.
- **A check about origin must read a fact the row carries**, never a property of something
  adjacent to it.
- **A test is an artifact too.** Ask what conditions the running system has that the test does not
  — pragmas, connection settings, constraint enforcement. They are configured somewhere the test
  never reads.

---

*Earned from:* seven instances in a single day in one application, five in the app, one in the
mechanism written to prevent them, and one in the test that was green for weeks about a database
that could not exist. Every one passed its own check.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'a test environment disabling a constraint production enables (foreign keys off, relaxed pragmas), and a migration or backfill with no test seeded from the defective population'
trigger: 'pre-commit or CI'
check: 'a test disables a constraint that production enables -> block; a migration with no polluted-state fixture -> block'
escape: 'a fixture that legitimately needs the constraint off declares it per file'
narrows: 'catches the check-and-artifact-are-different-objects shape; cannot verify the fix reached the running row'
fires_late: true
```
