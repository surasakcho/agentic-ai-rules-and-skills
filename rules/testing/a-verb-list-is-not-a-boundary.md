# A verb list is not a boundary — enumerate what is protected, never the ways in

**Task type:** testing — guards, gates and permission checks that defend a path, a file, or a
territory against being written.
**Related:**
[`validations-must-fail`](validations-must-fail.md) — corollary 2, *build the failure before you
guard against it*, and the `"404"` substring guard that threw away 15 good regions. That is the
false-positive half of this rule, already paid for.
[`absence-is-not-compliance`](absence-is-not-compliance.md) — what an incomplete guard reports
about the cases it cannot see: nothing, which reads as green.
[`a-classification-is-not-a-gate`](../how-we-work/a-classification-is-not-a-gate.md) — a residue
that is not declared becomes coverage nobody has.
[`exact-match-on-a-complete-key`](../data-engineering/exact-match-on-a-complete-key.md) — the same
error in a join: loosening the comparison until it matches, rather than completing the key.

---

## The rule

> **Never defend a boundary by listing the ways of crossing it. The ways in are an open set and
> the protected things are a closed one — so enumerate the protected things, and gate on the
> effect or on the capability.**

A guard written as *"refuse these commands"* is complete only if nobody ever invents another
command. A guard written as *"this file may not change"* is complete by construction, because it
is stated over the thing that has to hold.

## It fails in both directions, and the second failure kills the guard

**Short by at least one.** A tamper guard protecting a set of control files matched the verb
`patch`. It did not match `git apply` or `git am` — the same operation, spelled the way a git user
actually spells it. A patch applied that way rewrites the very dispatcher the guard lives in, and
the guard matches nothing while it happens. Extending the list closes those two and leaves
`python -c`, `perl -pi`, `tee`, `sponge`, `dd`, `install`, `rsync`, `ed`, an editor, and `>`.

**Wrong axis.** A locality gate — *an agent may write only inside its own territory* — was
specified against the tools that carry a path in their input, `Write` and `Edit`. `Bash` carries a
path too, in a string the gate does not parse, and reaches every territory on the machine. The
gate's own test file recorded this as a known gap **before it was ever built**, which is the
honest version of the failure and still leaves a gate that is incomplete on the day it ships.

**And then the reflex fix kills it.** The obvious repair is to widen the match until it cannot
miss: look for the protected path anywhere in the command string. That guard refused a read-only
`grep` whose **search pattern** contained a protected word next to a protected path. Nothing was
being written. Nothing could have been written.

> **A guard that fires on correct rows does not get fixed. It gets disarmed** — by the operator,
> under time pressure, on the first or second false refusal — and the estate is then strictly
> worse off than if it had never been built, because the disarming is quiet and the guard is still
> in the config where the next reader will count it as coverage.

### The disarming is usually silent accommodation, not an off-switch

Switching a guard off is the *visible* end of this, and it is the rarer one. The common case leaves
no trace at all: the person refused **changes their command and moves on.**

> **Incident.** A guard refused a correct command. The refused party did the right thing — they did
> not re-spell the command, split the write, or reach for another tool to get past it; they
> improved the underlying artifact and re-ran. Nothing was bypassed and nothing was disabled.
> **And the false refusal still left no record anywhere.** It reached the office that owned the
> discriminator only because a third party happened to ask them to forward it.
>
> Four such refusals were observed across three offices and two guards in a single day — a count
> that exists only because those three offices happened to be talking to each other that day. The
> fourth refused the document specifying the fix, at the sentence quoting the refusal text.

Every property that makes that an appropriate response also makes it invisible. So:

- **The false-refusal rate is unobservable by default**, because a correct adaptation and a
  correct allow look identical from outside.
- **A guard with no channel for reporting a false refusal reads as having none** — and a
  false-positive rate of zero, measured by a system that cannot receive the reports, is
  [`absence-is-not-compliance`](absence-is-not-compliance.md) wearing the one costume nobody
  questions, because it is the number everybody wants.
- **The accumulation is what kills it.** No single silent accommodation justifies action. The
  twentieth one, by an operator with a deadline, is the off-switch — and by then nobody can say
  how many there were.

**So a guard owes a channel, not just a discriminator.** Log every refusal with the segment that
matched and the arm that fired; give the refused party one cheap way to mark a refusal wrong; and
report the marked count as a rate. Until that exists, *"we have had no complaints"* is a statement
about the absence of a mailbox.

The two failures are the same mistake seen twice: **the discriminator is on the wrong axis.** A
command's name is not what makes it dangerous, and a string's contents are not what makes it a
write.

## The three instruments, strongest first

| instrument | what it gates | completeness |
|---|---|---|
| **Structural — remove the capability** | the protected path is not writable by this actor: not mounted, mounted read-only, owned by another uid | **Complete.** No verb reaches it, because the kernel is the discriminator |
| **Effect — check the outcome** | a manifest of hashes over the protected set, or a status sweep over every territory, compared at a moment the actor cannot skip | **Complete over outcomes**, blind to intent. Detects; does not prevent |
| **Argv — inspect the command** | the parsed command, before it runs | **Never complete.** Prevents, cheaply, in the honest cases |

**Pick the strongest one the situation allows, and use the weaker ones as a net rather than as the
boundary.** An argv check is worth building — most writes are honest, and refusing before the fact
is the only instrument that preserves the artifact — but it is the *third* line, and it must be
classified as `narrowed` with its residue written down.

**The argv check needs three answers, not two.** Shell is not reliably parseable: variables,
`$(...)`, heredocs and quoting defeat any decomposition. A parser that cannot decide must return
*ask*, never *allow* and never *deny*. Folding "cannot tell" into allow is how a boundary becomes
decoration; folding it into deny is how it starts firing on correct rows.

## Gate on write position, not on the presence of a word

When you do inspect a command, the discriminator that separates a command that **writes** a
protected path from one that merely **names** it:

0. **Separate the command from its data, first.** A quoted string, a search pattern, a heredoc
   body and an `echo` argument are *payloads*: text the command carries, not text the shell will
   run. Splitting on newlines without doing this converts every line of a heredoc body into
   something indistinguishable from a command — which is how a file whose **contents** mention a
   verb and a path gets convicted of being that command.
1. **Decompose** what remains into simple commands — split on `;`, `&&`, `||`, `|` and newlines,
   then strip the wrappers that hold another command as their argument (`env`, `sudo`, `nice`,
   `time`, `xargs`, `nohup`).
2. **Resolve the verb** of each, and classify it: *never writes* (`grep`, `cat`, `head`, `diff`,
   `git log`, `git show`), *writes only under a flag* (`sed -i`, `sort -o`, `awk > file`), *always
   writes* (`tee`, `patch`, `install`, `git apply`, `git am`, `git checkout -- <path>`).
3. **Require the protected path in a write position** of that verb: an operand of a writing verb,
   a redirect target, the argument of `-o`/`-i`/`--output`, or the directory of `git -C`. A path
   that appears only as a search pattern, a `--include`, a `-e` expression, or an operand of a
   verb that never writes is a **mention**, and a mention is not a violation.

Every one of these steps is a heuristic. They are worth having and they do not make the list
closed — which is why they sit under the structural instrument rather than replacing it.

## The second arm: a command that names no path can still write every path

**Position-based gating assumes the command names its victim, and the most destructive ones do
not.** `git checkout .`, `git restore` with no pathspec, `git reset --hard`, `git stash pop`,
`git clean -fd`, an `rm -rf` on an ancestor directory — each rewrites or deletes a protected file
while mentioning nothing a protected-path pattern can match. A discriminator built purely on write
position is **blind to exactly the commands with the largest blast radius**, and tightening it
makes that blindness worse.

So a path guard needs two arms, evaluated independently:

| arm | question | fires on |
|---|---|---|
| **path-anchored** | does this command write *this* path? | the protected path in a write position |
| **scope-anchored** | is this command's effect unbounded over the tree? | whole-tree restores, resets, cleans — **before** any path test, because there is no path to test |

The scope arm cannot be derived from the path arm and must not be folded into it. Getting this
wrong is a specific, tempting mistake: a reviewer tightening a guard for false positives deletes
the unconditional branch as "it doesn't even check the path", which is precisely why it is there.

## Guard

- **State the boundary over the protected set, not over the ways in.** "These files do not change"
  is checkable; "these commands are refused" is a list someone will add to forever.
- **Reach for the mount table and the owner uid before reaching for a regex.** A capability the
  actor does not hold needs no guard at all, and that is the only complete answer available.
- **Pair every argv guard with an effect check.** The argv half prevents the honest case; the
  effect half is what tells you the day the list was short.
- **Never widen a match to close a gap.** Widening trades a false negative you cannot see for a
  false positive the operator can, and the operator's response is to switch the guard off.
- **Narrow in the same normalisation space the matcher already used.** A pattern that tolerated
  `sudo`, `env` and a leading `./` has been quietly treating those forms as equivalent; a narrowing
  condition written against the raw text stops treating them so, and every form the old pattern
  caught through that tolerance becomes a hole the new one leaves. The tell is that the repair is
  expressed in different terms from the thing it repairs — *"only when the first token is the
  verb"*, against a pattern that never looked at tokens. **Check a narrowing fix against the cases
  the old pattern caught, not only against the case that prompted it.**
- **Three outcomes for anything that parses a command:** allow, deny, and **ask**. Ambiguity is a
  state, not a default.
- **Strip the payload before you read the verbs, and keep the scope arm separate from the path
  arm.** The first stops a file's contents being convicted as a command; the second catches the
  commands that name nothing at all.
- **Declare the residue in the gate's own clause.** An incomplete guard is acceptable; an
  incomplete guard presented as a boundary is not.
- **Ship a channel for false refusals with the guard, and report the rate.** A guard that cannot
  receive the report that it was wrong will be told so exactly once — by being switched off.
- **Never let a refusal message assert a cause it only pattern-matched.** *"…using `docker`"* when
  `docker` was a word inside a quoted payload sends the reader hunting for a call that was never
  made. Name what matched and where — the token, the segment, the arm — not what it was assumed to
  mean. A wrong explanation costs more than a bare refusal, because people debug the explanation.

---

*Earned from:* two guards in one estate, found the same day. A tamper guard whose protected-path
verb list matched `patch` but not `git apply` or `git am`, so a patch applied the git-native way
rewrites the gate dispatcher while the gate matches nothing — and the same guard refusing a
read-only `grep` because a protected word appeared in its **search pattern**. Alongside them, a
territory gate specified against `Write` and `Edit` whose own test file recorded, before it was
built, that `Bash` reaches every territory without either.

Then, while this rule was being written: **the same guard refused the author, on a write to a
scratch file in a temporary directory, because the file's own contents were a list of test cases
naming a verb beside a protected path.** No protected path was being written and none could have
been. A normaliser to strip data payloads already existed in that guard and did not catch it — it
recognises one input shape, and neither a search pattern nor this heredoc was that shape. Two
independent discoveries of the same false positive inside one day, by two readers, both of whom
were at that moment writing the specification for it.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'each deployed guard that defends a path or territory: whether its discriminator is a list of command names, whether a structural instrument (unmounted, read-only, foreign owner) covers the same protected set, whether an effect check (hash manifest or status sweep) exists, and whether its clause declares what it does not cover'
trigger: 'CI over the gate configuration, plus review at the moment a guard is added or its verb list is extended'
check: 'a guard whose match is a verb or substring list and whose clause carries no narrows: field -> fail; a protected set with no structural or effect instrument, defended by argv matching alone -> fail; a command parser with only two outcomes and no ask state -> fail'
escape: 'a protected set that genuinely cannot be made unwritable (the actor must write its neighbours) keeps the argv guard as the primary instrument - and then owes the effect check and the declared residue, not an extended list'
narrows: 'cannot prove a verb list is short - that is the whole difficulty, and only the effect check finds it, after the fact. Gates the SHAPE of the guard (is there a structural or effect instrument, is the residue declared, are there three outcomes), never its coverage'
```
