#!/usr/bin/env python3
"""
Generates dark.svg / light.svg — the profile README hero banner.

An instrument-panel terminal containing:
  left   : OPTIMIZER.TRACE   contour map + stepping gradient-descent marker
           FEATURE.WEIGHTS   horizontal bars that fill on a loop
  right  : SYSTEM.INFO       banded key/value readout
  bottom : PIPELINE          segmented progress track

Plain SVG + SMIL. No external fonts, no raster images, no build step.
Edit the DATA block below and re-run:

    python generate_banner.py
"""

import math

# ---------------------------------------------------------------- data

HANDLE = "codewithvikas96-ui"

INFO = [
    ("Subject",       "Vikas Vishwakarma",                             "value"),
    ("Role",          "AI / ML Engineer in Training",                  "steel"),
    ("Origin",        "India · IST (UTC+5:30)",                        "text"),
    ("Status",        "Shipping ML projects · Learning Deep Learning", "sage"),
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
    ("Grid.Mail",     "vikas221018@gmail.com",                         "steel"),
    ("Grid.LinkedIn", "vikas-vishwakarma-62959a387",                   "steel"),
    ("Grid.GitHub",   HANDLE,                                          "amber"),
]

# label, weight 0..1  — feature importances from the ShopSmart model
FEATURES = [
    ("page_value",   0.92),
    ("exit_rate",    0.71),
    ("session_dur",  0.58),
    ("visitor_type", 0.36),
    ("month",        0.24),
]

# stage, state: done | active | queued
PIPELINE = [
    ("Python", "done"),    ("DataSci", "done"),  ("ML", "done"),
    ("DL", "active"),      ("NLP", "active"),    ("GenAI", "queued"),
    ("Agents", "queued"),  ("Prod", "queued"),
]

# graphite + amber instrument panel (dark) / warm paper (light)
THEMES = {
    "dark": dict(
        bg="#0B0D11", panel="#12151C", sub="#0E1117", band="#161A22",
        border="#242A35", text="#8B94A3", value="#E9ECF1", dim="#5A6372",
        amber="#E8A33D", steel="#6C8CC7", sage="#8FB573", rose="#E0685E",
    ),
    "light": dict(
        bg="#F4F1EC", panel="#FFFFFF", sub="#FBF9F6", band="#F5F2EC",
        border="#DED7CC", text="#6B6257", value="#1C1917", dim="#9C9285",
        amber="#B4751A", steel="#3C5E9E", sage="#4F7A3A", rose="#B54A3E",
    ),
}

# ------------------------------------------------------------- geometry

W, H = 1180, 640
WIN_X, WIN_Y, WIN_W, WIN_H = 20, 20, 1140, 600
BAR_H = 36
MONO = "ui-monospace, 'JetBrains Mono', 'SF Mono', 'Cascadia Mono', Menlo, Consolas, monospace"

L_X, L_W = 40, 424
R_X, R_W = 488, 652
BOTTOM = 620

PLOT = (56, 118, 392, 250)      # x, y, w, h  — contour box


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


def rect(x, y, w, h, fill, stroke=None, rx=0, sw=1, op=None):
    a = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke:
        a += f' stroke="{stroke}" stroke-width="{sw}"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + "/>"


def line(x1, y1, x2, y2, stroke, sw=1, op=None):
    a = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + "/>"


def head(x, y, w, label, note, t):
    """Module heading: amber label, dim note, hairline rule."""
    return [
        text(x, y, label, t["amber"], size=11, ls=1.7),
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

    cmd = "vikas@ml-node:~/profile$ python optimizer.py --trace"
    cx = round(590 - len(cmd) * adv(13) / 2, 1)
    o.append(text(cx, 43, cmd, t["text"], size=13))

    # hard-blinking block caret — steps, never fades
    caret_x = round(cx + len(cmd) * adv(13) + 2, 1)
    o.append(f'<rect x="{caret_x}" y="31" width="8" height="14" fill="{t["amber"]}">'
             f'<animate attributeName="opacity" values="1;0" dur="1.1s" '
             f'calcMode="discrete" repeatCount="indefinite"/></rect>')

    o.append(rect(1140 - len(HANDLE) * adv(12) - 14, 31, 4, 4, t["amber"]))
    o.append(text(1140, 42, HANDLE, t["amber"], size=12, anchor="end"))
    return o


def optimizer(t):
    """Contour map with a marker that steps toward the minimum."""
    px, py, pw, ph = PLOT
    o = head(L_X + 16, 96, L_W - 32, "OPTIMIZER.TRACE", "lr 0.05 · 9 steps", t)
    o.append(rect(px, py, pw, ph, t["sub"], t["border"], rx=6))

    o.append(f'<clipPath id="pbox"><rect x="{px}" y="{py}" width="{pw}" '
             f'height="{ph}" rx="6"/></clipPath>')
    o.append('<g clip-path="url(#pbox)">')

    mx, my = 310, 300
    for i, (rx_, ry_) in enumerate(((26, 18), (54, 36), (86, 58), (122, 82), (162, 108))):
        o.append(f'<ellipse cx="{mx}" cy="{my}" rx="{rx_}" ry="{ry_}" fill="none" '
                 f'stroke="{t["dim"]}" stroke-width="1" '
                 f'opacity="{round(0.5 - i * 0.07, 2)}" '
                 f'transform="rotate(-22 {mx} {my})"/>')
    o.append("</g>")

    sx, sy = 110, 170
    pts = []
    for i in range(10):
        decay = math.exp(-0.45 * i)
        wob = 7 * math.exp(-0.3 * i) * (1 if i % 2 else -1)
        pts.append((round(mx + (sx - mx) * decay + wob, 1),
                    round(my + (sy - my) * decay - wob * 0.5, 1)))

    o.append(f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" '
             f'stroke="{t["amber"]}" stroke-width="1.4" opacity="0.5" '
             f'stroke-linejoin="round"/>')
    for x, y in pts:
        o.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{t["sub"]}" '
                 f'stroke="{t["amber"]}" stroke-width="1.2" opacity="0.75"/>')

    o.append(f'<circle cx="{mx}" cy="{my}" r="4" fill="{t["sage"]}"/>')
    o.append(text(mx + 10, my + 4, "min", t["sage"], size=9.5))

    xs = ";".join(str(x) for x, _ in pts)
    ys = ";".join(str(y) for _, y in pts)
    o.append(
        f'<circle r="5.5" fill="{t["amber"]}" cx="{pts[0][0]}" cy="{pts[0][1]}">'
        f'<animate attributeName="cx" values="{xs}" dur="4.5s" calcMode="discrete" '
        f'repeatCount="indefinite"/>'
        f'<animate attributeName="cy" values="{ys}" dur="4.5s" calcMode="discrete" '
        f'repeatCount="indefinite"/></circle>'
    )
    o.append(text(px + 10, py + ph - 10, "∇ gradient descent", t["dim"], size=9.5))
    o.append(text(px + pw - 10, py + ph - 10, "converged", t["sage"],
                  size=9.5, anchor="end"))
    return o


def features(t):
    """Feature-importance bars that grow, hold, then reset."""
    o = head(L_X + 16, 392, L_W - 32, "FEATURE.WEIGHTS", "gain, normalised", t)
    x0, maxw = 152, 258

    for i, (label, weight) in enumerate(FEATURES):
        y = 416 + i * 32
        w = round(maxw * weight, 1)
        o.append(text(L_X + 16, y + 9, label, t["text"], size=11))
        o.append(rect(x0, y, maxw, 10, t["band"], rx=5))
        o.append(
            f'<rect x="{x0}" y="{y}" width="0" height="10" rx="5" fill="{t["amber"]}">'
            f'<animate attributeName="width" values="0;{w};{w};0" '
            f'keyTimes="0;0.42;0.88;1" dur="5.5s" begin="{round(i * 0.16, 2)}s" '
            f'repeatCount="indefinite"/></rect>'
        )
        o.append(text(x0 + w + 8, y + 9, f"{weight:.2f}", t["dim"], size=10))
    return o


def system_info(t):
    o = head(R_X, 96, R_W, "SYSTEM.INFO", f"{len(INFO)} records", t)
    y, step, size = 126, 22, 13

    for i, (key, val, tone) in enumerate(INFO):
        if i % 2 == 0:
            o.append(rect(R_X, y - 14, R_W, 20, t["band"], rx=3, op=0.6))
        accent = t[tone] if tone in ("amber", "steel", "sage") else t["border"]
        o.append(rect(R_X, y - 13, 2, 18, accent, op=0.9))
        o.append(text(R_X + 12, y, key, t["text"], size=size))
        o.append(text(R_X + R_W - 8, y, val, t[tone], size=size, anchor="end"))
        y += step
    return o


def pipeline(t):
    done = sum(1 for _, s in PIPELINE if s == "done")
    act = sum(1 for _, s in PIPELINE if s == "active")
    o = head(R_X, 524, R_W, "PIPELINE",
             f"{done} complete · {act} in progress", t)

    n = len(PIPELINE)
    gap, y, h = 4, 548, 18
    seg = (R_W - gap * (n - 1)) / n

    for i, (label, state) in enumerate(PIPELINE):
        x = R_X + i * (seg + gap)
        if state == "done":
            o.append(rect(x, y, seg, h, t["sage"], rx=3, op=0.85))
        elif state == "active":
            o.append(rect(x, y, seg, h, t["band"], t["amber"], rx=3, sw=1.2))
            o.append(f'<rect x="{x}" y="{y}" width="{seg}" height="{h}" rx="3" '
                     f'fill="{t["amber"]}" opacity="0.55">'
                     f'<animate attributeName="opacity" values="0.55;0.12" dur="1.6s" '
                     f'calcMode="discrete" begin="{i * 0.8}s" '
                     f'repeatCount="indefinite"/></rect>')
        else:
            o.append(rect(x, y, seg, h, t["sub"], t["border"], rx=3))

        col = {"done": t["sage"], "active": t["amber"], "queued": t["dim"]}[state]
        o.append(text(x + seg / 2, y + 34, label, col, size=9.5, anchor="middle"))

    o.append(text(R_X, 604, "roadmap · each stage earned by shipping", t["dim"], size=9.5))
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
    o += optimizer(t)
    o += features(t)
    o += system_info(t)
    o += pipeline(t)
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for name, theme in THEMES.items():
        with open(f"{name}.svg", "w", encoding="utf-8") as f:
            f.write(build(theme))
        print(f"wrote {name}.svg")
