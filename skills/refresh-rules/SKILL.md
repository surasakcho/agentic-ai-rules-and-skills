---
name: refresh-rules
description: Refresh the rules a machine and a repo are actually bound by — copy the shared global rules verbatim into this machine's ~/.claude/CLAUDE.md, append a machine block derived from state, and adopt project rules as quotable statements rather than bare links. Use when a repo has no adopted-rules block, when its pin went stale, when a rule was adopted and did not fire, when working on a machine whose global rules were never refreshed, or when asked to refresh/re-adopt global or project rules.
---

# refresh-rules — the rules that are in force, on THIS machine, in THIS repo

**A rule is in force when its text is in context at the moment it applies.** Not when it is
adopted, not when it is pinned, and not when it is one of ninety URLs in a `CLAUDE.md`.

This is a **router**. It owns one thing — the machine block — and hands the rest to the skills
that already own them. It never becomes a second writer of a file that has one.

| file | holds | written by |
|---|---|---|
| `global/CLAUDE.md` *(shared repo)* | rules true on every machine | a human, in the shared repo |
| `~/.claude/CLAUDE.md` | that file **verbatim** + a generated machine block | **this skill** |
| repo `CLAUDE.md` | project rules, as statement + link | [`retrieve-lessons`](../retrieve-lessons/SKILL.md) |

## The failure this is built from

`board-for-state-sprint-for-commitment` was adopted into a repo, pinned to a sha, read during the
retrieval pass and quoted back to the operator — **and a flat task list was written anyway**, in
the repo whose `CLAUDE.md` links it. Adopted, cited, pinned, did not fire.

In one repo the adopted block is **97 lines carrying ~90 URLs and not one sentence of rule text.**
Nobody opens ninety links. The rules end up known by reputation.

## Steps

### 1. Report before you change anything

```sh
python3 refresh_rules.py --machine        # the facts, each with what they were read from
python3 refresh_rules.py --global         # global rules + machine block, to stdout
```

`refresh` reads as safe, so it behaves that way: **nothing is written without `--write`.**

**Done when:** you can name this machine's `kind` (host or container), its `purpose`, and its
preferred encoding — and none of the three was typed by anyone.

### 2. Refresh the machine's global rules

```sh
python3 refresh_rules.py --global --write ~/.claude/CLAUDE.md
```

⚠️ **On a container this file is often a read-only mount.** The script checks and **refuses**
rather than half-applying:

```
REFUSED -- <resolved-path>/CLAUDE.md is not writable (read-only mount?).
Nothing was written. Emit it and hand it to whoever can apply it.
```

When that fires, emit the block to a file and name who can apply it. **Never work around the
mount**; a read-only global file is a deliberate boundary, not an obstacle.

**Done when:** the machine's `~/.claude/CLAUDE.md` matches `global/CLAUDE.md` verbatim and carries
one machine block — or the block is in a named file with an owner.

### 3. Adopt the project rules

Hand this to `retrieve-lessons`. It owns the repo block, it reads the rules **at the pinned sha**
rather than from a working tree, and it now writes each rule as a **statement plus a link**.

```sh
python3 ../retrieve-lessons/retrieve.py --repo <target>            # show what it would adopt
python3 ../retrieve-lessons/retrieve.py --repo <target> --write    # re-select, then write
python3 ../retrieve-lessons/retrieve.py --repo <target> --repin    # advance the sha only
```

**`--write` and `--repin` are different risks and stay separate.** Re-selecting categories is
judgement and needs a human; advancing a sha over links a human already chose is mechanical.

**Done when:** every adopted rule in the repo's `CLAUDE.md` shows its own statement, and the
category selection was confirmed by a person.

### 4. Confirm each file, showing the diff

One confirmation per file, with the diff in front of the person confirming. A rules file that
changed without anyone reading the change is the defect that produced
[`ask-before-overwriting-uncommitted-work`](../../rules/coding/ask-before-overwriting-uncommitted-work.md).

**Done when:** every file this run touched was confirmed, or deliberately left alone.

## The refusal this skill is the gate for

**A rule with no machine-extractable statement stops the run and is named.** It is never emitted
as a bare link — the silent fallback is exactly how a block of ninety URLs accumulates without
anyone deciding to have one.

```
REFUSED -- 1 rule(s) have no machine-extractable statement:
  rules/coding/surgical-verified-change.md
```

The shape is specified in
[`a-rule-states-itself-in-one-line`](../../rules/how-we-work/a-rule-states-itself-in-one-line.md):
first non-empty line under `## The rule`, blockquote or bold. One parser implements it for both
scripts — [`skills/lib/rulestatement.py`](../lib/rulestatement.py). **Never write a second one.**

## The cap, and why it is reported

`how-we-work` always, plus the detected domain categories, to a ceiling of **25 rules**. Over the
ceiling the run says what it dropped and why. A silent cap reads as coverage —
[`a-classification-is-not-a-gate`](../../rules/how-we-work/a-classification-is-not-a-gate.md).

## What this skill does not do

- **Session role** (`-moff` / `-seer`). The `.claude-session` format holds one session per repo,
  so the two-role case may not exist. Fixing that format comes before handling it here.
- **Rendering adopted rules on demand.** That is
  [`rules-in-force`](../rules-in-force/SKILL.md), and it stays a separate read-only tool.
