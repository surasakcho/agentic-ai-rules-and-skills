# Nothing that will be used twice lives in temp — not a patch, not a script, not a generated config

**Task type:** how-we-work — any work product, at the moment you choose where to write it.
**Related:**
[`scratch-code-lives-outside-the-repo`](../coding/scratch-code-lives-outside-the-repo.md) is the
other side of this line and is **not** contradicted by it: that rule keeps single-use probes out
of the repo, this one keeps reusable work in it. They partition the space; neither licenses the
other's case.
[`bau-artifacts-are-built-permanent`](../coding/bau-artifacts-are-built-permanent.md) says the
same thing for recurring, scheduled and business-as-usual work — this is the general form, and it
fires for a one-off artifact that a second party runs exactly once.
[`quick-and-dirty-needs-a-logged-experiment`](quick-and-dirty-needs-a-logged-experiment.md) —
*"temporary is a description of intent, never of what actually happens to a file."*

---

## The rule

> **Never write something to a temp or session-scoped location if anything will read it after the
> current session ends, or if anyone other than you will run it.**

Not a patch someone else applies. Not a script you will re-run. Not a generated config, a
fixture, a rollback, or a data file another step consumes. Those go in the repo — or another
durable, backed-up location — **regardless of how rough they are or how temporary they feel.**

### The distinction, and the one question that draws it

| | Scratch | Deliverable |
|---|---|---|
| Written to answer a question you are holding **right now**, consumed by you, in this session, never referenced again | ✅ | |
| Anything a second party runs | | ✅ |
| Anything this session or a later one uses a second time | | ✅ |
| A patch, a generated config, a fixture, a rollback, a data file another step reads | | ✅ |

**The tell is not file type, not polish, not intent at the moment of writing.** A patch file
feels like scratch because it is small, mechanical, and was produced in passing. None of that is
the test. The test is one question:

> **Will anything read this after the current session ends, or will anyone but me run it?**

**Yes — or *I don't know* — means it is not temp.**

## The incident

A subagent was asked to arm a pre-commit gate. It produced a 49-line patch, verified it, had it
reviewed, corrected it once, and left it in the **session-scoped scratchpad directory** the
harness provides — on the reasoning that a patch file "is scratch".

The handover that came out of that was a single command asking a second party to apply the patch
**from that path**. The reviewer's response was the whole lesson:

> *"Why is it in temp, not in the repo?"*

**That scratchpad is session-scoped: when the session ends it is reaped.** So an unapplied patch
evaporates and the work has to be redone. The artifact had been built once, reviewed once and
corrected once, and was about to be depended on by someone else at a later time. Nothing about
that is scratch.

**Cost:** work that was already done, verified and corrected is lost to a directory cleanup and
has to be re-derived from a transcript. And **a handover instruction pointing into a temp
directory is unusable the moment it is delayed** — the person receiving it cannot tell that it
has an expiry. There is no error to read: the command simply reports a path that is not there,
long after the context that would explain it is gone.

The detail worth keeping: the artifact parked in temp **was itself a gate** — a control a rule had
already declared and that was not yet running. The one thing most in need of a durable home was
the thing judged least deserving of one.

## When in doubt, durable is the cheap side of the bet

This is the non-obvious half, and it is an asymmetry, not a preference:

- **A durable file that turns out to be single-use costs one deletion.** Bounded, visible,
  trivially reversed.
- **A temp file that turns out to be reused costs the whole rebuild** — and the loss is
  **silent**. Nothing announces that the directory was cleaned. There is no failed command, no
  log line, no diff; only an absence, discovered by whoever needed the file.

Under uncertainty the bet is not close, and it does not become close by thinking harder about it.
Write it somewhere durable and delete it later if you were wrong.

## Guard

- **Choose the home before writing, not after.** If you cannot name where the artifact
  permanently lives, you have not yet decided whether it is a probe or a deliverable — decide
  that first, because the decision is cheaper before the file exists than after it is referenced.
- **Never put a session-scoped or `tmpfs` path into an instruction for someone else.** The rule
  that already gives the command:
  [`bau-artifacts-are-built-permanent`](../coding/bau-artifacts-are-built-permanent.md) —
  `findmnt -no FSTYPE,OPTIONS <path>`. A per-session directory the harness creates and reaps
  disqualifies a path just as `tmpfs` does.
- **A patch, a diff or a one-line command is not exempt for being small.** Size is not the
  test; the second reader is.
- **"I'll move it into the repo once it's applied" is the deferred-cleanup failure wearing new
  clothes.** The moving step is skippable, and the handover is exactly the moment attention
  leaves.
- **If you are handing over work at all, the handover is evidence of a second party** — which
  answers the question above without further thought.

---

*Earned from:* a verified, reviewed, once-corrected patch arming a pre-commit gate, left in a
session-scoped scratchpad because "a patch file is scratch", and then handed to a second party as
a command to apply from that path — caught by the reviewer asking why it was in temp rather than
in the repo, before the directory was reaped.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'a session-scoped or tmpfs path appearing in an instruction meant for someone else, and the filesystem behind any path handed over - findmnt -no FSTYPE,OPTIONS <path>'
trigger: 'Stop, plus PreToolUse(Bash) when a path under a scratch directory is passed to a command prepared for another party'
check: 'an outgoing message references a scratchpad or tmpfs path -> refuse; findmnt reports tmpfs or a reaped per-session directory -> refuse'
escape: 'state plainly that the artifact is single-use and not for reuse - which is the judgement the rule asks for, said out loud'
narrows: 'gates the handover, which is where the incident surfaced; a reusable file written to temp and read only by a later session names nobody to anybody and passes'
fires_late: true
note: 'the moment this rule names is the choice of where to write; a Stop refusal catches it at handover, after the work is already done - the same gate bau-artifacts-are-built-permanent declares, which is not yet implemented'
```
