# A version string cannot detect drift — compare an identity the content derives

**Task type:** how we work — updating a dependency, plugin, skill pack or vendored copy; and any
claim of the form "these two copies are the same" or "this one is current".
**Related:**
[`a-pinned-reference-is-checked-at-its-pin`](a-pinned-reference-is-checked-at-its-pin.md) — the
nearest neighbour and a useful contrast: there the reference names a version and the check resolves
it against the wrong one. Here the check resolves the right field and the field cannot tell the two
apart.
[`discriminate-by-executing-not-inspecting`](discriminate-by-executing-not-inspecting.md) — the
family. A true number about the wrong object; this is a true number that is the same for both
objects.
[`status-fields-must-be-earned`](../data-engineering/status-fields-must-be-earned.md) — *an
unqueried hash is decoration*. This rule is the case where the hash was recorded, sat one line
below the field that was read, and was never queried.
[`count-the-join-not-the-inventories`](count-the-join-not-the-inventories.md) — the second incident
below is a count taken from the wrong population.

---

## The rule

> **Before using a field as evidence that two copies differ, ask what it would read if they DID
> differ in the way you care about. A version string is AUTHORED — it changes when a human
> remembers to change it — so it cannot discriminate between two different contents that both claim
> it. Compare an identifier the content DERIVES: a commit sha, a digest, a content hash.**

An authored label and a derived identity look equally authoritative in a report. Only one of them
is a function of the bytes.

## The incident

A plugin was installed from one marketplace, and the estate later re-pointed every machine at a
different marketplace carrying the same plugin. The question that mattered — *is what I am running
the same content?* — was asked of the version string.

**Three different commits all called themselves `1.2.3`.** Two machines sat two commits behind the
marketplace head, and on both of them:

```
$ claude plugin update <plugin>
already at the latest version (1.2.3)
```

The updater compares the version string. Refreshing the marketplace cache first changed nothing,
because the cache refresh updated the content and the comparison never looked at content. Only
uninstall-and-reinstall moved the recorded commit.

**The tell was sitting in the install record the whole time**, one line below the field being read:

```json
"version": "1.2.3",
"gitCommitSha": "959a8e9f1edc3adbe2f7e3054bb6fbefa6696260"
```

**And the storage layout says which of the two the tool treats as identity.** The install path is
keyed on the version string alone — `…/<plugin>/1.2.3` — so a new commit at an unchanged version
has no distinct place to land. The data model cannot represent the thing the update check would
need to notice.

> **Verified directly:** the two fields coexist in the install record, and the install path is
> keyed on the version segment. **Attributed, not independently reproduced:** the two-machines
> no-op measurement above is another session's, reported with its before/after shas. It is recorded
> as theirs because this office had a single machine already at head, where the update check
> correctly reports no work and therefore proves nothing — per
> [`a-finding-is-scoped-to-what-you-checked`](a-finding-is-scoped-to-what-you-checked.md).

## Authored versus derived is the whole distinction

| | changes when | can detect drift |
|---|---|---|
| version string, tag, release name, `latest` | a human edits a manifest | **no** — silence is indistinguishable from unchanged |
| commit sha, digest, content hash, mtime+size pair | the bytes change | yes |

A version string is a **promise about** the content, and a promise is only as good as the release
discipline behind it. Vendored copies, forks, mirrors, a maintainer patching in place, and any
`main`-tracking install all break it routinely — and none of them are misbehaviour, they are the
normal life of a package.

**So "already at the latest version" answers a narrower question than the one asked**, and the two
readings are identical in the output. The honest rendering names the field: *already at the latest
version string*.

## The second instance, within the hour, by the reader who had just published the first

The same session then measured the consequence of the re-point by **counting `SKILL.md` files on
disk** in each copy: 38 upstream against 37 in the mirror. It reported the difference as a lost
skill, named it, and escalated it as a decision for the operator.

**The loader does not load files on disk. It loads what the manifest's `skills[]` declares.** Both
copies declare 25, neither declares the named one, and the staging directory the count had swept in
was undeclared in both. Nothing had been lost; there was no decision to make.

A file count looks like a skill inventory and does not discriminate between *shipped* and *present
in the working tree* — the identical defect as the version string, one layer down, committed by
the person who had just written the version-string finding up.

**That is the part worth keeping.** Knowing the shape did not prevent the next instance of it,
because the shape is not recognised from the proxy — every non-discriminating proxy looks fine
while you are choosing it. It is recognised from the **question**, which is why the guard below is
phrased as a question to ask and not as a list of bad fields.

## This corpus had already written the correction down, for this exact repository

The file-count defect was not new here. [`skills/UPSTREAM.md`](../../skills/UPSTREAM.md) records a
fork comparison against the same upstream project that had to be **re-run and reconciled** because
"a first pass used a denominator that counted files as skills" — it overstated this side as 77
against a true 66, and ours-only as 53 against 42. That pass fixed the denominator and wrote the
definition into the policy file in bold.

**It recurred anyway, a few commits later, in another session answering a different question.** And
the reason is the part to take:

> The overlap set was computed by intersecting name lists, and the spurious entries — `README.md`,
> `package.json`, `LICENSE` and six others — could not collide with a directory name. **Had one
> spurious entry been named like a skill, it would have entered the decision set silently.**

A wrong denominator that happens to miss the bucket you act on is not a safe wrong denominator. It
is one whose blast radius nobody measured — and it leaves the method looking validated, which is
what carries it into the next use.

**And the corrected definition is still question-specific, not universal.** *A directory containing
`SKILL.md`* is the right population for deciding what to MERGE from a fork; the manifest's declared
`skills[]` is the right population for deciding what LOADS. Neither is wrong. There is no single
true count of a thing — there is one per consumer, which is why the corollary below is phrased as
*whose* population rather than *the* population.

## The discriminator test

One question, asked before the field is used as evidence:

> **If this had drifted in exactly the way I am checking for, would this field read differently?**

If the answer is no, or "only if someone remembered", the field is decoration and the check cannot
fail. Two corollaries that catch most of it:

- **Count the population the CONSUMER you are answering for reads, not the one the filesystem shows.** Declared set, not
  directory listing; loaded modules, not files present; rows the query returns, not rows in the
  table.
- **When a record carries both an authored label and a derived identity, the derived one is the
  answer and the authored one is the display name.** Read the sha; print the version.

## Guard

- **Never report "up to date" from a version comparison when a content identity is available.**
  Name the field you compared, or diff the shas.
- **An updater that reports no work is not evidence of no drift.** It is evidence about its own
  comparison. Confirm by moving the identity, not by re-running the updater.
- **A refresh that changes the cache and not the comparison changes nothing you can observe.**
  Re-checking after it is a second helping of the same answer.
- **Before counting, say which population the consumer actually reads.** A count off the wrong
  population is wrong in a direction that looks like diligence.
- **Attribute a measurement you did not reproduce.** A corroboration you cannot run is a report,
  not a second data point.

---

*Earned from:* a plugin re-point across an estate, 2026-09-19. `plugin update` reported
`already at the latest version (1.2.3)` on two machines sitting two commits behind, because it
compares the version string while the install record carries the commit sha; only
uninstall-and-reinstall moved it. The same session then counted `SKILL.md` files rather than the
manifest's declared `skills[]`, reported a skill as lost, escalated it for a decision, and
retracted it when the manifest was read — 25 declared in both copies, the named skill in neither.
Caught by a second reader checking the claim against the manifest, which is the same instrument
that has caught every other instance in this corpus: not a mechanism, a second reader.

---

## Enforcement

<!-- machine-readable; verdicts and rationale in docs/gateability.md -->

```yaml
verdict: narrowed
observable: 'a freshness or sameness claim about a fetched artifact, where the artifact record carries both an authored label (version, tag, release name) and a derived identity (commit sha, digest, content hash)'
trigger: 'at the moment the claim is made -- an update check reporting no work, or a report asserting two copies are the same'
check: 'the record carries a derived identity field AND the comparison read only the authored label -> fail, naming both fields. Narrow because it fires only where a derived identity is actually recorded alongside the label; where the source publishes no digest at all, the rule still binds and this check is silent'
narrows: 'the rule covers any non-discriminating proxy, including the file-count-versus-declared-set case in the incident. The gate covers only the version-versus-sha case, because that one has both fields in one machine-readable record; "count the population the consumer reads" has no general form a checker can resolve. The false positive is a deliberate label-only comparison against a source that guarantees immutable releases - a registry forbidding republication of a version - which the check cannot see and will fail; the gate answers it by naming both fields it compared rather than silently blocking'
escape: 'name the guarantee that makes the label sufficient (immutable-release registry, signed tag policy) in the caller, or state the claim as "latest version string" rather than "up to date"'
invoked_by: 'nothing'
note: 'This office specifies gates and does not build or deploy them (charter constraint), so this rule ships as declared debt. implemented_by is OMITTED rather than set to 'nothing' - the checker resolves that field as a locator, so a prose value lands in UNKNOWN (not yet examined) instead of UNGATED (the real, counted gap). Recorded per a-classification-is-not-a-gate: the clause is a specification someone else can build from, not a claim of coverage'
```
