# -*- coding: utf-8 -*-
"""1枚のスライドを区画ごとに複数枚へ分け、それぞれ relayout で文字を大きくする。
parts: [(x0, y0, x1, y1), ...]  区画の中心が入る図形を残す。
タイトル類（Top<90）と頁番号（Top>=525）は全部に残す。出典・KEY MESSAGE（Top>=BOT）は最後の1枚だけ。"""
import os, sys, json, shutil
from win32com.client import gencache
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import relayout

TOP = 90


def run(tag, parts, bot, widen=False, fmax=2.0):
    j = json.load(open(tag + ".json", encoding="utf-8"))
    n = j["n"]; dst = os.path.abspath(tag + "_t.pptx"); shutil.copyfile(tag + "_src.pptx", dst)
    app = gencache.EnsureDispatch("PowerPoint.Application")
    pr = app.Presentations.Open(dst, False, False, False)
    W = pr.PageSetup.SlideWidth
    new = []
    for k, (x0, y0, x1, y1) in enumerate(parts):
        sl = pr.Slides(n).Duplicate().Item(1)
        sl.MoveTo(n + 1 + k)
        last = (k == len(parts) - 1)
        for i in range(sl.Shapes.Count, 0, -1):
            s = sl.Shapes.Item(i)
            if s.Top < TOP or s.Top >= 525:
                continue
            if s.Top >= bot:
                if not last: s.Delete()
                continue
            cx, cy = s.Left + s.Width / 2, s.Top + s.Height / 2
            if not (x0 <= cx <= x1 and y0 <= cy <= y1):
                s.Delete()
        kx = (W - 84) / (x1 - x0) if widen else 1.0
        for i in range(1, sl.Shapes.Count + 1):
            s = sl.Shapes.Item(i)
            if s.Top < TOP or s.Top >= bot:
                continue
            s.Top = s.Top - (y0 - 95)
            if widen:
                s.Left = 42 + (s.Left - x0) * kx; s.Width = s.Width * kx
        new.append(n + 1 + k)
    pr.Slides(n).Delete()
    new = [x - 1 for x in new]
    pr.Save(); pr.Close()
    fl = fmax if isinstance(fmax, list) else [fmax] * len(new)
    res = []
    for sn, fm in zip(new, fl):
        res += relayout.main(dst, dst + ".tmp.pptx", [sn], fm)
        shutil.move(dst + ".tmp.pptx", dst)
    j["new"] = new; json.dump(j, open(tag + ".json", "w", encoding="utf-8"), ensure_ascii=False)
    return new, res


def show(tag):
    from PIL import Image
    j = json.load(open(tag + ".json", encoding="utf-8"))
    app = gencache.EnsureDispatch("PowerPoint.Application")
    pr = app.Presentations.Open(os.path.abspath(tag + "_t.pptx"), True, False, False); ims = []
    for n in j["new"]:
        p = os.path.abspath("%s_%d.png" % (tag, n)); pr.Slides(n).Export(p, "PNG", 640, 360); ims.append(Image.open(p))
    pr.Close()
    s = Image.new("RGB", (len(ims) * 644, 360), "gray")
    for i, im in enumerate(ims): s.paste(im, (i * 644, 0))
    s.save(tag + "_split.png")
