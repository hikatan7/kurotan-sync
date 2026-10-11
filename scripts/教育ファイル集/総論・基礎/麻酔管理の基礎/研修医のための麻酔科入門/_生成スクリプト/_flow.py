# -*- coding: utf-8 -*-
"""1頁ずつ固定して組む engine を、章ごとの流し組みに変え、文字を大きくする（2026-10-08）。"""
import io, re

p = "engine.py"
s = io.open(p, encoding="utf-8").read()

# 1) Book：同じ章の page() は一つの流れにまとめる
old = s[s.index("class Book:"):s.index("TPL = r")]
new = '''class Book:
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


'''
s = s.replace(old, new)

# 2) 用紙：表紙・目次は従来どおり 1 頁、章は余白つきで流す
s = s.replace("@page { size: A4; margin: 0; }",
              "@page { size: A4; margin: 17mm 17mm 16mm 17mm; }\n@page fixed { size: A4; margin: 0; }")
s = s.replace(".page {\n  position: relative; width: 210mm; height: 297mm;",
              ".page { page: fixed;\n  position: relative; width: 210mm; height: 297mm;")
s = s.replace(".page:last-child { page-break-after: auto; }",
              ".page:last-child { page-break-after: auto; }\n"
              ".flow { break-before: page; }\n"
              ".box, figure, .tbl, .keymsg, .th, .abbr, .dl { break-inside: avoid; }\n"
              "h2, h3 { break-after: avoid; }\n"
              ".chead { break-after: avoid; }")

# 3) 文字の大きさ
rep = [
    ("line-height: 1.75; font-size: 10.6pt;", "line-height: 1.78; font-size: 11pt;"),
    ("h2 { font-size:15pt;", "h2 { font-size:15.5pt;"),
    ("h2 .en { display:block; font-size:7.4pt;", "h2 .en { display:block; font-size:8pt;"),
    ("h3 { font-size:11.4pt;", "h3 { font-size:12pt;"),
    (".lead { font-size:11.2pt;", ".lead { font-size:11.6pt;"),
    ("font-weight:700; color:%NAVY%; font-size:9.7pt; }", "font-weight:700; color:%NAVY%; font-size:10.4pt; }"),
    (".dd { flex:1; font-size:9.9pt;", ".dd { flex:1; font-size:10.6pt;"),
    ("margin:1.4mm 0 2.8mm; font-size:9.4pt;", "margin:1.6mm 0 3mm; font-size:10pt;"),
    (".tbl.small { font-size:8.6pt; }", ".tbl.small { font-size:9.6pt; }"),
    ("border:.4pt solid %NAVY%; font-size:9.3pt;", "border:.4pt solid %NAVY%; font-size:10pt;"),
    (".tbl.small th { font-size:8.7pt;", ".tbl.small th { font-size:9.6pt;"),
    (".box-tag { font-size:7.8pt;", ".box-tag { font-size:8.4pt;"),
    (".box-t { font-size:10.4pt;", ".box-t { font-size:11pt;"),
    (".box-b { padding:0 2.6mm 1.9mm; font-size:9.8pt;", ".box-b { padding:0 2.6mm 1.9mm; font-size:10.4pt;"),
    ('monospace; font-size:9.2pt; }', 'monospace; font-size:10pt; }'),
    ("  font-size:9.9pt; font-weight:700; line-height:1.55;", "  font-size:10.6pt; font-weight:700; line-height:1.55;"),
    (".keymsg span { display:inline-block; font-size:7pt;", ".keymsg span { display:inline-block; font-size:7.6pt;"),
    ("font-weight:700; font-size:10.6pt;", "font-weight:700; font-size:11.2pt;"),
    ("margin-bottom:1.4mm; font-size:9.9pt;", "margin-bottom:1.4mm; font-size:10.6pt;"),
    (".abbr { font-size:8.5pt;", ".abbr { font-size:9.2pt;"),
    (".abbr-t { display:inline-block; font-size:7.4pt;", ".abbr-t { display:inline-block; font-size:8pt;"),
    ("figcaption { font-size:8.9pt;", "figcaption { font-size:9.6pt;"),
    (".chead-s { font-size:10pt;", ".chead-s { font-size:10.6pt;"),
]
for a, b in rep:
    assert a in s, a
    s = s.replace(a, b, 1)

# 4) 枠の名前
s = s.replace('"calc":  ("計算してみる",     "box-calc"),', '"calc":  ("計算のしくみ",     "box-calc"),')
io.open(p, "w", encoding="utf-8").write(s)
print("engine ok")
