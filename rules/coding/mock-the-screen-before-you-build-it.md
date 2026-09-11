# Mock the screen before you build it

**Task type:** coding — any user-facing screen, layout or flow, before implementation starts.
**Related:** [`write-the-prd-before-the-code`](write-the-prd-before-the-code.md) — the same
discipline for behaviour; this is its visual half and neither substitutes for the other.
[`a-gate-that-fires-at-commit-time-is-not-a-gate`](a-gate-that-fires-at-commit-time-is-not-a-gate.md)
— why "show the owner a picture" must happen before the build, not at review.

---

## The rule

> **No UI is built before the owner has looked at a picture of it.**
>
> **Screens are mocked in a real browser. Brand assets are mocked in a design tool.** Two lanes,
> and the split is deliberate.

## Why a browser and not a design tool, for screens

- **It uses the application's real stylesheet**, so what the owner approves is what gets built,
  rather than an impression of it that diverges the moment someone implements it.
- **Nothing to log into**, no account, no plugin loaded into every session's context.
- **Seconds per iteration.**

**The trade, stated openly: the owner cannot edit it themselves.** They can say yes, no, or change
this. **That is exactly why the other lane exists** — a logo, a social image or a store banner
outlives any one session and the owner will want to adjust it without asking anyone. **Design tool
there; browser for screens.**

*A rule that names one tool for both lanes will be wrong for one of them. Name the lanes.*

## Three states, not one

**Empty, typical, and overflowing.** Most layout defects live in the first and last, and a mockup
showing only the comfortable middle has hidden them rather than tested them. **Use realistic
content, never placeholder text** — a layout that works only with tidy filler is not a layout.

## Say what the picture cannot tell you

Every time, out loud: **how it behaves on a small screen, what it looks like while loading, what an
error state shows, whether contrast passes, how it reads in the other colour scheme.**

**A static image approved as though it settled those questions is the entire risk of mocking.** The
approval is real for what was shown and worthless for what was not.

## Rounds

**One round, then one review.** Round two names what would make you abandon the design direction
rather than adjust it.

**Pixel-nudging is the purest displacement activity available to a builder** — it always feels like
progress, every individual change is defensible, and it has no natural end. A mockup stage with no
stop condition does not protect the build; it replaces it.

## Guard

- **Commit the picture next to the code.** An approval nobody can find later did not happen.
- **The three states are not optional.** If only one was rendered, say which.
- **Producing an asset is not publishing it.** Keep those steps separate and never let one imply the
  other.

---

*Earned from:* an operator directive on 2026-09-11 that all visual and UX work be mocked before
development. The tool split came out of grilling the instruction rather than executing it as
stated — the named tool was right for brand assets and wrong for application screens.
