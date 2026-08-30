# Shell expansion silently deletes content from anything you publish through a command line

**Task type:** coding — any command that posts, commits, or writes text you composed.
**Related:** [`surgical-verified-change`](surgical-verified-change.md) is verifying the change you
made; this is verifying that what you *sent* is what you *wrote*. The two differ, and only one
of them is visible in your source.

---

## The rule

**Compose any body destined for a command through a QUOTED heredoc delimiter, and verify the
published artifact afterwards.**

```sh
cmd --body-file f.md   # f.md written via  <<'EOF'   quoted -> nothing expands
git commit -F -        # body via          <<'MSG'   quoted -> nothing expands
```

**The dangerous forms look identical in a diff:**

| form | expands? |
|---|---|
| `<<'EOF'` | no — `$`, `` ` ``, `\` all literal |
| `<<EOF` *(unquoted)* | **yes** |
| `--body "…"` *(double-quoted)* | **yes** |
| `--body '…'` *(single-quoted)* | no, but a single quote in the text ends it |

## Why this is worse than an ordinary bug

**The deletion is invisible in the source you wrote and appears only in the artifact you
published.** Reading your own command back shows the text intact. The damage exists solely in
the thing other people read.

And **the command succeeds.** Expansion failures go to stderr while the exit status stays `0`,
so nothing downstream notices:

```
$ B="gate `100,000 in profit` settled"; echo "$B"
sh: 100,000: command not found          <- stderr, ignored
gate  settled                            <- the figure is GONE, replaced by a space
```

A backtick-wrapped figure is not mangled or escaped into visible noise. **It is removed**, and
what remains reads as a fluent sentence that simply never contained the number.

## The incident

A financial threshold was deleted from a message to a project's decision-maker, inside a comment
whose entire purpose was **correcting an earlier claim that had understated what was
outstanding**. The figure sat in backticks — the natural way to write a value in Markdown — in a
double-quoted `--body`. The published comment read `gate  settled`.

The correction was correct. The correction of the correction was needed because the tooling ate
a number, in a message about not dropping things.

## The tell — positive evidence, not absence of damage

**A surviving `$(...)` in the published artifact proves the body was never expanded.** Absence of
visible damage proves nothing, because a deletion leaves no artifact.

```sh
$ cat <<'EOF'
canary: $(hostname)
EOF
canary: $(hostname)     <- literal: safe
                        <- had it expanded, this would be the machine's name
```

Put a canary in the body while testing a new posting path, then look for it in the **refetched**
artifact.

## Guard

| | |
|---|---|
| **Compose in a file** with a quoted delimiter; pass `--body-file` / `-F` | removes the shell from the path entirely |
| **Refetch and verify** anything published — count the figures, don't scan for them | the source is not evidence of what was sent |
| **Grep the artifact for what must survive** — a number, a threshold, a scope | a checked count is a check; a glance is not |

**Never trust a visual read of your own outgoing text.** You will read what you meant.

## Verification has a lifetime — arrange it before you publish, not after

Two checks are available, and they are not interchangeable:

| check | strength | availability |
|---|---|---|
| **Canary** — a `$(...)` in the body; look for it literal in the refetched artifact | proves no expansion occurred | always |
| **Byte-diff** — refetch the published body, `diff` it against the composed source | proves the artifact IS the source | **only while the source still exists** |

The byte-diff is exact and is the one to prefer. But it depends on an artifact that scratch
cleanup deletes, and the moment it is gone the only fallback is reading the published text and
calling it fine — **which is precisely the worthless check this rule exists to replace.** A
deletion leaves no trace, so a mangled body and a correct one look identical, and "I looked and
it seemed right" is the same non-check either way.

> One session's byte-diff succeeded only because its scratch files happened not to have been
> cleaned up yet. Had they gone, it would have fallen back to a visual read and published a
> false negative — after having correctly identified that the visual read was worthless.

So the practice is not "diff afterwards". It is **keep the composed body until the artifact is
verified, then clean up** — a decision made before publishing, not a step remembered after.
Expect one trailing-newline difference; some hosts append one.

*The canary is cheap and always there; the byte-diff is exact and perishable. Use the canary
when you did not arrange for the other one.*
