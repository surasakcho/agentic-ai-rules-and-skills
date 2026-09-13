# An additive change is not additive — a new member re-specifies every old one

**Task type:** coding — adding a value to any output vocabulary: a status string, a severity, a
colour, an enum, a label a reader acts on.
**Related:**
[`known-blast-radius-demands-scoped-fix-everywhere`](../how-we-work/known-blast-radius-demands-scoped-fix-everywhere.md)
— a *capability* owed to every sibling once it exists for one. This is the inverse: a *meaning*
taken from every sibling the moment one gains it.
[`absence-is-not-compliance`](../testing/absence-is-not-compliance.md) — "three states, not two" is
the fix this rule is the cost of. Splitting a value is right, and it re-specifies what the old
values meant.
[`a-correction-lands-where-you-noticed-it`](../how-we-work/a-correction-lands-where-you-noticed-it.md)
— the sweep for a wrong claim's other homes. Here nothing is wrong yet; the other homes became
wrong without being touched.
[`validations-must-fail`](../testing/validations-must-fail.md) — an unexercised branch is where
this hides, and its boundary on decoys is how you reach one.

---

## The rule

> **When you add a member to a vocabulary, every existing member is narrowed by it. The old callers
> keep their spelling and lose their meaning — and nothing changed at the sites that are now
> wrong.**

The trap is in the framing. **The change reads as purely additive**, which is exactly why nobody
re-reads the old sites: adding a value feels like it cannot break a value that already existed.

## The discriminator

**The question is not "did I use the new member correctly". It is "which existing members did I just
narrow".**

**Enumerate the old callers, not the new ones.** In every instance below the defect sits at a site
that was never edited — so it is invisible in the diff, invisible to a reviewer reading the change,
and invisible to a test suite that was passing before and still is.

## Three instances

> **A severity that gained a meaning.** Amber had been "a softer red" and promised nothing. A
> genuine amber class was added and its meaning written down: *real, printed in full, and not
> something an `up` makes worse.* **That sentence retroactively specified every amber line already
> in the file** — including one that sets the failure count and is the reason the run exits
> non-zero. A blocker went on printing in the not-a-blocker colour, and **the reader now skips it
> because of the change that was meant to help them.** Two callers updated, three left.

> **A label that was true until a source was added.** A checker printed the literal string `a hook`
> for every invoked row. True while hooks were the only invoker; **a lie the moment cron was added**
> — and nothing at the printing site changed. The lesson was written into that file's own comment
> and never carried to the next instance, which is the case for a rule rather than a comment.

> **A count that changed meaning under its own author.** A gate checker gained `bound`, then
> `deliberately unbound`. `UNGATED` silently acquired a second sense — *no in-corpus
> implementation*, **or** *the estate's binding failed to resolve* — and `gates no rule names` went
> from *no rule claims it* to *no rule claims it and nobody declared it deliberate*. **Every
> measurement recorded before those commits is now in a different vocabulary**, which is why "a
> printed label is a fact about transcripts" had to be ruled on hours later. The re-specification
> came first; the transcript problem is its bill.

## Where it hides, and how it was found

**In the branch nobody runs.** An unexercised path cannot notice that the vocabulary around it
moved — it has no occasion to. The amber defect was found by **executing** the one branch in that
file that never ran, which had been recorded as unexercised on the grounds that provoking it meant
touching a real credential. It did not: **an empty decoy file at the same path, fired, removed in
the same command.** The boundary in `validations-must-fail` exists for exactly that, and it is the
difference between a branch nobody has run and a branch nobody can run.

**This is a distinct question from "can this check fail".** It is *does this check still mean what
it meant, when nothing about it changed.*

## Guard

- **List every existing caller of the vocabulary before you add to it**, and re-read each one against
  the new definition. If the list is long, that is the cost of the change, not a reason to skip it.
- **Expect the defect in a file your diff does not touch.** Review of the change cannot find it;
  only the enumeration can.
- **Writing the new member's meaning down is the moment of re-specification.** Until amber promised
  something, no amber line was making a claim. The documentation is not the safe half.
- **Never compare a reading taken before the change with one taken after** without saying the
  vocabulary moved. Same word, different set.
- **Run the unexercised branches first.** They are where a silently-narrowed meaning survives
  longest, and a decoy usually reaches them.

---

*Earned from:* a severity vocabulary that gained a documented amber class and left a failure-setting
line printing in the not-a-blocker colour, with two of five callers updated; a checker printing
`a hook` for every invoked row, true until cron was added and recorded in a comment nobody
generalised; and a gate checker whose `UNGATED` and orphan counts changed meaning under their own
author on the same day, making every earlier recorded measurement a reading in a vocabulary that no
longer exists.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'a diff that adds a member to an enumerated output vocabulary - a status/severity constant list, an enum, a set of label strings - together with the set of call sites that emit any OTHER member of that same vocabulary and are unchanged in the diff'
trigger: 'pre-commit on the diff, at the moment the member is added'
check: 'a new member added to a declared vocabulary and one or more existing emitters untouched -> block, LISTING the untouched emitters so the enumeration is done rather than promised; a vocabulary whose members are not declared in one place -> advise, since nothing can enumerate it'
escape: 'confirm each listed emitter was re-read against the new definition - the guard asks for the enumeration, never for a particular outcome, because narrowing an old member is often correct'
narrows: 'lists the sites; cannot judge which are now wrong, which is the judgement the rule exists to force. Blind to a vocabulary spread across files with no single declaration, and blind to one whose members are constructed rather than named - both of which are the shape most likely to have the defect'
```
