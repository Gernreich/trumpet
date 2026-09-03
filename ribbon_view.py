#!/usr/bin/env python3
"""An interactive view of a ribbon bore: drag to turn.

    python3 ribbon_view.py                       # the coupon
    python3 ribbon_view.py --shape=serpentine    # and so on, same flags

Writes one self-contained HTML page beside the cut files it belongs to, so a
design folder holds the thing you cut and the thing you turn around, and they
cannot drift apart.

It draws the AIRWAY, not the parts - the passage the air actually takes,
bounded by the wall faces at +-bore/2 and the cheeks at +-bore/2. That is
deliberate: the section this repository is about is a property of the airway,
and a picture of the plywood would not show it. The bore came out 3mm narrow
for a week because nothing drew the space inside it.

Nothing here gates anything. check the cut files with ribbon_bore.py; this is
for looking.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ribbon_bore as B                                        # noqa: E402


def wheel(n):
    """n colours around the hue circle, kept clear of each other."""
    out = []
    for i in range(max(n, 1)):
        h = (i * 360.0 / max(n, 1) + 15) % 360
        c, x = 0.62, 0.62 * (1 - abs((h / 60) % 2 - 1))
        r, g, b = [(c, x, 0), (x, c, 0), (0, c, x),
                   (0, x, c), (x, 0, c), (c, 0, x)][int(h // 60) % 6]
        m = 0.30
        out.append('#%02x%02x%02x' % (int((r + m) * 255), int((g + m) * 255),
                                      int((b + m) * 255)))
    return out


def data_for():
    """Vertices and quads for the airway, plus what each face is."""
    c = B.centreline()
    # the airway's own boundary: the wall FACES, at +-bore/2. Not wall_off(),
    # which is where the walls' centrelines sit.
    a = B.offset(c, B.BORE / 2)
    d = B.offset(c, -B.BORE / 2)
    if sum(B.seglen(p, q) for p, q in zip(a, a[1:])) > \
       sum(B.seglen(p, q) for p, q in zip(d, d[1:])):
        a, d = d, a                       # a is the inner wall
    h = B.BORE / 2

    V, Q = [], []
    for i in range(len(c)):
        V += [[a[i][0], a[i][1], -h], [a[i][0], a[i][1], h],
              [d[i][0], d[i][1], h], [d[i][0], d[i][1], -h]]
    for i in range(len(c) - 1):
        p, q = 4 * i, 4 * (i + 1)
        Q.append({'v': [p + 0, p + 1, q + 1, q + 0], 'f': 0, 's': i})   # inner
        Q.append({'v': [p + 3, q + 3, q + 2, p + 2], 'f': 1, 's': i})   # outer
        Q.append({'v': [p + 1, p + 2, q + 2, q + 1], 'f': 2, 's': i})   # top
        Q.append({'v': [p + 0, q + 0, q + 3, p + 3], 'f': 3, 's': i})   # bottom
    n = len(c) - 1
    Q.append({'v': [0, 1, 2, 3], 'f': 4, 's': 0})                       # mouth
    Q.append({'v': [4*n+3, 4*n+2, 4*n+1, 4*n+0], 'f': 5, 's': n - 1})   # far end

    R = B.LOBE_R if B.SHAPE == 'serpentine' else B.RADIUS
    return {
        'V': [[round(v, 3) for v in p] for p in V],
        'Q': Q,
        'bore': B.BORE,
        'mm': round(sum(B.seglen(p, q) for p, q in zip(c, c[1:])), 1),
        'facet': B.FACET,
        'shape': B.SHAPE,
        'R': R,
        'segs': n,
        'over': round(100 * (1 / math.cos(math.radians(B.FACET) / 2) - 1), 2),
        'pal': wheel(n),
        'faces': ['inner wall', 'outer wall', 'top cheek', 'bottom cheek',
                  'mouth', 'far end'],
        'facecol': ['#5aa9e6', '#3d7ebd', '#c9d6e3', '#8fa3b8',
                    '#1c1c20', '#e0457b'],
    }


HTML = r'''<title>__TITLE__</title>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{color-scheme:dark;--bg:#14161a;--ink:#e8eaed;--dim:#9aa3ad;--line:#2a2f36;
      --panel:#1b1e24;--accent:#e0457b}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
     font:14px/1.5 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
header{padding:14px 18px 10px;border-bottom:1px solid var(--line)}
h1{margin:0;font-size:17px;font-weight:650;letter-spacing:-.01em}
.sub{color:var(--dim);font-size:13px;margin-top:3px}
.sub b{color:var(--ink);font-weight:600}
main{display:grid;grid-template-columns:1fr 220px;gap:0;height:calc(100vh - 62px);
     min-height:420px}
#wrap{position:relative;overflow:hidden}
canvas{display:block;width:100%;height:100%;cursor:grab;touch-action:none}
canvas.drag{cursor:grabbing}
aside{border-left:1px solid var(--line);padding:14px;overflow:auto;background:var(--panel)}
h2{margin:0 0 8px;font-size:11px;letter-spacing:.09em;text-transform:uppercase;
   color:var(--dim);font-weight:600}
.grp{margin-bottom:18px}
button{font:inherit;color:var(--ink);background:#232830;border:1px solid var(--line);
       border-radius:6px;padding:5px 9px;cursor:pointer;margin:0 4px 4px 0}
button[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:#fff}
button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
input[type=range]{width:100%;accent-color:var(--accent)}
.key{display:flex;align-items:center;gap:7px;margin:3px 0;font-size:12.5px}
/* the mouth's swatch is near-black on a near-black panel, so every swatch
   gets an outline rather than that one getting a special case */
.sw{width:12px;height:12px;border-radius:3px;flex:0 0 auto;
    box-shadow:inset 0 0 0 1px rgba(255,255,255,.35)}
.hint{color:var(--dim);font-size:12px;margin-top:10px}
dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:2px 10px;font-size:12.5px}
dt{color:var(--dim)}dd{margin:0;text-align:right;font-variant-numeric:tabular-nums}
@media (max-width:720px){main{grid-template-columns:1fr;height:auto}
  #wrap{height:56vh}aside{border-left:0;border-top:1px solid var(--line)}}
</style>
<header>
  <h1>__TITLE__</h1>
  <div class="sub" id="sub"></div>
</header>
<main>
  <div id="wrap"><canvas id="c"></canvas></div>
  <aside>
    <div class="grp"><h2>Colour</h2>
      <button id="m-face" aria-pressed="true">by face</button>
      <button id="m-sec" aria-pressed="false">by facet</button>
    </div>
    <div class="grp"><h2>Reveal</h2>
      <input id="rev" type="range" min="1" max="1" value="1">
      <div class="hint" id="revn"></div>
    </div>
    <div class="grp"><h2>Key</h2><div id="key"></div></div>
    <div class="grp"><h2>Numbers</h2><dl id="nums"></dl></div>
    <div class="hint">Drag to turn. Scroll to zoom. Double-click to reset.</div>
  </aside>
</main>
<script>
const D = __DATA__;
const cv = document.getElementById('c'), cx = cv.getContext('2d');
let yaw = -0.62, pitch = -0.42, zoom = 1, mode = 'face', reveal = D.segs;

/* --- the model, centred on its own middle so rotation feels right --- */
const C = (() => {
  let lo = [1e9,1e9,1e9], hi = [-1e9,-1e9,-1e9];
  for (const v of D.V) for (let i=0;i<3;i++){ lo[i]=Math.min(lo[i],v[i]); hi[i]=Math.max(hi[i],v[i]); }
  return [(lo[0]+hi[0])/2,(lo[1]+hi[1])/2,(lo[2]+hi[2])/2];
})();
function rot(p){
  const x=p[0]-C[0], y=p[1]-C[1], z=p[2]-C[2];
  const cy=Math.cos(yaw), sy=Math.sin(yaw);
  const x1=x*cy - z*sy, z1=x*sy + z*cy;
  const cp=Math.cos(pitch), sp=Math.sin(pitch);
  return [x1, y*cp - z1*sp, y*sp + z1*cp];
}
/* extent at this angle, so the fit does not jump as it turns */
function span(){
  let lo=[1e9,1e9], hi=[-1e9,-1e9];
  for (const v of D.V){ const r=rot(v);
    for (let i=0;i<2;i++){ lo[i]=Math.min(lo[i],r[i]); hi[i]=Math.max(hi[i],r[i]); } }
  return [hi[0]-lo[0], hi[1]-lo[1], (lo[0]+hi[0])/2, (lo[1]+hi[1])/2];
}
function draw(){
  const dpr = Math.min(devicePixelRatio||1, 2);
  const w = cv.clientWidth, h = cv.clientHeight;
  cv.width = w*dpr; cv.height = h*dpr;
  cx.setTransform(dpr,0,0,dpr,0,0);
  cx.clearRect(0,0,w,h);
  const [sw,sh,mx,my] = span();
  const s = Math.min(w/(sw||1), h/(sh||1)) * 0.86 * zoom;
  const P = p => { const r = rot(p);
    return [w/2 + (r[0]-mx)*s, h/2 + (r[1]-my)*s, r[2]]; };

  const items = [];
  for (const q of D.Q){
    if (q.f < 4 && q.s >= reveal) continue;
    if (q.f === 5 && reveal < D.segs) continue;
    const pts = q.v.map(i => P(D.V[i]));
    const z = pts.reduce((a,p)=>a+p[2],0)/pts.length;
    /* facing, from the projected winding: a back face winds the other way */
    let area = 0;
    for (let i=0;i<pts.length;i++){ const a=pts[i], b=pts[(i+1)%pts.length];
      area += a[0]*b[1] - b[0]*a[1]; }
    items.push({q, pts, z, front: area < 0});
  }
  items.sort((a,b) => a.z - b.z);          /* painter: far first */

  for (const it of items){
    const q = it.q;
    let col = mode === 'face' ? D.facecol[q.f]
            : (q.f >= 4 ? D.facecol[q.f] : D.pal[q.s % D.pal.length]);
    /* one flat light, so the form reads; back faces sit darker */
    const k = it.front ? 1 : 0.55;
    cx.fillStyle = shade(col, k * (q.f===2?1.06:q.f===3?0.72:q.f===0?0.86:0.95));
    cx.beginPath();
    cx.moveTo(it.pts[0][0], it.pts[0][1]);
    for (let i=1;i<it.pts.length;i++) cx.lineTo(it.pts[i][0], it.pts[i][1]);
    cx.closePath(); cx.fill();
    cx.strokeStyle = 'rgba(0,0,0,.30)'; cx.lineWidth = 0.6; cx.stroke();
  }
}
function shade(hex, k){
  const n = parseInt(hex.slice(1),16);
  const f = v => Math.max(0, Math.min(255, Math.round(v*k)));
  return `rgb(${f(n>>16&255)},${f(n>>8&255)},${f(n&255)})`;
}

/* --- controls --- */
let drag = null;
cv.addEventListener('pointerdown', e => {
  drag = [e.clientX, e.clientY]; cv.classList.add('drag');
  cv.setPointerCapture(e.pointerId);
});
cv.addEventListener('pointermove', e => {
  if (!drag) return;
  yaw += (e.clientX - drag[0]) * 0.008;
  pitch += (e.clientY - drag[1]) * 0.008;
  pitch = Math.max(-1.5, Math.min(1.5, pitch));
  drag = [e.clientX, e.clientY]; draw();
});
for (const ev of ['pointerup','pointercancel'])
  cv.addEventListener(ev, () => { drag = null; cv.classList.remove('drag'); });
cv.addEventListener('wheel', e => {
  e.preventDefault();
  zoom = Math.max(0.35, Math.min(6, zoom * (e.deltaY < 0 ? 1.1 : 1/1.1)));
  draw();
}, {passive:false});
cv.addEventListener('dblclick', () => {
  yaw = -0.62; pitch = -0.42; zoom = 1; draw();
});

const $ = id => document.getElementById(id);
function setMode(m){
  mode = m;
  $('m-face').setAttribute('aria-pressed', m === 'face');
  $('m-sec').setAttribute('aria-pressed', m === 'sec');
  key(); draw();
}
$('m-face').onclick = () => setMode('face');
$('m-sec').onclick = () => setMode('sec');

const rev = $('rev');
rev.max = D.segs; rev.value = D.segs;
rev.oninput = () => { reveal = +rev.value; revn(); draw(); };
function revn(){
  $('revn').textContent = reveal + ' of ' + D.segs + ' facets'
    + (reveal < D.segs ? '' : '  (all)');
}

function key(){
  const k = $('key');
  k.innerHTML = '';
  const rows = mode === 'face'
    ? D.faces.map((n,i) => [D.facecol[i], n])
    : [[D.facecol[4],'mouth'], [D.facecol[5],'far end'],
       [D.pal[0], 'facet 1'], [D.pal[Math.floor(D.segs/2) % D.pal.length],
        'facet ' + (Math.floor(D.segs/2)+1)],
       [D.pal[(D.segs-1) % D.pal.length], 'facet ' + D.segs]];
  for (const [c,n] of rows){
    const d = document.createElement('div'); d.className = 'key';
    d.innerHTML = `<span class="sw" style="background:${c}"></span><span>${n}</span>`;
    k.appendChild(d);
  }
}

$('sub').innerHTML = `<b>${D.bore} \u00d7 ${D.bore}mm</b> section, `
  + `<b>${D.mm}mm</b> of centreline, ${D.segs} facets of ${D.facet}\u00b0 `
  + `\u2014 exact along every facet, <b>+${D.over}%</b> at each mitre`;
$('nums').innerHTML = [
  ['shape', D.shape], ['bore', D.bore + ' \u00d7 ' + D.bore + 'mm'],
  ['section', (D.bore*D.bore) + 'mm\u00b2'],
  ['centreline', D.mm + 'mm'], ['bend radius', D.R + 'mm'],
  ['R / bore', (D.R/D.bore).toFixed(1)],
  ['facet', D.facet + '\u00b0'], ['area at a mitre', '+' + D.over + '%'],
].map(([a,b]) => `<dt>${a}</dt><dd>${b}</dd>`).join('');

key(); revn();
addEventListener('resize', draw);
draw();
</script>
'''


def build(title):
    d = data_for()
    return (HTML.replace('__TITLE__', title)
                .replace('__DATA__', json.dumps(d, separators=(',', ':'))))


def main():
    a = sys.argv[1:]
    for flag, cast in (('shape', str), ('bore', float), ('facet', float),
                       ('radius', float), ('lobes', int), ('lobe-r', float),
                       ('rise', float), ('lead', float), ('web', float)):
        hit = [x for x in a if x.startswith(f'--{flag}=')]
        if not hit:
            continue
        name = {'shape': 'SHAPE', 'bore': 'BORE', 'facet': 'FACET',
                'radius': 'RADIUS', 'lobes': 'LOBES', 'lobe-r': 'LOBE_R',
                'rise': 'RISE', 'lead': 'LEAD', 'web': 'WEB'}[flag]
        setattr(B, name, cast(hit[0].split('=', 1)[1]))

    here = os.path.dirname(os.path.abspath(__file__))
    if B.SHAPE == 'serpentine':
        stem = (f'ribbon-serpentine-bore{B.BORE:g}-{B.FACET:g}deg-'
                f'{B.LOBES}lobes-R{B.LOBE_R:.0f}')
        title = (f'Ribbon Serpentine, {B.BORE:g}mm Bore')
    else:
        stem = f'ribbon-coupon-bore{B.BORE:g}-{B.FACET:g}deg-R{B.RADIUS:g}'
        title = f'Ribbon Coupon, {B.BORE:g}mm Bore'
    out = [x for x in a if x.startswith('--out=')]
    path = out[0].split('=', 1)[1] if out else os.path.join(here, stem + '.html')
    open(path, 'w').write(build(title))
    d = data_for()
    print(f'  {os.path.basename(path):<52}drag to turn, colour by face '
          f'or facet')
    print(f'  {"":52}{d["mm"]}mm, {d["segs"]} facets, '
          f'{len(d["Q"])} quads')
    return 0


if __name__ == '__main__':
    sys.exit(main())
