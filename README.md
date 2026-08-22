# Bore designs

Every bore that has been worked out, built out into cut files and a viewer page and kept.
This is the corpus **[bore-generator](https://github.com/Gernreich/bore-generator)**
regresses against: `regress.py` runs the full gate over these, which is the only reason any
of it stays honest.

**[Read the writeup](https://gernreich.github.io/bore-designs/)** — the same text as this
page, set for reading, with a table of contents.

**[The rest of the build files](https://gernreich.github.io/)** — every instrument,
generator and tool, indexed.

The SVGs regenerate byte-identical from the walk, so the walk and the generator are the
real source — but they are kept here so there is something to send to the machine without
running anything.

The nested sheets are not kept: they assume a full sheet of material, and
partly cut boards do not work that way. `nest.py` still produces them if a
whole sheet ever comes up.

```sh
cd ../generator
W="N N10 U2 W2 S7 U2 E4 N9 W2 D2 N4 N"

python3 bore_split.py --write ../test "$W"        # the eight sections
python3 nest.py "$W" --out ../test/nest.svg       # the same parts nested
python3 nest.py "$W" --deepnest ../test/dn.svg    # input for Deepnest/SVGnest
python3 bore_render.py "$W"                       # the 3D view
python3 check.py "$W" --files ../test             # 234 checks, cut nothing until it passes
```

## The trumpet bore

```
N N10 U2 W2 S7 U2 E4 N9 W2 D2 N4 N     45 blocks, 1395 mm of centreline
```

Read off a Minecraft model coloured by direction — yellow north, grey south,
blue east, red west, orange up, green down, each block coloured by the way you
travelled to reach it. 45 blocks matches the count recorded for the earlier
build in `trumpet-curved`.

Eight sections, numbered along the bore from the mouthpiece. Every part is
engraved with its section number and nothing else, about 1.7 mm tall — enough
to tell a loose part which section it belongs to, which is what gets lost on
the bench.

Part names and per-edge marks were tried and dropped: on parts this size they
were harder to read than they were worth.

`P1` and `P2` — the two face plates of a section — are mirror images rather
than spares, and on sections 1, 3, 4, 6 and 8 they genuinely differ, one having
a coupling the other does not. The plate whose seam edge has no notch or tab is
the one that faces the elbow.

44 flat parts, 3 mm stock, 25 mm square bore throughout, every sheet inside the
xTool P2S bed of 600 x 308 mm.

**Couplings kept, six sides flattened.** An elbow's opening frame has three
sides — the fourth is its other opening — so at every seam with an elbow, one
side of the neighbour's frame has no mate: a notch nothing fills, or a tab with
nowhere to go. That side is a face plate in every case, so one of that
section's two plates drops its coupling at that end and the other keeps it.

Six sides in all, on sections 1, 3, 4, 6 (both ends) and 8, marked `_flatin` /
`_flatout` in the file name. Every other coupling stays, so the tabs still hold
each seam square while the glue sets.

The one thing no check can settle is **which** of the two plates was flattened:
they are the same shape mirrored, and which ends up facing the elbow depends on
how Boxes lays the mirrored copy out. It is derived rather than measured. Dry
fit section 1 to section 2 before cutting the rest — if it is the wrong way
round you will find a tab with nowhere to go, and it is a one-word change.

Nested, the lot is two sheets. Sections 2 and 7 are the same shape but are cut
separately so each carries its own number.

Sections 2, 5 and 7 are one-cell elbows, which is where the bore changes plane.
Each leaves its 3 x 3 x 25 mm corner open on the inside of the bend — sealed
from outside by the surrounding walls and plates, so a notch in the bore rather
than a leak.

**No ports.** A port opens one face plate so a change of plane can happen inside
a piece, which would make this five sections rather than eight. It is not used:
the plate it opens leaves that cell's walls supported on one side, with their
fingers facing nothing, and it failed to assemble four times.
`bore_split.py --ports` still turns it on; what remains is suppressing the fingers on the
missing-plate side over the port cell.

`trumpet_bore.png` is the assembled bore from six angles, coloured by section.

## When a turn costs a section

A piece is cut as a flat snake and its opening sits on the rim, opposite the
neighbouring cell, so **a piece's two end blocks must be straight**. A block
that bends cannot be at the end of one. Every turn therefore has to sit inside
a piece, which means a straight block on each side, in the same plane, not
already claimed by the piece next door.

Everything about how a design splits follows from that.

**Folding is free.** Two turns in a row that use only two axes - north to up,
then up to north again - stay in one plane and share a piece, however tightly
they are packed:

    N N3 U1 N3 U1 N3 N     y and z only    1 section, 0 elbows
    N N3 U2 N3 U2 N3 N     y and z only    1 section, 0 elbows
    N N3 U3 N3 U3 N3 N     y and z only    1 section, 0 elbows

**Coiling costs three blocks a turn.** Two turns in a row that reach a third
axis - north to up, then up to east - leave the plane, so the piece breaks
between them and each turn needs a straight block of its own:

    N N3 U1 E3 U1 S3 S     all three axes  7 sections, 4 elbows
    N N3 U2 E3 U2 S3 S     all three axes  5 sections, 2 elbows
    N N3 U3 E3 U3 S3 S     all three axes  3 sections, 0 elbows

Three blocks apart is the threshold: two straights between the turns, one for
each. With one straight they fight over it and one turn is stranded on its own
as a single-block elbow. With none - adjacent turns - both are.

The turn that is not stranded becomes the corner of an **L**, and two Ls in
place of an elbow is both fewer files and fewer parts:

    N N4 U1 E4 E   straight, elbow, elbow, straight   2 elbows  10 blocks, 16 parts
    N N4 U2 E4 E   straight, elbow, L                 1 elbow   11 blocks, 14 parts
    N N4 U3 E4 E   L, L                               0 elbows  12 blocks, 12 parts
    N N4 U4 E4 E   L, L                               0 elbows  13 blocks, 12 parts

### Writing it

Mid-walk, two Ls meeting is three consecutive terms on three different axes
with **3 in the middle**:

    ... E4 U3 S4 ...        east, up, south
    ... W4 N3 E6 ...        west, north, east
    ... S9 E3 U5 ...        south, east, up

The outer numbers can be anything - 1, 4, 9, it makes no difference. Only the
middle one has to be 3, because that is the leg the two pieces divide between
them; the legs either side are already there and each supplies an arm for
free. On its own, from a standing start, the same figure is six blocks:

    E E1 U3 S1 S

    block  travels  turns        piece  role
      1      E                     1    arm
      2      U      E -> U         1    corner
      3      U                     1    arm
      4      U                     2    arm
      5      S      U -> S         2    corner
      6      S                     2    arm

The seam always falls inside the three-block leg, one block to the piece behind
and two to the piece ahead.

Three is the number that is always safe rather than the number always needed,
and what decides it is whether the three terms name three different axes.

    ... W9 N2 U9 ...    x, z, y - all different    1 elbow, in every context
    ... W9 N3 U9 ...                               0 elbows, two 11-block Ls
    ... U5 W4 N2 E6 ...  two turns only            0 elbows, the search has slack

`W9 N2 U9` is the unlucky shape: both turns leave the plane, so they need an arm
each, and the two-block leg has one straight block to give. One turn takes it,
the other is left bare. The nine-block legs either side do not help - the
problem is between the turns, not outside them - and no context rescued it:
alone, mid-walk, with a turn before, with a turn after, always one elbow. `N3`
makes it two 11-block Ls for 31 mm more bore.

So: **if three consecutive terms name three different axes, the middle one must
be 3.** If two of them share an axis it is a fold, and can be as tight as you
like.

Apply that to **every** window of three terms, not the one you happen to be
looking at. A fragment can be blameless and still cost elbows through the
windows it forms with its neighbours:

    W W1 N2 E1 E           on its own, one 5-block bend, no elbows
    U U4 W1 N2 E1 U4 U     the same fragment in a walk, 7 sections, 4 elbows

        U4 W1 N2   three axes  middle=1  costs an elbow
        W1 N2 E1   a fold      middle=2  fine
        N2 E1 U4   three axes  middle=1  costs an elbow

    U U4 W3 N2 E3 U4 U     the two ones widened, 3 sections, no elbows

W1 N2 E1 is a fold and free in itself - W and E are both the x axis. What costs
is the W1 and the E1 each being the middle of their own window, where the terms
either side reach a third axis.

An L needs a straight block running out to each of its two ends - that is what
gives the piece the flat end faces its neighbours couple to - so two turns can
never share one straight between them. Whichever piece claims it, the other
ends on a bending block, and a bending block cannot open on the rim. Adjacent
turns therefore have no arrangement of Ls at all; that is geometry, not the
splitter being careful.

Note that this is the opposite trade from re-splitting a walk that is already
written. Adding a block to move two turns apart buys an L and pays for itself;
re-splitting the same blocks to avoid an elbow costs about two parts. The first
changes the walk, the second only changes where the seams fall.

It is not about which axes a single turn uses. One turn defines a plane by
itself and is always fine. It is about whether the turn after it stays in that
plane.

The splitter is set to take **the fewest single-block elbows**, and the fewest
pieces only after that. `--fewest-pieces` swaps the two.

In parts alone that is the wrong way round: measured over 133 walks it trades
23 elbows for 46 more parts and never fewer, because folding a turn into a bend
adds two walls to that bend while a lone elbow is four parts for its whole
block. It costs no extra pieces - over those same walks the count did not move
at all - but it is not free.

It is still the right setting, because the part count is not what an elbow
costs. An elbow's opening frame has three sides rather than four, and that
missing side propagates into the pieces either side of it:

    design             elbows   flats  tongues  voids  parts
    first trumpet          3       6        0      3     44
    spiral trumpet         3       5        1      2     68
    telescope spiral      11      18        2      9    106
    hilbert snorkel       24      26       20      4    260
    wide telescope         0       0        0      0     72
    metre spring           0       0        0      0     36

A **flat** is a plate whose coupling was dropped because it faced an elbow's
missing side: no tab, no notch, nothing to locate against. Two smooth faces
held square by eye while the glue grabs. A **tongue** is a wall run 3 mm past
the joint to fill the inside of a bend, glued the same way and having to clear
the elbow's face as it goes. A **void** is the corner nobody could fill.

None of those appear in the part count, and all of them track the elbow count
exactly. A design with no elbows has none of them: every seam is a full
four-sided coupling that locates itself, and the glue only has to hold what the
tabs have already squared up. Two more plywood parts against a butt joint held
square in mid-air is not a close trade.

Two other ways a turn becomes an elbow:

* **A turn in the last block of the bore.** There is nothing after it to make
  it interior, so it is always its own piece. Ending `N5 U` rather than `N5 U1`
  costs a file for that reason.
* **A bed split** landing on a turn, if the piece would otherwise be too big.

Which is why the designs here come out so differently. The switchback ramp
folds back and forth in one plane: 91 blocks, 17 sections, no elbows at all.
The Metre Spring coils, so every quarter leaves its plane - it gets away with
no elbows only because rising 3 gives each turn its own straight. The Hilbert
cube at scale 1 changes plane at nearly every turn with no room between, and
comes out as 56 elbows in 63 sections.

## How big a piece can be

A flat piece is one sheet, so the bed sets the limit: **at most 19 blocks one
way by 9 the other**, measured on the piece's bounding box in its own plane,
not on its block count. An L of 19 by 9 is 27 blocks and fits; a square of 10
by 10 is 19 blocks and does not.

    19 x 31 mm + tab + burn = 592 mm  against the 600 mm bed
     9 x 31 mm + tab + burn = 282 mm  against the 308 mm

`bore_split.py --no-write` prints the plate size of every piece and flags any
that will not fit, so a design can be checked before anything is drawn. The
size is read off the walk, exact on the long axis and 3 mm pessimistic on the
short one - it never says a piece fits when it does not.

A run longer than that is not an error: the splitter puts a turn's worth of it
in the next piece, or spills the parts onto a second sheet, which is why
section 6 is two files. The machine itself takes stock up to 3 m through the
pass-through, but nothing here knows how to use it.

## What a walk is checked for

Four layers, and the first three are automatic:

1. **Reading it.** A reversal, a block asked to bend twice, and a walk that
   runs into itself are refused outright, naming the blocks: "block 9 runs into
   block 1". Every entry point reports it the same way.
2. **Splitting it.** Whether each piece is one flat snake, whether an end block
   that bends can open on the rim, and whether the piece fits the bed. A piece
   too big is not an error - the search simply will not use it.
3. **Warnings that are not errors.** Blocks that touch without being joined
   along the bore, single elbows meeting directly, and inside corners left
   unfilled. All legal, all worth a look.
4. **The gate**, `check.py`: the parts, the sections, the seams and a voxel
   model of the assembled bore. `--write` runs it on what it just wrote, so a
   design folder having been made means it has been checked.

`regress.py` runs the gate over every design in the repository, which is the
only way any of this stays honest.

### Why Minecraft will not catch a crossing

Building the walk in Minecraft first is a good habit and it cannot check it. Nothing
there requires a tunnel to be a single unbranching path, so nothing there can object
when it stops being one — it has no notion of a bore, and so no notion of a bore
being wrong.

`N N3 U3 W5 N10 E5 S8 W3 S3 N12 N` is the example. Walked permissively it places
fifty-three blocks into forty-eight cells: five land where a block already is, and the
`S3 N12` at the end is a 180 that retraces its own last three blocks.

**How a walk like that actually arises is transcription, not building.** That one came
from typing `S3` where the build turned `D3`, and every attempt to fix it by changing
the *lengths* failed, because the fault was a direction. Read the walk back off the
page rather than off your memory of the build.

The reason it is fatal here and harmless there is what the cells are for. In
Minecraft they are scenery. In a bore they are the air path, and a cell filled
twice is a junction - the air arrives with two ways out. There is no box section
with an opening in four sides, so the crossing cannot be cut at all.

`mcwalk.py` draws a walk under Minecraft's rules instead of the bore's, and
lights up every cell that got filled more than once:

    python3 mcwalk.py "N N3 U3 W5 N10 E5 S8 W3 S3 N12 N" \
        --out ../test/doubled_walk/doubled_walk.html --title "..."

Use it when a walk is refused and the build looked fine. The step slider is the
tell: scrub it and watch *placed* keep climbing while *cells filled* stalls.

## Before cutting

`check.py` runs every check there is — 234 of them on this bore, across the
parts, the sections, and the seams between them. Each exists because something
was cut and thrown away:

| check | what it caught |
|---|---|
| part is one closed piece | a plate all but severed by a port hole |
| no feature under 1.5 mm | 0.5 mm and 0.1 mm slivers on three plates |
| the two plates are one part mirrored | a plate drawn a cell short, its fingers 2 mm out of phase |
| no wall finger left unengaged | section 5's closed-end wall, hanging off one plate |
| both sides agree on bore and tab size | an elbow tab sitting 1.5 mm off the centreline |
| seam has no port | the joint that failed four times |
| sheet fits the bed | a nested sheet 2 mm over |
| no two parts overlap | 12 pairs cut through each other by a nesting bug |
| engraving on material | labels placed in the notch of an L-shaped plate |
| the section closes round its bore | a port, or any face left open |
| the joint is closed | an end frame not backed by material |
| the bore carries on through the joint | two sections not meeting |
| the assembled bore is one sealed passage | anything the above miss, end to end |
| bore volume matches the walk | the assembly not being the bore you asked for |
| part count, part fits the bed, seam gender | — |

Run it with ports turned on and 13 checks fail, naming the three sections and
their seams — so it is known to fail when it should.

It does fold each section up in 3D. `assemble.py` builds the section as a
solid - plates over both faces, walls the full depth of the tube along every
boundary run that is not an opening - plugs the openings it is meant to have,
floods the outside, and asks whether the flood reaches the bore. The model is
checked against arithmetic on the way past: a two-cell straight comes out at
25 x 25 x 62 = 38,750 mm3 of bore, to the voxel.

The seams get the same treatment. Two sections are put where the bore actually
puts them with only their outer ends stopped up: if the joint leaves any of the
end frame unbacked the flood gets in, and if the two bores do not meet the bore
comes back as more than one region. Then all eight go in at once, and the volume
that comes out is compared with what the walk says it should be — 874,936 mm3
against 45 blocks x 25 x 25 x 31 = 871,875, the difference being the voxel size.

These are the checks that test the thing you are actually trying to do rather
than a proxy for it. On the port version the section check reports the whole
bore of sections 2, 4 and 5 open to the outside; break a seam deliberately and
the joint check reports the bore in two pieces.

## Turning one around

Every design folder carries a page you can turn around with the mouse, named
for the folder - `first_trumpet/first_trumpet.html`,
`spiral_trumpet/spiral_trumpet.html`, and `test_bore.html` for the nine-block
walk that has no cut files. Open one in a browser; nothing is installed and
nothing is fetched but the fonts. Drag to turn, scroll to zoom, right-drag to
pan, colour by direction or by section, click a legend row to isolate it, and
drag the slider to follow the bore from the mouthpiece a block at a time.

**Blocks** opens a list of every block from the mouth: its number, its colour,
which way the bore goes through it, and its position relative to block one,
with the turns ruled off. That is the list to build from - place block one
anywhere and follow the offsets - and every line is checkable against F3.

The direction colours are the ones the bore gets built in first:

    up     red        down   grey
    north  blue       south  orange
    east   green      west   purple

Down is grey rather than a sixth hue because grey is a block you can actually
get, and because it cannot be mistaken for south's orange once the faces are
shaded - which yellow can. Change them in `DIRCOL` at the top of
`bore_render.py`; `viewer.py` takes them from there, so one edit moves both the
pages and the still renders.

The walks with no cut files sit loose in `test/`:

    test_bore.html          9 blocks    the walk the splitter was shaken out on
    helix_rise2.html       29 blocks    square helix, rising two a corner
    helix_rise1.html       25 blocks    rising one, so elbows meet back to back
    helix_side6.html       47 blocks    six-block sides
    stepped_coil.html      40 blocks    six loops marching diagonally, 26 sections
    switchback_ramp.html   91 blocks    eight hairpins climbing, 17 sections, no elbows

The last two are worth reading together. The stepped coil is `U1 W1 S2 E2` six
times over and costs 116 parts for 40 blocks; the switchback ramp is the same
idea with every leg widened, `U2 W3 S3 E3`, and costs 132 parts for 91. Same
family, less than half the parts per block, because a leg of one block forces
a standalone elbow and a leg of three does not.

It goes the other way too. Every tool takes a walk, a file with one in, or one
of these pages - the walk sits in the page's title rail, so a page you kept is
enough to cut from and nothing else has to be filed:

    python3 bore_split.py --write out ../test/telescope_spiral/telescope_spiral.html
    python3 check.py ../test/tightest_coil.html
    python3 viewer.py walks/small_hook.txt --out again.html

`bore_split.py --write DIR` writes the page along with the cut files, so the
two cannot drift apart. For a walk you are only looking at:

    python3 viewer.py "<walk>" --out ../test/<name>.html --title "<Name> Bore"

## The pictures

<p>
<img src="notation_explained.png" alt="A diagram of the walk notation: the entry letter, then each term as a direction and a distance in blocks" width="620">
</p>

*The notation, laid out.*

<p>
<img src="first_trumpet/trumpet_bore.png" alt="The first trumpet bore assembled, shown from six angles and coloured by section" width="620">
</p>

*The first trumpet, six angles, coloured by section.*

Three more pictures were named here and are not in the repository —
`bore_UU2E2S2U2U.png` of the test bore, `bore_tunnel.png` of the notation, and
`DR1F_assembly_guide.png` from the early `D R1 F` exercise. They were lost before this
directory became a repository; the references are removed rather than left pointing at
nothing.

Released under [CC0 1.0](LICENSE).
