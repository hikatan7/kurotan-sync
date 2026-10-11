# -*- coding: utf-8 -*-
"""初期研修医のための麻酔科読本 — レンダリング基盤

ページは「流し込み」ではなく1ページ＝1ユニットで明示的に組む。
これにより総ページ数がソース側で確定する（溢れるとページ数が増えるので検出できる）。
"""
import html as _h

# ── 配色 ─────────────────────────────────────────
INK   = "#16202b"
SUB   = "#5b6b7c"
NAVY  = "#1f3a5f"
BLUE  = "#2d6a9f"
RED   = "#a8342a"
GREEN = "#2b6b52"
GOLD  = "#8a6d1f"
LINE  = "#c9d3dc"
PAPER = "#ffffff"

def esc(s):
    return _h.escape(s, quote=False)

def md(s):
    """**太字** と `強調` と ^上付き^ を最小限に解釈する。"""
    import re
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r'<span class="hl">\1</span>', s)
    s = re.sub(r"\^(.+?)\^", r"<sup>\1</sup>", s)
    s = re.sub(r"~(.+?)~", r"<sub>\1</sub>", s)
    s = s.replace("\n", "<br>")
    return s

# ── ブロック要素 ──────────────────────────────────
def h2(t, en=""):
    e = f'<span class="en">{esc(en)}</span>' if en else ""
    return f'<h2>{e}{md(t)}</h2>'

def h3(t):
    return f'<h3>{md(t)}</h3>'

def p(t):
    return f'<p>{md(t)}</p>'

def lead(t):
    return f'<p class="lead">{md(t)}</p>'

def ul(items, tight=False):
    li = "".join(f"<li>{md(i)}</li>" for i in items)
    return f'<ul class="{"tight" if tight else ""}">{li}</ul>'

def ol(items):
    li = "".join(f"<li>{md(i)}</li>" for i in items)
    return f"<ol>{li}</ol>"

def dl(pairs):
    """▸ 用語 — 説明 の定義リスト"""
    rows = "".join(
        f'<div class="dlrow"><span class="dt">{md(a)}</span><span class="dd">{md(b)}</span></div>'
        for a, b in pairs)
    return f'<div class="dl">{rows}</div>'

def table(head, rows, widths=None, small=False):
    w = ""
    if widths:
        w = "<colgroup>" + "".join(f'<col style="width:{x}">' for x in widths) + "</colgroup>"
    th = "".join(f"<th>{md(c)}</th>" for c in head)
    tb = "".join("<tr>" + "".join(f"<td>{md(c)}</td>" for c in r) + "</tr>" for r in rows)
    cls = "tbl small" if small else "tbl"
    return f'<table class="{cls}">{w}<thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table>'

# ── コラム枠 ──────────────────────────────────────
_BOX = {
    "mech":  ("しくみ",          "box-mech"),
    "pearl": ("ここが効く",       "box-pearl"),
    "pit":   ("ここを間違える",   "box-pit"),
    "col":   ("コラム",           "box-col"),
    "hist":  ("歴史",             "box-hist"),
    "calc":  ("計算のしくみ",     "box-calc"),
    "case":  ("症例",             "box-case"),
    "qa":    ("Q&A",              "box-qa"),
    "note":  ("補足",             "box-note"),
}

def box(kind, title, body, items=None):
    label, cls = _BOX[kind]
    inner = ""
    if body:
        inner += "".join(f"<p>{md(x)}</p>" for x in ([body] if isinstance(body, str) else body))
    if items:
        inner += ul(items, tight=True)
    return (f'<div class="box {cls}"><div class="box-h">'
            f'<span class="box-tag">{esc(label)}</span>'
            f'<span class="box-t">{md(title)}</span></div>'
            f'<div class="box-b">{inner}</div></div>')

def keymsg(t):
    return f'<div class="keymsg"><span>KEY</span>{md(t)}</div>'

def takehome(items):
    li = "".join(f'<li><span class="n">{i+1:02d}</span>{md(x)}</li>' for i, x in enumerate(items))
    return f'<div class="th"><div class="th-h">この章の要点</div><ol class="th-l">{li}</ol></div>'

def fig(svg, cap):
    return f'<figure>{svg}<figcaption>{md(cap)}</figcaption></figure>'

def abbr(items):
    """初出の略語を「略語 ＝ 英語正式名称（日本語名称）」の形で並べる帯。

    図や表のなかで初めて出た略語は、本文に括弧書きを差し込むより
    このほうが読みやすく、版面も食わない。
    """
    s = "".join(f'<span class="ab-i"><b>{esc(a)}</b> ＝ {esc(e)}（{esc(j)}）</span>'
                for a, e, j in items)
    return f'<div class="abbr"><span class="abbr-t">初出の略語</span>{s}</div>'

# ── ページ ────────────────────────────────────────
class Book:
    def __init__(self):
        self.pages = []          # (html, cls)
        self._chap = None

    def add(self, html, cls=""):
        self.pages.append((html, cls))
        self._chap = None

    def page(self, chap, chaptitle, blocks):
        body = "".join(blocks)
        if self._chap == chap and self.pages:
            h, c = self.pages[-1]
            self.pages[-1] = (h + body, c)
        else:
            self.pages.append((body, "flow"))
            self._chap = chap

    def render(self, title):
        secs = "".join(f'<section class="page {c}">{h}</section>' if c != "flow"
                       else f'<section class="flow">{h}</section>' for h, c in self.pages)
        return TPL.replace("__TITLE__", esc(title)).replace("__BODY__", secs)


TPL = r"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>__TITLE__</title>
<style>
@page { size: A4; margin: 17mm 17mm 16mm 17mm; }
@page fixed { size: A4; margin: 0; }
* { box-sizing: border-box; margin:0; padding:0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "Yu Gothic","Yu Gothic UI","Meiryo",sans-serif;
  color: %INK%; background:#fff;
  font-feature-settings: "palt" 1;
  line-height: 1.78; font-size: 11pt;
}
.page { page: fixed;
  position: relative; width: 210mm; height: 297mm;
  padding: 16mm 17mm 13mm 17mm; overflow: visible;
  page-break-after: always; break-after: page;
}
.page:last-child { page-break-after: auto; }
.flow { break-before: page; }
.refs { margin:2mm 0 0 6mm; font-size:9pt; line-height:1.5; color:%INK%; }
.refs li { margin-bottom:1.2mm; text-align:left; overflow-wrap:anywhere; }
.box, figure, .tbl, .keymsg, .th, .abbr, .dl { break-inside: avoid; }
h2, h3 { break-after: avoid; }
.chead { break-after: avoid; }

/* 柱とノンブル */
.run { position:absolute; top:8.5mm; left:17mm; right:17mm;
  display:flex; gap:8px; align-items:baseline;
  font-size:7.6pt; color:%SUB%; letter-spacing:.04em;
  border-bottom:.4pt solid %LINE%; padding-bottom:2mm; }
.run-c { color:%NAVY%; font-weight:700; }
.run-t { color:%SUB%; }
.pn { position:absolute; bottom:7mm; left:0; right:0; text-align:center;
  font-size:8pt; color:%SUB%; letter-spacing:.08em; }
.body { margin-top:4mm; }

/* 見出し */
h2 { font-size:15.5pt; line-height:1.44; color:%NAVY%; font-weight:700;
  margin: 0 0 2.6mm; letter-spacing:.01em; }
h2 .en { display:block; font-size:8pt; letter-spacing:.16em; color:%BLUE%;
  font-weight:700; margin-bottom:.8mm; font-family:"Segoe UI",sans-serif; }
h2 + p, h2 + .lead { margin-top:0; }
h3 { font-size:12pt; color:%INK%; font-weight:700; margin:3.4mm 0 1.4mm;
  padding-left:2.6mm; border-left:2.4pt solid %BLUE%; line-height:1.4; }
p { margin: 0 0 2.5mm; text-align:justify; }
.lead { font-size:11.6pt; color:%NAVY%; line-height:1.7; margin-bottom:3mm;
  font-weight:600; }
.hl { background:linear-gradient(transparent 62%, #ffe9a8 62%); font-weight:700; }
b { font-weight:700; }
sup,sub{ font-size:.68em; }

/* リスト */
ul { margin:0 0 2.4mm; padding-left:0; list-style:none; }
ul li { position:relative; padding-left:3.8mm; margin-bottom:1.3mm; text-align:justify; }
ul li:before { content:"—"; position:absolute; left:0; color:%BLUE%; }
ul.tight li { margin-bottom:.5mm; }
ol { margin:0 0 2.4mm; padding-left:5.2mm; }
ol li { margin-bottom:1.3mm; text-align:justify; }

/* 定義リスト */
.dl { margin:0 0 2.4mm; }
.dlrow { display:flex; gap:2.4mm; padding:.9mm 0; border-bottom:.35pt dotted %LINE%; }
.dt { flex:0 0 34mm; font-weight:700; color:%NAVY%; font-size:10.4pt; }
.dd { flex:1; font-size:10.6pt; text-align:justify; }

/* 表 */
.tbl { width:100%; border-collapse:collapse; margin:1.6mm 0 3mm; font-size:10pt;
  line-height:1.52; }
.tbl.small { font-size:9.6pt; }
.tbl th { background:%NAVY%; color:#fff; font-weight:700; text-align:left;
  padding:1.6mm 2.1mm; border:.4pt solid %NAVY%; font-size:10pt; letter-spacing:.02em; }
.tbl.small th { font-size:9.6pt; padding:1.4mm 1.7mm; }
.tbl td { padding:1.6mm 2.1mm; border:.4pt solid %LINE%; vertical-align:top; }
.tbl.small td { padding:1.3mm 1.7mm; }
.tbl tbody tr:nth-child(even) td { background:#f5f8fa; }

/* コラム枠 */
.box { margin:2.4mm 0 2.8mm; border-radius:1.4mm; overflow:hidden;
  border:.5pt solid %LINE%; }
.box-h { display:flex; gap:2.4mm; align-items:baseline; padding:1.7mm 2.6mm; }
.box-tag { font-size:8.4pt; font-weight:700; letter-spacing:.1em;
  padding:.4mm 1.8mm; border-radius:.8mm; white-space:nowrap; }
.box-t { font-size:11pt; font-weight:700; line-height:1.42; }
.box-b { padding:0 2.6mm 1.9mm; font-size:10.4pt; line-height:1.68; }
.box-b p { margin-bottom:1.2mm; }
.box-b p:last-child { margin-bottom:0; }
.box-b ul li:before { content:"·"; font-weight:700; }

.box-mech  { border-color:#b9d3e6; background:#f2f8fc; }
.box-mech  .box-tag{ background:#2d6a9f; color:#fff; } .box-mech .box-t{ color:#1b4b74; }
.box-pearl { border-color:#b6d8c6; background:#f2faf5; }
.box-pearl .box-tag{ background:#2b6b52; color:#fff; } .box-pearl .box-t{ color:#1e5240; }
.box-pit   { border-color:#e8bdb6; background:#fdf4f2; }
.box-pit   .box-tag{ background:#a8342a; color:#fff; } .box-pit .box-t{ color:#8a2b22; }
.box-col   { border-color:#ddd4c0; background:#fbf8f1; }
.box-col   .box-tag{ background:#8a6d1f; color:#fff; } .box-col .box-t{ color:#6b5417; }
.box-hist  { border-color:#ddd4c0; background:#faf7f0; }
.box-hist  .box-tag{ background:#7a6647; color:#fff; } .box-hist .box-t{ color:#5e4f38; }
.box-calc  { border-color:#cfd6c2; background:#f8faf3; }
.box-calc  .box-tag{ background:#5c6b3f; color:#fff; } .box-calc .box-t{ color:#485433; }
.box-calc  .box-b { font-family:"Consolas","Yu Gothic",monospace; font-size:10pt; }
.box-case  { border-color:#c5cfd8; background:#f7f9fb; }
.box-case  .box-tag{ background:#41586e; color:#fff; } .box-case .box-t{ color:#2f4459; }
.box-qa    { border-color:#c9c3dd; background:#f7f6fc; }
.box-qa    .box-tag{ background:#54488a; color:#fff; } .box-qa .box-t{ color:#413672; }
.box-note  { border-color:%LINE%; background:#f7f9fa; }
.box-note  .box-tag{ background:#5b6b7c; color:#fff; } .box-note .box-t{ color:#3f4d5c; }

/* KEY */
.keymsg { margin:2.4mm 0 0; padding:1.9mm 2.8mm; background:%NAVY%; color:#fff;
  font-size:10.6pt; font-weight:700; line-height:1.55; border-radius:1.2mm; }
.keymsg span { display:inline-block; font-size:7.6pt; letter-spacing:.14em;
  background:#fff; color:%NAVY%; padding:.2mm 1.4mm; border-radius:.6mm;
  margin-right:2.4mm; vertical-align:.6mm; }

/* 要点 */
.th { border:.8pt solid %NAVY%; border-radius:1.4mm; overflow:hidden; margin:3mm 0 0; }
.th-h { background:%NAVY%; color:#fff; font-weight:700; font-size:11.2pt;
  padding:1.6mm 2.6mm; letter-spacing:.06em; }
.th-l { list-style:none; padding:2mm 2.6mm; margin:0; }
.th-l li { position:relative; padding-left:8.4mm; margin-bottom:1.4mm; font-size:10.6pt;
  line-height:1.62; text-align:justify; }
.th-l li:last-child { margin-bottom:0; }
.th-l .n { position:absolute; left:0; top:.2mm; font-size:8pt; font-weight:700;
  color:#fff; background:%BLUE%; border-radius:.7mm; padding:.1mm 1.2mm;
  font-family:"Segoe UI",sans-serif; }

/* 初出略語の帯 */
.abbr { font-size:9.2pt; line-height:1.58; color:%SUB%; margin:1.6mm 0 2.6mm;
  padding:1.4mm 2.4mm; background:#f5f8fa; border-left:2.4pt solid %BLUE%;
  border-radius:.8mm; overflow-wrap:anywhere; }
.ab-i { display:inline-block; margin-right:5mm; }
.abbr b { color:%NAVY%; font-weight:700; }
.abbr-t { display:inline-block; font-size:8pt; font-weight:700; letter-spacing:.08em;
  color:#fff; background:%BLUE%; border-radius:.6mm; padding:.2mm 1.4mm;
  margin-right:2.4mm; vertical-align:.4mm; }

/* 図 */
figure { margin:2.6mm 0 3mm; }
figure svg { display:block; width:100%; height:auto; }
figcaption { font-size:9.6pt; color:%SUB%; margin-top:1.2mm; line-height:1.5;
  padding-left:.5mm; border-left:2pt solid %LINE%; padding-left:2mm; }

/* 表紙 */
.cover { padding:0; }
.cv { position:absolute; inset:0; display:flex; flex-direction:column; }
.cv-top { flex:0 0 74mm; background:%NAVY%; color:#fff; padding:22mm 20mm 0; }
.cv-series { font-size:8.6pt; letter-spacing:.24em; opacity:.82; }
.cv-en { font-size:8pt; letter-spacing:.3em; opacity:.55; margin-top:1.5mm;
  font-family:"Segoe UI",sans-serif; }
.cv-mid { flex:1; padding:16mm 20mm 0; }
.cv-title { font-size:29pt; font-weight:700; color:%NAVY%; line-height:1.34;
  letter-spacing:.01em; }
.cv-sub { font-size:12.4pt; color:%BLUE%; margin-top:5mm; font-weight:600;
  line-height:1.6; }
.cv-rule { width:38mm; height:2.4pt; background:%BLUE%; margin:8mm 0 7mm; }
.cv-note { font-size:9.6pt; color:%SUB%; line-height:1.85; }
.cv-bot { flex:0 0 96mm; padding:0 20mm 16mm; display:flex; flex-direction:column;
  justify-content:flex-end; }
.cv-chaps { font-size:9.4pt; color:#5b6b7c; line-height:2.3; letter-spacing:.02em;
  border-left:2.4pt solid #2d6a9f; padding-left:5mm; margin-bottom:9mm; }
.cv-meta { font-size:9.6pt; color:%INK%; line-height:1.9; border-top:.6pt solid %LINE%;
  padding-top:5mm; }
.cv-sig { font-size:11.6pt; font-weight:700; color:%NAVY%; margin-top:1.5mm; }

/* 目次 */
.toc-h { font-size:19pt; font-weight:700; color:%NAVY%; letter-spacing:.02em; }
.toc-h .en { display:block; font-size:7.6pt; letter-spacing:.28em; color:%BLUE%;
  margin-bottom:1.2mm; font-family:"Segoe UI",sans-serif; }
.toc-lead { font-size:9.8pt; color:%SUB%; margin:3mm 0 6mm; line-height:1.75;
  text-align:justify; }
.toc-i { display:flex; gap:4mm; padding:2.6mm 0; border-bottom:.4pt dotted %LINE%; }
.toc-n { flex:0 0 15mm; font-size:8.4pt; font-weight:700; color:#fff; background:%NAVY%;
  height:6.4mm; border-radius:.8mm; display:flex; align-items:center;
  justify-content:center; letter-spacing:.04em; }
.toc-b { flex:1; }
.toc-t { font-size:11.4pt; font-weight:700; color:%INK%; line-height:1.42; }
.toc-d { font-size:8.8pt; color:%SUB%; margin-top:.8mm; line-height:1.55; }
.toc-p { flex:0 0 12mm; text-align:right; font-size:9pt; color:%SUB%;
  font-family:"Segoe UI",sans-serif; padding-top:.6mm; }
.toc-foot { margin-top:6mm; font-size:8.6pt; color:%SUB%; line-height:1.7;
  border-top:.5pt solid %LINE%; padding-top:3.4mm; text-align:justify; }

/* 章扉の帯 */
.chead { background:%NAVY%; color:#fff; border-radius:1.6mm; padding:5mm 6mm;
  margin-bottom:4mm; }
.chead-n { font-size:7.6pt; letter-spacing:.24em; opacity:.72;
  font-family:"Segoe UI",sans-serif; }
.chead-t { font-size:18pt; font-weight:700; line-height:1.36; margin-top:1.4mm; }
.chead-s { font-size:10.6pt; opacity:.86; margin-top:2.6mm; line-height:1.66; }

.cols2 { display:flex; gap:4mm; }
.cols2 > * { flex:1; min-width:0; }
</style></head><body>
__BODY__
</body></html>"""

for k, v in [("%INK%", INK), ("%SUB%", SUB), ("%NAVY%", NAVY), ("%BLUE%", BLUE),
             ("%LINE%", LINE)]:
    TPL = TPL.replace(k, v)
