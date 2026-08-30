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
