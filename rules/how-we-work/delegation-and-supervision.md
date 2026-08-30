# Delegation and supervision

**Task type:** agent workflow — deciding what to hand to an AI agent, and what to do with
what comes back.

---

## Match effort to failure mode

**Expensive reasoning for silent failures; cheap execution for loud ones.**

Delegate when the task is execution against a known plan and mistakes surface immediately:
writing and running tests, authoring content against a locked format, UI wiring, doc updates.

Do **not** delegate:

- novel algorithmic or mathematical work
- architectural decisions spanning modules
- choosing *what* invariants to test — the invariant is named at full effort, the harness is
  built cheaply
- **any edit to an existing test's assertions or tolerances**

Standing rules for delegated work: never weaken an assertion to make a test pass; failures
come back for diagnosis rather than being worked around; diffs are reviewed before commit.

## Verify what agents report — including the parts that sound right

Agent output is evidence to check, not a result to relay.

> **Incident A.** Two independent reviewers were commissioned on the same dataset. Both
> produced strong reports. One concluded that a set of bound violations was "a bug in the
> profiler" — but that reviewer had run *after* the underlying data was fixed and was
> attributing clean output to the wrong cause. Relaying it would have published a false root
> cause.

> **Incident B.** A reviewer flagged a possible identifier mix-up between two units, based on
> exactly complementary population discrepancies repeated across three separate years. That
> one was real, specific, and would not have been found without the delegation.

Both came from the same pass. The lesson is not "distrust agents" — it is **re-measure the
claims that will be acted on**, and note explicitly which ones you verified.

### Re-derive the load-bearing claim yourself, on a different path

Delegate breadth. Never delegate the single step the conclusion rests on.

> **Incident.** Four agents investigated why a pipeline disagreed with a reference dataset for
> one region. Their reports were detailed, quantitative and confident. Of the three claims the
> conclusion rested on:
>
> - one was a **non-sequitur** — "only one classification code spans two categories, therefore no
>   relabelling can move value into categories W or M." The premise was true. The conclusion was
>   false: 31 codes were in fact unconstrained, several of them in W and M. The reasoning error
>   was invisible because the premise was checkable and the conclusion was not.
> - one was **circular** — a statistic offered as independent corroboration that was arithmetically
>   implied by a fact already established.
> - one **held**, and was the result worth having.
>
> **Cost:** a conclusion described to the user as "proven" that needed two public retractions.

The two bad claims shared a shape: **specific, quantitative, and unfalsifiable by anything else in
the report.** Confidence and numeric detail are not evidence of soundness; they are what a wrong
claim looks like when a capable writer produces it.

**The check that works: re-implement the decisive test from scratch, on a different path** — a
different input file, a different derivation of the same quantity, ideally a different method.
Agreement then means something. Here the decisive feasibility test was rewritten independently
against a different boundary source and returned the identical result set; *that* is what made it
safe to publish. Re-reading the agent's own script would have proved nothing.

**And state which claims you verified yourself.** A report that mixes verified and relayed claims
in one voice is a report whose reader cannot calibrate any of it.

## Ask reviewers for negative results

"I checked X and it is fine" is valuable and will not be volunteered unless requested. A
review that returns only findings gives no information about coverage.

## Grill before delegating, not after

If the requirement is at all unclear, interrogate it **before** handing it out. A vague
requirement delegated is a vague result returned, at full cost.

## The manager's own check

After every role signs off, review the output yourself before it reaches the user. In
practice this is where the "did anyone actually look at this?" question gets asked — and in
one project, asking it late turned up **six defects in the first fourteen figures examined**.
