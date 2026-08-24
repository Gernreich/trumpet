#!/usr/bin/env node
// Regenerate README.md. Every number in it comes from the tools, so the page
// cannot drift from the walks: node tools/gen_readme.js
const fs = require('fs'), path = require('path'), cp = require('child_process');
const { metrics } = require('./spiral_metrics.js');
const root = path.join(__dirname, '..');

const parts = JSON.parse(fs.readFileSync(path.join(root, 'parts.json'), 'utf8'));
const rows = fs.readdirSync(path.join(root, 'walks')).filter(f => f.endsWith('.txt'))
  .map(f => { const name = f.replace(/\.txt$/, '');
    const walk = fs.readFileSync(path.join(root,'walks',f),'utf8').trim();
    const p = parts[name] || {};
    // judged over the interior, described over the whole bore
    return { name, p, full: metrics(walk), m: metrics(walk, p.interiorBlocks) }; })
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
// The walk this started from, found through derived.txt rather than by name:
// standardising renamed every coil.
const derived = Object.fromEntries(
  fs.readFileSync(path.join(root,'derived.txt'),'utf8').split('\n')
    .map(l => l.replace(/#.*/,'').trim()).filter(Boolean)
    .map(l => { const [n, ...src] = l.split(/\s+/); return [n, src]; }));
const yours = rows.find(r => (derived[r.name] || []).includes('staircase_coil')) || rows[0];
const box   = best(r => r.m.vol);
const rise  = best(r => r.m.risePer360);
const tube  = best(r => r.m.blocksPer360);
const pcs   = best(r => r.p.innerPieces);
const dist  = best(r => r.p.interiorDistinct);
const calm  = best(r => r.m.turnsPerMetre);
const clean = rows.filter(r => r.m.touching === 0).sort((a,b) => a.m.vol - b.m.vol)[0];
const plateBest = rows.slice().sort((a,b) => b.p.meanPlate - a.p.meanPlate)[0];
// picked from the data, not named: standardising renamed every coil
const fewestShapes = rows.slice().sort((a,b) => a.p.interiorDistinct - b.p.interiorDistinct)[0];
const thinnest = rows.slice().sort((a,b) => (a.m.cross[0]*a.m.cross[1]) - (b.m.cross[0]*b.m.cross[1]))[0];
const fattest  = rows.slice().sort((a,b) => (b.m.cross[0]*b.m.cross[1]) - (a.m.cross[0]*a.m.cross[1]))[0];
const worstEnds = rows.slice().sort((a,b) => (b.p.distinct - b.p.interiorDistinct) - (a.p.distinct - a.p.interiorDistinct))[0];
const L = r => `[\`${r.name}\`](pages/${r.name}.html)`;
const { rows: srows, R: SR } = require('./score.js');
const { results: minres } = require('./minimal.js');
const minimal = minres.filter(r => r.saving === 0).map(r => r.name);
const slackiest = minres.slice().sort((a, b) => b.saving - a.saving)[0];
const stair = minres.find(r => r.name === yours.name) || minres[0];
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

## Standardised

Every coil here is in the same orientation, so two coils differ only where they really
differ:

* **forward is north** for all of them, and each walk opens on a north term
* **counter-clockwise**, seen looking along the bore from the mouth
* **whole periods only**, as many as fit within three times the longest period
  (48 x 3 = 144 blocks)
* **one block in, one block out**, and no partial period between them

A bore opens at both ends, so the first and last piece cannot be removed — they are
bounded by the mouth and the exit rather than by a neighbour, and the notation says as
much: the first term is only the way you came in. What is standardised is that every
walk has exactly one of each, and the judged metrics ignore them regardless.

Standardising collapsed 30 walks into ${rows.length}: several that looked different were the same
coil in another orientation, and [\`derived.txt\`](derived.txt) records which. The hand
reduction of the staircase coil, the tool's reduction of it, and the extension of the
hand reduction all turn out to be one coil.

**The one cost.** Whole periods of different lengths cannot all reach 144, so the bores
run ${Math.min(...rows.map(r=>r.full.blocks))} to ${Math.max(...rows.map(r=>r.full.blocks))} blocks — ${Math.min(...rows.map(r=>r.full.mm))}mm to ${Math.max(...rows.map(r=>r.full.mm))}mm, a spread of ${((Math.max(...rows.map(r=>r.full.mm))/Math.min(...rows.map(r=>r.full.mm))-1)*100).toFixed(0)}%. That is much wider
than the 1.6% the set used to hold, and it flatters the shorter coils on every measure
of size: a 127-block coil has less tube to put anywhere. Read the box column with the
blocks column beside it.

## Shape and cost

${tbl('--shape')}

Envelope, box and cross-section are in blocks; a block is 31mm of centreline. Sorted by
box, smallest first.

**The bore's mouth and exit are not judged.** Every design has them, no design chooses
them, and they are the two pieces that never join the rhythm — so every column here
except blocks and mm is measured on the interior, the pieces in between. It is not a
cosmetic change: the ends stick out of the envelope they bracket. \`${worstEnds.name}\` needs ${worstEnds.p.interiorDistinct} shapes
rather than ${worstEnds.p.distinct}, the difference being end pieces alone. Blocks and mm still describe the whole bore, because that is what the bore is.

**Cross-section** is the envelope with the coil axis taken out — how fat the coil is,
which is what decides whether it fits inside anything. It is not implied by the box: ${L(thinnest)} is
${thinnest.m.cross.join('x')} in section and ${L(fattest)} is ${fattest.m.cross.join('x')}, and the box does not say so.

**Distinct** is how many different piece shapes the cut list holds. A coil built by
repeating one period needs only a handful, however long it runs: ${dist.name} is
${dist.p.pieces} pieces cut from ${dist.p.distinct} shapes. The widest needs ${rows.slice().sort((a,b)=>b.p.interiorDistinct-a.p.interiorDistinct)[0].p.interiorDistinct}. That is files to check and parts to tell apart on the bench, and it
does not show up in the piece count at all.

**Rhythm** is how many pieces you lay before the cut list starts over, and how many
times it recurs. It is descriptive, not scored: across coils built by repeating a period
it barely varies — ${rows.filter(r => r.p.rhythm === 4).length} of the ${rows.length} here are a 4-piece rhythm — and a near-constant metric
in a mean only dilutes the ones that discriminate. It is worth knowing at the bench all
the same, and it is not the same thing as **distinct**: the two rank the set alike in
only 6 of ${rows.length} places. \`${fewestShapes.name}\` is ${fewestShapes.p.interiorDistinct} shapes laid in a
${fewestShapes.p.rhythm}-piece cycle repeated ${fewestShapes.p.repeats.toFixed(1)} times, between the two end pieces.

**Mean plate** is the average bounding box a piece is cut from, in mm2 — the
laser-cutting number. Fewer, larger parts means less weeding, less sorting and fewer
fingers to align, and it is the size of the part in your hand rather than the count of
them. \`${plateBest.name}\` averages ${Math.round(plateBest.p.meanPlate).toLocaleString('en-US')} mm2 against \`${yours.name}\`'s ${Math.round(yours.p.meanPlate).toLocaleString('en-US')}.

Average *blocks* per piece was the other reading of the same idea and is not used: the
block count varies by only ${((Math.max(...rows.map(r=>r.m.blocks))/Math.min(...rows.map(r=>r.m.blocks))-1)*100).toFixed(1)}% across the set, so blocks-per-piece is very nearly the
reciprocal of the piece count and ranks the set the same way in 15 of ${rows.length} places. Plate
area is not redundant: ${(() => {
  const byPieces = {};
  for (const r of rows) (byPieces[r.p.innerPieces] ||= []).push(r);
  const tie = Object.values(byPieces).filter(g => g.length > 1)
    .sort((a,b) => b.length - a.length)[0];
  if (!tie) return 'coils that tie on piece count still differ on it';
  return tie.map(r => '\`' + r.name + '\`').join(', ') + ' all split into ' +
    tie[0].p.innerPieces + ' pieces and cannot be told apart by blocks-per-piece at all, ' +
    'while their mean plates are ' +
    tie.map(r => Math.round(r.p.meanPlate).toLocaleString('en-US')).join(', ') + ' mm2';
})()}.

It is a bounding box, not the cut outline — an L-shaped piece leaves its corner behind
— so it measures the size of the part, not the material consumed.

**Touching** counts blocks that sit face to face without being joined along the bore —
two runs of the tube sharing a wall. \`bore_split.py\` warns about them, and they are the
version of "density" that has a consequence: where the bore passes itself, that one wall
is all that separates the two passages.

Because a shared wall shows in the finished instrument, it is the heaviest input in the
scoring and is penalized convexly — 1/(1+t), so no contact scores 1.000 and eight
contacts 0.111. \`node tools/score.js --clean\` ranks only the coils that have none.

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

| | winner | against the walk this started from |
| --- | --- | --- |
| smallest box | ${L(box)} — ${box.m.vol} | ${yours.m.vol}, so ${(yours.m.vol/box.m.vol).toFixed(2)}x larger |
| tightest spiral (least rise per turn) | ${L(rise)} — ${Math.round(rise.m.riseMMPer360)}mm | ${Math.round(yours.m.riseMMPer360)}mm, so ${(yours.m.risePer360/rise.m.risePer360).toFixed(1)}x slacker |
| least tube per turn | ${L(tube)} — ${tube.m.blocksPer360.toFixed(1)} blk | ${yours.m.blocksPer360.toFixed(1)} blk, within ${((yours.m.blocksPer360/tube.m.blocksPer360-1)*100).toFixed(0)}% |
| fewest pieces | ${L(pcs)} — ${pcs.p.innerPieces} | ${yours.p.innerPieces} |
| fewest distinct shapes | ${L(dist)} — ${dist.p.interiorDistinct} | ${yours.p.interiorDistinct} |
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

## Every block load-bearing

The staircase coil was reduced by hand — blocks removed wherever one could go without
introducing an elbow — and that reduction is in this set. (The names below predate
standardising, which renamed every coil; [\`derived.txt\`](derived.txt) maps them.)
\`tools/minimal.js\` checks the claim: a term's floor is 3 in a coil window, 2 in a
hairpin, 1 in a step, and a walk whose every term sits on its floor cannot be shortened
at all.

    node tools/minimal.js            # every walk
    node tools/minimal.js --terms    # and which terms have slack

Before it was reduced, the staircase coil had 16 terms with slack, every one a hairpin
sitting at 3 where 2 would do, and the reduction left **none**. It was exhaustive: the
tool later reproduced it exactly, and standardising then showed the two to be one coil.

It also says something about the search. Only **${minimal.length} of ${minres.length}** walks here are minimal:
${minimal.map(n => '\`' + n + '\`').join(', ')}. The search enumerated periods with legs up to
4 and never asked whether a leg was longer than it had to be, so most of what it found
carries slack — \`${slackiest.name}\` could lose ${slackiest.saving} blocks. Two of the ${minimal.length} minimal walks are
the two that were reduced by hand.

Removing slack is not automatically safe. The rule is local, and a shortened walk can
run into itself or start touching, so what the tool reports are candidates to put back
through \`bore_split.py\`.

### The reduction pass, and why minimality is not an optimisation

\`tools/reduce.js\` takes the slack out and rebuilds at comparable length. It has to
enumerate rather than apply, because **coiling is global and the elbow rule is local**.
A period coils only if it closes: drifting on one axis and returning to where it started
on the other two. Shorten one leg and not its opposite and the period stops closing, so
the walk wanders off diagonally instead of coiling. Taken naively, one coil went from a
box of 423 to **10,452** — still elbow-free, no longer a coil.

Keeping only the reductions that still close and still wind a whole number of turns, 14
of the ${minres.length} walks reduce. What that buys:

| | |
| --- | ---: |
| box smaller | 6 |
| box bigger | 7 |
| touching reduced | 2 |
| touching increased | 6 |

And **nothing it produced beat what was already there**: the smallest box stayed at 423
against the reduced field's 462, and the smallest walls-free at 477 against 522.

That is the point worth keeping. Shortening a leg reduces how far the coil advances per
turn, so the same tube buys more revolutions in a fatter, shorter package — a different
design, not a better one. Every block being load-bearing is a property, not a virtue.

One thing the pass did find: four results the search reported as distinct all reduce to
**the same walk**, \`E2 S3 U1 S3 W2 N3 U1 N3\` — one design wearing four amounts of slack.
Standardising later found more of the same, and \`derived.txt\` records every merge.

The reduced walks are kept, named \`*_min\`, with their sources recorded in
[\`derived.txt\`](derived.txt). They are in the scoring like anything else, so the
composite is now over a set that contains both a design and its own reduction — worth
remembering when reading a rank, since the normalization is across whatever is present.

    node tools/reduce.js             # the pass
    node tools/reduce.js --write     # and reduced.json

## Walks kept but not scored

The scoring normalizes every metric across the set, so a walk of a different length does
not merely rank oddly — it rescales everyone else. Those walks live in the repository and
in the tables, below a rule, and are listed in [\`unscored.txt\`](unscored.txt) with the
reason. Their rate metrics — blocks/360, rise/360, turns/m, touching — stay comparable
and are still worth reading.

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

    node tools/spiral_metrics.js "$(cat walks/${rows[0].name}.txt)"   # measure one walk

    cd ../bore-generator         # rebuild a viewer page
    ~/boxes/venv/bin/python viewer.py "$(cat ../spirals/walks/${rows[0].name}.txt)" \\
        --out ../spirals/pages/${rows[0].name}.html --title "${rows[0].name.replace(/_/g,' ')}"

## What has not been done

**No cut files.** These are walks, viewers and gate results; nothing here has been split to
SVG or nested. \`bore_split.py --write DIR\` will do it.

The block counts are not equal — the scored ones run ${Math.min(...rows.map(r=>r.m.blocks))} to ${Math.max(...rows.map(r=>r.m.blocks))}, so their bore lengths
run ${Math.min(...rows.map(r=>r.m.mm))}mm to ${Math.max(...rows.map(r=>r.m.mm))}mm, a spread of ${((Math.max(...rows.map(r=>r.m.mm))/Math.min(...rows.map(r=>r.m.mm))-1)*100).toFixed(1)}%. A period is repeated to about the right length and then trimmed
to wherever the tail comes out elbow-free, so these are the same bore only to within a few
blocks. For comparing packing that is fine; for comparing *bores* it is not, and the length
would have to be pinned first.

Released under [CC0 1.0](LICENSE).
`;
fs.writeFileSync(path.join(root, 'README.md'), md);
console.log('README.md written,', md.split('\n').length, 'lines');
