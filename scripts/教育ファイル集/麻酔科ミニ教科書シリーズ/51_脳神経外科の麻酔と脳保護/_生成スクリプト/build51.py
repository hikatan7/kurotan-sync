# -*- coding: utf-8 -*-
"""㊸ 脳神経外科の麻酔と脳保護　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr51
import refs51_extra
import refs51
import c51_p1
import c51_p2
import volno

bookkit.REFS = dict(refs51.REFS)
bookkit.REFS.update(refs51_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "脳神経外科の麻酔と脳保護.docx")

META = {
    "no": volno.circled(51),
    "vol": "51",
    "audience": "麻酔科専攻医・麻酔科医・手術室看護師",
    "title": "脳神経外科の麻酔と脳保護",
    "sub": "守れるのは、避けられる悪化を避けることである",
    "compose": "脳という臓器・開頭手術・急性期の脳・まわりの話",
    "extra": "全18章／図版6点／コラム2本／参考文献15件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c51_p1.BLOCKS + c51_p2.BLOCKS)


def build():
    doc = new_document()
    set_footer(doc, "麻酔科ミニ教科書シリーズ %s　%s　　"
               % (META["no"], META["title"]))

    # ---- 表紙
    for _ in range(2):
        para(doc)
    para(doc, "麻酔科ミニ教科書シリーズ　%s" % META["no"], size=12, bold=True,
         color=TEAL, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "第 %s 巻" % META["vol"], size=11, color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, META["audience"], size=12, color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "脳神経外科の麻酔と", size=26, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "脳保護", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    para(doc, "── %s ──" % META["sub"], size=12.5,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc)
    para(doc, META["compose"], align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, META["extra"], align=WD_ALIGN_PARAGRAPH.CENTER)
    for _ in range(4):
        para(doc)
    para(doc, "作成日　%s" % META["date"], color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "静岡市立静岡病院　麻酔科　玉里順子", size=11.5, bold=True,
         color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ---- 目次
    h = para(doc, "目　次", size=16, bold=True, color=NAVY,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    h.paragraph_format.page_break_before = True
    toc_field(doc)

    # ---- 前置き
    h = para(doc, "本書の立場と限界", size=14, bold=True, color=NAVY,
             space_after=6)
    h.paragraph_format.page_break_before = True
    para(doc, "本書が扱うのは、脳神経外科の手術の麻酔と、"
              "そこで言われる「脳保護」の中身である。")
    para(doc, "㊸『腹部・一般外科麻酔』は「腹腔という閉じた空間」を軸にした。"
              "頭蓋は、それよりもさらに厳密に閉じている ── 骨で囲まれ、容積が変わらない。"
              "中身は脳実質・血液・脳脊髄液の三つで、合計が一定なので、"
              "どれかが増えればほかのどれかが減らなければならない。"
              "この単純な関係が、この領域の麻酔のほぼすべてを規定している。")
    para(doc, "そこから出てくるのが脳灌流圧という考え方である ── "
              "入口の動脈圧から、出口の頭蓋内圧を引いたもの。"
              "実務で効くのは、麻酔科がこの式の両側を動かせるという点にある。"
              "そして頭蓋内圧を上げてしまう操作 ── 気道の刺激、換気の不足、"
              "頸部の屈曲、高い呼気終末陽圧、頭低位 ── は、"
              "どれも日常的に行っているものである。"
              "脳神経外科の麻酔では、普段は意識しない手順の一つ一つに理由がついてくる。")
    para(doc, "「脳を守る」という言葉は、本書では三つに分けた ── "
              "灌流を保つ、需要を減らす、二次的な傷害を避ける。"
              "このうち臨床で最も確かなのは三つめである。"
              "「脳を守る薬」は長く探され、前臨床では有望な結果が多数得られ、"
              "そして臨床試験のほとんどが失敗した（第17章）。"
              "本書が地味な内容に終始しているのは、そのためである ── "
              "いま確実に効くと分かっているのは、避けられる悪化を避けることだけである。")
    para(doc, "本書は目標値を一切書いていない。"
              "この領域では目標値の議論が活発で、"
              "病態ごとに、指針の版ごとに変わってきたためである。"
              "薬剤名と用量、手技も扱わない ── "
              "脳血流の生理そのものは㊺『周術期生理学』第16章に、"
              "大血管手術での脳・脊髄保護は㉜に置いた。"
              "何を書かなかったかは付録Cに、"
              "施設で決めておきたい事柄は付録Dにまとめた。")
    para(doc, "なお本巻から、巻番号の表記が変わっている。"
              "Unicode の丸数字は㊿（50）で打ち止めで、"
              "51 以降に相当する文字が存在しないためである。"
              "本書では亀甲括弧を用いて〔51〕と表記した（暫定）。")
    para(doc, "図版6点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた。"
              "引用した15件は、"
              "PubMed の書誌情報と題名を一件ずつ照合して確定している。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文は原則として日本語表記で書いてある。"
              "以下は、同じ事柄を英語の文献で探すときの手がかりである。")
    table(doc, None, abbr51.ABBREV[0], abbr51.ABBREV[1])

    n = {"fig": 0, "tbl": 0, "sum": 0, "note": 0, "col": 0, "p": 0,
         "ch": 0, "ul": 0}
    col_no = [0]
    prev = None
    for b in BLOCKS:
        k = b[0]
        if k == "h1":
            hh = heading(doc, b[1], 1)
            hh.paragraph_format.page_break_before = True
        elif k == "h2":
            hh = heading(doc, b[1], 2)
            n["ch"] += 1
            if str(b[1]).startswith(("付録", "おわりに")) and prev != "h1":
                hh.paragraph_format.page_break_before = True
        elif k == "h3":
            heading(doc, b[1], 3)
        elif k == "p":
            para(doc, b[1])
            n["p"] += 1
        elif k == "ul":
            bullets(doc, b[1])
            n["ul"] += 1
        elif k == "fig":
            p = os.path.join(FIGDIR, b[1])
            if os.path.exists(p):
                figure(doc, p, b[2])
                n["fig"] += 1
            else:
                print("!! missing figure:", b[1])
        elif k == "tbl":
            table(doc, None, b[1], b[2])
            n["tbl"] += 1
        elif k == "sum":
            summary(doc, b[1], b[2])
            n["sum"] += 1
        elif k == "note":
            note(doc, b[1], b[2])
            n["note"] += 1
        elif k == "col":
            col_no[0] += 1
            column(doc, col_no[0], b[2], b[3])
            n["col"] += 1
        elif k == "refs":
            n["refs"] = references(doc)
        else:
            print("!! unknown block:", k)
        prev = k

    drop_orphan_blanks(doc)
    doc.save(OUT)
    return n


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(build())
    print("saved:", os.path.abspath(OUT))
