#!/usr/bin/env node
// Piece counts, distinct piece shapes and plate sizes, read off bore_split.py and
// cached in parts.json so table.js does not have to shell out on every run.
//
// The plate is the bounding box the piece is cut from, which is what goes on the
// sheet and what the operator handles. Its average is the laser-cutting number:
// fewer, larger parts is less weeding, less sorting and fewer fingers to align.
// Note it is a bounding box, not the cut outline -- an L-shaped piece leaves the
// corner behind, so this overstates material for those and is a size measure
// rather than an area-used one.
// Usage: node tools/parts.js            (rebuild the cache)
const fs = require('fs'), cp = require('child_process'), path = require('path');
const root = path.join(__dirname, '..');
const GEN  = path.join(root, '..', 'bore-generator');
const PY   = process.env.BORE_PY || (process.env.HOME + '/boxes/venv/bin/python');

const out = {};
for (const f of fs.readdirSync(path.join(root, 'walks')).filter(f => f.endsWith('.txt')).sort()) {
  const name = f.replace(/\.txt$/, '');
  const walk = fs.readFileSync(path.join(root, 'walks', f), 'utf8').trim();
  const res = cp.execSync(`${JSON.stringify(PY)} bore_split.py --no-write ${JSON.stringify(walk)}`,
                          { cwd: GEN, encoding: 'utf8', maxBuffer: 1 << 24 });
  const pieces = +(res.match(/(\d+) pieces to assemble/) || [])[1];
  const plates = [];
  for (const m of res.matchAll(/^\s+\d+\s+(\d+)-(\d+)\s+\w+\s+\w+\s+\w+\s+\d+x\d+ bl (\d+)x(\d+)/gm))
    plates.push({ blocks: +m[2] - +m[1] + 1, mm2: +m[3] * +m[4] });
  const kinds = {};
  for (const l of res.split('\n')) {
    const m = l.match(/^\s+\d+\s+\d+-\d+\s+(\w+)\s/);
    if (m) kinds[m[1]] = (kinds[m[1]] || 0) + 1;
  }
  // a cut-list entry is NN_<kind>_<shape>.svg; the shape is what makes it distinct
  const shapes = new Set();
  for (const m of res.matchAll(/^\s+\d+\s+\d+_(\S+)\.svg/gm)) shapes.add(m[1]);
  const areas = plates.map(p => p.mm2);
  out[name] = { pieces, kinds, elbows: kinds.elbow || 0,
                distinct: shapes.size, shapes: [...shapes].sort(),
                meanPlate: areas.reduce((a, x) => a + x, 0) / areas.length,
                maxPlate: Math.max(...areas), minPlate: Math.min(...areas),
                totalPlate: areas.reduce((a, x) => a + x, 0) };
  console.log(name.padEnd(18), pieces + ' pieces', String(shapes.size) + ' distinct',
              'mean plate ' + Math.round(out[name].meanPlate) + ' mm2',
              'elbows ' + (kinds.elbow || 0));
}
fs.writeFileSync(path.join(root, 'parts.json'), JSON.stringify(out, null, 1));
console.log('wrote parts.json');
