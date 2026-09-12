#!/usr/bin/env python3
"""
Generates the project cards for section 03 of the profile README.

One card per project, each with its own accent from the shared palette and its
own motif — a small generated graphic that says what kind of work it is before
a word is read: a bar chart for the EDA, a decision tree for the classifier, a
confusion matrix for the model comparison, a fitted scatter for the regression,
a two-sided flow for the platform, a phone for the mobile app. That motif is
the project's logo; nothing is fetched from anywhere.

    project-01-{dark,light}.svg ... project-06-{dark,light}.svg

The card carries the index, name, domain, purpose, stack and a couple of facts,
so the markdown below it only needs the parts a card is bad at: what it does,
what was learned, and the link out.

Facts are deliberately qualitative — swap any of them for a real number the
moment you have one (rows, F1, ROC-AUC, users). One string in PROJECTS below.

Palette and helpers come from generate_banner.py, so every panel on the page
stays in the same design system. Edit PROJECTS and re-run:

    python generate_projects.py
"""

import math
import random

from generate_banner import THEMES, adv, esc, line, mix, rect, text

PW, PAD = 1180, 40

PROJECTS = [
    dict(
        idx="01", accent="cyan", motif="bars",
        name="IPL 2022 Data Analysis", domain="Data Analysis", status=None,
        purpose="A full IPL 2022 season turned into an interactive analytical "
                "story instead of a static spreadsheet.",
        stack=("Python", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Streamlit"),
        facts=("match-level EDA", "interactive Streamlit dashboard"),
    ),
    dict(
        idx="02", accent="green", motif="tree",
        name="ShopSmart", domain="Machine Learning", status=None,
        purpose="Predicts whether an online browsing session will generate "
                "revenue, from behavioural signals in that session.",
        stack=("Python", "scikit-learn", "Decision Tree", "Pandas"),
        facts=("engineered session features", "class-aware evaluation"),
    ),
    dict(
        idx="03", accent="violet", motif="matrix",
        name="Loan Approval Prediction", domain="Machine Learning", status=None,
        purpose="Classical classifiers benchmarked on a realistic credit "
                "decision — and a reason for why one of them wins.",
        stack=("Python", "Logistic Regression", "KNN", "Gaussian NB", "scikit-learn"),
        facts=("3 model families compared", "imbalance handled explicitly"),
    ),
    dict(
        idx="04", accent="amber", motif="scatter",
        name="Insurance Charges Prediction", domain="Regression", status=None,
        purpose="Models medical insurance cost and identifies which applicant "
                "attributes actually drive the premium.",
        stack=("Python", "Regression", "scikit-learn", "Pandas", "Seaborn"),
        facts=("engineered BMI & age bands", "correlation-led modelling"),
    ),
    dict(
        idx="05", accent="magenta", motif="flow",
        name="QuickFix Lite", domain="Full-Stack", status="hackathon winner",
        purpose="Connects students with local service providers through one "
                "full-stack platform, built under pressure.",
        stack=("Web", "Backend", "Database", "Full-stack architecture"),
        facts=("two-sided platform", "shipped in a hackathon window"),
    ),
    dict(
        idx="06", accent="blue", motif="phone",
        name="HR Management Application", domain="Mobile", status="in development",
        purpose="A mobile HR platform with real authentication, role separation "
                "and security enforced at the database layer.",
        stack=("React Native", "Expo", "TypeScript", "Supabase", "PostgreSQL"),
        facts=("role-based access", "Row Level Security at the DB layer"),
    ),
]


# ---------------------------------------------------------------- motifs
#
# Each draws inside the box (x, y, w, h) in the card's accent. They are the
# only thing that differs between one card and the next at a glance, so they
# stay geometric and flat — a silhouette you read in a quarter of a second.

def m_bars(x, y, w, h, a, t):
    """EDA — a season of matches as a distribution."""
    o = [line(x, y + h, x + w, y + h, t["border"], 1.5)]
    hs = (0.38, 0.66, 0.31, 0.86, 0.52, 0.72, 0.27, 0.95, 0.58)
    bw = (w - (len(hs) - 1) * 8) / len(hs)
    for i, f in enumerate(hs):
        bh, bx = h * f, x + i * (bw + 8)
        o.append(f'<rect x="{bx:.1f}" y="{y + h:.1f}" width="{bw:.1f}" '
                 f'height="0" rx="2" fill="{a}" opacity="{0.45 + 0.5 * f:.2f}">'
                 f'<animate attributeName="height" values="0;{bh:.1f}" dur="0.5s" '
                 f'begin="{i * 0.06:.2f}s" fill="freeze"/>'
                 f'<animate attributeName="y" values="{y + h:.1f};'
                 f'{y + h - bh:.1f}" dur="0.5s" begin="{i * 0.06:.2f}s" '
                 f'fill="freeze"/></rect>')
    return o


def m_tree(x, y, w, h, a, t):
    """A decision tree — one split, then leaves."""
    o, cx = [], x + w / 2
    rows = ((cx,), (cx - w * 0.24, cx + w * 0.24),
            (cx - w * 0.36, cx - w * 0.12, cx + w * 0.12, cx + w * 0.36))
    ys = (y + 12, y + h / 2, y + h - 10)
    for lvl in (0, 1):
        for i, px in enumerate(rows[lvl]):
            for k in (0, 1):
                qx = rows[lvl + 1][i * 2 + k]
                o.append(f'<line x1="{px:.1f}" y1="{ys[lvl]:.1f}" x2="{qx:.1f}" '
                         f'y2="{ys[lvl + 1]:.1f}" stroke="{a}" stroke-width="1.8" '
                         f'opacity="0.55"/>')
    for lvl, row in enumerate(rows):
        for i, px in enumerate(row):
            r = (7, 5.5, 4.5)[lvl]
            fill = a if lvl < 2 else (a if i % 2 else t["panel"])
            o.append(f'<circle cx="{px:.1f}" cy="{ys[lvl]:.1f}" r="{r}" '
                     f'fill="{fill}" stroke="{a}" stroke-width="1.8" '
                     f'opacity="{1 - lvl * 0.12:.2f}"/>')
    return o


def m_matrix(x, y, w, h, a, t):
    """A confusion matrix — the diagonal is the part you want dark."""
    o, s = [], min(w, h)
    cell, gap = (s - 6) / 2, 6
    ox = x + (w - s) / 2
    for r in range(2):
        for c in range(2):
            op = (0.92, 0.16, 0.2, 0.82)[r * 2 + c]
            o.append(f'<rect x="{ox + c * (cell + gap):.1f}" '
                     f'y="{y + r * (cell + gap):.1f}" width="{cell:.1f}" '
                     f'height="{cell:.1f}" rx="3" fill="{a}" opacity="{op}">'
                     f'<animate attributeName="opacity" values="0;{op}" '
                     f'dur="0.4s" begin="{(r * 2 + c) * 0.1:.1f}s" '
                     f'fill="freeze"/></rect>')
    o.append(line(ox - 8, y, ox - 8, y + s, t["border"], 1.5))
    o.append(line(ox, y + s + 8, ox + s, y + s + 8, t["border"], 1.5))
    return o


def m_scatter(x, y, w, h, a, t):
    """A regression — the cloud and the line drawn through it."""
    rng = random.Random(4)
    o = [line(x, y + h, x + w, y + h, t["border"], 1.5),
         line(x, y, x, y + h, t["border"], 1.5)]
    o.append(f'<line x1="{x + 8}" y1="{y + h - 10}" x2="{x + w - 6}" '
             f'y2="{y + 14}" stroke="{a}" stroke-width="2.2" '
             f'stroke-linecap="round" opacity="0.55"/>')
    for i in range(16):
        u = (i + 0.5) / 16
        px = x + 8 + u * (w - 14)
        py = y + h - 10 - u * (h - 24) + rng.uniform(-13, 13)
        py = min(max(py, y + 4), y + h - 4)
        o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.4" fill="{a}" '
                 f'opacity="0"><animate attributeName="opacity" '
                 f'values="0;0.9" dur="0.4s" begin="{i * 0.04:.2f}s" '
                 f'fill="freeze"/></circle>')
    return o


def m_flow(x, y, w, h, a, t):
    """A two-sided platform — both sides meeting through one hub."""
    o, hub = [], (x + w / 2, y + h / 2)
    left = [(x + 6, y + 10 + i * (h - 20) / 2) for i in range(3)]
    right = [(x + w - 6, y + 10 + i * (h - 20) / 2) for i in range(3)]
    for i, (px, py) in enumerate(left + right):
        o.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{hub[0]:.1f}" '
                 f'y2="{hub[1]:.1f}" stroke="{a}" stroke-width="1.6" '
                 f'opacity="0.4"/>')
        o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" '
                 f'fill="{t["panel"]}" stroke="{a}" stroke-width="2"/>')
        o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="{a}" '
                 f'opacity="0"><animate attributeName="opacity" '
                 f'values="0;1;0" dur="2.6s" begin="{i * 0.35:.2f}s" '
                 f'repeatCount="indefinite"/></circle>')
    o.append(f'<rect x="{hub[0] - 13:.1f}" y="{hub[1] - 13:.1f}" width="26" '
             f'height="26" rx="7" fill="{a}"/>')
    return o


def m_phone(x, y, w, h, a, t):
    """A mobile app — a role-split list behind a locked door."""
    pw, ph = h * 0.52, h
    px = x + (w - pw) / 2
    o = [rect(px, y, pw, ph, mix(t["panel"], a, 0.1), a, rx=9, sw=2),
         rect(px + pw * 0.32, y + 5, pw * 0.36, 3.5, a, rx=2, op=0.7),
         rect(px + 8, y + 16, pw - 16, 13, a, rx=3, op=0.75)]
    for i in range(3):
        ry = y + 36 + i * 15
        o.append(rect(px + 8, ry, 9, 9, a, rx=2.5, op=0.85))
        o.append(rect(px + 22, ry + 2, pw - 32, 5, a, rx=2.5, op=0.35))
    o.append(f'<rect x="{px + pw - 20:.1f}" y="{y + ph - 26:.1f}" width="14" '
             f'height="11" rx="2.5" fill="{a}"/>')
    o.append(f'<path d="M{px + pw - 16.5:.1f} {y + ph - 26:.1f} v-4 '
             f'a3.5 3.5 0 0 1 7 0 v4" fill="none" stroke="{a}" '
             f'stroke-width="2"/>')
    return o


MOTIFS = {"bars": m_bars, "tree": m_tree, "matrix": m_matrix,
          "scatter": m_scatter, "flow": m_flow, "phone": m_phone}


# ----------------------------------------------------------------- card

def chip(x, y, label, col, t, size=12, fill=None):
    """A bordered tag. Returns (svg, width) so rows can be packed."""
    w = len(label) * adv(size) + 22
    return (rect(x, y, w, 24, fill if fill else mix(t["panel"], col, 0.1),
                 col, rx=6, sw=1, op=0.95)
            + text(x + w / 2, y + 16, label, col, size=size, anchor="middle"),
            w)


def project_card(p, t):
    a = t[p["accent"]]
    h = 212
    mx, my, mw, mh = 920, 52, 200, 116

    # a line that runs under the motif is worse than one that reads short —
    # fail here rather than ship an overlapping card
    for field, size in (("purpose", 13), ("facts", 11.5)):
        s = p[field] if field == "purpose" else "  ·  ".join(p[field])
        assert PAD + len(s) * adv(size) <= mx - 20, (
            f'project {p["idx"]}: {field} runs to '
            f'{PAD + len(s) * adv(size):.0f}px, past the motif at {mx}px — '
            f'trim it')

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {h}" '
         f'width="{PW}" height="{h}" role="img" '
         f'aria-label="{esc(p["name"])}">',
         "<style>text{user-select:none;}</style>",
         f'<clipPath id="c"><rect x="0.75" y="0.75" width="{PW - 1.5}" '
         f'height="{h - 1.5}" rx="12"/></clipPath>',
         rect(0.75, 0.75, PW - 1.5, h - 1.5, t["panel"], t["border"], rx=12, sw=1.5),
         f'<rect x="0" y="0" width="5" height="{h}" fill="{a}" '
         f'clip-path="url(#c)"/>']

    o.append(text(PAD, 48, p["idx"], a, size=13, ls=2))
    o.append(line(PAD + 30, 43, PAD + 62, 43, a, 1.5, op=0.5))

    x = PW - PAD                                   # tags pack from the right
    for label, col in ([(p["status"], t["amber"] if p["status"] ==
                         "in development" else a)] if p["status"] else []) \
            + [(p["domain"], t["dim"])]:
        svg, w = chip(0, 0, label, col, t, size=11)
        x -= w
        o.append(f'<g transform="translate({x:.1f},26)">{svg}</g>')
        x -= 10

    o.append(text(PAD, 92, p["name"], t["value"], size=25))
    o.append(text(PAD, 120, p["purpose"], t["text"], size=13))

    x = PAD
    for s in p["stack"]:
        svg, w = chip(x, 146, s, t["dim"], t, size=12, fill=t["band"])
        o.append(svg)
        x += w + 8

    o.append(text(PAD, 194, "  ·  ".join(p["facts"]), a, size=11.5, op=0.9))
    o += MOTIFS[p["motif"]](mx, my, mw, mh, a, t)
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for p in PROJECTS:
        for theme, t in THEMES.items():
            with open(f"project-{p['idx']}-{theme}.svg", "w",
                      encoding="utf-8") as f:
                f.write(project_card(p, t))
            print(f"wrote project-{p['idx']}-{theme}.svg")
