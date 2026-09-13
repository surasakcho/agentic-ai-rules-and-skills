# Gate specifications handed to the enforcement layer

**This repo authors rules and specifies gates. It does not build or deploy them.** A rule here is
unfinished without an observable, a trigger, a false-positive shape and an escape hatch — and
finished without a line of hook code, which belongs to whoever owns the enforcement layer of the
estate adopting it.

Every rule's own specification lives in its `## Enforcement` clause; see
[`gateability.md`](gateability.md) for the verdicts and the build order. **This document is for the
few specifications that are not a single rule's clause** — guards that defend the enforcement
layer itself, where the gate's design is the finding.

Three specifications follow, each written against a real guard: one classified and unbuilt, two
deployed and defective. The general rule extracted from all three is
[`a-verb-list-is-not-a-boundary`](../rules/testing/a-verb-list-is-not-a-boundary.md).

---

## 1. Locality — an agent writes only inside its own territory

**Status when specified:** classified, with 11 cases already written, and no gate built. The
classification discriminates on `Write` and `Edit`; `Bash` reaches every territory on the machine
without either, and the test file records that gap before the gate exists.

> **Corrected 2026-09-13, after the two relevant fragments were quoted to this office verbatim.**
> This section originally assumed the known gap was a comment. It is not: the Bash case is real and
> carries a genuine trespassing payload. **But its expected verdict is *allow*.** So the suite does
> not merely fail to cover `Bash` — it currently *asserts that Bash trespass is permitted*, and
> that assertion is green today and will stay green. See "the residue must be a debt, not a
> permission" below, which is the part of this specification that changed.
>
> Standing caveat: this office has read two quoted fragments of that file and not the file. Every
> claim here is scoped to what was quoted.

### The ruling: the residue is acceptable as a *layer*, and not as the *boundary*

The discriminator is on the wrong axis. What makes a write dangerous is the **path** it lands on,
not the **tool** that carries it, and a tool list is an open set —
[`a-verb-list-is-not-a-boundary`](../rules/testing/a-verb-list-is-not-a-boundary.md). Shipping a
tool-keyed gate as the boundary produces a control that is incomplete on day one and reads as
coverage, which is worse than the classification it replaces.

It is acceptable **as the third of three instruments**, under three conditions, all of which are
part of this specification rather than advice attached to it:

1. **The confined population is covered structurally.** For any agent that runs inside its own
   filesystem view, locality is the **mount table**, not a hook: a territory the agent must not
   write is not mounted, or is mounted read-only. That is complete — the kernel is the
   discriminator, and no verb, tool or spelling reaches past it. This is the `structural` verdict
   [`gateability.md`](gateability.md) records as empty at the rules layer, and it is empty there
   because it belongs here.
2. **The unconfined population is covered by effect.** An agent that can see every territory —
   typically one running outside any container — cannot be fenced by mounts, so the instrument is
   a **sweep over outcomes**: for every declared territory other than the current one, the dirty
   set and the untracked set, captured at session start and compared at `Stop`. This detects a
   crossing regardless of how it was made. It is blind to territories that are not version
   controlled, and that blindness is named in the clause rather than left implicit.
3. **The tool-input check declares its residue.** Verdict `narrowed`, with `narrows:` naming
   `Bash` explicitly. Not `interposed`.

### The residue must be a debt, not a permission

Condition 3 above says the residue is *declared*. That is necessary and it is not sufficient, and
the existing suite shows why.

A case whose expected verdict is **allow** is indistinguishable from a case that documents correct
behaviour. The suite has two values available — *deny* and *not-deny* — and `not-deny` is being
asked to carry two incompatible meanings: **"this is permitted"** and **"this is a hole we have
not closed"**. A reader who did not write the file cannot tell them apart, and the one who did
will not always be the reader. It is the same defect as a deliberate blank standing where an
untriaged one would look identical, and the remedy is the same one:
[`absence-is-not-compliance`](../rules/testing/absence-is-not-compliance.md) — **three states, not
two.**

So the specification is a third expected-verdict value, not a change of sign:

| expected verdict | meaning | goes red when |
|---|---|---|
| `deny` | the gate must refuse this | the gate stops refusing |
| `allow` | the gate must permit this — a **decision** | the gate starts refusing |
| `known_gap` | the gate does **not** cover this, and should | the gate starts covering it |

`known_gap` passes today, exactly as `allow` does. The difference is that it is **countable**: the
suite prints *"N cases, M known gaps"* every run, so the residue appears in the output of the
thing that reports coverage rather than only in a comment above one line. It keeps the property
the current case already has — the day someone closes the gap, the case goes red and forces the
change to be deliberate — and it drops the property nobody wants, which is a green assertion,
read cold, that a trespass is fine.

**One more distinction, and it is this document's own standard applied one level down.** These
cases sit in a pending set: they are declared, not executed. A declared case is a
*specification*; only an executed one is evidence. So the residue is **counted and addressable,
and not yet observed** — which is
[`a-classification-is-not-a-gate`](../rules/how-we-work/a-classification-is-not-a-gate.md)'s
distinction between a verdict and an implementation, arriving inside the test suite instead of
inside the rule.

**This office does not make that edit and has not asked for it.** The file defines what the gate
must do; the population it governs includes writes made this week; and the layer that owns a spec
editing it in response to a question from the layer that writes the specs is the shape both
offices should refuse. The specification is above; applying it is the Core's call and its timing.

### Discriminator

- **Territory** is the session's declared working directory, read from the repo's own committed
  session declaration — not inferred from the process's cwd, which moves.
- Compare **resolved absolute paths**: expand `~`, resolve `..`, resolve symlinks. A gate that
  compares path strings is defeated by `../`, and by a symlink into the neighbour.
- For `Write` / `Edit` / notebook edits, the path is in the tool input: resolve it and compare.
- For `Bash`, apply the write-position discriminator in §2, and treat its ambiguous outcome as
  ambiguous — see the three outcomes below.

### The escape hatch, and why it must not be a refusal

**The trespass this gate defines is a thing that legitimately happens.** The precedent is on the
record: an unconfined session wrote into four confined repositories in one day, under explicit
operator direction. A gate that made that impossible would have been routed around within the
hour, and a guard that gets routed around is worse than no guard — see
[`validations-must-fail`](../rules/testing/validations-must-fail.md), corollary 2.

So the outgoing behaviour is **ask, naming the territory being entered**, not deny. Plus a
recorded line per crossing, so the effect sweep in condition 2 reports an *unacknowledged* write
rather than every write.

### Expected false positives

Shared read-only mounts; a session writing its own sibling worktree; tool caches under the home
directory; a temp directory that happens to sit inside another territory. Each is an allowlist
entry, and **each allowlist entry is a path, never a tool or a verb.**

### Three outcomes, not two

`allow` · `ask` · `deny`. A command that cannot be decomposed with confidence resolves to **ask**.
Folding "cannot tell" into allow makes the boundary decorative; folding it into deny is how it
starts firing on correct rows.

---

## 2. Write vs name — the discriminator for a protected-path guard

**Status when specified:** deployed, and refusing correct rows. The observed refusal was a
read-only `grep` whose **search pattern** contained a protected word beside a protected path.
Nothing was being written; nothing could have been. This estate has already had to disarm one
guard that fired on correct rows, so the next one to do it is on a short leash.

**Then it refused this office, the same day, while this section was being written** — on a write
to a scratch file in a temporary directory, because that file's *contents* were a list of test
cases naming a verb beside a protected path. Two readers, independently, inside one day, both
writing the specification for the thing that refused them.

### Confirmed by execution, not by reading

The guard's matcher was quoted to this office verbatim and replicated locally, and a corpus of 33
command shapes was run through the replica rather than reasoned about. Three findings matter to
this specification:

- **Matching is over the whole segment string. There is no argv decomposition anywhere in the
  Bash branch.** Segments come from a five-token split (`||`, `&&`, `;`, `|`, newline) and every
  pattern is a regex search over the resulting text. This was an inference in the first draft of
  this document and is now a confirmed fact.
- **Exactly one construct is tested in a genuine write position today** — the target of a shell
  redirect. That is the shape the rest of this section generalises, and it is already present for
  one case.
- **The destination-verb branch is positional by approximation**: it tests whether the protected
  path is the *last token of the segment*. That is the middle ground between a text search and a
  real operand model, and it fails in both directions depending on what follows the destination.

**A divergence list — the specific shapes the deployed patterns admit or refuse against intent —
was produced by that run and handed to the Core privately.** It is deliberately not in this
document: see [what is deliberately absent](#what-is-deliberately-absent-from-this-document).

Standing caveat: three helpers used by the matcher were not quoted, so every verdict from the
replica is scoped to the patterns that were. **That caveat was not boilerplate — it changed the
answer by half.** Four replica findings were flagged as unverifiable for exactly this reason, and
when the missing helper was checked against, two of the four turned out to be covered. Reporting
them as gaps would have been four wrong claims about a running control; reporting them as *scoped
to what was read* cost one sentence. See
[`a-finding-is-scoped-to-what-you-checked`](../rules/how-we-work/a-finding-is-scoped-to-what-you-checked.md).

### The discriminator

A command **writes** a protected path only when all three hold. Anything less is a **mention**,
and a mention is not a violation.

**Step 0 — separate the command from its data, and do it first.** A quoted string, a search
pattern, an `echo` argument and a heredoc body are payloads the command *carries*, not text the
shell will run. Splitting on newlines without this turns every line of a heredoc body into
something indistinguishable from a command, which is how a file's **contents** get convicted of
being the command that writes it.

A normaliser of this kind already exists in the deployed guard and did not prevent either
observed refusal, which is the instructive part: **it recognises one input shape.** A payload
stripper that handles heredocs but not quoted operands is not a smaller version of this step, it
is a different step that happens to share a name. The requirement is *every* payload position, and
where that cannot be decided the answer is **ask** — see the three outcomes below.

**Step 1 — decompose what remains into simple commands.** Split on `;`, `&&`, `||`, `|` and
newlines. Then strip the wrappers that hold another command as their argument, recursively: `env`,
`sudo`, `nice`, `time`, `nohup`, `xargs`, `timeout`, `stdbuf`.

**Step 2 — resolve the verb and classify it.**

| class | examples | rule |
|---|---|---|
| **never writes** | `grep`, `rg`, `cat`, `head`, `tail`, `less`, `diff`, `stat`, `file`, `wc`, `git log`, `git show`, `git diff`, `git status` | a protected path anywhere in its argv is a mention |
| **writes under a flag** | `sed -i`, `sort -o`, `awk` with a redirect, `tar -x`, `unzip -d`, `cp`/`mv` (target position only) | writes only when the flag or position is present |
| **always writes** | `tee`, `patch`, `install`, `dd`, `truncate`, `git apply`, `git am`, `git checkout -- <path>`, `git restore` | any protected operand is a write |

**Step 3 — require the protected path in a write position** of that verb: an operand of an
always-writes verb; a redirect target (`>`, `>>`, `<>`); the argument of `-o`, `-i`, `--output`,
`-d`; the target operand of `cp`/`mv`/`rsync`; the directory of `git -C`.

**Explicitly not write positions:** the pattern operand of a search verb; `--include` / `--exclude`
/ `-e` / `--regexp` values; a path inside a quoted string being searched *for*; a heredoc body not
redirected at the path; a comment.

### The second arm — and a property of the current guard that must survive

The three steps above are **path-anchored**, and a path-anchored discriminator is blind to every
command that names no path: a whole-tree restore, a hard reset, a `stash pop`, a `clean -fd`.
The deployed guard already handles this with a branch that fires **unconditionally, before any
protected path is looked for**, and that branch is correct precisely because it does not check a
path.

**A position-based rewrite must keep it as a separate arm, not fold it in.** The tempting mistake
is specific: someone tightening this guard for false positives deletes the unconditional branch on
the grounds that it does not even test a path, and removes the only cover against the commands
with the largest blast radius. The rule is
[`a-verb-list-is-not-a-boundary`](../rules/testing/a-verb-list-is-not-a-boundary.md), under *the
second arm*.

| arm | question | evaluated |
|---|---|---|
| scope-anchored | is the effect unbounded over the tree? | first, with no path test |
| path-anchored | does this write *this* path? | after, per step 0–3 above |

### Deployment gate — both directions, before it ships

Per [`validations-must-fail`](../rules/testing/validations-must-fail.md), this is not deployable
on the strength of passing. It ships with, at minimum:

- **must refuse:** `tee`, `patch`, `git apply`, `sed -i`, `> protected`, `cp src protected`, each
  wrapped once in `sudo` and once behind `&&`.
- **must allow:** the exact command that produced the false positive — a `grep` whose search
  pattern contains a protected verb and whose path operand is a protected file — plus
  `git log -- <protected>`, `cat <protected>`, and `sed 's/patch/x/' <protected>` with no `-i`.

A refusal case that has never been observed refusing, and an allow case that has never been
observed allowing, are both unverified.

### What this does not do

It reduces false positives. **It does not close the verb list** — see §3. Do not treat a clean
false-positive record as evidence of coverage; those are different questions, and conflating them
is [`absence-is-not-compliance`](../rules/testing/absence-is-not-compliance.md).

---

## 3. Closing the tamper verb list — and the plain answer that it does not close

**Status when specified:** deployed. `patch` is matched; `git apply` and `git am` are not. A patch
applied the git-native way rewrites the guard's own dispatcher while the guard matches nothing.

### The immediate closure — worth doing, and cheap

Add the git-native writers: `git apply`, `git am`, `git checkout -- <path>`, `git restore`,
`git stash pop`, `git stash apply`, `git revert`, `git cherry-pick`, `git reset --hard`,
`git merge`, `git rebase`, `git rm`, `git mv`, `git clean`, `git worktree add`,
`git config -f <path>`, `git submodule update`.

### And the plain answer: this is a whack-a-mole shape

**It is not closable by enumeration.** The list above closes today's hole and leaves, without
trying hard: `python -c`, `python -m`, `perl -pi -e`, `ruby -i`, `awk` with a redirect, `sed -i`,
`tee`, `sponge`, `dd`, `install`, `cp`, `mv`, `rsync`, `ed`, `ex`, `vi -c`, `busybox` applets, a
bare shell redirect, a `make` target, `$EDITOR`, and any script that wraps any of these. Each
addition is correct and none of them changes the shape: **the set of ways to write a file is open,
and the set of protected files is closed.**

### One case is covered by accident, and tightening an unrelated pattern uncovers it

Worth knowing before anyone edits the generic verb list. Two version-control operations that
rewrite a protected path are **not** in the subcommand-aware arm and are refused anyway — because
the generic list contains the bare verbs they are spelled with, and the segment happens to carry
one with a space in front of it. The pattern that saves them is not looking at version control at
all.

So the coverage is real and its attribution is wrong, which has a specific consequence: **someone
tightening the generic list to fix a false positive silently uncovers those two, without ever
touching the arm they believed owned them.** The false positives above are exactly the pressure
that would prompt that edit, so this is not a hypothetical ordering of events.

The instrument is per-arm mutation — disable the arm believed to cover a case and re-run it — and
the rule is
[`validations-must-fail`](../rules/testing/validations-must-fail.md), corollary 4. A guard with
two paths to the same verdict owes a test that says **which** one fired.

### The instruments that do close it

1. **Ownership or mount — the protected set is not writable by the agent.** A different uid, or a
   read-only mount. This is the only complete answer, it needs no list, and where it is available
   it removes the guard rather than improving it.
2. **A content manifest — check the effect.** Hash the protected set; verify at session start, at
   `Stop`, and after any command the parser in §2 could not decompose. A mismatch is reported as a
   finding with the before/after hashes, not as a refusal — by then the write has happened, and
   the value is in knowing, immediately and without having predicted the verb.

Keep the verb list as a **fast path** that refuses the honest cases before they run, classified
`narrowed`, with `narrows:` stating that it enumerates verbs and cannot close.

### What must not be done

**Do not widen the match to the whole command string.** That is the change that produced §2's
false positive, and it trades a false negative nobody can see for a false refusal the operator
can — and the operator's response to a guard that refuses correct work is to switch it off.

---

## 4. The absence case

Specified as a rule rather than as a one-off guard, because it is a species rather than an
instance: [`absence-is-not-compliance`](../rules/testing/absence-is-not-compliance.md), with its
observable, trigger, check and escape in that file's `## Enforcement` clause. Two instances found
on one day — a credential verifier that passed an agent configured with no credential, and a link
checker that accepted a regular file where a symlink was the whole requirement — and a third
inside this repo, which is why the clause exists.

The instrument, in one line: **a checker reports three states and prints its denominator.**

---

## What is deliberately absent from this document

**The divergence list.** Running the replica produced a specific inventory of command shapes the
deployed patterns treat contrary to intent. The false-*positive* half is in this document, because
a guard refusing correct work is a usability defect its users need to recognise. **The
false-negative half is not**, and will not be: an enumerated list of what a live guard fails to
stop is a working bypass for a control that is running right now, on a host holding credentials.
[`sanitise-before-sharing`](../rules/how-we-work/sanitise-before-sharing.md) names four categories
— people, places, paths and **findings** — and says the fourth needs a reader rather than a
pattern. This is the fourth. It went to the Core directly, and the operator can publish it if they
ever want it public; that is their call and not this office's.

**No code, and nothing deployed.** These are specifications. Building the dispatcher, editing the
settings that install the hooks, and putting any of it in front of a live session belong to the
enforcement layer, not to the office that writes the rules — and that separation is the point,
not an inconvenience. A rules author who can also deploy the gate is a rules author with no
counterparty.
