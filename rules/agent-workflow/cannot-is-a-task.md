# "I can't" is a task, not a conclusion

**Task type:** agent workflow — any point where you hit a blocker and are about to report it.
**Related:** [`close-your-own-gaps`](close-your-own-gaps.md) is about gaps you created;
this is about obstacles you found. Both fail the same way: handing unfinished work back.

---

## The rule

**When you cannot do something, the deliverable is a route to doing it — not a note saying you
gave up. If the route needs something only the user can supply, say exactly what, and do
everything around it first.**

This covers every kind of blocker: a source you cannot reach, a tool that errors, a credential
you lack, a format you cannot parse, an API that refuses. In all of them the wrong move is the
same — reporting the obstacle as if it were the answer.

## Before you may report anything as impossible

- **The tools you already have.** Check your own tool list before declaring something out of
  reach. In the incident below, a data portal was documented as blocked to *scripted* clients,
  and the same document named the working route — a live browser session — while a browser
  automation tool sat unused in the session. "Blocked" was true of one method and got reported
  as true of the source.
- **Every alternative, named individually.** Not "there's no other way", but *"tried A, B, C;
  A needs a login, B is three years stale, C does not go below the level I need"*. A named dead
  end is a result. An unnamed one is an assumption.
- **The indirect route.** If the artifact cannot be had, can the *answer* still be derived — from
  metadata, a sibling file, directory names, a checksum, an adjacent version, a file the pipeline
  already reads? Here, directory names nobody had cross-referenced identified the exact missing
  item, and a metadata file sitting beside them dated it.
- **Narrowing the ask until it is small.** "Which version is this" is answerable in a minute.
  "The data differs somehow" is not. Do the work that makes the question precise.

## Then report a route, not a wall

What each step costs, what it would settle, and which single step — if any — needs the user. A
credential, a paid tier, a scope decision: isolate it, do everything else first, so the moment
they act the rest is already in place.

## Asking is not giving up. Abandoning the problem silently is.

The rule is not "never ask" — it is "never stop". An explicit, narrow request with the
surrounding work already finished is a completed handoff. A vague "this isn't possible" is an
abandoned one.

## Why this matters more than it looks

A problem reported as impossible is **closed forever**. Nobody re-opens it, and it quietly becomes
a permanent limitation of the work. A problem reported as "here is the route, here is the one
thing I need from you" gets solved. The entire difference is whether the work of finding the route
was done.

## How the incident resolved

The missing dataset was declared unobtainable and handed back as the user's call. Pushed to look
harder:

1. Directory names in an adjacent data folder identified the exact missing version.
2. A metadata file beside them dated the layer.
3. The blocked page turned out to be reachable; the earlier failure was transient rate-limiting
   from a burst of scripted requests, not a permanent block.
4. The single genuinely human step — a per-item form the user had to submit as themselves —
   took them about ten seconds once everything else was staged.
5. The recovered file reproduced the reference output **exactly**, closing a discrepancy that had
   been open for days.

Every one of those steps was available at the moment I said it could not be done.

---

*Earned from:* declaring a missing dataset unobtainable while holding an unused browser tool, and
without checking directory names or metadata that between them identified it exactly. Both checks
took minutes.
