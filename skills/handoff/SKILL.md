---
name: handoff
description: Write a handoff document so a fresh agent can continue the work, saved as a new dated file in the repo's handoffs/ folder, then committed and pushed so it survives a reboot and reaches any machine.
argument-hint: "What should the next session focus on?"
disable-model-invocation: true
---

Write a handoff document that summarises the current conversation, so a fresh agent can continue the work.

**The handoff must survive.** Never save it to OS temp (`/tmp` is RAM-backed on some hosts, so a reboot deletes it) or to Claude memory. Never write it into `CONTEXT.md`: that file is a domain glossary, and session notes don't belong there.

## 1. Pick the file

- Write to `<repo root>/handoffs/YYYY-MM-DD-HHMM.md`, using the current UTC time. Create `handoffs/` if it doesn't exist.
- Always create a **new** file. Never overwrite an earlier handoff, because it is the record of what the previous session knew.
- If `handoffs/` already has files, name the most recent one in a **Supersedes** line, and say which of its points are now out of date.
- If the working directory is not a git repo, write the file anyway, then tell the user it is not durable and ask where it should live.

## 2. Write it

- **Next session focus.** If the user passed arguments, they describe what the next session will work on, so tailor the whole document to that.
- **State now.** Say what is done, what is in progress, and what is blocked or on hold, with the reason for each.
- **Standing constraints.** List the instructions the user gave this session that the next agent must keep following, including corrections to your own behaviour.
- **Unverified.** List the claims you did not check, and label them unverified.
- **Suggested skills.** Name the skills the next agent should call the Skill tool for, and say why.
- **Reference, don't duplicate.** Anything already in specs, plans, ADRs, issues, comments, commits or diffs gets linked by path or URL, not copied.
- **Redact** secrets and personal information: API keys, passwords, tokens, private keys, email addresses.
- **Carry over stranded facts.** If this session learned something that exists nowhere durable yet (a research result, a measurement), write it into the handoff or post it where it belongs, then link it. A handoff is often the only place such a fact would otherwise survive.

## 3. Commit and push

1. **Check the repo's rules first.** Read the repo's `CLAUDE.md` and any earlier handoff. If they limit commits or pushes (for example "no commits to main" or "WIP branch only"), follow those limits. If committing isn't allowed, leave the file uncommitted. If committing is allowed but pushing isn't, commit without pushing. Either way, tell the user the handoff exists only on this machine, and stop.
2. **Stage only the handoff file.** Never run `git add -A`.
3. Commit with `docs: handoff YYYY-MM-DD-HHMM`.
4. Push to the current branch's upstream. If the branch has no upstream, report that and don't create one without asking.
5. **Verify the push actually reached the remote.** `git status -sb` should show nothing ahead, or `git ls-remote` should show the new SHA. A push command returning is not proof.

## 4. Report back

Tell the user three things:
- the file path
- the commit SHA
- whether the push was verified

If a step was skipped, say which step and why.
