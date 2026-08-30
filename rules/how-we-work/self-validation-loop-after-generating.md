# Run a self-validation loop after generating an answer or code

**Task type:** agent workflow — after producing any substantive answer, document, or code
change, before presenting it as finished.
**Related:** [`record-thinking-before-complex-work`](record-thinking-before-complex-work.md) —
that rule verifies the plan before acting; this one verifies the output after acting, closing
the loop.

---

## The rule

**After generating an answer or code, run this checklist before calling the work done. If any
check fails, revise and run the checklist again — don't stop at the first pass.**

1. **Addresses all points** — does the output cover every part of what was asked, not just the
   part that was easiest or most interesting to answer?
2. **No contradictions** — does any claim, code path, or instruction in the output conflict with
   another part of it, or with something already established earlier in the task?
3. **Format matches requirements** — does the output match the structure, schema, or convention
   that was specified or implied (see
   [`propose-xml-schema-before-strict-output`](propose-xml-schema-before-strict-output.md) when
   that structure is strict)?
4. **If any check fails, revise and recheck** — a fix to one point can introduce a new
   contradiction or drop coverage of another; the loop doesn't end at the first revision, it ends
   at the first *clean* pass.

## Why a loop, not a single pass

A one-time check after generation catches the failure modes present at that moment, but a fix
for one of them can create another — tightening an answer to close a coverage gap can introduce
a contradiction with an earlier claim; correcting a format mismatch can silently drop content
that no longer fits the new structure. Treating this as a loop rather than a checklist you run
once is what catches the failure the fix itself introduced.

## Why these four checks, not a general "review it"

"Review your answer" is vague enough to skip in practice — there's no way to know when it's
done. Four named checks make the review falsifiable: each one either passes or names a specific
defect, and "all four pass" is a concrete stopping condition instead of a feeling that the answer
looks fine.

---

*Earned from:* proactive practice, no incident yet — added on user instruction rather than
extracted from a failure, consistent with
[`record-thinking-before-complex-work`](record-thinking-before-complex-work.md).
