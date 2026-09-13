---
name: ship-a-rule
description: Ship a rule or a skill with its gate decided, named and watched refusing. Use when adding or editing a rule, adding a skill, assigning or changing an enforcement verdict, or when a rule is about to be published without one.
---

# Ship a rule

**A rule is finished when its enforcement is decided — not when its prose is good.** This skill
exists because a corpus of 86 rules once reported 9 as gated while **nothing in the repo invoked any
of them**, and one of the nine named a prose checklist as its implementation.

Run it for a new rule, an edited rule, a new skill, or any change to a `verdict:`.

## 1. Check it does not already exist

Grep the corpus for the claim, not the wording. **Name the command you ran.** If a rule already
covers it, strengthen that one — a second rule beside an existing one drifts, and the drift is
silent.

**Completion criterion:** you can name the search and the nearest existing rule, and say why it is
not this.

## 2. Name the incident and what it cost

No incident, no rule. A rule from an instruction rather than a failure is allowed and says so.

**Completion criterion:** the write-up names what broke, the cost, and how it was caught.

## 3. Assign a verdict — three values, and a blank is not one of them

| state | how it is written | what it owes |
|---|---|---|
| **gateable** — `interposed` / `deferred` / `narrowed` | a `verdict:` in the clause | everything in steps 4–6 |
| **irreducible** — or `structural`, where the capability itself is removed | a `verdict:` in the clause | a `reason:`, and a `weaker:` instrument that still applies |
| **not yet examined** | **no clause at all** | nothing — but it is counted, and it is not clean |

**Take the vocabulary from the checker, never from memory.** The five accepted values live in
`skills/check-rule-gates/check_rule_gates.py`, and that file is the authority: a verdict it does not
know is reported `UNKNOWN`, not assumed gateable. **Do not invent a sixth spelling.** Two
vocabularies for one field is the drift this step exists to prevent, and `structural` is the one
most often left out of a list written from recollection — it is rare, it is real, and the corpus
defines it.

**An absent clause means *not yet examined*, and that is the only way to say it.** It has never
meant irreducible — that convention was tried here and failed, because a deliberate judgement became
indistinguishable from an omission. There is no `verdict: not-yet-examined`: the absence already
carries it without ambiguity now that irreducible is declared, and a third spelling would put two
ways of saying one thing into a field a machine reads.

**Choosing `irreducible` must stay cheap.** A process that makes it expensive produces invented
gates, which are worse than recorded debt: debt is counted, a fake gate reports green. If the honest
answer is that it does not reduce, take it and move on.

## 4. If it is gateable, specify the gate — six fields, none optional

`observable` · `trigger` · `check` · `escape` · the **false-positive shape** · and `narrows:` if the
gate is smaller than the rule.

**The trigger is the moment the rule names**, not the moment that is convenient. A control that
catches "do not start X without Y" at commit time does not prevent the work, it prevents the work
from landing, after it is paid for. If the trigger is later than the rule's moment, say
`fires_late: true`.

**Completion criterion:** someone else could build it from the clause alone.

## 5. Name what INVOKES it, not only what implements it

**These are two claims and the second is the one that gets skipped.**

- `implemented_by:` — the thing that exists and **can refuse**.
- `invoked_by:` — what **causes it to run**: a pre-commit hook, a CI step, a `PreToolUse` hook.

A checker that exists, is correct, and is wired to nothing is not a control — and it reports exactly
as green as one that is. If nothing invokes it yet, **write that as the value**. An honest
`invoked_by: nothing` is a countable gap; an absent field is a silent one.

**A skill that is prose is `assisted_by:`, never `implemented_by:`.** It cannot refuse, however
faithfully it is followed.

**Completion criterion:** both fields have values, and the `invoked_by` value names a real
invocation point or says plainly that there is none.

## 6. Verify by watching it REFUSE

**A gate observed only allowing good input is unproven.** It is not a gate yet; it is a function
nobody has asked a hard question.

1. Feed it a known violation. **Watch it refuse.** Record the command and the refusal text.
2. Feed it a known-good case. **Watch it allow.** A gate that refuses everything is discovered by
   being switched off.
3. **If the gate has more than one arm, disable each arm separately.** A case that still fails when
   you remove the arm you believe covers it is covered by accident, and the next tidy-up of an
   unrelated pattern will uncover it silently.
4. **Read the exit code, unpiped.** A pipeline reports the status of its last command and the gate
   is never the last command.

> ⚠️ **The one exception:** a control whose only direct test is performing the act it prevents is
> not tested that way. Test the predicate as data, substitute a decoy, have it answered from outside
> a session, or record it unverified **with the reason** — never "probably fine".

**Completion criterion:** you can quote the refusal. Not "the tests pass".

## 7. If the gate cannot ship in this change, record the debt with a count

Say it plainly, with a number: *"N rules classified, M gated."* **Do not ship the clause and the
intention together** — the clause reads as coverage to the next person, who then stops enforcing it
by hand and is replaced by nothing.

## 8. Reuse the corpus's own parser — never write a second one

If you are building a check **over these clauses**, import the vocabulary and the path resolver
from `check_rule_gates.py`. Do not restate them.

`implemented_by` values are not all single clean paths — some name two files, some carry a trailing
phrase — and the existing resolver has deliberate tokenising logic for that, arrived at once. **A
second parser of one field agrees with the first on the day it is written and drifts silently
afterwards**, and the first symptom is a gate refusing a clause its sibling checker accepts.

## 9. Update the index and run the corpus checks

The rule table, the counts, and every check the repo ships — read their exit codes.

**Completion criterion:** the counts in the index were re-measured, not edited to match.

## The failure this skill is written against

Every step above was earned the same way: a green report over an unbuilt control.

- a classification treated as an implementation — **86 rules, 9 reported gated**
- an implementation treated as an invocation — **and 0 of those 9 invoked by anything**
- a prose checklist treated as an implementation
- a blank treated as a decision
- a gate reported working because it passed
- an exit code discarded by a pipe

**None of these were carelessness.** Each was a defensible judgement that stopped one step early,
and each produced a number that was true and meant something other than what it looked like.
