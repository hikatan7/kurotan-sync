# -*- coding: utf-8 -*-
"""縦長の図で生じる「ページ末の大きな空白」を、図の幅を実測で縮めて詰める。

buildN.py → PDF → 空白検出 → figwidths.W を書き換え、を数回まわす。
"""
import io, os, re, sys, glob, importlib
import fitz
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
FIGDIR = os.path.join(BASE, "図版")
BOT = 785.0          # 本文下端(pt)  A4 29.7cm - 下余白 2.0cm
PT = 28.3465         # 1cm
CAP = 46.0           # 図キャプション＋前後の空き(pt)
MINW, MAXW = 11.6, 16.0
GAP_MIN = 150.0      # これ以上の空白を「詰めるべき空白」とみなす

NAMES = {
 1: "第Ⅰ章_ペースメーカー・ICDと周術期麻酔",
 2: "第Ⅱ章_大血管手術の脳保護",
 3: "第Ⅲ章_脊髄保護と髄液ドレナージ",
 4: "第Ⅳ章_M-TEERと僧帽弁インターベンション",
 5: "第Ⅴ章_TAVIと三尖弁インターベンション",
 6: "第Ⅵ章_透析患者の心大血管手術",
 7: "第Ⅶ章_人工心肺・出血と輸血・循環の目標",
 8: "第Ⅷ章_心臓麻酔と神経モニタリング",
}

def norm(s):
    return re.sub(r"\s+", "", s)

def fig_map():
    """キャプション(空白除去) -> 図ファイル名"""
    m = {}
    for n in range(1, 9):
        for part in ("p1", "p2"):
            mod = importlib.import_module("c%d_%s" % (n, part))
            for b in mod.BLOCKS:
                if b[0] == "fig":
                    m[norm(b[2])] = b[1]
    return m

def aspect(name):
    with Image.open(os.path.join(FIGDIR, name)) as im:
        return im.height / im.width

def scan(pdf, capmap):
    """(空白pt, 次ページ先頭の図ファイル名) の一覧"""
    out = []
    d = fitz.open(pdf)
    for i in range(len(d) - 1):
        bl = [b for b in d[i].get_text("blocks") if b[1] < 760]
        if not bl:
            continue
        gap = BOT - max(b[3] for b in bl)
        if gap < GAP_MIN or i < 4:
            continue
        nxt = d[i + 1]
        tb = [b for b in nxt.get_text("blocks") if b[4].strip() and b[1] < 760]
        im = [g["bbox"] for g in nxt.get_image_info()]
        if not tb or not im:
            continue
        head = min(tb, key=lambda b: b[1])
        top_img = min(im, key=lambda b: b[1])
        if top_img[1] > head[1]:      # 図より前に本文がある＝送られた図ではない
            continue
        key = norm(head[4])
        for k, v in capmap.items():
            if key.startswith(k[:18]):
                out.append((i + 1, gap, v))
                break
    d.close()
    return out

def main(rounds=3):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.path.insert(0, HERE)
    capmap = fig_map()
    import figwidths
    cur = dict(figwidths.W)
    for r in range(rounds):
        changed = 0
        total_gap = 0.0
        report = []
        for n, nm in NAMES.items():
            pdf = os.path.join(BASE, nm + ".pdf")
            hits = scan(pdf, capmap)
            for pageno, gap, fn in hits:
                total_gap += gap
                a = aspect(fn)
                w_cm = (gap - CAP) / a / PT
                w_cm = min(MAXW, w_cm)
                now = cur.get(fn, MAXW)
                if w_cm >= MINW and w_cm < now - 0.15:
                    cur[fn] = round(w_cm, 2)
                    changed += 1
                    report.append("  ch%d p%-3d gap=%3.0f  %-38s %.1f→%.2fcm"
                                  % (n, pageno, gap, fn, now, w_cm))
                else:
                    report.append("  ch%d p%-3d gap=%3.0f  %-38s 縮小不可(%.2f)"
                                  % (n, pageno, gap, fn, w_cm))
        print("--- round %d : 空白ページ %d 箇所 / 合計 %.0fpt" % (r + 1, len(report), total_gap))
        print("\n".join(report))
        if not changed:
            print("=> これ以上は詰められない。終了。")
            break
        write(cur)
        rebuild()
    return cur

def write(cur):
    src = ['# -*- coding: utf-8 -*-',
           '"""図版ごとの版面上の幅（cm）。既定は 16.0。',
           '',
           '縦に長い図はページに入りきらず次ページへ送られ、',
           '手前のページに大きな空白が残る。その図だけを少し縮めて',
           '手前のページに収める。値は autofit.py が実測して書き戻す。',
           '"""',
           '',
           'W = {']
    for k in sorted(cur):
        src.append('    "%s": %.2f,' % (k, cur[k]))
    src.append('}')
    io.open(os.path.join(HERE, "figwidths.py"), "w", encoding="utf-8").write("\n".join(src) + "\n")

def rebuild():
    import subprocess
    for n in range(1, 9):
        subprocess.run([sys.executable, "build%d.py" % n], cwd=HERE,
                       capture_output=True)
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File",
                    os.path.join(HERE, "to_pdf_all.ps1")], cwd=HERE)

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
