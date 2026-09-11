#!/usr/bin/env python3
"""
Generates dark.svg / light.svg — the profile README hero banner.

A terminal window containing:
  left   : animated feed-forward network + live training-loss plot
  right  : SYSTEM.INFO key/value readout with dotted leaders
  bottom : PIPELINE.STATUS learning track

Everything is plain SVG + SMIL. No external fonts, no raster images,
no build step. Edit the DATA block below and re-run:

    python generate_banner.py
"""

import math

# ---------------------------------------------------------------- data

HANDLE = "codewithvikas96-ui"  # <- your GitHub username (no spaces)

INFO = [
    ("Subject",       "Vikas Vishwakarma",                           "value"),
    ("Role",          "AI / ML Engineer in Training",                "violet"),
    ("Origin",        "India · IST (UTC+5:30)",                      "text"),
    ("Status",        "Shipping ML projects · Learning Deep Learning", "emerald"),
    ("Focus",         "Python → Data Science → ML → AI",             "text"),
    ("Core.Lang",     "Python, C, C++, Java, JavaScript, TypeScript", "text"),
    ("Data.Stack",    "NumPy, Pandas, Matplotlib, Seaborn, Jupyter", "text"),
    ("ML.Stack",      "scikit-learn, XGBoost, LightGBM, CatBoost",   "text"),
    ("ML.Methods",    "Regression, Ensembles, Clustering, PCA",      "text"),
    ("AI.Loading",    "Deep Learning, NLP, Generative AI, Agents",   "amber"),
    ("Core.Backend",  "Node.js, Express, Supabase Edge Functions",   "text"),
    ("Core.Database", "PostgreSQL, MySQL, MongoDB, Oracle PL/SQL",   "text"),
    ("Core.Mobile",   "React Native, Expo, TypeScript",              "text"),
    ("Core.Tools",    "Git, GitHub, Jupyter, PyQt5",                 "text"),
    ("Grid.Mail",     "vikas221018@gmail.com",                       "cyan"),
    ("Grid.LinkedIn", "vikas-vishwakarma-62959a387",                 "cyan"),
    ("Grid.GitHub",   HANDLE,                                        "cyan"),
]

# stage label, state: done | active | queued
PIPELINE = [
    ("Python",   "done"),
    ("DataSci",  "done"),
    ("ML",       "done"),
    ("DL",       "active"),
    ("NLP",      "active"),
    ("GenAI",    "queued"),
    ("Agents",   "queued"),
    ("Prod",     "queued"),
]

THEMES = {
    "dark": dict(
        bg="#0A101F", panel="#0F1626", sub="#0C1322", border="#1E2A44",
        leader="#1E2A44", text="#94A3B8", value="#E2E8F0", dim="#64748B",
        cyan="#22D3EE", violet="#A78BFA", emerald="#10B981",
        amber="#F59E0B", red="#EF4444", grid="#16203A",
    ),
    "light": dict(
        bg="#EEF2F8", panel="#FFFFFF", sub="#F8FAFC", border="#CBD5E1",
        leader="#E2E8F0", text="#64748B", value="#0F172A", dim="#94A3B8",
        cyan="#0E7490", violet="#6D28D9", emerald="#047857",
        amber="#B45309", red="#DC2626", grid="#EDF2F8",
    ),
}

# ------------------------------------------------------------- geometry

W, H = 1180, 640
WIN_X, WIN_Y, WIN_W, WIN_H = 20, 20, 1140, 600
BAR_H = 36
MONO = "ui-monospace, 'JetBrains Mono', 'SF Mono', 'Cascadia Mono', Menlo, Consolas, monospace"

L_X, L_W = 40, 424           # left panel
R_X, R_W = 488, 652          # right column
BOTTOM = 620                 # inner content floor


def adv(size):
    """Monospace advance width for a given font-size."""
    return size * 0.605


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, fill, size=13, anchor="start", ls=None, weight=None, op=None):
    a = f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}"'
    if anchor != "start":
        a += f' text-anchor="{anchor}"'
    if ls is not None:
        a += f' letter-spacing="{ls}"'
    if weight:
        a += f' font-weight="{weight}"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + f">{esc(s)}</text>"


def rect(x, y, w, h, fill, stroke=None, rx=0, sw=1, op=None):
    a = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke:
        a += f' stroke="{stroke}" stroke-width="{sw}"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + "/>"


def line(x1, y1, x2, y2, stroke, sw=1, dash=None, op=None):
    a = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"'
    if dash:
        a += f' stroke-dasharray="{dash}"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + "/>"


def section(x, y, w, label, note, t):
    """Section heading: accent label on the left, dim note on the right, rule under."""
    return [
        text(x, y, label, t["cyan"], size=11, ls=1.6),
        text(x + w, y, note, t["dim"], size=10, anchor="end"),
        line(x, y + 10, x + w, y + 10, t["border"], 1),
    ]


# ------------------------------------------------------------- sections

def title_bar(t):
    o = [
        rect(WIN_X, WIN_Y, WIN_W, WIN_H, t["panel"], t["border"], rx=10, sw=1.5),
        rect(WIN_X, WIN_Y + BAR_H - 10, WIN_W, 10, t["panel"]),
        line(WIN_X, WIN_Y + BAR_H, WIN_X + WIN_W, WIN_Y + BAR_H, t["border"], 1),
    ]
    for i, c in enumerate(("#FF5F56", "#FFBD2E", "#27C93F")):
        o.append(f'<circle cx="{42 + i * 20}" cy="38" r="6" fill="{c}"/>')

    o.append(text(590, 43, "vikas@ml-node : ~/profile — train.py --watch",
                  t["text"], size=13, anchor="middle"))

    pill_w = (len(HANDLE) + 1) * adv(12) + 26
    o.append(rect(1048 - pill_w, 27, pill_w, 22, t["bg"], t["cyan"], rx=11, sw=1))
    o.append(text(1048 - pill_w / 2, 42, "@" + HANDLE, t["cyan"], size=12, anchor="middle"))

    o.append(f'<circle cx="1064" cy="38" r="4" fill="{t["red"]}">'
             f'<animate attributeName="opacity" values="1;0.25;1" dur="1.6s" '
             f'repeatCount="indefinite"/></circle>')
    o.append(text(1074, 42, "LIVE", t["red"], size=12, ls=1))

    # accent rule under the title bar
    o.append('<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{t["cyan"]}"/>'
             f'<stop offset="50%" stop-color="{t["violet"]}"/>'
             f'<stop offset="100%" stop-color="{t["emerald"]}"/></linearGradient>')
    o.append(rect(WIN_X, WIN_Y + BAR_H, WIN_W, 1.5, "url(#accent)", op=0.65))
    return o


def network(t):
    """Animated feed-forward network. Signal sweeps left to right."""
    o = section(L_X + 16, 96, L_W - 32, "NEURAL.NET", "forward pass", t)

    layers = [4, 6, 6, 3]
    colors = [t["cyan"], t["violet"], t["violet"], t["emerald"]]
    xs = [116, 212, 308, 404]
    cy, gap = 258, 40

    pos = []
    for n, x in zip(layers, xs):
        pos.append([(x, cy + (i - (n - 1) / 2) * gap) for i in range(n)])

    # edges first so nodes paint over them
    for li in range(len(pos) - 1):
        for a_i, (x1, y1) in enumerate(pos[li]):
            for b_i, (x2, y2) in enumerate(pos[li + 1]):
                begin = round(li * 0.5 + (a_i + b_i) * 0.055, 3)
                o.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="{colors[li]}" stroke-width="0.9" opacity="0.1">'
                    f'<animate attributeName="opacity" values="0.08;0.42;0.08" '
                    f'dur="3.2s" begin="{begin}s" repeatCount="indefinite"/></line>'
                )

    for li, layer in enumerate(pos):
        for i, (x, y) in enumerate(layer):
            begin = round(li * 0.5 + i * 0.09, 3)
            o.append(
                f'<circle cx="{x}" cy="{y}" r="7" fill="{t["sub"]}" '
                f'stroke="{colors[li]}" stroke-width="1.5">'
                f'<animate attributeName="r" values="7;8.4;7" dur="3.2s" '
                f'begin="{begin}s" repeatCount="indefinite"/>'
                f'<animate attributeName="stroke-opacity" values="0.5;1;0.5" dur="3.2s" '
                f'begin="{begin}s" repeatCount="indefinite"/></circle>'
            )

    for x, lbl in zip(xs, ("input", "h₁", "h₂", "out")):
        o.append(text(x, 396, lbl, t["dim"], size=9.5, anchor="middle"))
    return o


def loss_plot(t):
    """Training-loss curve that redraws itself on a loop."""
    o = section(L_X + 16, 436, L_W - 32, "TRAINING.LOSS", "epoch 120 / 120", t)

    px, py, pw, ph = L_X + 16, 458, L_W - 32, 124
    o.append(rect(px, py, pw, ph, t["grid"], op=0.5, rx=4))
    for i in range(1, 4):
        y = py + ph * i / 4
        o.append(line(px, y, px + pw, y, t["border"], 1, dash="2 5", op=0.7))

    pts, n = [], 64
    for i in range(n):
        u = i / (n - 1)
        v = math.exp(-2.4 * u) * (1 + 0.09 * math.sin(u * 27) + 0.05 * math.sin(u * 11 + 1.3))
        pts.append((round(px + 6 + u * (pw - 12), 2),
                    round(py + 10 + (1 - min(v, 1.0)) * (ph - 22), 2)))

    length = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)

    o.append(f'<path d="{d} L {pts[-1][0]} {py + ph} L {pts[0][0]} {py + ph} Z" '
             f'fill="{t["emerald"]}" opacity="0.07"/>')
    o.append(
        f'<path d="{d}" fill="none" stroke="{t["emerald"]}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'stroke-dasharray="{length:.0f}" stroke-dashoffset="{length:.0f}">'
        f'<animate attributeName="stroke-dashoffset" values="{length:.0f};0;0" '
        f'keyTimes="0;0.75;1" dur="6s" repeatCount="indefinite"/></path>'
    )
    o.append(f'<circle cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="3.5" fill="{t["emerald"]}">'
             f'<animate attributeName="opacity" values="0;0;1;0.4;1" '
             f'keyTimes="0;0.72;0.8;0.9;1" dur="6s" repeatCount="indefinite"/></circle>')

    o.append(line(px, py + ph, px + pw, py + ph, t["border"], 1))
    o.append(text(px, 600, "loss  0.0312 ↓", t["emerald"], size=10))
    o.append(text(px + pw, 600, "val_acc  0.94", t["dim"], size=10, anchor="end"))
    return o


def system_info(t):
    o = section(R_X, 96, R_W, "SYSTEM.INFO", "17 records", t)
    y, step, size = 130, 22, 13

    for key, val, tone in INFO:
        o.append(text(R_X, y, key, t["text"], size=size))
        o.append(text(R_X + R_W, y, val, t[tone] if tone in t else t["value"],
                      size=size, anchor="end"))
        x1 = R_X + len(key) * adv(size) + 10
        x2 = R_X + R_W - len(val) * adv(size) - 10
        if x2 - x1 > 16:
            o.append(line(x1, y - 4, x2, y - 4, t["leader"], 1, dash="1 4"))
        y += step
    return o


def pipeline(t):
    done = sum(1 for _, s in PIPELINE if s == "done")
    active = sum(1 for _, s in PIPELINE if s == "active")
    o = section(R_X, 530, R_W, "PIPELINE.STATUS",
                f"{done}/{len(PIPELINE)} complete · {active} active", t)

    x0, x1, cy = R_X + 28, R_X + R_W - 28, 574
    step = (x1 - x0) / (len(PIPELINE) - 1)
    tone = {"done": t["emerald"], "active": t["amber"], "queued": t["dim"]}

    for i in range(len(PIPELINE) - 1):
        a, b = x0 + i * step, x0 + (i + 1) * step
        c = tone["done"] if PIPELINE[i + 1][1] == "done" else t["border"]
        o.append(line(a + 11, cy, b - 11, cy, c, 1.5, op=0.75))

    for i, (label, state) in enumerate(PIPELINE):
        x, c = x0 + i * step, tone[state]
        if state == "done":
            o.append(f'<circle cx="{x}" cy="{cy}" r="8" fill="{c}" opacity="0.18"/>')
            o.append(f'<circle cx="{x}" cy="{cy}" r="4.5" fill="{c}"/>')
        elif state == "active":
            o.append(f'<circle cx="{x}" cy="{cy}" r="8" fill="none" stroke="{c}" '
                     f'stroke-width="1.5"><animate attributeName="r" values="7;10;7" '
                     f'dur="2.4s" begin="{i * 0.4}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="1;0.3;1" dur="2.4s" '
                     f'begin="{i * 0.4}s" repeatCount="indefinite"/></circle>')
            o.append(f'<circle cx="{x}" cy="{cy}" r="4" fill="{c}"/>')
        else:
            o.append(f'<circle cx="{x}" cy="{cy}" r="4.5" fill="{t["sub"]}" '
                     f'stroke="{t["border"]}" stroke-width="1.5"/>')
        o.append(text(x, cy + 22, label, c if state != "queued" else t["dim"],
                      size=9.5, anchor="middle"))
    return o


# ----------------------------------------------------------------- build

def build(t):
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="Vikas Vishwakarma — AI/ML engineer in training">',
        "<style>text{user-select:none;}</style>",
        rect(0, 0, W, H, t["bg"]),
    ]
    o += title_bar(t)
    o.append(rect(L_X, 72, L_W, BOTTOM - 72, t["sub"], t["border"], rx=8))
    o += network(t)
    o += loss_plot(t)
    o += system_info(t)
    o += pipeline(t)
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for name, theme in THEMES.items():
        out = f"{name}.svg"
        with open(out, "w", encoding="utf-8") as f:
            f.write(build(theme))
        print(f"wrote {out}")
