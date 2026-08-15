# Write research and ad-hoc findings to disk, not to chat

**Task type:** research — source discovery, feasibility checks, one-off questions.

---

## The rule

**Every research task produces a written log in the repo, including the sources examined.** A
finding that exists only in a chat reply is lost at the end of the session. Research is the
most expensive work per unit of output and the easiest to accidentally repeat.

One file per question, committed like any other output.

## What a research log must contain

- **The question as scoped, and the date.** Web sources rot; an undated finding cannot be
  trusted later.
- **A source table** — one row per source *actually examined*: name, exact fetchable URL (not
  a homepage), what it provides, coverage, format, size, licence, and **access status verified
  from this machine** (HTTP code, whether it was actually downloaded, whether a proxy blocked
  it).
- **Sources rejected, and why.** A rejected source is a result. Without it, the next session
  re-evaluates the same dead end.
- **Negative and blocked results, stated plainly.** "This does not exist at this granularity"
  and "this host is blocked from here" are among the most valuable things research can
  establish. Never omit them because they feel like failure.
- **What was verified firsthand versus taken on trust.**
- **Open questions**, and the decision each one blocks.

> **Incident.** A source search established that no time-varying road dataset existed at the
> required granularity for the country in question — the national agencies publish annual
> totals only, and the global alternatives are static. Because that negative result was
> written down with the specific agencies checked and what each publishes, a later session did
> not repeat the search. It built a *control* for the known measurement artifact instead.

## Ad-hoc questions are where the findings hide

Log every ad-hoc question and its answer, newest first, with the evidence or file references
that support it. These arrive in passing during other work and are lost when the session ends
unless captured in the same turn they are answered.

Log the **substance**, not the transcript — enough that the finding is useful months later
without re-deriving it.

## Stale logs are defects

When a source moves, a licence changes, or a finding is superseded, **update the log** — do
not leave a second, contradictory file. Anything a research log asserts is liable to be quoted
back as fact by someone later, so a wrong log actively causes harm.

## Licences are decisions, not details

Record the licence of every source at the moment you evaluate it, because it can disqualify a
technically superior option.

> **Incident.** The best available bare-earth elevation product was rejected on licence, not
> quality: its NonCommercial + ShareAlike terms would have made derived columns adapted
> material, with the clause potentially propagating to how the whole dataset could be
> published. A weaker method was used instead, and the rejection was recorded **as a rejection
> on licence** so nobody re-evaluates it as a quality question.
