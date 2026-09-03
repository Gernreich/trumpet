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

The inner wall is the centreline offset inward by `bore/2`, so its radius is
`R − bore/2` and **there is no bore at all below `R = bore/2`**.

Long before that the inner panel gets too short to carry a finger. A Boxes.py
tooth is `2 × thickness` and **does not scale with the bore**, so at the 10mm
bore and 30° facets:

| R / bore | R | inner panel | holds a 6mm tooth? |
| ---: | ---: | ---: | --- |
| 1.0 | 10mm | 2.50mm | no |
| 1.5 | 15mm | 5.09mm | no |
| 2.0 | 20mm | 7.67mm | no |
| **2.5** | **25mm** | **10.26mm** | **yes, with 2.13mm shoulders** |
| 4.0 | 40mm | 18.03mm | yes, two teeth |

The coupon is R 25 for that reason, not because the bend wants to be that
open. A real Bb trumpet runs R/bore ≈ 4.3.

## The coupon

**[`ribbon-coupon-bore10-30deg-R25-180turn-cut-files.svg`](ribbon-coupon-bore10-30deg-R25-180turn-cut-files.svg)**
— a 180° turn at the 10mm bore, 107.6mm of centreline, **18 parts on a
297 × 99mm sheet**.

| | |
| --- | --- |
| Material | 3mm Baltic birch ply |
| Kerf (`BURN`) | 0.1mm |
| Play | 0.025mm per side, out of the slot, never off the tab |
| Section | 10 × 10mm = 100mm², exact along every facet |
| Parts | 2 cheeks (`0`) · 8 inner panels (`1`–`8`) · 8 outer panels (`9`–`10`) |

**Both cheeks are identical and both go on the same way up.** Flipping one over
mirrors its slot pattern, and this U is not symmetric about the line you would
flip it on, so a flipped cheek does not meet a single tab.

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
