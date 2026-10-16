# -*- coding: utf-8 -*-
"""図版用の最小SVG DSL。すべて viewBox 座標（幅1000固定）で描く。"""
from engine import esc

NAVY, BLUE, RED, GREEN, GOLD = "#1f3a5f", "#2d6a9f", "#a8342a", "#2b6b52", "#8a6d1f"
SUB, LINE, INK = "#5b6b7c", "#c9d3dc", "#16202b"
FILL = {"blue": "#eaf2f9", "red": "#fbeeeb", "green": "#eef7f2",
        "gold": "#faf5e6", "gray": "#f2f5f7", "navy": "#1f3a5f", "white": "#ffffff"}
EDGE = {"blue": "#9dc2dd", "red": "#dfae a5".replace(" ", ""), "green": "#a8cfbb",
        "gold": "#d9c98f", "gray": "#c9d3dc", "navy": "#1f3a5f", "white": "#c9d3dc"}
TXT = {"blue": "#1b4b74", "red": "#8a2b22", "green": "#1e5240", "gold": "#6b5417",
       "gray": "#3f4d5c", "navy": "#ffffff", "white": "#16202b"}

FONT = '"Yu Gothic","Meiryo",sans-serif'


# 図ごとの文字の倍率（figscale.py が実測して figscale.json に書く）。2026-10-08
import os as _os, json as _json, re as _re
_FS_FILE = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "figscale.json")
_FS = {"n": 0}


def _scale_for(i):
    if _os.environ.get("FIGSCALE_ALL"):
        return float(_os.environ["FIGSCALE_ALL"])
    try:
        return float(_json.load(open(_FS_FILE, encoding="utf-8")).get(str(i), 1.0))
    except Exception:
        return 1.0


def svg(w, h, body, pad=0):
    _FS["n"] += 1
    i = _FS["n"]
    k = _scale_for(i)
    if k != 1.0:
        body = _re.sub(r'font-size="([\d.]+)"', lambda m: 'font-size="%.2f"' % (float(m.group(1)) * k), body)
    return (f'<svg data-fig="{i}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family={chr(39)}{FONT}{chr(39)}>'
            f'<defs>{_defs()}</defs>{body}</svg>')


def _defs():
    m = ""
    for name, col in [("ar", SUB), ("arb", BLUE), ("arr", RED), ("arg", GREEN),
                      ("arn", NAVY), ("arw", "#ffffff")]:
        m += (f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
              f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
              f'<path d="M0,1 L10,5 L0,9 z" fill="{col}"/></marker>')
    return m


def t(x, y, s, size=15, col=INK, anchor="start", bold=False, ls=0, op=1):
    b = ' font-weight="700"' if bold else ""
    o = f' opacity="{op}"' if op != 1 else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" '
            f'text-anchor="{anchor}"{b}{l}{o}>{esc(s)}</text>')


def tlines(x, y, lines, size=14, col=INK, anchor="start", lh=18, bold=False):
    return "".join(t(x, y + i * lh, s, size, col, anchor, bold)
                   for i, s in enumerate(lines))


def rect(x, y, w, h, tone="gray", r=6, sw=1.4, dash=None, fill=None, stroke=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="{fill or FILL[tone]}" stroke="{stroke or EDGE[tone]}" '
            f'stroke-width="{sw}"{d}/>')


def cbox(x, y, w, h, lines, tone="gray", size=14, r=6, lh=18, title=None,
         tsize=15, dash=None):
    """中央寄せテキストの箱"""
    s = rect(x, y, w, h, tone, r=r, dash=dash)
    col = TXT[tone]
    n = len(lines) + (1 if title else 0)
    total = (n - 1) * lh
    cy = y + h / 2 - total / 2 + size * 0.36
    i = 0
    if title:
        s += t(x + w / 2, cy, title, tsize, col, "middle", bold=True)
        i = 1
    for j, ln in enumerate(lines):
        s += t(x + w / 2, cy + (i + j) * lh, ln, size, col, "middle")
    return s


def lbox(x, y, w, h, title, lines, tone="gray", size=13, lh=16, tsize=14.5, pad=12):
    """左寄せ・見出し付きの箱"""
    s = rect(x, y, w, h, tone)
    col = TXT[tone]
    s += t(x + pad, y + 20, title, tsize, col, bold=True)
    s += tlines(x + pad, y + 40, lines, size, col if tone == "navy" else INK, lh=lh)
    return s


def arrow(x1, y1, x2, y2, col=SUB, sw=1.8, marker="ar", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" '
            f'stroke-width="{sw}" marker-end="url(#{marker})"{d}/>')


def line(x1, y1, x2, y2, col=LINE, sw=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" '
            f'stroke-width="{sw}"{d}/>')


def path(d, col=SUB, sw=1.8, fill="none", marker=None, dash=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"{m}{da}/>')


def circle(cx, cy, r, tone="gray", sw=1.4, fill=None, stroke=None):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill or FILL[tone]}" '
            f'stroke="{stroke or EDGE[tone]}" stroke-width="{sw}"/>')


def badge(cx, cy, s, tone="navy", r=13, size=13):
    return (circle(cx, cy, r, tone) +
            t(cx, cy + size * 0.36, s, size, TXT[tone], "middle", bold=True))


def caplabel(x, y, s, col=BLUE, size=12.5):
    return t(x, y, s, size, col, bold=True, ls=1.2)


def chain(x, y, w, items, tone="blue", bh=64, gap=34, size=13.5, lh=17):
    """横並びの流れ図。items は [ [line,...], ... ]"""
    n = len(items)
    bw = (w - gap * (n - 1)) / n
    s = ""
    for i, lines in enumerate(items):
        bx = x + i * (bw + gap)
        s += cbox(bx, y, bw, bh, lines, tone, size=size, lh=lh)
        if i < n - 1:
            s += arrow(bx + bw + 7, y + bh / 2, bx + bw + gap - 7, y + bh / 2,
                       BLUE, 2, "arb")
    return s


def vbar(x, y, w, h, segs, size=12):
    """縦の積み上げ棒。segs=[(比率, ラベル, tone)]"""
    s = ""
    cy = y
    tot = sum(a for a, _, _ in segs)
    for i, (a, lab, tone) in enumerate(segs):
        hh = h * a / tot
        s += rect(x, cy, w, hh, tone, r=3)
        s += t(x + w / 2, cy + hh / 2 + size * 0.36, lab, size, TXT[tone], "middle",
               bold=True)
        cy += hh
    return s


def axes(x, y, w, h, xlab="", ylab="", col=SUB):
    s = line(x, y, x, y + h, col, 1.6) + line(x, y + h, x + w, y + h, col, 1.6)
    if xlab:
        s += t(x + w, y + h + 22, xlab, 12.5, col, "end")
    if ylab:
        s += t(x - 4, y - 8, ylab, 12.5, col, "start")
    return s
