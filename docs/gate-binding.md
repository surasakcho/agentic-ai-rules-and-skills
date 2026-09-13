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
satisfies  a-pinned-reference-is-checked-at-its-pin  commit-gates  "the shared-rules pin is not stale"
satisfies  nothing-leaves-git-without-permission     deny-list     "Bash(git update-index:*)"
```

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
