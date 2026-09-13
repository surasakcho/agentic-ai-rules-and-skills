# What the test harness supplies, the harness cannot test — and the mode is the usual casualty

**Task type:** testing — any suite whose subject is a script, a binary, a hook, or anything a
caller *starts* rather than imports.
**Related:**
[`a-check-that-shares-a-source-is-not-a-check`](a-check-that-shares-a-source-is-not-a-check.md) —
the closest in shape, and a different object: that one is about a shared **source** for the
expectation, this one about a shared **invocation** with the caller.
[`a-fix-that-cannot-reach-the-artifact-is-not-a-fix`](../coding/a-fix-that-cannot-reach-the-artifact-is-not-a-fix.md)
— there the remediation never reaches the defective state; here the artifact is present, correct,
and cannot be started.
[`validations-must-fail`](validations-must-fail.md) — corollary 4 asks which branch passed a case.
This asks a prior question: **which invocation was the case about?**
[`absence-is-not-compliance`](absence-is-not-compliance.md) — the suite is green over a population
of one invocation, and nothing says which one.

---

## The rule

> **A test supplies the interpreter, the working directory and the environment — so every one of
> those is a part of the interface the suite substitutes for rather than exercises. Its green is
> evidence about the invocation the harness chose, and callers use a different one.**

The usual casualty is the **file mode**. A suite runs `python3 tool.py` or `bash tool.sh` or
imports the module; a caller runs `./tool.py`. **The execute bit is invisible to the suite by
construction**, which is not the same as under-tested — it is untestable from inside the one thing
that would have noticed.

## Two incidents, two repositories, the same silence

> **A test suite that could not be run.** Eight suites in one `bin/`; seven printed a tally and one
> printed nothing and returned **126**. It was committed `100644`. Run as `python3 <file>` it passed
> **24 of 24, and always had.** The suite was never broken — it was unrunnable by the invocation its
> seven siblings all use, and nothing reported that.

> **Three scripts shipped `100644`.** A standby loop failed `Permission denied` **every cycle for
> about a day**, invisibly, until somebody looked. Already cited in this corpus as an example; it
> was never the subject of a rule.

**The tell is identical in both: a green suite, and a caller getting exit 126 or `Permission
denied`, with nothing joining the two.** No test fails. No output is wrong. The artifact is correct.

## Why this is not "remember to chmod"

Because the failure is structural, and advice aimed at memory does not touch it:

- **The suite is not wrong.** It tests the code, correctly, and the code is fine.
- **The suite cannot be extended to catch it.** Adding a case that runs the file directly tests the
  *checkout you have*, not the mode recorded in the index — and the mode in the index is what ships.
- **Everything the harness supplies is in the same blind spot**, not just the mode: a shebang naming
  an interpreter that is not on the caller's PATH, a CRLF line ending that makes the shebang
  unparseable, an assumed working directory, an environment variable the harness exports and the
  caller does not. Each is a property the suite *provides* instead of *verifying*.

**So the question to ask of any suite whose subject is startable is: what does my harness hand this
thing that a caller would not?** That list is the untested surface, and it is knowable in advance.

## Where it is checkable

**The mode is a fact about the git index, so commit time is the moment the rule names — not late.**
The predicate is two commands: a tracked file whose first bytes are `#!` and whose index mode is
`100644`. `git ls-files -s` reports the mode; the shebang reports the intent. Disagreement is the
finding.

**Read the index mode against the checkout's bytes — that pair, specifically.** A file can be
`100644` in the index and `755` in somebody's working copy, and **only the first one ships**. So the
check is `git ls-files -s` for the mode and the first two bytes of the file for the intent; a sweep
that stats the checkout passes on every machine where someone once ran `chmod` and never committed
it.

**A file that is sourced or imported rather than executed is a legitimate `100644` and says so in
itself** — *"sourced, never executed"* in the header, or a documented `python3 <file>` interface. A
sweep of one tree found ten shebang files not `100755`: **one real defect and six honest
non-findings of exactly that kind**, plus three symlinks. The escape is not a suppression list; it
is a sentence in the file, which the next reader also needs.

## Run against the corpus that published it: 17 of 34

**First run of this rule's own check, on this repository, at the moment the rule landed:** 34
tracked shebang files, **17 of them `100644`** — every checker and self-test it ships.

**That is not seventeen defects, and the distinction is the rule's own escape clause doing real
work.** This corpus documents its tools with an interpreter in front of them — `python -X utf8
skills/lesson-review/harvest.py --check` is the invocation in the README, and the skills' own docs
match. So the interface genuinely is interpreter-prefixed and `100644` is genuinely right for most
of them.

**But not one of the seventeen says so in itself**, which is the half that is owed. Nothing in
`harvest.py` states that it is not meant to be started directly, so the next reader cannot tell a
deliberate `100644` from the defect that cost two repositories a day of silence. **A sweep whose
hits all need a human to remember which were intended is a sweep nobody will run twice.**

**Recorded as a count rather than fixed by a bulk `chmod`**, because flipping seventeen modes would
assert an executable interface for files whose documented interface is not executable — the
reflexive repair, and the wrong one. The work owed is a line per file, and it is
[`a-classification-is-not-a-gate`](../how-we-work/a-classification-is-not-a-gate.md) debt stated
with its number rather than hidden.

### And some files cannot declare it, which is a third state and not an omission

A file that is **denied to the session that would annotate it** cannot carry its own sentence. In
one estate, two of the four undeclared files were the gate dispatcher and its installer — **on that
session's edit deny list, because a control the controlled party can edit is not a control.** The
machinery was refusing edits to itself, correctly, and the declaration it owes is a casualty of that
working.

**The answer is to put the declaration where it can be written and say whose it is** — in that case,
the header of the adjacent test file, naming both. **Two of four undeclared for a refusal rather
than an omission is a legible state; two silently missing is not**, and the difference is one
sentence in a file nobody is denied.

## Guard

- **Name the invocation your suite uses and the one your callers use, and say whether they are the
  same.** If the suite supplies an interpreter, the mode is untested — write that down rather than
  inferring coverage from green.
- **Check the mode in the index, not in your checkout.** A local `chmod` that is never committed
  passes every local run and ships nothing.
- **Treat exit 126 and `Permission denied` as interface defects, not environment noise.** Both
  incidents survived because the symptom looked like somebody's machine.
- **Declare the non-executable ones in the file.** `100644` on a shebang file is fine and must say
  why; the sweep is worthless if every hit needs a human to remember which are deliberate.

---

*Earned from:* a test suite committed `100644` that printed nothing and returned 126 while passing
24 of 24 under the interpreter its own siblings were run with, and — in a different repository, and
already cited in this corpus as an example rather than as a rule — three scripts shipped `100644`
whose standby loop failed `Permission denied` every cycle for about a day, invisibly.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: deferred
observable: 'every tracked file whose first bytes are a shebang, against its mode in the git index'
trigger: 'pre-commit, or CI over the tree -- the mode is a fact about the index, so commit time IS the moment this rule names and it is not fires_late'
check: 'git ls-files -s for the INDEX mode, and the first two bytes of the path for the shebang -- that pair, since a file can be 100644 in the index and 755 in a working copy and only the index ships. Mode 100644 with a shebang and no declared non-executable interface -> block, naming the file; report the count of shebang files checked, never a colour'
escape: 'a file that is sourced or imported rather than executed declares so in its own header, and a file DENIED to the session that would annotate it has that declaration written in an adjacent file naming both -- undeclared-for-a-refusal is a state, not a gap -- sourced, never executed, or a documented interpreter-prefixed interface. A suppression list outside the file is not an escape, because the next reader needs the reason more than the checker does'
invoked_by: 'nothing yet. In the estate that reported this, the pre-commit hook is a fixed sequence of numbered gates with no extension point AND is on the reporting session deny list, so the rule classifies as gateable and stays ungated there -- the debt a-classification-is-not-a-gate names, recorded rather than hidden'
narrows: 'gates the MODE, which is one member of the blind spot the rule describes. A shebang naming an interpreter absent from the caller PATH, a CRLF that makes the shebang unparseable, an assumed working directory, an environment variable the harness exports -- each is supplied by the harness in the same way and none is visible to this check'
```
