# Upstream — where `skills/` came from, and how changes from it are taken

**`skills/` is a fork, not an original.** It began as
[github.com/mattpocock/skills](https://github.com/mattpocock/skills) — MIT, © Matt Pocock, whose
`LICENSE` is vendored here beside this file and stays there. `package.json` still carries the
upstream name and repository URL, which is the honest record of where these files started.

Since the fork, this corpus has added skills of its own and rewritten several of the originals.
This file is the policy for taking upstream changes into that fork, and it exists because the
default tool for the job decides everything by overwrite, in install order, with no record.

---

## The measurement this policy rests on

Measured 2026-09-13 against upstream `3cca18b` by a peer office, and **partially re-measured here.**
Their set arithmetic assumed 77 skills on this side. **This repo has 66** — 69 directories under
`skills/`, of which `docs/`, `lib/` and `scripts/` are not skills. That is a discrepancy of 11 in
the denominator of the decision, so **the overlap sets below are recorded as reported and are not
yet confirmed.** Re-run before acting on the per-skill numbers.

| bucket | reported | status |
|---|---|---|
| upstream-only | 13 | to re-check against a corrected denominator |
| ours-only | 53 | inconsistent with 66 total; re-measure |
| overlap, identical | 2 | `migrate-to-shoehorn`, `scaffold-exercises` |
| overlap, frontmatter only | 6 | `grill-me`, `grill-with-docs`, `implement`, `setup-pre-commit`, `git-guardrails-claude-code`, `resolving-merge-conflicts` |
| overlap, divergent | 16 | the real decision set |

## The policy

**1. Never run an installer that resolves the overlaps for us.** `npx skills add` decides all 24
overlaps by overwrite, in install order, and reports a count of what it installed rather than what
it replaced. A count of installs is a net figure —
[`a-delta-is-three-numbers`](../rules/analytics/a-delta-is-three-numbers.md) — and the composition
underneath it is the whole question. The largest thing it would take without a word is `tdd`, which
is 38 lines upstream and **108 here**: a rewrite somebody did for a reason.

**2. Pin the upstream ref, and diff against the pin.** Not against upstream `HEAD`, which moves for
reasons that have nothing to do with us. The pin is what makes drift a measurable event instead of
a permanent condition — the same mechanism `retrieve-lessons` already uses for rules.

**3. Every overlapping skill carries a dated verdict with a reason.** `ours` · `theirs` ·
`merged` · `not yet compared`. The verdict lives beside the skill, not in a message, and
**"not yet compared" is a real and acceptable value** — an undated blank is the thing that is not,
because a deliberate decision and an omission would otherwise look identical
([`absence-is-not-compliance`](../rules/testing/absence-is-not-compliance.md)).

**4. An upstream-only skill is not a free adoption.** No name collision is not the same as no cost.
Each one still clears this repo's bar: a code-bearing skill carries a self-test or an explicit line
in `_no-selftest.txt`, and every skill has to be something somebody here would actually reach for.
Adopting thirteen unreviewed skills into a corpus whose whole claim is that everything earned its
place would spend that claim to save an afternoon.

**5. The check fails on OUR omission, never on THEIR activity.** This is the part most easily got
backwards. Upstream moving is a correct state, not a defect — a check that fails when someone else
commits fires on correct rows, and a check that fires on correct rows gets switched off
([`a-verb-list-is-not-a-boundary`](../rules/testing/a-verb-list-is-not-a-boundary.md)). So:

- **report** the drift — which skills differ from the pin, with a count
- **fail** when an overlapping skill has no dated verdict, or when a skill whose verdict was
  `merged` has diverged again since that date

That way the trigger to re-ask "which is better" arrives on a real event, and the red light is
about a decision nobody made rather than about work somebody else did.

## Why the default is lossless

The question this fork cannot answer today is which version of a diverged skill is better. That is
the operator's own position — *"I want the better one to win, but we cannot tell that right away."*
**When the winner is unknown, the cheap error and the expensive error are not symmetric:** keeping
ours costs a stale file that a later comparison fixes; taking theirs costs a rewrite nobody
recorded, discovered later by someone who cannot tell it ever existed.

So the default is ours, the disagreement is dated, and the comparison is re-asked when evidence
arrives — not resolved now by whichever tool ran last.
