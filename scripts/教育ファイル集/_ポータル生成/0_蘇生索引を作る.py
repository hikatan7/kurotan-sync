# -*- coding: utf-8 -*-
"""麻酔資料ポータルの蘇生の部（theme_resus.json）の「本文」行を、今の㉖ docx / PDF から作り直す。
図版・一次資料の行はそのまま残す。
（26_…/_生成スクリプト/portal26.py は古い本文ソースから作るので、2026-10-01 からこちらを使う）
章＝スタイル「21」、節＝「31」、部＝「1」。頁は目次頁を除き、見出しの先頭14字で PDF を探す。"""
import io, json, os, re, sys

import fitz
from docx import Document
from docx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
ED = os.path.dirname(HERE)                      # 教育ファイル集
VD = "麻酔科ミニ教科書シリーズ/26_蘇生アルゴリズムの変遷と周術期心停止/"
STEM = "蘇生アルゴリズムの変遷と周術期心停止"
D = os.path.join(ED, VD, STEM)
JS = os.path.join(HERE, "theme_resus.json")
SKIP = ("本書で使う略語",)


def ptext(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t")))


def sid(p):
    ppr = p.find(qn("w:pPr"))
    if ppr is not None and ppr.find(qn("w:pStyle")) is not None:
        return ppr.find(qn("w:pStyle")).get(qn("w:val"))
    return None


def main():
    doc = Document(D + ".docx")
    chs, cur, part = [], None, ""
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:p"):
            t = ptext(el).strip(); s = sid(el)
            if s == "1":
                part = t; continue
            if s == "21" and t:
                cur = {"title": t, "part": part, "subs": [], "text": []}
                if not t.startswith(SKIP):
                    chs.append(cur)
                continue
            if cur is None or not t:
                continue
            if s == "31":
                cur["subs"].append(t)
            cur["text"].append(t)
        elif el.tag == qn("w:tbl") and cur is not None:
            for tc in el.iter(qn("w:tc")):
                t = ptext(tc).strip()
                if t:
                    cur["text"].append(t)

    pdf = fitz.open(D + ".pdf")
    texts = [("" if p.get_text().count("...") > 3 else re.sub(r"\s+", "", p.get_text())) for p in pdf]
    path0 = "教育ファイル集/" + VD + STEM + ".pdf"
    new = []
    for c in chs:
        key = re.sub(r"\s+", "", c["title"])[:14]
        pg = next((i + 1 for i, t in enumerate(texts) if t and key in t and i >= 3), 0)
        part = c["part"] or "本書の前置き"
        new.append({"kind": "本文", "name": c["title"], "sub": "　/　".join(c["subs"]),
                    "desc": "　".join(c["text"])[:2000],
                    "path": path0 + ("#page=%d" % pg if pg else ""),
                    "meta": "%s・PDF %d 頁" % (part, pg) if pg else part})

    j = json.load(io.open(JS, encoding="utf-8"))
    rest = [r for r in j["rows"] if r["kind"] != "本文"]
    j["rows"] = new + rest
    json.dump(j, io.open(JS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    nopage = [n["name"] for n in new if "#page" not in n["path"]]
    print("蘇生の部：本文 %d 行を作り直しました%s" % (len(new), ("（頁が見つからない章: %s）" % "、".join(nopage)) if nopage else ""))


if __name__ == "__main__":
    main()
