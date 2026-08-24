#!/usr/bin/env node
// The reduction pass: shorten every leg that can be shortened, without losing
// the coil.
//
// tools/minimal.js reports slack against a purely local rule -- a term's floor
// in its own window of three. Taking all of it at once usually destroys the
// design, because coiling is global: the period has to close laterally, drifting
// on one axis and returning to where it started on the other two. Shorten one
// leg and not its opposite and the period stops closing, so the walk wanders
// diagonally instead of coiling and its envelope explodes. coil_3x3_47 reduced
// naively goes from a box of 423 to 10452.
//
// So this enumerates the reductions rather than applying them, keeps only those
// that still close and still wind a whole turn, takes the shortest, rebuilds at
// comparable length and puts the result back through bore_split.py.
//
// Usage: node tools/reduce.js [--write]
const fs = require('fs'), cp = require('child_process'), path = require('path');
const root = path.join(__dirname, '..');
const GEN  = path.join(root, '..', 'bore-generator');
const PY   = process.env.BORE_PY || (process.env.HOME + '/boxes/venv/bin/python');
const { metrics } = require('./spiral_metrics.js');
const WRITE = process.argv.includes('--write');

const V  = {N:[0,0,-1],S:[0,0,1],E:[1,0,0],W:[-1,0,0],U:[0,1,0],D:[0,-1,0]};
const AX = {N:2,S:2,E:0,W:0,U:1,D:1};
const parse = w => w.trim().split(/\s+/).map(t => ({d:t[0], n:t.length>1?+t.slice(1):1}));

function periodOf(t){
  const body = t.slice(2,-2).map(x => x.d + x.n);      // lead-in and tail are partial
  for (let p = 1; p <= body.length - p; p++){
    let ok = true;
    for (let i = 0; i + p < body.length; i++) if (body[i] !== body[i+p]){ ok = false; break; }
    if (ok) return body.slice(0, p).map(s => ({ d: s[0], n: +s.slice(1) }));
  }
  return null;
}
const floorOf = (t, i) => {
  const k = t.length, a = t[(i+k-1)%k], c = t[(i+1)%k];
  return AX[a.d] !== AX[c.d] ? 3 : a.d === c.d ? 1 : 2;
};
const net = t => t.reduce((a,m) => {
  const v = V[m.d]; return [a[0]+v[0]*m.n, a[1]+v[1]*m.n, a[2]+v[2]*m.n]; }, [0,0,0]);

// A whole number of revolutions per period, not necessarily one: the staircase
// coil's period turns three times, and demanding exactly one rejected it and its
// reduction outright.
function windsWhole(t, ax){
  const lat = [0,1,2].filter(i => i !== ax), proj = [];
  for (const m of t){ const v = V[m.d]; if (v[lat[0]] || v[lat[1]]) proj.push([v[lat[0]], v[lat[1]]]); }
  let q = 0;
  for (let i = 0; i < proj.length; i++){
    const u = proj[i], w = proj[(i+1) % proj.length];
    q += u[0]*w[1] - u[1]*w[0];
  }
  return q !== 0 && Math.abs(q) % 4 === 0;
}
// still a coil: travels on exactly one axis, and turns a whole revolution about it
function isCoil(t){
  const p = net(t), nz = p.map((v,i)=>[v,i]).filter(([v]) => v !== 0);
  if (nz.length !== 1) return false;
  return windsWhole(t, nz[0][1]);
}

function split(walk){
  try {
    const out = cp.execSync(`${JSON.stringify(PY)} bore_split.py --no-write ${JSON.stringify(walk)}`,
      { cwd: GEN, encoding: 'utf8', maxBuffer: 1<<24, stdio: ['pipe','pipe','pipe'] });
    const kinds = {};
    for (const l of out.split('\n')){ const m = l.match(/^\s+\d+\s+\d+-\d+\s+(\w+)\s/); if (m) kinds[m[1]] = (kinds[m[1]]||0)+1; }
    return { ok: true, elbows: kinds.elbow || 0,
             pieces: +(out.match(/(\d+) pieces to assemble/)||[])[1],
             blocks: +(out.match(/(\d+) blocks/)||[])[1],
             oversize: /does not fit|too big/i.test(out) };
  } catch (e) { return { ok: false }; }
}

const names = fs.readdirSync(path.join(root,'walks')).filter(f => f.endsWith('.txt'))
  .map(f => f.replace(/\.txt$/,'')).sort();

const results = [];
for (const name of names){
  const walk = fs.readFileSync(path.join(root,'walks',name+'.txt'),'utf8').trim();
  const per = periodOf(parse(walk));
  if (!per){ results.push({ name, status: 'no clean period' }); continue; }

  const slack = per.map((m,i) => ({ i, floor: floorOf(per,i), n: m.n }))
                   .filter(x => x.n > x.floor);
  if (!slack.length){ results.push({ name, status: 'already minimal' }); continue; }

  // every combination of reductions, shortest first
  let combos = [[]];
  for (const s of slack){
    const next = [];
    for (const c of combos) for (let v = s.floor; v <= s.n; v++) next.push([...c, { i: s.i, v }]);
    combos = next;
    if (combos.length > 50000) break;
  }
  combos.sort((a,b) => a.reduce((x,y)=>x+y.v,0) - b.reduce((x,y)=>x+y.v,0));

  let found = null;
  for (const c of combos){
    const t = per.map(m => ({ ...m }));
    for (const { i, v } of c) t[i].n = v;
    if (t.some((m,i) => m.n < floorOf(t,i))) continue;   // floors shift as legs change
    if (!isCoil(t)) continue;
    const red = t.map(m => m.d + m.n).join(' ');
    for (let T = 196; T >= 188; T--){
      const w = cp.execSync(`node ${JSON.stringify(path.join(__dirname,'mknotation.js'))} ${JSON.stringify(red)} ${T}`)
                  .toString().trim();
      const s = split(w);
      if (s.ok && s.elbows === 0 && !s.oversize){ found = { red, walk: w, s }; break; }
    }
    if (found) break;
  }
  if (!found){ results.push({ name, status: 'no reduction keeps the coil' }); continue; }

  const before = metrics(walk), after = metrics(found.walk);
  results.push({ name, status: 'reduced', ...found, before, after,
                 periodBefore: per.map(m=>m.d+m.n).join(' ') });
}

for (const r of results){
  if (r.status !== 'reduced'){ console.log(r.name.padEnd(16) + r.status); continue; }
  console.log(r.name.padEnd(16) +
    'box ' + String(r.before.vol).padStart(4) + ' -> ' + String(r.after.vol).padStart(4) +
    '   blocks ' + String(r.before.blocks).padStart(3) + ' -> ' + String(r.after.blocks).padStart(3) +
    '   touching ' + String(r.before.touching).padStart(2) + ' -> ' + String(r.after.touching).padStart(2) +
    '   blk/360 ' + r.before.blocksPer360.toFixed(1) + ' -> ' + r.after.blocksPer360.toFixed(1) +
    '   ' + r.s.pieces + ' pieces');
}
const won = results.filter(r => r.status === 'reduced');
console.log('\n' + won.length + ' of ' + results.length + ' reduced while staying a coil; ' +
  won.filter(r => r.after.vol < r.before.vol).length + ' came out smaller.');
if (WRITE) fs.writeFileSync(path.join(root,'reduced.json'), JSON.stringify(won, null, 1));
module.exports = { results };
