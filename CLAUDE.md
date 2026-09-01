# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A **test bore**, and a fork of the toolchain that cuts it. Straight blocks are 30mm long,
turning blocks are 16mm cubes, and the airway is 10 x 10mm the whole way. 548mm of
centreline from a walk that gives 352mm on a uniform 16mm block.

Not an instrument: no mouthpiece, no bell, and the walk was borrowed from
`../trumpet-final-youtube-candidate` rather than designed for a stretched lattice.

## The other repositories are FROZEN

`../bore-generator` and every repository it cuts for — `../trumpet-coiled`,
`../trumpet-octagonal`, `../trumpet-parts`, `../trumpet-final-youtube-candidate` — keep the
scripts they were gated against. **Do not change them to suit this one.** That is why
`tools/` is a copy rather than an import, and why the generator installs as `SnakeBoxVar`
beside the frozen `SnakeBox` instead of over it.

Two things follow:

- **Fixes do not flow back on their own.** Two files here already differ beyond the stretch.
  `tools/bore_split.py` has a tightened page-title rule, because the frozen one climbs past
  `bore-stretched` to the parent directory and titles the page "Git Bore Stretched Bore".
  `tools/viewer.py` draws each block from its real box rather than as a unit cube, and hides
  a face only where a neighbour measurably covers the whole of it — the frozen one culls by
  lattice index, which no longer exists here. If a fix matters over there, it has to be
  asked for, not assumed.

  The viewer is worth calling out because **nothing gates it**. `check.py` never looks at
  the page, so a render can be wrong while 194 checks pass — which is exactly what happened:
  the geometry, the plates and the voxel model were all correct and the picture still showed
  a uniform 10mm lattice. Look at the render after changing the geometry.
- **Check the freeze after touching Boxes.py.** Installing anything into `~/boxes` can
  disturb the shared checkout. The test is that the frozen toolchain still reproduces a
  shipped file byte for byte:

```sh
cd ../bore-generator
W="$(cat walks/trumpet_final_youtube_candidate.txt)"
~/boxes/venv/bin/python bore_split.py --blocksize=16 --refuse-elbows "$W" --write /tmp/f
cmp /tmp/f/02_bend_LUUR.svg ../trumpet-final-youtube-candidate/10mm/bore/02_bend_LUUR.svg
```

## A turn is a cube because it has to be

A turning block has two openings on two different faces, both of which must sit square in
the same frame. Stretch it along one axis and one opening comes out longer than the other.
So `--straight` lengthens straight blocks only, and `extent()` is the single place that
decides: long along the axis a block runs straight on, the section everywhere else.

## The lattice is not a grid any more, and that is the whole cost

The same column index wants 30mm in one part of the bore and 16mm in another, so **no single
number takes a lattice index to a millimetre**. Positions are carried in mm by
`block_boxes()`, each block butting its entry face onto the last block's exit face. For a
cubic cell that reproduces `index x blocksize` exactly — there is a test for it, and it is
the first thing to re-run if geometry looks wrong.

Everything downstream of that had to stop counting cells:

- `SnakeBoxVar.span()` sums the widths of the columns a boundary run crosses, instead of
  steps times one pitch. `bore_split.piece_widths()` supplies them, **rebased on the piece's
  first cell**, because SnakeBox lays its own cells out from (0,0) following `--path`.
- `assemble.build()` takes real boxes and decides face contact geometrically, so a face a
  neighbour only partly covers is walled over the rest of itself.
- `plate_span_mm()` sums column widths for the bed-fit test. It used to be `blocksize x
  blocks`, which under-reported by 13mm a side here.

**The grid still has to hold within a piece.** `piece_widths()` raises, naming the column,
when a straight and a turn share one — a plate is drawn on a rectilinear grid even though
the bore as a whole is not on one. This walk happens to satisfy it; most will not.

## Do not trust a passing gate

194 checks and 0 failed is not the evidence. Two of those checks were vacuous on this
geometry until the voxel model was rewritten, and a passing gate means no check failed, not
that the part is buildable. The number that means something:

    voxelised bore volume   55520 mm3
    the same from the walk  55520 mm3     14 straights, 8 turns, corner voids

Two unrelated routes to one figure, exact against a 0.5% tolerance, with the passage coming
back as one region and no leak. If you change the geometry, re-derive that by hand and
compare — do not read the tally.

## Commands

```sh
cd tools
W="$(cat walks/stretched_test.txt)"
python3 bore_split.py --bore=10 --straight=30 --refuse-elbows "$W" --write ../bore
~/boxes/venv/bin/python check.py "$W" --bore=10 --straight=30 --files ../bore
```

**`--notch` exists but this design does not use it.** It sizes the coupling from the female
side, the tab following at `notch - 2 x play`, and it **overrides the finger-tooth floor** —
a 5mm notch gives a 4.7mm tab, back under the teeth, which is the state that was reported as
"not wide enough" before the floor existed. It was tried at 5mm on 2026-08-31 and reverted,
because **parts 1 and 2 had already been cut** at the default and the files have to match
the wood. If you change it, the cut parts stop matching the files: say so, do not just
regenerate.

`--bore` is the airway and `--blocksize` is the outside; they differ by two wall
thicknesses and confusing them is the mistake this switch exists to stop. `check.py` needs
**the same two switches** as the writer or it gates a design nobody cut — `--files` looks
only at the sheets as the machine sees them and never at the geometry.

`bore_split.py --write` calls the gate itself, but `check.py` imports **shapely**, which is
not in `/usr/bin/python3`. Run as a script it writes all six files and then dies on the
import, files written and ungated. Use the Boxes.py venv.

**There is no `regress.py` here.** The frozen corpus lives in `../bore-generator` and gates
the frozen toolchain; this fork has one design and gates it on write. If this grows a second
design, it needs its own corpus rather than borrowing that one.

**After editing `README.md`** — regenerate the page, then audit:

```sh
G=../lasermade-tools
python3 $G/md2html.py README.md index.html
python3 $G/doc-audit.py README.md --html index.html
python3 $G/svg-stroke-check.py --dir . --quiet
```

## Cut files belong to the author

The author edits SVGs in Inkscape during a session. **Stage by name** — never `git add -A`.
A changed section length renames a file and the generator does not delete what it stops
writing, so check `bore/` for orphans after a regenerate.

## Colour is the cut order

**Blue engraves, then green -> orange -> cyan -> black**; black frees the part, violet
`#8000ff` means skip.
