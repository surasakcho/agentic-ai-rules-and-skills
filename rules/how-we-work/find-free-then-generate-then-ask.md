# Find it free, then generate it, then ask — and record what the licence actually permits

**Task type:** how we work — any task that needs an asset it does not have: an image, icon, font,
texture, sound, model, sample dataset.
**Related:**
[`a-blocked-list-is-a-fact-about-a-moment`](a-blocked-list-is-a-fact-about-a-moment.md) — the same
failure one level up. A missing asset that a search would have produced is not a blocker, and
handing the choice upward is the forbidden output of that rule wearing different clothes.
[`cannot-is-a-task`](cannot-is-a-task.md) — *"I need an asset"* is a requisition only after the
route has been looked for.
[`research-and-qa-logs`](../research/research-and-qa-logs.md) — *"licences are decisions, not
details"*, recorded there for research **sources**. This rule is the same discipline for shipped
**assets**, where the consequence lands on a published artifact instead of on an analysis.
[`prompt-and-store-config`](prompt-and-store-config.md) — the provenance record is a stored fact,
not something the next session re-derives.

---

## The rule

> **When work needs an asset, go in this order and stop at the first branch that works:**
>
> 1. **Find one that is free and openly licensed**, and **pick one**.
> 2. **Generate it yourself** if nothing suitable exists.
> 3. **Ask** — and only for what money or identity buys, never for what a search would have found.
>
> **Record the source and the licence beside the asset, always.**

## Branch 3 is for what a person can supply that you cannot

A question spends someone's attention, and a question about a freely downloadable file spends it on
a decision they have **no information to add to**. They would run the same search. The only things
that genuinely need them:

- **money** — anything paid, and anything on their accounts
- **identity** — anything requiring their name, login, signature or agreement to terms
- **a licence unclear enough that being wrong would be theirs to answer for**

Everything else on that list is a search you have not run.

## Select one. A shortlist handed upward is not a decision made

**The judgement clause is the part most likely to be softened, so it is stated as a prohibition:**
never present three candidates and ask which. That is not diligence, it is the choice returned
unmade with research attached — and it costs more than asking plainly, because the reader now has to
evaluate your three options as well as make the call.

Pick the one that fits. Say in one line why, and what you rejected. If it turns out wrong, it is a
swap, not a rework — which is precisely why the decision was never worth escalating.

## ⚠️ Free to DOWNLOAD is not free to USE

This is where the rule earns its keep. The directive removes a question; **the risk it creates is
not a bad choice, it is an unattributed file** — and that risk surfaces at publication, long after
the download, when it belongs to whoever shipped it.

- **The word "free" on a download page is not a licence.** It describes the price of the download,
  and says nothing about redistribution, modification, commercial use, or training.
- **Read the licence against the actual use.** Will this be published? Sold? Modified? Redistributed
  inside a product? Fed to a model? A licence that permits one of those does not imply the rest.
  **NonCommercial and ShareAlike are the two that most often disqualify a technically perfect
  asset**, and ShareAlike can propagate to the work that embeds it.
- **Clean, in the normal case:** CC0, public domain, MIT, Apache-2.0, OFL, and explicit
  commercial-use grants.
- **Attribution required means attribution rendered**, in the artifact, before it ships. A
  requirement you recorded and did not satisfy is worse than one you never read, because the record
  proves you knew.

### A clean licence is not the whole permission

Some assets carry a *second* right that the licence does not speak for, and this is the case most
often missed because the licence page looks green:

- **a recognisable person** — a permissive photo licence is not a model release, and commercial use
  of a likeness is a separate permission
- **a trademark or logo** — trademark survives any file licence
- **a landmark, artwork or product** with its own restrictions

When the asset contains one of those and the use is public or commercial, it belongs in branch 3.

## Record it beside the asset, at the moment you take it

A file with no provenance is a liability somebody inherits, and the person who inherits it cannot
reconstruct what you saw. At minimum: **source URL, licence identifier, the date, and the required
attribution text** if there is one. Beside the asset — in a manifest in the same directory, not in a
chat message and not in a commit body that the next reader will not think to search.

**A generated asset gets the same record**: the tool, and the terms under which its output may be
used. "We made it" is a provenance claim like any other, and the terms attached to generators change.

## Guard

- **Search before you ask.** The question that names no search is the one to catch in your own draft.
- **Never return a shortlist as the answer.** Pick, say why in a line, name the runner-up.
- **Never record "free" as a licence.** Record the identifier, or record that it is unclear — and if
  it is unclear, it is branch 3.
- **Check the licence against the specific use**, not against the general idea of using it.
- **Attribution is shipped, not noted.**
- **Ask when the asset carries a person, a mark, or a price** — those are the branch-3 cases, and
  they are not rare enough to treat as exceptions.

---

*Earned from:* an operator directive — *"anything that needs an asset, find free first; select one
with your judgement; no need for my input for anything blocked that is freely available from the
internet"* — issued to a media-production Sector after sessions stopped on assets that a search
would have settled. The provenance half is not in the directive: it is the risk the directive
creates, and it is the half that is expensive later, since an unlicensed file is discovered by
whoever publishes it rather than by whoever downloaded it.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'three things: an asset file added to the repo (image, font, audio, model, media) with no provenance entry carrying a source and a licence identifier; an outgoing message asking the user to supply or choose an asset with no search performed in the session; and a message presenting two or more candidate assets and asking which to use'
trigger: 'pre-commit for the provenance half, Stop for the asking half'
check: 'a new binary or media file staged with no accompanying manifest row naming source and licence -> block; a licence field whose value is free, unknown or a bare URL -> block; msg asks the user to supply an asset and no search occurred this session -> refuse; msg presents 2+ candidates and asks the user to choose -> refuse, naming this rule'
escape: 'record the licence identifier, which is the rule own prescription; an asset that genuinely needs a person - paid, identity-bound, unclear licence, or carrying a likeness or mark - is asked for with the reason named, and that message passes because it names what a search cannot settle'
narrows: 'gates that a licence was RECORDED and that the question was not asked before a search. It cannot read the licence, cannot tell whether it permits the specific use, and cannot see the second-permission cases at all - a recognisable person or a trademark under a clean file licence passes every predicate here. The choosing half is judgement and only its worst shape, the shortlist returned upward, is mechanically visible'
```
