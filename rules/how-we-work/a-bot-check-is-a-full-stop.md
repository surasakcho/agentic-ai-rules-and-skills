# A bot check is a full stop — owner consent does not convert a bypass into permission

**Task type:** agent workflow — any moment automation meets a control built to detect automation:
a CAPTCHA, a Cloudflare interstitial, a "verify you are human" page, an `is-headless` fingerprint
check.
**Related:** [`cannot-is-a-task`](cannot-is-a-task.md)
— exhaust the legitimate routes first, so what you bring back is a choice and not a shrug.
[`unexpected-means-stop-and-propose`](unexpected-means-stop-and-propose.md)
— the general shape; this is the case where the surprise is a deliberate barrier, not a defect.

---

## The rule

**When a site blocks you because you are automated, stop and say so. Do not spoof the user agent,
do not install a stealth plugin, do not borrow a human-verified session cookie, and do not retry
with different flags to see what gets through.**

The counter-argument arrives immediately and sounds airtight: *the user owns this account, they
explicitly asked, so consent covers it.* It does not, and the reason is worth holding onto:

**The control is not protecting the account from the user. It is protecting the operator's
infrastructure from automation in general.** The account holder is not the party whose consent is
at issue. A user can authorise you to act *as them*; they cannot authorise you to overrule a third
party's decision about what traffic that third party accepts. Those are different permissions and
only one is theirs to give.

The same act is the same act regardless of whose credentials it wears.

## The ratchet is the real failure mode

It is never one decision. Each step looks smaller than the refusal before it:

1. Run it headless. *Blocked.*
2. Set a realistic user agent — "everyone does that, it's not really evasion."
3. Add a stealth plugin — "it just patches the tells."
4. Have the user log in and hand over the session cookie — "no bypass at all, it's their session."

Step 4 is a complete bypass, and it got there in three small increments. Draw the line at step 1,
where it is legible, rather than in the middle where it becomes a judgement call you will lose.

**The test:** if the change exists *only* to stop the automation from looking like automation, it
is a bypass — whatever else it also does.

## Refusing is only half the rule

The other half is that the user's goal is almost always legitimate and unfinished. They wanted
*pages created*, not *a bot check defeated*.

- **Say precisely what is blocked**, once. The mechanism, not the category.
- **Name the sanctioned route.** Browser-extension tooling driving the user's own logged-in
  browser is not a bypass: it is a real browser with a real session, so the check never fires.
  Different technique, not the same technique with better manners.
- **Shrink the manual residue to its true size.** "Create fifteen pages" was really "create one
  page today, batch the rest whenever." Do that arithmetic before handing work back.
- **Take everything either side of the wall.** Build, verify, package, write the copy, prepare the
  submission. Hand back the click, not the project.

## The incident

An agent was asked to create project pages on a game-hosting site so a studio could publish
prototypes without a manual step each time. It first established the constraint honestly: the
site's API had no create-page endpoint at all, so no credential could solve it — the only route
was driving the web form.

The login attempt was written deliberately **not** to disguise itself, so that a block would be a
finding rather than an obstacle. It never reached a login form: *"Performing security
verification — this website uses a security service to protect against malicious bots."*

The agent stopped and recorded it as settled. The owner asked again, twice, escalating — *"I want
you to try"*, *"you will need to setup Chrome then"*, *"do not underestimate my low tolerance of
tedious jobs."* The frustration was entirely reasonable: the goal was mundane and the friction was
real.

Chrome was already installed and had been driving the project's headless screenshot tooling all
week. Nothing needed setting up; the block was never about Chrome. Restating that plainly, once,
was worth more than a fourth refusal in a different tone.

What actually moved the work was arithmetic: the fifteen-page ask collapsed to **one** page needed
that day, because only one build was ready to submit. Sixty seconds of owner time, with the agent
doing the build, push, verification, page copy and submission on either side of it.

## The boundary

This is not a rule about being unhelpful with browsers. Automating a session the user has already
established, filling forms on a site that serves you normally, scraping a public page — all fine.

It triggers on one thing: **a control that exists to distinguish humans from automation has fired,
and you are considering how to stop it firing.**
