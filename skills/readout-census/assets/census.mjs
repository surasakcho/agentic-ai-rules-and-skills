// Readout census: audit every named flag, predicate and outcome a game ships
// against the hidden fact it is NAMED AFTER.
//
//   npm run qa:census nightpath          # default 40 runs per profile per mode
//   npm run qa:census nightpath 200
//   npm run qa:census nightpath 200 run  # one mode only; the long night costs 4x
//
// ---------------------------------------------------------------------------
// WHY THIS EXISTS, AND WHY NOTHING ELSE IN qa/ COULD HAVE FOUND IT
// ---------------------------------------------------------------------------
//
// `qa/ablate.mjs` deletes a BOT BEHAVIOUR and re-measures. `qa/probe.mjs`
// counts the BOT's own decision predicates. `qa/axes.mjs` perturbs BOT
// precision. All three instrument the bot. **Nothing in this repo has ever
// instrumented the CORE's own readouts against the CORE's own truth** -- even
// though `sense` and `hidden` sit in the same state object on the same tick and
// every sweep already generates that join for free and throws it away.
//
// Four nightpath defects came out of that gap, each mistaken for a design
// failure and each costing days:
//
//   the Torch predicate fired 3 times in 7.4M ticks   -> rate ~ 0
//   `endedBy: 'seen'` was structurally impossible     -> rate = 0
//   `heard.rising` read 42.7% -- a healthy-looking     -> rate FINE, lift -7.9
//     rate -- while ANTI-CORRELATED with the hunt
//     it is named after
//
// The third is the one this tool is really for. Counting alone would have
// caught the first two. Nothing but a correlation catches the third, and it was
// the expensive one: it made the game read 0% cleared and nearly cost a
// teaching beat that was never at fault.
//
// So, for every named readout, two numbers:
//
//   RATE  fraction of ticks (or runs) on which it is true
//   LIFT  P(true | the hidden fact it is named after)
//       - P(true | that fact absent)                     ... in POINTS
//
// A row FAILS on any of:
//
//   rate ~ 0     never exercised -- the mechanic is not in the game
//   rate ~ 100   always true -- it distinguishes nothing
//   lift <= 0    it does not detect the thing it is named after, or detects
//                its OPPOSITE
//
// and is reported UNTESTED when the hidden fact itself never happened often
// enough to correlate against -- which is a finding in its own right, and the
// shape `endedBy: 'seen'` had: the readout was not wrong, the world never
// produced the thing it names.
//
// One more verdict, SIMPSON, exists because pooling across bot profiles can
// REVERSE a sign. A row whose pooled lift is negative while every profile with
// enough evidence lifts positively is not inverted; it is a row where the weak
// profiles never meet the fact at all and drag the pooled contrast. It still
// fails -- the pooled number is unusable -- but it is named for what it is and
// the reader is sent to the per-profile block. A tool built to catch a
// misleading correlation must not manufacture one.
//
// ---------------------------------------------------------------------------
// THE DECLARATION -- deliberately two arrow functions, because a check nobody
// registers their flags with is a check that finds nothing
// ---------------------------------------------------------------------------
//
// A core declares `export const CENSUS = [...]`, OR -- when the core is being
// worked in and must not be touched -- a sidecar `experiments/<name>/census.js`
// exports the same array. The sidecar is read only if the core exports nothing;
// in-core is preferred because a manifest that lives beside the flag is a
// manifest that gets updated when the flag moves.
//
//   export const CENSUS = [
//     { name:  'sense.heard.rising',
//       scope: 'tick',                              // 'tick' | 'run'
//       of:    'a Howler is hunting',               // the fact, in English
//       read:  (s) => s.sense.heard.rising,         // the READOUT
//       truth: (s) => s.hidden.howlers.some((w) => w.mode === 'hunting'),
//     },
//     { name:  "endedBy: 'seen'",
//       scope: 'run',
//       of:    'a Stalker ever hunted in this run',
//       read:  (fin) => fin.endedBy === 'seen',     // read on the FINAL state
//       everTruth: (s) => s.hidden.stalkers.some((x) => x.mode === 'hunting'),
//     },
//   ]
//
// Fields:
//
//   name       what it is called in the game. Use the path a reader would grep.
//   scope      'tick'  -- read every tick;  'run' -- read once, on the final state
//   read       the readout. Truthy/falsy. MUST NOT MUTATE.
//   of         the hidden fact, as a sentence. Required whenever a truth is given;
//              it is what makes the failure line readable by someone who did not
//              write the row.
//   truth      the hidden fact, on the SAME tick. tick scope.
//   everTruth  the hidden fact, ORed across the whole run. run scope. Use this
//              when the fact is an event ("a Stalker ever hunted") rather than a
//              state readable at the end.
//   when       optional population filter: only ticks where this is true are
//              counted. Use it when a readout is only meaningful in a phase --
//              a cue latch measured over every tick reads ~0% for arithmetic
//              reasons and tells you nothing.
//   modes      optional [names]; restrict the row to some of core.MODES.
//   expect     optional { rateMin, rateMax, liftMin } overriding the defaults
//              below. A legitimately rare flag is DECLARED rare here, rather
//              than silenced by lowering the bar for everything.
//
// A row with no `truth`/`everTruth` is RATE-ONLY: it still catches "never
// exercised" and "always true", and the footer counts how many rows dodged the
// lift column, so laziness is visible rather than silent.
//
// ---------------------------------------------------------------------------
// READ-ONLY, AND PROVEN SO
// ---------------------------------------------------------------------------
//
// Census only observes. If a `read` or `truth` mutated the state it inspects,
// the run it measures would stop being the run every other tool measured. The
// sampled determinism replay at the bottom is what enforces that, exactly as
// `qa/probe.mjs` enforces the same property for bot-side counters.

import { createDriver, replay, TICK_DT } from '../shared/loop.js'

const NAME = process.argv[2] || '_template'
const RUNS = +(process.argv[3] || 40)
const MAX_TICKS = +(process.env.QA_MAX_TICKS || 400000)

// Defaults, and each is a claim rather than a round number:
//
//   DEAD    the Torch predicate fired 3 times in 7.4M ticks (4e-7). Anything
//           under a thousandth of the sweep is not a mechanic players meet.
//   ALWAYS  a flag true on 99.5% of the population partitions nothing; the
//           render layer could hard-code `true` and no test would notice.
//   MIN_*   below this much evidence of the FACT, a lift is arithmetic noise
//           and reporting it as a number would be worse than reporting nothing.
//   LIFT    the specification's own bar. Zero is failure, not neutrality: a
//           readout that does not beat its own base rate is decoration.
const DEAD = 0.001
const ALWAYS = 0.995
const MIN_FACT_TICKS = 200
const MIN_FACT_RUNS = 5
const LIFT_MIN = 0
const LIFT_WEAK = 0.05     // 5 points: reported, not failed

const core = await import(`../experiments/${NAME}/game.js`)
const { createBot, PROFILES } = await import(`../experiments/${NAME}/bot.js`)

let CENSUS = core.CENSUS
let source = `experiments/${NAME}/game.js`
if (!CENSUS) {
  try {
    CENSUS = (await import(`../experiments/${NAME}/census.js`)).CENSUS
    source = `experiments/${NAME}/census.js (sidecar)`
  } catch { /* neither -- reported below */ }
}
if (!Array.isArray(CENSUS) || !CENSUS.length) {
  console.error(`\nNo readout manifest for '${NAME}'.`)
  console.error(`Declare one, either in the core:`)
  console.error(`    export const CENSUS = [ { name, scope, of, read, truth } ]`)
  console.error(`or, if the core is being worked in, as experiments/${NAME}/census.js`)
  console.error(`exporting the same array. Two arrow functions per readout; see`)
  console.error(`the header of qa/census.mjs for the contract.\n`)
  process.exit(2)
}

for (const [i, r] of CENSUS.entries()) {
  const bad = []
  if (!r.name) bad.push('no `name`')
  if (typeof r.read !== 'function') bad.push('no `read` function')
  if (r.scope !== 'tick' && r.scope !== 'run') bad.push(`scope must be 'tick' or 'run'`)
  if ((r.truth || r.everTruth) && !r.of) bad.push('has a truth but no `of` sentence')
  if (r.scope === 'tick' && r.everTruth) bad.push('`everTruth` is for run scope; use `truth`')
  if (bad.length) {
    console.error(`CENSUS[${i}] (${r.name ?? 'unnamed'}): ${bad.join('; ')}`)
    process.exit(2)
  }
}

const MODES = core.MODES ?? { '': {} }
const only = process.argv.slice(4)
const modeNames = only.length ? Object.keys(MODES).filter((m) => only.includes(m)) : Object.keys(MODES)
if (!modeNames.length) {
  console.error(`no such mode: ${only.join(', ')}. Declared: ${Object.keys(MODES).join(', ')}`)
  process.exit(2)
}
const profiles = Object.keys(PROFILES)

/** One accumulator per (row, mode, profile). Pooling happens at report time. */
const cell = () => ({ n: 0, t: 0, fact: 0, tFact: 0, noFact: 0, tNoFact: 0 })
const acc = new Map()   // `${rowIx}|${mode}|${profile}` -> cell
const key = (i, m, p) => `${i}|${m}|${p}`
const get = (i, m, p) => {
  const k = key(i, m, p)
  let c = acc.get(k)
  if (!c) acc.set(k, (c = cell()))
  return c
}

/** Fold one observation into a cell. `fact` is null when the row is rate-only. */
function observe(c, val, fact) {
  c.n++
  if (val) c.t++
  if (fact === null) return
  if (fact) { c.fact++; if (val) c.tFact++ }
  else { c.noFact++; if (val) c.tNoFact++ }
}

let mismatches = 0
const errors = []
const dead = new Set()   // rows whose predicates threw; reported, never silent

function guard(fn, s, rowName, what) {
  try { return fn(s) } catch (e) {
    if (!dead.has(rowName + what)) {
      dead.add(rowName + what)
      errors.push(`${rowName}: \`${what}\` threw -- ${e.message}`)
    }
    return undefined
  }
}

const t0 = Date.now()
let ticksSeen = 0

for (const mode of modeNames) {
  const rows = CENSUS.map((r, i) => ({ r, i }))
    .filter(({ r }) => !r.modes || r.modes.includes(mode))
  const tickRows = rows.filter(({ r }) => r.scope === 'tick')
  const runRows = rows.filter(({ r }) => r.scope === 'run')

  for (const profile of profiles) {
    for (let k = 0; k < RUNS; k++) {
      const seed = 1000 + k
      const driver = createDriver(core, { seed, opts: MODES[mode].opts })
      const bot = createBot(profile, seed, core)
      // `everTruth` is ORed across the run; one flag per run-scope row.
      const ever = new Array(runRows.length).fill(false)

      let ticks = 0
      const onTick = (s) => {
        for (const { r, i } of tickRows) {
          if (r.when && !guard(r.when, s, r.name, 'when')) continue
          const val = !!guard(r.read, s, r.name, 'read')
          const fact = r.truth ? !!guard(r.truth, s, r.name, 'truth') : null
          observe(get(i, mode, profile), val, fact)
        }
        for (let j = 0; j < runRows.length; j++) {
          const { r } = runRows[j]
          if (!ever[j] && r.everTruth && guard(r.everTruth, s, r.name, 'everTruth')) ever[j] = true
        }
      }

      try {
        while (!core.isOver(driver.state) && ticks < MAX_TICKS) {
          driver.advance(TICK_DT, bot.decide(driver.state), onTick)
          ticks++
        }
      } catch (e) {
        errors.push(`seed=${seed} ${profile}${mode ? ' [' + mode + ']' : ''}: ${e.message}`)
        continue
      }
      ticksSeen += ticks

      const fin = driver.state
      for (let j = 0; j < runRows.length; j++) {
        const { r, i } = runRows[j]
        const val = !!guard(r.read, fin, r.name, 'read')
        const fact = r.everTruth ? ever[j] : (r.truth ? !!guard(r.truth, fin, r.name, 'truth') : null)
        observe(get(i, mode, profile), val, fact)
      }

      // The read-only proof. A `read` that mutated the state would move the
      // live summary away from the replayed one, and that is the only way this
      // tool can lie about the run it is measuring.
      if (k % 20 === 0) {
        const got = core.summary(fin)
        const again = core.summary(replay(core, driver.replayLog()))
        if (JSON.stringify(again) !== JSON.stringify(got)) {
          if (mismatches < 3) {
            console.error(`  CENSUS MUTATED THE RUN  seed=${seed} ${profile}`)
            console.error(`    live   ${JSON.stringify(got)}`)
            console.error(`    replay ${JSON.stringify(again)}`)
          }
          mismatches++
        }
      }
    }
  }
}

// --- report ----------------------------------------------------------------

const pc = (x) => (100 * x)
const f1 = (x) => (Number.isFinite(x) ? +x.toFixed(1) : null)

/** Pool a row's cells across the profiles of one mode. */
function pool(i, mode, only) {
  const c = cell()
  for (const p of only ?? profiles) {
    const x = acc.get(key(i, mode, p))
    if (!x) continue
    for (const f of Object.keys(c)) c[f] += x[f]
  }
  return c
}

/**
 * Per-profile lifts for one row, for the profiles with enough evidence in BOTH
 * cells. This exists because pooling can reverse a sign: fogcall's `timeouts`
 * row pools to -3.0 while the only profile that ever reaches a tight window
 * lifts +39.6, because the two weak profiles never meet the fact at all and
 * still time out constantly. Reporting that as INVERTED would be the exact
 * class of misleading number this tool was built to delete, so it gets its own
 * verdict and sends the reader to the per-profile block.
 */
function perProfileLifts(i, mode, minFact) {
  const out = []
  for (const p of profiles) {
    const c = pool(i, mode, [p])
    if (c.fact < minFact || c.noFact < minFact) continue
    out.push({ profile: p, lift: c.tFact / c.fact - c.tNoFact / c.noFact })
  }
  return out
}

function judge(r, c, scope, i, mode) {
  const minFact = scope === 'run' ? MIN_FACT_RUNS : MIN_FACT_TICKS
  const rateMin = r.expect?.rateMin ?? DEAD
  const rateMax = r.expect?.rateMax ?? ALWAYS
  const liftMin = r.expect?.liftMin ?? LIFT_MIN

  if (!c.n) return { verdict: 'NO DATA', fail: true }
  const rate = c.t / c.n
  if (rate <= rateMin) return { rate, verdict: 'DEAD', fail: true }
  if (rate >= rateMax) return { rate, verdict: 'ALWAYS', fail: true }

  const rateOnly = !r.truth && !r.everTruth
  if (rateOnly) return { rate, verdict: 'rate-only', fail: false, rateOnly: true }

  if (c.fact < minFact || c.noFact < minFact) {
    return {
      rate, verdict: 'UNTESTED', fail: true,
      why: c.fact < minFact
        ? `the fact (${r.of}) occurred ${c.fact}x -- too rare to correlate`
        : `the fact (${r.of}) was ABSENT only ${c.noFact}x -- nothing to contrast with`,
    }
  }

  const pT = c.tFact / c.fact
  const pF = c.tNoFact / c.noFact
  const lift = pT - pF
  if (lift <= liftMin) {
    const per = perProfileLifts(i, mode, minFact)
    if (per.length && per.every((x) => x.lift > liftMin)) {
      return {
        rate, pT, pF, lift, verdict: 'SIMPSON', fail: true,
        why: `pooled lift is ${(100 * lift).toFixed(1)} but EVERY profile with evidence lifts positively (` +
             per.map((x) => `${x.profile} ${(100 * x.lift).toFixed(1)}`).join(', ') +
             `). The pooled number is reversed by profiles that never meet the fact; read this row per profile.`,
      }
    }
  }
  if (lift < liftMin) return { rate, pT, pF, lift, verdict: 'INVERTED', fail: true }
  if (lift === liftMin) return { rate, pT, pF, lift, verdict: 'FLAT', fail: true }
  if (lift < LIFT_WEAK) return { rate, pT, pF, lift, verdict: 'weak', fail: false, warn: true }
  return { rate, pT, pF, lift, verdict: 'ok', fail: false }
}

console.log(`\nreadout census: ${NAME}   manifest: ${source}`)
console.log(`${CENSUS.length} readouts x ${RUNS} seeds x ${profiles.length} profiles` +
            (modeNames.length > 1 || modeNames[0] !== '' ? ` x ${modeNames.length} modes (${modeNames.join(', ')})` : '')
            + `   ${(ticksSeen / 1e6).toFixed(2)}M ticks in ${((Date.now() - t0) / 1000).toFixed(0)}s`)

let fails = 0, warns = 0, rateOnly = 0
const failing = []

for (const mode of modeNames) {
  const table = []
  for (const [i, r] of CENSUS.entries()) {
    if (r.modes && !r.modes.includes(mode)) continue
    const c = pool(i, mode)
    const v = judge(r, c, r.scope, i, mode)
    if (v.fail) { fails++; failing.push({ r, i, mode, c, v }) }
    if (v.warn) warns++
    if (v.rateOnly) rateOnly++
    table.push({
      readout: r.name,
      scope: r.scope,
      n: c.n,
      'rate %': f1(pc(v.rate ?? 0)),
      'P(t|fact) %': v.pT === undefined ? '' : f1(pc(v.pT)),
      'P(t|no fact) %': v.pF === undefined ? '' : f1(pc(v.pF)),
      'lift pts': v.lift === undefined ? '' : f1(pc(v.lift)),
      verdict: v.verdict,
    })
  }
  if (modeNames.length > 1 || modeNames[0] !== '') console.log(`\n--- mode: ${mode} ---`)
  console.table(table)
}

// A failing row is only half a diagnosis. "Dead for every profile" and "dead
// for everyone but `flailing`" have different fixes -- the first is a missing
// mechanic, the second is a bot that never chooses it -- and the pooled number
// cannot separate them, which is the same trap `qa/probe.mjs` exists to avoid.
if (failing.length) {
  console.log(`\nFAILING ROWS, per profile:`)
  for (const { r, i, mode, v } of failing) {
    const tag = mode ? ` [${mode}]` : ''
    console.log(`\n  ${r.name}${tag}  -- ${v.verdict}`)
    if (r.of) console.log(`    named after: ${r.of}`)
    if (v.why) console.log(`    ${v.why}`)
    for (const p of profiles) {
      const c = pool(i, mode, [p])
      if (!c.n) { console.log(`    ${p.padEnd(9)} no data`); continue }
      const pT = c.fact ? f1(pc(c.tFact / c.fact)) : null
      const pF = c.noFact ? f1(pc(c.tNoFact / c.noFact)) : null
      console.log(`    ${p.padEnd(9)} rate ${String(f1(pc(c.t / c.n))).padStart(5)}%  ` +
        `(${c.t}/${c.n})` +
        (r.truth || r.everTruth
          ? `   fact ${c.fact}x -> ${pT}%   no-fact ${c.noFact}x -> ${pF}%` +
            (pT != null && pF != null ? `   lift ${f1(pT - pF)}` : '')
          : ''))
    }
  }
}

if (errors.length) {
  console.log(`\nERRORS (${errors.length}); first 5:`)
  for (const e of errors.slice(0, 5)) console.log(`  ${e}`)
}

console.log(`\nrate ~0 = never exercised   rate ~100 = distinguishes nothing   lift <= 0 = does not detect what it names`)
console.log(`failing readouts: ${fails}   weak (lift < ${pc(LIFT_WEAK)} pts): ${warns}   rate-only (no lift declared): ${rateOnly}/${CENSUS.length}`)
console.log(`determinism mismatches: ${mismatches}   (census must not change the run it measures)`)

process.exit(fails || mismatches || errors.length ? 1 : 0)
