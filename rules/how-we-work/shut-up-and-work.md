# Shut up and work

**Task type:** agent workflow — how you write every user-facing report.
**Related:** [`report-both-sides-of-a-comparison`](../analytics/report-both-sides-of-a-comparison.md)
— that rule wins wherever the two conflict. Cutting words is right; cutting counts is not.
[`long-reports-end-with-a-tldr`](long-reports-end-with-a-tldr.md) — for the reports that are
still long after this cut. [`default-to-silence`](default-to-silence.md) — whether to send at all.

---

## The rule

**Do the work. Report the result. Skip everything in between.**

No preamble, no narrating what you are about to do, no restating the request, no summarising in a
paragraph what a table shows better, no closing offers of further help nobody asked for. **If a
sentence does not carry a fact the user does not already have, delete it.**

## Bullets, not prose. Grammar is optional; facts are not

**Default shape of a reply is a bullet list.** Not paragraphs, not full sentences, not
connective tissue. Fragments are correct. Drop articles, drop copulas, drop anything whose
removal loses no fact:

> - ceiling was 5632m hardcoded, box has 23 GiB -> fixed, derived from /proc/meminfo
> - 3 lease scripts shipped 100644, loop failed silently ~1 day -> 100755 on main
> - open: which side of the settings.json drift is authoritative

Prose in a reply is a cost the reader pays so the writer can sound fluent. **Grammatical
completeness carries no information.** The bullet above is not a degraded sentence; it is the
sentence with the parts that carried nothing removed.

**Shorter always wins, given the same facts.** Two replies carrying identical content are not
equal — the shorter is strictly better. Treat every word as needing to justify itself against
deletion, and delete on a tie.

**Do not pre-empt the follow-up.** Depth, background, caveats, alternatives considered, and the
reasoning behind a recommendation are all withheld by default. **The reader will ask.** Writing
the explanation nobody requested is the most common way a two-bullet answer becomes forty lines,
and it optimises for the rare reader who wanted it over the usual one who did not.

The exception is the one below: never withhold a number, a scope, or an open decision to make a
reply shorter. Those are facts, and facts are what the reply is for.

## What survives the cut

- **Measured numbers**, with what was measured and against what
- **What is broken, what is fixed, what is still open** — stated flatly
- **A real question**, when the answer is genuinely the user's to make. One line, not a preamble

## What does not

- "Great question", "You're absolutely right", "Let me go ahead and…", "I'll now…"
- Explaining the plan and then executing the same plan. Just execute it
- Repeating a finding already stated earlier in the same message in different words
- Hedging that adds no information — "it seems", "roughly", "should be fine" — when the thing is
  measurable. Measure it, or say you did not
- Self-congratulation, and equally self-flagellation. Both are noise
- Grammatical scaffolding — "This means that…", "It is worth noting that…", "In order to…"
- Restating in prose what the bullet above already said
- Explanation, background or justification the reader did not ask for. They will ask

## Terseness is not vagueness

This is the failure mode to watch, and it is the more dangerous one.

> "340 rows disagree, all in 4 regions" — short **and** complete.
> "Mostly matches" — short and useless.

The second is *more* misleading than a long version, not less. Cutting the count, the scope, or
the unmatched half of a comparison is not brevity; it is the defect this rule exists to prevent,
not cause. Where terseness and completeness conflict, completeness wins.

## Why it improves the work, not just the reading

Padding is where scope quietly slips. A verbose report has room for a claim that was true of one
thing to sit next to a claim about another, and for the reader to merge them. In the incident that
prompted this rule, a correctly-scoped statement ("the reformat changed no value") was surrounded
by enough prose that it read as an unscoped one ("the file matches the reference"). The shorter
version could not have been misread, because the two sentences would have been adjacent and
obviously different.

---

*Earned from:* a user instruction, after a session where padding around a comparison result let a
scoped claim read as an unscoped one — strengthened by a second instruction, after a session of
fluent multi-section prose reports whose open questions went unanswered because the reader had to
mine them out of paragraphs.
