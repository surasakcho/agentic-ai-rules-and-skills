# If the space is enumerable, solve it — do not sample it one hypothesis at a time

**Task type:** analytics — root-causing a discrepancy, or establishing that no explanation of a
given kind exists.
**Related:** [`validations-must-fail`](../testing/validations-must-fail.md) — the positive
control below is that rule applied to a solver.
[`adjudicate-with-an-external-source`](../data-engineering/adjudicate-with-an-external-source.md)
— what to do once you have established the discrepancy is real.

---

## The rule

**A hypothesis hunt can only ever say "not this one." If the space of explanations is finite and
describable, formulate it as a feasibility problem and solve it exactly — that is the only way to
say "and nothing else will work."**

Sampling a space and solving a space produce different *kinds* of claim. A hundred failed
hypotheses is weak evidence of impossibility. One infeasibility certificate over the whole space
is proof. The second is usually far cheaper than the first, and it is the one that closes a
question instead of deferring it.

## The incident

A pipeline's category breakdown disagreed with a reference file for one region — same
boundaries, same identifiers, same totals, but area distributed differently across ~5 categories.

**Hours were spent sampling:** dozens of processing variants, edge-handling configurations,
combinations of source layer and boundary file, and brute-force searches over individual
records. Every run answered "not this either." None could answer "and nothing else will work,"
so the question stayed open and kept being re-litigated.

The space was **finite and small to describe**: does any assignment of the region's ~100
classification codes to 5 categories reproduce the reference figures? That is 5^100 candidate
mappings, and an integer program settles it in a single solve:

```
binary x[c,k],  Σ_k x[c,k] = 1                        # each code gets exactly one category
∀ unit u, category k:  Σ_c value[u,c] · x[c,k] = target[u,k] ± tol
```

**Result: INFEASIBLE at every tolerance up to ±85 area units**, against a match threshold of
0.003 — a factor of ~27,000. Hours of variant-testing replaced by one certificate, and the
question closed.

**Cost of not doing this first:** most of a working session, plus a conclusion stated as "proven"
that had to be partly retracted because it rested on hand-built arguments instead of the solve.
One of those arguments was a **non-sequitur that survived because nobody could check it against
anything**: "only one code spans two categories, therefore no relabelling can move value into
categories W or M." True premise; false conclusion — 31 codes were in fact unconstrained. The
solve had no such failure mode.

## Ask this early

> **Is the space I am sampling actually enumerable?**

It usually is, and more often than it looks:

- assignments of labels to categories → integer program / SAT
- "could this total be made of some subset of these parts?" → subset-sum, exact by dynamic
  programming
- orderings, groupings, mappings between two finite sets → constraint solver
- "which combination of these N flags reproduces the output?" → 2^N, brute-forceable to ~25

If it is, stop generating variants and write the constraint.

## Prove the solver proved it — `success == False` is not a negative result

**This is where a solve can silently become as weak as the sampling it replaced.**

`scipy.optimize.milp` returns `success=False` for **infeasible (status 2)**, **iteration or time
limit (1)**, and **numerical failure (4)** alike. Reporting "no such assignment exists" off the
boolean would have been an unfalsifiable claim resting on a timeout. The same trap exists in
every solver API that offers a convenience boolean over a status enum.

Three things a load-bearing negative needs:

1. **The certificate, not the flag.** Read the status: `status == 2`, backend
   `model_status = Infeasible`. That is a proof of infeasibility; a limit is not.
2. **A bound, by binary search on the tolerance.** "Infeasible at ±0.001" invites the reply
   *"then loosen it"*. **"Infeasible up to ±85.16, feasible from ±85.94"** does not — it states
   how far from possible the best candidate is, in the reader's own units.
3. **A positive control on the same harness.** A comparable case with a *known* explanation must
   come back FEASIBLE. Here a second region — where the reference file was known to have used an
   older survey vintage — returned feasible **and reconstructed the pipeline's own mapping with
   zero codes reassigned.** Without that, "INFEASIBLE" is equally consistent with having
   misspecified the model.

The positive control is the whole difference between "the solver says no" and "no exists."

## Guard

If a conclusion depends on *nothing else being possible*, it must rest on an enumeration or a
certificate — never on a list of things you happened to try. And if a solver produced the
certificate, state its status code and show the control that came back positive.
