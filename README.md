# Spirals

Coiling bore walks that turn about an axis while advancing along it, collected with
the numbers that say how *hard* each one spirals. Every walk here splits into pieces
with **no elbows** — every turn folds into a piece as an L, none is stranded as a
single-block piece of its own.

The one this started from is [`staircase_coil`](pages/staircase_coil.html); the rest
came out of an exhaustive search for something tighter.

## The rotation metrics

A coil turns about one axis while travelling down it. Drop that axis and what is left
— the lateral projection — is what actually rotates, and on a cubic lattice it can only
turn in ninety degree steps. So the winding is counted in quarter turns and multiplied
up. Steps along the coil axis project to nothing and are skipped: they are advance, not
rotation.

* **Rotation** — the whole turn of the walk end to end, in degrees. 4230 degrees is
  11.75 full turns.
* **Blocks / 360** — tube spent on one complete revolution. Lower is a tighter spiral:
  less bore buys the same turn.
* **Rise / 360** — how far down its own axis the coil has to travel to come back round
  to where it started, in blocks and in mm. This is the pitch. Lower is a steeper coil,
  packed closer along the axis.
* **Deg / block** — the same thing per block, averaged over the walk.

**Axis** names the direction the coil advances, which is not north for all of them —
the search was free to build about any axis, so a coil that runs east is measured
against east.

## The spirals

| spiral | blocks | mm | envelope | box | pieces | axis | rotation | turns | blocks/360 | rise/360 blk / mm | deg/block |
| --- | ---: | ---: | --- | ---: | ---: | :-: | ---: | ---: | ---: | ---: | ---: |
| [`coil_3x3_47`](pages/coil_3x3_47.html) | 193 | 5983 | 47 x 3 x 3 | 423 | 37 | E | 3240 | 9.00 | 21.4 | 5.11 / 158 | 16.8 |
| [`coil_3x3_50`](pages/coil_3x3_50.html) | 193 | 5983 | 50 x 3 x 3 | 450 | 37 | E | 3240 | 9.00 | 21.4 | 5.11 / 158 | 16.8 |
| [`coil_3x7_22`](pages/coil_3x7_22.html) | 193 | 5983 | 3 x 22 x 7 | 462 | 43 | U | 3870 | 10.75 | 18.0 | 1.95 / 61 | 20.1 |
| [`coil_3x3_53`](pages/coil_3x3_53.html) | 193 | 5983 | 53 x 3 x 3 | 477 | 36 | E | 3150 | 8.75 | 22.1 | 5.71 / 177 | 16.3 |
| [`coil_3x3_53_2`](pages/coil_3x3_53_2.html) | 194 | 6014 | 3 x 3 x 53 | 477 | 35 | N | 3060 | 8.50 | 22.8 | 6.00 / 186 | 15.8 |
| [`coil_3x8_20`](pages/coil_3x8_20.html) | 194 | 6014 | 8 x 20 x 3 | 480 | 39 | U | 3510 | 9.75 | 19.9 | 1.95 / 60 | 18.1 |
| [`coil_3x9_18`](pages/coil_3x9_18.html) | 194 | 6014 | 3 x 18 x 9 | 486 | 35 | U | 3240 | 9.00 | 21.6 | 1.89 / 59 | 16.7 |
| [`coil_4x7_20`](pages/coil_4x7_20.html) | 194 | 6014 | 4 x 20 x 7 | 560 | 39 | U | 3510 | 9.75 | 19.9 | 1.95 / 60 | 18.1 |
| [`coil_4x8_18`](pages/coil_4x8_18.html) | 194 | 6014 | 4 x 18 x 8 | 576 | 35 | U | 3240 | 9.00 | 21.6 | 1.89 / 59 | 16.7 |
| [`coil_2x2_146`](pages/coil_2x2_146.html) | 194 | 6014 | 2 x 2 x 146 | 584 | 48 | N | 4230 | 11.75 | 16.5 | 12.34 / 383 | 21.8 |
| [`coil_4x9_17`](pages/coil_4x9_17.html) | 194 | 6014 | 9 x 17 x 4 | 612 | 33 | U | 2880 | 8.00 | 24.3 | 2.00 / 62 | 14.8 |
| [`coil_5x7_18`](pages/coil_5x7_18.html) | 193 | 5983 | 5 x 18 x 7 | 630 | 35 | U | 3150 | 8.75 | 22.1 | 1.94 / 60 | 16.3 |
| [`coil_5x8_17`](pages/coil_5x8_17.html) | 194 | 6014 | 17 x 5 x 8 | 680 | 32 | E | 2880 | 8.00 | 24.3 | 2.00 / 62 | 14.8 |
| [`staircase_coil`](pages/staircase_coil.html) | 196 | 6076 | 4 x 4 x 52 | 832 | 48 | N | 4230 | 11.75 | 16.7 | 4.34 / 135 | 21.6 |
| [`coil_3x4_73`](pages/coil_3x4_73.html) | 193 | 5983 | 4 x 73 x 3 | 876 | 49 | U | 4320 | 12.00 | 16.1 | 6.00 / 186 | 22.4 |
| [`coil_3x4_73_2`](pages/coil_3x4_73_2.html) | 193 | 5983 | 73 x 4 x 3 | 876 | 49 | E | 4320 | 12.00 | 16.1 | 6.00 / 186 | 22.4 |
| [`coil_3x4_74`](pages/coil_3x4_74.html) | 194 | 6014 | 3 x 4 x 74 | 888 | 48 | N | 4230 | 11.75 | 16.5 | 6.21 / 193 | 21.8 |
| [`coil_3x4_78`](pages/coil_3x4_78.html) | 194 | 6014 | 3 x 78 x 4 | 936 | 45 | U | 4140 | 11.50 | 16.9 | 6.70 / 208 | 21.3 |

Envelope and box are in blocks; a block is 31mm of centreline. Sorted by box, smallest
first. Every page is a viewer — drag to turn, scroll to zoom, colour by direction or by
section, and drag the slider to follow the bore from the mouthpiece a block at a time.

## What wins what

There is no single tightest, because "tight" splits in two and the two do not agree.

**Smallest package** is [`coil_3x3_47`](pages/coil_3x3_47.html) at
423 blocks of bounding box against 832 for the staircase coil —
1.97x smaller, in 37 pieces against 48. It wins on
both counts at once, which is the reason to care about it.

**Tightest spiral** is [`coil_3x9_18`](pages/coil_3x9_18.html), which comes back round
after only 1.89 blocks of rise — 59mm — against
4.34 blocks (135mm) for the staircase coil. That is a
2.3x steeper coil, but it does not have the smallest box: a steep coil
is fat, and pays for its pitch in cross-section.

**Least tube per turn** is [`coil_3x4_73`](pages/coil_3x4_73.html) at
16.1 blocks per revolution. The staircase coil is
16.7, so on this measure the walk that started it off was already within
4% of the best in the set — it is a genuinely economical
spiral, and what the search beat it on was packing, not turning.

**Fewest pieces** is [`coil_5x8_17`](pages/coil_5x8_17.html) at 32.

## How they were found

`tools/search_spirals.js` walks every periodic term sequence up to eight terms with legs
up to four blocks, and keeps those that: never reverse, come back to the same lateral
position each period so the thing is a coil rather than a drift, wind a whole number of
turns per period, stay self-avoiding when repeated, and satisfy the elbow-free rule.

That rule, for a window of three consecutive terms — outer A, middle m, outer C:

| A and C | | middle term |
| --- | --- | ---: |
| same axis, same direction | a step | >= 1 |
| same axis, opposite direction | a hairpin | >= 2 |
| different axes | a coil | >= 3 |

The bore-designs README states only the third case and calls the other two "a fold ...
as tight as you like". That holds for steps and not for hairpins: `U3 N1 D3` costs two
elbows and `U3 N2 D3` costs none. The three cases above were read off `bore_split.py`
by probing it, not derived.

Search output is a period. `tools/mknotation.js` repeats it to length and writes it in
the bore notation, trimming the tail so the last block is not mid-turn — a turn in the
last block has nothing after it to make it interior, so it is always its own piece.
Then every candidate goes through `bore_split.py` and only the ones that come back with
zero elbows are kept. **The splitter decides, not the rule.**

## Regenerating

    node tools/table.js          # the metrics table, as printed above
    node tools/table.js --md     # the same, as markdown

    # measure one walk
    node tools/spiral_metrics.js "$(cat walks/coil_3x3_47.txt)"

    # rebuild a viewer page
    cd ../bore-generator
    python3 viewer.py "$(cat ../spirals/walks/coil_3x3_47.txt)" \
        --out ../spirals/pages/coil_3x3_47.html --title "Coil 3x3 47"

## What has not been done

These are walks and viewers, not designs. **No cut files, and the full gate has not
run**: `check.py` needs shapely, which is not installed here, so every walk in this
repository has been through `bore_split.py` only. That covers the split, the piece
kinds and the bed, and it does not cover the parts, the seams or the assembled bore.
Nothing here should be cut without running `check.py` first.

The block counts are not all equal either — they run 193 to 196, so the bore
lengths run 5983mm to 6076mm. A coil is repeated to about the right length and
then trimmed to wherever the tail comes out elbow-free, so these are the same bore only
to within a few blocks. For a comparison of packing that is fine; for a comparison of
*bores* it is not, and the length would have to be fixed first.

Released under [CC0 1.0](LICENSE).
