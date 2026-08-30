# A pull request with no reviewer is invisible, however open it is

**Task type:** how-we-work — any time an agent opens a PR against a repository a human owns.
**Related:** [`silence-must-be-the-alarm`](silence-must-be-the-alarm.md) — there the report has
no reader; here it has no *route*. [`open-decisions-go-in-the-tracker`](open-decisions-go-in-the-tracker.md)
— a PR awaiting a merge decision is an open decision, and the same burial applies.

---

## The rule

**Every PR opened against someone else's repository names them as reviewer at creation time,
in the same command that opens it.** Not afterwards, not when someone asks where it went.

```sh
gh pr create --title … --body-file … --reviewer <owner> --assignee <owner>
```

An agent working under a bot identity is always in this case: it is never the repository owner,
so its PR is never routed by default.

## The incident

An agent working under a bot account opened a PR against its operator's public repository, from
a fork, and reported it as done. It was open, mergeable, correctly authored, and carried a
reviewed rule. **The operator could not find it.**

Nothing was broken. `reviewRequests` and `assignees` were both empty, and the author was the bot
rather than the human — so the PR missed **every** default filter the GitHub mobile app and web
dashboard use to build a person's list: *authored by you*, *assigned to you*, *review requested
from you*. It sat in a state visible only to someone who already knew the URL.

A sweep of the same owner's other repositories then found a **third party's** PR in the identical
state: opened months earlier by an outside contributor, no reviewer, no assignee, and therefore
never surfaced to the owner at all.

**Cost:** a reviewed and mergeable contribution stalled indefinitely, and the discovery that the
same hole had already swallowed somebody else's contribution to a different repository.

## Why this is easy to get wrong

**"Open" reads as "delivered."** The PR exists, its URL resolves, CI is green, and the reporting
agent has a link to paste. Every signal available *to the author* says the work arrived. None of
those signals is the one that matters, which is whether it appears in a list the reviewer
actually opens.

The failure is also invisible from the author's side **permanently**. The author sees their own
PR in their own dashboard, because they authored it. Nothing about the view from inside
distinguishes a routed PR from an unrouted one.

And it compounds with good behaviour: an agent that correctly avoids pushing to `main` and opens
a PR instead has, without a reviewer, converted a visible commit into an invisible one.

## Guard

- **Put `--reviewer` in the `gh pr create` command itself**, alongside `--title`. A follow-up
  step is a step that gets skipped when the turn ends early.
- **Add `--assignee` too.** Reviewer and assignee populate different filters, and GitHub will
  not let an author request review from themselves — the assignee is what survives that case.
- **Report the PR by what it is routed to, not that it exists.** "Open, review requested from
  X" is a status; "opened PR #8" is not.
- **Sweep periodically for the ones already lost:**
  ```sh
  gh search prs --owner <owner> --state open --json number,author,repository,url
  ```
  then check `reviewRequests` and `assignees` on each. Unrouted PRs accumulate silently and
  nothing will ever report them.
- **An archived repository refuses assignment but still accepts a review request.** Do not treat
  the first failure as the whole operation failing.

---

*Earned from:* a bot-authored fork PR that its operator could not find in their GitHub app,
because no reviewer or assignee was ever set — and a sweep prompted by that which found an
outside contributor's PR sitting unrouted in another repository of the same owner.
