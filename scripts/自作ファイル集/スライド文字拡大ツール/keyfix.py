import os, sys, json, shutil
from win32com.client import gencache
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from relayout import runs, need_h
def fix(src, dst, n):
    shutil.copyfile(src, dst)
    app = gencache.EnsureDispatch("PowerPoint.Application")
    pr = app.Presentations.Open(os.path.abspath(dst), False, False, False); sl = pr.Slides(n)
    shs = [sl.Shapes.Item(i) for i in range(1, sl.Shapes.Count + 1)]
    src_t = [s for s in shs if s.HasTextFrame and s.TextFrame2.HasText and s.TextFrame2.TextRange.Text.startswith("出典")][0]
    key = [s for s in shs if s.HasTextFrame and s.TextFrame2.HasText and s.TextFrame2.TextRange.Text.startswith("KEY MESSAGE")][0]
    bar = [s for s in shs if not (s.HasTextFrame and s.TextFrame2.HasText) and abs(s.Top - key.Top) < 2 and s.Width > key.Width][0]
    for r in runs(src_t): r.Font.Size = r.Font.Size * 12.0 / 8.0 if r.Font.Size < 10 else r.Font.Size
    src_t.TextFrame2.AutoSize = 0; src_t.Height = need_h(src_t)
    k = 18.0 / max(r.Font.Size for r in runs(key))
    for r in runs(key): r.Font.Size = round(r.Font.Size * k * 2) / 2
    key.TextFrame2.AutoSize = 0
    top = src_t.Top + src_t.Height + 10
    key.Top = top; key.Height = max(need_h(key) + 12, 40); bar.Top = top; bar.Height = key.Height
    pr.Save(); pr.Close()
if __name__ == "__main__":
    for tag in sys.argv[1:]:
        j = json.load(open(tag + ".json", encoding="utf-8")); n = list(j["map"].values())[0][0]
        fix(tag + "_src.pptx", tag + "_t.pptx", n); print(tag, n)
