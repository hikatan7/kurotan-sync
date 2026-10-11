import fitz, sys
def med(path):
    d = fitz.open(path); hs = []
    for p in d:
        sc = 595 / p.rect.width
        for b in p.get_text("rawdict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    for c in s["chars"]:
                        if c["c"].strip() and ord(c["c"]) > 0x3000: hs.append((c["bbox"][3] - c["bbox"][1]) * sc)
    hs.sort(); n = len(hs) or 1
    return round(hs[n // 2], 1), round(100 * sum(h < 7.5 for h in hs) / n), d.page_count
if __name__ == "__main__":
    for f in sys.argv[1:]: print(med(f), f)
