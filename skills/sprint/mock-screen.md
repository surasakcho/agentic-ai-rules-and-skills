# Mocking a screen

**The rule is [`mock-the-screen-before-you-build-it`](../../rules/coding/mock-the-screen-before-you-build-it.md).
This file is the procedure, not a replacement for it.**

**No UI is built before the owner has looked at a picture of it.** For screens that means an HTML
mockup screenshotted in a real browser — not Canva. *Canva is for brand assets; see
[`mock-brand.md`](mock-brand.md).*

## Why the browser and not a design tool

- It uses **the app's real stylesheet**, so what the owner approves is what gets built, rather than
  an impression of it that diverges the moment it is implemented.
- Nothing to log into, no third-party account, no plugin loaded into context.
- Seconds per iteration.

**The trade being made, openly: the owner cannot edit it themselves.** They can only say yes, no, or
change this. If they need to move things around with their own hands, that is the Canva lane.

## The procedure

1. **Write `mockups/<screen>.html`** — a single self-contained file. Import the app's real CSS if it
   exists. **Use realistic content, never lorem ipsum**: real titles, real names, plausible counts.
   A layout that only works with tidy placeholder text is not a layout.
2. **Render three states, not one.** Empty, typical, and overflowing. *Most UI defects live in the
   first and last, and a mockup that shows only the happy middle has hidden them.*
3. **Screenshot it headfully** and commit the PNG beside the HTML.
4. **Show the owner the PNG**, and say what it does NOT show.
5. **Only then build.**

## What the screenshot must not hide

**Say out loud, every time, what the mockup cannot tell you:** how it behaves on a phone, what
happens while data is loading, what an error looks like, whether the contrast passes, and how it
reads in the other colour scheme. **A static picture approved as though it settled these is the
whole risk of mocking.**

## Rounds

**One round, then one review.** Round two names what would make you abandon the design direction
rather than adjust it. **Pixel-nudging is the easiest displacement activity there is** — it always
feels like progress and it has no natural end.
