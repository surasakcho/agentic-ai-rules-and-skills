# Join on the code as it is — never invent or patch a key to force a match

**Task type:** data engineering — any join between tables that share an identifier.
**Related:** [`adjudicate-with-an-external-source`](adjudicate-with-an-external-source.md) — how
to decide *which* side's code is right. [`read-the-authority-never-type-the-table`](read-the-authority-never-type-the-table.md)
— a lookup table must be read, not typed; this rule says some lookup tables must not exist at
all. [`completeness-checking`](completeness-checking.md) — partitioning the misses, which is what
step 2 below actually is.

---

## The rule

**Use the codes as they are. Never invent a code, rewrite a code, or hand-author a translation
table to make a join succeed.**

A non-match is information. Patching it away destroys the information *and* keeps the bad key.

**The escalation, in order — do not skip a step, and do not take the last one alone:**

1. **Join as-is.** Both sides keep their own values. Count matches and misses, in both
   directions.
2. **If a lot is missing, question the KEYS, not the rows.** Are these actually the same code
   system — same issuing authority, same standard, same granularity, same vintage? A high miss
   rate almost never means "the data is incomplete." It means the two columns do not mean the
   same thing.
3. **If a lot is still missing after that, stop and ask. Propose; implement nothing.** A key
   mismatch is a data-definition problem. The resolution is a decision about the reference frame,
   not a patch inside one join.

## Why the patch is worse than the gap

A missing join is loud, countable and fixable. A patched join is **silent and permanent**: it
looks healthy, so nobody returns to the real problem, and the wrong key survives everywhere the
patch was not applied.

## The incident

A hand-written, undocumented 21-row table mapped `our_code -> their_code`, and existed solely to
make one join land. Tested against the **issuing authority's own roster** — the body that assigns
these codes:

| column | valid codes under the national standard |
|---|---|
| `their_code` | **21 of 21** |
| `our_code` | **1 of 21** — and that one only because an earlier defect had already corrected it |

There was no second numbering system. **There were 20 wrong codes in our reference frame**, and
the table was a list of what each should have been. The consumer applied it as
`dict(zip(their_code, our_code))` — taking the authority's *correct* value and rewriting it into
our *invalid* one so the merge would land.

**Three costs, all measured:**

- **It patched one join out of many.** One unit received its population through the table and its
  economic output **from the wrong province, 200 km away — a 17.3% error** — because every other
  stage derived the region from the first two digits of the same bad code.
- **Five of the rows collided.** Their target code was *already* a row in our frame — a separate
  polygon with **zero overlap**. One district held **11 frame rows against the authority's 10**;
  the extra one was not a national code at all. One real unit split into two rows, one carrying
  an invented code, and a single source population row covering both.
- **The "fix" made it worse.** Seeing 12 values go blank, I made the rewrite conditional so it
  skips codes already present in the frame. That did not repair a mis-seat — it changed *which
  half of a split unit* received the entire population, and left two sibling blocks from the same
  source disagreeing: **28 columns, 5 pairs, shipped.** I diagnosed from the symptom without
  reading the existing consumer or checking either column against the authority.

## The correct pattern, from the same repo

A separate module rewrote **our** codes, never the authority's, and a companion script pushed the
correction through **every** derived file. That is why exactly one row of the bad table read as
valid: it was the one already fixed properly.

**A code correction is a frame rebuild applied everywhere — not a dictionary inside one join.**

## The same failure wearing a different costume

Fuzzy name matching. Four other scripts in the same project forced joins with `difflib` instead
of a code, and produced the identical class of defect: one rural unit received the *provincial*
administration's entire budget because the name was close enough.

**If your join needs a similarity threshold or a manual override list to succeed, the key is
wrong. Fix the key or stop.**

---

*Earned from:* a hand-written 21-row crosswalk whose own column of "our" codes turned out to be
1-of-21 valid against the issuing authority, used for months to make a demographic join succeed
while the underlying frame stayed wrong — costing a 17.3% error on an unrelated variable, a split
unit whose population landed on whichever half the last edit favoured, and 28 shipped columns in
which two blocks from one source disagreed with each other.
