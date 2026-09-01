#!/usr/bin/env python3
"""Run the pre-cut gate over every design in this repository.

    python3 regress.py            # every design
    python3 regress.py coil       # those whose name matches

The frozen corpus in ../../bore-generator gates the frozen toolchain and knows
nothing about this fork: it has no stretched lattice in it, so it cannot catch a
change to `bore_split.py` here. Each design is otherwise gated only when it is
written, which means a change to tools/ is proved against whichever design you
happened to rebuild and no other. This runs both.

Every design carries the switches it is cut with. Passing the wrong ones gates a
design nobody is cutting -- --files never looks at the pitch, so it will not
notice.
"""
import os
import subprocess
import sys

# (name, walk file, folder of cut files, switches it is cut with)
DESIGNS = [
    # The original test: the trumpet candidate's walk on a stretched lattice.
    # Parts are cut from this one, so a change that moves it needs asking about.
    ('stretched test', 'walks/stretched_test.txt', '../bore',
     ['--bore=10', '--straight=30']),
    # WUED repeated with an N spacer every three terms: a square circuit in
    # cross-section that steps north. The first walk laid out for this lattice.
    ('coil', 'walks/coil.txt', '../coil',
     ['--bore=10', '--straight=30']),
]


def main(pattern=None):
    here = os.path.dirname(os.path.abspath(__file__))
    bad = 0
    for name, walk, folder, switches in DESIGNS:
        if pattern and pattern.lower() not in name.lower():
            continue
        text = open(os.path.join(here, walk)).read().strip()
        args = [sys.executable, 'check.py', text] + switches
        if folder and os.path.isdir(os.path.join(here, folder)):
            args += ['--files', folder]
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
