# When two inventories describe one territory, count the join — each is complete on its own terms

**Task type:** how we work — coverage, compliance, monitoring, any claim of the form "we have N of
these" where a second list describes the same ground from the other end.
**Related:**
[`a-classification-is-not-a-gate`](a-classification-is-not-a-gate.md) — one list with a missing
referent. This is two lists that never meet.
[`completeness-checking`](../data-engineering/completeness-checking.md) — *check both directions* —
the same instruction for a data pipeline. This is that discipline applied to two registries nobody
thinks of as data.
[`exact-match-on-a-complete-key`](../data-engineering/exact-match-on-a-complete-key.md) — a join
that runs and drops its misses. Here the join is never run at all.
[`status-fields-must-be-earned`](../data-engineering/status-fields-must-be-earned.md) — *an
unqueried hash is decoration*, which is what happens to the join when it is computed and kept out
of the headline.

---

## The rule

> **When two independently-maintained lists describe the same territory from opposite ends, the only
> number that means anything is the JOIN — matched, left-only, right-only. Each list is complete by
> its own definition, so each side reports green while the overlap is empty, and neither owner is
> positioned to notice.**

## Why both sides report green

This is not two people being careless with one list. It is two lists, each correct:

- The **left** list says what is required. It is complete — every requirement is on it.
- The **right** list says what exists. It is complete — everything that exists is on it.
- **Neither says anything about the other**, and the question everybody actually has —
  *is the required thing the thing that exists?* — lives only in a join that has no owner.

So the failure has a distinctive signature: **nobody is wrong, no number is false, and the
conclusion everyone draws is untrue.** Asking either owner to check harder produces a better version
of the same list.

## Three instances, one estate, one day

| left list | right list | matched |
|---|---|---|
| rules declaring `implemented_by` — the gate exists | gates something actually **invokes** | **8 declared, 0 invoked** |
| repos declaring a session name | sessions actually **registered** under one | **12 declarations, 10 registrations, 0 matches** |
| rules naming a gate | gates the estate actually **runs** | **74 rules name gates nobody built; every gate that exists is named by no rule** |

The third is the clearest. The corpus's gate inventory resolves all eight of its gated rules into
its own repository and **not one into the estate** — while the estate runs a pre-commit pin check, a
tamper guard, a tree-wipe guard and a deny list, **none of which any rule names.** Read from the
corpus, coverage is 8. Read from the estate, every gate is installed and firing. Both true; the join
is empty.

## The join is often already computed, and kept where nobody reads it

**Check before building anything.** In the third instance the checker *already produced* the
right-only set — gates that exist and that no rule names — and labelled it *"never a failure"*, and
its headline printed four numbers that were all left-list numbers. The join's other half existed,
was correct, and sat below the summary for as long as nobody scrolled.

**A number computed and kept out of the headline is not reported.** If it belongs to the conclusion,
it belongs on the line people read; if it does not belong to the conclusion, deleting it is more
honest than printing it where it will be missed.

## Guard

- **Name both lists and their owners, out loud.** If you cannot name the second list, you do not
  have a coverage number — you have an inventory.
- **Report matched / left-only / right-only, always three.** A single coverage figure is a net, and
  a net cannot show that the sets do not overlap.
- **Put the join in the headline**, not in a section below it. The section is where a computed
  number goes to be ignored.
- **Neither owner can be asked to fix it.** The join needs someone whose job is the pair — assign
  it, or accept that the gap will be found by accident.
- **Suspect it whenever two groups report on one territory and both are content.** Agreement
  between two lists that have never been joined is not corroboration; it is two people describing
  different things in compatible words.

---

*Earned from:* three instances on three different objects in a single day, each found only because
two parties happened to compare notes. A corpus reporting eight gates in place while nothing invoked
any of them. Twelve repositories declaring session names against ten live registrations, with zero
matches and nobody having listed both. And a rules corpus whose every gated rule resolves into its
own repository while every gate the estate actually runs is named by no rule at all — the two lists
blind to each other, both complete, both green.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'for each declared pair of inventories over one territory: the matched count and BOTH orphan sets, and whether all three appear in the headline of whatever reports either side'
trigger: 'CI over the reporting tools, and review when a coverage figure is added'
check: 'a report emitting a coverage count for one inventory with no orphan count for the other -> block; a declared pair with no join computed anywhere -> fail; a join computed but absent from the summary line while other counts are present -> block, naming the line'
escape: 'a legitimately non-empty orphan set is explained per entry rather than hidden - the rule asks for the number to be visible, never for it to be zero'
narrows: 'needs the PAIR declared. It cannot discover that a second inventory exists, which is the whole difficulty - in all three incidents the second list was known to somebody and paired with nothing. Once the pair is declared this is arithmetic; before that it is a question nobody has asked'
```
