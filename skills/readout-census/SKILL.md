---
name: readout-census
description: Audit every named flag, metric or status a system ships against the hidden fact it is named after, using rate and lift rather than rate alone. Use when a metric looks healthy but conclusions drawn from it keep being wrong, before trusting telemetry in a design or product decision, when a feature is blamed for being flat, or when asked whether an instrument actually measures what its name claims.
---

# Readout census — does the flag measure the thing it is named after?

## The problem this exists for

A flag named `heard.rising` — *"a predator is hunting nearby"* — read a perfectly healthy **42.7%
of ticks**. It was a readout of the player's own footsteps. It fired **less** during a hunt than
outside one.

Three days of conclusions rested on it. The game read **0% cleared** and a teaching beat was blamed
for it. Repairing that one expression took the clear rate to **45%** with no design change at all.

**Counting could not have found this.** 42.7% is a true number. It was about the wrong object.
Every check anyone had was a check on the *rate*, and the rate was fine.

## The measurement

For every named readout, two numbers instead of one:

```
RATE   fraction of ticks (or runs) on which it is true
LIFT   P(true | the hidden fact it is named after)
     − P(true | that fact absent)              ... in points
```

**Lift is the guard question made computable** — *if the thing I am claiming were false, would this
number be different?* Rate said healthy. Lift said **−7.9**: anti-correlated with the thing it names.

A row fails on `rate ≈ 0` (never exercised), `rate ≈ 100` (distinguishes nothing), or `lift ≤ 0`
(does not detect the thing it is named after, or detects its opposite).

## Two verdicts that were earned, not designed

**`UNTESTED` — the fact never happened often enough to correlate against.** This is a finding in
its own right, and not the same as a broken readout: the world never produced the thing the flag
names. One project's death cause `endedBy: 'seen'` was structurally impossible to reach, so its
zero read as balance.

**`SIMPSON` — pooled lift ≤ 0 while every profile with evidence lifts positively.** Pooling across
populations can reverse a sign. One released game pools to **−8.7** on a row where the only profile
that ever meets the condition lifts **+37.5**. Reporting that as inverted would be exactly the class
of misleading number this tool exists to delete, so it fails — the pooled figure is unusable — but
it is named for what it is and the reader is sent to the per-profile block. **A tool built to catch
a misleading correlation must not manufacture one.**

## The manifest is the cost centre

Someone has to declare, per readout, the hidden fact it is named after:

```js
export const CENSUS = [
  { name:  'sense.heard.rising',
    scope: 'tick',                                   // 'tick' | 'run'
    of:    'a predator is hunting',                  // the fact, in English
    read:  (s) => s.sense.heard.rising,              // the READOUT
    truth: (s) => s.hidden.predators.some((w) => w.mode === 'hunting'),
  },
]
```

**This is what decides whether the tool gets used at all.** A check nobody registers their flags
with finds nothing. Two arrow functions and a one-sentence `of` is the cheapest declaration that
still carries meaning — and putting reference rows in the project *template* means copying the
template hands someone a working manifest to edit rather than a document to obey.

The `of` line is load-bearing beyond readability: it is the inspecting step that survives inside an
executing check. **A wrong `of` produces a confident, useless row.** One row read `−4.3` because the
comparison pool for *"predator interested"* contained *"predator hunting"*, where the flag is true
62.9% of the time — measuring against the strongest state of the same fact. Corrected: `+1.3`.

A row with no `truth` is rate-only. It still catches "never exercised" and "always true", and the
footer counts how many rows dodged the lift column, **so laziness is visible rather than silent.**

## What it is for: auditing work you already shipped

Run against a game that had already been released and rated, it found the death taxonomy had two
values of which one had never once occurred in 600 runs, and that the "mistiming" metric measures
timing for exactly one of three player profiles — below that it is recall failure wearing timing's
name. **That game's central design claim was measured with that column.**

## Porting it

`assets/census.mjs` is a **reference implementation, not a drop-in.** It imports its host project's
simulation harness (`createDriver`, `replay`, `TICK_DT`) and assumes a deterministic engine that can
be replayed. What ports is the method: the manifest shape, rate-and-lift, the four verdicts, and the
read-only guarantee — census only observes, and a sampled determinism replay enforces it, because a
`read` that mutated state would stop measuring the run every other tool measured.

Any system with named readouts and a recoverable ground truth can carry this: feature flags against
the conditions they gate, alert predicates against the incidents they fire for, a classifier's
labels against adjudicated outcomes.

## Related

[`discriminate-by-executing-not-inspecting`](../../rules/how-we-work/discriminate-by-executing-not-inspecting.md)
— the rule this mechanises; its "measure lift, not rate" section is this tool in one paragraph.
[`validations-must-fail`](../../rules/testing/validations-must-fail.md) — ask what would still be
green if the thing were already broken.

Built in a gamedev-lab repo (`qa/census.mjs`) and published here as a reference implementation.
