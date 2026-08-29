# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A laser-cutting build repository, not a software project. The deliverables are six **SVG
cut files** that someone sends to a laser, plus the page describing them. Everything here
is **generated** by the sibling repository **`../bore-generator`**; nothing in this
repository is authored by hand except `README.md` and this file.

It holds one design: the bore candidate for the build video. The bell and the mouthpiece
are not here — they are shared with the other trumpets and live in `../trumpet-parts`.

Sibling repositories — `trumpet-coiled`, `trumpet-octagonal`, `torus-octagonal`,
`knotwork-soundholes`, `living-hinge` and others — follow the same conventions. Shared
documentation tooling lives in **`../lasermade-tools`** (its own repository).

## The design is one line

The bore is a walk through a lattice of blocks, and the walk is the whole specification:

```
N N1 W3 U2 E3 N3 D3 W2 U3 N1
```

The first letter is the way in; each term after it turns where you stand and then travels
*n* blocks, so **the bore is 1 + the sum of the numbers** — 22 blocks here. Axes match
Minecraft: `U`/`D` are +Y/−Y, `N` is −Z, `S` is +Z, `E` is +X, `W` is −X.

**The walk is stored in `../bore-generator/walks/trumpet_final_youtube_candidate.txt`**,
and `regress.py` there names this repository as where its cut files live. Unlike
`../trumpet-coiled`, which keeps its walk in its page, the file is the record here — the
page carries the same string in its `<div class="walk">` and `bore_split.py` will read
either, but they are only equal because the page was generated from the file.

Never transcribe the walk from memory. Read it out of the file.

## No lead-out, and why that is not a change

A walk may end with a bare letter naming the way you leave. This one does not, and that
costs nothing: a term whose direction matches your heading does not turn, and a bare term
carries no distance, so after `N1` a trailing `N` would only restate a heading the walk
already has. Checked on 2026-08-29 by writing it both ways — **the six SVGs came back
byte-identical**. It would matter if the exit direction differed from the last term: `N1 U`
turns the final block and buys an elbow.

## One block is 31mm, not 25

A block is 25 × 25 × 25mm of sound space wrapped in **3mm of wall**, so its outside is
**31mm**, and coring it out for air does not shrink it. A run of *N* blocks is **31N mm**
along the bore. The 22 blocks here are 682mm of centreline.

Standard flags, uniform across the set — mixing `burn` changes finger joint fit while every
outside dimension still matches, which no drawing shows:

```
--blocksize=31 --thickness=3 --burn=0.1 --labels=0 --reference=0
--inner_corners=corner --spacing=0.5
```

## No elbows — the rule that shapes the walk

An **elbow** is a single block stranded as its own piece because the turn in it had no
straight block to fold into. Its opening frame has **three sides, not four**, so both
neighbouring sections need flattened plates butt-glued to it, plus tongues, plus an
unfilled void inside the corner. That gluing is the difficulty of the whole build.
**This design has none.**

Whether a turn costs an elbow is decided over **every window of three consecutive terms**
(outer *A*, middle *m*, outer *C*), not once per walk. Consecutive terms are always on
different axes, so there are three cases:

| *A* and *C* | case | *m* must be |
| --- | --- | ---: |
| same axis, same direction | step | >= 1 |
| same axis, opposite direction | hairpin | >= 2 |
| different axes | coil | >= 3 |

`../bore-generator/CLAUDE.md`, `../trumpet-coiled/CLAUDE.md` and that repository's
`README.md` all stated only the coil case until 2026-08-29, lumping the other two together
as a fold that "costs nothing at any spacing" — right for steps, wrong for hairpins, and
this walk has two hairpins sitting exactly on the limit. All three now carry the table
above. Treat `bore_split.py` as the authority, not any document and not a reimplementation
of the rule.

Checking the current walk:

```
N1 W3 U2     3 axes         coil,    m = 3   OK
W3 U2 E3     W/E opposed    hairpin, m = 2   OK
U2 E3 N3     3 axes         coil,    m = 3   OK
E3 N3 D3     3 axes         coil,    m = 3   OK
N3 D3 W2     3 axes         coil,    m = 3   OK
D3 W2 U3     D/U opposed    hairpin, m = 2   OK
W2 U3 N1     3 axes         coil,    m = 3   OK
```

**Every window sits exactly on its minimum.** Verified 2026-08-29 by decrementing each
interior term in turn: all seven produce elbows, the two hairpins two apiece and the rest
one. There is no slack anywhere in this walk — it cannot be tightened by a single block
without paying for it, and any proposal to shorten it must add length elsewhere.

## The ends are as short as a section can be

Sections 1 and 6 have a single straight block either side of their turn, which is the least
a section can hold. That was deliberate — the mouth and bell runs were cut back to leave
room for the mouthpiece and the bell to seat — but it means **neither end will absorb
another block of trimming**. If a socket needs to seat *into* a section rather than butt
against it, the walk has to grow, not shrink.

## Four sections, two shapes

Sections 1 and 4 are both `BDL`; sections 3 and 6 are both `BRD`. They are cut separately
anyway so each carries its own engraved number and the assembly order stays readable on the
bench. That duplication is also why this design is in `regress.py` — nothing else in the
library checks that a repeated shape still gets its own number.

## Colour is the cut order

Shared across all these repositories: **blue engraves, then green → orange → cyan →
black**; black is always the cut that frees the part; **violet `#8000ff` means skip**.

These nets use two stages — `#0000ff` engraves the section number on every part, then
`#000000` cuts.

## Cut files belong to the author

The author edits SVGs in Inkscape **during a session**. Treat every cut file as
concurrently modified:

- **Stage by name.** Never `git add -A` or `git add .` — it will sweep up an in-progress
  Inkscape save.
- **Never regenerate a cut file** the author has hand-edited (nesting, numbering, curve
  conversion) without asking.
- Regenerating rewrites **every** SVG here, and a changed section length renames a file —
  `06_bend_RDD.svg` became `06_bend_RD.svg` when the last term went from `N2` to `N1`. The
  old file is not deleted for you. Check for orphans after a regenerate.

## The gate does not run under the system python

`bore_split.py --write` calls the gate itself, but `check.py` imports **shapely**, which is
not in `/usr/bin/python3`. Run as a script it therefore writes all six files and then dies
with `ModuleNotFoundError` — **the files are written and ungated**. shapely lives in the
Boxes.py virtualenv, so run the gate from there:

```sh
~/boxes/venv/bin/python check.py "$(cat walks/trumpet_final_youtube_candidate.txt)" \
    --files ../trumpet-final-youtube-candidate
```

`regress.py` passes `sys.executable` down to `check.py`, so it must be started with the
same interpreter or every design fails on the import.

`regress.py` also only passes `--files` **when the folder exists**. If this repository is
moved or renamed without updating the path in its `DESIGNS` entry, the gate will go on
printing `pass` while checking the geometry alone and never touching these SVGs.

## Commands

```sh
G=../lasermade-tools
S=../bore-generator
```

**Test a walk without writing anything** — always do this before proposing a change:

```sh
cd $S && python3 bore_split.py --no-write "N N1 W3 U2 E3 N3 D3 W2 U3 N1"
```

**Regenerate the cut files** (rewrites everything — ask first):

```sh
cd $S && python3 bore_split.py \
    "$(cat walks/trumpet_final_youtube_candidate.txt)" \
    --write ../trumpet-final-youtube-candidate
```

**Checks:**

```sh
python3 $G/svg-stroke-check.py --dir . --quiet   # stroke declared twice, disagreeing
cd $S && ~/boxes/venv/bin/python regress.py      # every design in the library
```

The gate reports **194 checks, 0 failed** on this design, and `regress.py` covers 20
designs. Nothing here should be cut from a file that has not passed it.

**After editing `README.md`** — regenerate the page, then audit:

```sh
python3 $G/md2html.py README.md index.html
python3 $G/doc-audit.py README.md --html index.html
```

**Read the audit output before pushing.** It ends with a pass/fail tally. `.doc-audit-ignore`
lists `bore_split.py` and `regress.py`, which the prose names but which live in
`../bore-generator`; the audit also insists every tracked file is named somewhere, which is
why the section table carries a file column.

## Publishing

GitHub Pages deploys from `main` via Actions — `.github/workflows/pages.yml` is the sibling
repositories' workflow, with a per-sha concurrency group rather than one for the whole
site. A single shared group means a run that wedges holds the lock and every later push
queues behind it; keyed on the sha, a stuck run can only block a re-run of its own commit.

`index.html` is generated and committed, not built on the server, so **a stale `index.html`
publishes stale content**. Pages was switched to Actions with
`gh api -X POST repos/Gernreich/trumpet-final-youtube-candidate/pages -f build_type=workflow`
on 2026-08-29; without that the deploy has nowhere to publish to.

**Match the deploy to your SHA**, not to "the most recent run":

```sh
SHA=$(git rev-parse HEAD)
gh run list -L5 --json status,conclusion,headSha \
  -q ".[] | select(.headSha==\"$SHA\") | .status+\" \"+(.conclusion//\"-\")"
```

## The name

The design was called **twin switchback** until 2026-08-29, when it was moved out of the
shared library at `~/LaserMadeMusic/test` and given this repository. The folder, the walk
file and the `regress.py` entry were renamed together — if you find "twin switchback"
anywhere, it is a leftover.
