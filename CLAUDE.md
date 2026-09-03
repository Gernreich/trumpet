# CLAUDE.md

## Working in this repository

A laser-cutting build repository. `ribbon_bore.py` is the generator and the
authority; the SVG beside it is its output and is regenerated, not edited.
Everything is 3mm birch on an xTool P2S.

This is the **third** way these repositories cut a bore, and the three are not
variations on each other:

| | curve | section at a turn | why it exists |
| --- | --- | --- | --- |
| `bore-generator` | 90° lattice turns | +41.4% | fits a walk into a box |
| `torus-octagonal` | a circle, 45° facets | +8.2% | a closed constant-section loop |
| here | any planar curve | +3.5% at 30° | constant section on a smooth curve |

## The geometry, in one paragraph

Sweep a rectangle along a curve **in a plane**, with one axis normal to that
plane, and the duct has two flat faces and two cylindrical ones. Flat cuts from
the sheet; cylindrical does not, because 3mm birch will not bend to these
radii. So the curved pair are faceted, and the facet angle is the only dial:
the section is exactly `bore × bore` along a facet and `bore² / cos(φ/2)` at
each mitre.

**The centreline polyline IS the facet plan.** There is no separate faceting
step, so there is nothing for it to disagree with. `walls()` offsets it and
asserts which side came out inner, because the sign depends on which way round
the centreline was written and getting it backwards silently swaps every panel
length in the cut list.

## What limits a bend, and it is not what you would guess

The inner wall is the centreline offset inward by `bore/2`, so there is no bore
at all below `R = bore/2`. **But the tooth runs out long before the geometry
does.** A Boxes.py tooth is `2 × thickness` and does *not* scale with the bore —
the same fact that forced `pin_width()` in `bore-generator` to floor at the
tooth. At the 10mm bore and 30° facets:

    R 15   inner panel 5.09mm   shorter than one tooth
    R 20   inner panel 7.67mm   still no room for shoulders
    R 25   inner panel 10.26mm  fits, 2.13mm shoulders

R 25 is why this coupon is R 25. Coarser facets need less radius, finer facets
need more: 20° wants R 35, 15° wants R 45. `build()` refuses rather than
drawing a panel that cannot hold its tab.

## A half-circle advances 2/pi of its own length

Which is the whole reason the serpentine has three lobes and long straight
runs. A 1000mm run of half-circles wants **637mm of width** whatever the lobe
count, and the bed is 600 — dividing it finer only claws back the lead-in and
shortens the panels until they cannot hold a tooth. The straight verticals are
what make it fit, because they buy length in y where there is room.

**Solve the radius against this generator's own faceted centreline**, never
against a smooth arc: an inscribed chord is **1.14% short** of the arc it
spans, so a radius picked from the arc comes out 11mm long over a metre.

## Long panels get more than one tooth

`teeth(L)` gives `floor((L - 2*SHOULDER + TOOTH) / (2*TOOTH))`, alternating
tooth and gap of equal width. One tab in a 90mm straight run is a hinge: it
pivots about the tab and the seam opens. Every coupon panel is short enough to
want exactly one, so the coupon's cut geometry did not move when this arrived —
checked by comparing the cut groups as position-independent shapes, which is
the only comparison that means anything once the packer may have reordered
them.

## One sheet per bedful

`pack()` row-wraps into `BED - 2 x margin`, not into the bed. Filling to the
edge produced a sheet **600 x 307 on a 600 x 308 bed** — passes a fits-the-bed
check and cannot be positioned on a real machine. A part bigger than the usable
area is a refusal, not a smaller sheet.

## Kerf goes opposite ways on a part and on a hole

The laser removes `BURN` centred on the line, so a part comes out `BURN` under
and a hole `BURN` over. Every panel dimension is therefore drawn `BURN` **over**
and every slot `BURN` **under**, plus `PLAY` per side taken out of the slot and
never off the tab — `bore-generator`'s standing rule, and its 0.025mm figure for
the 10mm bore.

Measured back out of the written file rather than asserted: a 6.100mm drawn tab
and a 5.950mm drawn slot give a 6.000mm tab in a 6.050mm slot, 0.025mm a side.

## Both cheeks are identical and both go on the same way up

Flipping one over mirrors its slot pattern, and a U is not symmetric about the
line you would flip it on, so a flipped cheek meets no tab at all. Two identical
parts, same orientation. The consequence is that one cheek carries its numbers
on the inside; that is the cheaper of the two mistakes.

## The cheek stops 2mm outboard of its slots

`WEB`, not `MARGIN`, is the number to change — `MARGIN` is derived from it.
The band is `bore + 2 × (thickness/2 + WEB)`: 17mm at the 10mm bore. Asked for
"as thin as possible" and 2mm is the answer that still cuts; 1.5mm is the floor
in 3mm birch.

The knock-on is that there is no flange left to engrave on, so the cheek's
panel numbers moved **into the channel**, which is the floor of the bore. Two
checks hold that: no engraved point off its own part, and none inside a slot.

## Look at the render. The checks do not see the drawing

Two defects in this generator got through every check and were caught by
screenshotting the SVG:

- **Every glyph was mirrored top to bottom.** The glyph table's y runs up and
  SVG's runs down. A `2` came out as something that is not a `2`, and no
  geometric invariant cares.
- **The cheek's own number was engraved in the hole in the middle of the arch.**
  The centre of a U's bounding box is air.

`checks()` now includes *every engraved point is on its own part*, which found
the second one immediately — 18 points off, exactly the two cheek labels. It is
there because the render found it first. **Screenshot the SVG after any change
to drawing code.**

A third, from the same family: *no engraving lands in a slot* was written
comparing ink in sheet coordinates against slots rebuilt at design
coordinates. Two spaces that cannot overlap, so it passed, and the tell was
that it said **16 slots on a sheet that has 32**. A count printed beside a
verdict is what makes that visible. Both now come out of `sheet()`, which is
the only place that knows where anything was actually put.

Then it failed the same way again once there were several sheets: it compared
ink on sheet 3 against slots on sheet 1. Two sheets are two files and their
coordinates have nothing to do with each other. Both are now tagged with their
sheet. **Twice in one file is a pattern, not bad luck: any check comparing two
sets of coordinates must first establish what space they are both in.**

Every check reports its own count (`40 stations`, `504 points`, `120 pairs`) so
a check that measured nothing cannot print the same clean line as one that
measured everything.

## `id="..."` contains `d="..."`

Measuring the output with `re.findall(r'd="([^"]+)"')` matches the `id`
attribute too and hands you `slots` where a coordinate should be. Use
`(?:^|\s)d="`. `torus-octagonal`'s writeup records the same trap; it still cost
a run here.

**A failing run deletes its output**, which is right — a sheet that failed a
check should not be sitting there looking cuttable. It also means a copy of
this script tried out in this folder writes to, and then deletes, the real cut
file. That happened. Use `--out` for trials.

## Colour is the cut order

Shared across all these repositories: **blue engraves, then green → orange →
cyan → black**; black frees the part; violet `#8000ff` means skip. This sheet
uses three — blue for the numbers, orange for the slots so the cheek is cut
while the sheet still holds it, black for the outlines.

## Cut files belong to the author

- **Stage by name.** Never `git add -A` or `git add .`.
- Do not regenerate a cut file the author has hand-edited without asking.
- Commit straight to `main`. Push only when asked.

## Commands

```sh
python3 ribbon_bore.py                 # cut file + the checks
python3 ribbon_bore.py --no-write      # the checks alone
python3 ribbon_bore.py --out=/tmp/x.svg   # a trial, somewhere it cannot hurt

G=~/LaserMadeMusic/GIT/lasermade-tools
python3 $G/md2html.py README.md index.html
python3 $G/doc-audit.py README.md --html index.html \
    --rebuild "python3 $G/md2html.py {md} {out}" --links
python3 $G/svg-stroke-check.py --dir . --quiet
```

**Read the audit output before pushing.** It ends with a pass/fail tally.
