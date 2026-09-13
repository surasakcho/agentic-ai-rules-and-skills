# A reference that names its own version is checked at that version — not against now

**Task type:** how we work — verifying links, citations, dependencies or any reference that carries
a version in it. Also writing the checkers that do it.
**Related:**
[`discriminate-by-executing-not-inspecting`](discriminate-by-executing-not-inspecting.md) — the
family this belongs to, and the distinction worth holding: that rule is a true number about the
wrong **object**. This is a true number about the right object at the wrong **version**.
[`a-remembered-claim-is-not-a-checked-one`](a-remembered-claim-is-not-a-checked-one.md) — the
neighbouring failure where no check ran. Here one did, correctly, against the wrong thing.
[`validations-must-fail`](../testing/validations-must-fail.md) — the `"404"` guard that discarded 15
good regions. Same direction of error: a check that manufactures work.
[`retrieve-lessons-weekly`](retrieve-lessons-weekly.md) — the pin this rule protects, and why
holding a stale pin can be the correct state.

---

## The rule

> **When a reference names a version — a commit sha, a tag, a digest, a lockfile entry, an archived
> snapshot, a version segment in a URL — resolve it AT that version. Checking it against current
> state does not test the reference; it tests something the reference was deliberately built not to
> depend on.**

## The pin exists so that later change cannot break it

That is the whole point of pinning, and it is why this error is not a near miss. A sha-pinned link
survives every rename, move and deletion that follows it — permanently, by construction. So a check
that resolves the path against `HEAD` is **measuring a property the artifact is designed not to
have**, and every rename in the repo's future will make it report more failures.

**The failing check and the healthy artifact are the same fact seen from two angles.** The more
reorganising a repo does, the more pinned links it accumulates that a HEAD-check calls dead — which
is exactly backwards, because heavy reorganisation is the condition pinning was chosen for.

## The incident

> A sweep over **696 links across 13 repositories** reported that one repository carried **23 dead
> links**, attributed to a directory merge — `rules/agent-workflow/` → `rules/how-we-work/`.
> It was posted to a public issue as a finding.
>
> It was false. The links were `blob/<sha>/<path>`. The check asked whether `<path>` existed on
> local disk **at HEAD**; a sha-pinned link does not name HEAD. `git ls-tree -r <sha> --
> rules/agent-workflow/` returns all 23 files and the live URLs return 200. **The rename could not
> have broken them, because that is what the pin is for.**
>
> Caught by a second party checking the claim, and retracted publicly on the same issue.

**Cost:** a false finding published under a repository's name, a retraction, and the work of two
sessions — all of it manufactured.

## The direction of error is what makes it dangerous

**This class fails toward more work, and it reads as diligence.** A false "23 links are dead" is
acted on immediately: someone opens 23 files. Nobody asks whether the checker was right, because a
checker reporting problems is doing what checkers do, and a checker reporting nothing is the one
that attracts suspicion.

So the usual defence — *"we would have noticed if it were wrong"* — is inverted here. **You notice a
check that is silent. You obey a check that is loud.**

## A stale pin is not a defect — the defect is a pin the citing sentence has outrun

The corollary, and it is what keeps this rule from generating work rather than saving it. **An older
SHA is a perfectly stable link.** That is the whole reason it was pinned. So "this link is behind"
is not a finding, and a sweep that reports it as one is manufacturing exactly the work this rule
warns about.

**The predicate that splits them is one command:** `git diff <link's sha>..<current> -- <the linked
path>`. Empty means the linked file has not moved and the citation still says what it said. Non-empty
means the reader is sent to a version that may no longer support the sentence citing it.

> **Measured across one estate:** 14 files carrying a managed block, 8 prose links into the shared
> repo, **7 not at their own file's current pin — and only 4 of those 7 were defects.** Three were
> legitimately stable. One of the four pointed at a document that had since gained a slug-rename
> paragraph, a retracted count, and a sentence the citing text did not know about.

**Tool-managed regions do not cover prose.** A repin moves the block and nothing else, so every
hand-written link beside it drifts silently — visible to nobody, because the managed part is
correct and the file looks maintained.

## Where it hides

Anything that carries its own verification context:

| reference | checked at |
|---|---|
| `blob/<sha>/<path>`, `raw/<tag>/…` | the sha or tag, via `git ls-tree` / the live URL |
| a lockfile entry, a vendored dependency | the locked version, not the registry's latest |
| a container image digest | the digest, not the moving tag that once pointed at it |
| a docs URL with a version segment | that version's docs |
| an archived or DOI'd citation | the snapshot, not the live page |
| a quoted line number in a file | the commit it was read at |

## Guard

- **Read the version out of the reference before you resolve it.** It is in the string. The check
  that ignores it is not a weaker check, it is a different one.
- **Resolve at the pin:** `git ls-tree -r <sha> -- <path>`, `git show <sha>:<path>`, or fetch the
  pinned URL. All are one command and all are cheaper than the retraction.
- **Before publishing a count of failures, resolve ONE by hand.** A single manual check on a single
  reported failure would have ended this incident before it was posted, and the cost is seconds
  against a count you are about to put someone else's name on.
- **When a checker's findings scale with how much a repo has been reorganised, suspect the
  checker.** That correlation is a symptom of the wrong-version error, not evidence of decay.
- **Writing one? Strip nothing and assume nothing about context.** A link inside a fenced block or
  between backticks is a *template*, not a link; a link carrying a sha is resolved at the sha. Both
  are the same mistake — reading a reference without its own context — and both produce confident
  false failures.

---

*Earned from:* a sweep of 696 links across 13 repositories that reported 23 dead ones in a public
issue, caused by a directory rename. The links were sha-pinned and the check resolved them against
HEAD, so it measured the exact property the pin exists to remove. Found by a second party checking
the claim, retracted on the same issue. Alongside it, the same class in the same afternoon and in
this corpus's own tooling: a link checker that read a `](link)` placeholder inside a fenced template
as a real link, and — after that was fixed — read the identical placeholder quoted between backticks
one hour later.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'any reference resolver in the repo, and whether it extracts a version from the reference before resolving: a link matching blob/<sha>/ or raw/<ref>/ resolved against the working tree, a dependency checked against a registry latest rather than the lockfile pin, an image tag resolved where a digest was written'
trigger: 'pre-commit lint on checker code, plus a self-test case per resolver'
check: 'AST or grep: a resolver that matches a versioned reference pattern and then tests existence against the working tree or HEAD -> block; a link-checking resolver with no test case for a sha-pinned target -> block; a findings report whose count scales with rename activity -> advise'
escape: 'resolve at the named version, or declare the resolver as current-state-only and exclude versioned references from its input rather than failing them'
narrows: 'gates the RESOLVER, which is where the defect is reproducible. It cannot catch a human reading a pinned reference and checking it against now - the incident was a person running a sweep, not a committed tool - and it cannot tell a correctly-resolved-but-genuinely-dead pin from a live one without fetching'
```
