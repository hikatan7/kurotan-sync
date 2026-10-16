# -*- coding: utf-8 -*-
"""シリーズ全巻の PDF から空白ページを洗い出す"""
import glob
import io
import os
import fitz

BASE = (r"C:\Users\junch\OneDrive\デスクトップ\教育ファイル集"
        r"\麻酔科ミニ教科書シリーズ")
out = []
for pdf in sorted(glob.glob(os.path.join(BASE, "*", "*.pdf"))):
    try:
        d = fitz.open(pdf)
    except Exception as e:
        out.append("%s  読めません (%s)" % (pdf, e))
        continue
    blank = [i + 1 for i in range(d.page_count)
             if len(d[i].get_text().strip()) < 3 and not d[i].get_images()]
    rel = os.path.relpath(pdf, BASE)
    out.append("%-58s %4d頁  空白: %s" % (rel, d.page_count, blank or "なし"))
    d.close()
io.open("qa_blank.txt", "w", encoding="utf-8").write("\n".join(out))
print("wrote qa_blank.txt", len(out))
