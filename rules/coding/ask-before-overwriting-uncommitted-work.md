# Ask before overwriting an uncommitted file

**Task type:** coding — any write that destroys the existing contents of a file that is
already there.
**Related:** [`nothing-leaves-git-without-permission`](../how-we-work/nothing-leaves-git-without-permission.md)
is why the file was unprotected in the first place; this is the last checkpoint before the
damage. [`surgical-verified-change`](surgical-verified-change.md) keeps a change small once
you are allowed to make it.

---

## The rule

**Before any write that destroys existing content, run `git status` on the target. If it is
untracked, or tracked with uncommitted changes, stop and ask.**

`git status` on one path is one command. It is the difference between a mistake that is a
`git checkout` away and one that needs a filesystem snapshot to recover.

## The three states, and what each permits

| State of the target | Recovery if you are wrong | What you may do |
|---|---|---|
| Tracked, clean | `git checkout -- <path>` | Proceed |
| Tracked, uncommitted changes | Nothing in git — the edits were never committed | **Ask** |
| Untracked | Nothing in git at all | **Ask** |

Only the first row is safe, and it is safe for exactly one reason: git is holding a copy.

## What counts as a destructive write

Not just the obvious ones. All of these overwrite in place, and all of them have caused this:

- running a generator, build script, formatter, linter `--fix`, or codegen tool
- `Write`/`echo`/`>`/`>>` onto an existing path
- `cp` or `mv` onto an existing target
- `git checkout`, `git restore`, `git stash` over local modifications
- anything with `--force`, `--overwrite`, `--yes`, or `--clean`

**"Verifying my change still works" is the most dangerous of these**, because it feels like a
read. Re-running the build to confirm nothing broke is a full overwrite of the build's output,
and the incident below is exactly that.

## If the user says go ahead

Copy the file aside first anyway, and say where the copy is. Permission to overwrite is not
the same as confidence that overwriting is correct, and a scratch copy costs nothing.

## Why this matters more than it looks

The agent that overwrites uncommitted work almost never intends to write to that file. It
intends to *run a command*, and the write is a side effect the command performs somewhere the
agent was not looking. That is why "be careful with writes" does not work as a rule and
`git status` on the target does: the check has to attach to the thing you are actually about
to do, not to the intention you have in mind.

---

## The incident

*2026-08-19, a Tableau workbook deck built by hand-authoring XML.*

The user solved a long-open problem in the Tableau GUI — matching data-label colour to line
colour — saved the workbook, and asked the agent to *study the file and update the API doc*.

The agent read the file, found the answer (`color-mode='match'`), wrote it into the doc, and
then re-ran the build script **to verify the change rendered correctly**. That run regenerated
the workbook and destroyed the user's save. The file was untracked, so there was nothing to
restore from.

The state of the target at that moment, had anyone run `git status` on it:

```
?? 20250716-Fraud/Compendium/compendium.twb
```

Two characters. The whole rule is: read them before you write.

The recovery worked only because the folder happened to sit in OneDrive and version history
still held the save. The user's instruction afterwards is this rule:

> "when uncommitted file is being overwrite, make sure to prompt or ask for permission first."
