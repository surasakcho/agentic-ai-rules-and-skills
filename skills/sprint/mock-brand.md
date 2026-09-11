# Brand and marketing assets

**Logo, social image, store banner, anything the owner may want to edit themselves: Canva.**
Screens are not in this lane — see [`mock-screen.md`](mock-screen.md).

## Why Canva here and nowhere else

**The owner can open it and change it without anyone's help.** For an asset that carries their brand
and outlives any one session, that matters more than the speed lost. A logo they cannot adjust
without asking is a logo that stays wrong.

## Access — settle this before promising anything

The Canva plugin is an MCP server and needs an **OAuth login to the owner's Canva account**. That is
**one-off setup labour by them**, done once over the VNC desktop, after which the browser profile
persists across container recreation because the home directory is a host bind mount.

**Until that login exists, this lane is not runnable.** Say so plainly rather than producing a
substitute and calling it the brand asset.

## The procedure

1. **Write the brief first, in words** — what it is for, where it appears, what it must not look
   like. *A brand brief that cannot say what it must NOT look like has not been thought about.*
2. **Check the brand file** for palette, wordmark and typography before generating anything.
3. Create the design, **export a PNG, and commit it in the repo.** The Canva design is the editable
   master; the committed export is what survives losing access to the account.
4. Record the design's link next to the export so the master is findable.

## The constraint nobody remembers until it bites

**Anything published under the owner's identity needs their approval per act.** Producing a brand
asset is not publishing it. **Keep those two steps separate and never let one imply the other.**
