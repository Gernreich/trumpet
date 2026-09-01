# bore-stretched

A bore whose **straight blocks are longer than its turns**. The cross-section
stays square the whole way — 10 x 10mm of air — but a block that runs straight
is 30mm long, while a block that turns is a 16mm cube. The same walk that gives
352mm of centreline on a uniform 16mm block gives **548mm** here, without
changing a single term of it.

    N N1 W3 U2 E3 N3 D3 W2 U3 N1

This is a **test**, not an instrument: it has no mouthpiece and no bell, and the
walk was borrowed from
[trumpet-final-youtube-candidate](https://github.com/Gernreich/trumpet-final-youtube-candidate)
rather than designed for a stretched lattice.

<!-- readme-only -->
**[Read the writeup](https://gernreich.github.io/bore-stretched/)** — the same
text as this page, set for reading, with a table of contents.

Built for **[LaserMadeMusic](https://www.youtube.com/@LaserMadeMusic)**, where
the cutting and the playing are shown.

**[The rest of the build files](https://gernreich.github.io/)** — every
instrument, generator and tool, indexed.

## Why a turn has to be a cube

A block is 16mm outside and 10mm of air, a 3mm wall each side. Along the way the
bore travels it can be any length, and here it is 30mm — but **only if it runs
straight**. A block where the bore turns has two openings on two different
faces, and both have to sit square in the same 16mm frame, so a turning block is
a 16mm cube. Stretch it and one opening would end up longer than the other.

That is the whole design. Eight of the 22 blocks turn, so:

| | |
| --- | ---: |
| straight blocks, 30mm each | 14 |
| turning blocks, 16mm cubes | 8 |
| centreline | 548mm |
| the same walk on a uniform 16mm block | 352mm |
| envelope | 92 x 92 x 152mm |

**1.56x, not 3x.** Stretching 30/16 is 1.875 per straight block, and the turns
do not stretch at all.

## The sections

Cut in order; each part is engraved with its section number. Sections 1 and 6
are flat where they face outward, so a mouthpiece or a bell can seat against
them.

| # | file | blocks | in | out | plate | shape | sheet |
|---|---|---|---|---|---|---|---|
| 1 | [`bore/01_bend_DL_buttin.svg`](bore/01_bend_DL_buttin.svg) | 1-3 | N | W | 49x49 | BDL~a | 325x70mm |
| 2 | [`bore/02_bend_LUUR.svg`](bore/02_bend_LUUR.svg) | 4-8 | W | E | 65x49 | BLUUR | 456x86mm |
| 3 | [`bore/03_bend_RD.svg`](bore/03_bend_RD.svg) | 9-11 | E | N | 49x49 | BRD | 337x70mm |
| 4 | [`bore/04_bend_DL.svg`](bore/04_bend_DL.svg) | 12-14 | N | D | 49x49 | BDL | 331x73mm |
| 5 | [`bore/05_bend_DLLU.svg`](bore/05_bend_DLLU.svg) | 15-19 | D | U | 65x49 | BDLLU | 482x73mm |
| 6 | [`bore/06_bend_RD_buttout.svg`](bore/06_bend_RD_buttout.svg) | 20-22 | U | N | 49x49 | BRD~b | 337x70mm |

[`bore/bore.html`](bore/bore.html) is the viewer: drag to turn, colour by
direction or by section.

## The joint between sections

Each section couples to the next with one tab entering one notch. The notch is
sized first and the tab follows:

| | |
| --- | ---: |
| notch | **6.3mm** wide, 3.2mm deep |
| tab | **6.2mm** wide, 3.0mm deep |
| clearance | 0.1mm across the width, 0.2mm at the bottom |
| shoulder | 1.85mm beside the notch, 1.90mm beside the tab |

**Both numbers come from the bench.** At zero clearance the sections would not
go together at all. At 0.3mm they went together with a perceptible rock. 0.1mm
is a snug slip fit that still leaves glue somewhere to sit.

**The notch is held at 6.3mm because part 1 is already cut**, and its notch is
the one part 2's tab enters. Tightening therefore had to come from the tab,
which is why the joint is sized with `--notch=6.3` rather than left to the
automatic width.

**The clearance is the point.** SnakeBox leaves `--pin_play` at 0 on the grounds
that finger joints carry none either, and that does not follow: a finger joint
is a dozen teeth sharing an edge, where the errors average out, and a section
seam is one tab in one notch drawn to exactly the same width. At zero the two
will not go together.

**The tab is a shade wider than the finger teeth**, which are 6mm —
`2 x thickness`, and they do not shrink with the block. Sized as a fraction of
the frame alone the tab comes out at 4.8mm, narrower than the ordinary teeth
beside it, which is backwards for the one feature carrying a whole seam; the
automatic width floors it at the tooth for that reason. Here it is 6.2mm, set
from the notch instead.

Going much wider is not free: at 6.2mm there is 1.9mm of material beside the
tab, and `check.py` refuses anything under 1.5mm.

Every seam runs SLOT to TAB, and the two outer ends carry neither.

## The toolchain is a fork, on purpose

`tools/` is a copy of
**[bore-generator](https://github.com/Gernreich/bore-generator)**, changed to
handle a lattice whose cells are not all the same length. That repository and
every repository it cuts for are **frozen**: they keep the scripts they were
gated against, and nothing here touches them.

Its generator installs into Boxes.py as **`SnakeBoxVar`**, beside the frozen
`SnakeBox` rather than over it, so both are available at once.

| file | what it does |
| --- | --- |
| `tools/bore_split.py` | turns a walk into pieces and drives the generator |
| `tools/snakeboxvar.py` | the Boxes.py generator that draws one flat piece |
| `tools/check.py` | the gate: every check that runs before anything is cut |
| `tools/assemble.py` | voxels the assembled bore, for the seal and volume checks |
| `tools/viewer.py` | writes the 3D page beside the cut files |
| `tools/bore_render.py` | the colours and direction names the viewer uses |
| `tools/svgpath.py` | reads and writes the path data |
| `tools/walks/stretched_test.txt` | the walk, and the only design here |

```sh
cd tools
python3 bore_split.py --bore=10 --straight=30 --notch=6.3 --refuse-elbows \
    "$(cat walks/stretched_test.txt)" --write ../bore
```

`--bore` is the airway, square, rather than the block outside. `--straight` is
how long a straight block runs; leave it out and every cell is a cube, which is
exactly what the frozen toolchain does. `--notch` sizes the coupling from the
female side, the tab following at `notch - 2 x play`; **it is not optional
here** — leave it out and the tab drops to 6.0mm, which is the loose fit the
bench rejected.

## What had to change, and what it cost

**The integer lattice had to go.** A block is long only along the axis it runs
straight on, so the same column index wants 30mm in one part of the bore and
16mm in another — there is no single number taking a lattice index to a
millimetre. Positions are carried in mm instead, each block butting its entry
face onto the last block's exit face. For a cubic cell that reproduces
`index x blocksize` exactly.

Three things moved with it:

- **The plate outline.** A run's length now sums the widths of the columns its
  boundary crosses, rather than multiplying steps by one pitch.
- **The voxel model** behind the seal and volume checks, which takes real boxes
  and decides face contact geometrically.
- **The bed-fit test**, which summed `blocksize x blocks` and so under-reported
  this design by 13mm a side.

**Not every walk will take it.** A straight and a turn sharing a column want two
widths at once, and the generator raises, naming the column, rather than drawing
it. This walk satisfies the constraint; how many others would is not something
that has been measured.
One-cell pieces are refused outright: every straight being one file, and four
rotations of a turn sharing one, both rest on the cell being a cube.

## What the gate checks

**194 checks, 0 failed.** The number worth trusting is not that, though — it is
that the voxelised bore comes to **55520 mm3** and the independent arithmetic for
14 straights, 8 turns and their corner voids also comes to **55520 mm3**, exact
against a 0.5% tolerance, with the passage coming back as one region and no leak.

## Colour is the cut order

**Blue engraves, then green -> orange -> cyan -> black**; black frees the part,
violet `#8000ff` means skip. These nets use two stages: `#0000ff` engraves the
section number, `#000000` cuts.

## Licence

CC0 1.0 Universal. See `LICENSE`.
