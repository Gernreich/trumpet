#!/usr/bin/env python3
"""A bore of constant cross-section swept along a planar curve.

    python3 ribbon_bore.py                      # the 10mm 30-degree coupon
    python3 ribbon_bore.py --no-write           # the numbers, no file

Sweep a rectangle along a curve that lies in a plane, with one axis normal to
that plane, and the duct has two FLAT faces and two CYLINDRICAL ones. The flat
pair are the cheeks and cut straight from the sheet. The curved pair are the
whole problem: 3mm birch will not bend to these radii, so they are faceted -
short flat panels, each finger-jointed into both cheeks.

The section is exactly bore x bore along every facet. At each facet joint the
walls mitre, and the area there is bore^2 / cos(phi/2):

    phi = 90 deg   +41.4%      a turn in the Minecraft lattice
    phi = 45 deg    +8.2%      the octagonal torus
    phi = 30 deg    +3.5%      this
    phi = 15 deg    +0.9%

So the facet angle is the whole design dial, and it trades against part count
and against how short the inner panels get.

WHAT LIMITS THE BEND. The inner wall is the centreline offset inward by
bore/2, so its radius is R - bore/2 and there is no bore at all below
R = bore/2. Long before that the inner panel gets too short to carry a finger:
a Boxes.py tooth is 2 x thickness and does NOT scale with the bore, so at the
10mm bore and 30 degrees the inner panel holds no tooth at all until R = 25mm.
That is why this coupon is R 25 and not the R 15 it looks like it wants to be.
"""
import math
import os
import sys

BORE = 10.0          # the square section, mm
FACET = 30.0         # degrees of turn per wall panel
RADIUS = 25.0        # bend radius of the centreline
TAIL = 15.0          # straight lead-in and lead-out
THICK = 3.0          # ply
WEB = 2.0            # material left outboard of a slot; the cheek's thin part
MARGIN = THICK / 2 + WEB   # so the cheek band hugs the slots and stops
BURN = 0.1           # kerf; the laser takes this out, centred on the line
PLAY = 0.025         # per side, from bore-generator's PLAY_BY_BORE at 10mm
TOOTH = 2 * THICK    # Boxes.py FingerJointSettings; does not scale
SHOULDER = 2.0       # least material either side of a tooth

CUT, INNER, MARK = '#000000', '#ff8000', '#0000ff'
OUT = None           # --out=PATH, for trying a change without touching the file


def centreline():
    """The coupon's centreline: a straight tail, a 180 turn, a straight tail.

    Returned as a polyline already faceted at FACET, because the panels ARE
    the segments of this polyline offset sideways - there is no separate
    faceting step to disagree with it.
    """
    n = int(round(180.0 / FACET))
    if abs(n * FACET - 180.0) > 1e-9:
        raise ValueError(f'--facet={FACET:g} does not divide 180 a whole '
                         f'number of times; {n} facets would turn '
                         f'{n * FACET:g} degrees.')
    # The tails have to leave the arc along its TANGENT, or the first facet
    # turns by something that is not FACET and the panel that sits on it is
    # the wrong length. Attaching them at the arc's endpoints is not the same
    # thing as attaching them tangentially, and the first attempt here did the
    # former: it produced a 98mm panel on a coupon 78mm long.
    pts = [(RADIUS, TAIL)]                        # lead in, running -y
    for i in range(n + 1):                        # the turn, centred on origin
        a = -i * math.radians(FACET)              # (R,0) -> (0,-R) -> (-R,0)
        pts.append((RADIUS * math.cos(a), RADIUS * math.sin(a)))
    pts.append((-RADIUS, TAIL))                   # lead out, running +y
    return pts


def walls(poly):
    """(inner, outer) offset polylines, named by which one is actually inside.

    Asserted rather than assumed: the sign of the offset depends on which way
    round the centreline is written, and getting it backwards silently swaps
    every panel length in the cut list.
    """
    a, b = offset(poly, BORE / 2), offset(poly, -BORE / 2)
    la = sum(seglen(p, q) for p, q in zip(a, a[1:]))
    lb = sum(seglen(p, q) for p, q in zip(b, b[1:]))
    return (a, b) if la < lb else (b, a)


def offset(poly, d):
    """The polyline offset sideways by d, mitred at every interior vertex.

    Mitred by intersecting the neighbouring offset LINES, not by moving each
    vertex along its bisector by d - those agree only for a right angle, and
    at 30 degrees the second one is wrong by 3.5%, which is exactly the
    quantity this file exists to keep track of.
    """
    segs = []
    for a, b in zip(poly, poly[1:]):
        ux, uy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ux, uy)
        nx, ny = -uy / L, ux / L                  # left normal
        segs.append(((a[0] + nx * d, a[1] + ny * d),
                     (b[0] + nx * d, b[1] + ny * d)))
    out = [segs[0][0]]
    for s, t in zip(segs, segs[1:]):
        p = meet(s, t)
        out.append(p if p else s[1])
    out.append(segs[-1][1])
    return out


def meet(s, t):
    """Where two segments' infinite lines cross, or None if they are parallel."""
    (x1, y1), (x2, y2) = s
    (x3, y3), (x4, y4) = t
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(d) < 1e-12:
        return None
    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / d,
            (a * (y3 - y4) - (y1 - y2) * b) / d)


def seglen(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def rot(p, ang, at=(0.0, 0.0)):
    c, s = math.cos(ang), math.sin(ang)
    x, y = p[0] - at[0], p[1] - at[1]
    return (at[0] + x * c - y * s, at[1] + x * s + y * c)


def path(pts, close=True):
    d = 'M ' + ' L '.join(f'{x:.3f},{y:.3f}' for x, y in pts)
    return d + (' Z' if close else '')


def panel(L):
    """One wall panel, flat, centred on the origin, kerf already taken out.

    The laser removes BURN centred on the line, so every edge with material
    behind it is drawn BURN/2 outboard of where the material should end. Draw
    the true shape and the panel comes out BURN under in each dimension and
    the tab rattles.

    Shoulder to shoulder is the bore height exactly, because that is the gap
    between the cheeks' inner faces. The tab passes through its cheek and sits
    flush with the outside.
    """
    e = BURN / 2
    hl, ht = L / 2 + e, TOOTH / 2 + e
    hb, tip = BORE / 2 + e, BORE / 2 + THICK + e
    return [(-hl, -hb), (-ht, -hb), (-ht, -tip), (ht, -tip), (ht, -hb),
            (hl, -hb), (hl, hb), (ht, hb), (ht, tip), (-ht, tip),
            (-ht, hb), (-hl, hb)]


def slot(mid, ang):
    """The cheek's mortice for one tab: the hole is drawn BURN UNDER size.

    Opposite sign to the panel, and for the same reason - the kerf opens a
    hole and closes a part. Plus PLAY per side, which is bore-generator's
    figure for the 10mm bore, taken out of the notch and never off the tab.
    """
    e = BURN / 2
    hw = (TOOTH + 2 * PLAY) / 2 - e
    hh = THICK / 2 - e
    box = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
    return [(mid[0] + p[0] * math.cos(ang) - p[1] * math.sin(ang),
             mid[1] + p[0] * math.sin(ang) + p[1] * math.cos(ang))
            for p in box]


def cheek(poly):
    """The flat face: a ribbon of the bore plus a flange each side.

    Closed by running out along one offset and back along the other, so it is
    one contour with no island - which for a U with open tails it genuinely
    is, and a hole would have been wrong.
    """
    a = offset(poly, BORE / 2 + MARGIN)
    b = offset(poly, -(BORE / 2 + MARGIN))
    return a + b[::-1]


GLYPH = {'0': [[(0.5, 1), (0.85, 0.8), (0.85, 0.2), (0.5, 0), (0.15, 0.2), (0.15, 0.8), (0.5, 1)]], '1': [[(0.3, 0.78), (0.52, 1), (0.52, 0)], [(0.28, 0), (0.78, 0)]], '2': [[(0.1, 0.78), (0.3, 1), (0.7, 1), (0.9, 0.78), (0.9, 0.6), (0.1, 0), (0.9, 0)]], '3': [[(0.1, 1), (0.9, 1), (0.45, 0.55)], [(0.45, 0.55), (0.9, 0.55), (0.9, 0.16), (0.72, 0), (0.28, 0), (0.1, 0.16)]], '4': [[(0.7, 0), (0.7, 1), (0.12, 0.32), (0.92, 0.32)]], '5': [[(0.85, 1), (0.2, 1), (0.15, 0.55), (0.5, 0.62), (0.8, 0.5), (0.88, 0.28), (0.75, 0.06), (0.4, 0), (0.15, 0.12)]], '6': [[(0.82, 0.92), (0.55, 1), (0.25, 0.85), (0.15, 0.45), (0.15, 0.18), (0.35, 0), (0.62, 0), (0.85, 0.18), (0.85, 0.38), (0.62, 0.55), (0.3, 0.55), (0.15, 0.45)]], '7': [[(0.12, 1), (0.9, 1), (0.42, 0)]], '8': [[(0.5, 0.55), (0.22, 0.68), (0.22, 0.87), (0.5, 1), (0.78, 0.87), (0.78, 0.68), (0.5, 0.55), (0.18, 0.4), (0.18, 0.14), (0.5, 0), (0.82, 0.14), (0.82, 0.4), (0.5, 0.55)]], '9': [[(0.18, 0.08), (0.45, 0), (0.75, 0.15), (0.85, 0.55), (0.85, 0.82), (0.65, 1), (0.38, 1), (0.15, 0.82), (0.15, 0.62), (0.38, 0.45), (0.7, 0.45), (0.85, 0.55)]], 'A': [[(0.1, 0), (0.5, 1), (0.9, 0)], [(0.26, 0.4), (0.74, 0.4)]], 'B': [[(0.15, 0), (0.15, 1), (0.68, 1), (0.88, 0.83), (0.88, 0.68), (0.68, 0.55), (0.15, 0.55)], [(0.15, 0.55), (0.72, 0.55), (0.9, 0.4), (0.9, 0.16), (0.7, 0), (0.15, 0)]], 'C': [[(0.9, 0.8), (0.7, 1.0), (0.3, 1.0), (0.1, 0.8), (0.1, 0.2), (0.3, 0.0), (0.7, 0.0), (0.9, 0.2)]], 'D': [[(0.15, 0), (0.15, 1), (0.58, 1), (0.88, 0.74), (0.88, 0.26), (0.58, 0), (0.15, 0)]], 'E': [[(0.9, 1), (0.15, 1), (0.15, 0), (0.9, 0)], [(0.15, 0.5), (0.68, 0.5)]], 'F': [[(0.88, 1), (0.15, 1), (0.15, 0)], [(0.15, 0.52), (0.68, 0.52)]]}


def label(text, cx, cy, h, ang=0.0):
    """Hex glyphs centred on (cx, cy), with the baseline tick.

    The same table and the same tick as the bore sections, the bell rings and
    the torus pieces: 6 and 9 are one shape turned over, and the tick says
    which way up. Blue, so it engraves and never cuts.
    """
    w, gap = h * 0.62, h * 0.18
    total = len(text) * w + (len(text) - 1) * gap
    x, out = -total / 2, []
    for ch in text:
        for st in GLYPH[ch]:
            # the table's y runs up and SVG's runs down, so py has to be
            # flipped - without it every glyph is mirrored top to bottom and
            # a 2 comes out as something that is not a 2
            pts = [rot((x + px * w, h / 2 - py * h), ang) for px, py in st]
            out.append(path([(cx + p[0], cy + p[1]) for p in pts], close=False))
        x += w + gap
    tg, tl = h * 0.16, h * 0.22
    a = rot((total / 2 + tg, h / 2), ang)
    b = rot((total / 2 + tg + tl, h / 2), ang)
    out.append(path([(cx + a[0], cy + a[1]), (cx + b[0], cy + b[1])], close=False))
    return out


def build():
    """Every part, in millimetres, with the numbers each one carries."""
    c = centreline()
    inn, out = walls(c)
    parts, report = [], []
    # Numbered straight through in hex rather than I1/O1: the glyph table is
    # the one the bore sections and bell rings use, and adding I and O to it
    # would put I beside 1 and O beside 0 on a part you read at the bench.
    # Which wall a panel belongs to is never in doubt anyway - the inner ones
    # are 10-14mm and the outer ones 15-16mm, and the cheek slot carries the
    # same number.
    seq = 0
    for name, poly in (('inner', inn), ('outer', out)):
        for i, (a, b) in enumerate(zip(poly, poly[1:]), 1):
            L = seglen(a, b)
            if L < TOOTH + 2 * SHOULDER:
                raise ValueError(
                    f'{name} panel {i} is {L:.2f}mm and a {TOOTH:g}mm tooth '
                    f'with {SHOULDER:g}mm shoulders needs '
                    f'{TOOTH + 2 * SHOULDER:g}mm. Open the bend radius or '
                    f'coarsen --facet; the tooth does not scale with the bore.')
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            # away from the bore: the left normal of the segment, flipped
            # for the inner wall. The number goes out here, on the flange -
            # engraving inside the airway is roughness in the bore, and this
            # is a bore.
            nx, ny = -(b[1] - a[1]) / L, (b[0] - a[0]) / L
            if name == 'inner':
                nx, ny = -nx, -ny
            seq += 1
            tag = f'{seq:X}'
            parts.append({'kind': 'panel', 'wall': name, 'n': i, 'len': L,
                          'mid': mid, 'ang': ang, 'out': (nx, ny), 'tag': tag})
            report.append((tag, name, L))
    return c, inn, out, parts, report


def sheet(parts, cheekpoly, cline, path_out):
    """Lay the coupon out: two cheeks, then the panels in rows.

    Colour is the cut order, shared with every repository here: blue engraves,
    then orange, then black. The slots are orange because they are inside the
    cheek and have to be cut while the sheet still holds it; black frees the
    parts.

    The two cheeks are IDENTICAL and both go on the same way up. Flipping one
    over mirrors its slot pattern, and this U is not symmetric about the line
    you would flip it on, so a flipped cheek does not meet a single tab.
    """
    M, GAP, ROW = 10.0, 4.0, 300.0
    marks, holes, cuts = [], [], []
    # every engraved point, with the outline it has to sit on. The cheek's
    # own number was engraved in the hole in the middle of the arch until
    # this existed; the render showed it and no check did.
    ink = []
    cut_slots = []          # slots where they were PLACED, for the checks

    def engrave(ds, owner):
        marks.extend(ds)
        for d in ds:
            for tok in d.replace('M ', '').replace('Z', '').split(' L '):
                a, b = tok.strip().split(',')
                ink.append((float(a), float(b), owner))

    xs = [p[0] for p in cheekpoly]
    ys = [p[1] for p in cheekpoly]
    cw, chh = max(xs) - min(xs), max(ys) - min(ys)
    for k in range(2):
        dx, dy = M - min(xs) + k * (cw + GAP), M - min(ys)
        here = [(x + dx, y + dy) for x, y in cheekpoly]
        cuts.append(path(here))
        for p in parts:
            mx, my = p['mid'][0] + dx, p['mid'][1] + dy
            here_slot = slot((mx, my), p['ang'])
            cut_slots.append(here_slot)
            holes.append(path(here_slot))
            # Into the channel, not out onto the flange. With WEB at 2mm
            # the flange is 2mm wide and a legible glyph does not fit on it.
            # The channel is the floor of the bore, so this is 0.1mm of
            # engraving inside a 10mm airway - which is the cheaper of the
            # two mistakes, the other being sixteen near-identical panels
            # with nothing on the cheek to say which slot each one goes in.
            ox, oy = p['out']
            off = THICK / 2 + 1.5
            engrave(label(p['tag'], mx - ox * off, my - oy * off, 2.0, p['ang']),
                    here)
        # in the channel at the mouth of the first tail. Not the centre of
        # the bounding box - for a U that centre is the hole in the middle
        # of the arch, and the first attempt engraved this onto the waste.
        t0 = cline[0]
        engrave(label('0', t0[0] + dx, t0[1] + dy - 2.6, 2.6), here)

    y, x, wide = M + chh + GAP + 8, M, 0.0
    for p in parts:
        w = p['len'] + BURN
        if x + w + M > ROW:
            x, y = M, y + BORE + 2 * THICK + BURN + GAP
        h2 = (BORE + 2 * THICK + BURN) / 2
        here = [(px + x + w / 2, py + y + h2) for px, py in panel(p['len'])]
        cuts.append(path(here))
        engrave(label(p['tag'], x + w / 2, y + h2, 3.2), here)
        x += w + GAP
        wide = max(wide, x)
    H = y + BORE + 2 * THICK + M
    W = max(2 * cw + GAP + 2 * M, wide + M - GAP)

    def grp(ds, col, name):
        if not ds:
            return ''
        return (f'  <g id="{name}" fill="none" stroke="{col}" '
                f'stroke-width="0.2">\n'
                + '\n'.join(f'    <path d="{d}"/>' for d in ds) + '\n  </g>\n')

    body = (grp(marks, MARK, 'numbers') + grp(holes, INNER, 'slots')
            + grp(cuts, CUT, 'outlines'))
    over = 100 * (1 / math.cos(math.radians(FACET) / 2) - 1)
    open(path_out, 'w').write(
        f'<?xml version="1.0" encoding="utf-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" '
        f'height="{H:.2f}mm" viewBox="0 0 {W:.2f} {H:.2f}">\n'
        f'<title>Ribbon bore coupon - {BORE:g}mm square bore, {FACET:g} degree '
        f'facets, R{RADIUS:g} 180 degree bend</title>\n'
        f'<desc>1 user unit = 1mm. A duct of constant {BORE:g} x {BORE:g}mm '
        f'section swept along a planar curve. Two identical cheeks (C, both '
        f'the same way up) and {len(parts)} wall panels: I* inside the bend, '
        f'O* outside, numbered along the flow. The section is exact along '
        f'every facet and {over:.1f}% over at each mitre. {THICK:g}mm ply, '
        f'{BURN:g}mm kerf, {PLAY:g}mm play per side taken out of the slot and '
        f'never off the tab. blue #0000ff engraves, orange #ff8000 cuts the '
        f'slots first, black #000000 frees the parts.</desc>\n'
        + body + '</svg>\n')
    return W, H, ink, cut_slots


def inside(poly, x, y):
    n, c = len(poly), False
    for i in range(n):
        (ax, ay), (bx, by) = poly[i], poly[i - 1]
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax:
            c = not c
    return c


def checks(c, inn, out, parts, cheekpoly, W, H, ink, cut_slots):
    """What has to be true, said out loud with the number that makes it true.

    A check that measured nothing would print the same clean run as a check
    that measured everything, so each one reports its count.
    """
    res = []

    def note(ok, what, detail):
        res.append((ok, what, detail))

    # --- the whole point: the section is the bore, everywhere along a facet
    worst, n = 0.0, 0
    for (a, b), (p, q) in zip(zip(inn, inn[1:]), zip(out, out[1:])):
        for t in (0.15, 0.35, 0.5, 0.65, 0.85):
            m = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            ux, uy = q[0] - p[0], q[1] - p[1]
            L2 = ux * ux + uy * uy
            s = ((m[0] - p[0]) * ux + (m[1] - p[1]) * uy) / L2
            f = (p[0] + ux * s, p[1] + uy * s)
            worst = max(worst, abs(math.hypot(f[0] - m[0], f[1] - m[1]) - BORE))
            n += 1
    note(n > 0 and worst < 1e-9, 'the section is the bore along every facet',
         f'{n} stations, worst {worst:.2e}mm from {BORE:g}')

    # --- every slot has to be in the cheek, or a tab has nothing to enter
    off = sum(1 for p in parts for pt in slot(p['mid'], p['ang'])
              if not inside(cheekpoly, *pt))
    note(off == 0, 'every slot corner is inside its cheek',
         f'{4 * len(parts)} corners, {off} outside')

    # --- and no two slots may run into each other
    # Separating axis, not centre distance: two slots 8mm apart can still
    # overlap if they are nearly parallel and 6mm long, and a centre-distance
    # test would call that clear.
    def apart(A, B):
        for R in (A, B):
            for i in range(len(R)):
                ax, ay = R[(i + 1) % len(R)][0] - R[i][0], R[(i + 1) % len(R)][1] - R[i][1]
                px, py = -ay, ax
                pa = [q[0] * px + q[1] * py for q in A]
                pb = [q[0] * px + q[1] * py for q in B]
                if max(pa) <= min(pb) or max(pb) <= min(pa):
                    return True
        return False
    boxes = [slot(p['mid'], p['ang']) for p in parts]
    pairs = [(i, j) for i in range(len(boxes)) for j in range(i + 1, len(boxes))]
    bad = sum(1 for i, j in pairs if not apart(boxes[i], boxes[j]))
    note(bad == 0, 'no two slots overlap',
         f'{len(pairs)} pairs, {bad} overlapping')

    # --- the tooth does not scale, so short panels are the failure mode
    short = min(p['len'] for p in parts)
    note(short >= TOOTH + 2 * SHOULDER, 'the shortest panel still holds a tooth',
         f'{short:.2f}mm against {TOOTH + 2 * SHOULDER:g}mm needed')

    off = sum(1 for x, y, owner in ink if not inside(owner, x, y))
    note(off == 0 and len(ink) > 0, 'every engraved point is on its own part',
         f'{len(ink)} points, {off} off the material')

    # a number engraved over a slot is engraved into a hole, and what it
    # actually marks is the edge of the panel standing in it
    over = sum(1 for x, y, _ in ink
               if any(inside(sl, x, y) for sl in cut_slots))
    note(over == 0 and len(cut_slots) == 2 * len(parts),
         'no engraving lands in a slot',
         f'{len(ink)} points against {len(cut_slots)} slots, {over} inside one')

    note(WEB >= 1.5, 'the web outboard of a slot is cuttable',
         f'{WEB:g}mm of ply beside a {THICK:g}mm slot, band '
         f'{BORE + 2 * MARGIN:g}mm wide')

    note(W <= 600 and H <= 308, 'the sheet fits the P2S bed',
         f'{W:.0f} x {H:.0f}mm against 600 x 308')
    return res


def main(write=True):
    c, inn, out, parts, report = build()
    over = 100 * (1 / math.cos(math.radians(FACET) / 2) - 1)
    print(f'ribbon bore coupon   {BORE:g}mm square, {FACET:g} degree facets, '
          f'R{RADIUS:g} 180 degree bend')
    print(f'  centreline {sum(seglen(a, b) for a, b in zip(c, c[1:])):.1f}mm, '
          f'section {BORE:g} x {BORE:g} = {BORE * BORE:.0f}mm2, '
          f'+{over:.1f}% at each mitre')
    print(f'  bend R/bore = {RADIUS / BORE:.1f}; the inner wall runs at '
          f'R{RADIUS - BORE / 2:g}\n')
    print('  part   wall     length     tooth   shoulders')
    for tag, wall, L in report:
        print(f'  {tag:<5}  {wall:<7}  {L:>6.2f}mm   {TOOTH:g}mm    '
              f'{(L - TOOTH) / 2:>5.2f}mm')
    cheekpoly = cheek(c)
    # --out exists because a failing run deletes its output, and a copy of
    # this script tried out in the same folder therefore deleted the real cut
    # file. A trial writes somewhere else or it does not write at all.
    out_path = OUT or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f'ribbon-coupon-bore{BORE:g}-{FACET:g}deg'
        f'-R{RADIUS:g}-180turn-cut-files.svg')
    W, H, ink, cut_slots = sheet(parts, cheekpoly, c,
                                 out_path if write else '/dev/null')
    print(f'\n  {len(parts)} wall panels + 2 cheeks = {len(parts) + 2} parts, '
          f'sheet {W:.0f} x {H:.0f}mm')
    bad = 0
    print()
    for ok, what, detail in checks(c, inn, out, parts, cheekpoly,
                                   W, H, ink, cut_slots):
        print(f'  {"pass" if ok else "FAIL"}  {what:<44} {detail}')
        bad += not ok
    if write and not bad:
        print(f'\n  wrote {os.path.basename(out_path)}')
    elif bad:
        if write:
            os.remove(out_path)
        print(f'\n  {bad} check(s) failed. Nothing written.')
    return 1 if bad else 0


if __name__ == '__main__':
    # a geometry that cannot be built is an answer, not a crash
    a = sys.argv[1:]
    o = [x for x in a if x.startswith('--out=')]
    if o:
        OUT = o[0].split('=', 1)[1]
    try:
        sys.exit(main(write='--no-write' not in a))
    except ValueError as e:
        print(f'error: {e}')
        sys.exit(1)
