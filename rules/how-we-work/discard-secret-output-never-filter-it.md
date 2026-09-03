# Discard the output of a secret-resolving command; never filter it

**Task type:** operations — any command that expands, renders or dumps resolved configuration,
run anywhere the session is transcribed.
**Related:** [`sanitise-before-sharing`](sanitise-before-sharing.md) — the same one-way door, but
for what you deliberately publish rather than what you incidentally capture.
[`a-finding-is-scoped-to-what-you-checked`](a-finding-is-scoped-to-what-you-checked.md) — after a
leak, scope the exposure by tracing the paths off the box, not by assuming the worst.

---

## The rule

**A filter shapes what you SEE. It never shapes what was CAPTURED.**

By the time `grep` decides to drop a line, the producing command has already written every byte
to the pipe, and in an agent session that pipe is a transcript on disk. `| grep`, `| head`,
`| tail`, `| jq .someField` — all of them run *after* the secret has been recorded.

So for any command that resolves secrets, there is exactly one safe shape:

```sh
cmd >/dev/null 2>&1 && echo VALID || echo INVALID     # check the exit code
```

If you need a *fact* about the output, derive it without reproducing the value: the key's name,
its length, whether it is non-empty, whether the exit code was zero.

## The incident

A `docker compose` file gained an `env_file:` entry for an itch.io API secret. To confirm the
wiring, the session ran:

```sh
docker compose -f compose.gamedev.yaml config | grep -A3 -iE "env_file|itch"
```

`config` renders **resolved** values. The grep printed the API key in full. The intent was to
see the structure; the effect was to write the credential into a 23 MB session transcript.

The same session had, minutes earlier, been careful in exactly the right way — reading the
secret's key names with `sed -E 's/=.*/=<redacted>/'` and never `cat`-ing the file. Care applied
to the obvious command and not to the one that renders config is not care, it is luck.

A peer session that used the same key stayed clean by accident of style: it wrote
`"${itch_api_secret}"` inside the command rather than interpolating the value into printed text,
so its transcript holds `<set>` and an account name. **Same secret, same hour, two sessions, one
leak** — and the difference was entirely whether a resolved value ever reached stdout.

## Where this bites beyond compose

Anything that resolves configuration and prints it:

| Command | What it renders |
|---|---|
| `docker compose config` | env_file and `${VAR}` fully expanded |
| `docker inspect` | `.Config.Env` — every variable, with values |
| `env` / `printenv` | the whole environment |
| `terraform show`, `kubectl get secret -o yaml` | state and base64 payloads |
| `wrangler d1 execute --json` | any row that happens to hold a token |
| `git config --list` | credential helpers with inline tokens |

## Guard

- **Never pipe a secret-resolving command into a filter.** Redirect to `/dev/null`, test `$?`.
- **Assert on a derived fact, not the value**: `test -n "$VAR" && echo "set, length ${#VAR}"`.
- **Read structure from the source, not the render** — `grep env_file compose.yaml` is safe
  because the file holds `${HOME}/...`, not the value.
- **When it does leak, scope it before recommending panic.** Trace the real paths off the
  machine — backup includes, sync scripts, container mounts, what is committed. "One command
  rendered it once into one local file" and "two sessions saw it" are different rotation
  stories, and the operator deserves the accurate one.
- **Rotate anyway.** Scoping the exposure justifies calm, never inaction.
