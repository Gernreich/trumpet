"""Run the pre-cut gate over every design we have built or tried.

Designs diverge more than they look: the first trumpet never called the lap
code, so a crash in it went unseen until a spiral needed one, and a volume
check that passed the trumpet at +0.35% was 6% out on a spiral of identical
construction. A change is only known good against the whole set.

    python3 regress.py            # every design
    python3 regress.py trumpet    # those whose name matches
"""
import subprocess
import sys
import os

# (name, walk or walks/*.txt, folder of cut files or None[, block pitch mm])
DESIGNS = [
    ('first trumpet', 'N N10 U2 W2 S7 U2 E4 N9 W2 D2 N4 N',
     '../../test/first_trumpet'),
    ('spiral trumpet', 'U U3 N2 W2 S4 E4 U2 N6 W6 S8 E8 U2 N10 W10 S12 E12 U3 U',
     '../../test/spiral_trumpet'),
    ('helix, rise 2', 'N N4 U2 E4 U2 S4 U2 W4 U2 N4 N', None),
    ('helix, rise 1', 'N N4 U1 E4 U1 S4 U1 W4 U1 N4 N', None),
    ('helix, side 6', 'N N6 U2 E6 U2 S6 U2 W6 U2 N6 U2 E6 E', None),
    ('test bore', 'U U2 E2 S2 U2 U', None),
    ('three blocks', 'W D3 E4 N', None),
    # corners in a row. A leg of one block makes its block a corner, so these
    # are chains of touching corners - the case that used to raise rather than
    # cut, because the lap was named in the walk's frame and an elbow is drawn
    # in a canonical one.
    ('4 corners, flat', 'N N2 U1 N1 U1 N2 N', None),
    ('4 corners, solid', 'N N2 U1 E1 S1 E4 E', None),
    ('5 corners, solid', 'N N2 U1 E1 S1 W1 S3 S', None),
    ('6 corners, solid', 'N N2 E1 U1 E1 U1 E1 U3 U', None),
    # coils tight enough to touch themselves. The second used to be refused by
    # the generator: a piece came back alongside its own blocks, so one cell
    # had three neighbours and it was no longer a snake.
    ('tightest coil', 'U U3 N1 E1 S1 U1 W1 U1 N1 E1 S1 U1 W1 U1 '
                      'N1 E1 S1 U1 W1 U1 U', None),
    ('touching coil', 'N N2 E1 S2 U1 W1 U1 N2 E1 S2 U1 W1 U1 '
                      'N2 E1 S2 U1 W1 U1 U', None),
    # a space-filling curve: every cell of a 2x2x2 used, so it touches itself
    # everywhere it can. python3 hilbert.py 1 prints it.
    ('hilbert cube 1', 'S S1 U1 N1 E1 S1 D1 N1', None),
    # the same curve at scale 2: the open knot rather than the solid block.
    # Too long to sit in this list, so it is kept beside it.
    ('hilbert cube 2', 'walks/hilbert_cube.txt', None),
    # the same 4x4x4 filled corner to opposite corner instead, so the mouth and
    # the bell are as far apart as the box allows
    ('corner to corner', 'walks/corner_to_corner.txt', None),
    # the knot with the bell taken out under it and up past the top, so the
    # two ends are at opposite corners of the whole thing
    ('hilbert snorkel', 'walks/hilbert_snorkel.txt', None),
    # a piece spiralling inward touches its own arms at a corner, which the
    # generator refuses as a pinch. This one used to raise.
    ('double spiral', 'N N4 W4 S3 E3 N2 W2 U2 E2 N3 W3 S4 E4 E', None),
    ('metre spring', 'walks/metre_spring.txt', None),
    # a folded run that doubles back twice inside a 4x4 cross-section, cut
    # short at both ends to leave room for the mouthpiece and the bell. Four
    # of its six sections come out as one of two shapes, so it is the set's
    # check that duplicates still get their own section number engraved.
    ('trumpet final youtube candidate',
     'walks/trumpet_final_youtube_candidate.txt',
     '../trumpet-final-youtube-candidate/25mm/bore'),
    # the same walk on a 16mm block - 10mm of air inside 3mm walls, where the
    # 31mm sibling above gives 25. The only design here not cut at the stock
    # pitch, so it is the one thing keeping --blocksize honest: everything
    # scaled with the block except SnakeBox's 12mm tab, which does not fit a
    # 10mm frame. Its folder is named for the bore, not the block, so it reads
    # against bore-25mm rather than against 16.
    ('trumpet final youtube candidate, 10mm',
     'walks/trumpet_final_youtube_candidate.txt',
     '../trumpet-final-youtube-candidate/10mm/bore', 16),
    # The elbow-free walks. Every design above either contains elbows or is too
    # small to be interesting, so nothing was checking that a long walk still
    # splits without one - the property every build is chosen for.
    # 190 blocks and 27 pieces, no elbows: the open Hilbert knot is the largest
    # elbow-free walk here by a factor of three, and gates 1010 checks.
    ('hilbert open', 'walks/hilbert_open.txt', '../../test/hilbert_open'),
    # a telescope whose legs grow 4, 5, 6 ... so every turn is a fold and the
    # risers between loops are the only thing leaving the plane
    ('wide telescope', 'walks/wide_telescope.txt', '../../test/wide_telescope'),
    # two-piece walks that turn: the smallest cases where a bend has to carry
    # its corner internally rather than strand it
    ('three block turn', 'walks/three_block_turn.txt', None),
    ('hook check', 'walks/hook_check.txt', None),
]


def walk_of(spec, here):
    """A design is a walk, or the name of a file holding one."""
    if spec.endswith('.txt'):
        return open(os.path.join(here, spec)).read().strip()
    return spec


def main(pattern=None):
    here = os.path.dirname(os.path.abspath(__file__))
    bad = 0
    for name, walk, folder, *rest in DESIGNS:
        if pattern and pattern.lower() not in name.lower():
            continue
        args = [sys.executable, 'check.py', walk_of(walk, here)]
        if folder and os.path.isdir(os.path.join(here, folder)):
            args += ['--files', folder]
        # a fourth field is the block pitch, for the designs not cut at 31
        if rest:
            args += [f'--blocksize={rest[0]}']
        r = subprocess.run(args, cwd=here, capture_output=True, text=True)
        last = (r.stdout.strip().splitlines() or ['no output'])[-1]
        ok = r.returncode == 0 and '0 failed' in last
        bad += not ok
        print(f'  {"pass" if ok else "FAIL"}  {name:<16} {last}')
        if not ok:
            for line in r.stdout.splitlines():
                if 'FAIL' in line or line.startswith('      '):
                    print(f'          {line.strip()}')
            if r.stderr.strip():
                print(f'          {r.stderr.strip().splitlines()[-1]}')
    print(f'\n  {bad} design(s) failing' if bad else '\n  all designs pass')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
