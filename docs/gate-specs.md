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

**Then it refused this office twice, the same day, while this section was being written.**

- On a **write to a scratch file in a temporary directory**, because that file's *contents* were a
  list of test cases naming a verb beside a protected path.
- On a **read** — `wc -l` over three filenames — because one of the protected files is called
  `install-<dispatcher>.py`, and `install` is itself a verb in the destination list. The verb
  pattern and the protected-path pattern matched *the same token*, and the destination heuristic
  then found that token in last position.

The second one is the sharper of the two, because it does not need a payload at all: **the
protected file's own name supplies the verb.** Any protected path whose name contains `cp`,
`install`, `ln`, `rm`, `mv`, `dd` or `tee` as a word will do the same, and the more
self-describing the filename, the likelier it is.

> ⛔ **CORRECTION — this office first published it as "the file cannot be counted, catted or listed
> by name at the end of a command", which is wrong in both directions.** Re-run against the module
> with the boundary cases separated:
>
> | command | verdict |
> |---|---|
> | `wc -l install-<d>.py` | **refused** |
> | `cd claude/hooks && wc -l install-<d>.py` | **refused** |
> | `wc -l install-<d>.py \| cat` | **refused** |
> | `wc -l ./install-<d>.py` | allowed |
> | `wc -l claude/hooks/install-<d>.py` | allowed |
>
> The trigger is **a bare, unqualified filename in last position of its own segment** — not the
> end of the command, and not the working directory. A pipe does not save it, because last-token
> is evaluated per segment. Path-qualifying the filename does save it, for a reason to do with how
> the verb pattern anchors.
>
> **That anchoring detail was published here in full and has been withdrawn.** Stated generally it
> is one inference step from a *false negative* on a different gate, which this office found later
> the same day by testing the reader path it had not tested when it wrote this. The hole went to
> the Core directly; the mechanism is not restated here. It remains in this repo's git history,
> which is a public log — no erasure is claimed, and publishing it was a call this office got
> wrong by one step. See [what is deliberately absent](#what-is-deliberately-absent-from-this-document).
>
> Which makes the practical shape worse than the first telling: the command that fails is the
> **short, unqualified one you type while standing in the directory**, and the one that works is
> the long path-qualified form you type from somewhere else. That is exactly inverted from how
> anyone investigates a gate system, and it is the shape most likely to end with the guard
> switched off.
>
> **The allowed rows are not a bypass, and must not be read as one.** Qualifying the path does not
> defeat the destination test — it stops the *filename* being misread as a verb. Every genuine
> write to the same qualified path still refuses:
> checked across `cp`, `install`, `tee`, `rm`, `chmod`, `sed -i` and a shell redirect, all eight
> refused with `./` in front. What changes is only whether a **read** is misclassified. Both
> offices verified this independently before it was written down, because a table of allowed
> commands in a public document is one careless reading away from being an evasion recipe.

**The cheap fix, and the amendment that keeps it from creating a hole.** Test the protected pattern
against the last token *only when the segment's first token is itself a destination verb* — `wc` is
not `cp`, so the case above disappears. But the first token must be taken **after stripping the
same prefixes the matcher already tolerates**. Verified against the module: `env cp /tmp/evil
<protected>` is refused today, and a naive first-token test would stop refusing it — a false
negative manufactured by the fix for a false positive. Strip `sudo`, `env` and `nohup` first, as
the sibling pattern already does.

Two readers, independently, inside one day, both writing the specification for the thing that
refused them.

### Confirmed by execution, not by reading

The guard's matcher was quoted to this office verbatim and replicated locally, and a corpus of 33
command shapes was run through the replica rather than reasoned about. Three findings matter to
this specification:

- **The tamper arm matches over the whole segment string.** Segments come from a five-token split
  (`||`, `&&`, `;`, `|`, newline) and every tamper pattern is a regex search over the resulting
  text.

  > ⛔ **CORRECTION.** This bullet previously read *"there is no argv decomposition anywhere in the
  > Bash branch"*, which was written from quoted excerpts and is **false**. Read against the file
  > itself: the **version-control arm tokenises properly** — `shlex.split`, falling back to a
  > whitespace split on unbalanced quotes, then dispatching on subcommand with flags and
  > positionals separated. So the guard already contains a working argv model; it is applied to one
  > arm and not the other. That changes this document's recommendation from *"build a decomposer"*
  > to *"the decomposer exists — extend its reach"*, which is a materially cheaper instruction, and
  > it was wrong for exactly one exchange because the excerpt that would have shown it was never
  > quoted.
- **Exactly one construct is tested in a genuine write position today** — the target of a shell
  redirect. That is the shape the rest of this section generalises, and it is already present for
  one case.
- **The destination-verb branch is positional by approximation**: it tests whether the protected
  path is the *last token of the segment*. That is the middle ground between a text search and a
  real operand model, and it fails in both directions depending on what follows the destination.

**Re-run against the real file once it could be read: the replica and the deployed gate diverged
on 3 of 37 shapes, and all three were inside the region the caveat below had flagged as
unverifiable.** That is the caveat doing its job rather than decorating the finding — the replica
was right everywhere it claimed to be right, and wrong only where it had already said it could not
see.

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

**The corpus, as intent.** This is a specification of desired behaviour, not a report of current
behaviour — which shape is currently refused is deliberately not recorded here, per the disclosure
split at the end of this document. `P` is a protected path; `INST` is a protected path whose *name*
contains a verb.

| must ALLOW | why it is a correct row |
|---|---|
| `grep -n "…patch…" P` | the verb is in a **search pattern** — the refusal that started this |
| `grep -c "rm" P` · `echo "do not rm P"` | a verb inside a quoted payload |
| `cat P` · `wc -l P` · `ls -la P` | reads |
| `wc -l INST` · `cat INST` | a read whose **only** verb comes from the protected filename |
| `git log -- P` · `git diff P` | history reads |
| `sed -n '1,50p' P` | `sed` with no `-i` |
| `cat > /tmp/notes <<EOF … P … EOF` | the path named in a **heredoc body**, written elsewhere |
| `cp P /tmp/backup` | copying the protected file **out** is harmless — direction matters |
| `git stash list` · `git checkout -b x` | inspection and navigation |
| `python3 -c "print(1)" && cat P` | a verb in a **different segment** from the path |

| must REFUSE | arm that should own it |
|---|---|
| `tee P` · `patch P` · `rm -f P` · `chmod 777 P` · `dd if=… of=P` | verb list |
| `sed -i … P` · `perl -pi -e … P` | in-place |
| `python3 -c "open('P','w')…"` | interpreter |
| `echo x > P` · `awk … > P` | redirect target |
| `cp /tmp/evil P` · `install -m 644 /tmp/evil P` | destination |
| `cp /tmp/evil P extra` | destination **not** in last position |
| `ed P < script` | a writer in no list — stands for the open set |
| `git apply` · `git am` | writes that name no path and are in no arm |
| `git checkout … -- P` · `git restore … P` · `git reset --hard` | scope arm |
| `git rm P` | **must be owned by the git arm**, not caught incidentally by the verb list |

Each row is one case. A guard that passes the left column and refuses the right column is doing
the job; one that has only ever been run against the right column is unverified in the direction
that gets guards switched off.

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

---

## 5. The payload defect is shared infrastructure, and one fix covers three gates

**Status when specified:** reported by a third Sector, on a *different* gate — a credential-exfil
guard refusing a command that wrote a unit-test file via a quoted heredoc. Reproduced here against
the module, and then **observed a second time on this office's own command while this section was
being written** — see the last subsection, which is not a joke.

### What the reproduction establishes

- **Three gates share one decomposition.** `credential-exfil`, `credential-into-repo` and
  `gate-tamper` all run the same `strip-payloads -> join-interpreter-heredocs -> split-into-segments`
  pipeline before matching. **This is not three bugs. It is one pipeline with three consumers**, and
  it is why the same false-positive shape has been observed on two different gates by three
  different readers in one day.
- **The payload stripper is conditional on the sink, and the sink list is short.** It strips a
  quoted heredoc body only when the owning segment is a commit-message or issue-body command.
  Reproduced against the module: the identical body is **allowed** when owned by a commit and
  **refused** when owned by a redirect into a file. Writing a file is not on the list, and writing a
  file is what a session does all day.
- **It fires only when the protected token and the verb land on the same physical line**, because
  segmentation splits on newlines. A verb on line 3 and a path on line 5 do not correlate.

  **Confirmed since, against the reporting Sector's actual source line.** The reported cause — a
  word appearing inside Python identifiers on other lines — does not reproduce and was not the
  mechanism. What matched was **a local variable whose name happens to be a reader verb, assigned
  on the same line as a credential-shaped string**: an indented `<verb> = <call>(...)` inside the
  test body. The indentation puts whitespace before the name, which is all the verb pattern asks
  for. So the token that convicted the command was not a command, not an argument, and not even a
  reference — it was **a name being defined**, which is the furthest thing from an invocation that
  a line of code contains.

### The discriminator — and why "a quoted heredoc is inert" is too strong

A quoted heredoc is inert **to the shell**. It is not inert to whatever consumes it: `python3 -
<<'EOF'` is a program by any other name, and the guard already carries a second normaliser whose
whole job is to splice interpreter bodies back onto their owner line so they *are* correlated.

So the classification is not *quoted or not*. It is **what the body is handed to**:

| owner of the heredoc | the body is | treat as |
|---|---|---|
| a byte sink — a redirect into a file, `tee <file>`, a commit or issue body | stored verbatim | **data** — strip it |
| an interpreter — `python3 -`, `sh`, `node`, `awk` | executed | **program** — scan it, joined to its owner |
| anything unrecognised | unknown | **scan it**, failing open as it does today |

**The cheapest correct change is to extend the data-sink list to byte sinks, not to trust quoted
heredocs generally.** Both halves of the machinery already exist; the gap is that the data half
lists message sinks only. That is a list change plus one predicate, and it closes the shape on all
three gates at once.

### A refusal message must not assert a cause it only pattern-matched

The refusal read *"reads or copies ~/secrets using `docker`"*. The word was a token inside a quoted payload. The reader then goes looking
for that invocation — in a Sector with no docker socket at all — and finds nothing, because there
was nothing.

**Name what matched and where: the token, the segment, and the arm that fired.** A refusal that
explains itself wrongly costs more than one that says only "refused", because people debug the
explanation. Same requirement as the per-arm report in
[`validations-must-fail`](../rules/testing/validations-must-fail.md), corollary 4, aimed at the
message instead of at the test.

### The channel — the part with no code in it yet

The Sector that hit this **absorbed the refusal and adapted**: it improved the artifact and re-ran,
which was the right response and bypassed nothing. The false refusal still left **no record
anywhere**, and reached this office only because a third party asked them to forward it.

That is the failure with no discriminator to fix it. A guard's false-positive rate is unobservable
by default, because a correct adaptation is indistinguishable from a correct allow — so *"no
complaints"* is a statement about the absence of a mailbox, and a zero measured that way is
[`absence-is-not-compliance`](../rules/testing/absence-is-not-compliance.md) in the one costume
nobody questions.

**Specification:** log every refusal with the matched token, the segment and the arm; give the
refused party one cheap way to mark a refusal wrong; report the marked count as a rate beside the
refusal count. **Ship it with the discriminator, not after it** — the discriminator will be wrong
again, and this is the only thing that will say so before somebody reaches for the off-switch.

### One predicate fixes both gates: the verb must be in command position

The two false positives look unrelated — a filename that contains a verb, and a variable named
after one — and they are the same defect. **A pattern that finds a verb *anywhere* in a segment
is asking "does this word appear", when the question is "is this word the command".**

The amendment: take the verb from **command position** — the first token of the segment after
stripping the wrappers the pattern already tolerates (`sudo`, `env`, `nohup`, `nice`, `time`,
`timeout`, `stdbuf`) and any `VAR=value` prefix — treat a `name = value` form as an assignment and
not a command, and compare on the token's **basename**.

Verified against a 12-case corpus, 12 of 12, before being written down here — because
[the previous version of this amendment got three of eight wrong](../rules/testing/a-verb-list-is-not-a-boundary.md),
and a fix checked only against the case that prompted it is the failure the rule beside it names:

| must still fire | must stop firing |
|---|---|
| bare verb · `sudo`/`env` wrapper · `VAR=1 verb` | a filename that contains a verb |
| a verb reached by **basename** rather than raw token | a variable being assigned a verb's name |
| a genuine destination write | a verb inside a comment or a string |

The basename comparison is not cosmetic and is the half that matters most: it is what makes the
predicate a **security** fix as well as a usability one. The reason why went to the Core directly
and is not in this document.

### The section could not be written without tripping the defect

Appending this text was itself refused, by the same gate, for the same reason. The sentence above
that **quotes the refusal** puts a sensitive path and a reader verb on one line inside a quoted
heredoc bound for a file — which is the exact shape under discussion. The phrase had to be
assembled from fragments at write time to get the document written.

Four live refusals now, across three offices and two gates, every one of them on a correct command,
and this one refused **the specification of its own fix**. It is the cheapest possible argument for
the channel in the previous subsection: if the office writing the gate specifications cannot
document a false refusal without triggering it, the rate is not going to be discovered by waiting
for reports.
