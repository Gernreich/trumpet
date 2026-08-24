#!/usr/bin/env node
// Composite scoring across the common means.
//
// Seven metrics, each normalized to (0,1] with 1 = best in the set, plus the
// touching count carried the same way and given an explicit weight. Then the
// power-mean family and three means that sit outside it.
//
// blocks/360 is deliberately absent: it is anti-correlated with turns/m by
// construction -- a tighter spiral must turn more often -- so carrying both let
// them cancel and made the composite quieter about coiling than the columns are.
//
// Usage: node tools/score.js [--md]
const fs = require('fs'), path = require('path');
const { metrics } = require('./spiral_metrics.js');
const root = path.join(__dirname, '..');
const md = process.argv.includes('--md');
const parts = JSON.parse(fs.readFileSync(path.join(root, 'parts.json'), 'utf8'));

const METRICS = [
  { k: 'vol',             dir: 'lo', label: 'box'          },
  { k: 'crossArea',       dir: 'lo', label: 'cross area'   },
  { k: 'pieces',          dir: 'lo', label: 'pieces'       },
  { k: 'distinct',        dir: 'lo', label: 'distinct'     },
  { k: 'risePer360',      dir: 'lo', label: 'rise/360'     },
  { k: 'turnsPerMetre',   dir: 'lo', label: 'turns/m'      },
  { k: 'longestStraight', dir: 'hi', label: 'longest str'  },
  { k: 'meanPlate',       dir: 'hi', label: 'mean plate'   },
];
const TOUCH_WEIGHT = 3;
const EPS = 0.01;              // a floor, so one worst-in-set value cannot zero a product

const rows = fs.readdirSync(path.join(root, 'walks')).filter(f => f.endsWith('.txt'))
  .map(f => {
    const name = f.replace(/\.txt$/, '');
    const m = metrics(fs.readFileSync(path.join(root, 'walks', f), 'utf8').trim());
    const p = parts[name];
    return { name, m, v: {
      vol: m.vol, crossArea: m.cross[0] * m.cross[1],
      pieces: p.pieces, distinct: p.distinct,
      risePer360: m.risePer360, turnsPerMetre: m.turnsPerMetre,
      longestStraight: m.longestStraight, meanPlate: p.meanPlate,
      touching: m.touching } };
  });

const lo = {}, hi = {};
for (const M of METRICS) {
  const xs = rows.map(r => r.v[M.k]);
  lo[M.k] = Math.min(...xs); hi[M.k] = Math.max(...xs);
}
const maxTouch = Math.max(...rows.map(r => r.v.touching));

// Every input on one scale: (0,1], 1 = best. Touching included the same way
// rather than as a special case, so each mean sees the same numbers.
function inputs(r) {
  const out = METRICS.map(M => {
    const span = hi[M.k] - lo[M.k];
    const t = span === 0 ? 1 : (r.v[M.k] - lo[M.k]) / span;
    const good = M.dir === 'lo' ? 1 - t : t;
    return { x: EPS + (1 - EPS) * good, w: 1, label: M.label };
  });
  const tn = maxTouch ? 1 - r.v.touching / maxTouch : 1;
  out.push({ x: EPS + (1 - EPS) * tn, w: TOUCH_WEIGHT, label: 'touching' });
  return out;
}

// --- the means -------------------------------------------------------------
// The power mean of order p. p = 1 arithmetic, p -> 0 geometric, p = -1
// harmonic, p = 2 quadratic (RMS), p = 3 cubic. All weighted by w.
function power(vals, p) {
  const W = vals.reduce((a, v) => a + v.w, 0);
  if (p === 0) return Math.exp(vals.reduce((a, v) => a + v.w * Math.log(v.x), 0) / W);
  return Math.pow(vals.reduce((a, v) => a + v.w * Math.pow(v.x, p), 0) / W, 1 / p);
}
// Outside the family: order statistics and a ratio of moments.
function median(vals) {
  const xs = [];
  for (const v of vals) for (let i = 0; i < v.w; i++) xs.push(v.x);
  xs.sort((a, b) => a - b);
  const n = xs.length;
  return n % 2 ? xs[(n - 1) / 2] : (xs[n/2 - 1] + xs[n/2]) / 2;
}
const midrange = vals => (Math.max(...vals.map(v => v.x)) + Math.min(...vals.map(v => v.x))) / 2;
const contra   = vals => {
  const num = vals.reduce((a, v) => a + v.w * v.x * v.x, 0);
  const den = vals.reduce((a, v) => a + v.w * v.x, 0);
  return num / den;
};

const MEANS = [
  { k: 'harm',   label: 'harmonic',      f: v => power(v, -1) },
  { k: 'geo',    label: 'geometric',     f: v => power(v,  0) },
  { k: 'arith',  label: 'arithmetic',    f: v => power(v,  1) },
  { k: 'quad',   label: 'quadratic',     f: v => power(v,  2) },
  { k: 'cubic',  label: 'cubic',         f: v => power(v,  3) },
  { k: 'median', label: 'median',        f: median   },
  { k: 'midr',   label: 'midrange',      f: midrange },
  { k: 'contra', label: 'contraharmonic',f: contra   },
];

for (const r of rows) {
  const v = inputs(r);
  for (const M of MEANS) r[M.k] = M.f(v);
}
const R = {};
for (const M of MEANS) {
  const s = rows.slice().sort((a, b) => b[M.k] - a[M.k]);
  R[M.k] = new Map(s.map((r, i) => [r.name, i + 1]));
}

const head = ['spiral', 'touch', ...MEANS.flatMap(M => [M.label, '#'])];
const body = rows.slice().sort((a, b) => R.geo.get(a.name) - R.geo.get(b.name))
  .map(r => [r.name, String(r.v.touching),
             ...MEANS.flatMap(M => [r[M.k].toFixed(4), String(R[M.k].get(r.name))])]);

if (require.main === module) {
  if (md) {
    console.log('| ' + head.join(' | ') + ' |');
    console.log('| ' + head.map((h, i) => i === 0 ? '---' : '---:').join(' | ') + ' |');
    for (const b of body) console.log('| ' + b.join(' | ') + ' |');
  } else {
    const w = head.map((h, i) => Math.max(h.length, ...body.map(b => b[i].length)));
    console.log(head.map((h, i) => h.padEnd(w[i])).join('  '));
    for (const b of body) console.log(b.map((v, i) => v.padEnd(w[i])).join('  '));
  }
}
module.exports = { rows, METRICS, MEANS, R, inputs, TOUCH_WEIGHT, EPS };
