# Always come up with sanity-check test cases, and hand-trace a few

**Task type:** coding — writing or changing logic, before calling it done.
**Related:** [`surgical-verified-change`](surgical-verified-change.md) — turning "add
validation" into "write tests, then make them pass" is the same discipline this rule specifies
further. [`self-validation-loop-after-generating`](../agent-workflow/self-validation-loop-after-generating.md)
— that loop checks the *output*; this rule checks the *logic* the output came from.

---

## The rule

**For any non-trivial piece of logic, come up with sanity-check test cases before treating it as
done — not just the happy path, but edge cases and inputs likely to break it. Then take a few of
those cases and manually trace the logic against the code's actual output, by hand, rather than
only trusting that the tests passed.**

## Why a test suite passing isn't the whole check

A green test suite proves the code satisfies the tests you wrote — it doesn't prove the tests
were the right ones, or that you understood the logic correctly when you wrote both the code and
the tests to match each other. Tests written by the same reasoning that produced the bug tend to
encode the same blind spot. **Manually tracing a few sample cases against the actual output is a
check on the tests themselves**, not a repeat of what the tests already do.

## What "sanity-check" cases means

- Typical input — the case the code is obviously meant to handle.
- Boundary values — empty, zero, one, the max, the min, one past the max.
- The case that's likely to break it — a duplicate key, an out-of-order timestamp, a partial
  match, a value the type system allows but the domain doesn't.

## What "manually sample and trace" means

Pick a few of those cases — not all of them — and work out by hand (or by inspection, without
running the full test harness) what the correct output should be. Then compare that against what
the code actually produces for that exact input. This is slower per case than running a test
suite, which is exactly why it's reserved for a *sample*: it catches the case where the code and
the automated check agree with each other but both disagree with reality.

---

*Earned from:* proactive practice, no incident yet — added on user instruction rather than
extracted from a failure, consistent with
[`record-thinking-before-complex-work`](../agent-workflow/record-thinking-before-complex-work.md).
