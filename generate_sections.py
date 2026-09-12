#!/usr/bin/env python3
"""
Generates the README section panels — the body counterpart to the hero banner.

GitHub strips CSS from a README, so the only surface you can actually style is
SVG. Anything else renders in GitHub's chrome: same grey slab, same borders,
same fonts. These panels take the sections whose content is structural rather
than prose and render them in the banner's own design system — same palette,
same mono stack, same card chrome, same animation language — so the page reads
as one continuous terminal session instead of a hero followed by a plain README.

  capabilities-{dark,light}.svg   section 01  CAPABILITY REPORT
  trajectory-{dark,light}.svg     section 02  ROLE TRAJECTORY
  roadmap-{dark,light}.svg        section 04  LEARNING ROADMAP
  buildlog-{dark,light}.svg       section 06  BUILD LOG
  quote-{dark,light}.svg          closing     a typed-out quote

Prose stays in markdown on purpose — it has to stay searchable, copyable and
readable by a screen reader. Only the chrome and the diagrams move to SVG.

Palette and helpers come from generate_banner.py, so the two scripts can never
drift apart. Edit the data blocks below and re-run:

    python generate_sections.py
"""

from generate_banner import THEMES, adv, esc, line, mix, rect, text

# ---------------------------------------------------------------- data

CAPS = [
    ("ONLINE",  "Python",                      "core language · daily driver"),
    ("ONLINE",  "Mathematics & Statistics",    "linear algebra · probability · inference"),
    ("ONLINE",  "Data Analysis / EDA",         "NumPy · Pandas · Matplotlib · Seaborn"),
    ("ONLINE",  "Classical Machine Learning",  "scikit-learn · boosting · clustering"),
    ("ONLINE",  "Software Engineering",        "full-stack web · mobile · databases"),
    ("LOADING", "Deep Learning",               "neural nets · backprop · architectures"),
    ("LOADING", "Natural Language Processing", "text pipelines · embeddings"),
    ("QUEUED",  "Generative AI",               "LLM application patterns · RAG"),
    ("QUEUED",  "AI Agents",                   "tool use · planning loops"),
    ("QUEUED",  "Production AI Systems",       "serving · monitoring · MLOps"),
]

ROLES = [
    ("00", "Developer",      "current",   "green"),
    ("01", "Data Scientist", "in-flight", "amber"),
    ("02", "ML Engineer",    "next",      "dim"),
    ("03", "AI Engineer",    "target",    "magenta"),
]

STAGES = [
    ("00", "Python + Mathematics", "done"),
    ("01", "Data Science",         "done"),
    ("02", "Machine Learning",     "done"),
    ("03", "Deep Learning",        "active"),
    ("04", "NLP",                  "active"),
    ("05", "Generative AI",        "queued"),
    ("06", "AI Agents",            "queued"),
    ("07", "Production AI",        "queued"),
]

QUOTE = "The purpose of computing is insight, not numbers."
QUOTE_BY = "Richard W. Hamming · Numerical Methods for Scientists and Engineers, 1962"
QUOTE_CMD = "cat ~/.philosophy"

BUILD = [
    ("ml",   "comparing boosting families — XGBoost vs LightGBM vs CatBoost", "green"),
    ("dl",   "implementing backpropagation by hand before trusting a framework", "amber"),
    ("nlp",  "building text preprocessing pipelines from tokenization upward", "magenta"),
    ("data", "sharpening EDA workflow: profile → clean → engineer → validate", "cyan"),
    ("eng",  "keeping notebooks reproducible instead of accidentally stateful", "blue"),
    ("next", "first end-to-end deep learning project, served behind an API", "violet"),
]


# ------------------------------------------------------------- geometry

PW = 1180                                  # matches the banner, so widths line up
PAD = 40


def card(h, label, note, accent, t, alt):
    """Panel chrome — the same card, rule and header the banner modules use."""
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {h}" '
        f'width="{PW}" height="{h}" role="img" aria-label="{esc(alt)}">',
        "<style>text{user-select:none;}</style>",
        rect(0.75, 0.75, PW - 1.5, h - 1.5, t["panel"], t["border"], rx=12, sw=1.5),
        text(PAD, 46, label, accent, size=12, ls=1.8),
        text(PW - PAD, 46, note, t["dim"], size=11, anchor="end"),
        line(PAD, 58, PW - PAD, 58, t["border"], 1),
    ]


def printed(at, dur=0.01):
    """Appear at `at` seconds and stay — a line printing to a terminal."""
    return (f'<animate attributeName="opacity" values="0;1" dur="{dur}s" '
            f'begin="{at}s" fill="freeze"/>')


def pill(x, y, w, label, col, t, size=10):
    """A bracketed status chip."""
    return (rect(x, y, w, 20, mix(t["panel"], col, 0.16), col, rx=10, sw=1,
                 op=0.95)
            + text(x + w / 2, y + 14, label, col, size=size, anchor="middle",
                   ls=1.1))


# ------------------------------------------------------- terminal window

def window(h, title, t, alt):
    """The hero's own window chrome — traffic lights, rule, accent seam."""
    bar = 36
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {h}" '
         f'width="{PW}" height="{h}" role="img" aria-label="{esc(alt)}">',
         "<style>text{user-select:none;}</style>",
         rect(0.75, 0.75, PW - 1.5, h - 1.5, t["panel"], t["border"], rx=10, sw=1.5),
         line(0, bar, PW, bar, t["border"], 1)]
    for i, c in enumerate(("#FF5F56", "#FFBD2E", "#27C93F")):
        o.append(f'<circle cx="{30 + i * 20}" cy="{bar / 2}" r="6" fill="{c}"/>')
    o.append(text(PW / 2, bar / 2 + 4, title, t["text"], size=13, anchor="middle"))
    o.append('<linearGradient id="seam" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{t["green"]}"/>'
             f'<stop offset="30%" stop-color="{t["cyan"]}"/>'
             f'<stop offset="60%" stop-color="{t["magenta"]}"/>'
             f'<stop offset="82%" stop-color="{t["violet"]}"/>'
             f'<stop offset="100%" stop-color="{t["amber"]}"/></linearGradient>')
    o.append(rect(0, bar, PW, 1.5, "url(#seam)", op=0.7))
    return o


def shows(at, clear, cyc):
    """Cut in at `at`, cut out at `clear` — no fade, like a terminal."""
    return ('<animate attributeName="opacity" values="0;1;0;0" '
            f'keyTimes="0;{at / cyc:.4f};{clear / cyc:.4f};1" '
            f'calcMode="discrete" dur="{cyc}s" repeatCount="indefinite"/>')


def fades(at, dur, clear, cyc):
    return ('<animate attributeName="opacity" values="0;0;1;1;0;0" '
            f'keyTimes="0;{at / cyc:.4f};{(at + dur) / cyc:.4f};'
            f'{clear / cyc:.4f};{(clear + 0.3) / cyc:.4f};1" '
            f'dur="{cyc}s" repeatCount="indefinite"/>')


def _steps(n, t0, t1, clear, cyc):
    """keyTimes for one character-per-step typing, then a wipe."""
    return ["0"] + [f"{(t0 + (t1 - t0) * i / n) / cyc:.4f}" for i in range(1, n + 1)] \
        + [f"{clear / cyc:.4f}", "1"]


def typed(s, x, y, size, fill, t0, t1, clear, cyc, cid):
    """Reveal `s` one character at a time.

    A clip rectangle widens by exactly one character advance per step, so the
    glyphs are never scaled or slid — they simply arrive, the way they do when
    someone is actually typing. Monospace makes the arithmetic exact.
    """
    n = len(s)
    vals = ["0"] + [f"{i * adv(size):.1f}" for i in range(1, n + 1)] + ["0", "0"]
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y - size}" width="0" '
            f'height="{size * 1.4:.0f}">'
            f'<animate attributeName="width" values="{";".join(vals)}" '
            f'keyTimes="{";".join(_steps(n, t0, t1, clear, cyc))}" '
            f'calcMode="discrete" dur="{cyc}s" repeatCount="indefinite"/>'
            f'</rect></clipPath>'
            f'<g clip-path="url(#{cid})">{text(x, y, s, fill, size=size)}</g>')


def caret(s, x, y, size, col, t0, t1, clear, cyc):
    """The cursor that walks along behind the characters being typed."""
    n = len(s)
    xs = [f"{x:.1f}"] + [f"{x + i * adv(size):.1f}" for i in range(1, n + 1)] \
        + [f"{x:.1f}", f"{x:.1f}"]
    return (f'<rect x="{x}" y="{y - size + 2:.0f}" width="{adv(size):.1f}" '
            f'height="{size:.0f}" fill="{col}" opacity="0">'
            f'<animate attributeName="x" values="{";".join(xs)}" '
            f'keyTimes="{";".join(_steps(n, t0, t1, clear, cyc))}" '
            f'calcMode="discrete" dur="{cyc}s" repeatCount="indefinite"/>'
            f'{shows(t0, t1 + 0.25, cyc)}</rect>')


# ------------------------------------------------------------- panels

def capabilities(t):
    """Section 01 — status board.

    Replaces a ```diff block, which coloured the two skills being actively
    learned in deletion-red and read as "something is broken". Here the state
    bar carries the meaning instead: full, sweeping, or empty.
    """
    accent = t["green"]
    tone = {"ONLINE": t["green"], "LOADING": t["amber"], "QUEUED": t["dim"]}
    BX, BW = 940, 200
    body, loading, y = [], [], 92

    for i, (state, name, det) in enumerate(CAPS):
        if i and CAPS[i - 1][0] != state:
            y += 14                            # a breath between the groups
        col = tone[state]
        fill = mix(t["panel"], col, 0.12 if state != "QUEUED" else 0.05)
        g = [f'<g opacity="0">{printed(round(0.12 + i * 0.07, 2))}',
             rect(PAD, y, PW - 2 * PAD, 30, fill, rx=6),
             rect(PAD, y, 3.5, 30, col, rx=1.8, op=0.9),
             pill(PAD + 20, y + 5, 100, state, col, t),
             text(PAD + 142, y + 20, name, t["value"], size=14),
             text(470, y + 20, det, t["text"], size=12.5),
             rect(BX, y + 12, BW, 6, t["dim"], rx=3, op=0.22)]
        if state == "ONLINE":
            g.append(rect(BX, y + 12, BW, 6, col, rx=3, op=0.9))
        elif state == "LOADING":
            loading.append(y + 12)
        g.append("</g>")
        body += g
        y += 34

    # the sweeping block that makes LOADING read as in-progress, not failed
    if loading:
        body.append('<clipPath id="bars">'
                    + "".join(rect(BX, by, BW, 6, "#000", rx=3)
                              for by in loading) + "</clipPath>")
        body.append('<g clip-path="url(#bars)">')
        for by in loading:
            body.append(f'<rect x="{BX}" y="{by}" width="70" height="6" rx="3" '
                        f'fill="{t["amber"]}" opacity="0.95">'
                        f'<animateTransform attributeName="transform" '
                        f'type="translate" values="-80,0;{BW + 10},0" dur="2.1s" '
                        f'repeatCount="indefinite"/></rect>')
        body.append("</g>")

    y += 18
    x = PAD
    for col, label in ((t["green"], "proven in shipped projects"),
                       (t["amber"], "actively learning"),
                       (t["dim"], "queued next")):
        body.append(rect(x, y + 2, 10, 10, col, rx=3, op=0.9))
        body.append(text(x + 18, y + 11, label, t["dim"], size=11))
        x += 26 + len(label) * adv(11) + 34
    h = y + 44

    return "\n".join(card(h, "CAPABILITY REPORT", "self-assessed · project-backed",
                          accent, t, "Capability report") + body + ["</svg>"])


def trajectory(t):
    """Section 02 — where the roles are heading, as four connected stages."""
    accent = t["blue"]
    gap, cw = 26, (PW - 2 * PAD - 3 * 26) / 4
    top, ch = 92, 104
    body = []

    for i, (idx, role, state, tone) in enumerate(ROLES):
        col = t[tone]
        x = PAD + i * (cw + gap)
        live = state in ("current", "in-flight")
        body.append(f'<g opacity="0">{printed(round(0.15 + i * 0.12, 2))}')
        body.append(rect(x, top, cw, ch, mix(t["panel"], col, 0.09),
                         col if live else t["border"], rx=10,
                         sw=1.5 if live else 1))
        body.append(text(x + 18, top + 28, idx, t["dim"], size=11, ls=1.4))
        body.append(text(x + 18, top + 58, role, t["value"], size=16))
        body.append(pill(x + 18, top + 70, 92, state, col, t))
        if state == "in-flight":                # the stage actually in motion
            body.append(f'<rect x="{x}" y="{top}" width="{cw}" height="{ch}" '
                        f'rx="10" fill="none" stroke="{col}" stroke-width="1.5" '
                        f'opacity="0"><animate attributeName="opacity" '
                        f'values="0;0.85;0" dur="2.4s" repeatCount="indefinite"/>'
                        f'</rect>')
        body.append("</g>")
        if i < 3:                               # chevron in the gap
            cx, cy = x + cw + gap / 2, top + ch / 2
            body.append(f'<polyline points="{cx - 4},{cy - 6} {cx + 3},{cy} '
                        f'{cx - 4},{cy + 6}" fill="none" stroke="{t["dim"]}" '
                        f'stroke-width="1.8" stroke-linecap="round" '
                        f'stroke-linejoin="round" opacity="0.8"/>')

    y = top + ch + 40
    body.append(text(PAD, y, "note: this is a roadmap, not a résumé.",
                     t["dim"], size=12))
    body.append(text(PAD + 52, y + 22,
                     "each stage is earned by shipping, not by reading.",
                     t["dim"], size=12))
    return "\n".join(card(y + 52, "ROLE TRAJECTORY", "developer → AI engineer",
                          accent, t, "Role trajectory") + body + ["</svg>"])


def roadmap(t):
    """Section 04 — the learning track, horizontal.

    The mermaid version stacked eight nodes vertically (a full screen of
    scrolling) and clipped its own labels — "NLP" rendered as "NLF" — because
    the font override broke mermaid's text measurement. Laid out by hand here.
    """
    accent = t["green"]
    tone = {"done": t["green"], "active": t["amber"], "queued": t["dim"]}
    x0, x1, ry = 130, 1050, 158
    step = (x1 - x0) / (len(STAGES) - 1)
    xs = [x0 + i * step for i in range(len(STAGES))]
    frontier = max(i for i, s in enumerate(STAGES) if s[2] != "queued")
    body = []

    body.append(line(60, ry, 1120, ry, t["border"], 4, op=0.5))
    body.append(f'<line x1="{xs[0]}" y1="{ry}" x2="{round(xs[2], 1)}" y2="{ry}" '
                f'stroke="{t["green"]}" stroke-width="4" stroke-linecap="round" '
                f'opacity="0.85"/>')
    body.append(f'<line x1="{round(xs[2], 1)}" y1="{ry}" '
                f'x2="{round(xs[frontier], 1)}" y2="{ry}" stroke="{t["amber"]}" '
                f'stroke-width="4" stroke-linecap="round" opacity="0.85"/>')

    for i, (idx, name, state) in enumerate(STAGES):
        col, x = tone[state], round(xs[i], 1)
        up = i % 2 == 0
        body.append(f'<g opacity="0">{printed(round(0.15 + i * 0.09, 2))}')
        body.append(rect(x - 1, ry - 26 if up else ry + 10, 2, 16, t["border"]))
        body.append(text(x, ry - 52 if up else ry + 54, idx, t["dim"], size=10,
                         anchor="middle", ls=1.4))
        body.append(text(x, ry - 34 if up else ry + 72, name, col, size=13,
                         anchor="middle"))
        if state == "queued":
            body.append(f'<circle cx="{x}" cy="{ry}" r="7.5" '
                        f'fill="{t["panel"]}" stroke="{t["border"]}" '
                        f'stroke-width="2"/>')
        else:
            body.append(f'<circle cx="{x}" cy="{ry}" r="7.5" fill="{col}"/>')
        if state == "active":
            body.append(f'<circle cx="{x}" cy="{ry}" r="7.5" fill="none" '
                        f'stroke="{col}" stroke-width="2" opacity="0">'
                        f'<animate attributeName="r" values="7.5;16" dur="2.2s" '
                        f'begin="{round(i * 0.4, 2)}s" repeatCount="indefinite"/>'
                        f'<animate attributeName="opacity" values="0.8;0" '
                        f'dur="2.2s" begin="{round(i * 0.4, 2)}s" '
                        f'repeatCount="indefinite"/></circle>')
        body.append("</g>")

    # the same travelling signal the neuron uses, run up to the frontier
    body.append(f'<circle cy="{ry}" r="4.5" fill="{t["cyan"]}" opacity="0">'
                f'<animate attributeName="cx" values="{xs[0]};'
                f'{round(xs[frontier], 1)}" dur="4.5s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" '
                f'keyTimes="0;0.06;0.88;1" dur="4.5s" repeatCount="indefinite"/>'
                f'</circle>')

    y, x = 256, PAD
    for col, label in ((t["green"], "done"), (t["amber"], "in progress"),
                       (t["dim"], "queued")):
        body.append(rect(x, y - 8, 10, 10, col, rx=3, op=0.9))
        body.append(text(x + 18, y + 1, label, t["dim"], size=11))
        x += 26 + len(label) * adv(11) + 30
    body.append(text(PW - PAD, y + 1,
                     f"current focus · {STAGES[frontier - 1][1]} → "
                     f"{STAGES[frontier][1]}", t["dim"], size=11, anchor="end"))

    return "\n".join(card(288, "LEARNING ROADMAP", "8 stages · 3 complete",
                          accent, t, "Learning roadmap") + body + ["</svg>"])


def buildlog(t):
    """Section 06 — what is actually on the bench, printing like a live tail."""
    accent = t["cyan"]
    body = [rect(PAD, 76, PW - 2 * PAD, len(BUILD) * 30 + 28, t["sub"],
                 t["border"], rx=8)]
    y = 106
    for i, (tag, msg, tone) in enumerate(BUILD):
        body.append(f'<g opacity="0">{printed(round(0.2 + i * 0.28, 2))}'
                    + text(PAD + 22, y, f"[{tag:<4}]", t[tone], size=13)
                    + text(PAD + 110, y, msg, t["text"], size=13)
                    + "</g>")
        y += 30

    y += 30
    prompt = "vikas@ml-node:~$"
    body.append(text(PAD, y, prompt, t["green"], size=13))
    cx = PAD + len(prompt) * adv(13) + 8
    body.append(f'<rect x="{round(cx, 1)}" y="{y - 11}" width="8" height="14" '
                f'fill="{accent}"><animate attributeName="opacity" '
                f'values="1;0" dur="1.1s" calcMode="discrete" '
                f'repeatCount="indefinite"/></rect>')
    body.append(text(PW - PAD, y, "tail -f · live", t["dim"], size=11,
                     anchor="end"))
    return "\n".join(card(y + 30, "BUILD LOG", "what is on the bench now",
                          accent, t, "Build log") + body + ["</svg>"])


def quote(t):
    """Closing panel — a terminal session that types out one line worth keeping.

    The whole thing loops: the animation fires when the image loads, not when
    it scrolls into view, so a one-shot reveal would already be over by the
    time anyone reached the bottom of the page. Fourteen seconds — type, sit,
    clear, again — means there is always something to catch.
    """
    cyc, h, a = 14.0, 290, t["cyan"]
    clear = 12.4
    prompt = "vikas@ml-node:~$"
    px = PAD + 16
    cx = px + len(prompt) * adv(15) + 9

    o = window(h, "vikas@ml-node: ~", t, f"{QUOTE} — {QUOTE_BY}")

    o.append(f'<g opacity="0">{shows(0.2, clear, cyc)}'
             + text(px, 92, prompt, t["green"], size=15) + "</g>")
    o.append(typed(QUOTE_CMD, cx, 92, 15, a, 0.5, 2.3, clear, cyc, "q1"))
    o.append(caret(QUOTE_CMD, cx, 92, 15, a, 0.5, 2.3, clear, cyc))

    o.append(f'<g opacity="0">{shows(2.7, clear, cyc)}'
             + rect(px, 132, 3, 34, a, rx=1.5, op=0.8) + "</g>")
    o.append(typed(f'"{QUOTE}"', px + 18, 158, 24, t["value"],
                   2.8, 6.1, clear, cyc, "q2"))
    o.append(f'<g opacity="0">{fades(6.5, 0.6, clear, cyc)}'
             + text(px + 18, 196, f"— {QUOTE_BY}", t["dim"], size=13.5) + "</g>")

    o.append(f'<g opacity="0">{shows(7.2, clear, cyc)}'
             + text(px, 250, prompt, t["green"], size=15)
             + f'<rect x="{cx:.1f}" y="237" width="9" height="15" fill="{a}">'
             f'<animate attributeName="opacity" values="1;0" dur="1.1s" '
             f'calcMode="discrete" repeatCount="indefinite"/></rect></g>')
    o.append("</svg>")
    return "\n".join(o)


PANELS = {
    "capabilities": capabilities,
    "trajectory": trajectory,
    "roadmap": roadmap,
    "buildlog": buildlog,
    "quote": quote,
}


if __name__ == "__main__":
    for name, fn in PANELS.items():
        for theme, t in THEMES.items():
            with open(f"{name}-{theme}.svg", "w", encoding="utf-8") as f:
                f.write(fn(t))
            print(f"wrote {name}-{theme}.svg")
