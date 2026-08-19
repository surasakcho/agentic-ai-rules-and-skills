# A successful download is not data — open the file and look at it

**Task type:** data engineering — any ingest that fetches files from an external source.
**Related:** [`status-fields-must-be-earned`](status-fields-must-be-earned.md) — verify at the
moment of acquisition; this is what to verify when the source declares nothing to check
against. [`completeness-checking`](completeness-checking.md) — what the resulting gap looks
like downstream, and why it hides. [`text-encoding`](text-encoding.md) — mangled text is one of
the tells below.

---

## The rule

**Every downloaded file gets inspected for whether it looks like the thing you asked for.
Report anything unexpected, and treat it as a defect to be handled — never as an input to
carry on with.**

The check is not "did the download succeed". It is "is this the data".

## HTTP 200 is not success

A server under load, behind a WAF, rate-limiting, or simply erroring will return a **200 OK**
with an error page, a login redirect, a stub, or a truncated response. Every naive guard passes
it:

| guard | why it passes |
|---|---|
| exit code / no exception | the request genuinely succeeded |
| `size > 0` | an error page has a size |
| file exists | it does |
| parses without error | HTML, or a header row with no body, parses fine |
| checksum recorded | it faithfully hashes the wrong bytes |

**And a cache makes it permanent.** A cache check that tests *existence* rather than
*integrity* will serve that stub forever, and every later run looks clean.

## What to check, in order of strength

1. **Records extracted, not bytes received.** The only check that caught the incident below:
   *this file yielded 1 row where its siblings yield ~100.* Assert a minimum record count per
   file, and make zero records a hard failure rather than an empty result.
2. **The source's own declared size**, when the page states one before the click. Free, exact,
   and catches truncation immediately.
3. **The sibling distribution — the check that works when nothing is declared.** You almost
   never fetch one file; you fetch hundreds of the same kind. Sort them by size and look at the
   tails. A file three orders of magnitude off its median sibling is not a small region, it is
   a failure.
4. **Content shape.** Expected columns present, delimiter count per line sane, the header
   matching the schema you were promised.
5. **Text that decodes cleanly.** Mojibake in a name field — `Ã¨.Â¡ÃÂºÃ¨`-style bytes where a
   name should be — is a strong tell that you fetched an error page rendered in the wrong
   charset, not the data file.

## Report it, and make it a defect

An unexpected file is a **finding with an owner**, not a warning to be logged and stepped over.
It gets a defect entry, and the pipeline stops or flags rather than producing a quietly
incomplete output. "The file looked odd so I skipped it" and "the file looked odd so I raised"
lead to completely different datasets six months later.

## The incident — stated because the guard WORKED

An ingest pulls **693 files** — one per region, per year — from a government statistics portal.
Three come back as ~1.3 KB stubs against a median of **83,933 bytes**: a single header line, no
detail rows, and the place name double-encoded into mojibake. The server returns them with a
normal **200 OK**.

Exit code, `size > 0`, file-exists and parseability all pass them. What rejects them is a check
counting **delimited data rows** — 1 against a floor of 5 — because the record count, not the
status code and not the byte size, separates every bad case from every good one with an enormous
margin. The build then **raises** unless that region-period appears in a `KNOWN_UPSTREAM_GAPS`
allowlist carrying per-entry evidence, whose error message names the prior incident it exists to
prevent.

Two things that guard bought, both worth copying:

- An **earlier** version of the check sniffed the file head for the substring `404` and **threw
  away 15 perfectly good regions**, whose population counts happened to contain the digits
  `|4046|`. Content sniffing is not the same as counting records — this rule says *records* for
  a reason, and it was paid for.
- The **third** stub surfaced only once the hard failure was in place. The audit before it had
  found two of the three. **Read any "we checked and found N" as a lower bound.**

The residual damage is genuine but bounded and *known*: two regions have no data for one period,
**102 units**, sitting in the same column as ~651 blanks that are real absence. The source truly
does not publish the breakdown — re-requested live, the responses are byte-identical to the
cached copies while a same-period control returns a full file.

**The cheap screen, worth running over any fetched corpus:**

```python
sizes = sorted((os.path.getsize(f), f) for f in files)
# median 83,933 bytes; three files at 1,250 / 1,283 / 1,291
```

**A postscript on how this rule nearly shipped wrong.** Its first draft asserted the stubs had
been skipped *silently*. They had not. That was inferred from the **data** — clustered nulls,
files present on disk — without reading the code that handled them, which documented the case by
name. The guidance survived; the incident did not. **Verify the mechanism in the code before
writing down what a system does.**

## Guard

- Assert a **minimum record count per file**; zero records raises.
- Compare each file against **its siblings' size distribution**, not against zero.
- Verify against the **source's declared size** wherever the source declares one.
- **Cache validity means integrity, not existence.**
- An unexpected file is **reported and handled as a defect**, never silently skipped.
