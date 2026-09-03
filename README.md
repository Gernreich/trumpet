# bore-ribbon

A bore of **constant cross-section** swept along a **planar curve** — cut flat,
assembled with finger joints, no bending and no lamination.

    python3 ribbon_bore.py

<!-- readme-only -->
**[Read the writeup](https://gernreich.github.io/bore-ribbon/)** — the same
text as this page, set for reading, with a table of contents.

**[Download everything as a ZIP](https://github.com/Gernreich/bore-ribbon/archive/refs/heads/main.zip)**
— GitHub builds it from `main` on every push, so it is never out of date.

Built for **[LaserMadeMusic](https://www.youtube.com/@LaserMadeMusic)**, where
the cutting and the playing are shown.

**[The rest of the build files](https://gernreich.github.io/)** — every
instrument, generator and tool, indexed.

## See it before you cut it

Three pages, self-contained, **drag to turn**. Colour by face to read the
construction, or by facet to follow the bore along its length; the reveal
slider builds it up a facet at a time.

| | |
| --- | --- |
| [`ribbon-coupon-bore10-30deg-R30.html`](ribbon-coupon-bore10-30deg-R30.html) | the 180° coupon |
| [`ribbon-serpentine-bore10-30deg-3lobes-R72.html`](ribbon-serpentine-bore10-30deg-3lobes-R72.html) | the metre serpentine, 10mm bore |
| [`ribbon-serpentine-bore25-30deg-3lobes-R72.html`](ribbon-serpentine-bore25-30deg-3lobes-R72.html) | the metre serpentine, 25mm bore |

Built by [`ribbon_view.py`](ribbon_view.py), which takes the same flags as the
generator. **It draws the airway, not the plywood** — the passage the air takes,
bounded by the wall faces. That is the point: the section this repository is
about is a property of the airway, and the bore was cut 3mm narrow for a week
because nothing drew the space inside it.

The cut files themselves are hairlines on no background, which is close to
invisible on a page, so `previews/` holds a readable rendering of each — same
geometry and same cut order, thicker strokes, inks darkened to stay legible on
a light ground.

<p align="center"><img src="previews/ribbon-serpentine-bore10-30deg-3lobes-R72-1000mm-cheek-x2-cut-files.svg" alt="One cheek of the 10mm serpentine: a thin band following three half-circles joined by straight runs, with 145 slots along it" width="760"></p>

<p align="center"><img src="previews/ribbon-coupon-bore10-30deg-R30-180turn-panels-cut-files.svg" alt="The coupon sheet: two U-shaped cheeks and sixteen small wall panels, each a rectangle with a tab top and bottom" width="760"></p>

## How this differs from the other two

| | curve | section | joints |
| --- | --- | --- | --- |
| [`bore-generator`](https://github.com/Gernreich/bore-generator) | 90° lattice turns | +41.4% at each turn | finger joints |
| [`torus-octagonal`](https://github.com/Gernreich/torus-octagonal) | a circle, 45° facets | +8.2% at each facet | finger joints |
| **`bore-ribbon`** | **any planar curve** | **+3.5% at 30°, and the dial goes lower** | **finger joints** |

## Why a planar curve

Sweep a rectangle along a curve that lies in a plane, with one axis normal to
that plane, and the duct has **two flat faces and two cylindrical ones**. The
flat pair are the cheeks and come straight off the sheet. The curved pair are
the whole problem: 3mm birch will not bend to these radii, so they are
faceted — short flat panels, each finger-jointed into both cheeks.

The section is exactly `bore × bore` along every facet. At each facet joint the
walls mitre and the area there is `bore² / cos(φ/2)`:

| facet angle | area at the joint | |
| --- | ---: | --- |
| 90° | +41.4% | a turn in the Minecraft lattice |
| 45° | +8.2% | the octagonal torus |
| **30°** | **+3.5%** | **this coupon** |
| 15° | +0.9% | |

That is the whole design dial. It trades against part count, and against how
short the inner panels get.

## What limits the bend

A wall is `thickness` thick and its slot is centred on the offset line, so the
line the walls are offset to is **`(bore + thickness)/2`, not `bore/2`** — put
them at `bore/2` and each wall intrudes half its thickness, leaving an airway
of `bore − thickness`. That is exactly what this generator did until
2026-09-03: a bore asked to be 10 × 10 came out **7 × 10**.

The inner wall's radius is `R − (bore + thickness)/2`, so there is no bore at
all below that. Long before it, the inner panel gets too short to carry a
finger: a Boxes.py tooth is `2 × thickness` and **does not scale with the
bore**. At the 10mm bore and 30° facets:

| R / bore | R | inner panel | holds a 6mm tooth? |
| ---: | ---: | ---: | --- |
| 2.0 | 20mm | 6.87mm | no |
| 2.5 | 25mm | 9.46mm | no |
| 2.61 | 26.1mm | 10.03mm | just |
| **3.0** | **30mm** | **12.05mm** | **yes, with 3.02mm shoulders** |
| 4.0 | 40mm | 17.22mm | yes |

The coupon is R 30 for that reason, not because the bend wants to be that
open. A real Bb trumpet runs R/bore ≈ 4.3.

## The 1000mm serpentine

    python3 ribbon_bore.py --shape=serpentine              # the 10mm bore
    python3 ribbon_bore.py --shape=serpentine --bore=25    # the 25mm bore

**1000.0mm of centreline**, in **52 parts on 2 files** — three half-circles of
R 71.754 joined by 90mm straight runs, with a 20mm lead at each end.

The same centreline is cut at both bores. Only the band around it changes:

| | 10 × 10mm | 25 × 25mm |
| --- | --- | --- |
| the cheek, **cut twice** | [`bore10`](ribbon-serpentine-bore10-30deg-3lobes-R72-1000mm-cheek-x2-cut-files.svg) | [`bore25`](ribbon-serpentine-bore25-30deg-3lobes-R72-1000mm-cheek-x2-cut-files.svg) |
| the panels, cut once | [`bore10`](ribbon-serpentine-bore10-30deg-3lobes-R72-1000mm-panels-cut-files.svg) | [`bore25`](ribbon-serpentine-bore25-30deg-3lobes-R72-1000mm-panels-cut-files.svg) |
| section | 100mm² | 625mm² |
| cheek band | 20mm | 35mm |
| R / bore | 7.2 | 2.9 |
| play, per side | 0.025mm | **0** |
| shortest panel | 19.14mm | 18.16mm |
| slots per cheek | 145 | 137 |

**The play is not a constant, it is a lookup.** `PLAY_BY_BORE` carries
bore-generator's measured figures — 0.025mm per side at the 10mm bore and **0
at the 25mm** — because required clearance *falls* as the joint grows. A bore
that is not in the table gets the small-joint value and the generator says so,
because too loose is a worse joint and too tight is no joint at all.

The 25mm bore has *fewer* slots than the 10mm one on the same curve. The mitre
trims each inner panel by `((bore + thickness)/2) × tan(φ/2)` at both ends —
3.75mm at 25mm against 1.74mm at 10mm — so the panels are shorter and fit
fewer teeth.

### Why three half-circles and not two

A half-circle advances only **2/π of its own length** in x. So a 1000mm
serpentine wants **637mm of width** no matter how many lobes it is cut into,
and the bed is 600mm. Dividing it finer barely helps — it only claws back the
lead-in:

| lobes | R | cheek | fits |
| ---: | ---: | --- | --- |
| 2 | 118mm | 634 × 274mm | no |
| 4 | 65mm | 620 × 161mm | no |
| 6 | 43mm | 600 × 119mm | no, by 0mm |
| 8 | 32mm | 581 × 96mm | barely |

What actually fixes it is the **straight vertical runs between the lobes**.
They buy length in y, where there is room, instead of in x, where there is not.
At three lobes and a 90mm rise the cheek is **531 × 251mm** with 57mm of spare
in the worse direction, and the panels stay long enough to carry real joints.

### Long panels get more than one tooth

A 90mm straight run held by a single 6mm tab in its middle is a hinge, not a
joint: it pivots and the seam opens. Teeth alternate with gaps of their own
width, as Boxes.py does —

    n = floor((L − 2 × shoulder + tooth) / (2 × tooth))

— which is 1 up to 17.9mm, 3 at 34mm and **7 at 90mm**. Every panel on the
coupon is short enough to want exactly one, so the coupon's cut geometry did
not move when this arrived.

## The coupon

Two files: **[the cheek](ribbon-coupon-bore10-30deg-R30-180turn-cheek-x2-cut-files.svg)**,
which you cut **twice**, and **[the panels](ribbon-coupon-bore10-30deg-R30-180turn-panels-cut-files.svg)**,
which you cut once — a 180° turn at the 10mm bore, 123.2mm of centreline,
**18 parts**.

| | |
| --- | --- |
| Material | 3mm Baltic birch ply |
| Kerf (`BURN`) | 0.1mm |
| Play | 0.025mm per side, out of the slot, never off the tab |
| Section | 10 × 10mm = 100mm², exact along every facet |
| Parts | 2 cheeks (`0`) · 8 inner panels (`1`–`8`) · 8 outer panels (`9`–`10`) |

**The cheek is a thin band, not a plate.** It stops `WEB` = 2mm outboard of
each slot, so the band is 20mm wide for a 10mm bore — the bore, its two 3mm
walls, and 2mm of ply either side. Less material, less weight, and the shape
tells you what it is. 1.5mm is the floor worth cutting in 3mm birch; below that
the strip beside a slot chars through.

Because there is no flange left to write on, **the panel numbers are engraved
in the channel** — which is the floor of the bore. That is 0.1mm of roughness
in a 10mm airway, and the alternative is sixteen near-identical panels with
nothing on the cheek to say which slot each goes in.

**The two cheeks are the same part — outline, slots and engraving all
identical — and both go on the same way up.**

Whether a flipped cheek would *fit* depends on the shape, and the generator
reports it rather than assuming: the coupon's U is congruent to its own mirror,
so one cheek could be turned over and rotated 180° and every tab would still
land. **Do it anyway and its numbers read mirrored, facing into the bore.** The
serpentine is not congruent to its mirror at any angle, so there a flipped
cheek meets no tab at all.

Same way up, both of them, either way. The consequence is that one cheek
carries its numbers on the inside; that is the cheaper of the two mistakes.

**Because they are the same part, the cheek gets its own file and you cut that
file twice.** Nothing else is on it — the panels are a separate file, cut once.
That is the whole reason for the split: the packer used to fill the second
cheek's sheet with panels, so cutting one sheet twice left you thirteen panels
short and no way to notice but counting.

Panels are numbered in hex with the baseline tick, the same glyphs the bore
sections, the bell rings and the torus pieces use — `6` and `9` are one shape
turned over and the tick says which way up. Each cheek slot carries the number
of the panel that goes in it. Stand every panel with its number facing **out**;
the engraving is 0.1mm of roughness and it does not belong in the airway.

**Colour is the cut order**: blue `#0000ff` engraves, orange `#ff8000` cuts the
slots while the sheet still holds the cheek, black `#000000` frees the parts.

## What this coupon is for

Three things, none of which a check can answer:

1. **The butt gap.** Neighbouring wall panels do not join to each other — they
   butt, and the cheeks hold the alignment. At 30° facets with 3mm ply the gap
   on the convex side is `3 × tan(15°)` = **0.80mm**. That is a glue line, and
   whether it seals is the question.
2. **The tab fit at 0.025mm per side**, on a tooth that is 6mm in a panel that
   is only 10.26mm long.
3. **Whether 18 small parts is an assembly anyone wants to do twice.**

If 0.80mm is too much, the gap is `thickness × tan(φ/2)`, so it comes down with
the facet angle: **0.53mm at 20°, 0.40mm at 15°**. Halving it means 15°, not 20°
— and 15° costs a bend radius of R 45 at this bore, because the inner panels
shrink as the facets do and the tooth still does not scale.
