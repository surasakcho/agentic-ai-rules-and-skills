# A classification is not a gate — a rule that can be gated ships with its gate

**Task type:** agent workflow — writing, publishing or reviewing a rule in this repo.
**Related:**
[`a-gate-that-fires-at-commit-time-is-not-a-gate`](../coding/a-gate-that-fires-at-commit-time-is-not-a-gate.md)
gives the ladder and the firing moment; this rule says the ladder is **mandatory**, not a
ranking to admire.
[`a-correction-is-not-a-control`](a-correction-is-not-a-control.md) — a control has an
off-switch; if nothing has ever thrown it, it is commentary.
[`validations-must-fail`](../testing/validations-must-fail.md) — the discharge condition: a
check you have never seen fail is untested.
[`publish-lessons-weekly`](publish-lessons-weekly.md) — *"mechanise what can fail"* is step 3 of
the weekly pass; this is what "can" obliges.

---

## The rule

> **Never declare a rule gateable and leave it ungated. Classifying a rule as mechanisable
> creates an obligation, and the obligation is discharged only by a gate that has been proven to
> REFUSE.**

`prose < checklist < test < gate` is a ladder, and a rung is not a plan. A rule carrying
`verdict: interposed` with no gate actually deployed is an **unfinished rule** — and it is worse
than one that honestly declares it does not reduce, because **the clause reads as coverage that
does not exist.**

## A declared gate that does not exist is worse than no gate at all

The failure is not that the control is missing. It is that the control is **documented**.

- A rule with no enforcement clause is read as prose, and prose is trusted the way prose is
  trusted — weakly, by a reader who knows they are the only thing enforcing it.
- A rule whose clause names an observable, a trigger and a check is read as *handled*. The
  reader stops enforcing it by hand, and nothing replaces them.

That is the same shape as a health signal not attached to what it reports: the honest answer to
*"what would this be showing if the thing were already broken?"* is **green**. A classification
block is a status field, and per
[`status-fields-must-be-earned`](../data-engineering/status-fields-must-be-earned.md) a status
set from intent rather than outcome is not a status.

## Proven to refuse — the discharge condition

**A gate only ever observed allowing good input is unproven.** It is not a gate yet; it is a
function that has never been asked a hard question.

This corpus already knows the specific trap: **a check that passes on the first try, in a
situation that should have failed, is evidence of nothing.** Run the gate against input you know
violates the rule and watch it refuse. Both directions — one case that must fire, one that must
not — or the gate discriminates nothing and will fire on everything until someone routes around
it.

So the obligation is discharged by three things, not one:

1. the gate **exists** and runs where the rule's moment is,
2. it has been **observed refusing** a real violation,
3. the rule's clause **names it** — `implemented_by:` pointing at the thing that runs.

Without the third, the rule and its enforcement drift apart, which is the failure the clause
format exists to prevent.

## The gate ships with the rule, not later

A rule published ahead of its gate has **no forcing function to ever get one.** Nothing in the
repo knows the gate is owed; the clause already describes it; the next reader sees a
documented control. "We'll build the gate next pass" is the deferred-cleanup failure applied to
enforcement — the step is skippable, and it gets skipped at exactly the moment the rule stops
feeling new.

If the gate cannot ship in the same change as the rule, the rule is not finished. Say that
plainly, with a count, rather than shipping the clause and the intention together.

## Where a gate genuinely cannot be built, record that instead

**Honest "this does not reduce" is fine. Unimplemented "interposed" is not.**

The vocabulary for that verdict in this corpus is **`irreducible`**, and the convention is
deliberate: *an irreducible rule carries no `## Enforcement` clause at all, and its reason is
recorded in [`docs/gateability.md`](../../docs/gateability.md)'s irreducibles table.* The absence
is the finding — an empty block asserting "nothing here" is indistinguishable from one nobody has
written yet.

So there are exactly two acceptable end states for a rule, and no third:

| End state | What it looks like |
|---|---|
| **Gated** | a clause naming a gate that exists, has been seen refusing, and is pointed at by `implemented_by` |
| **Irreducible** | no clause, and a reason written down where the reasons live |

"Classified, gate pending" is not an end state. It is the state this rule exists to end.

## This rule applies to itself — and it arrives in debt

It is checkable by exactly the means it demands: read every rule's enforcement clause, assert the
declared gate exists, and assert it has been seen firing. That check is a few lines over this
repo, and it is named in the clause below.

**The honest state at the time of writing, measured rather than estimated:** 80 rule files, of
which **50 carry an enforcement clause** and **7 name an implementation that actually runs**. A
prior reduction pass found **50 of 56** rules in two categories mechanisable. So the obligation
this rule creates is not a handful — the gap between "classified" and "running" is currently
**43 rules**, and this rule is the first thing its own check would refuse.

Naming that is the point. A rule that quietly exempts itself while demanding the gate from
everyone else is the decoration it is written against.

## Guard

- **When you classify a rule as gateable, build the gate in the same change.** If you cannot,
  the rule is unfinished — record the debt with a count, do not ship the clause alone.
- **Never report a gate as working on the strength of it passing.** Feed it a known violation and
  watch it refuse, or it is untested.
- **Point the clause at the thing that runs.** `implemented_by:` is what keeps the rule and its
  enforcement from drifting.
- **Prefer an honest `irreducible` to an aspirational verdict.** Downgrading a classification you
  cannot implement is a correction; leaving it in place is a false status.
- **Count the gap rather than describing it.** "Most rules are enforced" is the claim that rots;
  a number derived from the clauses themselves cannot.

---

*Earned from:* a direct instruction, 2026-09-12 — *"when a rule can have a gate, set the gate
up"* — with no failure of its own yet, consistent with
[`phrase-narrow-rules-as-prohibitions`](phrase-narrow-rules-as-prohibitions.md) and
[`sanity-check-test-cases`](../coding/sanity-check-test-cases.md), which were also added on
instruction rather than extracted from an incident. The measurement behind it is this corpus: a
reduction pass classified 50 of 56 rules as mechanisable, 50 rule files now carry an enforcement
clause, and 7 name a gate that runs.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: deferred
observable: 'every Enforcement clause in this repo, against whether the gate it declares exists and has been observed refusing a known violation'
trigger: 'check exit code over this repo, at the moment a rule lands'
check: 'clause present and verdict is not irreducible and implemented_by absent -> fail; implemented_by names a path that does not exist -> fail; report the count of clauses backed by a running gate, never a colour'
escape: 'a rule that genuinely does not reduce carries no clause at all and its reason goes in docs/gateability.md - absence is the finding, an empty block is not'
note: 'commit time IS the moment this rule names - a rule lands at commit - so this is not fires_late. The check is specified and not yet implemented; 50 clauses exist and 7 name a running gate, so this rule is the first thing its own check would refuse, and that debt is stated in the rule rather than hidden by it'
```
