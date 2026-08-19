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

## Guard

- **No cutoff constants.** A `cutoff=`, `threshold=`, `ratio >` or `n=1` closest-match anywhere near
  a join is the smell.
- **No fallback chains.** `exact → fuzzy → startswith` means three different match qualities
  arriving in one column with nothing recording which. If a method label is computed, **it must be
  persisted** — a discarded label is a match quality nobody can audit.
- **Assert key uniqueness in the reference before joining**, not after.
- **A silent drop is as bad as a wrong match.** Unmatched rows must be counted, listed and returned.
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
