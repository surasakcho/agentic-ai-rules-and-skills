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

**Status when specified:** classified, with 11 executable cases already written, and no gate
built. The test file records a known gap before the gate exists: the classification discriminates
on `Write` and `Edit`, and `Bash` reaches every territory on the machine without either.

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

### The discriminator

A command **writes** a protected path only when all three hold. Anything less is a **mention**,
and a mention is not a violation.

**Step 1 — decompose into simple commands.** Split on `;`, `&&`, `||`, `|` and newlines. Then
strip the wrappers that hold another command as their argument, recursively: `env`, `sudo`,
`nice`, `time`, `nohup`, `xargs`, `timeout`, `stdbuf`.

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

**No code, and nothing deployed.** These are specifications. Building the dispatcher, editing the
settings that install the hooks, and putting any of it in front of a live session belong to the
enforcement layer, not to the office that writes the rules — and that separation is the point,
not an inconvenience. A rules author who can also deploy the gate is a rules author with no
counterparty.
