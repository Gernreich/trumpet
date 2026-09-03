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
RADIUS = 30.0        # bend radius of the centreline; see the minimum below
TAIL = 15.0          # straight lead-in and lead-out
THICK = 3.0          # ply
WEB = 2.0            # material left outboard of a slot; the cheek's thin part

# Where a wall's CENTRELINE sits, and where the cheek's edge does.
#
# The wall is THICK thick and its slot is centred on this line, so its inner
# face stands THICK/2 inboard of it. Offsetting the walls to +-BORE/2 - which
# is what this did until 2026-09-03 - therefore puts the wall FACES at
# +-(BORE-THICK)/2 and makes the airway BORE-THICK wide: 7mm at the 10mm bore,
# not 10. Reported from a measurement of a cut file, and the section check did
# not catch it because it measured centreline to centreline and called that
# the bore.
# Functions, not constants: --bore and --web change these, and a module-level
# value computed at import cannot follow. WALL_OFF was a constant for exactly
# one run and --bore=25 quietly kept the 10mm figure - which the airway check
# caught, reporting 15mm of error against a 25mm bore.
def wall_off():
    return BORE / 2 + THICK / 2


def cheek_off():
    return wall_off() + THICK / 2 + WEB


def band():
    return 2 * cheek_off()
BURN = 0.1           # kerf; the laser takes this out, centred on the line
# Per side, and a lookup of what has actually been cut, not a curve through
# it - bore-generator's PLAY_BY_BORE, same figures. 0 at the 25mm bore and
# 0.025 at the 10mm: required clearance FALLS as the joint grows, which fits a
# fabrication error that does not scale against elastic take-up that does.
# A bore not in the table gets the small-joint value, because too loose is a
# worse joint and too tight is no joint at all.
PLAY_BY_BORE = {25.0: 0.0, 10.0: 0.025}
PLAY_UNMEASURED = 0.025
PLAY = PLAY_BY_BORE.get(25.0, PLAY_UNMEASURED)   # set for BORE in main()
TOOTH = 2 * THICK    # Boxes.py FingerJointSettings; does not scale
SHOULDER = 2.0       # least material either side of a tooth

CUT, INNER, MARK = '#000000', '#ff8000', '#0000ff'
OUT = None           # --out=PATH, for trying a change without touching the file
BED_W, BED_H = 600.0, 308.0        # xTool P2S work area

# --shape. 'coupon' is the 180 degree test piece; 'serpentine' is a run of
# alternating half-circles joined by straight verticals, which is the drawn
# shape generalised. LOBES/LOBE_R/RISE describe it.
SHAPE = 'coupon'
# Solved against this generator's own faceted centreline, not a smooth arc:
# an inscribed chord is 1.14% short of the arc it spans, so a radius picked
# from the arc comes out 11mm long over a metre. R here gives 1000.0mm.
# The rise is chosen to balance the cheek on the bed rather than to be small:
# a half-circle advances only 2/pi of its own length in x, so a 1000mm run
# wants 637mm of width and the bed has 600 - a straight vertical run buys
# length in y, where there is room. At rise 90 the cheek is 531 x 251mm.
LOBES, LOBE_R, RISE, LEAD = 3, 71.754, 90.0, 20.0


def walk(spec):
    """A faceted polyline from a list of ('s', mm) and ('a', degrees, sign).

    Arcs are inscribed, so a chord's direction is the tangent at its midpoint
    and the junction where a straight meets an arc turns by half a facet, not
    a whole one. That is a smaller mitre and less area error, and it falls out
    of inscribing rather than having to be arranged.
    """
    pts, x, y, a = [(0.0, 0.0)], 0.0, 0.0, 0.0
    for item in spec:
        if item[0] == 's':
            x, y = x + math.cos(a) * item[1], y + math.sin(a) * item[1]
            pts.append((x, y))
        else:
            _, deg, sign = item
            n = int(round(deg / FACET))
            if abs(n * FACET - deg) > 1e-9:
                raise ValueError(
                    f'--facet={FACET:g} does not divide a {deg:g} degree turn '
                    f'a whole number of times; {n} facets would turn '
                    f'{n * FACET:g} degrees.')
            R = LOBE_R if SHAPE == 'serpentine' else RADIUS
            cx = x - sign * R * math.sin(a)
            cy = y + sign * R * math.cos(a)
            t0 = math.atan2(y - cy, x - cx)
            for i in range(1, n + 1):
                t = t0 + sign * math.radians(deg) * i / n
                x, y = cx + R * math.cos(t), cy + R * math.sin(t)
                pts.append((x, y))
            a += sign * math.radians(deg)
    return pts


def flip(pts):
    """Negate y, so the file renders the way the shape is drawn.

    Everything here is worked out with y running up, the way the geometry
    reads. SVG runs y down, so writing those coordinates straight out renders
    the shape upside down - a hump becomes a trough. The cut part is identical
    either way, being a mirror of itself turned over, but a cut file that does
    not look like the thing it makes is a cut file you check twice.

    Applied here and nowhere else, so every offset, normal, mitre and label
    angle downstream is computed in the flipped space and comes out right.
    Glyphs are NOT flipped: label() already draws them for SVG.
    """
    return [(x, -y) for x, y in pts]


def centreline():
    """The centreline, already faceted at FACET and flipped into SVG's y.

    The panels ARE the segments of this polyline offset sideways - there is no
    separate faceting step, so there is nothing for it to disagree with.
    """
    if SHAPE == 'serpentine':
        # a lead-in, a quarter turn up, then alternating half-circles joined
        # by straight verticals, and a tail. The verticals are what make it
        # fit: a half-circle advances only 2/pi of its own length in x, so a
        # 1000mm run needs 637mm of width however it is divided, and the bed
        # is 600. A vertical run buys length in y, where there is room.
        spec = [('s', LEAD), ('a', 90, +1)]
        for i in range(LOBES):
            spec.append(('a', 180, -1 if i % 2 == 0 else +1))
            if i < LOBES - 1:
                spec.append(('s', RISE))
        spec.append(('s', LEAD))
        return flip(walk(spec))
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
    return flip(pts)


def walls(poly):
    """(inner, outer) offset polylines, named by which one is actually inside.

    Asserted rather than assumed: the sign of the offset depends on which way
    round the centreline is written, and getting it backwards silently swaps
    every panel length in the cut list.
    """
    w = wall_off()
    a, b = offset(poly, w), offset(poly, -w)
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


def teeth(L):
    """Where the tabs sit along a panel of length L, as offsets from centre.

    One tooth was enough at the coupon's 10-16mm panels and is a hinge at 90mm:
    a straight run held by a single 6mm tab in its middle pivots about it and
    the seam opens. Alternating tooth and gap of equal width, as Boxes.py does,
    so a panel gets as many as it has room for:

        n = floor((L - 2*SHOULDER + TOOTH) / (2*TOOTH))

    which is 1 up to 17.9mm, 3 at 34mm and 7 at 90mm, and still 1 for every
    panel on the coupon - so the coupon's cut file does not move.
    """
    n = max(1, int((L - 2 * SHOULDER + TOOTH) // (2 * TOOTH)))
    return [(i - (n - 1) / 2.0) * 2 * TOOTH for i in range(n)]


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
    cs = teeth(L)
    out = [(-hl, -hb)]
    for c in cs:
        out += [(c - ht, -hb), (c - ht, -tip), (c + ht, -tip), (c + ht, -hb)]
    out += [(hl, -hb), (hl, hb)]
    for c in reversed(cs):
        out += [(c + ht, hb), (c + ht, tip), (c - ht, tip), (c - ht, hb)]
    out.append((-hl, hb))
    return out


def slots_for(part):
    """Every mortice for one panel, placed on its segment.

    One per tooth, spaced along the segment exactly as the tabs are.
    """
    mx, my = part['mid']
    ca, sa = math.cos(part['ang']), math.sin(part['ang'])
    return [slot((mx + c * ca, my + c * sa), part['ang'])
            for c in teeth(part['len'])]


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
    d = cheek_off()
    a = offset(poly, d)
    b = offset(poly, -d)
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
    cl = c
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
            # Away from the bore, measured rather than assumed: from the
            # centreline's own midpoint out to the wall's. A left normal with
            # a sign flip for the inner wall works only for one handedness,
            # and flipping y into SVG's coordinates reverses it - which put
            # 122 of 504 engraved points off the material.
            m0 = ((cl[i - 1][0] + cl[i][0]) / 2, (cl[i - 1][1] + cl[i][1]) / 2)
            dx, dy = mid[0] - m0[0], mid[1] - m0[1]
            dl = math.hypot(dx, dy) or 1.0
            nx, ny = dx / dl, dy / dl
            seq += 1
            tag = f'{seq:X}'
            parts.append({'kind': 'panel', 'wall': name, 'n': i, 'len': L,
                          'mid': mid, 'ang': ang, 'out': (nx, ny), 'tag': tag})
            report.append((tag, name, L))
    return c, inn, out, parts, report


def bbox(pts):
    xs = [q[0] for q in pts]
    ys = [q[1] for q in pts]
    return min(xs), min(ys), max(xs), max(ys)


def items_for(parts, cheekpoly, cline):
    """Every part as (outline, slots, labeller), in its own coordinates.

    The labeller is deferred because a label's position depends on where the
    part is finally placed, and placement is the packer's business.
    """
    out = []
    for k in range(2):
        def cheek_marks(dx, dy, _p=parts, _c=cline):
            m = []
            for q in _p:
                mx, my = q['mid'][0] + dx, q['mid'][1] + dy
                ox, oy = q['out']
                off = THICK / 2 + 1.5
                # into the channel: with WEB at 2mm there is no flange to
                # write on, and the channel is the floor of the bore
                m += label(q['tag'], mx - ox * off, my - oy * off, 2.0, q['ang'])
            # a little way ALONG the first segment, not at its start: the
            # band begins there and half the glyph hung off the end. A
            # quarter of the way in also clears panel 1's label, which sits
            # at the segment's midpoint offset across.
            a0, a1 = _c[0], _c[1]
            t = 0.22
            gx = a0[0] + (a1[0] - a0[0]) * t + dx
            gy = a0[1] + (a1[1] - a0[1]) * t + dy
            m += label('0', gx, gy, 2.6,
                       math.atan2(a1[1] - a0[1], a1[0] - a0[0]))
            return m
        out.append({'outline': cheekpoly,
                    'slots': [sl for q in parts for sl in slots_for(q)],
                    'marks': cheek_marks})
    for q in parts:
        w = q['len'] + BURN
        h2 = (BORE + 2 * THICK + BURN) / 2
        poly = [(px + w / 2, py + h2) for px, py in panel(q['len'])]

        def panel_marks(dx, dy, _t=q['tag'], _w=w, _h=h2):
            return label(_t, _w / 2 + dx, _h + dy, 3.2)
        out.append({'outline': poly, 'slots': [], 'marks': panel_marks})
    return out


MARGIN_S = 10.0      # sheet margin: the packer's and the reported size's


def pack(items, margin=MARGIN_S, gap=4.0):
    """Row-wrap into sheets, closing a sheet when the next row would overflow.

    Packs into BED minus a margin all round, not into the bed. Filling to the
    edge gave a sheet 600 x 307 on a 600 x 308 bed, which passes a fits-the-bed
    check and cannot be positioned on a real machine.

    A part larger than the usable area is a refusal, not a smaller sheet: it
    cannot be cut at all and saying so beats writing a file that looks fine.
    """
    use_w, use_h = BED_W - 2 * margin, BED_H - 2 * margin
    sheets, cur = [], []
    x, y, rowh = margin, margin, 0.0
    for it in items:
        x0, y0, x1, y1 = bbox(it['outline'])
        w, h = x1 - x0, y1 - y0
        if w > use_w or h > use_h:
            raise ValueError(
                f'a part is {w:.0f} x {h:.0f}mm and the usable area is '
                f'{use_w:.0f} x {use_h:.0f} on a {BED_W:g} x {BED_H:g} bed. '
                f'Nothing written. Shorten the bore, or add lobes so each '
                f'half-circle is smaller.')
        if x > margin and x + w > margin + use_w:
            if y + rowh + gap + h > margin + use_h:
                sheets.append(cur)
                cur, x, y, rowh = [], margin, margin, 0.0
            else:
                x, y, rowh = margin, y + rowh + gap, 0.0
        cur.append((it, x - x0, y - y0))
        x += w + gap
        rowh = max(rowh, h)
    if cur:
        sheets.append(cur)
    return sheets


def sheet(parts, cheekpoly, cline, path_out, write=True):
    """Write one SVG per sheet, and report what went on them.

    Colour is the cut order, shared with every repository here: blue engraves,
    then orange, then black. The slots are orange because they are inside the
    cheek and have to be cut while the sheet still holds it; black frees the
    parts.

    The two cheeks are IDENTICAL and both go on the same way up. Flipping one
    over mirrors its slot pattern, and neither of these shapes is symmetric
    about the line you would flip it on, so a flipped cheek does not meet a
    single tab.
    """
    sheets = pack(items_for(parts, cheekpoly, cline))
    ink, cut_slots, written = [], [], []
    over = 100 * (1 / math.cos(math.radians(FACET) / 2) - 1)
    for n, placed in enumerate(sheets, 1):
        marks, holes, cuts = [], [], []
        for it, dx, dy in placed:
            here = [(q[0] + dx, q[1] + dy) for q in it['outline']]
            cuts.append(path(here))
            for sl in it['slots']:
                moved = [(q[0] + dx, q[1] + dy) for q in sl]
                # tagged with the sheet, because two sheets are two files and
                # their coordinates have nothing to do with each other. The
                # first version of the slot check compared ink on sheet 3
                # against slots on sheet 1 and reported three collisions that
                # were two different pieces of paper.
                cut_slots.append((moved, n))
                holes.append(path(moved))
            for d in it['marks'](dx, dy):
                marks.append(d)
                for tok in d.replace('M ', '').replace('Z', '').split(' L '):
                    a, b = tok.strip().split(',')
                    ink.append((float(a), float(b), here, n))
        # the same margin the packer used, not a second constant that can
        # drift from it
        W = max(bbox(it['outline'])[2] + dx for it, dx, dy in placed) + MARGIN_S
        H = max(bbox(it['outline'])[3] + dy for it, dx, dy in placed) + MARGIN_S

        def grp(ds, col, name):
            if not ds:
                return ''
            return (f'  <g id="{name}" fill="none" stroke="{col}" '
                    f'stroke-width="0.2">\n'
                    + '\n'.join(f'    <path d="{d}"/>' for d in ds)
                    + '\n  </g>\n')

        of = f' {n} of {len(sheets)}' if len(sheets) > 1 else ''
        stem, ext = os.path.splitext(path_out)
        this = path_out if len(sheets) == 1 else f'{stem}-sheet{n}{ext}'
        body = (
            f'<?xml version="1.0" encoding="utf-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" '
            f'height="{H:.2f}mm" viewBox="0 0 {W:.2f} {H:.2f}">\n'
            f'<title>Ribbon bore{of} - {BORE:g}mm square bore, {FACET:g} degree '
            f'facets, {SHAPE}</title>\n'
            f'<desc>1 user unit = 1mm. A duct of constant {BORE:g} x {BORE:g}mm '
            f'section swept along a planar curve. Two identical cheeks (0, both '
            f'the same way up) and {len(parts)} wall panels numbered along the '
            f'flow. The section is exact along every facet and {over:.1f}% over '
            f'at each mitre. {THICK:g}mm ply, {BURN:g}mm kerf, {PLAY:g}mm play '
            f'per side taken out of the slot and never off the tab. blue '
            f'#0000ff engraves, orange #ff8000 cuts the slots first, black '
            f'#000000 frees the parts.</desc>\n'
            + grp(marks, MARK, 'numbers') + grp(holes, INNER, 'slots')
            + grp(cuts, CUT, 'outlines') + '</svg>\n')
        if write:
            open(this, 'w').write(body)
        written.append((os.path.basename(this), W, H, len(placed)))
    return written, ink, cut_slots


def inside(poly, x, y):
    n, c = len(poly), False
    for i in range(n):
        (ax, ay), (bx, by) = poly[i], poly[i - 1]
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax:
            c = not c
    return c


def checks(c, inn, out, parts, cheekpoly, written, ink, cut_slots):
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
            # centreline to centreline MINUS one wall thickness, because
            # half a wall stands inboard on each side. Measuring the two
            # offset lines and calling the answer the bore is how a 7mm
            # airway passed this check calling itself 10mm.
            air = math.hypot(f[0] - m[0], f[1] - m[1]) - THICK
            worst = max(worst, abs(air - BORE))
            n += 1
    note(n > 0 and worst < 1e-9, 'the airway is the bore along every facet',
         f'{n} stations, worst {worst:.2e}mm from {BORE:g} '
         f'(wall face to wall face)')

    # --- every slot has to be in the cheek, or a tab has nothing to enter
    allslots = [sl for p in parts for sl in slots_for(p)]
    off = sum(1 for sl in allslots for pt in sl
              if not inside(cheekpoly, *pt))
    note(off == 0 and allslots, 'every slot corner is inside its cheek',
         f'{4 * len(allslots)} corners on {len(allslots)} slots, {off} outside')

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
    boxes = allslots
    pairs = [(i, j) for i in range(len(boxes)) for j in range(i + 1, len(boxes))]
    bad = sum(1 for i, j in pairs if not apart(boxes[i], boxes[j]))
    note(bad == 0, 'no two slots overlap',
         f'{len(pairs)} pairs, {bad} overlapping')

    # --- the tooth does not scale, so short panels are the failure mode
    short = min(p['len'] for p in parts)
    note(short >= TOOTH + 2 * SHOULDER, 'the shortest panel still holds a tooth',
         f'{short:.2f}mm against {TOOTH + 2 * SHOULDER:g}mm needed')

    off = sum(1 for x, y, owner, _ in ink if not inside(owner, x, y))
    note(off == 0 and len(ink) > 0, 'every engraved point is on its own part',
         f'{len(ink)} points, {off} off the material')

    # a number engraved over a slot is engraved into a hole, and what it
    # actually marks is the edge of the panel standing in it
    over = sum(1 for x, y, _, sh in ink
               if any(inside(sl, x, y) for sl, s2 in cut_slots if s2 == sh))
    note(over == 0 and len(cut_slots) == 2 * len(allslots),
         'no engraving lands in a slot',
         f'{len(ink)} points against {len(cut_slots)} slots, {over} inside one')

    note(WEB >= 1.5, 'the web outboard of a slot is cuttable',
         f'{WEB:g}mm of ply beside a {THICK:g}mm slot, band '
         f'{band():g}mm wide')

    big = [n for n, w, h, _ in written if w > BED_W or h > BED_H]
    note(not big and len(written) > 0, 'every sheet fits the P2S bed',
         f'{len(written)} sheet(s), largest '
         f'{max(w for _, w, _, _ in written):.0f} x '
         f'{max(h for _, _, h, _ in written):.0f}mm against '
         f'{BED_W:g} x {BED_H:g}')
    return res


def main(write=True):
    global PLAY
    PLAY = PLAY_BY_BORE.get(round(BORE, 3), PLAY_UNMEASURED)
    c, inn, out, parts, report = build()
    over = 100 * (1 / math.cos(math.radians(FACET) / 2) - 1)
    R = LOBE_R if SHAPE == 'serpentine' else RADIUS
    what = (f'{LOBES} half-circles of R{R:g} joined by {RISE:g}mm straights'
            if SHAPE == 'serpentine' else f'one 180 degree bend of R{R:g}')
    print(f'ribbon bore, {SHAPE}   {BORE:g}mm square, {FACET:g} degree facets')
    print(f'  {what}')
    print(f'  centreline {sum(seglen(a, b) for a, b in zip(c, c[1:])):.1f}mm, '
          f'section {BORE:g} x {BORE:g} = {BORE * BORE:.0f}mm2, '
          f'+{over:.1f}% at each mitre')
    known = round(BORE, 3) in PLAY_BY_BORE
    print(f'  bend R/bore = {R / BORE:.1f}; the inner wall runs at '
          f'R{R - BORE / 2:g}')
    print(f'  play {PLAY:g}mm per side'
          + ('' if known else f'  (the {BORE:g}mm bore is not in PLAY_BY_BORE; '
                              f'this is the small-joint default. Measure it '
                              f'and add a row.)') + '\n')
    print('  part   wall     length     tooth   shoulders')
    for tag, wall, L in report:
        print(f'  {tag:<5}  {wall:<7}  {L:>6.2f}mm   {TOOTH:g}mm    '
              f'{(L - TOOTH) / 2:>5.2f}mm')
    cheekpoly = cheek(c)
    # --out exists because a failing run deletes its output, and a copy of
    # this script tried out in the same folder therefore deleted the real cut
    # file. A trial writes somewhere else or it does not write at all.
    L = sum(seglen(a, b) for a, b in zip(c, c[1:]))
    if SHAPE == 'serpentine':
        stem = (f'ribbon-serpentine-bore{BORE:g}-{FACET:g}deg-{LOBES}lobes'
                f'-R{LOBE_R:.0f}-{L:.0f}mm-cut-files.svg')
    else:
        stem = (f'ribbon-coupon-bore{BORE:g}-{FACET:g}deg'
                f'-R{RADIUS:g}-180turn-cut-files.svg')
    out_path = OUT or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), stem)
    written, ink, cut_slots = sheet(parts, cheekpoly, c, out_path, write)
    print(f'\n  {len(parts)} wall panels + 2 cheeks = {len(parts) + 2} parts, '
          f'{len(written)} sheet{"s" if len(written) > 1 else ""}')
    for name, w, h, k in written:
        print(f'    {name:<56}{k:>3} parts  {w:.0f} x {h:.0f}mm')
    bad = 0
    print()
    for ok, what, detail in checks(c, inn, out, parts, cheekpoly,
                                   written, ink, cut_slots):
        print(f'  {"pass" if ok else "FAIL"}  {what:<44} {detail}')
        bad += not ok
    if write and not bad:
        print(f'\n  wrote {len(written)} file(s)')
    elif bad:
        if write:
            for name, _, _, _ in written:
                f = os.path.join(os.path.dirname(os.path.abspath(out_path)), name)
                if os.path.exists(f):
                    os.remove(f)
        print(f'\n  {bad} check(s) failed. Nothing written.')
    return 1 if bad else 0


if __name__ == '__main__':
    # a geometry that cannot be built is an answer, not a crash
    a = sys.argv[1:]
    for flag, cast in (('out', str), ('shape', str), ('bore', float),
                       ('facet', float), ('radius', float), ('lobes', int),
                       ('lobe-r', float), ('rise', float), ('lead', float),
                       ('web', float)):
        hit = [x for x in a if x.startswith(f'--{flag}=')]
        if not hit:
            continue
        v = cast(hit[0].split('=', 1)[1])
        {'out': 'OUT', 'shape': 'SHAPE', 'bore': 'BORE', 'facet': 'FACET',
         'radius': 'RADIUS', 'lobes': 'LOBES', 'lobe-r': 'LOBE_R',
         'rise': 'RISE', 'lead': 'LEAD', 'web': 'WEB'}[flag]
        globals()[{'out': 'OUT', 'shape': 'SHAPE', 'bore': 'BORE',
                   'facet': 'FACET', 'radius': 'RADIUS', 'lobes': 'LOBES',
                   'lobe-r': 'LOBE_R', 'rise': 'RISE', 'lead': 'LEAD',
                   'web': 'WEB'}[flag]] = v
    try:
        sys.exit(main(write='--no-write' not in a))
    except ValueError as e:
        print(f'error: {e}')
        sys.exit(1)
