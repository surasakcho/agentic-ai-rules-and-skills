# Match exactly, on a complete key — and hand back the unmatched

**Task type:** data engineering — every join between a source and a reference frame.
**Related:** [`never-patch-a-key-to-force-a-join`](never-patch-a-key-to-force-a-join.md) — don't
*rewrite* the key. This one: don't *loosen* the comparison, and don't leave the key half-specified.
[`never-reseat-a-value-silently`](never-reseat-a-value-silently.md) — what a wrong match does once
it lands.
[`completeness-checking`](completeness-checking.md) — how to partition the unmatched list.

---

## The rule

**Join only on exact equality of a complete key.** No similarity threshold, no fuzzy ratio, no
`startswith`, no substring, no "closest candidate", no cascading fallback chain.

**And every row that does not match is a deliverable, not a problem to route around.** Collect it,
diagnose it, and bring it back with a proposed decision. Never drop it, never approximate it,
never let a fallback quietly absorb it.

## Two ways a join goes wrong, and the second is worse

### 1. The comparison is loosened

A similarity ratio **cannot distinguish a typo from a different place whose name contains this
one.** Both score high; only the first is a match.

> `"CITY"` vs `"OLD CITY"` — ratio 0.82, clears a 0.8 cutoff, and put a city government's entire
> budget on a rural unit 60 km away.

Every threshold you pick has this property. Raising the cutoff trades false matches for silent
drops; there is no value that separates the two cases, because **the ratio is not measuring the
thing you care about.**

### 2. The key is incomplete — and this one survives every fuzzy-matching fix

Here is the number that matters. In a name-seated join audited across eight years, **~154 rows per
year landed on the wrong administrative unit. Only 11 came from fuzzy matching. The other 142 were
exact matches.**

The candidate pool was keyed on `(region, unit_name)`. The source's own `district` column was
parsed, held in memory, and **never used as a constraint** — while **133 of 7,108
`(region, unit_name)` pairs in the reference registry span 2 to 5 different districts**, one of
them 5. The resolver returned `candidates[0]`.

**Exactness does not save an under-specified key**, and this failure is more dangerous than
fuzziness precisely because it looks rigorous: the log says `exact`, the reviewer relaxes, and
every guard aimed at the fuzzy path — cutoffs, length checks, edit distance — is irrelevant to it.

**Before trusting an exact match, prove the key is unique in the reference.** One `groupby(key)`
with a `nunique()` on the discriminating field answers it. If the key is ambiguous, either add the
field that disambiguates — it is usually already sitting in the source row — or the match is
undecidable and belongs in the unmatched list.

## Unmatched is an output, with a shape

Do not report a count. Produce one row per unmatched item, each carrying a **proposed decision** and
the evidence for it:

| label | meaning | what to prove |
|---|---|---|
| `EXACT_MATCH_EXISTS` | matches once the full key is used | show the completed key |
| `SOURCE_TYPO` | clear typo of exactly one candidate **within the same parent unit** | both spellings, edit distance |
| `FRAME_NAME_CORRUPT` | our reference is wrong, not the source | the authority's spelling, keyed on code |
| `NOT_IN_FRAME` | genuinely absent | the parent's full child list, ours vs the authority's |
| `AMBIGUOUS_NEEDS_USER` | two or more equally plausible | list them all — **do not pick** |
| `NOT_A_UNIT_OF_THIS_KIND` | the row has no counterpart by definition | why |

**`AMBIGUOUS_NEEDS_USER` is the whole point of the taxonomy.** Everything else you can settle with
evidence; that one you may not, and a fuzzy matcher's entire purpose was to answer it silently.

## The degenerate case: no join at all, rendered as a resolved one

**Every guard below presupposes that a join exists** and asks whether it was loosened,
under-keyed, or silently dropping. The commonest member of this family is the one where **there is
no join to inspect** — a value read from one vocabulary, printed in a column whose *heading*
promises resolution against another.

> **Incident.** A report listed each repository with an **owner** — who to hand the work to. The
> value was read out of each repo's own declaration file. It is only actionable if the launcher's
> config declares it, because that config is what actually starts a session. **The two were never
> joined.** Measured over the 12 repositories carrying a declaration: **3 resolve, 9 do not.** Nine
> rows had shipped that morning naming an owner the launcher refuses.
>
> Underneath it, three vocabularies name one identity and **no two of the three agree** — the
> declaring file, the launcher's config, and the live registrations a peer actually sees. The
> divergence is total, not marginal, so nothing about the printed value looks wrong.

**Re-reading the function finds nothing, and that is the diagnostic.** The three lines that read the
file are correct. There is no `merge`, no `cutoff=`, no candidate selection — nothing for a reviewer
or a lint to bind against. **The defect is at the call site**, in the gap between what the label
promises and what the code did.

**So the tell is the heading, not the code: a column name is a claim about provenance.** `owner`,
`assignee`, `handler`, `status`, `link` each promise a value resolvable in the vocabulary of
whoever will act on it. If the code only *read* it, the heading is asserting a resolution that never
happened — and the reader has no way to see that, because an unresolvable name and a resolvable one
are the same string.

**The repair is the family's:** resolve into the acting vocabulary, or mark the value
`UNKNOWN(<what was read>)` — and keep *"the source could not be read"* distinct from *"the name is
not there"*, because condemning every row when the reference file is unreadable is the opposite
error and costs the same trust. See
[`absence-is-not-compliance`](../testing/absence-is-not-compliance.md).

## Guard

- **Before printing a value under a heading that implies resolution, name the vocabulary the reader
  will act in — and resolve into it, or mark it unresolved.** The question is not "is this value
  correct" but "correct *where*". A single-vocabulary read rendered as a resolved reference is this
  rule's most common failure and the only one with no join to review.
- **No cutoff constants.** A `cutoff=`, `threshold=`, `ratio >` or `n=1` closest-match anywhere near
  a join is the smell.
- **No fallback chains.** `exact → fuzzy → startswith` means three different match qualities
  arriving in one column with nothing recording which. If a method label is computed, **it must be
  persisted** — a discarded label is a match quality nobody can audit.
- **Assert key uniqueness in the reference before joining**, not after.
- **A silent drop is as bad as a wrong match.** Unmatched rows must be counted, listed and returned.
  When the join feeds a *status*, a dropped row does not read as missing — it reads as the
  **default state**, and that reading is indistinguishable from a true one. Reported from a live
  estate: a monitor joined running sessions to a declared roster on exact equality and dropped the
  misses, so a known naming drift would have rendered every staffed unit as *running, nobody
  aboard* — identical to a genuinely idle one. Fixed by publishing the misses, **not** by loosening
  the join, because a fuzzy match would have concealed a real misconfiguration. See
  [`absence-is-not-compliance`](../testing/absence-is-not-compliance.md).
- **Put the matcher in one place.** A guard added in the *caller* protects that caller only — one
  project had a length guard in one consumer and not in two siblings calling the same helper.

---

*Earned from:* a name-seated revenue join audited over eight fiscal years. ~154 rows per year seated
on the wrong district — **142 of them exact matches on an under-specified key**, 133 ambiguous pairs
in the registry, and `candidates[0]` chosen silently. 357 published rows (2.16%) and 1.38% of the
money sat on the wrong unit; 128 units also received their correct row, so the two were **summed**
and the total silently inflated. A sibling script placed 56 of 276 city locations by the same
fuzzy helper — without the length guard the first had — and 24.6% of all units took their distance
measurement from one of those cities.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: interposed
observable: 'fuzzy-matching symbols near a join - difflib, get_close_matches, cutoff=, threshold=, a ratio comparison, startswith or a substring test used to select a candidate - and any merge with no preceding assertion that the join key is unique in the reference'
trigger: 'PreToolUse(Write/Edit) on code paths, with a pre-commit backstop'
check: 'a fuzzy-match symbol within N lines of a merge or join call -> deny; a merge whose key has no preceding uniqueness assertion on the reference -> block; a computed match-method label that is never persisted to the output -> block'
escape: 'declare a non-join use of the same helper; a key proven unique by the assertion the gate demands'
narrows: 'the incident measured 142 of 154 wrong seats as EXACT matches on an under-specified key, so the fuzzy half of this gate addresses the minority case. The uniqueness assertion is the half that covers the majority, and it can be compelled to exist but not to name the right discriminating field'
```
