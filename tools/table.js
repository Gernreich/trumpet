#!/usr/bin/env node
// Print the metrics table for every walk in walks/, newest measurement each time.
// Usage: node tools/table.js [--md]
const fs = require('fs'), path = require('path');
const { metrics } = require('./spiral_metrics.js');
const root = path.join(__dirname, '..');
const md = process.argv.includes('--md');

const rows = fs.readdirSync(path.join(root, 'walks'))
  .filter(f => f.endsWith('.txt')).sort()
  .map(f => {
    const walk = fs.readFileSync(path.join(root, 'walks', f), 'utf8').trim();
    return { name: f.replace(/\.txt$/, ''), walk, m: metrics(walk) };
  });

const head = ['spiral', 'blocks', 'mm', 'envelope', 'box', 'axis',
              'rotation', 'turns', 'blocks/360', 'rise/360', 'deg/block'];
const body = rows.map(r => [
  r.name, r.m.blocks, r.m.mm, r.m.size.join('x'), r.m.vol,
  r.m.axisDir, r.m.degrees + ' deg', r.m.turns.toFixed(2),
  r.m.blocksPer360.toFixed(1),
  r.m.risePer360.toFixed(2) + ' blk / ' + Math.round(r.m.riseMMPer360) + 'mm',
  r.m.degPerBlock.toFixed(1)
].map(String));

if (md) {
  console.log('| ' + head.join(' | ') + ' |');
  console.log('| ' + head.map((h, i) => i === 0 ? '---' : '---:').join(' | ') + ' |');
  for (const b of body) console.log('| ' + b.join(' | ') + ' |');
} else {
  const w = head.map((h, i) => Math.max(h.length, ...body.map(b => b[i].length)));
  console.log(head.map((h, i) => h.padEnd(w[i])).join('  '));
  for (const b of body) console.log(b.map((v, i) => v.padEnd(w[i])).join('  '));
}
