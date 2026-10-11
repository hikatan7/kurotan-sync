# -*- coding: utf-8 -*-
"""編集した pptx の指定スライドを PDF にし、今の PDF の対応頁と入れ替える。pptx も差し替える。
swap(pptx_new, pptx_dst, pdf_dst, {pdf頁: スライド番号})"""
import os, shutil, fitz, re, difflib
from win32com.client import gencache
H = os.path.dirname(os.path.abspath(__file__))
def swap(pptx_new, pptx_dst, pdf_dst, mapping, tag):
    bk = os.path.join(H, "orig"); os.makedirs(bk, exist_ok=True)
    for f in (pptx_dst, pdf_dst):
        b = os.path.join(bk, tag + "_" + os.path.basename(f))
        if not os.path.exists(b): shutil.copy2(f, b)
    app = gencache.EnsureDispatch("PowerPoint.Application")
    pr = app.Presentations.Open(os.path.abspath(pptx_new), True, False, False)
    tmp = os.path.join(H, tag + "_all.pdf"); pr.SaveAs(tmp, 32); pr.Close()
    allp = fitz.open(tmp); cur = fitz.open(pdf_dst); out = fitz.open()
    for i in range(cur.page_count):
        if (i + 1) in mapping:
            out.insert_pdf(allp, from_page=mapping[i + 1] - 1, to_page=mapping[i + 1] - 1)
        else:
            out.insert_pdf(cur, from_page=i, to_page=i)
    tmp2 = os.path.join(H, tag + "_new.pdf"); out.save(tmp2, garbage=1, deflate=True); out.close(); cur.close()
    # 入れ替えなかった頁が元と同じか
    a = fitz.open(pdf_dst); b = fitz.open(tmp2)
    same = all(re.sub(r"\s", "", a[i].get_text()) == re.sub(r"\s", "", b[i].get_text()) for i in range(a.page_count) if (i + 1) not in mapping)
    a.close(); b.close()
    shutil.copyfile(tmp2, pdf_dst); shutil.copyfile(pptx_new, pptx_dst)
    return same

def same_named(name):
    out = []
    for dp, dn, fn in os.walk(r"C:\Users\junch\OneDrive\_旧デスクトップ"):
        if name in fn and "$Recycle" not in dp: out.append(os.path.join(dp, name))
    return out
def swap_tag(tag):
    import json
    j = json.load(open(os.path.join(H, tag + ".json"), encoding="utf-8"))
    mp = {int(k): v[0] for k, v in j["map"].items()}
    ok = swap(os.path.join(H, tag + "_t.pptx"), j["pptx"], j["pdf"], mp, tag)
    others = [p for p in same_named(os.path.basename(j["pptx"])) if os.path.normcase(p) != os.path.normcase(j["pptx"])]
    for p in others:
        b = os.path.join(H, "orig", tag + "_other_" + os.path.basename(p))
        if not os.path.exists(b): shutil.copy2(p, b)
        shutil.copyfile(os.path.join(H, tag + "_t.pptx"), p)
    return ok, others
