# A rule that cannot be quoted in one line gets adopted as a URL

**Task type:** how we work — authoring a rule in a shared corpus, and building anything that
adopts rules into a consuming repo.
**Related:**
[`a-classification-is-not-a-gate`](a-classification-is-not-a-gate.md) — the sibling obligation.
That one says a rule ships with its gate; this says it ships with its statement.
[`structure-new-project-claude-md`](structure-new-project-claude-md.md) — what the consuming
file looks like once the statements arrive in it.
[`write-in-fragments-not-sentences`](write-in-fragments-not-sentences.md) — the same compression
discipline, applied to a reply instead of a rule.
[`retrieve-lessons-weekly`](retrieve-lessons-weekly.md) — the pass that does the adopting, and
the thing this rule exists to keep useful.

---

## The rule

> **Every rule states itself in ONE quotable line, in a fixed place a machine can find: the first
> non-empty line under `## The rule`, as a blockquote or a bold statement.** A rule with no such
> line cannot be adopted as text, so it gets adopted as a link — and a link is not in context at
> the moment the rule applies.

## The incident

**Adopted, pinned, read aloud, and it still did not fire.**
`board-for-state-sprint-for-commitment` was adopted into a repo, pinned to a sha, read during the
retrieval pass and quoted back to the operator. A flat task list was written anyway, in the repo
whose `CLAUDE.md` links it. The diagnosis at the time was exact: *it is a URL in `CLAUDE.md`, not
text in context.*

The shape of the adopted block explains it. In one repo that block is **97 lines carrying ~90
URLs and not one sentence of rule text.** Nobody opens ninety links, so the rules end up known by
reputation.

**The fix that followed was a renderer** — a skill that prints the rule text on demand. It is a
good tool and it does not close this: a rule you must invoke something to see is still not in
front of you at the moment it applies. **On-demand is the same failure as a link, one step later.**

## Why the statement has to be MECHANICAL, not merely present

Every rule here "had" a statement in the sense that a human could read one out. Measured across
93 rule files, **9 had no line a script could lift**: they opened `## The rule` on plain prose,
and two had no `## The rule` heading at all.

**Nobody had specified the shape, so it drifted into three** — blockquote (36), bold (57), and
bare prose (9). The first two are both fine and both extractable; the third is only extractable
by a human.

That is the whole cost: **an adopter cannot tell "this rule has no short form" from "this rule's
short form is written differently".** It has to either guess, or fall back to the link — and the
fallback is silent, which is how 90 URLs accumulate without anyone deciding to have them.

> **A parser with a fallback hides an inconsistency forever.** The fallback fires, the output
> looks complete, and the nine malformed files stay malformed because nothing ever complains.
> Fix the shape and the extraction becomes structural rather than a promise — the same argument
> `--repin` uses for never re-running detection.

## Two shapes, not one — and why that is not drift

**Blockquote and bold are both accepted.** 57 rules use bold and 36 use a blockquote; forcing
either population into the other is 57 or 36 edits of pure churn, and neither reads better.

What makes two shapes safe here is that the predicate is still exact: *the first non-empty line
under `## The rule` begins with `>` or `**`*. A machine can answer that. **Two shapes a checker
accepts is a specification; three shapes nobody wrote down is drift.**

## The statement carries the trigger, or it is only half a pointer

A quotable line is necessary and not sufficient. The adopted block is a **context pointer**, and
a pointer does two jobs: say what the material is, and say **when to reach for it**. A statement
with no trigger is a fact the reader agrees with and never acts on.

- **State the behaviour, not the topic.** *"Join only on exact equality of a complete key"* fires.
  *"About joins"* does not.
- **Lead with the moment where it is decidable.** *"Before any write that destroys existing
  content…"* puts the trigger first, so the reader meets it while the decision is still open.
- **Positive over prohibition where both work.** A ban drags the banned behaviour into context;
  the corpus keeps prohibitions for hard guardrails and pairs them with the positive target.

## Guard

- **Write the statement first, then the rule.** If it will not compress to a line, the rule is
  carrying two rules and should be split.
- **Put it in the fixed place.** First non-empty line under `## The rule`, blockquote or bold.
- **Make the adopter REFUSE a rule with no statement** rather than falling back to the link.
  A silent fallback is indistinguishable from coverage.
- **Never widen the accepted shapes to make a malformed file pass.** Fix the file.

---

*Earned from:* the measured non-firing of an adopted, pinned, quoted rule, whose diagnosis was
that it existed in the consuming repo only as a URL; and from a sweep of this corpus on
2026-09-19 that found 9 of 93 rules with no machine-extractable statement and no specified shape
for one. Both were found while building the adopter that needs the statements — which is the
usual way a missing specification is discovered: by the first tool that tries to rely on it.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: interposed
observable: 'every file under rules/, against whether its first non-empty line beneath the "## The rule" heading begins with ">" or "**"'
trigger: 'at adoption -- the moment a rule is about to be written into a consuming repo as text'
check: 'heading absent, or first non-empty line beneath it is neither blockquote nor bold -> REFUSE to adopt that rule, naming the file. Never fall back to emitting the bare link: the fallback is silent and is how an all-URL block accumulates'
escape: 'none for adoption. A rule genuinely too large for one line is two rules and gets split'
implemented_by: 'skills/refresh-rules/'
invoked_by: 'refresh-rules, at adoption time'
note: 'Gateable and gated here WITHOUT touching the estate machinery this office may not build: the refusal lives in the adopting tool, not in a hook, a settings.json or a pre-commit installer. A consuming repo that never runs the adopter is never wrong about its own rules -- it simply has none, which is the honest state'
```
