# -*- coding: utf-8 -*-
import os, sys, subprocess, glob, importlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from engine import Book
import front

OUT_HTML = os.path.join(HERE, "book.html")
OUT_PDF = os.path.join(HERE, "book.pdf")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

MODS = ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8"]


def main():
    b = Book()
    b.add(front.cover(), "cover")
    b.add(front.toc())
    for m in MODS:
        if not os.path.exists(os.path.join(HERE, m + ".py")):
            continue
        mod = importlib.import_module(m)
        importlib.reload(mod)
        mod.build(b)
    html = b.render(front.TITLE_MAIN + " ── " + front.TITLE_SUB)
    open(OUT_HTML, "w", encoding="utf-8").write(html)
    print("pages(source):", len(b.pages))

    if os.path.exists(OUT_PDF):
        os.remove(OUT_PDF)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=8000",
                    f"--print-to-pdf={OUT_PDF}", "--no-pdf-header-footer",
                    "file:///" + OUT_HTML.replace("\\", "/")],
                   capture_output=True, timeout=180)
    import fitz
    d = fitz.open(OUT_PDF)
    print("pages(pdf):   ", d.page_count)
    # 溢れ検出：各ページの本文最下端
    for i, pg in enumerate(d):
        blocks = pg.get_text("blocks")
        if not blocks:
            print(f"  p{i+1}: EMPTY")
            continue
        cb = [bb for bb in blocks if not bb[4].strip().isdigit()]
        if not cb: continue
        maxy = max(bb[3] for bb in cb)
        top, bot = 62.0, 805.0
        fill = (maxy - top) / (bot - top) * 100
        flag = "OVER " if maxy > 805 else ("thin " if fill < 88 else "     ")
        print(f"  p{i+1:>3}: {flag}fill={fill:5.1f}%  maxY={maxy:.0f}")
    d.close()


if __name__ == "__main__":
    main()
