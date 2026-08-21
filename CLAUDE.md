# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The bore toolchain: a walk through a lattice of blocks goes in, per-piece laser
cut files come out, and every one of them is checked before you cut. Unlike its
sibling repositories this **is** a software project — it ships no cut files of
its own, only the thing that makes them.

It produces the bore in **`trumpet-coiled`**. Split out of
**`../../octomino-snakes`**, which enumerated the 369 octominoes and is archived;
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

## Never regenerate what you cannot check

`regress.py` runs the full gate over every design in `walks/` and the design
library. It is the only reason any of this stays honest, it takes about four
minutes, and **it must pass before anything is pushed**:

```sh
python3 regress.py       # all 21 designs, ~6000 checks
```

A change that alters cut geometry and still passes has not been proved right —
it has been proved not obviously wrong. Say which it is.

## Standing decisions

**Fewest elbows at any cost** unless told otherwise. `FEWEST_ELBOWS` is the
switch and `--fewest-pieces` turns it off. An elbow's opening frame has three
sides rather than four, so both neighbours need flattened plates butt-glued to
it, plus tongues, plus an unfilled void in the corner. Flat-to-flat gluing is
the difficulty of the whole build.

**A turn is free in a plane and costs three blocks out of it.** Checked over
every window of three consecutive terms, not once per walk: if three consecutive
terms name three different axes, the middle one must be 3 or more; if they name
only two, the turn is a fold and costs nothing at any spacing.

**A walk that revisits a cell is refused.** The cells are the air path, so a cell
filled twice is a junction with two ways out and no box section has an opening in
four sides. Minecraft cannot catch this — filling an occupied cell there is a
no-op, so a bore that runs back through itself still builds into a connected
tunnel that looks right. `mcwalk.py` draws a walk under Minecraft's rules and
lights up every cell filled more than once; reach for it when a walk is refused
and the build looked fine.

## Colour is the cut order

Shared across these repositories: **blue engraves, then green → orange → cyan →
black**; black frees the part; **violet `#8000ff` means skip**. Bore nets use two
stages — blue engraves the section number, black cuts.

## Cut files belong to the author

Output lands in other people's repositories. `--write` rewrites **every** file in
the directory it is given, so ask before pointing it at one that has cut files in
it, and never at a directory holding hand-nested or hand-edited work.
