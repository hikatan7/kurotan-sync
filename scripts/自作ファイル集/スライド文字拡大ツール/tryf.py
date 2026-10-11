import sys, os, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep, relayout
from win32com.client import gencache
from PIL import Image
B = r"C:\Users\junch\OneDrive\_旧デスクトップ"
J = [("教育ファイル集/_PDF（閲覧用）/03_区域麻酔_①専門医版20枚.pdf", 2),
     ("教育ファイル集/麻酔科ミニ教科書シリーズ/_スライド版/_PDF（閲覧用）/10_ICUにおける心房細動_①専門医版20枚.pdf", 15),
     ("教育ファイル集/麻酔科ミニ教科書シリーズ/_スライド版/_PDF（閲覧用）/04_AKIと利尿薬_①専門医版20枚.pdf", 4),
     ("教育ファイル集/麻酔科ミニ教科書シリーズ/_スライド版/_PDF（閲覧用）/04_AKIと利尿薬_②研修医版10枚＋用語解説.pdf", 4)]
app = gencache.EnsureDispatch("PowerPoint.Application"); ims = []
for k, (rel, pn) in enumerate(J):
    pdf = os.path.join(B, os.path.normpath(rel)); pptx = prep.find_pptx(pdf)[0]
    n = prep.mapping(pdf, pptx, [pn])[pn][0]
    src = "m%d_src.pptx" % k; shutil.copyfile(pptx, src)
    json.dump({"pdf": pdf, "pptx": pptx, "map": {str(pn): [n, 1.0]}}, open("m%d.json" % k, "w", encoding="utf-8"), ensure_ascii=False)
    row = []
    for fm in (1.2, 1.35):
        dst = "m%d_%s_t.pptx" % (k, fm); print(k, fm, relayout.main(src, dst, [n], fm))
        pr = app.Presentations.Open(os.path.abspath(dst), True, False, False); p = os.path.abspath("m%d_%s.png" % (k, fm)); pr.Slides(n).Export(p, "PNG", 640, 360); pr.Close(); row.append(Image.open(p))
    ims.append(row)
s = Image.new("RGB", (2 * 644, 4 * 364), "gray")
for i, row in enumerate(ims):
    for j, im in enumerate(row): s.paste(im, (j * 644, i * 364))
s.save("tryf.png")
