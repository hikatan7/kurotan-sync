# -*- coding: utf-8 -*-
"""流し組み版のビルド：1回目で章の開始頁を測り、目次に入れて2回目を組み、柱とノンブルを入れる。"""
import os, sys, re, subprocess, importlib, shutil
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fitz
import front
from engine import Book

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
MODS = ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8"]
HTML = os.path.join(HERE, "book.html")
RAW = os.path.join(HERE, "book_raw.pdf")
OUT = os.path.join(HERE, "book.pdf")


def build_once():
    import svglib; svglib._FS["n"] = 0
    importlib.reload(front)
    b = Book()
    b.add(front.cover(), "cover")
    b.add(front.toc())
    for m in MODS:
        mod = importlib.import_module(m)
        importlib.reload(mod)
        mod.build(b)
    open(HTML, "w", encoding="utf-8").write(b.render(front.TITLE_MAIN + " ── " + front.TITLE_SUB))
    if os.path.exists(RAW):
        os.remove(RAW)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000",
                    "--print-to-pdf=" + RAW, "--no-pdf-header-footer",
                    "file:///" + HTML.replace("\\", "/")], capture_output=True, timeout=240)
    d = fitz.open("pdf", open(RAW, "rb").read())
    starts = {}
    for i, pg in enumerate(d):
        m = re.search(r"CHAPTER0(\d)", re.sub(r"\s", "", pg.get_text()))
        if m and int(m.group(1)) not in starts and i >= 2:
            starts[int(m.group(1))] = i + 1
    return d, starts


d, starts = build_once()
# 目次の頁を実測値に
s = open(os.path.join(HERE, "front.py"), encoding="utf-8").read()
for n, pgno in starts.items():
    s = re.sub(r'(\(%d, "[^"]*",\s*"[^"]*", )(\d+)(\))' % n, lambda m: m.group(1) + str(pgno) + m.group(3), s)
open(os.path.join(HERE, "front.py"), "w", encoding="utf-8").write(s)
d, starts2 = build_once()
assert starts == starts2, (starts, starts2)

# 柱とノンブル
font = fitz.Font(fontfile=r"C:\Windows\Fonts\YuGothM.ttc")
fontb = fitz.Font(fontfile=r"C:\Windows\Fonts\YuGothB.ttc")
titles = {n: t for n, t, _, _ in front.CHAPTERS}
order = sorted(starts.items(), key=lambda x: x[1])
for i, pg in enumerate(d):
    pno = i + 1
    if pno <= 2:
        continue
    pg.wrap_contents()
    w, h = pg.rect.width, pg.rect.height
    chap = None
    for n, st in order:
        if pno >= st:
            chap = n
    tw = fitz.TextWriter(pg.rect)
    if chap and pno != starts[chap]:
        lab = "第%d章" % chap
        tw.append((48, 30), lab, font=fontb, fontsize=7.8)
        tw.append((48 + fontb.text_length(lab, 7.8) + 6, 30), titles[chap], font=font, fontsize=7.8)
    num = str(pno)
    tw.append(((w - font.text_length(num, 8.5)) / 2, h - 20), num, font=font, fontsize=8.5)
    tw.write_text(pg, color=(0.40, 0.46, 0.54))
    if chap and pno != starts[chap]:
        pg.draw_line((48, 35), (w - 48, 35), color=(0.82, 0.85, 0.89), width=0.4)
d.save(OUT)
print("pages", len(d), "chapters", starts)
