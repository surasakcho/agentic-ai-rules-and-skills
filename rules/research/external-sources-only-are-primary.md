# Only an external source is primary — a repo file is a lead, not evidence

**Task type:** research — any claim that will be cited, reused, or handed to a decision-maker.
**Related:** [`research-and-qa-logs`](research-and-qa-logs.md) is where findings get written down;
this is the rule that stops a written-down finding from being mistaken for verification.

---

## The rule

**A claim is only as good as its most recent check against a live, external source** — a news
article, a government or regulator page, a company filing or press release, academic literature,
or similar material published outside this project's own AI-agent output. Anything else — a `.md`
research note, a ledger entry, a prior agent's summary, a deliverable — is a **lead to go re-check**,
never itself the evidence.

This holds **even when the internal file says "VERIFIED."** A prior pass's confidence is not
current evidence. Treat every AI-written file in the repo, including ones you wrote yourself
earlier this session, as capable of containing a hallucinated figure, a wrong attribution, or a
fabricated link — because it is exactly that kind of file that produces exactly that kind of error.

## What counts as primary and what does not

| Counts as primary | Does not count |
|---|---|
| News/press article, read directly | A `.md` note that cites the article without a link |
| Government/regulator page or PDF | A ledger entry summarizing "what the regulator said" |
| Company SET filing, annual report, press release | An internal repo archive of an extracted filing, with no link to the filing itself |
| Academic paper (DOI/URL resolvable) | A citation to the paper's *name* with no DOI or URL |
| A source **read again, this pass** | The same source, remembered as "already checked" |

## Why "flag as unverifiable" beats "trust the prior label"

A ledger, note, or deliverable that says VERIFIED is doing exactly what it looks like it's doing —
reporting a *past* verification. Time, source changes, and simple compounding-error risk (one
agent's hallucination cited by the next agent as fact) all erode that over a session, let alone
across sessions. The cheap, correct default is: **UNVERIFIABLE until re-confirmed against an
external source in the current pass.** Downgrading by default costs a re-check; trusting by default
costs a false claim reaching a reader who cannot tell the difference.

## The incident

A source ledger tracking ~90 factual claims for a board briefing had many entries internally
labeled **VERIFIED** by earlier agentic passes — but on a restructuring pass forced to ask "does
this entry carry a clickable external URL," roughly two-thirds of the "VERIFIED" entries turned out
to cite only a named outlet ("Source: Bangkok Post") or an internal file cross-reference, with no
link a human could actually open and check. One entry had already let a stale, disproven claim
survive uncaught for this exact reason — the fix for that specific case became a project-level
rule about citation links; this rule generalizes it: the fix is not just "add a link," it's "default
to distrust of internal artifacts, no matter how confidently labeled."

## The cheap habit that prevents it

Before citing anything from a repo file, ask: *have I (or an agent, this pass) actually opened the
underlying external source and read the claim there* — not "does a file in this repo say this is
true." If the answer is no, the claim is UNVERIFIABLE, full stop, regardless of what label a prior
pass attached to it.

---

*Earned from:* a source-ledger restructuring where the majority of internally-"VERIFIED" entries
turned out to rest on named-but-unlinked outlets or internal cross-references rather than a
directly checkable external source.
