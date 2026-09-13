# Review every output before handing it over

**Task type:** analytics — producing figures, tables, or numbers quoted in prose.
**Mechanised by:** [`skills/verify-outputs`](../../skills/verify-outputs/) (partly).
**When you realise you skipped this:** do it now, do not ask — see
[`close-your-own-gaps`](../how-we-work/close-your-own-gaps.md). The failure mode this rule
describes reappears one level up, as *"I only reviewed some of them"* offered to the reader as
a caveat instead of finished.

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

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'the count of artifacts produced against the count screened by the programmatic screen and the count actually opened; a handover message asserting the outputs were reviewed; and every caption claim against what the artifact draws'
trigger: 'pre-commit or CI on the output directory, plus Stop on the handover message'
check: 'artifacts changed and verify_outputs screen not run over them -> block; screen reports a flagged artifact that no later run cleared -> block; message asserts reviewed while the log shows screened-only -> refuse and require both numbers'
escape: 'state both numbers - screened N, eyeballed M - which is the rule prescription; a declared exemption for artifacts that are not for a reader'
implemented_by: skills/verify-outputs/
invoked_by: 'nothing in this repo - needs a pre-commit hook or a CI step in the adopting repo, and this corpus repo has no core.hooksPath and no hooks directory (checked 2026-09-13)'
narrows: 'the screen catches blank, single-colour, invisible-signal, inverted-colormap and low-ink renders. It cannot check that a caption matches its figure, that the magnitude is plausible, or that the sample eyeballed spanned mechanisms rather than being fourteen at random - all three stay prose, and the caption check is the one the incident cost most'
```
