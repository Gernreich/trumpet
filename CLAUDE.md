# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The bore toolchain: a walk through a lattice of blocks goes in, per-piece laser
cut files come out, and every one of them is checked before you cut. Unlike its
sibling repositories this **is** a software project — it ships no cut files of
its own, only the thing that makes them.

It produces the bore in **`trumpet-coiled`**. Split out of
**`../../octomino-snakes`**, which enumerated the 369 octominoes and is archived and
private;
a live instrument should not depend on a frozen repository to rebuild its parts.

Read `README.md` first. It is 447 lines and carries the geometry — why an elbow's
opening frame has three sides, what a lap closes, how the notation splits into
pieces. This file covers only how to work on the code.

## Where things are

The scripts are flat at the repository root. That is deliberate: it puts them at
the same depth `octomino-snakes/generator/` had, so every relative path came
across unchanged.

    ../../test          the design library, outside every repository
    ../../GIT/trumpet-coiled/bore   the instrument this cuts for

`bore_split.py` writes to `../../test` when `--write` is given no path.

## The dependency graph

    svgpath      <- bore_split, check
    bore_split   <- bore_render, check, viewer, mcwalk, nest, hilbert, piece_render
    bore_render  <- viewer, mcwalk
    assemble     <- check
    snakebox     is a Boxes.py generator, driven by subprocess, not imported

`snakebox.py` is not standalone — it installs into a Boxes.py checkout, which
supplies the finger joints, burn compensation and SVG writer. `bore_split.py`
shells out to it. Point `SNAKEBOX_BOXES` at the checkout and `SNAKEBOX_PY` at
its venv python.

## The switches must reach the gate

`--ports`, `--flat` and `--fewest-pieces` are module globals. Run as a script this file
is `__main__`, and `check.py`'s `import bore_split` loads it a second time with its own
globals — so setting a switch on `__main__` set it for the writer and not for the gate.
`--ports --write` wrote ported cut files, gated the *unported* design, and reported
226 checks and 0 failed on parts nothing had looked at. The `__main__` block now
delegates to the imported module so there is one set of globals. If another switch is
added, set it on `B`, not on `globals()`.

**The bore's outer ends are plain.** `plain_ends()` always marks the first piece's entry
and the last piece's exit, not just the openings that meet a port. Nothing couples there —
the mouthpiece and the bell each glue a flat plate onto the end face, and a proud tab holds
it off. This renames end sections that used to share a shape with an inner one (`BDL` ->
`BDL~a`, `01_bend_DL.svg` -> `01_bend_DL_buttin.svg`) and **orphans the old file**, which
nothing deletes for you. `check_sheets` then globs the folder and gates the orphan too, at
three checks a sheet: the switchback reported 200 checks instead of 194 purely because two
stale files were still sitting there. **A check count that rises after a rename is a
warning.**

**The tab is floored at the finger tooth, and the notch carries the play.** Two bench
failures, both on 2026-08-31, both invisible to the gate. `--pin_width` scaled with the
block while the finger teeth did not (Boxes.py sizes those at `2 x thickness`), so at the
10mm bore the seam tab came out 4.8mm against 6mm teeth — the narrowest feature on the
sheet, where it should be the strongest. And `--pin_play` was 0, so the notch was drawn
exactly the tab's width and section 1 would not enter section 2. `pin_width()` now floors
at the tooth and caps at `MIN_SHOULDER`, and `PIN_PLAY` is 0.025 per side. Both are in
`COMMON`, so `check.py` sees the same geometry.

The gate did not catch either. Its floor is `MIN_FEATURE`, 1.5mm, which 4.8 clears
comfortably, and nothing compares a feature against the other features beside it or checks
that a joint has any clearance at all. **A passing gate means no check failed, not that the
part is buildable.**

`--blocksize` is the same hazard with a quieter failure. It is two numbers, not one:
`BLOCK`, the pitch the plan is laid out on, and `--blocksize` in `COMMON`, the pitch
SnakeBox cuts to. Both now come from `set_blocksize()`, and `COMMON` is built by `_common()`
from the constants rather than typed out — `check.py` and `piece_render.py` used to keep
their own copies of that list, which is a second place to forget. Use `bore_split.COMMON`.

A design folder may sit below its repository — the switchback's are `<size>/bore/` — so a
page title climbs past any ancestor that only names a size or says "bore" until it reaches
one that names the instrument. `trumpet-coiled/bore` still reads "Trumpet Coiled Bore"; the
switchback's reads "Trumpet Switchback 10mm Bore" rather than "10mm Bore".

`check.py --files` never looks at the pitch: it checks the written sheets for bed fit,
overlaps and engraving on material, all of which a 16mm folder passes at `--blocksize=31`.
The pitch decides the *geometry* half of the gate, which is recut in-process. Gate a folder
at the wrong blocksize and it reports 194 checks and 0 failed on a design nobody cut.

## One viewer, one bore or several

`viewer.build_many([(label, walk), ...], title)` is the only page builder. `build()` is it
with a single item, and a single item hides the selector, so a per-bore page is what it
always was. `sizes.py` passes two and writes one page holding a design at both the block
sizes it is cut at.

A gallery is **more sets in the same viewer**, not a second viewer: two templates would
drift, and the drawing code is the part that has been wrong before.

Anything derived from `D` has to be rebuilt when the set changes — `occAll` and `centre`
both are, and a stale `occAll` hides faces the new set has no neighbour for. The switch also
resets the camera, because a zoom kept from the 25mm strands the 10mm off-screen.

## Never regenerate what you cannot check

`regress.py` runs the full gate over every design in `walks/` and the design
library. It is the only reason any of this stays honest, it takes about four
minutes, and **it must pass before anything is pushed**:

```sh
python3 regress.py       # all 25 designs, ~8000 checks
```

A change that alters cut geometry and still passes has not been proved right —
it has been proved not obviously wrong. Say which it is.

## Standing decisions

**Fewest elbows at any cost** unless told otherwise. An elbow's opening frame has
three sides rather than four, so both neighbours need flattened plates butt-glued
to it, plus tongues, plus an unfilled void in the corner. Flat-to-flat gluing is
the difficulty of the whole build. `FEWEST_ELBOWS` is the switch and
`--fewest-pieces` turns it off.

**For a build, fewest is not the standard — none is.** `--refuse-elbows` raises
before a single file is written, naming the sections at fault, so a walk that
would cost one cannot be cut by accident:

    error: --refuse-elbows: section 2 of 3 is an elbow. Nothing written.

It is off by default because much of the library exists to exercise elbows —
17 of the 25 designs in `regress.py` contain them, the Hilbert curves 22 and 24 —
so turning it on globally would refuse the corpus. Use it on anything headed for
a build repository.

The other eight are there for the opposite reason: `hilbert open` (190 blocks,
27 pieces), `wide telescope`, `metre spring`, `4 corners, flat`, `three block
turn`, `hook check` and the trumpet candidate at both of its sizes all split
with **no** elbows, so a
change that started stranding turns would break them and leave the elbow-heavy
designs looking fine.

**What a turn costs is set by the window of three consecutive terms around it**,
outer A, middle m, outer C — checked over every window, not once per walk.
Consecutive terms are always on different axes, which leaves three cases:

| A and C | case | m must be |
| --- | --- | ---: |
| same axis, same direction | step | >= 1 |
| same axis, opposite direction | hairpin | >= 2 |
| different axes | coil | >= 3 |

This said, until 2026-08-29, that three different axes need a middle of 3 and
that anything else was "a fold, free at any spacing". Steps are indeed free;
hairpins are not. Probed with `--no-write`:

    N N3 U1 N3 N   step      0 elbows      N N3 U1 E3 E   coil   2 elbows
    N N3 U1 S3 S   hairpin   2 elbows      N N3 U2 E3 E   coil   1 elbow
    N N3 U2 S3 S   hairpin   0 elbows      N N3 U3 E3 E   coil   0 elbows

`bore_split.py` is the authority on this, not this file and not a
reimplementation of the rule.

**A walk that revisits a cell is refused.** The cells are the air path, so a cell
filled twice is a junction with two ways out and no box section has an opening in
four sides. **Trust the build and suspect the transcription**: the design is laid
out in Minecraft floating in open space, where a section running into an earlier
one is plainly visible, so a refusal usually means the walk was written down
wrong — and a wrong direction before a wrong length. `mcwalk.py` draws a refused
walk under permissive rules and lights up every cell entered more than once,
which the ordinary viewer cannot do.

## Colour is the cut order

Shared across these repositories: **blue engraves, then green → orange → cyan →
black**; black frees the part; **violet `#8000ff` means skip**. Bore nets use two
stages — blue engraves the section number, black cuts.

## Cut files belong to the author

Output lands in other people's repositories. `--write` rewrites **every** file in
the directory it is given, so ask before pointing it at one that has cut files in
it, and never at a directory holding hand-nested or hand-edited work.

## Publishing

Pages deploys from `main` through `.github/workflows/pages.yml`, keyed per commit.
`index.html` is `README.md` rendered by `md2html.py` and committed, not built on the
server, so a stale `index.html` publishes stale content — regenerate it after editing the
README, and read the audit before pushing:

```sh
G=../lasermade-tools
python3 $G/md2html.py README.md index.html
python3 $G/doc-audit.py README.md --html index.html
```
