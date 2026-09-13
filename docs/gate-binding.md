# Binding a portable rule to a local gate — the specification

**The problem in one line: a rule is portable and a gate is not, and today the corpus is the side
being asked to name the gate.**

`check_rule_gates.py` resolves a rule's `implemented_by` by looking for a declared gate identifier
**inside the rule's own text**, before falling back to path resolution. That works, and it means the
estate's private naming has to be written into a shared rule — `commit-gates: the shared-rules pin
is not stale` published to every consumer of this corpus, none of whom have that gate. So the only
expressible binding is one that should never be committed, which is why the join is empty in a
corpus where both sides are fully declared.

Measured 2026-09-13 in an estate that **does** declare its providers — 106 gates across four
providers, config passed, roots resolving:

| | |
|---|---|
| matched — a rule naming an estate gate | **0** |
| rules only | **74** of 89 |
| estate gates only | **106** of 106 |

**Every gate the estate runs is an orphan, and the config is not the missing piece.** It was already
there. The missing piece is a direction.

---

## The inversion

**The estate declares which of its gates satisfies which rule. The corpus declares nothing about
gates it cannot see.**

That is the whole change, and everything below follows from it:

- **Only the estate knows its gates.** Asking the corpus to name them is asking the side without the
  information to hold the mapping.
- **Adding an estate then requires no corpus change.** Today a second estate wanting credit for the
  same rule would have to add its own naming to the same shared file, and the two would collide.
- **Nothing private is published.** The binding file lives with the gates it names.

## The identifier: use the rule's own slug

**No new vocabulary is needed, and inventing one would be the mistake.** Every rule already has a
unique, stable, kebab-case identity — its filename without `.md` — which is portable by
construction, leaks nothing, and is already how rules refer to one another.

**Bare slug, not category-qualified — and the corpus has already proved why.** The checker displays
rules as `coding/surgical-verified-change`, so the qualified form looks like the obvious identifier.
It is the wrong one: commit `4dacbe9` folded two entire categories into `how-we-work` at **100%
rename similarity**, so every filename survived and every category path did not. **The category is
the part that has demonstrably moved; the slug is what survived it.** A qualified identifier would
have invalidated every binding written before that commit.

The cost is that slugs must stay unique across categories. They are today — 90 of 90 — and nothing
enforced it, so **the enforcement ships with this decision**: `harvest.py --check` now fails on a
duplicate rule slug, naming both paths. Proven both directions before landing.

So a binding is a statement in the estate's config:

```
# satisfies <rule-slug> <provider> <gate-id>
satisfies  retrieve-lessons-weekly                commit-gates  "the shared-rules pin is not stale"
satisfies  nothing-leaves-git-without-permission  deny-list     "Bash(git update-index:*)"
```

> ⛔ **The first row was originally written as
> `a-pinned-reference-is-checked-at-its-pin`, and that binding was false.** It was bound off
> the rule's **title** — both are about pins, so it reads right. The rule's `observable` is
> *"any reference resolver in the repo, and whether it extracts a version before resolving"*,
> and that gate inspects no resolver: it **runs** one, and asks whether this repo's recorded
> pin is stale. That is `retrieve-lessons-weekly`, which was already correctly bound to the
> same gate on the next line.
>
> **So: bind against the `observable` and `check` lines, never the headline.** A binding read
> off a title is the cheapest possible wrong row, it survives every mechanical check in this
> design, and the two rules most likely to be confused are the two whose titles rhyme.
>
> The tempting half, recorded so nobody re-binds it: that gate invokes a script whose
> link-verifier *does* resolve every link at its sha, and which refused a real commit. That
> satisfies the rule's escape clause for one artifact class. It does nothing about the rule's
> actual subject — resolvers in this repo that check a pinned reference against now — and the
> one such defect found today was found **by hand**, which is the evidence that nothing gates
> it.

**The gate-id is the id as the CHECKER ENUMERATES it, which is not always the name a human would
use.** Each provider kind yields ids differently: a `regex` provider yields its capture group, so
`"the shared-rules pin is not stale"` is correct for a `commit-gates` binding; a `py-tuple` provider
yields **the first string of each entry**, which may be a short key rather than the human-readable
description sitting beside it. Bind what the orphan list prints, not what the file reads like — the
orphan list is the authoritative enumeration, and a binding that names the description of a
`py-tuple` gate fails as *no such gate* while looking obviously right.

**Many-to-many, deliberately.** One rule may be enforced by several gates (a `PreToolUse` refusal
plus a pre-commit backstop); one gate may satisfy several rules (a deny entry covering three
adjacent prohibitions). A schema that assumed either was single would force the estate to lie about
the common case.

## What the rule side does — nothing new

A rule whose enforcement is estate-local **carries no `implemented_by` at all**, which is already
what those 74 do. `implemented_by` keeps exactly its current meaning: an implementation that ships
**inside this corpus** and travels with it. The two fields answer different questions and neither
should be stretched to cover the other:

| field | lives in | means |
|---|---|---|
| `implemented_by` | the rule | a thing in this corpus that can refuse |
| `invoked_by` | the rule | what causes that thing to run |
| `satisfies` | the **estate's** config | a local gate that enforces this rule here |

## The states the report owes

**Four, and the two that are usually collapsed are the point:**

| state | meaning |
|---|---|
| **gated here** | a binding names this rule, and the gate it names **exists in the provider inventory** |
| **bound to nothing that exists** | a binding names a gate the inventory does not contain — a **failure**, and the one this design most needs to catch, because a binding is a claim |
| **unbound** | no binding, no in-corpus implementation. The 74. |
| **not examined** | no clause at all |

**`unbound` and `not examined` must never share a value**, and neither may be reported as clean —
see [`absence-is-not-compliance`](../rules/testing/absence-is-not-compliance.md). A binding file
that has never been written produces `unbound: 89`, which is a true and useful number; a binding
file that does not exist produces *nothing*, which is not.

## The join, in the headline

Three numbers, on the summary line, per
[`count-the-join-not-the-inventories`](../rules/how-we-work/count-the-join-not-the-inventories.md):

```
rules gated here: N   rules unbound: N   gates no rule claims: N
```

**The third one is not a failure and must not be silently dropped for that reason.** A gate may
legitimately enforce something written down elsewhere or nowhere. But 106 of 106 is not a
distribution of legitimate exceptions, and the only way anyone learns that is if the number is on
the line people read.

## A binding is a claim, so it owes evidence

Per [`a-classification-is-not-a-gate`](../rules/how-we-work/a-classification-is-not-a-gate.md), a
declared control that nobody has seen refuse is a classification. So the binding accepts an optional
observation:

```
satisfies  <rule-slug>  <provider>  "<gate-id>"  observed:2026-09-13
```

**Optional on purpose.** Making evidence mandatory would make binding expensive, and an expensive
binding produces an empty binding file — which is exactly the state being fixed. Unobserved
bindings are counted and reported, never refused: the report reads `(never observed refusing)`
where the date would be.

### The one thing a binding asserts that nothing can check — and the instrument that does exist

**A binding claims that gate X enforces rule Y, and no checker can confirm that.** It confirms the
gate exists and that someone claimed the pairing. A wrong row reports green, and prose at the top of
the file is the weakest instrument available.

There is a stronger one, and it is the discharge condition this corpus already uses everywhere else:
[`validations-must-fail`](../rules/testing/validations-must-fail.md). **Make `observed` replayable
rather than asserted.** Per binding, the estate keeps the two things it must already have had to
write the row honestly:

- an **input that violates the named rule**, and
- the gate's **refusal** of it.

Then the claim is not "someone watched it once" but "this input still gets refused", and CI can
re-run it. A binding whose replay stops refusing has become false, and says so on the day the gate
changes rather than at the next audit.

**A few gates must not have their fixture written down — and far fewer than the obvious argument
suggests.**

> ⛔ **This clause was published wider than it should have been, and the narrowing came from
> checking rather than reasoning.** It read: *any gate whose violation is itself the harm*. Both
> credential gates in the estate that prompted it were nominated as the examples — and both turn out
> to have been **replayable for weeks**, 27 and 12 deny cases respectively, found by one grep of the
> test file. Nominating them from the shape of the problem instead of opening the file is the same
> error as binding a rule off its title, which is the other retraction on this page.

**The discriminator is whether a decoy exists that the predicate accepts**, not whether the real
thing is dangerous. A **pattern-matching** gate — a regex over a token shape, a path, a verb — takes
a synthetic input and stays fully replayable; its predicate cannot tell a real credential from a
shaped one, which is exactly what makes the fixture safe. `fixture-unsafe` is for the narrower case
where **no decoy the predicate accepts exists**, so provoking a refusal means performing the act.

### Assemble the violating input at runtime, never as a literal

The technique that makes credential fixtures safe, and it generalises to every gate whose trigger is
a token shape:

```python
GHP = "ghp_" + "A" * 36        # never written out as one string
```

Two consequences, and the second is the one worth the paragraph:

1. **No violating literal ever lands in a tracked file**, so the fixture obeys the gate it tests.
2. **The gate needs no self-exemption.** An exemption keyed on a path or a marker — *ignore matches
   inside `test_*.py`* — is a hole anything climbs through by naming itself accordingly, and it is
   the first thing anyone reaches for when a fixture trips its own gate.

The estate that wrote it records that the first draft used literals and **the live gate refused the
write of the test file itself.** That refusal is better evidence than the suite: it is the gate
firing on real input rather than on input shaped to please it.

Beyond pattern-matching gates, the same distinction applies — see
[`discard-secret-output-never-filter-it`](../rules/how-we-work/discard-secret-output-never-filter-it.md)
and the boundary in
[`validations-must-fail`](../rules/testing/validations-must-fail.md) for controls whose only direct
test is performing the act they prevent.

So a binding is in one of **three** evidence states, and they must be distinguishable — one date
standing in for all three is the collapse this corpus keeps finding. Trailing tokens, repeatable:

```
satisfies <slug> <provider> "<gate-id>"  fixture:<path>
satisfies <slug> <provider> "<gate-id>"  observed:<date>
satisfies <slug> <provider> "<gate-id>"  fixture-unsafe:"<reason>"
```

| token | state | checked |
|---|---|---|
| `fixture:<path>` | **replayable** — a violating input and its refusal | the path must exist under a declared root; **a fixture named and absent is a failure**, since the whole point of the strong state is that somebody can re-run it |
| `observed:<date>` | observed once | nothing — it is an assertion, and reads as one |
| `fixture-unsafe:"<reason>"` | no decoy the predicate accepts | **the reason is mandatory.** A bare marker is the classification this corpus keeps warning about |
| none | never observed refusing | — |

**An unrecognised trailing token is reported and the binding is KEPT.** The first parser accepted
only `observed:` and dropped the whole line on anything else — loud about the syntax and silent
about the consequence, which would have quietly reversed part of a join it had just moved. The
louder half is not the safer half when the quiet half is a dropped claim.

A gate marked `fixture-unsafe` is verified the way that boundary prescribes: against the predicate
as data, against a decoy, or from outside a session.

**Still optional, for the same reason as above** — a mandatory fixture per binding produces an empty
binding file. But `observed:<date>` should be read as the weak form and a replayable case as the
strong one, and the report should be able to tell them apart rather than printing one date for both.
**This is specified and not built**: nothing in the checker replays anything today.

## What this does not do

- **It cannot tell whether the named gate actually enforces the rule.** It checks that the gate
  exists and that someone claimed the pairing. Whether the claim is true is a judgement, and a wrong
  binding will report green — which is why the observation field exists and why its absence is
  counted.
- **It cannot discover bindings.** Somebody has to write them, once per gate, and the first pass
  over 106 gates is the real cost of this design. There is no way around it that does not involve
  guessing.
- **It does not make the corpus aware of any estate.** The corpus stays ignorant of every gate; the
  report is assembled at run time from a file the estate owns.

## Who owns the pair

The question [`count-the-join-not-the-inventories`](../rules/how-we-work/count-the-join-not-the-inventories.md)
leaves open — *the join needs someone whose job is the pair* — is answered by the binding file
itself. **The estate owns it, because the estate is the only party that can see both lists.** The
corpus owns the rule slugs; the estate owns the mapping; neither has to know the other's internals.

And when it has an owner, the *"never a failure"* label on the orphan list is the first thing to
revisit — an orphan is not a failure while nobody is responsible for the pairing, and becomes one
the moment somebody is.
