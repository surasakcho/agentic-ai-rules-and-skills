# Propose the XML tag schema before producing strictly formatted output

**Task type:** agent workflow — any task whose output must follow a strict, machine-consumed
format (parsed by another program, another prompt, a pipeline stage).
**Related:** [`record-thinking-before-complex-work`](record-thinking-before-complex-work.md) —
the same "check the plan before spending effort on it" logic, applied to output shape instead of
task steps.

---

## The rule

**When an output must be strictly formatted, do not go straight to generating the filled
content. First draft the empty XML tag skeleton — the tag names and nesting, with no content
inside — and show it to the user. Only fill it in once the shape is confirmed.**

```xml
<review>
  <finding>
    <file></file>
    <line></line>
    <summary></summary>
  </finding>
</review>
```

## Why the skeleton, not just a description of the format

A prose description of a format ("I'll include the file, line, and summary for each finding") is
ambiguous exactly where strictness matters: nesting, repetition (is `<finding>` a list or one
block?), naming (`summary` or `description`?), and whether fields are optional. A downstream
parser doesn't care about the intent, only the actual tags — so the ambiguity that prose leaves
open is precisely the ambiguity a strict consumer can't tolerate.

An XML skeleton removes that ambiguity before either side has spent effort: the user can see and
correct `<line>` vs `<line_number>`, or a missing repeatable wrapper, in one glance — without
reading through generated content to infer the shape it implies.

## Why before, not after

Filling the skeleton in and then adjusting field names or nesting afterward means redoing the
generation, not just relabeling it — the content was produced against a shape that turns out to
be wrong. Confirming the skeleton first is the cheap version of that same fix.

## Scope

Applies when the output feeds something that will fail on the wrong shape: another prompt, a
parser, a pipeline stage, a schema-validated field. Does not apply to output meant only for a
human to read in prose — proposing a skeleton there is overhead with nothing strict to protect.

---

*Earned from:* proactive practice, no incident yet — added on user instruction rather than
extracted from a failure, consistent with
[`record-thinking-before-complex-work`](record-thinking-before-complex-work.md).
