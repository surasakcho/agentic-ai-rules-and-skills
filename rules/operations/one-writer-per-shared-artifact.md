# Every shared artifact has exactly one writer, named at design time

**Task type:** operations — any file, branch, table, or endpoint that more than one process,
host, or schedule can mutate.
**Related:** [`ask-before-overwriting-uncommitted-work`](../coding/ask-before-overwriting-uncommitted-work.md)
— the interactive case of the same loss. [`never-reseat-a-value-silently`](../data-engineering/never-reseat-a-value-silently.md)
— what a second writer does to a value on its way past.

---

## The rule

**For every mutable artifact two processes can reach, decide which one owns it, write that down,
and enforce it in code.** Two uncoordinated writers is a defect on sight — not a risk to monitor,
not a race that is unlikely to hit, a defect.

Enforcement means a host check, a lease, or a lock. **Not a convention, not a comment, and not
"it only runs on one machine"** — that last one is an assumption with an expiry date, and the
second machine is usually added by somebody solving an unrelated problem who never reads the
comment.

## The incident

One modest system accumulated **four instances of this single root cause**, each discovered
separately and each initially diagnosed as something else:

**1. A liveness file written by both hosts.** A primary and its standby each wrote their
heartbeat to the same shared file. Each overwrote the other, so neither could determine whether
the other was alive — the file always looked fresh. The failover mechanism's core signal was
structurally incapable of carrying the information it existed to carry. Replaced with a
single-owner lease.

**2. A backup script that ran on the wrong machine.** It copied the local machine's
configuration *over* the repository's copy and pushed. On the intended host that is a backup. Run
on the standby — whose configuration was a frozen image baked at build time — it rewrote the
backup **backwards** and pushed the result. **One such commit cut the governing configuration
document from 226 lines to 174.** The push succeeded. Nothing failed. Fifty-two lines of standing
instructions were deleted by an automated job and stayed deleted until a human read the file.

**3. A shared branch written by two scheduled jobs on two hosts, neither pulling first.** Once
both were live, divergence was guaranteed, and thereafter the nightly push was rejected every
night — see [`silence-must-be-the-alarm`](silence-must-be-the-alarm.md) for how long that went
unnoticed.

**4. A metadata file rewritten wholesale by concurrent processes.** A long-running fetch and a
streaming collector both regenerated the same index. Mitigated with atomic replace via a
**pid-unique** temp name — a fixed temp filename would merely have moved the race.

**Cost:** the one that can be measured is 52 lines of a governing document silently destroyed and
published by an automated job. The others cost a failover mechanism that could not detect
failure, and three nights of unbacked-up configuration.

## Why this is easy to get wrong

Every one of these was correct when written. Each had exactly one writer at the time. **The
second writer arrives later, added by someone solving a different problem, who has no reason to
audit what else touches the artifact** — and nothing about adding a second writer looks like
modifying the first.

It is also invisible in code review of either side. Each writer, read alone, is correct. The
defect exists only in the pair, and no file contains the pair.

## Guard

- **Name the owner in the artifact's own vicinity** — the file's header, the job's docstring, the
  schedule entry. "Written by X only" is a claim that a reader can check and a second writer's
  author will actually encounter.
- **Enforce with a host guard where ownership is per-machine.** It is one line, it costs nothing,
  and it converts a silent data-destroying run into a no-op:

  ```sh
  [ "$(hostname)" = "$OWNER_HOST" ] || { log "not the owner — skipping"; exit 0; }
  ```

  Make the override explicit and loud, so a genuine ownership transfer is a decision rather than
  an accident.
- **Read-modify-write across processes needs atomic replace with a *unique* temp name.** A fixed
  `.tmp` name is not a fix; it is the same race with extra steps.
- **When two hosts must coordinate, use a lease with a single owner, not a shared mutable file.**
  A file both parties write records neither of them.
- **Before adding a writer to anything, ask what else writes it** — and search rather than
  recall. This is the question whose omission produces every instance above.
- **A shared branch is a shared artifact.** Two automated jobs pushing to one branch without
  pulling is the same defect as two processes writing one file, and it presents identically:
  fine, fine, fine, then permanently broken.

---

*Earned from:* four separate instances of uncoordinated writers in one small system — a heartbeat
file both hosts overwrote, a backup script that rewrote its own backup backwards from the wrong
machine and pushed it, a branch two schedules diverged, and a metadata index two processes
regenerated concurrently.
