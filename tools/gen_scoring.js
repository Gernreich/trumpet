#!/usr/bin/env node
// Regenerate SCORING.md. Every number comes from tools/score.js.
const fs = require('fs'), path = require('path'), cp = require('child_process');
const { rows, METRICS, R } = require('./score.js');
const root = path.join(__dirname, '..');

const table = cp.execSync(`node ${JSON.stringify(path.join(__dirname,'score.js'))} --md`,
                          { encoding: 'utf8' }).trim().split('\n').filter(l => l.startsWith('|')).join('\n');

const touch = rows.filter(r => r.v.touching > 0);
const byScore   = touch.slice().sort((a,b) => b.geoRaw - a.geoRaw).map(r => r.name);
const byQuality = touch.slice().sort((a,b) => Math.abs(b.geoRaw) - Math.abs(a.geoRaw)).map(r => r.name);
let mirror = 0;
for (let i = 0; i < touch.length; i++) if (byScore[i] === byQuality[touch.length-1-i]) mirror++;

const spread = key => {
  const a = rows.map(r => r[key]);
  const full = Math.max(...a) - Math.min(...a);
  const clean = rows.filter(r => !r.v.touching).map(r => r[key]);
  const within = Math.max(...clean) - Math.min(...clean);
  return { full, within, pct: 100 * (1 - within / full) };
};
const sRaw = spread('addRaw'), sNorm = spread('addNorm');
let sameRatio = 0, movedNorm = 0;
for (const r of rows){
  if (R.geoRaw.get(r.name) === R.geoRatio.get(r.name)) sameRatio++;
  if (R.geoRaw.get(r.name) !== R.geoNorm.get(r.name)) movedNorm++;
}
const winners = ['geoRaw','addRaw','geoNorm','addNorm','geoFix','addFix']
  .map(k => rows.slice().sort((a,b) => (R[k].get(a.name) - R[k].get(b.name)))[0].name);
const unanimous = winners.every(w => w === winners[0]) ? winners[0] : null;

const md = `# Scoring

Eight metrics, four ways of combining them, and a touching flag folded in as
specified: **-1 / +1** as a factor in the geometric mean, **-100 / +100** as a term
in the additive one. Regenerate with \`node tools/gen_scoring.js\`; the table comes
straight out of \`tools/score.js\`.

## The metrics scored

${METRICS.map(M => `* **${M.label}** — ${M.dir === 'lo' ? 'less' : 'more'} is better`).join('\n')}
* **touching** — the flag, handled separately

A mean cannot tell a cost from a benefit, so every metric is first oriented so that
bigger is better. In the raw columns that means taking the reciprocal of the
less-is-better ones; in the normalized columns the normalization does it.

## The four scorings, and two repairs

${table}

\`geo fix\` and \`add fix\` are the same intent without the traps below.

## Can each metric be normalized?

Yes — and for the additive mean it is not optional. Raw box volume runs in the
hundreds while turns/m runs about 10 to 14, so an unnormalized sum is very nearly a
ranking by box volume alone. Two normalizations are worth separating:

**Ratio to best** (\`best / x\` for less-is-better) is a pure per-metric rescaling into
(0,1]. **It cannot change a geometric-mean ranking at all** — scaling metric *i* by
*cᵢ* multiplies every spiral's score by the same (∏cᵢ)^(1/n). Measured here: ${sameRatio}/${rows.length}
ranks identical to raw.

**Min-max** ((x−min)/(max−min)) shifts as well as scales, and a shift is not
scale-invariant, so it does change the geometric ranking — ${movedNorm}/${rows.length} ranks move. It also
sends the worst value in each metric to zero, which annihilates a product, so the
floor here is ${0.01} rather than 0.

So: normalize for the additive mean because you must; for the geometric mean, know
that a pure rescale buys nothing and a min-max is a real change of question.

## Three things the specified scheme does

**1. In a geometric mean, -1 does not penalize — it flips the sign, and inverts the
order it is applied to.** Magnitude is the quality; the negative sign then sorts the
largest magnitude last. Among the ${touch.length} touching spirals, ranking by score and ranking by
|score| are exact mirrors in **${mirror}/${touch.length}** positions. The best touching coil is ranked the
worst touching coil. A multiplicative penalty has to be a factor *below one*: 1 is
the identity, so "+1 for clean" correctly does nothing, but its opposite is 0.5, not
-1.

**2. It depends on how many metrics are in the mean.** With ${METRICS.length} metrics plus the flag
there are ${METRICS.length + 1} values — odd, so a negative product has a real root. Drop one metric
and there are ${METRICS.length}, and every touching spiral scores \`NaN\`: no real even root of a
negative number. The score is one metric away from undefined.

**3. ±100 is not a weight, it is a verdict.** It accounts for **${sRaw.pct.toFixed(1)}%** of the raw score
range and **${sNorm.pct.toFixed(1)}%** of the normalized one — the full spread is ${sNorm.full.toFixed(2)} and everything the
other ${METRICS.length} metrics do fits in ${sNorm.within.toFixed(2)} of it. That is a filter written as a mean. If
touching really is disqualifying, filtering on it is clearer and says so; if it is
merely bad, it wants a weight you can turn.

\`add fix\` puts touching on the same 0..1 scale as the rest with an explicit weight of
3, and \`geo fix\` uses a factor of 1/(1+touching) — positive, graded by how much contact
there is, and indifferent to how many metrics sit beside it.

## What survives all six

${unanimous
 ? `**${unanimous}** comes first under every one of the six scorings — literal and repaired, raw and normalized. When a ranking is that indifferent to the scheme, the scheme is not what is deciding it.`
 : `No spiral wins every scoring; the winners are ${[...new Set(winners)].join(', ')}.`}

The repairs do move things. Under the literal scheme every touching spiral sorts below
every clean one, so ${rows.filter(r=>!r.v.touching).length} clean coils take the top ${rows.filter(r=>!r.v.touching).length} places. Under \`geo fix\` and
\`add fix\`, \`coil_3x3_50\` and \`coil_3x3_47\` climb into the top four on the strength of
everything else — a graded penalty lets a coil be good enough elsewhere to be worth
the contact, and a verdict never does.
`;
fs.writeFileSync(path.join(root, 'SCORING.md'), md);
console.log('SCORING.md written,', md.split('\n').length, 'lines');
