#!/usr/bin/env python3
"""One page holding a design at every block size it is cut at.

    python3 sizes.py trumpet_switchback ../trumpet-switchback/sizes.html

A design cut at two sizes is one shape and two pitches: the walk, the sections
and the shapes are identical, and only the millimetres differ. Two pages make
that hard to see, because you lose the camera opening the second one. Here they
share a viewer and a control swaps the pitch.

Not a second viewer -- viewer.build_many is the same template and the same
drawing code a per-size page goes through, with more than one set in it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bore_split as B                                        # noqa: E402
import viewer                                                 # noqa: E402

# label, the --blocksize it is cut at. Largest first: it is the one the design
# was drawn for, and the small one reads as a reduction of it.
SIZES = [('25mm', 31.0), ('10mm', 16.0)]


def main(walk_name, out):
    here = os.path.dirname(os.path.abspath(__file__))
    text = open(os.path.join(here, 'walks', walk_name + '.txt')).read().strip()
    items, stats = [], []
    for label, block in SIZES:
        # the walk is the same string at both sizes; only the pitch moves, and
        # data_for reads BLOCK when it builds, so set it before each one
        B.set_blocksize(block)
        items.append((label, text))
        rec, groups, _, _, _ = B.specs_for(B.walk_text(text))
        stats.append((label, block, len(rec), len(rec) * block, len(groups)))
    title = walk_name.replace('_', ' ').title() + ' Bore'
    open(out, 'w').write(viewer.build_many(items, title))
    print(f'  {os.path.basename(out)}')
    for label, block, n, mm, g in stats:
        print(f'    {label:>5}  block {block:g}mm  {n} blocks  {mm:g}mm  {g} sections')


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) != 2:
        sys.exit('usage: sizes.py WALK_NAME OUT.html')
    main(a[0], a[1])
