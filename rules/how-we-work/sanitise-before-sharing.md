# Sanitise before sharing

**Publishing is a one-way door.** A lesson extracted from private work carries the private
work with it unless someone actively strips it out. Nobody does that by accident, and no
existing rule about *what is worth sharing* also answers *what is safe to share* — the two
questions feel like one and are not.

---

## The incident

This repo was seeded with 9 rules, 2 skills and 2 lesson write-ups harvested from a private
research project, then made public. Every rule was reviewed for portability. **None of them
was reviewed for disclosure.** A re-check hours later found three separate classes of leak
already pushed:

| What leaked | Where | Why it mattered |
|---|---|---|
| The private repo's name — which contained a **collaborator's given name** | `lessons/_review-log.md` | Named a real person and their unpublished project in a public repo |
| The **machine username and local directory layout** | two paths in a skill's `SKILL.md` | `C:/Users/<name>/Repos/...` as a documented example command |
| A project-internal defect write-up: **real variable names, real counts, and preliminary results** from an unpublished study | `lessons/<date>-…​.md`, published in full alongside its own de-identified version | Disclosed someone else's unpublished findings; the de-identified version published next to it made the anonymisation pointless |

**Cost:** a public repo carrying a third party's unpublished research for several hours, and
a history rewrite to remove it. Caught only because the owner thought to ask.

**The tell:** the de-identified version and the raw version were *both* published. Whoever
prepared it understood that de-identification was needed and still shipped the original.
That is what an unchecked step looks like — the intent was there, the gate was not.

---

## The rule

> **Before anything leaves a private context for a public one, scan it for four things:
> people, places, paths, and findings.** The scan is a separate pass from the
> is-this-worth-sharing pass, and it happens last.

**People.** Names, usernames, emails, handles, org names. A repository name can be a person's
name. So can a directory.

**Places.** Private repo names, internal hostnames, bucket names, ticket IDs, dashboard URLs,
Slack channels. These are not secrets, but together they map an organisation.

**Paths.** Absolute paths publish a username, an OS, and a directory layout, and they are the
single most common leak because they arrive as *helpful example commands*. In shared code and
docs, paths are arguments with placeholder names — never literals.

**Findings.** The hardest one, and the one that actually harms someone. A lesson about
*process* almost never needs the result that surrounded it. If a write-up carries real
variable names, real counts, effect directions, significance levels or sample sizes from
unpublished work, it is publishing that work. Strip it to the mechanism; the mechanism is the
part that was portable in the first place.

## Two corollaries that carry most of the weight

**Never publish the raw and the redacted version side by side.** The redacted one exists
because the raw one cannot be shared. Shipping both is not caution, it is disclosure with an
extra step. The raw write-up stays in the originating repo.

**Someone else's unpublished work is not yours to share, even in fragments.** Portability is
your call; disclosure is theirs. When a lesson comes from collaborative or client work and you
cannot strip it to pure mechanism, **ask them or drop it** — do not publish a version you
judged to be probably fine.

## Mechanise it

`prose < checklist < test < gate`. Most of this can run:

- `lesson-review`'s `harvest.py --check` scans the shared repo for absolute paths, emails,
  usernames and a configurable denylist of private terms, and exits non-zero. Add the private
  repo names, collaborator names and internal hostnames to `--deny` so the gate is specific to
  what you actually need to keep out.
- It also rejects relative links that resolve **outside the repo root**. A `../../CLAUDE.md`
  in a published file silently resolved to a file on the author's machine and the link checker
  called it valid — the leak and the false pass came from the same line.

What cannot be mechanised is the findings check: only a reader knows whether a number is a
result. Do that one by hand, deliberately, and say that you did.

## What "sanitised" looks like

- [ ] no absolute paths, usernames or emails anywhere in the repo
- [ ] no private repo, host, bucket or ticket identifiers
- [ ] no personal names beyond the repo owner's own public handle
- [ ] every quoted number is about the *defect*, not about the *result*
- [ ] no raw write-up published alongside its redacted version
- [ ] every relative link resolves inside the repo
- [ ] for anything from collaborative work: consent, or stripped to pure mechanism

Related: [publish-lessons-weekly](publish-lessons-weekly.md) decides *what* gets shared; this
rule decides what that thing may *contain*. Run this one second, and treat it as blocking.
