---
name: rules-in-force
description: Print what a repo is actually bound by right now — every adopted rule's own statement, verbatim, grouped by category, read at the commit the repo pinned, plus the repo's own local rules. Use at the start of work in a repo, when asked "what are the rules here", before a review, or whenever a rule was adopted and did not fire.
---

# rules-in-force — the rules as text, not as ninety links

## Why this exists

**A rule that is a URL is not in front of you at the moment it applies.**

`retrieve-lessons` writes an adopted block into `CLAUDE.md`, and that block is a list of
**links**. In one real repo it is 97 lines carrying ~90 URLs and not one sentence of rule text.
Nobody opens ninety links, so the rules end up known by reputation.

**This has been measured failing, in this estate.**
`board-for-state-sprint-for-commitment` was adopted, pinned, read during the retrieval pass and
quoted back to the operator — and a flat task list was written anyway, in the repo whose
`CLAUDE.md` links it. **Adopted, cited, pinned, did not fire.** The diagnosis at the time was
exact: *it is a URL in `CLAUDE.md`, not text in context.*

**The fix is not to paste the rules into `CLAUDE.md`.** A copied rule drifts out of agreement
with its source and nobody notices, because a copy looks exactly as authoritative as the
original. Linking is the right storage decision. What was missing was a way to *render* the
linked text on demand — which is all this is.

## Use it

```sh
python3 rules_in_force.py --repo <repo>                      # the full digest
python3 rules_in_force.py --repo <repo> --category coding     # one category, repeatable
python3 rules_in_force.py --repo <repo> --brief               # names only
python3 rules_in_force.py --repo <repo> --drift               # also: what moved since the pin
```

`--shared <clone>` points at the shared rules repo; it defaults to the clone this script lives
in. Exit 0 digest printed · 1 nothing adopted · 2 cannot run.

**It reads only. It never edits `CLAUDE.md`, never re-pins, never fetches.** Refreshing a stale
pin is `retrieve-lessons`' job, and it involves reading a diff — which is a decision, not a
render.

## The three decisions that make the output trustworthy

**1. Verbatim, never paraphrased.** Each line is the rule's own statement lifted from its file.
The tool arranges; it does not write. The moment a digest phrases a rule in its own words it
becomes a second copy of that rule, drifting, and indistinguishable from the original to
whoever reads it next.

*Emphasis markers are stripped for legibility. Nothing else is altered — no rewording, no
truncation, no summarising.*

**2. Read at the PIN, not at HEAD.** The block pins a commit, so the rules in force are the
rules *as they were at that commit*. A digest built from the working tree describes rules the
repo has not adopted — confidently, and wrongly. `--drift` names the ones that differ, and says
plainly that the pin is what binds.

**3. The count must reconcile, and omissions are named.**
`rules adopted = statements shown + not extracted + filtered out`, printed every run, with
every unextractable file listed by path. **A digest that silently drops a rule reproduces the
exact failure it was built to fix, inside the tool.** Two files in the corpus carry no
`## The rule` section and are reported by name on every run rather than quietly skipped.

## Local rules come first, and are listed first

The repo's own `CLAUDE.md` content — everything outside the adopted block — **wins on conflict**
with anything shared. A digest that showed only the adopted rules would be wrong rather than
merely incomplete, so local headings are printed above the shared set and labelled as taking
precedence.

## What it will not tell you

- **Whether a rule applies to the work in front of you.** Adoption already chose the
  categories; relevance is yours.
- **Which rule wins** beyond the local-over-shared split above.
- **Whether the rules are being followed.** Knowing them and conforming to them are different
  problems and this is only the first.

## A known limit, stated because green is the dangerous colour

**Running this does not make a rule fire.** It closes the gap between *the rule is linked* and
*the rule is legible*, which is a real gap and the measured one — but a digest read once at the
start of a session is still text somebody has to remember at the right moment. `prose <
checklist < test < gate`: where a rule can be mechanised, mechanise it, and treat this as the
floor rather than the ceiling.

## Related

[`retrieve-lessons`](../retrieve-lessons/SKILL.md) — writes and re-pins the block this reads.
[`write-it-down-when-you-read-it`](../../rules/how-we-work/write-it-down-when-you-read-it.md)
— why the statement is quoted rather than summarised.
[`a-gate-that-fires-at-commit-time-is-not-a-gate`](../../rules/coding/a-gate-that-fires-at-commit-time-is-not-a-gate.md)
— why a digest is a floor, not a control.

[`PRD.md`](PRD.md) — the problem, and the five things this deliberately will not do.
