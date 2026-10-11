import os, sys, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep
from win32com.client import gencache
B = r"C:\Users\junch\OneDrive\_旧デスクトップ\教育ファイル集"
J = [("q0", r"麻酔科ミニ教科書シリーズ\_スライド版\_PDF（閲覧用）\07_麻酔薬理ハンドブック_①専門医版20枚.pdf", 30),
     ("q1", r"麻酔科ミニ教科書シリーズ\_スライド版\_PDF（閲覧用）\08_星状神経節ブロック_②研修医版10枚＋用語解説.pdf", 8),
     ("q2", r"麻酔科ミニ教科書シリーズ\_スライド版\_PDF（閲覧用）\01_麻酔中の輸液管理_ベーシック_①専門医版20枚.pdf", 2),
     ("q3", r"麻酔科ミニ教科書シリーズ\_スライド版\_PDF（閲覧用）\02_麻酔中の輸液管理_アドバンス_①専門医版20枚.pdf", 10),
     ("q4", r"麻酔科ミニ教科書シリーズ\_スライド版\_PDF（閲覧用）\02_麻酔中の輸液管理_アドバンス_①専門医版20枚.pdf", 14),
     ("q5", r"麻酔科ミニ教科書シリーズ\_スライド版\_PDF（閲覧用）\02_麻酔中の輸液管理_アドバンス_①専門医版20枚.pdf", 39),
     ("q6", r"麻酔科ミニ教科書シリーズ\04_AKIと利尿薬\AKIと利尿薬_講義スライド.pdf", 37)]
app = gencache.EnsureDispatch("PowerPoint.Application")
for tag, rel, pn in J:
    pdf = os.path.join(B, rel); pptx = prep.find_pptx(pdf)[0]; n = prep.mapping(pdf, pptx, [pn])[pn][0]
    pr = app.Presentations.Open(pptx, True, False, False); sl = pr.Slides(n)
    shs = [sl.Shapes.Item(i) for i in range(1, sl.Shapes.Count + 1)]
    bot = min([s.Top for s in shs if s.Top > 440] or [525])
    c = [s for s in shs if 90 <= s.Top < bot]
    # x の切れ目
    xs = sorted((s.Left, s.Left + s.Width) for s in c if s.Width < 800)
    segs = []
    for a, b in xs:
        if segs and a < segs[-1][1] + 4: segs[-1][1] = max(segs[-1][1], b)
        else: segs.append([a, b])
    ys = sorted((s.Top, s.Top + s.Height) for s in c)
    ysg = []
    for a, b in ys:
        if ysg and a < ysg[-1][1] + 3: ysg[-1][1] = max(ysg[-1][1], b)
        else: ysg.append([a, b])
    wide = [round(s.Width) for s in c if s.Width >= 800]
    print(tag, "slide", n, "下端", round(bot), "x区間", [[round(a), round(b)] for a, b in segs], "y区間", [[round(a), round(b)] for a, b in ysg], "全幅", wide)
    pr.Close()
    shutil.copyfile(pptx, tag + "_src.pptx")
    json.dump({"pdf": pdf, "pptx": pptx, "pn": pn, "n": n}, open(tag + ".json", "w", encoding="utf-8"), ensure_ascii=False)
