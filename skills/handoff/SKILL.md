---
name: handoff
description: Write a handoff document so a fresh agent can continue the work, saved as a new dated file in a repo's handoffs/ folder, committed and pushed, with a pointer the next session loads automatically. Works inside or outside a repo.
argument-hint: "What should the next session focus on?"
disable-model-invocation: true
---

Write a handoff document that summarises the current conversation, so a fresh agent can continue the work.

A handoff only matters if the next session **finds it** and it **survives**:

- Never save it to OS temp. `/tmp` is RAM-backed on some hosts, so a reboot deletes it.
- Never write it into `CONTEXT.md`. That file is a domain glossary, and session notes don't belong there.
- Nothing reads `handoffs/` on its own. Step 6 leaves the pointer that makes the next session read it.

## 1. Pick the repo

Run `git rev-parse --show-toplevel` in the working directory.

- **Inside a repo:** that repo is the **home repo**.
- **Outside a repo:** ask the user which repo this session's work belongs to, and suggest the repos the session actually edited. Their answer is the home repo.
- **The work belongs to no repo:** the home repo is `~/projects/obsidian-vault`.

Remember whether you started inside or outside the home repo. Step 6 depends on it.

## 2. Pick the file

- Write to `<home repo>/handoffs/YYYY-MM-DD-HHMM.md`, using the current UTC time. Create `handoffs/` if it doesn't exist.
- Always create a **new** file. Never overwrite an earlier handoff, because it is the record of what the previous session knew.
- If you started outside the home repo, include a **Working directory** line naming where the session ran, so the next agent knows where to start.

**Open handoffs.** A handoff is **open** until a later handoff names it in its `**Supersedes:**` line. Usually only the newest one is open. Parallel sessions can leave several open at once.

## 3. Close the open handoffs

List the open handoffs in `handoffs/`: every file that no other handoff's `**Supersedes:**` line names. Read each one, whether or not this session started from it.

Account for **every** item under their "State now" and "Next session focus":

- **carried forward:** still open, so it goes into this handoff;
- **done:** say so, with evidence (a commit, a closed issue, a URL);
- **dropped:** say so, with the reason, and who decided.

Put the done and dropped items in a short **Closed since last handoff** section.

Open the new handoff with `**Supersedes:** handoffs/<file>, handoffs/<file>`, naming every open handoff you read, by filename. That closes them and merges parallel threads back into one.

**Done when:** every item in every open handoff is carried forward, done or dropped, and the Supersedes line names all of them. If there are no earlier handoffs, skip this step.

## 4. Write it

- **Next session focus.** If the user passed arguments, they describe what the next session will work on, so tailor the whole document to that. This is the first section.
- **State now.** Say what is done, what is in progress, and what is blocked or on hold, with the reason for each.
- **Standing constraints.** List the instructions the user gave this session that the next agent must keep following, including corrections to your own behaviour.
- **Unverified.** List the claims you did not check, and label them unverified.
- **Suggested skills.** Name the skills the next agent should call the Skill tool for, and say why.
- **Reference, don't duplicate.** Anything already in specs, plans, ADRs, issues, comments, commits or diffs gets linked by path or URL, not copied.
- **Redact** secrets and personal information: API keys, passwords, tokens, private keys, email addresses.
- **Carry over stranded facts.** If this session learned something that exists nowhere durable yet (a research result, a measurement), write it into the handoff or post it where it belongs, then link it. A handoff is often the only place such a fact would otherwise survive.

## 5. Commit and push

1. **Check the home repo's rules first.** Read its `CLAUDE.md` and any earlier handoff. If they limit commits or pushes (for example "no commits to main" or "WIP branch only"), follow those limits. If committing isn't allowed, leave the file uncommitted. If committing is allowed but pushing isn't, commit without pushing. Either way, tell the user the handoff exists only on this machine.
2. **Stage only the files this skill wrote:** the handoff, plus `CLAUDE.md` if step 6 changed it. Never run `git add -A`. Some repos hold local-only files that must not be swept in.
3. Commit with `docs: handoff YYYY-MM-DD-HHMM`.
4. Push to the current branch's upstream. If the branch has no upstream, report that and don't create one without asking.
5. **Verify the push actually reached the remote.** `git status -sb` should show nothing ahead, or `git ls-remote` should show the new SHA. A push command returning is not proof.

## 6. Leave a pointer the next session loads

Do this before committing, so a `CLAUDE.md` change goes into the same commit.

**Started inside the home repo:** make sure the home repo's root `CLAUDE.md` contains this line, and add it only once. Replace an older start-of-session handoff line rather than adding a second:

> **Start of session:** use the `pickup` skill. It reads the open handoffs in `handoffs/` before doing anything else, and their "Next session focus" is the plan.

If there is no `CLAUDE.md`, create one. If the repo has an `AGENTS.md`, put `@AGENTS.md` on the first line so its instructions still load.

**Checked out on a branch other than the default branch:** stop and ask the user before committing. A `CLAUDE.md` pointer or handoff committed on that branch is invisible from the default branch and from a fresh clone. The simple fix is to commit the handoff to the default branch. Don't build pointer issues or branch-switching instructions around it.

**Started outside the home repo:** a `CLAUDE.md` in the home repo won't load in the directory you're in. Use the working directory's memory instead, because Claude Code loads it automatically in any directory:

- The memory directory is `~/.claude/projects/<slug>/memory/`. `<slug>` is the working directory's absolute path with each `/` replaced by `-`, so `/home/me/work` becomes `-home-me-work`. How other characters (dots, spaces) are handled hasn't been verified. Don't compute it: find the matching directory with `ls ~/.claude/projects/`. The current session's directory already exists.
- Create or update **one** file there, `latest-handoff.md`. Give it memory frontmatter (`name: latest-handoff`, a one-line `description`, `metadata.type: project`), and in the body give the handoff's absolute path and its date.
- Make sure `MEMORY.md` in that directory has exactly one line for it:
  `- [Latest handoff](latest-handoff.md) — read <absolute path> before doing anything else`.
- Update the existing file and line. Never add a second one.

## 7. Report back

Tell the user:
- the home repo and the file path
- where the pointer went (`CLAUDE.md`, or the memory entry for which directory)
- the commit SHA
- whether the push was verified

If a step was skipped, say which step and why.
