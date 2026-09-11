#!/usr/bin/env python3
"""
Generates dark.svg / light.svg — the profile README hero banner.

A terminal window whose left panel cycles through six modules, 5s each,
looping forever. The right column (SYSTEM.INFO + PIPELINE) stays visible
the whole time so your stack is always readable.

  scene 1  NEURAL.NET       feed-forward net, signal sweep      [green]
  scene 2  OPTIMIZER.TRACE  contour map + feature weights       [amber]
  scene 3  NEURON.SPIKE     biological neuron firing            [magenta]
  scene 4  STACK.MATRIX     tooling grid, scanned in sequence   [violet]
  scene 5  RUNTIME.PYTHON   particle logo, swirl assembly       [blue]
  scene 6  TRAINING.LOG     streaming run log                   [cyan]

Plain SVG + SMIL. No external fonts, no raster images, no build step.
Edit the DATA block below and re-run:

    python generate_banner.py
"""

import math
import random

# ---------------------------------------------------------------- data

HANDLE = "codewithvikas96-ui"

INFO = [
    ("Subject",       "Vikas Vishwakarma",                             "value"),
    ("Role",          "AI / ML Engineer in Training",                  "cyan"),
    ("Origin",        "India · IST (UTC+5:30)",                        "text"),
    ("Status",        "Shipping ML projects · Learning Deep Learning", "green"),
    ("Focus",         "Python → Data Science → ML → AI",               "text"),
    ("Core.Lang",     "Python, C, C++, Java, JavaScript, TypeScript",  "text"),
    ("Data.Stack",    "NumPy, Pandas, Matplotlib, Seaborn, Jupyter",   "text"),
    ("ML.Stack",      "scikit-learn, XGBoost, LightGBM, CatBoost",     "text"),
    ("ML.Methods",    "Regression, Ensembles, Clustering, PCA",        "text"),
    ("AI.Loading",    "Deep Learning, NLP, Generative AI, Agents",     "amber"),
    ("Core.Backend",  "Node.js, Express, Supabase Edge Functions",     "text"),
    ("Core.Database", "PostgreSQL, MySQL, MongoDB, Oracle PL/SQL",     "text"),
    ("Core.Mobile",   "React Native, Expo, TypeScript",                "text"),
    ("Core.Tools",    "Git, GitHub, Jupyter, PyQt5",                   "text"),
    ("Grid.Mail",     "vikas221018@gmail.com",                         "cyan"),
    ("Grid.LinkedIn", "vikas-vishwakarma-62959a387",                   "cyan"),
    ("Grid.GitHub",   HANDLE,                                          "green"),
]

FEATURES = [
    ("page_value", 0.92), ("exit_rate", 0.71), ("session_dur", 0.58),
    ("visitor_type", 0.36), ("month", 0.24),
]

PIPELINE = [
    ("Python", "done"),   ("DataSci", "done"), ("ML", "done"),
    ("DL", "active"),     ("NLP", "active"),   ("GenAI", "queued"),
    ("Agents", "queued"), ("Prod", "queued"),
]

# name, kind (lang|data|ml|tool), state (using|next)
# "next" renders dashed — tools on the roadmap, not claimed as current skills.
STACK = [
    ("Python", "lang", "using"),        ("NumPy", "data", "using"),
    ("Pandas", "data", "using"),        ("Matplotlib", "data", "using"),
    ("Seaborn", "data", "using"),       ("Jupyter", "tool", "using"),
    ("scikit-learn", "ml", "using"),    ("XGBoost", "ml", "using"),
    ("LightGBM", "ml", "using"),        ("CatBoost", "ml", "using"),
    ("PyTorch", "ml", "next"),          ("OpenCV", "ml", "next"),
]

LOG = [
    ("[ ok ]", "loading dataset ... 12,330 rows x 18 cols",      "green"),
    ("[ ok ]", "train/test split 0.80 / 0.20  stratified",       "green"),
    ("[ run]", "fitting GradientBoostingClassifier ...",         "cyan"),
    ("[    ]", "epoch 12/20   loss 0.0684   val_acc 0.921",      "text"),
    ("[    ]", "epoch 16/20   loss 0.0473   val_acc 0.934",      "text"),
    ("[    ]", "epoch 20/20   loss 0.0312   val_acc 0.941",      "text"),
    ("[warn]", "class imbalance detected -> applying weights",   "amber"),
    ("[ ok ]", "grid_search best: max_depth=6  lr=0.05",         "green"),
    ("[ ok ]", "roc_auc 0.947   f1 0.883   recall 0.861",        "green"),
    ("[save]", "model -> artifacts/shopsmart.pkl",               "cyan"),
    ("[next]", "queued: backprop_from_scratch.ipynb",            "magenta"),
]

THEMES = {
    "dark": dict(
        bg="#06080C", panel="#0B0F14", sub="#080B10", band="#0E131A",
        border="#1B2430", text="#7E8A99", value="#E6EDF3", dim="#4E5A68",
        green="#3BE08A", cyan="#2BD3E8", magenta="#FF3D8A",
        amber="#E8A33D", violet="#A06CFF", blue="#4D9EFF",
    ),
    "light": dict(
        bg="#EDF1EE", panel="#FFFFFF", sub="#F7F9F7", band="#F0F3F0",
        border="#D3DAD3", text="#5B6660", value="#10151B", dim="#8C968F",
        green="#1E7D4F", cyan="#0E7490", magenta="#B3246B",
        amber="#B4751A", violet="#6D3DBF", blue="#1D4ED8",
    ),
}

# ------------------------------------------------------------- geometry

W, H = 1180, 640
WIN_X, WIN_Y, WIN_W, WIN_H = 20, 20, 1140, 600
BAR_H = 36
MONO = "ui-monospace, 'JetBrains Mono', 'SF Mono', 'Cascadia Mono', Menlo, Consolas, monospace"

L_X, L_W = 40, 424
R_X, R_W = 488, 652
IX0, IX1 = 56, 448
BOTTOM = 620

HOLD, FADE = 5.0, 0.45
N_SCENES = 6
CYCLE = HOLD * N_SCENES


def adv(size):
    return size * 0.605


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, fill, size=13, anchor="start", ls=None, op=None):
    a = f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}"'
    if anchor != "start":
        a += f' text-anchor="{anchor}"'
    if ls is not None:
        a += f' letter-spacing="{ls}"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + f">{esc(s)}</text>"


def rect(x, y, w, h, fill, stroke=None, rx=0, sw=1, op=None, dash=None):
    a = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke:
        a += f' stroke="{stroke}" stroke-width="{sw}"'
    if dash:
        a += f' stroke-dasharray="{dash}"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + "/>"


def line(x1, y1, x2, y2, stroke, sw=1, op=None):
    a = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + "/>"


def head(y, label, note, accent, t):
    return [
        text(IX0, y, label, accent, size=11, ls=1.7),
        text(IX1, y, note, t["dim"], size=10, anchor="end"),
        line(IX0, y + 10, IX1, y + 10, t["border"], 1),
    ]


def plen(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def poly(pts):
    return " ".join(f"{x},{y}" for x, y in pts)


def travel(pts, color, dur, begin, sw=2.4, dash=14):
    """A short dash that runs along a polyline — a signal travelling."""
    L = plen(pts)
    return (f'<polyline points="{poly(pts)}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" '
            f'stroke-dasharray="{dash} 9999" stroke-dashoffset="0">'
            f'<animate attributeName="stroke-dashoffset" values="{dash};-{L:.0f}" '
            f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></polyline>')


# --------------------------------------------------------- scene timing

def scene_anim(i):
    start, end = i * HOLD, (i + 1) * HOLD
    if i == 0:
        kt = [0, (end - FADE) / CYCLE, end / CYCLE, (CYCLE - FADE) / CYCLE, 1]
        vals = [1, 1, 0, 0, 1]
    else:
        kt = [0, (start - FADE) / CYCLE, start / CYCLE,
              (end - FADE) / CYCLE, end / CYCLE]
        vals = [0, 0, 1, 1, 0]
        if i < N_SCENES - 1:
            kt.append(1)
            vals.append(0)
    return ('<animate attributeName="opacity" '
            f'values="{";".join(str(v) for v in vals)}" '
            f'keyTimes="{";".join(f"{k:.4f}" for k in kt)}" '
            f'dur="{CYCLE:g}s" repeatCount="indefinite"/>')


def reveal(at):
    return ('<animate attributeName="opacity" values="0;1;1" '
            f'keyTimes="0;{at / CYCLE:.4f};1" calcMode="discrete" '
            f'dur="{CYCLE:g}s" repeatCount="indefinite"/>')


def wrap(i, parts):
    return [f'<g opacity="0">{scene_anim(i)}'] + parts + ["</g>"]


# ------------------------------------------------------------- chrome

COMMANDS = [
    "vikas@ml-node:~/profile$ python train.py --watch",
    "vikas@ml-node:~/profile$ python optimize.py --trace",
    "vikas@ml-node:~/profile$ python neuron.py --spike",
    "vikas@ml-node:~/profile$ pip list --format=columns",
    'vikas@ml-node:~/profile$ python -c "import this"',
    "vikas@ml-node:~/profile$ tail -f logs/train.log",
]


def title_bar(t, accents):
    o = [
        rect(WIN_X, WIN_Y, WIN_W, WIN_H, t["panel"], t["border"], rx=10, sw=1.5),
        rect(WIN_X, WIN_Y + BAR_H - 10, WIN_W, 10, t["panel"]),
        line(WIN_X, WIN_Y + BAR_H, WIN_X + WIN_W, WIN_Y + BAR_H, t["border"], 1),
    ]
    for i, c in enumerate(("#FF5F56", "#FFBD2E", "#27C93F")):
        o.append(f'<circle cx="{42 + i * 20}" cy="38" r="6" fill="{c}"/>')

    for i, cmd in enumerate(COMMANDS):
        cx = round(575 - len(cmd) * adv(13) / 2, 1)
        caret = round(cx + len(cmd) * adv(13) + 3, 1)
        o += wrap(i, [
            text(cx, 43, cmd, t["text"], size=13),
            f'<rect x="{caret}" y="31" width="8" height="14" fill="{accents[i]}">'
            f'<animate attributeName="opacity" values="1;0" dur="1.1s" '
            f'calcMode="discrete" repeatCount="indefinite"/></rect>',
        ])

    for i in range(N_SCENES):
        x = 912 + i * 14
        o.append(f'<circle cx="{x}" cy="38" r="3.5" fill="none" '
                 f'stroke="{t["border"]}" stroke-width="1.2"/>')
        o += wrap(i, [f'<circle cx="{x}" cy="38" r="3.5" fill="{accents[i]}"/>'])

    o.append(text(1140, 42, HANDLE, t["green"], size=12, anchor="end"))

    o.append('<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{t["green"]}"/>'
             f'<stop offset="30%" stop-color="{t["cyan"]}"/>'
             f'<stop offset="60%" stop-color="{t["magenta"]}"/>'
             f'<stop offset="82%" stop-color="{t["violet"]}"/>'
             f'<stop offset="100%" stop-color="{t["amber"]}"/></linearGradient>')
    o.append(rect(WIN_X, WIN_Y + BAR_H, WIN_W, 1.5, "url(#accent)", op=0.7))
    return o


# -------------------------------------------------------------- scenes

def scene_network(t):
    a = t["green"]
    o = head(96, "NEURAL.NET", "forward pass", a, t)

    layers, xs = [4, 6, 6, 3], [116, 212, 308, 404]
    cols = [t["green"], t["cyan"], t["cyan"], t["green"]]
    cy, gap = 246, 38
    pos = [[(x, cy + (i - (n - 1) / 2) * gap) for i in range(n)]
           for n, x in zip(layers, xs)]

    for li in range(len(pos) - 1):
        for ai, (x1, y1) in enumerate(pos[li]):
            for bi, (x2, y2) in enumerate(pos[li + 1]):
                o.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="{cols[li]}" stroke-width="0.9" opacity="0.1">'
                    f'<animate attributeName="opacity" values="0.07;0.4;0.07" '
                    f'dur="3.2s" begin="{round(li * .5 + (ai + bi) * .055, 3)}s" '
                    f'repeatCount="indefinite"/></line>')

    for li, layer in enumerate(pos):
        for i, (x, y) in enumerate(layer):
            o.append(
                f'<circle cx="{x}" cy="{y}" r="7" fill="{t["sub"]}" '
                f'stroke="{cols[li]}" stroke-width="1.5">'
                f'<animate attributeName="r" values="7;8.4;7" dur="3.2s" '
                f'begin="{round(li * .5 + i * .09, 3)}s" repeatCount="indefinite"/>'
                f'</circle>')

    for x, lbl in zip(xs, ("input", "h₁", "h₂", "out")):
        o.append(text(x, 376, lbl, t["dim"], size=9.5, anchor="middle"))

    o += head(410, "TRAINING.LOSS", "epoch 120 / 120", a, t)
    px, py, pw, ph = IX0, 432, IX1 - IX0, 134
    o.append(rect(px, py, pw, ph, t["band"], rx=4, op=0.6))
    for i in range(1, 4):
        o.append(line(px, py + ph * i / 4, px + pw, py + ph * i / 4,
                      t["border"], 1, op=0.7))

    pts, n = [], 64
    for i in range(n):
        u = i / (n - 1)
        v = math.exp(-2.4 * u) * (1 + .09 * math.sin(u * 27) + .05 * math.sin(u * 11 + 1.3))
        pts.append((round(px + 6 + u * (pw - 12), 2),
                    round(py + 10 + (1 - min(v, 1.0)) * (ph - 22), 2)))
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    length = plen(pts)

    o.append(f'<path d="{d} L {pts[-1][0]} {py + ph} L {pts[0][0]} {py + ph} Z" '
             f'fill="{a}" opacity="0.07"/>')
    o.append(f'<path d="{d}" fill="none" stroke="{a}" stroke-width="2" '
             f'stroke-linecap="round" stroke-linejoin="round" '
             f'stroke-dasharray="{length:.0f}" stroke-dashoffset="{length:.0f}">'
             f'<animate attributeName="stroke-dashoffset" '
             f'values="{length:.0f};0;0" keyTimes="0;0.75;1" dur="6s" '
             f'repeatCount="indefinite"/></path>')
    o.append(line(px, py + ph, px + pw, py + ph, t["border"], 1))
    o.append(text(px, 588, "loss  0.0312 ↓", a, size=10))
    o.append(text(px + pw, 588, "val_acc  0.94", t["dim"], size=10, anchor="end"))
    return o


def scene_optimizer(t):
    a = t["amber"]
    o = head(96, "OPTIMIZER.TRACE", "lr 0.05 · 9 steps", a, t)
    px, py, pw, ph = IX0, 118, IX1 - IX0, 228
    o.append(rect(px, py, pw, ph, t["band"], t["border"], rx=6, op=0.7))

    o.append(f'<clipPath id="pbox"><rect x="{px}" y="{py}" width="{pw}" '
             f'height="{ph}" rx="6"/></clipPath><g clip-path="url(#pbox)">')
    mx, my = 310, 282
    for i, (rx_, ry_) in enumerate(((24, 16), (52, 34), (82, 54), (116, 76), (154, 102))):
        o.append(f'<ellipse cx="{mx}" cy="{my}" rx="{rx_}" ry="{ry_}" fill="none" '
                 f'stroke="{t["dim"]}" stroke-width="1" '
                 f'opacity="{round(0.5 - i * 0.07, 2)}" '
                 f'transform="rotate(-22 {mx} {my})"/>')
    o.append("</g>")

    sx, sy = 108, 160
    pts = []
    for i in range(10):
        dec = math.exp(-0.45 * i)
        wob = 7 * math.exp(-0.3 * i) * (1 if i % 2 else -1)
        pts.append((round(mx + (sx - mx) * dec + wob, 1),
                    round(my + (sy - my) * dec - wob * 0.5, 1)))

    o.append(f'<polyline points="{poly(pts)}" fill="none" stroke="{a}" '
             f'stroke-width="1.4" opacity="0.5" stroke-linejoin="round"/>')
    for x, y in pts:
        o.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{t["sub"]}" '
                 f'stroke="{a}" stroke-width="1.2" opacity="0.75"/>')
    o.append(f'<circle cx="{mx}" cy="{my}" r="4" fill="{t["green"]}"/>')
    o.append(text(mx + 10, my + 4, "min", t["green"], size=9.5))

    o.append(f'<circle r="5.5" fill="{a}" cx="{pts[0][0]}" cy="{pts[0][1]}">'
             f'<animate attributeName="cx" values="{";".join(str(p[0]) for p in pts)}" '
             f'dur="4.5s" calcMode="discrete" repeatCount="indefinite"/>'
             f'<animate attributeName="cy" values="{";".join(str(p[1]) for p in pts)}" '
             f'dur="4.5s" calcMode="discrete" repeatCount="indefinite"/></circle>')
    o.append(text(px + 10, py + ph - 10, "∇ gradient descent", t["dim"], size=9.5))

    o += head(378, "FEATURE.WEIGHTS", "gain, normalised", a, t)
    x0, maxw = 152, 258
    for i, (label, weight) in enumerate(FEATURES):
        y = 402 + i * 30
        w = round(maxw * weight, 1)
        o.append(text(IX0, y + 9, label, t["text"], size=11))
        o.append(rect(x0, y, maxw, 10, t["band"], rx=5))
        o.append(f'<rect x="{x0}" y="{y}" width="0" height="10" rx="5" fill="{a}">'
                 f'<animate attributeName="width" values="0;{w};{w};0" '
                 f'keyTimes="0;0.42;0.88;1" dur="5.5s" '
                 f'begin="{round(i * .16, 2)}s" repeatCount="indefinite"/></rect>')
        o.append(text(x0 + w + 8, y + 9, f"{weight:.2f}", t["dim"], size=10))
    return o


def scene_neuron(t):
    """Scene 3 — a biological neuron fires: dendrites -> soma -> axon -> synapse."""
    a = t["magenta"]
    o = head(96, "NEURON.SPIKE", "membrane potential", a, t)

    cycle = 2.6
    dend = [
        [(62, 152), (98, 178), (128, 208), (152, 236)],
        [(58, 216), (94, 228), (126, 238), (150, 246)],
        [(64, 302), (98, 294), (128, 278), (152, 262)],
        [(76, 356), (106, 330), (132, 304), (153, 272)],
        [(122, 140), (136, 180), (147, 214), (154, 240)],
    ]
    axon = [(212, 252), (250, 262), (290, 282), (330, 300), (366, 314), (398, 322)]
    terms = [[(398, 322), (424, 302)], [(398, 322), (430, 326)], [(398, 322), (418, 348)]]

    for pts in dend:
        o.append(f'<polyline points="{poly(pts)}" fill="none" stroke="{t["border"]}" '
                 f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(f'<circle cx="{pts[0][0]}" cy="{pts[0][1]}" r="3" fill="{t["border"]}"/>')

    # myelinated axon: solid core, dashed sheath on top
    o.append(f'<polyline points="{poly(axon)}" fill="none" stroke="{t["border"]}" '
             f'stroke-width="9" stroke-linecap="round" stroke-linejoin="round" '
             f'opacity="0.55"/>')
    o.append(f'<polyline points="{poly(axon)}" fill="none" stroke="{t["sub"]}" '
             f'stroke-width="9" stroke-linecap="butt" stroke-linejoin="round" '
             f'stroke-dasharray="3 17"/>')
    o.append(f'<polyline points="{poly(axon)}" fill="none" stroke="{t["border"]}" '
             f'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    for pts in terms:
        o.append(f'<polyline points="{poly(pts)}" fill="none" stroke="{t["border"]}" '
                 f'stroke-width="2.4" stroke-linecap="round"/>')

    # travelling signals
    for i, pts in enumerate(dend):
        o.append(travel(pts, a, cycle, round(i * 0.09, 2)))

    o.append(f'<ellipse cx="180" cy="250" rx="32" ry="28" fill="{t["sub"]}" '
             f'stroke="{t["border"]}" stroke-width="2"/>')
    o.append(f'<ellipse cx="180" cy="250" rx="32" ry="28" fill="{a}" opacity="0">'
             f'<animate attributeName="opacity" values="0;0.32;0" '
             f'keyTimes="0;0.42;0.62" dur="{cycle}s" repeatCount="indefinite"/></ellipse>')
    o.append(f'<ellipse cx="180" cy="250" rx="32" ry="28" fill="none" stroke="{a}" '
             f'stroke-width="2" opacity="0.25">'
             f'<animate attributeName="opacity" values="0.25;1;0.25" '
             f'keyTimes="0;0.45;0.7" dur="{cycle}s" repeatCount="indefinite"/></ellipse>')
    o.append(f'<circle cx="180" cy="250" r="10" fill="none" stroke="{t["dim"]}" '
             f'stroke-width="1.5"/>')

    o.append(travel(axon, a, cycle, round(cycle * 0.46, 2), sw=3, dash=18))
    for i, pts in enumerate(terms):
        o.append(travel(pts, a, cycle, round(cycle * 0.78, 2), sw=2.4, dash=10))
        ex, ey = pts[1]
        o.append(f'<circle cx="{ex}" cy="{ey}" r="4.5" fill="{t["sub"]}" '
                 f'stroke="{t["border"]}" stroke-width="1.5"/>')
        o.append(f'<circle cx="{ex}" cy="{ey}" r="4.5" fill="{a}" opacity="0">'
                 f'<animate attributeName="opacity" values="0;1;0" '
                 f'keyTimes="0;0.9;1" dur="{cycle}s" begin="{round(i * .05, 2)}s" '
                 f'repeatCount="indefinite"/></circle>')

    o.append(text(60, 382, "dendrites", t["dim"], size=9.5))
    o.append(text(180, 300, "soma", t["dim"], size=9.5, anchor="middle"))
    o.append(text(272, 264, "axon", t["dim"], size=9.5))
    o.append(text(IX1, 372, "synapse", t["dim"], size=9.5, anchor="end"))

    # spike train
    o += head(420, "SPIKE.TRAIN", "28 ms window", a, t)
    base, x = 542, IX0 + 4
    for i in range(28):
        h = 10 + 34 * abs(math.sin(i * 1.9) * math.cos(i * 0.7))
        o.append(f'<rect x="{round(x, 1)}" y="{round(base - h, 1)}" width="3" '
                 f'height="{round(h, 1)}" rx="1.5" fill="{a}" opacity="0.15">'
                 f'<animate attributeName="opacity" values="0.15;1;1;0.15" '
                 f'keyTimes="0;0.06;0.8;1" dur="{cycle}s" '
                 f'begin="{round(i * 0.07, 2)}s" repeatCount="indefinite"/></rect>')
        x += 13.8
    o.append(line(IX0, base, IX1, base, t["border"], 1))
    o.append(text(IX0, 570, "threshold -55 mV · resting -70 mV", t["dim"], size=9.5))
    return o


def scene_stack(t):
    """Scene 4 — the tooling grid, scanned tile by tile."""
    a = t["violet"]
    o = head(96, "STACK.MATRIX", f"{len(STACK)} tools", a, t)

    kind_col = {"lang": t["violet"], "data": t["cyan"],
                "ml": t["green"], "tool": t["amber"]}
    tw, th, gap, cols = 124, 76, 12, 3

    for i, (name, kind, state) in enumerate(STACK):
        c, r = i % cols, i // cols
        x = IX0 + c * (tw + gap)
        y = 130 + r * (th + gap)
        col = kind_col[kind]
        nxt = state == "next"

        o.append(rect(x, y, tw, th, t["band"],
                      t["border"] if not nxt else t["dim"],
                      rx=6, op=0.75, dash="4 4" if nxt else None))

        gx, gy = x + tw / 2, y + 30
        if kind == "lang":
            g = f'<circle cx="{gx}" cy="{gy}" r="9" fill="none" stroke="{col}" stroke-width="2"/>'
        elif kind == "data":
            g = (f'<rect x="{gx - 8}" y="{gy - 8}" width="16" height="16" rx="2" '
                 f'fill="none" stroke="{col}" stroke-width="2"/>')
        elif kind == "ml":
            g = (f'<polygon points="{gx},{gy - 9} {gx + 9},{gy + 7} {gx - 9},{gy + 7}" '
                 f'fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>')
        else:
            g = (f'<polygon points="{gx},{gy - 10} {gx + 9},{gy} {gx},{gy + 10} '
                 f'{gx - 9},{gy}" fill="none" stroke="{col}" stroke-width="2" '
                 f'stroke-linejoin="round"/>')
        o.append(g if not nxt else g.replace('stroke-width="2"', 'stroke-width="2" opacity="0.55"'))

        o.append(text(gx, y + 56, name, t["dim"] if nxt else t["value"],
                      size=10.5, anchor="middle"))
        if nxt:
            o.append(text(gx, y + 69, "next", a, size=8, anchor="middle", ls=0.6))

        o.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="6" '
                 f'fill="none" stroke="{a}" stroke-width="1.6" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0.95;0" '
                 f'keyTimes="0;0.5;1" dur="0.62s" begin="{round(i * 0.3, 2)}s" '
                 f'repeatCount="indefinite"/></rect>')

    ly = 130 + 4 * (th + gap) + 18
    lx = IX0
    for kind, label in (("lang", "language"), ("data", "data"),
                        ("ml", "modelling"), ("tool", "tooling")):
        col = kind_col[kind]
        o.append(f'<circle cx="{lx + 4}" cy="{ly - 4}" r="4" fill="{col}"/>')
        o.append(text(lx + 14, ly, label, t["dim"], size=9.5))
        lx += len(label) * adv(9.5) + 42

    o.append(text(IX0, ly + 24, "solid = in use today", t["text"], size=9.5))
    o.append(text(IX1, ly + 24, "dashed = next on the roadmap", a,
                  size=9.5, anchor="end"))
    return o


def scene_particles(t):
    """Scene 5 — the Python mark, sampled into particles that swirl into place.

    The shape is two interlocking Γ hooks (top bar + left leg, and its 180°
    rotation). Points are tested against that geometry, so there is no bitmap
    and no traced logo file — the mark is computed.
    """
    a = t["blue"]
    o = head(96, "RUNTIME.PYTHON", "particle build", a, t)

    def in_rr(px, py, x0, y0, x1, y1, r):
        dx = max(x0 + r - px, 0.0, px - (x1 - r))
        dy = max(y0 + r - py, 0.0, py - (y1 - r))
        return dx * dx + dy * dy <= r * r

    def in_shape(px, py):
        if not in_rr(px, py, -35, -50, 35, 50, 15):           # outer silhouette
            return False
        if in_rr(px, py, 7, -27, 44, -1, 9):                  # right interlock notch
            return False
        if in_rr(px, py, -44, 1, -7, 27, 9):                  # left  (180° mirror)
            return False
        if (px + 18) ** 2 + (py + 34) ** 2 <= 42.25:          # upper eye
            return False
        if (px - 18) ** 2 + (py - 34) ** 2 <= 42.25:          # lower eye
            return False
        return True

    def piece(px, py):
        if not in_shape(px, py):
            return None
        return "u" if (py <= 1 or (px <= -7 and py <= 27)) else "l"

    def mix(c1, c2, u):
        p = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
        q = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
        return "#" + "".join(f"{round(p[k] + (q[k] - p[k]) * u):02X}" for k in range(3))

    cx0, cy0, s, step = 252, 286, 2.35, 3.1
    rng = random.Random(7)

    dots, yy = [], -53.0
    while yy <= 53.0:
        xx = -39.0
        while xx <= 39.0:
            px = xx + rng.uniform(-1.0, 1.0)
            py = yy + rng.uniform(-1.0, 1.0)
            k = piece(px, py)
            if k:
                dots.append((px, py, k))
            xx += step
        yy += step

    for i, (px, py, k) in enumerate(dots):
        sx, sy = round(cx0 + px * s, 1), round(cy0 + py * s, 1)
        u = min(max((px + 35) / 70, 0.0), 1.0)
        col = mix(t["blue"], t["cyan"], u) if k == "u" \
            else mix(t["violet"], t["magenta"], u)

        edge = not all(piece(px + dx, py + dy)
                       for dx, dy in ((2.6, 0), (-2.6, 0), (0, 2.6), (0, -2.6)))
        r = 1.9 if edge else 1.25
        op = 0.95 if edge else round(0.42 + rng.random() * 0.36, 2)

        th = math.atan2(py, px)
        R = 230 + rng.random() * 110
        S = (f"{cx0 + math.cos(th + 1.5) * R - sx:.0f},"
             f"{cy0 + math.sin(th + 1.5) * R - sy:.0f}")
        M = (f"{cx0 + math.cos(th + 0.7) * R * 0.42 - sx:.0f},"
             f"{cy0 + math.sin(th + 0.7) * R * 0.42 - sy:.0f}")
        d = (i % 14) * 0.0018

        o.append(
            f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="{col}" opacity="{op}">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="{S};{S};{M};0,0;0,0;{S};{S}" '
            f'keyTimes="0;0.6667;{0.708 + d:.4f};{0.738 + d:.4f};0.8;0.8333;1" '
            f'dur="{CYCLE:g}s" repeatCount="indefinite"/></circle>')

    o.append(line(IX0, 452, IX1, 452, t["border"], 1))
    x = IX0
    for label, col in (("core language", t["blue"]),
                       ("4 / 6 projects", t["cyan"]),
                       ("NumPy · Pandas · sklearn", t["dim"])):
        w = len(label) * adv(9.5) + 18
        o.append(rect(x, 470, w, 22, t["band"], t["border"], rx=11))
        o.append(text(x + w / 2, 485, label, col, size=9.5, anchor="middle"))
        x += w + 8

    o.append(text(IX0, 532, f"{len(dots)} particles · assembled from scatter",
                  t["dim"], size=9.5))
    o.append(text(IX0, 588, "import this  →  simple is better than complex",
                  t["dim"], size=9.5))
    return o


def scene_log(t):
    a = t["cyan"]
    o = head(96, "TRAINING.LOG", "tail -f · live", a, t)

    start = (N_SCENES - 1) * HOLD + 0.15
    y = 132
    for i, (tag, msg, tone) in enumerate(LOG):
        at = start + i * 0.27
        o.append(f'<g opacity="0">{reveal(at)}'
                 + text(IX0, y, tag, t[tone] if tone != "text" else t["dim"], size=11)
                 + text(IX0 + 52, y, msg, t[tone], size=11)
                 + "</g>")
        y += 24

    py = y + 6
    o.append(line(IX0, py, IX1, py, t["border"], 1))
    prompt = "vikas@ml-node:~$"
    o.append(text(IX0, py + 24, prompt, t["green"], size=11))
    cx = IX0 + len(prompt) * adv(11) + 6
    o.append(f'<rect x="{cx}" y="{py + 14}" width="7" height="12" fill="{a}">'
             f'<animate attributeName="opacity" values="1;0" dur="1.1s" '
             f'calcMode="discrete" repeatCount="indefinite"/></rect>')
    o.append(text(IX1, py + 24, "run complete · 0 errors", t["dim"],
                  size=9.5, anchor="end"))
    return o


# ------------------------------------------------- persistent right column

def system_info(t):
    o = [
        text(R_X, 96, "SYSTEM.INFO", t["green"], size=11, ls=1.7),
        text(R_X + R_W, 96, f"{len(INFO)} records", t["dim"], size=10, anchor="end"),
        line(R_X, 106, R_X + R_W, 106, t["border"], 1),
    ]
    y, step, size = 126, 22, 13
    for i, (key, val, tone) in enumerate(INFO):
        if i % 2 == 0:
            o.append(rect(R_X, y - 14, R_W, 20, t["band"], rx=3, op=0.7))
        accent = t[tone] if tone in ("green", "cyan", "amber", "magenta", "violet") \
            else t["border"]
        o.append(rect(R_X, y - 13, 2, 18, accent, op=0.9))
        o.append(text(R_X + 12, y, key, t["text"], size=size))
        o.append(text(R_X + R_W - 8, y, val, t[tone], size=size, anchor="end"))
        y += step
    return o


def pipeline(t):
    done = sum(1 for _, s in PIPELINE if s == "done")
    act = sum(1 for _, s in PIPELINE if s == "active")
    o = [
        text(R_X, 524, "PIPELINE", t["green"], size=11, ls=1.7),
        text(R_X + R_W, 524, f"{done} complete · {act} in progress",
             t["dim"], size=10, anchor="end"),
        line(R_X, 534, R_X + R_W, 534, t["border"], 1),
    ]
    n, gap, y, h = len(PIPELINE), 4, 548, 18
    seg = (R_W - gap * (n - 1)) / n
    for i, (label, state) in enumerate(PIPELINE):
        x = R_X + i * (seg + gap)
        if state == "done":
            o.append(rect(x, y, seg, h, t["green"], rx=3, op=0.8))
        elif state == "active":
            o.append(rect(x, y, seg, h, t["band"], t["amber"], rx=3, sw=1.2))
            o.append(f'<rect x="{x}" y="{y}" width="{seg}" height="{h}" rx="3" '
                     f'fill="{t["amber"]}" opacity="0.55">'
                     f'<animate attributeName="opacity" values="0.55;0.12" '
                     f'dur="1.6s" calcMode="discrete" begin="{i * 0.8}s" '
                     f'repeatCount="indefinite"/></rect>')
        else:
            o.append(rect(x, y, seg, h, t["sub"], t["border"], rx=3))
        col = {"done": t["green"], "active": t["amber"], "queued": t["dim"]}[state]
        o.append(text(x + seg / 2, y + 34, label, col, size=9.5, anchor="middle"))
    o.append(text(R_X, 604, "roadmap · each stage earned by shipping",
                  t["dim"], size=9.5))
    return o


# ----------------------------------------------------------------- build

def build(t):
    accents = [t["green"], t["amber"], t["magenta"], t["violet"],
               t["blue"], t["cyan"]]
    scenes = [scene_network, scene_optimizer, scene_neuron,
              scene_stack, scene_particles, scene_log]

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="Vikas Vishwakarma — AI/ML engineer in training">',
        "<style>text{user-select:none;}</style>",
        rect(0, 0, W, H, t["bg"]),
    ]
    o += title_bar(t, accents)
    o.append(rect(L_X, 72, L_W, BOTTOM - 72, t["sub"], t["border"], rx=8))
    for i, fn in enumerate(scenes):
        o += wrap(i, fn(t))
    o += system_info(t)
    o += pipeline(t)
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for name, theme in THEMES.items():
        with open(f"{name}.svg", "w", encoding="utf-8") as f:
            f.write(build(theme))
        print(f"wrote {name}.svg")
