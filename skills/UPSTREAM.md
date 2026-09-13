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

Measured against upstream `3cca18b` on 2026-09-13, **re-run and reconciled** after a first pass used
a denominator that counted files as skills. The definition, applied symmetrically to both sides:
**a skill is a directory containing `SKILL.md`.**

| bucket | count |
|---|---|
| ours | **66** |
| upstream | **37** |
| in both — the decision set | **24** |
| upstream-only | **13** |
| ours-only | **42** |

Of the 24: 2 identical (`migrate-to-shoehorn`, `scaffold-exercises`), 6 differing only in
frontmatter (`grill-me`, `grill-with-docs`, `implement`, `setup-pre-commit`,
`git-guardrails-claude-code`, `resolving-merge-conflicts`), and 16 divergent in content — ranked by
divergence: `setup-matt-pocock-skills`, `prototype`, `triage`, `tdd`,
`improve-codebase-architecture`, `diagnosing-bugs`, `ask-matt`, `codebase-design`,
`domain-modeling`, `teach`, `writing-beats`, `handoff`, `writing-shape`, `loop-me`, `grilling`,
`writing-fragments`.

**The first pass overstated ours as 77 and ours-only as 53. The 24-name overlap set was unaffected**
— and that was luck rather than design. The overlap was computed by intersecting name lists, and the
spurious entries were files (`README.md`, `package.json`, `LICENSE` and six others) which cannot
collide with a directory name. **Had one spurious entry been named like a skill, it would have
entered the decision set silently.** A wrong denominator that happens to miss the bucket you act on
is not a safe wrong denominator; it is one whose blast radius nobody measured.

### A consequence worth knowing before anyone says yes

`setup-matt-pocock-skills` is **the most divergent file in the comparison**, and this corpus's copy
describes itself as prompt-driven rather than deterministic. So "apply the skills across all repos"
is not 24 identical edits — it is **24 judgement calls**, each one landing on whoever runs it.

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

**4. An upstream-only skill is not a free adoption, and a NAME is not enough to adopt from.** No
collision is not no cost. Each one clears this repo's bar: a code-bearing skill carries a self-test
or an explicit line in `_no-selftest.txt`, and every skill has to be something somebody here would
actually reach for. Adopting thirteen unreviewed skills into a corpus whose whole claim is that
everything earned its place would spend that claim to save an afternoon.

**Adoption reads the file, not the list.** The thirteen are known here only as names —
`claude-handoff`, `code-review`, `implement-spec`, `research`, `retro`, `setup-ts-deep-modules`,
`to-questionnaire`, `to-spec`, `to-tickets`, `wait-what`, `wayfinder`, `wizard`,
`writing-for-agents` — and a name states neither what a skill does nor whether it is code-bearing.
Adopting from a list is building from a relay
([`a-faithful-relay-loses-the-clause-that-matters`](../rules/how-we-work/a-faithful-relay-loses-the-clause-that-matters.md)):
the primary exists and is reachable, so it gets read first, one at a time, with the reason recorded
beside the adoption.

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

---

## The thirteen upstream-only skills — first-pass verdicts, 2026-09-13

**What these rest on, stated so they can be weighed:** the upstream tree read at the pin — category,
line count, files shipped, and the `description` line of each — plus **one skill read in full**
(`wayfinder`). They are survey verdicts, not reviews. Nothing is adopted.

**Three facts from the tree that no name list carries, and all three bear on adoption:**

1. **Four of the thirteen sit in upstream's own `in-progress/`** — `claude-handoff`,
   `implement-spec`, `retro`, `setup-ts-deep-modules`. The author has filed them as unfinished. That
   is a first-hand statement from the only person able to make it, and it settles those four without
   a line of comparison.
2. **Every upstream skill ships `agents/openai.yaml`** — a second-provider manifest. This corpus has
   none, and adopting brings a cross-provider surface nobody here has asked for or maintains. It is
   not a blocker; it is a cost that was invisible from the names.
3. **Upstream's tree is nested by category; ours is flat**, deliberately — `~/.claude/skills` points
   at `skills/`, so discovery stays flat. Every adoption is a move, not a copy, and `wizard` and
   `setup-ts-deep-modules` ship sibling files that move with them.

| skill | verdict | reason |
|---|---|---|
| `wayfinder` | **adopt, when the chain is approved** | The one genuine gap: planning work too large for a session as decision tickets on a tracker. 128 lines, domain-agnostic, nothing here does it. **Caveat that changes its cost:** it resolves tracker operations through the abstraction that `setup-matt-pocock-skills` installs — the single most divergent file in the comparison — so adopting it pulls that decision forward with it. |
| `to-spec` | **decline as duplicate** | We have `to-prd`, same job, different noun. |
| `to-tickets` | **decline as duplicate** | We have `to-issues`, same job, different noun. |
| `claude-handoff` | **decline for now** | Upstream `in-progress/`. We have `handoff` and `wrap`. |
| `implement-spec` | **decline for now** | Upstream `in-progress/`, 35 lines. We have `implement`. |
| `retro` | **decline for now** | Upstream `in-progress/`. |
| `setup-ts-deep-modules` | **decline for now** | Upstream `in-progress/`, and ships a `dependency-cruiser` config — a TypeScript-specific tool this corpus does not otherwise depend on. |
| `code-review` | not yet | 87 lines. Needs a real comparison against our `review`, which is not in the overlap set only because the names differ. |
| `writing-for-agents` | not yet | 81 lines, overlaps `writing-great-skills`. Same comparison, same reason. |
| `to-questionnaire` | not yet, worth a look | Turning a decision you cannot answer into a questionnaire is adjacent to `open-decisions-go-in-the-tracker` and may strengthen it rather than duplicate it. |
| `research` | not yet | 12 lines. Thin against `rules/research/`, which covers the same ground at length. |
| `wizard` | not yet | Ships `template.sh`. **Code-bearing under this repo's bar**, so adoption owes a self-test or a declared line in `_no-selftest.txt`. |
| `wait-what` | not yet | 7 lines. |

**`to-spec` and `to-tickets` are the decision hiding inside the adoption question.** They are not
free and they are not merely duplicates: adopting them beside `to-prd` and `to-issues` puts **two
chains with different nouns doing one job** into a flat namespace, and two implementations that
agree today diverge after the next edit
([`parallel-variants-same-schema`](../rules/data-engineering/parallel-variants-same-schema.md)). If
upstream's naming is preferred, the move is to **rename ours**, not to run both.
