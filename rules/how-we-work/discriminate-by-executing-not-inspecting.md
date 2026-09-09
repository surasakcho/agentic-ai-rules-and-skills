# Discriminate by executing, not by inspecting

**Task type:** how-we-work — any claim about what a system does, in any project. It applies to
verifying a fix, confirming a deployment, checking a diff, and reporting a number to someone who
will act on it.
**Related:** [`a-finding-is-scoped-to-what-you-checked`](a-finding-is-scoped-to-what-you-checked.md)
— why the artifact near the thing feels like the thing.
[`a-check-that-shares-a-source-is-not-a-check`](../testing/a-check-that-shares-a-source-is-not-a-check.md)
— the sibling failure: right object, wrong *source* for the expectation.
[`review-every-output`](../analytics/review-every-output.md) — "recompute, don't read", the same
instruction for numbers you are about to publish.

---

## The rule

> **A check must run the thing it is checking. Reading an artifact that sits near the thing is not
> a check, however precise the artifact is.**

The failing shape is always the same: **a true number about the wrong object.** Not a guess, not a
sloppy reading — a real measurement, correctly taken, of something adjacent to the question.

The discriminating question is not *"is this number accurate?"* It is **"if the thing I am claiming
were false, would this number be different?"** If the answer is no, the check cannot fail, and a
check that cannot fail has told you nothing by passing.

**The fix is nearly always cheaper than the inspection that replaced it.** Every instance below was
resolved by an execution taking under a minute, and in every case the artifact had been read
*instead of* running that execution, not because running it was hard.

## The incidents

Four in one evening, from three sessions whose explicit task at the time was applying this exact
class of rule. Two more the same morning, same shape.

| the claim | what was inspected | why it could not fail | what discriminated |
|---|---|---|---|
| "8 rules were modified, 5 by name — read this diff carefully" | `git diff --stat`: *11 deletions* | a stat line counts changed lines, not changed meaning; 7 of the 8 had zero substantive lines and every deletion was a link-path fix | reading the diff body: `non_link_lines=0` |
| "the sync notifier reports what landed" | the notifier ran and printed a block | it printed the *branch's* range, empty whenever the branch already sits on `origin/main` — a successful land beside an empty commit list | running it with two worktrees and two commits, and looking at the contents |
| "the recursion guard is fixed" | `hook fired 2 time(s) for ONE commit` | git fires post-commit per replayed commit regardless; the count is 2 before and after the fix | same scenario against both scripts: unfixed **did not land**, fixed **landed** |
| "yf-agent cannot see shared skills" | `docker inspect ... \| grep .claude \| head -3` | `head -3` cut the skills mount out of the list; silence read as absence | enumerating all eight containers and testing the path inside each |
| "97c9933 cannot have the deadlock" | `git ls-tree 97c9933` — no `seedlock.py` | the flock was never the cause; a bare `threading.Lock.acquire()` in an `async def` froze the loop on its own | rebuilding 97c9933 and watching `/healthz` time out 3× |
| "the container is still exploitable" | the deployment that had been *requested* | the recreate was blocked before it ran; no such container existed | asking the daemon what was running |

## Why this is easy to get wrong

**The artifact is genuinely about the right subject.** A `--stat` really does describe that diff. A
firing count really does describe that hook. This is not a category error you can feel — it is a
scope error, and scope errors are invisible from inside because the thing you looked at answered
the question you asked.

**Inspection is fast and feels like diligence.** Reading a stat line is *work*. It produces a number
you did not have before. The cost of the mistake is not laziness; it is that a cheap true fact
crowds out the expensive discriminating one.

**Passing is the ambiguous outcome.** A failing check is informative whatever its quality. A passing
one is only worth what its ability to fail was worth — and nobody examines a green result. Six of
the six instances above were caught by another person or by an execution, never by re-reading.

**Adoption does not help.** All six happened in repos that had adopted the neighbouring rules, cited
them in prose, and pinned them to a commit. Two happened *inside sessions actively applying that
rule to someone else's work.* Knowing the rule is not the control; running the thing is.

## Guard

Before reporting a check as passed, answer in one line: **what would this have shown if the claim
were false?** If you cannot answer, you have an observation, not a check.

Then prefer, in order: run the thing and read its effect · run the two cases and compare · read the
primary artifact in full · read a summary of it. **The last is not a check** — it is a reason to do
one of the first three.
