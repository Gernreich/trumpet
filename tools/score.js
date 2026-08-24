#!/usr/bin/env node
// Composite scoring. Four rankings: geometric and additive mean, each on raw
// and on normalized metrics, with the touching flag folded in as specified --
// -1 / +1 as a factor in the geometric mean, -100 / +100 as a term in the
// additive one.
//
// Usage: node tools/score.js [--md]
const fs = require('fs'), path = require('path');
const { metrics } = require('./spiral_metrics.js');
const root = path.join(__dirname, '..');
const md = process.argv.includes('--md');
const parts = JSON.parse(fs.readFileSync(path.join(root, 'parts.json'), 'utf8'));

// Every metric needs a direction, or a mean of them means nothing. "lo" = less
// is better, "hi" = more is better.
const METRICS = [
  { k: 'vol',            dir: 'lo', label: 'box'          },
  { k: 'crossArea',      dir: 'lo', label: 'cross area'   },
  { k: 'pieces',         dir: 'lo', label: 'pieces'       },
  { k: 'distinct',       dir: 'lo', label: 'distinct'     },
  { k: 'blocksPer360',   dir: 'lo', label: 'blocks/360'   },
  { k: 'risePer360',     dir: 'lo', label: 'rise/360'     },
  { k: 'turnsPerMetre',  dir: 'lo', label: 'turns/m'      },
  { k: 'longestStraight',dir: 'hi', label: 'longest str'  },
];

const rows = fs.readdirSync(path.join(root, 'walks')).filter(f => f.endsWith('.txt'))
  .map(f => {
    const name = f.replace(/\.txt$/, '');
    const m = metrics(fs.readFileSync(path.join(root, 'walks', f), 'utf8').trim());
    const p = parts[name];
    return { name, v: {
      vol: m.vol, crossArea: m.cross[0] * m.cross[1],
      pieces: p.pieces, distinct: p.distinct,
      blocksPer360: m.blocksPer360, risePer360: m.risePer360,
      turnsPerMetre: m.turnsPerMetre, longestStraight: m.longestStraight,
      touching: m.touching } };
  });

// --- orientation -----------------------------------------------------------
// Raw: turn every metric into "bigger is better" by reciprocal where needed,
// because a mean cannot tell a cost from a benefit on its own.
const oriented = r => METRICS.map(M => M.dir === 'lo' ? 1 / r.v[M.k] : r.v[M.k]);

// Normalized, min-max, 1 = best in the set, 0 = worst. Floored just above zero
// so a single worst-in-set value does not annihilate a geometric mean.
const EPS = 0.01;
const lo = {}, hi = {};
for (const M of METRICS) {
  const xs = rows.map(r => r.v[M.k]);
  lo[M.k] = Math.min(...xs); hi[M.k] = Math.max(...xs);
}
const normed = r => METRICS.map(M => {
  const span = hi[M.k] - lo[M.k];
  if (span === 0) return 1;
  const t = (r.v[M.k] - lo[M.k]) / span;      // 0 at min, 1 at max
  const good = M.dir === 'lo' ? 1 - t : t;
  return EPS + (1 - EPS) * good;
});

// Ratio-to-best: pure per-metric rescaling, in (0,1].
const ratio = r => METRICS.map(M => M.dir === 'lo' ? lo[M.k] / r.v[M.k] : r.v[M.k] / hi[M.k]);

// --- the means -------------------------------------------------------------
function geo(vals) {
  const n = vals.length;
  const prod = vals.reduce((a, x) => a * x, 1);
  if (prod === 0) return 0;
  if (prod < 0) {
    if (n % 2 === 0) return NaN;              // no real nth root of a negative
    return -Math.pow(-prod, 1 / n);
  }
  return Math.pow(prod, 1 / n);
}
const add = vals => vals.reduce((a, x) => a + x, 0) / vals.length;

for (const r of rows) {
  const touchG = r.v.touching > 0 ? -1  : 1;      // factor
  const touchA = r.v.touching > 0 ? -100 : 100;   // term
  r.geoRaw   = geo([...oriented(r), touchG]);
  r.addRaw   = add([...oriented(r), touchA]);
  r.geoNorm  = geo([...normed(r),   touchG]);
  r.addNorm  = add([...normed(r),   touchA]);
  r.geoRatio = geo([...ratio(r),    touchG]);
}

// --- the same intent, without the three traps -------------------------------
// Geometric: a penalty in a product is a factor BELOW one, not a negative. This
// grades by how much contact there is and keeps every value positive, so there
// is no sign flip and no dependence on how many metrics happen to be in the mean.
// Additive: put touching on the same 0..1 scale as everything else and give it
// an explicit weight, so its influence is a number you choose rather than 100.
const TOUCH_WEIGHT = 3;
const maxTouch = Math.max(...rows.map(r => r.v.touching));
for (const r of rows) {
  r.geoFix = geo([...normed(r), 1 / (1 + r.v.touching)]);
  const tn = maxTouch ? 1 - r.v.touching / maxTouch : 1;      // 1 = clean
  const vals = normed(r);
  r.addFix = (vals.reduce((a, x) => a + x, 0) + TOUCH_WEIGHT * tn)
             / (vals.length + TOUCH_WEIGHT);
}

const rank = (key) => {
  const s = rows.slice().sort((a, b) => (isNaN(b[key]) ? -Infinity : b[key]) -
                                        (isNaN(a[key]) ? -Infinity : a[key]));
  const m = new Map(); s.forEach((r, i) => m.set(r.name, i + 1)); return m;
};
const R = { geoRaw: rank('geoRaw'), addRaw: rank('addRaw'),
            geoNorm: rank('geoNorm'), addNorm: rank('addNorm'), geoRatio: rank('geoRatio'),
            geoFix: rank('geoFix'), addFix: rank('addFix') };

const head = ['spiral', 'touch', 'geo raw', '#', 'add raw', '#',
              'geo norm', '#', 'add norm', '#', 'geo fix', '#', 'add fix', '#'];
const body = rows.slice().sort((a, b) => R.addNorm.get(a.name) - R.addNorm.get(b.name))
  .map(r => [r.name, String(r.v.touching),
    r.geoRaw.toPrecision(4),  String(R.geoRaw.get(r.name)),
    r.addRaw.toFixed(2),      String(R.addRaw.get(r.name)),
    r.geoNorm.toFixed(4),     String(R.geoNorm.get(r.name)),
    r.addNorm.toFixed(2),     String(R.addNorm.get(r.name)),
    r.geoFix.toFixed(4),      String(R.geoFix.get(r.name)),
    r.addFix.toFixed(4),      String(R.addFix.get(r.name))]);

// printing only when run directly, so the generators can import the numbers
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
module.exports = { rows, METRICS, R };
