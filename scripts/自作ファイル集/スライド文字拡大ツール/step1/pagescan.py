import json, os, fitz, sys
BASE = r"C:\Users\junch\OneDrive\_旧デスクトップ"; ED = os.path.join(BASE, "教育ファイル集")
paths = set()
def walk(o):
    if isinstance(o, dict): [walk(v) for v in o.values()]
    elif isinstance(o, list): [walk(v) for v in o]
    elif isinstance(o, str) and o.lower().split('#')[0].endswith('.pdf'): paths.add(o.split('#')[0])
walk(json.load(open(os.path.join(ED, '_portal_data.json'), encoding='utf-8')))
walk(json.load(open(os.path.join(ED, '_ポータル生成', 'theme_resus.json'), encoding='utf-8')))
out = []
for p in sorted(paths):
    f = os.path.join(BASE, os.path.normpath(p))
    if not os.path.exists(f) or "_教材化待ち" in p or "_原典資料" in p or "JSCVA" in p: continue
    d = fitz.open(f); small = []
    for i, pg in enumerate(d):
        W = pg.rect.width; sc = 595 / W if W < 1000 or pg.rect.height < W else 595 / W
        if pg.rect.height > pg.rect.width and W > 700: sc = 1  # A3縦などは実寸
        hs = []
        for b in pg.get_text("rawdict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    for c in s["chars"]:
                        if c["c"].strip() and ord(c["c"]) > 0x3000: hs.append((c["bbox"][3] - c["bbox"][1]) * sc)
        if len(hs) < 30: continue
        hs.sort(); m = hs[len(hs) // 2]
        if m < 8.0: small.append((i + 1, round(m, 1)))
    if small: out.append((p, d.page_count, small))
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for p, n, s in out: print(len(s), "/", n, p.split("/")[-1][:50], s[:8])
