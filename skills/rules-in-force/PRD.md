# PRD — rules-in-force

**Status:** agreed
**Owner:** the operator.

*Filed in the skill directory; this repo has no `docs/` tree.*

## The user and the problem

**Anyone — person or session — starting work in a repo that has adopted the shared rules, who
needs to know what they are actually bound by right now.**

What they do today instead: nothing, or they scroll `CLAUDE.md`. The adopted block is a list of
**links**. In one real repo it is 97 lines holding ~90 URLs and not one sentence of rule text.
Opening ninety links is not a thing anyone does, so in practice the rules are known by
reputation.

**This has already been measured failing, in this estate, on this repo.**
`board-for-state-sprint-for-commitment` was adopted, read during the retrieval pass, and quoted
back to the operator — and a flat task list was then written anyway, in the repo whose
`CLAUDE.md` links it. Adopted, cited, pinned, **did not fire.** The recorded diagnosis was
exact: *it is a URL in `CLAUDE.md`, not text in context, so it was not in front of me at the
moment it applied.*

A second, quieter problem sits underneath. The block is **pinned to a commit**, so the rules in
force are the rules *as they were at that commit* — not as they read today. Anyone summarising
from the current working tree describes rules the repo has not adopted.

## What it must do

- Given a repo, print the rules currently in force, **grouped by category, one statement each**,
  so the set can be read in one pass instead of ninety.
- Take each rule's statement **verbatim from the rule file**. Never paraphrase, never generate.
  Paraphrase is where meaning shifts, and the shift is undetectable once the original is gone.
- Read every rule **at the pinned commit**, not at the shared repo's HEAD. Where the two differ,
  say so — that difference is the repo's staleness, and it is information, not an error.
- Include the repo's **own** local rules as well as the adopted ones. Local rules win on
  conflict, so a digest that omits them is wrong rather than merely incomplete.
- **Report a denominator and name every omission.** How many rules are in force, how many
  statements were extracted, and which files it could not extract — by name. A digest that
  silently drops a rule is worse than no digest.
- Take the repo as an argument; no machine-specific paths in the tool.

## What it will NOT do

- **Not summarise, rank, shorten or interpret a rule.** It extracts and arranges. The moment it
  writes its own sentence about a rule it becomes a second, drifting copy of that rule.
- **Not modify anything** — not `CLAUDE.md`, not the pin, not the shared clone. Refreshing a
  stale pin belongs to `retrieve-lessons`.
- **Not judge whether a rule applies** to the work at hand, and not tell anyone which to obey
  first. Adoption already selected the categories; precedence is the reader's.
- **Not fetch over the network.** It reads a local clone at a local commit. A digest that needs
  connectivity cannot run at session start, which is the only moment it matters.
- **Not check whether the rules are being followed.** Knowing the rules and conforming to them
  are different problems; this is the first one only.

## Done

**A reader who has never opened the repo can run one command and, from its output alone, state
what every rule in force requires — without following a single link.** For a repo with ~90
adopted rules the digest is one screenful per category, every line traceable to a file, and the
run ends with a count that reconciles: rules in force = statements extracted + omissions named.

**Stop condition:** written once, reviewed once. Round two must name what would make me abandon
it rather than revise it — the likely candidate being that the digest is still too long to be
read at session start, in which case the answer is not a shorter digest but a different
mechanism, and this tool should be deleted rather than trimmed.

## Open questions

- Whether the digest should be *injected* at session start rather than run on demand. That is
  the Kanban item this tool serves ("every session actually FOLLOWS how-we-work, not just links
  it") and it is not settled; this tool is useful either way and does not presuppose the answer.
