# When two sources disagree, go outside both

**Task type:** data engineering — reconciling a mismatch between datasets, files, or fields that
are supposed to agree.
**Related:** [`report-both-sides-of-a-comparison`](../analytics/report-both-sides-of-a-comparison.md)
— that rule is how you *report* a comparison; this is how you *settle* one.
[`completeness-checking`](completeness-checking.md) supplies the both-directions count that turns
a matched label into a matched population.

---

## The rule

**A mismatch between two datasets cannot be adjudicated by those two datasets. Reach for a third
source that neither one produced, and prefer the authority that *issues* the thing in dispute.**

The failure is quiet and feels like diligence. Source A says X, source B says Y, and you resolve it
by reasoning about A and B — which looks more internally consistent, which is newer, which the
pipeline already trusts. That is a coin flip wearing the costume of analysis.

Worse is resolving it from your own repo's prior conclusion. **That is not evidence at all**: it is
the claim you are supposed to be testing, cited back under a different filename. If a code comment
and a defect log both assert the answer, that is one source counted twice.

## Where to look, strongest first

| Source | Why it outranks the disputants |
|---|---|
| **The issuing authority** | Codes, identifiers and classifications are *assigned* by somebody — the registry that mints them, the body that publishes the standard, the agency that surveys the boundary. Their statement is not one opinion among several. |
| **A published standard, cited by number** | If the disputed field implements a named standard, the standard settles it and nothing downstream can outvote it. |
| **Independent third parties** | Meaningful only if they derived their answer separately. Two databases agreeing proves nothing if one copied the other — check for a shared upstream before counting them twice. |
| **The disputed file's own contradictions** | Files often argue against themselves: one field disagrees with a sibling field in the same record. This does not identify the truth, but it identifies *which file is unreliable* — half the answer, and free. |

## Say which tier every answer came from

Primary, secondary, tertiary — and whether you actually reached it or only found something *about*
it. A community-maintained page and a government registry are both "a source"; listing them
undifferentiated is a false claim about the strength of your evidence.

State plainly what you could not reach. **"The standard's own text is paywalled and I did not read
it" is worth more than a citation implying you did.**

## Two traps about what counts as "external"

**A source cached in your repo can still be external.** What matters is *who produced it*, not
where the bytes sit. In the incident below, the strongest evidence was a registry export sitting in
a scratch directory — external to the agency under suspicion, and decisive.

**A source that looks independent may not be.** One candidate had to be discarded mid-check on
discovering that its "independent" identifier column was a reformatting of the very code in
dispute. It contributed nothing and had to be dropped from the tally rather than counted. Verify
provenance before you count a source, not after.

## Reconcile populations, not just the disputed value

Agreement on the label is not enough. Once you have the third source, count both sides. Two
independent sources landing on the same *total* is far stronger than one matched value — and if the
totals disagree while the labels match, the real defect is somewhere you were not looking.

## The incident

Two boundary files from one agency disagreed about which administrative area a numeric code
belonged to. I reported the answer confidently. Asked how I had confirmed it, the honest answer was
that I had not: I had read it from a comment in this project's own code and from its own defect
log — the same claim twice, presented as corroboration.

The real check took minutes:

1. **The file argued against itself.** Its name field and all sixty of its own composite
   identifiers pointed one way; a single code field pointed the other. That established which file
   was unreliable.
2. **The issuing registry** — an authority independent of the agency that produced both files —
   gave the mapping directly.
3. **An international standard and the corresponding national standard** confirmed it from outside
   the country's own administrative apparatus.
4. **Both populations reconciled exactly** against the registry: the two areas' item counts matched
   the built frame with zero on either side.

Four sources, independent of the file under suspicion and largely of each other. The original two
"sources" were one.

**And the check paid for itself.** The same investigation, run properly, found that the project's
canonical frame was silently *fusing two distinct entities into one row* wherever an identifier
field collided — deleting two real entities from the study frame and doubling the recorded area of
the two rows that absorbed them. That defect had been invisible for as long as the mismatch had
been resolved by assertion.

---

*Earned from:* resolving a disagreement between two files from one agency by citing the project's
own comment and defect log — the same claim counted as two sources — when a registry, a standard,
and the file's own internal contradiction were all minutes away.
