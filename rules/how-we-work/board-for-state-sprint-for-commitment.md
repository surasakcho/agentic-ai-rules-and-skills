# A board holds the state; a sprint holds the commitment

**Task type:** how-we-work — any project with more than a handful of tasks, and every project
where an agent generates work faster than a human closes it.
**Related:** [`open-decisions-go-in-the-tracker`](open-decisions-go-in-the-tracker.md) — the same
principle for questions rather than tasks; the board is where its entries live.
[`escalate-the-blocker-before-polishing-the-rest`](escalate-the-blocker-before-polishing-the-rest.md)
— what a WIP limit is for: it makes the blocked card visible instead of letting work drift to the
unblocked ones.

---

## The rule

> **Task state lives on a Kanban board. Implementation is committed in sprints.**

Two halves, and they answer different questions.

**The board answers "where is everything?"** Every task is a card in exactly one column, and the
columns are *states* the work is genuinely in — not a to-do list with headings. A card that exists
only in a plan document, a chat message or an agent's context is not tracked; it is remembered, and
remembering is what fails.

**Columns carry WIP limits, and that is the entire point of using a board rather than a list.** A
limit on the in-progress column is the mechanism that forces something to be finished before
something else is started. **A board with unlimited columns is a list drawn sideways** and buys
nothing.

**The sprint answers "what are we finishing, by when?"** A timeboxed set of cards with a stated
goal, agreed at the start and closed at the end. **Closing is the load-bearing act:** at the end of
the timebox every unfinished card is explicitly re-decided — carried, split, or dropped — and
saying which is not optional. Work that silently rolls forward has no cost and therefore no
deadline.

**A card that cannot plausibly finish inside one sprint is split before it is started**, not
discovered to be too big halfway through.

**The board is the single source of truth for status.** A progress report is read off the board.
If a report and the board disagree, the board is what is real and the report is a defect.

## Why this is easy to get wrong, and why agents make it worse

**A plan is a snapshot; a board is state.** Plans are written once, at the moment of most optimism,
and then diverge silently. Nothing in a plan document changes when a task is blocked, so a
three-week-old plan reads exactly like a current one.

**An agent has no yesterday.** A human carries an ambient sense of what is half-finished; a fresh
session carries none. Whatever is not written into a durable board simply does not exist at the
start of the next session — so an agent-driven project without one restarts its own prioritisation
from scratch, repeatedly, and each restart looks like diligence.

**And agents generate work faster than they close it, in a specific direction.** Analysis, options,
review rounds and further investigation are cheap and always available; shipping is not. Without a
WIP limit and a timebox, the cheap work expands to fill the project — and it is
*indistinguishable from rigour from the inside*, because every individual step is defensible. The
sprint boundary is the only thing that asks "and what shipped?"

## The pattern this was written from

**Stated as an operator directive rather than earned from one failure**, and grounded in a pattern
that recurred across an incubator project over several months:

- **Dozens of ideas explored end to end; nothing shipped.** Every exploration was individually
  well-executed. None was ever the last step of anything.
- **One design document took seven review rounds, costing several times what simply running the
  experiment it was designing would have cost.** Every round found real defects. The design never
  changed shape, and no round was allowed to end the object.
- **A blocker was identified in round two and never escalated**, while work continued on the parts
  that were not blocked — because those were the tractable ones.
- That project eventually had to add a rule that *a check must be able to end in shipping*, because
  every check it ran was capable of killing and none was capable of clearing.

**All four are the same disease: unbounded work-in-progress and no timebox.** A WIP limit stops the
second and third directly — you cannot open round seven while the limit is full, and the blocked
card is the visible reason nothing moves. A sprint boundary stops the first and fourth, because
"what shipped this sprint?" is a question that cannot be answered with analysis.

## Guard

- **One card, one column, one owner.** A task in two places is a task nobody owns.
- **Set a WIP limit on the in-progress column before the first card enters it.** Retrofitting a
  limit onto a full board just relabels the overload.
- **Close the sprint out loud.** Name every unfinished card and say carried / split / dropped.
  Silence is how a sprint becomes a rolling backlog with extra ceremony.
- **Split before starting, not halfway through.** "Too big" discovered mid-flight is what produces
  a card that has been in progress for a month.
- **Read status off the board.** If you are writing a progress summary from memory, the board is
  not being maintained and the summary is fiction.
- **A blocked card stays visible and keeps its slot.** Moving it aside to "unblock the flow" is
  exactly the displacement this rule exists to prevent — a blocked card occupying a WIP slot is
  the pressure that gets it escalated.
- **Where the board lives is per-project and belongs in that project's own configuration** — an
  issue tracker, a project board, a checked-in markdown file. The rule is that one exists, is
  written to as work changes state, and outlives any single session.

---

*Earned from:* an operator directive, grounded in an incubator project that explored dozens of
ideas without shipping one, ran seven review rounds on a single document at several times the cost
of the experiment it described, and left a round-two blocker unescalated while polishing the parts
that were not blocked — one disease with three symptoms, all of them unbounded WIP and no timebox.
