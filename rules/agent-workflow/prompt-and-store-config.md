# Prompt for machine-specific values, store them locally

**A shared rule or skill must not contain a username, a hostname, or a path.** When it needs
one, it asks on first use and stores the answer in the consuming repo's gitignored `.env`.
The artifact stays portable; the value stays on the machine it describes.

---

## The incident

A leak scan across this machine's public skills repo — 201 commits, 441 text blobs — found no
tokens, no keys, and no collaborator names. What it found was **machine paths, in four
separate skills, three of them written long before the scan existed**:

| File | Literal | What it published |
|---|---|---|
| `wrap-all/SKILL.md` | `C:\Users\<user>\Repos\<private-repo>` | username **and the name of another private repo** |
| `setup-status-line/SKILL.md` | `C:/Users/<user>/.antigravity/statusline.ps1` | username, OS, tool layout |
| `session-sandbox/assets/sbx-env.sh` | `SBX_REPO="/home/<user>/repos/sandbox"` | username and directory layout |
| `lesson-review/SKILL.md` | `C:/Users/<user>/Repos/<repo>` | username, as a *documented example command* |

**Cost:** four public disclosures of a machine's layout, and — the part that actually blocks a
fix — three of them are **functional defaults, not illustrations**. Deleting the literal breaks
the skill. That is why they survived a leak scan that flagged them correctly: the scan could say
*this is wrong* but there was nowhere for the value to go.

**The tell:** the leak scan and this rule are two halves of one thing. A prohibition with no
supported alternative does not get followed; it gets worked around, and the workaround is a
literal with an apologetic comment above it.

---

## The rule

> **Machine-specific values are prompted for on first use and written to the consuming repo's
> `.env`. They are never literals in a shared artifact, and never committed.**

What counts: usernames, hostnames, machine names, absolute paths, scan roots, sandbox
locations, local ports, personal directory layouts. Anything true of *this machine* and false
of the next one.

What does not: values that are the same everywhere (a public URL, an upstream repo name), and
secrets — those belong in a secret manager, not in a file that exists to be convenient.

## How

[`lib/skillconfig.py`](../../lib/skillconfig.py) implements it. Shell and Python skills both
use it the same way, because the **prompt goes to stderr and only the value goes to stdout**:

```bash
SBX_REPO="$(python skillconfig.py get SBX_REPO --repo . --prompt 'Sandbox repo root')"
```

```bash
python skillconfig.py set SCAN_ROOT "D:/work" --repo .   # non-interactive
python skillconfig.py check --repo .                     # is storage safe here?
```

First call asks and stores. Every later call reads back silently. The key — never the value —
is appended to a committed `.env.example`, so what a repo requires is discoverable and
reviewable without anyone's machine leaking into it.

## The four refusals that make it safe

A config helper that only ever succeeds is the same failure mode as a guard that never fires.
These are the behaviours worth having, and each is pinned by
[`test_skillconfig.py`](../../lib/test_skillconfig.py):

- **It never invents a default.** With nobody to prompt — cron, CI, a piped stdin — it exits
  **2**, prints the exact `set` command, and **writes nothing**. A machine-specific value has
  no safe fallback, and a plausible guess is worse than a stop.
- **A blank answer is not an answer.** Pressing enter re-prompts; it does not store `""`.
- **It refuses to write where `.env` is already git-tracked.** That is the dangerous state: the
  next `git add -A` publishes it. The refusal names the fix rather than describing the problem.
- **It adds `.env` to `.gitignore` itself** rather than trusting that someone did. The test
  proves `git add -A` then leaves `.env` unstaged, and that `.env.example` never contains a
  real value.

## What is gated and what is not

`prose < checklist < test < gate`, honestly applied:

- **Gated.** `harvest.py --check` fails on any absolute path in a shared rule or skill, so a
  regression cannot be published. `skillconfig.py check` fails on a tracked or un-ignored
  `.env`, and on a real value that reached `.env.example`.
- **Not gated.** Whether a skill *asks* rather than assuming. Nothing can detect a value that
  was silently defaulted somewhere else, so this stays a review question: when reading a skill,
  ask what it would do on a machine that is not yours.

Related: [sanitise-before-sharing](sanitise-before-sharing.md) says a machine path must not be
published. This says where the value goes instead. Neither works alone.
