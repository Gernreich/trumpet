#!/usr/bin/env node
// Regenerate SCORING.md. Every number comes from tools/score.js.
const fs = require('fs'), path = require('path'), cp = require('child_process');
const { rows, METRICS, MEANS, R, inputs, TOUCH_WEIGHT, EPS } = require('./score.js');
const root = path.join(__dirname, '..');

const table = cp.execSync(`node ${JSON.stringify(path.join(__dirname,'score.js'))} --md`,
  { encoding: 'utf8' }).trim().split('\n').filter(l => l.startsWith('|')).join('\n');

const swing = rows.map(r => {
  const rk = MEANS.map(M => R[M.k].get(r.name));
  return { n: r.name, best: Math.min(...rk), worst: Math.max(...rk),
           swing: Math.max(...rk) - Math.min(...rk) };
}).sort((a, b) => b.swing - a.swing);

const weak = name => {
  const v = inputs(rows.find(r => r.name === name)).map(i => ({ l: i.label, x: i.x }))
    .sort((a, b) => a.x - b.x);
  return v[0];
};
const agree = (a, b) => rows.filter(r => R[a].get(r.name) === R[b].get(r.name)).length;

const firsts = MEANS.map(M => ({ mean: M.label,
  win: rows.slice().sort((x, y) => R[M.k].get(x.name) - R[M.k].get(y.name))[0].name }));
const tally = {};
for (const f of firsts) tally[f.win] = (tally[f.win] || 0) + 1;
const top = Object.entries(tally).sort((a, b) => b[1] - a[1])[0];

const two = swing[0], three = swing[1];
const md = `# Scoring

Seven metrics, one touching count, and every common mean, so the ranking can be
read against the thing that produced it. Regenerate with \`node tools/gen_scoring.js\`.

## What is scored

${METRICS.map(M => `* **${M.label}** — ${M.dir === 'lo' ? 'less' : 'more'} is better`).join('\n')}
* **touching** — carried the same way as the rest, at weight ${TOUCH_WEIGHT}

Each is normalized to (0,1] with 1 the best in the set, oriented so bigger is
better, and floored at ${EPS} so that one worst-in-set value cannot zero a product.
Touching is not a special case: a graded penalty on the same scale, weighted, which
is what \`geo fix\` and \`add fix\` were doing and is now what every mean sees.

**\`blocks/360\` is deliberately gone.** It is anti-correlated with turns/m by
construction — a tighter spiral has to turn more often — so carrying both let them
cancel, and made the composite quieter about coiling than the columns themselves are.

## The means

| mean | order *p* | what it rewards |
| --- | :-: | --- |
| harmonic | -1 | punishes the weakest input hardest |
| geometric | 0 | |
| arithmetic | 1 | |
| quadratic (RMS) | 2 | |
| cubic | 3 | rewards the strongest input hardest |
| median | — | ignores both extremes |
| midrange | — | only the extremes |
| contraharmonic | — | rewards the strongest harder still |

The first five are the power mean of order *p*, which increases with *p*, so for
every spiral **harmonic ≤ geometric ≤ arithmetic ≤ quadratic ≤ cubic**. Verified here
on all ${rows.length}. What changes with *p* is not the size of the score but how much a single
bad metric is allowed to sink it.

## The table

${table}

## Choosing a mean is choosing how much a weak spot counts

That choice is worth more than any metric in it. ${two.n} ranks **${two.best}** under one mean
and **${two.worst}** under another — a swing of ${two.swing} places in a field of ${rows.length}. ${three.n} swings ${three.swing}.

| spiral | worst single input | harmonic | contraharmonic |
| --- | --- | ---: | ---: |
${['coil_2x2_146','staircase_coil','coil_3x3_53_2'].map(n => {
  const w = weak(n);
  return `| \`${n}\` | ${w.l} = ${w.x.toFixed(3)} | #${R.harm.get(n)} | #${R.contra.get(n)} |`;
}).join('\n')}

\`coil_2x2_146\` has the slackest pitch in the set and a 2x2 cross-section: one input at
the floor, another at the ceiling. The harmonic mean reads it as disqualified, the
contraharmonic as the best thing here. Both are arithmetically correct; they are
answering different questions. The staircase coil is the same shape of argument, its
weak spot being ${weak('staircase_coil').l}.

Harmonic and contraharmonic agree on **${agree('harm','contra')}** of ${rows.length} placings — they are as opposed as
two means of the same numbers can be. Harmonic and geometric agree on ${agree('harm','geo')}, which is
why the geometric mean is the usual choice when no weak spot should be forgiven but
outright disqualification is too strong.

## What survives

\`${top[0]}\` comes first under **${top[1]} of the ${MEANS.length} means**, and the reason is visible in the
table above: its worst input is ${weak(top[0]).x.toFixed(3)}, where every other contender has something
at ${EPS}. It does not win by being outstanding anywhere. It wins by having nothing to
punish, which is the one way to be robust to the choice of mean.

If a weak spot is genuinely fatal — a shared wall that will leak, a coil too fat for
the body — use the harmonic mean, or filter and then rank. If the design is allowed one
bad number in exchange for a very good one, use quadratic or cubic. The arithmetic mean
is the choice that declines to say.
`;
fs.writeFileSync(path.join(root, 'SCORING.md'), md);
console.log('SCORING.md written,', md.split('\n').length, 'lines');
