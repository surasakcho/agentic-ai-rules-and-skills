# Review every output before handing it over

**Task type:** analytics — producing figures, tables, or numbers quoted in prose.
**Mechanised by:** [`skills/verify-outputs`](../../skills/verify-outputs/) (partly).

---

## The rule

Every artifact you produce — figure, table, or a number in a sentence — gets reviewed for
**accuracy, sanity and readability** before it reaches a reader. Producing an output is not
finishing it.

These are three separate properties and only the first one is self-evident:

- **Accuracy — recompute, don't read.** Verify a table by recomputing it from source, not
  by looking at it. Every count in a caption and every N in a table is a claim. If you also
  wrote the note describing the number, that note is a *hypothesis you wrote down*, not
  evidence.
- **Sanity — predict, then look.** Say what the output should show before you open it. Does
  the geography match known geography, the sign match theory, the magnitude match the units?
  An output that renders cleanly and says something impossible is the dangerous kind, because
  nothing complains.
- **Readability — open it and look at it.** Can the thing it exists to show actually be seen?
  Is the colour scale the right way round? Does the axis range let the signal show? And
  **does the caption match what the image actually draws?**

## The incident

A remediation produced 321 maps and 9 tables, verified them with unit tests, a completeness
audit and an acceptance gate at 26/26, and reported them as deliverables. Nobody had looked
at most of them.

**Reviewing found six distinct defects in the first fourteen figures examined**, including:

| Defect | Cost |
|---|---|
| A custom colormap that never registered (`flag` is a library builtin, so the guard `if "flag" not in colormaps` was always false) | 30 maps drawn **inverted**; the 44 units each flag existed to identify were invisible |
| A log scale masking zeros, with a transparent bad-colour | **39,829 values** rendered blank — identical to no-data — under titles reading "0 no data" |
| A fixed 0–1 colour scale applied to variables topping out at 0.449 | 9 maps using under 40% of their range, including **the study's main regressor** |
| A caption asserting a regional difference the figure's axis range could not show | The difference was real at p=5×10⁻⁹¹; the figure showed four flat lines |

Every one was invisible in the source and obvious in the image.

## Sample across mechanisms, not at random

Defects do not live in artifacts. They live in the **shared policy code** that produces them
— a colour rule, a normalisation rule, a scale rule — so one defect lands on every artifact
that policy touches, 4 to 30 at a time.

The fourteen figures were chosen to span different policies: one per colour family, one per
transform type, one per data family. **Random sampling of fourteen out of 321 would likely
have found one or two.**

## Say what you eyeballed versus what you screened

At scale, write a programmatic screen over the rendered output — see
[`verify-outputs`](../../skills/verify-outputs/) — then eyeball everything it flags plus a
mechanism-spanning sample.

Then state both numbers. **"I reviewed them" when you screened them is a false claim about
your own work.**

## Caption-versus-content is its own check

A caption that overstates, understates, or describes something the figure does not draw is a
defect of the same severity as a wrong number, **because the reader believes the caption**.
