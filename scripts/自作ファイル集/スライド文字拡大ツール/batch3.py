import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep
B = r"C:\Users\junch\OneDrive\_旧デスクトップ"
L = json.load(open(r"C:\Users\junch\AppData\Local\Temp\fontscan\step1\pagescan3.json", encoding="utf-8"))
import fitz
SKIP = ("車　有紀", "気道管理コース", "RRS記録", "09_声門上器具", "心臓手術後の心停止")
jobs = []
for p, n, s in L:
    if any(k in p for k in SKIP): continue
    d = fitz.open(os.path.join(B, os.path.normpath(p))); pages = []
    for pn, m in s:
        pg = d[pn - 1]; W = pg.rect.width
        mark = [x for b in pg.get_text("dict")["blocks"] for l in b.get("lines", []) for x in l["spans"] if x["bbox"][1] < 30 and x["bbox"][0] > W - 70 and "/" in x["text"]]
        if mark or pn == 1: continue
        if "ICUにおける心房細動_①" in p and pn == 15: continue
        pages.append(pn)
    if pages: jobs.append((p, pages))
for k, (p, pages) in enumerate(jobs):
    tag = "b3_%02d" % k
    try:
        pdf = os.path.join(B, os.path.normpath(p))
        if not prep.find_pptx(pdf): print(tag, "pptxなし", os.path.basename(p)); continue
        r = prep.run(pdf, pages, tag, 1.6)
        print(tag, os.path.basename(p)[:30], r[1], r[2], flush=True)
    except Exception as e:
        print(tag, "ERR", os.path.basename(p)[:30], repr(e)[:150], flush=True)
