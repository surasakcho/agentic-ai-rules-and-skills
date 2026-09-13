# Detecting it afterwards is not preventing it — that trade needs the act to be reversible AND visible

**Task type:** testing — designing controls, and deciding where one sits. Also any governance
arrangement that substitutes review for refusal.
**Related:**
[`a-gate-that-fires-at-commit-time-is-not-a-gate`](../coding/a-gate-that-fires-at-commit-time-is-not-a-gate.md)
— the same trade one notch earlier: a control that catches the work *landing* has already paid for
the work. This rule asks the harder question of whether catching it at all is enough.
[`absence-is-not-compliance`](absence-is-not-compliance.md) — what an auditor with no channel
reports, which is nothing, which reads as clean.
[`a-verb-list-is-not-a-boundary`](a-verb-list-is-not-a-boundary.md) — removing the capability beats
declaring the rule, and the silent-accommodation section is this rule's observability half.
[`a-check-that-shares-a-source-is-not-a-check`](a-check-that-shares-a-source-is-not-a-check.md) —
an auditor holding the file that constrains it is this failure at the governance layer.

---

## The rule

> **Replacing a refusal with a review is a real and often correct trade — but it is only sound when
> the act is BOTH reversible and visible.** Reversible, so the reviewer can restore the position.
> Visible, so the reviewer knows to look. Lose either and after-the-fact review is not a weaker
> control; it is a **record of the thing having happened.**

Both halves are load-bearing and they fail in different ways:

| property lost | what the reviewer can do | what the control has become |
|---|---|---|
| **reversible** | sees it, cannot undo it | a notification |
| **visible** | could undo it, never learns of it | nothing at all |
| both | — | a belief |

## Irreversibility is the half everybody names

It is the easier half, and the list is short and knowable: a secret printed, a message sent, a page
published, a credential moved, a force-push over unpushed work, a delete with no copy. **For these,
the reviewer arrives to confirm it already happened.** No amount of review speed helps — the
distance between detection and prevention is not latency, it is that the position cannot be
restored.

## Visibility is the half that is assumed, and it is usually the one that is missing

**A control that depends on the reviewer learning of the act is only as good as the channel that
tells them** — and that channel is normally nobody's job to build, because the act it reports is
one nobody expects to happen.

Three measurements from one estate, one day, all of the same shape:

> **A guard refused four correct commands.** Every refusal was handled properly — the refused party
> adapted and moved on, bypassing nothing. **None of the four left a record anywhere.** They reached
> the office that owned the guard because three offices happened to be talking to each other that
> afternoon. The false-positive rate of that guard was, and had always been, unmeasured — and
> "no complaints" was a statement about the absence of a mailbox.

> **A corpus reported 8 controls as in place.** All 8 named real files that existed. **Nothing
> invoked any of them:** no hooks path, no hooks directory. The report was accurate about existence
> and silent about invocation, which is the only property that mattered.

> **An auditing body was created with a charter forbidding it from being altered by the party it
> audits — in a repository that party owns and can rewrite.** The charter says so in its own text.
> Declared, not structural: the constraint is a sentence inside the thing it constrains.

### The worst case: the act that hides itself, in one move

The visibility failures above assume a **separate** concealment — something happened, and nobody
was told. The hardest case has no second step: **the self-interested action is itself the removal
of the instrument that would have seen it.**

> **Incident.** A published false-refusal rate turned out to have a denominator the measured party
> controlled. Suppressing one true configuration change would have protected the number — quietly,
> unaudited, and defensibly. **The same suppression would also have kept the gate silent**, because
> the configuration was what gave the gate anything to look at. The self-interested move buys a
> clean number *and* a quiet instrument, in one act, leaving nothing afterwards to find.

**Audit cannot reach this, and not because the auditor is weak.** There is no concealment to detect
and no altered record to compare: the artifact is a system that legitimately had nothing to report.
An auditor arriving later sees a clean instrument and a clean number, both true.

So this is the case that decides where a control goes rather than how good the review is. **When the
action that benefits someone is the same action that blinds the check, the control has to sit before
the act or in someone else's hands** — the first two rungs of the ladder below, never the third.
And the tell is available in advance, which is the only good news here: ask **whose configuration
decides what this instrument can see**, and if the answer is *the party it measures*, the
after-the-fact half is already spent.

## The sound version of the trade

Review is not second-best. It is the right instrument for the large class of acts that are
recoverable, and it costs far less than a gate that has to be correct in advance. **Make the trade
deliberately, and make it in this order:**

1. **Remove the capability** where the act is irreversible and the actor never needs it. Nothing to
   review, nothing to detect.
2. **Refuse before the fact** where the act is irreversible and the actor does need it sometimes.
   The refusal is the control; the review is the audit of the refusals.
3. **Review afterwards** where the act is recoverable — **and build the channel in the same change
   as the review.** An auditor is created with its inputs, or it is created with a claim.
4. **Never leave a detect-only control over an irreversible act.** That pairing is not a weak
   control; it is the absence of one, wearing a control's name.

## Guard

- **Name the two properties for every control you place, out loud.** *Is this act reversible? Will
  the reviewer learn of it without anyone choosing to tell them?* Two questions, both cheap, and the
  second is the one that gets skipped.
- **Build the channel with the reviewer, never after.** A review body with no feed measures its own
  silence — and silence is the reading everyone prefers.
- **Distinguish declared from structural, and write down which one you have.** A constraint the
  constrained party can edit is declared. That is not worthless, and it is not a control.
- **When you carve out exceptions to "carry out the order", carve on both properties.** An
  irreversible-only carve-out leaves every silent act inside the obedience, and silent acts are the
  ones no audit recovers.
- **An auditor that has never reported anything is not evidence of a clean estate.** It is an
  untested instrument, and the discharge condition is the same as any other: it has to have been
  seen firing.

---

*Earned from:* a governance change that replaced refusal-and-escalation with carry-it-out-and-audit,
and the carve-out argued alongside it — that an irreversible act stays refusable. The carve-out is
right and was drawn on one property. Written the same day as three measured instances of the second:
four false refusals that left no record and surfaced only because three parties happened to compare
notes, a corpus reporting 8 controls in place with 0 of them invoked by anything, and an auditing
body whose charter forbidding interference lives in a repository the audited party owns.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'the declared control inventory: each control tagged prevent or detect, each governed act tagged reversible or irreversible, and for every detect-only control the named channel that carries the act to the reviewer'
trigger: 'CI over the control inventory, and review at the moment a control is added or relocated'
check: 'a detect-only control over an act tagged irreversible -> fail; a detect-only control with no named channel -> fail; a control declared prevent whose clause carries no invoked_by -> fail; a reviewing body with zero findings since creation -> report the count and the age, never a colour'
escape: 'an act genuinely recoverable is tagged so, with the recovery method named - naming it is the check, since a recovery nobody has written down is a belief about a recovery'
narrows: 'gates the PAIRING once both facts are declared. It cannot decide whether an act is reversible - that is the judgement the rule exists to force, and a wrong tag passes every predicate here. Nor can it see a control that was never declared at all, which is the commonest way an estate has fewer controls than it thinks'
```
