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
3. the rule's clause **names it** — `implemented_by:` pointing at the thing that can refuse, and
   `invoked_by:` pointing at what causes it to run. **Those are two claims and the second is the
   one that gets skipped**: a checker that exists, is correct, and is wired to nothing is not a
   control, and it reports exactly as green as one that is. A skill that is prose cannot satisfy
   either — it cannot refuse, so it is `assisted_by:`, never `implemented_by:`.

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

The vocabulary for that verdict in this corpus is **`irreducible`**, and it is **written down as
a verdict**: the rule carries an `## Enforcement` clause reading `verdict: irreducible`, with a
`reason:` and the `weaker:` instrument that still covers part of the ground. The reasons are
collected in [`docs/gateability.md`](../../docs/gateability.md)'s irreducibles table.

> ⛔ **CORRECTION, 2026-09-13 — this section previously said the opposite**, that an irreducible
> rule carries *no* clause at all, on the reasoning that "the absence is the finding — an empty
> block asserting 'nothing here' is indistinguishable from one nobody has written yet."
>
> The second half of that sentence is true and the conclusion inverts it. **An absence is
> indistinguishable from an omission in the other direction too**, and that is the direction this
> corpus actually failed in: the checker below reported `unavailable: 0` while six rules had
> already been judged irreducible, and all six sat in `UNKNOWN` beside 24 rules nobody had triaged,
> under one undifferentiated reason — *no `## Enforcement` section*. A deliberate finding that
> cannot be told from an omission is not a finding. See
> [`absence-is-not-compliance`](../testing/absence-is-not-compliance.md), the rule this was the
> third incident for.
>
> **A clause saying `irreducible` is not an empty block asserting "nothing here".** It is a
> judgement, with a reason, that a machine can count — which is what makes an absence mean *not
> yet examined* again.

So there are exactly two acceptable end states for a rule, and no third:

| End state | What it looks like |
|---|---|
| **Gated** | a clause naming a gate that exists, has been seen refusing, and is pointed at by `implemented_by` |
| **Irreducible** | a clause reading `verdict: irreducible`, carrying its `reason:` and the `weaker:` instrument that still applies |

"Classified, gate pending" is not an end state. It is the state this rule exists to end.

## This rule applies to itself — and it arrives in debt

It is checkable by exactly the means it demands: read every rule's enforcement clause, assert the
declared gate exists, and assert it has been seen firing. That check is a few lines over this
repo, and it is named in the clause below.

**The honest state, measured rather than estimated.** At the time of writing, 2026-09-12: 80 rule
files, of which 50 carried an enforcement clause and 7 named an implementation that actually runs.
**Re-measured 2026-09-13**, after the four remaining categories were triaged and the irreducible
convention was corrected — `check_rule_gates.py` over 83 rule files:

```
gated: 8   UNGATED: 68   unavailable: 7   UNKNOWN: 0
```

So the obligation this rule creates is not a handful — the gap between "classified" and "running"
is **68 rules**, and this rule is the first thing its own check would refuse. The number went *up*
because the triage was finished, which is the correct direction: an unread corpus was never a clean
one.

Naming that is the point. A rule that quietly exempts itself while demanding the gate from
everyone else is the decoration it is written against.

## The debt is honest only while something reports it — and that is one pipe away

68 rules currently declare a gate that does not exist. What stops that from reading as coverage
is a single non-zero exit code, and **a non-zero exit code is the most fragile signal in a shell.**

Observed twice on 2026-09-13, by two readers independently, within minutes of each other:

```sh
$ check_rule_gates.py                 # exit 1  -- correct
$ check_rule_gates.py | tail -40      # exit 0  -- while the output says FAILED
$ set -o pipefail; … | tail -40       # exit 1  -- correct again
```

A pipeline reports the exit status of its **last** command, and the gate is never the last
command — `tail`, `head`, `grep`, `tee` and a `| cat` for paging all succeed unconditionally. So
the checker printed `RULE GATES FAILED` and the shell said everything was fine, in the same
breath, to someone who was reading the failure text at the time.

**Nothing was wrong with the checker.** Its exit codes are correct, deliberate and documented.
The signal was discarded one layer out, by a habit — piping a long report through `tail` — that
nobody would think of as a change to a control.

The general shape is already a rule:
[`silence-must-be-the-alarm`](silence-must-be-the-alarm.md), whose observable names *unchecked
pipelines* and whose check now carries the predicate. Recorded here because this is the rule with
something to lose: **every "classified" verdict in this corpus is backed by that one integer.**

- **Run a gate unpiped, or set `pipefail`, or read `PIPESTATUS`.** In CI, never pipe a gate into a
  formatter.
- **A gate whose failure has only ever been read as text has not been observed refusing.** The
  discharge condition above is about the exit code, not the message.

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
check: 'clause present and verdict is not irreducible and implemented_by absent -> fail; implemented_by names a path that does not exist -> fail; report the count of clauses backed by a running gate, never a colour; and the caller reads the exit code unpiped, or under pipefail, or via PIPESTATUS - a gate piped into tail or grep reports the exit status of tail'
assisted_by: 'skills/ship-a-rule/ - the authoring checklist. Prose: it cannot refuse, and it is not this clause implementation'
escape: 'a rule that genuinely does not reduce declares verdict: irreducible with its reason and its weaker instrument, and is counted as unavailable rather than owed. Absence of a clause means NOT YET EXAMINED and is reported as UNKNOWN, never as clean'
note: 'commit time IS the moment this rule names - a rule lands at commit - so this is not fires_late. The check is specified and not yet implemented; 50 clauses exist and 7 name a running gate, so this rule is the first thing its own check would refuse, and that debt is stated in the rule rather than hidden by it'
```
