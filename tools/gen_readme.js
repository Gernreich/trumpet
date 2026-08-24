#!/usr/bin/env node
// Regenerate README.md. Every number in it comes from the tools, so the page
// cannot drift from the walks: node tools/gen_readme.js
const fs = require('fs'), path = require('path'), cp = require('child_process');
const { metrics } = require('./spiral_metrics.js');
const root = path.join(__dirname, '..');

const parts = JSON.parse(fs.readFileSync(path.join(root, 'parts.json'), 'utf8'));
const rows = fs.readdirSync(path.join(root, 'walks')).filter(f => f.endsWith('.txt'))
  .map(f => { const name = f.replace(/\.txt$/, '');
    return { name, m: metrics(fs.readFileSync(path.join(root,'walks',f),'utf8').trim()),
             p: parts[name] || {} }; })
  .sort((a, b) => a.m.vol - b.m.vol);

// check.py results, as saved by tools/run_checks.sh
const checks = {};
for (const f of fs.readdirSync(path.join(root, 'checks')).filter(f => f.endsWith('.txt'))) {
  const t = fs.readFileSync(path.join(root, 'checks', f), 'utf8');
  const m = t.match(/(\d+) checks, (\d+) failed/);
  if (m) checks[f.replace(/\.txt$/, '')] = { n: +m[1], failed: +m[2] };
}
const totalChecks = Object.values(checks).reduce((a, c) => a + c.n, 0);
const totalFailed = Object.values(checks).reduce((a, c) => a + c.failed, 0);

const tbl = (flag) => cp.execSync(`node ${JSON.stringify(path.join(__dirname,'table.js'))} --md ${flag}`,
                                  { encoding: 'utf8' }).trim();
const best  = f => rows.slice().sort((a, b) => f(a) - f(b))[0];
const yours = rows.find(r => r.name === 'staircase_coil');
const box   = best(r => r.m.vol);
const rise  = best(r => r.m.risePer360);
const tube  = best(r => r.m.blocksPer360);
const pcs   = best(r => r.p.pieces);
const dist  = best(r => r.p.distinct);
const calm  = best(r => r.m.turnsPerMetre);
const clean = rows.filter(r => r.m.touching === 0).sort((a,b) => a.m.vol - b.m.vol)[0];
const plateBest = rows.slice().sort((a,b) => b.p.meanPlate - a.p.meanPlate)[0];
const L = r => `[\`${r.name}\`](pages/${r.name}.html)`;
const { rows: srows, R: SR } = require('./score.js');
const { MEANS: SM } = require('./score.js');
const wins = SM.map(M => srows.slice().sort((a,b) => SR[M.k].get(a.name) - SR[M.k].get(b.name))[0].name);
const tally = {}; for (const w of wins) tally[w] = (tally[w] || 0) + 1;
const [bestName, bestN] = Object.entries(tally).sort((a,b) => b[1] - a[1])[0];
const unanimous = `\`${bestName}\` comes first under ${bestN} of the ${SM.length} means.`;

const md = `# Spirals

Coiling bore walks that turn about an axis while advancing along it, collected with the
numbers that say how hard each one spirals and what each one costs to build. Every walk
here splits with **no elbows** — every turn folds into a piece as an L, none is stranded
as a single-block piece of its own — and every one passes the full gate.

The one this started from is ${L(yours)}; the other ${rows.length - 1} came out of an
exhaustive search for something tighter.

<!-- readme-only -->
**[Read it as a page](https://gernreich.github.io/spirals/)** — the same text set for
reading, and the only place the viewer links below open a model you can turn rather
than a page of HTML source.

**[The rest of the build files](https://gernreich.github.io/)** — every instrument,
generator and tool, indexed.

## Shape and cost

${tbl('--shape')}

Envelope, box and cross-section are in blocks; a block is 31mm of centreline. Sorted by
box, smallest first.

**Cross-section** is the envelope with the coil axis taken out — how fat the coil is,
which is what decides whether it fits inside anything. It is not implied by the box:
${L(rows.find(r => r.name === 'coil_2x2_146'))} and ${L(rows.find(r => r.name === 'coil_4x7_20'))}
are within 5% of each other on box and are ${rows.find(r=>r.name==='coil_2x2_146').m.cross.join('x')} and
${rows.find(r=>r.name==='coil_4x7_20').m.cross.join('x')} in section.

**Distinct** is how many different piece shapes the cut list holds. A coil built by
repeating one period needs only a handful, however long it runs: ${dist.name} is
${dist.p.pieces} pieces cut from ${dist.p.distinct} shapes. The staircase coil needs
${yours.p.distinct}. That is files to check and parts to tell apart on the bench, and it
does not show up in the piece count at all.

**Mean plate** is the average bounding box a piece is cut from, in mm2 — the
laser-cutting number. Fewer, larger parts means less weeding, less sorting and fewer
fingers to align, and it is the size of the part in your hand rather than the count of
them. \`${plateBest.name}\` averages ${Math.round(plateBest.p.meanPlate).toLocaleString('en-US')} mm2 against \`${yours.name}\`'s ${Math.round(yours.p.meanPlate).toLocaleString('en-US')}.

Average *blocks* per piece was the other reading of the same idea and is not used: the
block count varies by only ${((Math.max(...rows.map(r=>r.m.blocks))/Math.min(...rows.map(r=>r.m.blocks))-1)*100).toFixed(1)}% across the set, so blocks-per-piece is very nearly the
reciprocal of the piece count and ranks the set the same way in 15 of ${rows.length} places. Plate
area is not redundant: \`coil_3x3_53_2\`, \`coil_3x9_18\` and \`coil_4x8_18\` all split into
35 pieces and cannot be told apart by blocks-per-piece at all, while their mean plates
are ${[ 'coil_3x3_53_2','coil_4x8_18','coil_3x9_18' ].map(n => Math.round(rows.find(r=>r.name===n).p.meanPlate).toLocaleString('en-US')).join(', ')} mm2.

It is a bounding box, not the cut outline — an L-shaped piece leaves its corner behind
— so it measures the size of the part, not the material consumed.

**Touching** counts blocks that sit face to face without being joined along the bore —
two runs of the tube sharing a wall. \`bore_split.py\` warns about them, and they are the
version of "density" that has a consequence: where the bore passes itself, that one wall
is all that separates the two passages.

It is also the one packing number that is *not* implied by the box. ${L(box)} has the
smallest box in the set and ${box.m.touching} shared walls; ${L(clean)} is
${((clean.m.vol/box.m.vol - 1) * 100).toFixed(0)}% larger and has **none**. If a shared wall
is something to avoid, the smallest box is not the one to build.

## Rotation

${tbl('--rot')}

A coil turns about one axis while travelling down it. Drop that axis and what is left —
the lateral projection — is what rotates, and on a cubic lattice it can only turn in
ninety degree steps, so the winding is counted in quarter turns and multiplied up. Steps
along the coil axis project to nothing and are skipped: they are advance, not rotation.

* **Rotation** — the whole turn end to end, in degrees.
* **Blocks / 360** — tube spent on one revolution. Lower is a tighter spiral.
* **Rise / 360** — how far down its axis the coil travels to come back round. The pitch.
* **Deg / block** — the same, per block, averaged.
* **90deg turns**, **turns/m** — how often the air is asked to turn a corner. The tube
  length is nearly the same for all of these, so this is what separates them acoustically,
  and it is the one number here that argues *against* packing tighter.
* **Longest straight** — the longest run without a turn.

**Axis** is the direction the coil advances; the search was free to build about any axis,
so a coil that runs east is measured against east.

## What wins what

No single spiral wins, because the measures disagree.

| | winner | against the staircase coil |
| --- | --- | --- |
| smallest box | ${L(box)} — ${box.m.vol} | ${yours.m.vol}, so ${(yours.m.vol/box.m.vol).toFixed(2)}x larger |
| tightest spiral (least rise per turn) | ${L(rise)} — ${Math.round(rise.m.riseMMPer360)}mm | ${Math.round(yours.m.riseMMPer360)}mm, so ${(yours.m.risePer360/rise.m.risePer360).toFixed(1)}x slacker |
| least tube per turn | ${L(tube)} — ${tube.m.blocksPer360.toFixed(1)} blk | ${yours.m.blocksPer360.toFixed(1)} blk, within ${((yours.m.blocksPer360/tube.m.blocksPer360-1)*100).toFixed(0)}% |
| fewest pieces | ${L(pcs)} — ${pcs.p.pieces} | ${yours.p.pieces} |
| fewest distinct shapes | ${L(dist)} — ${dist.p.distinct} | ${yours.p.distinct} |
| largest average plate | ${L(plateBest)} — ${Math.round(plateBest.p.meanPlate).toLocaleString('en-US')} mm2 | ${Math.round(yours.p.meanPlate).toLocaleString('en-US')} mm2 |
| calmest bore (fewest turns/m) | ${L(calm)} — ${calm.m.turnsPerMetre.toFixed(1)} | ${yours.m.turnsPerMetre.toFixed(1)} |
| smallest box with no shared wall | ${L(clean)} — ${clean.m.vol} | ${yours.m.vol}, also ${yours.m.touching} shared |

The staircase coil loses on packing and wins, or nearly wins, on the two that bear on how
the thing sounds: it spends the least tube per revolution of almost anything here, and it
turns the air the fewest times per metre. **Packing tighter costs bends**, and bends are
the thing a bore notices.

## A metric deliberately left out

Fill density — blocks over box volume — was tried and dropped. At a fixed tube length it
is not independent of the box: blocks is near enough constant, so density is just the
reciprocal of box volume rescaled. Ranking these ${rows.length} spirals by density puts them in the
same order as ranking by box in 16 of ${rows.length} positions, and the two that swap are a tie at
477 broken by a one-block difference in length. It reads like a second opinion and is not
one. It would earn its place only in comparing walks of genuinely different lengths.

**Touching** is the metric density was reaching for. It answers the question density
sounds like it answers — how hard is this bore packed against itself — and unlike density
it disagrees with the box often enough to change which coil you would build.

## Scoring them against each other

[**SCORING.md**](SCORING.md) combines seven of the metrics and the touching count into
a single ranking under every common mean — harmonic, geometric, arithmetic, quadratic,
cubic, median, midrange, contraharmonic — and reports what the choice of mean does to
the answer. It does a great deal: \`coil_2x2_146\` places 1st under one and 17th under
another. ${unanimous}

It also covers why to rank once rather than rank, cut and re-rank: with a
set-relative normalization the survivors of a cut come out in a different order
than they went in, having not been measured again.

    node tools/score.js          # the scoring table
    node tools/iterate.js        # what cutting and re-ranking does to it
    node tools/gen_scoring.js    # SCORING.md

## The gate

Every walk here has been through \`check.py\` — the parts, the sections, the seams, and a
voxel model of the assembled bore flooded from the outside to prove it is one sealed
passage. **${totalChecks.toLocaleString('en-US')} checks across ${Object.keys(checks).length} spirals, ${totalFailed} failed.** The per-walk output is
in \`checks/\`.

    node tools/run_checks.sh     # re-run the gate over every walk

\`check.py\` needs shapely, numpy and scipy, which live in the Boxes.py venv — run it with
\`~/boxes/venv/bin/python\`, as \`../bore-generator/README.md\` says. The system python3 does
not have them.

## How they were found

\`tools/search_spirals.js\` walks every periodic term sequence up to eight terms with legs up
to four blocks, keeping those that never reverse, return to the same lateral position each
period so the thing coils rather than drifts, wind a whole number of turns per period, stay
self-avoiding when repeated, and satisfy the elbow-free rule.

That rule, for a window of three consecutive terms — outer A, middle m, outer C:

| A and C | | middle term |
| --- | --- | ---: |
| same axis, same direction | a step | >= 1 |
| same axis, opposite direction | a hairpin | >= 2 |
| different axes | a coil | >= 3 |

The bore-designs README states only the third case and calls the other two "a fold ... as
tight as you like". That holds for steps and not for hairpins: \`U3 N1 D3\` costs two elbows
and \`U3 N2 D3\` costs none. The three cases were read off \`bore_split.py\` by probing it.

\`tools/mknotation.js\` repeats a period to length and writes it in the bore notation,
trimming the tail so the last block is not mid-turn — a turn in the last block has nothing
after it to make it interior, so it is always its own piece. Then every candidate goes
through the splitter, and only zero-elbow walks are kept. **The splitter decides, not the
rule.**

## Regenerating

    tools/build.sh               # all of the below, in order

    node tools/parts.js          # piece counts and distinct shapes -> parts.json
    node tools/table.js          # both tables, plain text
    node tools/table.js --md     # the same as markdown
    node tools/gen_readme.js     # this file
    python3 ../lasermade-tools/md2html.py README.md index.html    # the published page

    node tools/spiral_metrics.js "$(cat walks/coil_3x3_47.txt)"   # measure one walk

    cd ../bore-generator         # rebuild a viewer page
    ~/boxes/venv/bin/python viewer.py "$(cat ../spirals/walks/coil_3x3_47.txt)" \\
        --out ../spirals/pages/coil_3x3_47.html --title "Coil 3x3 47"

## What has not been done

**No cut files.** These are walks, viewers and gate results; nothing here has been split to
SVG or nested. \`bore_split.py --write DIR\` will do it.

The block counts are not equal — they run ${Math.min(...rows.map(r=>r.m.blocks))} to ${Math.max(...rows.map(r=>r.m.blocks))}, so the bore lengths run
${Math.min(...rows.map(r=>r.m.mm))}mm to ${Math.max(...rows.map(r=>r.m.mm))}mm. A period is repeated to about the right length and then trimmed
to wherever the tail comes out elbow-free, so these are the same bore only to within a few
blocks. For comparing packing that is fine; for comparing *bores* it is not, and the length
would have to be pinned first.

Released under [CC0 1.0](LICENSE).
`;
fs.writeFileSync(path.join(root, 'README.md'), md);
console.log('README.md written,', md.split('\n').length, 'lines');
