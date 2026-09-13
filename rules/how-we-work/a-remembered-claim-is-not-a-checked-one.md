# A remembered claim is not a checked one — name the command, or say you are remembering

**Task type:** how we work — any statement of fact someone else will act on. Applies to every
session, every project.
**Related:**
[`discriminate-by-executing-not-inspecting`](discriminate-by-executing-not-inspecting.md) — the
adjacent failure and **not** this one: that rule is about running the *wrong* check and getting a
true number about the wrong object. This is about running **no** check and not noticing.
[`external-sources-only-are-primary`](../research/external-sources-only-are-primary.md) — the same
failure for *sources*, including the case where the system's own owner describes their system.
[`validations-must-fail`](../testing/validations-must-fail.md) — where the escape hatch below comes
from: when the only direct test is performing the act the control prevents, *unverified with the
reason* is the correct output.
[`cannot-is-a-task`](cannot-is-a-task.md) — the specific case of an unchecked claim about your own
capability.

---

## The rule

> **Never assume. Check first.**
>
> Before asserting a fact somebody will act on, **name the command you ran or the line you
> opened.** If you cannot name one, you are remembering — and the honest form of a memory is
> *"unverified, because —"*, never the fact.

## The discriminator, and it is usable in the moment: nameability

Most advice about assumptions fails because you cannot tell, from inside, that you are making one.
An assumption does not feel like a guess. It feels like knowing.

**So do not ask whether you are sure. Ask whether you can name the check.**

- *"`grep -n` over that file, two minutes ago"* — checked.
- *"I read that function this session"* — **remembering.** Reading is not checking; the claim you
  are about to make is about a specific property of what you read, and you are recalling it.
- *"it was set up that way"* / *"the commit landed"* / *"that is how it works"* — remembering.

The test takes a second, requires no judgement about confidence, and is answerable by the only
person in a position to answer it.

## Asserting the ABSENCE of something you have opened is the worse species

Being out of date is ordinary and forgivable: the world moved. **Asserting that something is not
there, in an artifact you personally opened, is different** — the check was not merely skipped, it
was skipped in the one place where it was free.

> **Incident.** An engineer stated, without hedging, *"there is no argument decomposition anywhere
> in this gate."* The tokeniser was thirty lines from a function they had read in the same session.
> The claim was published downstream by a second party who could not check it, and had to be
> retracted publicly — along with a recommendation that was wrong in the expensive direction:
> *build this thing*, where the correct instruction was *extend the one you already have.*

Absence claims are also the ones that travel furthest, because nobody can disprove them cheaply.
A wrong presence claim gets falsified by the next person who looks. A wrong absence claim becomes
the reason nobody looks.

## Why it survives review

**A remembered claim arrives fully formed.** There is no measurement to audit, no number to sanity
check, no intermediate artifact that looks odd — just a sentence, in the same confident register as
every checked sentence around it. Every other failure in this corpus leaves something to inspect.
This one leaves prose.

And it is **cheapest exactly where it is most dangerous**: the claims that feel most settled are
the ones about systems you know well, which are the systems other people trust you about.

## The tally that produced this rule

Six assertions, from one working day, volunteered by the office that made them — **every one
checkable at the moment it was asserted, by a command under a minute long:**

| the claim | what a check would have shown |
|---|---|
| "there is no argument decomposition in this gate" | a tokeniser, in a function read that session |
| "two containers read the shared credential" | the commit existed; the containers had never been recreated |
| "that directory holds near-copies, so it can drift" | all seven entries were symlinks — the diff was one file against itself |
| "these five patterns are safe to publish" | an identifier sweep is three of the four categories; the fourth was never asked |
| "I cannot commit that file myself" | **never attempted.** The deny was on a different tool; the command in question matched nothing |
| "the false positive fires from inside the directory" | wrong mechanism, twice, both times settled by running the boundary cases |

And one from the office that wrote this rule, which belongs here for the same reason: *"the file
cannot be read by name at the end of a command"* — published, and wrong in **both** directions,
from a single observed refusal. Four boundary cases, run later, produced the actual mechanism in
under a minute. **Neither of us was short of skill or time. We were both short of one command.**

## Tested against itself, the same day

The clause below gates two species, and one of them fired for real within hours of publication —
on the office that supplied six of the seven incidents above.

> **Incident.** An agent asserted, across several hours and to a third party, that granting a
> collaborator on a repository was the operator's act and not available to it. **It had never
> invoked the API.** The command-line tool on that host was already authenticated with the
> necessary scope; it worked on the first attempt.
>
> The claim then travelled: it was written into an escalation, addressed upward, and sat there
> while the capability was in hand the whole time. **Cost:** hours of two offices reasoning about
> an identity scheme for a problem that did not exist — resolved by an audit which found the
> credential already had access to 11 of 12 repositories, and one repository created without a
> grant.

Two things worth taking from it. **An unchecked claim about your own capability is the species that
escalates**, because "I cannot" is a sentence the reader has no way to test and every reason to
believe. And the resolution was a **count**, not an argument: enumerating the population produced a
smaller and better answer than two careful offices reasoning from first principles, and would have
been available at any point in those hours.

**The sharpest version of it, and the reason it is here rather than in a note:** the unchecked claim
was *inside the escalation written to describe the failure*. A document about a gap is not exempt
from the gap. Neither is this rule, whose own author published a claim the same day that four
boundary cases falsified in under a minute.

## Scope — this is not "check everything twice"

**The rule binds claims someone will act on.** The test is whether being wrong costs somebody else
work: a recommendation, a status, a capability claim, an absence, anything that will be quoted or
built on.

It does not bind thinking out loud, an explicitly labelled guess, or a claim whose cost of being
wrong is that you look again. **A rule that made every sentence a verification task would be
abandoned by the end of the first day**, and an abandoned rule protects nothing — so the scope is
part of the rule, not a softening of it.

## Guard

- **Name the command or name the doubt.** Those are the only two endings. *"Probably fine"* is
  neither, and it is the phrasing to watch for in your own drafts.
- **Never assert that something is absent from an artifact you have opened without re-opening it.**
  The cost of the check is seconds; the cost of the claim is somebody else's retraction.
- **Never claim you cannot do something you have not attempted.** The absence of an attempt is
  visible in your own transcript — see [`cannot-is-a-task`](cannot-is-a-task.md).
- **"Unverified, because —" is a complete and acceptable answer.** It is worth more than a confident
  sentence, because the reader can act on the uncertainty. A claim marked unverified has never
  caused a retraction.
- **When someone else's claim is load-bearing, check it rather than relay it.** Relaying is how an
  unchecked claim acquires a second author and stops looking like one person's memory.

---

*Earned from:* an operator directive — *"never assume. Check first."* — issued after a single day
in which six assertions from one office and at least three from another were each falsified by a
command that would have taken under a minute, including one that reached a public repository and
had to be retracted there. Every one was made by someone with access to the artifact at the moment
they spoke. The nameability discriminator, the absence-claim distinction and the scope test were
supplied by the office whose tally appears above.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'the session transcript, which is an artifact: (a) an outgoing message asserting a specific property of a named path, where no read, grep or open of that path occurs in the session; (b) an outgoing message asserting an inability - cannot, blocked, not permitted, impossible - where no tool call attempting it appears anywhere in the transcript'
trigger: 'Stop'
check: 'msg names a path and asserts a property of its contents and no read of that path this session -> advise, naming the path and the command that would settle it; msg asserts an inability with no attempt in the transcript -> refuse'
escape: 'state it unverified with the reason, which is the rule own prescription and costs four words; a claim about a path read in an earlier session is re-read or marked stale'
narrows: 'gates the two species that leave a trace in the transcript - a file claim with no read, and a capability claim with no attempt. It CANNOT see the general case, because a remembered claim about the world, about a system not named as a path, or about what a commit accomplished arrives as prose and is indistinguishable from a checked one. Four of the six incidents in the rule are outside the gate. Do not read a green Stop as evidence the rule was followed'
```
