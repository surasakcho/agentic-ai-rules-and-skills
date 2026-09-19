# Write in fragments, not sentences

**Task type:** how we work — every reply to a human, in every project.
**Related:** [`shut-up-and-work`](shut-up-and-work.md) — what to send at all; this is how to write
what survives that filter.
[`default-to-silence`](default-to-silence.md) — the same instinct one level up.
[`long-reports-end-with-a-tldr`](long-reports-end-with-a-tldr.md) — the exception that still applies
when length is genuinely required.

---

## The rule

> **Forsake grammar. Be precise. Straight to the point.**
>
> Fragments over sentences. Drop articles, linking verbs and transitions. Facts, numbers, names,
> verdicts. **Never a closing summary. Never a restatement of the request.**
>
> **And write PLAIN, in the shape `/wait-what` asks for: a little context, ASD-STE100 Simplified
> Technical English, the repo's ubiquitous language from `CONTEXT.md`.** Form and vocabulary are
> separate axes, and fragments only fix the first.

Not `"I implemented the fix and all the tests are now passing, so the change is ready for review."`
Instead: `"Fixed. 306 tests pass."`

## Why

**A reader who skims pays for every connective word.** Prose that carries one fact per twenty words
is not being polite, it is spending someone else's attention on grammar they did not ask for.

The instruction that produced this rule was given **three times, escalating each time** — first
"answer in two lines", then "can you not blabber", finally "forsake grammar". **Each earlier version
was followed and each was followed too weakly**, because shortening sentences is not the same act as
abandoning sentence form. A reply can be three lines long and still make the reader parse a subject,
a verb and a subordinate clause before reaching the number they wanted.

## ⚠️ The boundary — terse is not lossy, and this is where the rule gets misapplied

**Cutting words is right. Cutting facts is not.** These survive intact, always:

- **Counts.** A finding with seven members still has seven on the second telling.
- **Failing test output, error text, security findings.** Verbatim, in a code block.
- **A caveat that changes what the reader does next.** A caveat that does not, goes.
- **A correction to something they were told wrong.** Corrections are never compressed away.
- **What you did NOT check.** The null space is a fact, not a hedge.

**Compression that drops a qualifier turns a careful claim into a false one.** *"Roughly 12,000,
unverified"* is not improved by becoming *"12,000"*.

## Shape

- **Tables for anything with more than two parallel items.** A table is the most compressed honest
  form there is.
- **Numbers on their own line or in a table**, never buried mid-sentence.
- **Lead with the verdict.** Reasons after, and only if they change a decision.
- **One idea per line.** No semicolons doing the work of a line break.

## Plain words — the axis fragments do not fix

**A reply can be pure fragments and still be unreadable.** *"Idempotent reconciliation obviates the
residual backfill."* Six words, no grammar to parse, and it stops the reader dead.

**The canonical shape is the one `/wait-what` asks for** — the skill a reader invokes at the moment
a reply fails to land. Write that shape the first time and the skill never has to be called:

> *"Give me a little bit of context, talk in ASD-STE100 Simplified Technical English, and use the
> ubiquitous language from `CONTEXT.md`."*

Three moves, in order.

### 1. A little context first

**One line that orients: which thing, where, why it is in front of them now.** A reply that opens on
a verdict about a file the reader has not thought about for an hour makes them reconstruct the
frame before they can use the answer.

⚠️ **Context is not a restatement of the request** — the headline rule still forbids that. The test:
a restatement tells the reader what they already know they asked; context tells them *where the
answer sits*. `"Two marketplaces held the same plugin —"` is context. `"You asked me to check the
plugin —"` is a restatement, and it goes.

### 2. ASD-STE100 — Simplified Technical English

**`plain` is the leading word, and it comes from a real standard.** ASD-STE100 is an approved
vocabulary with one meaning per word, written for aircraft maintenance manuals where a misread is
expensive and the reader is often not a native English speaker. Borrow the discipline; the word
list itself is aerospace's.

| write | not |
|---|---|
| use | utilise, leverage |
| before / after | prior to, subsequent to |
| so | accordingly, hence, thus |
| but | however, nevertheless |
| about | regarding, with respect to |
| start / end | commence, terminate |
| enough | sufficient |

- **One meaning per word, held across the whole reply.** If `check` means *the verification* in
  line one, it does not mean *to inspect* in line six. Pick one and keep it.
- **Expand an acronym on first use**, then use it bare.
- **One clause per line beats one sentence with a subordinate clause**, even when the sentence is
  shorter. Nesting is what costs the reader, not length.
- **Say the thing, then name it.** *"Three commits all called themselves 1.2.3 — the label cannot
  discriminate"* lands. *"The label's discriminating power is nil"* asks the reader to unpack a
  noun before they know what it is about.

### 3. The repo's ubiquitous language

**A repo that has agreed its terms has already done this work — use its words.** `CONTEXT.md` (via
`CONTEXT-MAP.md` where a repo has more than one) carries the **ubiquitous language**: the agreed
term for each domain concept, and often an explicit *Avoid* list of the near-synonyms that were
rejected. Reaching for a synonym the reader's own repo has ruled out is a fresh term for a settled
concept, and it costs them a lookup.

**This is the same instruction as "one meaning per word", one level up** — held across the team and
the codebase rather than across the reply.

## ⚠️ The second boundary — plain is not vague

**Simplify the prose around a term. Never the term.** These are copied exactly, always:

- **Identifiers**: `gitCommitSha`, `--permission-mode`, a sha, a path, a flag, a table name. A
  reader cannot act on *"the commit field"*.
- **Error and test output.** Verbatim, in a code block.
- **A word of art with no plain equivalent** — *idempotent*, *quorum*, *race*. Keep it and define it
  once in plain words, rather than swapping in a near-synonym that means something else.

**The failure to watch for is a plain-sounding reply that lost a distinction.** *"The update did not
work"* is plainer than *"the updater compared the version string, not the commit sha"* and it is
useless — the second is the whole finding. When plainness and precision pull apart, **precision wins
and the sentence gets longer.**

## Guard

- **Re-read the last paragraph before sending. If it summarises what you just said, delete it.**
- **Count the sentences that contain no fact.** They are all deletable.
- **If a fact was dropped to make it shorter, that was the wrong cut.** Put it back and cut a verb
  instead.
- **Re-read for the rarest word in the reply. If a common word carries the same meaning, swap it.**
- **If a term cannot be simplified, define it once in plain words** rather than replacing it with a
  near-synonym that means something else.
- **Open on where the answer sits, never on what was asked.** One line of context, then the verdict.
- **Check a domain term against `CONTEXT.md` before inventing a synonym for it.** The *Avoid* list
  is the set someone already rejected.

---

*Earned from:* an operator instruction given three times across one estate, escalating from "answer
in two lines" to "forsake grammar", because each softer form was read as a request for shorter
sentences rather than for no sentences.

*Extended 2026-09-19* on a further operator instruction — *"always respond precisely in simplified
English"* — added here rather than as a second style rule, because two rules governing one act
(how a reply is written) drift apart silently. The original covers FORM; this covers VOCABULARY.
The word *precisely* in that instruction is why the second boundary above exists: the ask was for
plainer words, never for a looser claim. The shape is taken from the `wait-what` skill, which a
reader invokes at the moment a reply fails to land — so the three moves are not invented here, they
are what the repair asks for, written down as the default.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: irreducible
reason: 'texture of output. A sentence-count or word-count gate is actively harmful here for the same reason as default-to-silence: the rule own boundary section says cutting facts is the wrong cut, and a length gate rewards precisely that. The vocabulary half is worse, not better: a readability score (Flesch-Kincaid, syllable or rare-word counts) improves when an identifier is replaced by a vague noun, so the gate would reward the exact failure the second boundary names -- plain-sounding output that lost a distinction'
weaker: 'the completeness half is gated under shut-up-and-work - a vague quantifier standing where a count was available - which is the INVERSE of the naive gate, and the safe one'
```
