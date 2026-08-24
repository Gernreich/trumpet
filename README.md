# Spirals

Coiling bore walks that turn about an axis while advancing along it, collected with the
numbers that say how hard each one spirals and what each one costs to build. Every walk
here splits with **no elbows** — every turn folds into a piece as an L, none is stranded
as a single-block piece of its own — and every one passes the full gate.

The one this started from is [`coil_4x4_38`](pages/coil_4x4_38.html); the other 23 came out of an
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

Standardising collapsed 30 walks into 24: several that looked different were the same
coil in another orientation, and [`derived.txt`](derived.txt) records which. The hand
reduction of the staircase coil, the tool's reduction of it, and the extension of the
hand reduction all turn out to be one coil.

**The one cost.** Whole periods of different lengths cannot all reach 144, so the bores
run 127 to 145 blocks — 3937mm to 4495mm, a spread of 14%. That is much wider
than the 1.6% the set used to hold, and it flatters the shorter coils on every measure
of size: a 127-block coil has less tube to put anywhere. Read the box column with the
blocks column beside it.

## Shape and cost

| spiral | blocks | mm | envelope | box | cross-section | along axis | pieces | distinct | rhythm | mean plate mm2 | touching |
| --- | ---: | ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [`coil_3x3_33`](pages/coil_3x3_33.html) | 127 | 3937 | 3 x 3 x 30 | 270 | 3 x 3 blk / 93 x 93 mm | 30 / 930 mm | 22 | 4 | 4 x5.5 | 8404 | 5 |
| [`coil_3x3_36`](pages/coil_3x3_36.html) | 127 | 3937 | 3 x 3 x 31 | 279 | 3 x 3 blk / 93 x 93 mm | 31 / 961 mm | 22 | 3 | 4 x5.5 | 8404 | 4 |
| [`coil_3x3_38`](pages/coil_3x3_38.html) | 133 | 4123 | 3 x 3 x 35 | 315 | 3 x 3 blk / 93 x 93 mm | 35 / 1085 mm | 22 | 4 | 4 x5.5 | 9216 | 0 |
| [`coil_3x9_14`](pages/coil_3x9_14.html) | 133 | 4123 | 3 x 9 x 12 | 324 | 3 x 9 blk / 93 x 279 mm | 12 / 372 mm | 22 | 4 | 4 x5.5 | 8736 | 9 |
| [`coil_3x3_42`](pages/coil_3x3_42.html) | 133 | 4123 | 3 x 3 x 37 | 333 | 3 x 3 blk / 93 x 93 mm | 37 / 1147 mm | 22 | 3 | 4 x5.5 | 9216 | 0 |
| [`coil_3x7_18`](pages/coil_3x7_18.html) | 145 | 4495 | 3 x 7 x 16 | 336 | 3 x 7 blk / 93 x 217 mm | 16 / 496 mm | 30 | 4 | 4 x7.5 | 6240 | 13 |
| [`coil_3x7_18_2`](pages/coil_3x7_18_2.html) | 145 | 4495 | 7 x 3 x 16 | 336 | 3 x 7 blk / 93 x 217 mm | 16 / 496 mm | 30 | 4 | 4 x7.5 | 6240 | 13 |
| [`coil_3x8_16`](pages/coil_3x8_16.html) | 141 | 4371 | 8 x 3 x 14 | 336 | 3 x 8 blk / 93 x 248 mm | 14 / 434 mm | 26 | 4 | 4 x6.5 | 7728 | 11 |
| [`coil_3x3_44`](pages/coil_3x3_44.html) | 141 | 4371 | 3 x 3 x 40 | 360 | 3 x 3 blk / 93 x 93 mm | 40 / 1240 mm | 26 | 4 | 4 x6.5 | 7728 | 0 |
| [`coil_3x3_44_2`](pages/coil_3x3_44_2.html) | 141 | 4371 | 3 x 3 x 40 | 360 | 3 x 3 blk / 93 x 93 mm | 40 / 1240 mm | 26 | 3 | 4 x6.5 | 7614 | 0 |
| [`coil_3x3_47`](pages/coil_3x3_47.html) | 141 | 4371 | 3 x 3 x 42 | 378 | 3 x 3 blk / 93 x 93 mm | 42 / 1302 mm | 26 | 3 | 4 x6.5 | 7728 | 0 |
| [`coil_4x8_14`](pages/coil_4x8_14.html) | 133 | 4123 | 4 x 8 x 12 | 384 | 4 x 8 blk / 124 x 248 mm | 12 / 372 mm | 22 | 4 | 4 x5.5 | 8871 | 9 |
| [`coil_4x7_16`](pages/coil_4x7_16.html) | 141 | 4371 | 4 x 7 x 14 | 392 | 4 x 7 blk / 124 x 217 mm | 14 / 434 mm | 26 | 4 | 4 x6.5 | 7248 | 11 |
| [`coil_2x2_110`](pages/coil_2x2_110.html) | 145 | 4495 | 2 x 2 x 102 | 408 | 2 x 2 blk / 62 x 62 mm | 102 / 3162 mm | 34 | 2 | 4 x8.5 | 6240 | 0 |
| [`coil_5x7_14`](pages/coil_5x7_14.html) | 133 | 4123 | 5 x 7 x 12 | 420 | 5 x 7 blk / 155 x 217 mm | 12 / 372 mm | 22 | 4 | 4 x5.5 | 8255 | 9 |
| [`coil_4x9_14`](pages/coil_4x9_14.html) | 145 | 4495 | 9 x 4 x 12 | 432 | 4 x 9 blk / 124 x 279 mm | 12 / 372 mm | 22 | 4 | 4 x5.5 | 10224 | 9 |
| [`coil_5x8_14`](pages/coil_5x8_14.html) | 145 | 4495 | 5 x 8 x 12 | 480 | 5 x 8 blk / 155 x 248 mm | 12 / 372 mm | 22 | 4 | 4 x5.5 | 10704 | 9 |
| [`coil_4x4_38`](pages/coil_4x4_38.html) | 145 | 4495 | 4 x 4 x 34 | 544 | 4 x 4 blk / 124 x 124 mm | 34 / 1054 mm | 33 | 8 | 12 x2.8 | 5568 | 0 |
| [`coil_3x4_56_2`](pages/coil_3x4_56_2.html) | 145 | 4495 | 4 x 3 x 49 | 588 | 3 x 4 blk / 93 x 124 mm | 49 / 1519 mm | 34 | 4 | 4 x8.5 | 5933 | 0 |
| [`coil_3x4_56_3`](pages/coil_3x4_56_3.html) | 145 | 4495 | 3 x 4 x 49 | 588 | 3 x 4 blk / 93 x 124 mm | 49 / 1519 mm | 34 | 4 | 4 x8.5 | 5933 | 0 |
| [`coil_3x4_56`](pages/coil_3x4_56.html) | 145 | 4495 | 4 x 3 x 51 | 612 | 3 x 4 blk / 93 x 124 mm | 51 / 1581 mm | 33 | 4 | 4 x8.3 | 5923 | 0 |
| [`coil_3x4_56_4`](pages/coil_3x4_56_4.html) | 145 | 4495 | 4 x 3 x 51 | 612 | 3 x 4 blk / 93 x 124 mm | 51 / 1581 mm | 33 | 4 | 4 x8.3 | 5923 | 0 |
| [`coil_3x4_58`](pages/coil_3x4_58.html) | 137 | 4247 | 3 x 4 x 52 | 624 | 3 x 4 blk / 93 x 124 mm | 52 / 1612 mm | 29 | 4 | 4 x7.3 | 6634 | 0 |
| [`coil_5x5_38`](pages/coil_5x5_38.html) | 133 | 4123 | 5 x 5 x 34 | 850 | 5 x 5 blk / 155 x 155 mm | 34 / 1054 mm | 33 | 8 | 12 x2.8 | 4897 | 0 |

Envelope, box and cross-section are in blocks; a block is 31mm of centreline. Sorted by
box, smallest first.

**The bore's mouth and exit are not judged.** Every design has them, no design chooses
them, and they are the two pieces that never join the rhythm — so every column here
except blocks and mm is measured on the interior, the pieces in between. It is not a
cosmetic change: the ends stick out of the envelope they bracket. `coil_3x3_33` needs 4 shapes
rather than 6, the difference being end pieces alone. Blocks and mm still describe the whole bore, because that is what the bore is.

**Cross-section** is the envelope with the coil axis taken out — how fat the coil is,
which is what decides whether it fits inside anything. It is not implied by the box: [`coil_2x2_110`](pages/coil_2x2_110.html) is
2x2 in section and [`coil_5x8_14`](pages/coil_5x8_14.html) is 5x8, and the box does not say so.

**Distinct** is how many different piece shapes the cut list holds. A coil built by
repeating one period needs only a handful, however long it runs: coil_2x2_110 is
36 pieces cut from 4 shapes. The widest needs 8. That is files to check and parts to tell apart on the bench, and it
does not show up in the piece count at all.

**Rhythm** is how many pieces you lay before the cut list starts over, and how many
times it recurs. It is descriptive, not scored: across coils built by repeating a period
it barely varies — 22 of the 24 here are a 4-piece rhythm — and a near-constant metric
in a mean only dilutes the ones that discriminate. It is worth knowing at the bench all
the same, and it is not the same thing as **distinct**: the two rank the set alike in
only 6 of 24 places. `coil_2x2_110` is 2 shapes laid in a
4-piece cycle repeated 8.5 times, between the two end pieces.

**Mean plate** is the average bounding box a piece is cut from, in mm2 — the
laser-cutting number. Fewer, larger parts means less weeding, less sorting and fewer
fingers to align, and it is the size of the part in your hand rather than the count of
them. `coil_5x8_14` averages 10,704 mm2 against `coil_4x4_38`'s 5,568.

Average *blocks* per piece was the other reading of the same idea and is not used: the
block count varies by only 18.3% across the set, so blocks-per-piece is very nearly the
reciprocal of the piece count and ranks the set the same way in 15 of 24 places. Plate
area is not redundant: `coil_3x3_33`, `coil_3x3_36`, `coil_3x3_38`, `coil_3x9_14`, `coil_3x3_42`, `coil_4x8_14`, `coil_5x7_14`, `coil_4x9_14`, `coil_5x8_14` all split into 22 pieces and cannot be told apart by blocks-per-piece at all, while their mean plates are 8,404, 8,404, 9,216, 8,736, 9,216, 8,871, 8,255, 10,224, 10,704 mm2.

It is a bounding box, not the cut outline — an L-shaped piece leaves its corner behind
— so it measures the size of the part, not the material consumed.

**Touching** counts blocks that sit face to face without being joined along the bore —
two runs of the tube sharing a wall. `bore_split.py` warns about them, and they are the
version of "density" that has a consequence: where the bore passes itself, that one wall
is all that separates the two passages.

Because a shared wall shows in the finished instrument, it is the heaviest input in the
scoring and is penalized convexly — 1/(1+t), so no contact scores 1.000 and eight
contacts 0.111. `node tools/score.js --clean` ranks only the coils that have none.

It is also the one packing number that is *not* implied by the box. [`coil_3x3_33`](pages/coil_3x3_33.html) has the
smallest box in the set and 5 shared walls; [`coil_3x3_38`](pages/coil_3x3_38.html) is
17% larger and has **none**. If a shared wall
is something to avoid, the smallest box is not the one to build.

## Rotation

| spiral | axis | rotation | turns | blocks/360 | rise/360 blk / mm | deg/block | 90deg turns | turns/m | longest straight |
| --- | :-: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [`coil_3x3_33`](pages/coil_3x3_33.html) | N | 1890 | 5.25 | 22.1 | 4.38 / 136 | 16.3 | 44 | 12.2 | 4 blk / 124 mm |
| [`coil_3x3_36`](pages/coil_3x3_36.html) | N | 1890 | 5.25 | 21.9 | 5.71 / 177 | 16.4 | 44 | 12.3 | 4 blk / 124 mm |
| [`coil_3x3_38`](pages/coil_3x3_38.html) | N | 1890 | 5.25 | 23.0 | 5.71 / 177 | 15.6 | 44 | 11.7 | 4 blk / 124 mm |
| [`coil_3x9_14`](pages/coil_3x9_14.html) | N | 1980 | 5.50 | 22.0 | 2.00 / 62 | 16.4 | 44 | 11.7 | 4 blk / 124 mm |
| [`coil_3x3_42`](pages/coil_3x3_42.html) | N | 1890 | 5.25 | 23.0 | 6.86 / 213 | 15.6 | 44 | 11.7 | 4 blk / 124 mm |
| [`coil_3x7_18`](pages/coil_3x7_18.html) | N | 2700 | 7.50 | 18.0 | 2.00 / 62 | 20.0 | 60 | 14.3 | 3 blk / 93 mm |
| [`coil_3x7_18_2`](pages/coil_3x7_18_2.html) | N | 2700 | 7.50 | 18.0 | 2.00 / 62 | 20.0 | 60 | 14.3 | 3 blk / 93 mm |
| [`coil_3x8_16`](pages/coil_3x8_16.html) | N | 2340 | 6.50 | 20.0 | 2.00 / 62 | 18.0 | 52 | 12.9 | 4 blk / 124 mm |
| [`coil_3x3_44`](pages/coil_3x3_44.html) | N | 2250 | 6.25 | 20.8 | 5.92 / 184 | 17.3 | 52 | 12.9 | 3 blk / 93 mm |
| [`coil_3x3_44_2`](pages/coil_3x3_44_2.html) | N | 2250 | 6.25 | 20.8 | 5.60 / 174 | 17.3 | 52 | 12.9 | 3 blk / 93 mm |
| [`coil_3x3_47`](pages/coil_3x3_47.html) | N | 2250 | 6.25 | 20.8 | 6.56 / 203 | 17.3 | 52 | 12.9 | 3 blk / 93 mm |
| [`coil_4x8_14`](pages/coil_4x8_14.html) | N | 1980 | 5.50 | 22.2 | 2.00 / 62 | 16.2 | 44 | 11.6 | 4 blk / 124 mm |
| [`coil_4x7_16`](pages/coil_4x7_16.html) | N | 2340 | 6.50 | 20.0 | 2.00 / 62 | 18.0 | 52 | 12.9 | 3 blk / 93 mm |
| [`coil_2x2_110`](pages/coil_2x2_110.html) | N | 2970 | 8.25 | 16.5 | 12.24 / 380 | 21.8 | 68 | 16.1 | 3 blk / 93 mm |
| [`coil_5x7_14`](pages/coil_5x7_14.html) | N | 1980 | 5.50 | 22.0 | 2.00 / 62 | 16.4 | 44 | 11.7 | 4 blk / 124 mm |
| [`coil_4x9_14`](pages/coil_4x9_14.html) | N | 1980 | 5.50 | 24.0 | 2.00 / 62 | 15.0 | 44 | 10.8 | 4 blk / 124 mm |
| [`coil_5x8_14`](pages/coil_5x8_14.html) | N | 1980 | 5.50 | 24.0 | 2.00 / 62 | 15.0 | 44 | 10.8 | 4 blk / 124 mm |
| [`coil_4x4_38`](pages/coil_4x4_38.html) | N | 2970 | 8.25 | 16.0 | 4.00 / 124 | 22.5 | 44 | 10.8 | 3 blk / 93 mm |
| [`coil_3x4_56_2`](pages/coil_3x4_56_2.html) | N | 3060 | 8.50 | 16.0 | 5.65 / 175 | 22.5 | 51 | 12.1 | 3 blk / 93 mm |
| [`coil_3x4_56_3`](pages/coil_3x4_56_3.html) | N | 3060 | 8.50 | 16.0 | 5.65 / 175 | 22.5 | 51 | 12.1 | 3 blk / 93 mm |
| [`coil_3x4_56`](pages/coil_3x4_56.html) | N | 2880 | 8.00 | 16.4 | 6.25 / 194 | 22.0 | 49 | 12.1 | 3 blk / 93 mm |
| [`coil_3x4_56_4`](pages/coil_3x4_56_4.html) | N | 2880 | 8.00 | 16.4 | 6.25 / 194 | 22.0 | 49 | 12.1 | 3 blk / 93 mm |
| [`coil_3x4_58`](pages/coil_3x4_58.html) | N | 2520 | 7.00 | 17.4 | 7.29 / 226 | 20.7 | 57 | 15.1 | 3 blk / 93 mm |
| [`coil_5x5_38`](pages/coil_5x5_38.html) | N | 2970 | 8.25 | 14.7 | 4.00 / 124 | 24.5 | 44 | 11.7 | 3 blk / 93 mm |

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
| smallest box | [`coil_3x3_33`](pages/coil_3x3_33.html) — 270 | 544, so 2.01x larger |
| tightest spiral (least rise per turn) | [`coil_3x9_14`](pages/coil_3x9_14.html) — 62mm | 124mm, so 2.0x slacker |
| least tube per turn | [`coil_5x5_38`](pages/coil_5x5_38.html) — 14.7 blk | 16.0 blk, within 9% |
| fewest pieces | [`coil_3x3_33`](pages/coil_3x3_33.html) — 22 | 33 |
| fewest distinct shapes | [`coil_2x2_110`](pages/coil_2x2_110.html) — 2 | 8 |
| largest average plate | [`coil_5x8_14`](pages/coil_5x8_14.html) — 10,704 mm2 | 5,568 mm2 |
| calmest bore (fewest turns/m) | [`coil_4x9_14`](pages/coil_4x9_14.html) — 10.8 | 10.8 |
| smallest box with no shared wall | [`coil_3x3_38`](pages/coil_3x3_38.html) — 315 | 544, also 0 shared |

The staircase coil loses on packing and wins, or nearly wins, on the two that bear on how
the thing sounds: it spends the least tube per revolution of almost anything here, and it
turns the air the fewest times per metre. **Packing tighter costs bends**, and bends are
the thing a bore notices.

## A metric deliberately left out

Fill density — blocks over box volume — was tried and dropped. At a fixed tube length it
is not independent of the box: blocks is near enough constant, so density is just the
reciprocal of box volume rescaled. Ranking these 24 spirals by density puts them in the
same order as ranking by box in 16 of 24 positions, and the two that swap are a tie at
477 broken by a one-block difference in length. It reads like a second opinion and is not
one. It would earn its place only in comparing walks of genuinely different lengths.

**Touching** is the metric density was reaching for. It answers the question density
sounds like it answers — how hard is this bore packed against itself — and unlike density
it disagrees with the box often enough to change which coil you would build.

## Every block load-bearing

The staircase coil was reduced by hand — blocks removed wherever one could go without
introducing an elbow — and that reduction is in this set. (The names below predate
standardising, which renamed every coil; [`derived.txt`](derived.txt) maps them.)
`tools/minimal.js` checks the claim: a term's floor is 3 in a coil window, 2 in a
hairpin, 1 in a step, and a walk whose every term sits on its floor cannot be shortened
at all.

    node tools/minimal.js            # every walk
    node tools/minimal.js --terms    # and which terms have slack

Before it was reduced, the staircase coil had 16 terms with slack, every one a hairpin
sitting at 3 where 2 would do, and the reduction left **none**. It was exhaustive: the
tool later reproduced it exactly, and standardising then showed the two to be one coil.

It also says something about the search. Only **5 of 24** walks here are minimal:
`coil_2x2_110`, `coil_3x4_58`, `coil_3x7_18`, `coil_3x7_18_2`, `coil_5x5_38`. The search enumerated periods with legs up to
4 and never asked whether a leg was longer than it had to be, so most of what it found
carries slack — `coil_4x9_14` could lose 36 blocks. Two of the 5 minimal walks are
the two that were reduced by hand.

Removing slack is not automatically safe. The rule is local, and a shortened walk can
run into itself or start touching, so what the tool reports are candidates to put back
through `bore_split.py`.

### The reduction pass, and why minimality is not an optimisation

`tools/reduce.js` takes the slack out and rebuilds at comparable length. It has to
enumerate rather than apply, because **coiling is global and the elbow rule is local**.
A period coils only if it closes: drifting on one axis and returning to where it started
on the other two. Shorten one leg and not its opposite and the period stops closing, so
the walk wanders off diagonally instead of coiling. Taken naively, one coil went from a
box of 423 to **10,452** — still elbow-free, no longer a coil.

Keeping only the reductions that still close and still wind a whole number of turns, 14
of the 24 walks reduce. What that buys:

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
**the same walk**, `E2 S3 U1 S3 W2 N3 U1 N3` — one design wearing four amounts of slack.
Standardising later found more of the same, and `derived.txt` records every merge.

The reduced walks are kept, named `*_min`, with their sources recorded in
[`derived.txt`](derived.txt). They are in the scoring like anything else, so the
composite is now over a set that contains both a design and its own reduction — worth
remembering when reading a rank, since the normalization is across whatever is present.

    node tools/reduce.js             # the pass
    node tools/reduce.js --write     # and reduced.json

## Walks kept but not scored

The scoring normalizes every metric across the set, so a walk of a different length does
not merely rank oddly — it rescales everyone else. Those walks live in the repository and
in the tables, below a rule, and are listed in [`unscored.txt`](unscored.txt) with the
reason. Their rate metrics — blocks/360, rise/360, turns/m, touching — stay comparable
and are still worth reading.

## Scoring them against each other

[**SCORING.md**](SCORING.md) combines seven of the metrics and the touching count into
a single ranking under every common mean — harmonic, geometric, arithmetic, quadratic,
cubic, median, midrange, contraharmonic — and reports what the choice of mean does to
the answer. It does a great deal: `coil_2x2_146` places 1st under one and 17th under
another. `coil_3x3_38` comes first under 3 of the 8 means.

It also covers why to rank once rather than rank, cut and re-rank: with a
set-relative normalization the survivors of a cut come out in a different order
than they went in, having not been measured again.

    node tools/score.js          # the scoring table
    node tools/iterate.js        # what cutting and re-ranking does to it
    node tools/gen_scoring.js    # SCORING.md

## The gate

Every walk here has been through `check.py` — the parts, the sections, the seams, and a
voxel model of the assembled bore flooded from the outside to prove it is one sealed
passage. **22,866 checks across 24 spirals, 0 failed.** The per-walk output is
in `checks/`.

    node tools/run_checks.sh     # re-run the gate over every walk

`check.py` needs shapely, numpy and scipy, which live in the Boxes.py venv — run it with
`~/boxes/venv/bin/python`, as `../bore-generator/README.md` says. The system python3 does
not have them.

## How they were found

`tools/search_spirals.js` walks every periodic term sequence up to eight terms with legs up
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
tight as you like". That holds for steps and not for hairpins: `U3 N1 D3` costs two elbows
and `U3 N2 D3` costs none. The three cases were read off `bore_split.py` by probing it.

`tools/mknotation.js` repeats a period to length and writes it in the bore notation,
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

    node tools/spiral_metrics.js "$(cat walks/coil_3x3_33.txt)"   # measure one walk

    cd ../bore-generator         # rebuild a viewer page
    ~/boxes/venv/bin/python viewer.py "$(cat ../spirals/walks/coil_3x3_33.txt)" \
        --out ../spirals/pages/coil_3x3_33.html --title "coil 3x3 33"

## What has not been done

**No cut files.** These are walks, viewers and gate results; nothing here has been split to
SVG or nested. `bore_split.py --write DIR` will do it.

The block counts are not equal — the scored ones run 115 to 136, so their bore lengths
run 3565mm to 4216mm, a spread of 18.3%. A period is repeated to about the right length and then trimmed
to wherever the tail comes out elbow-free, so these are the same bore only to within a few
blocks. For comparing packing that is fine; for comparing *bores* it is not, and the length
would have to be pinned first.

Released under [CC0 1.0](LICENSE).
