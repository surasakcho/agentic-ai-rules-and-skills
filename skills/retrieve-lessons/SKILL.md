---
name: retrieve-lessons
description: Adopt the shared working rules from the agentic-ai-rules-and-skills repo into a repo that does not have them yet — detect what kind of work the repo actually does, select only the rule categories with evidence behind them, and link them from its CLAUDE.md pinned to a commit so drift is detectable. Use when starting work in a new or unfamiliar repo, when a repo's CLAUDE.md has no shared-rules section, when asked to "retrieve/adopt/apply the shared lessons or rules", or to re-check whether an adopted pin has gone stale.
license: MIT
---

# Retrieve Lessons

The consuming half of the cycle. [`lesson-review`](../lesson-review/SKILL.md) publishes what a
project learned; this pulls it into the next repo so the lesson is paid for once.

**Shared repo:** `https://github.com/surasakcho/agentic-ai-rules-and-skills`

```bash
python -X utf8 retrieve.py --repo <target-repo>            # detect + show what it would adopt
python -X utf8 retrieve.py --repo <target-repo> --write    # re-detect categories, write the block
python -X utf8 retrieve.py --repo <target-repo> --repin    # advance the SHA, keep the categories
python -X utf8 retrieve.py --repo <target-repo> --check    # exit 1 only if a RULE moved
```

## `--write` and `--repin` are different operations, and separating them is what makes this safe

`--write` does two things at once, with very different risk:

| | risk | needs |
|---|---|---|
| **re-select** — which categories apply | judgement; detection is wrong in both directions | a human |
| **re-pin** — advance the SHA over links already chosen | mechanical, fully verifiable | nothing |

Coupling them is why none of this could be automated. A job that silently re-runs detection
across twenty repos is a bad idea; a job that advances a SHA over a set a human already chose,
and **stops** if any of those links stopped resolving, is not.

`--repin` reads the categories back out of the existing block and never calls `detect()` — it runs
before detection is reached at all, so *"never re-detects"* is structural rather than a promise.
The original *"selected because…"* evidence is preserved verbatim; re-deriving it would be
detection by the back door. It **refuses** on a repo with no block, because first-time adoption is
category selection and that is judgement.

**A rule that VANISHED stops the run.** `verify_links` cannot catch that — it checks the links
about to be written, and a deleted rule simply stops being one. A rule contradicted by later
experience is *deleted, not hedged*, so a disappearance can mean this repo is currently doing
something now known to be wrong. That is the one case that must reach a person.

## `--check` fires on `rules/`, not on repo HEAD

**A commit touching only `skills/` does not make any consumer stale, and `--check` no longer says
it does.** Skills reach sessions by symlink and are live on pull; only rules are pinned. The old
HEAD comparison marked every repo stale on a skills-only commit, and the fix it recommended was a
**provable no-op** — one observed case would have rewritten 78 links to say nothing different.

**A checker whose recommended fix changes nothing is how a checker gets muted**, and a muted
checker misses the commit that did move a rule. So `--check` now reports three states, and
`--repin` holds by itself unless `--force` is passed:

- **current** — pin equals the published SHA.
- **behind, but no rule moved** — exit 0, and it says holding is correct.
- **behind, and N rules moved** — exit 1, **naming each file**, so you read the diff rather than
  re-pinning blind.

A fourth exists and is deliberately not folded into "no change": if the diff between the two SHAs
cannot be read at all, that is **unverifiable, not verified**, and it fails.

Paths are arguments, never literals — a machine path in a shared skill publishes a username
and a directory layout.

## The two decisions this encodes

**Link, don't copy.** A copied rule drifts out of agreement with its source and nobody
notices, because a copy looks exactly as authoritative as the original. The block written into
`CLAUDE.md` contains links, not text.

**Pin the commit.** A bare link silently becomes a link to something else. The block records
the shared repo's commit, so `--check` can tell you the rules moved and you can go read *what*
changed. An unpinned reference cannot distinguish "still true" from "nobody looked".

## Select on evidence, never adopt wholesale

`retrieve.py` matches each rule category against real signals — declared dependencies,
directory names, file globs — and adopts only the categories that hit. A repo with no `tests/`
and no test runner does not get the testing rule.

This restraint is the whole point. A `CLAUDE.md` carrying nine rules where two apply teaches
the reader that most of it is skippable, and then the two that mattered get skipped too.
**Adopting nothing is a valid outcome** and the script says so rather than inventing a match.

## The pass, in order

1. **Run it without `--write`** and read what it proposes. The evidence for each category is
   printed next to it — if the evidence looks wrong, the detection is wrong, and adopting on
   top of a bad match is worse than not adopting.
2. **Read the rules it selected.** They are short and each names a real incident. This is the
   step that cannot be automated and the one that makes the adoption real; a linked rule
   nobody has read is a citation, not a practice.
3. **`--write`.** Idempotent — re-running refreshes the block in place and preserves
   everything else in `CLAUDE.md`.
4. **Install the skills the rules mechanise,** where they apply: `verify-outputs` for any repo
   that produces figures, tables or reported numbers. `prose < checklist < test < gate` — a
   rule that can run should be running.
5. **Re-check periodically.** `--check` in a pre-commit hook turns a stale pin into a failing
   commit instead of a rule nobody re-read.

## When the shared repo has moved

`--check` failing is not noise — it means a rule you are relying on may have changed or been
deleted. **A rule contradicted by later experience gets deleted, not hedged**, so a moved pin
can mean something you are currently doing is now known to be wrong. Read the diff, then
`--write` to re-pin.

If the shared repo has been reorganised such that a selected category no longer exists, the
script **errors out** rather than quietly adopting fewer rules. A silent skip is how a repo
ends up believing it has coverage it does not have.
