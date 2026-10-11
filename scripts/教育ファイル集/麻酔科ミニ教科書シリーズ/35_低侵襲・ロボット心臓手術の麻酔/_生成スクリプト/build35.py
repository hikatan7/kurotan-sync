# -*- coding: utf-8 -*-
"""㉞ 心臓麻酔の緊急と補助循環　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr35
import refs35_extra
import refs35
import c35_p1
import c35_p2
import c35_p3

bookkit.REFS = dict(refs35.REFS)
bookkit.REFS.update(refs35_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "低侵襲・ロボット心臓手術の麻酔.docx")

META = {
    "no": "㉟",
    "vol": "35",
    "audience": "麻酔科専攻医・麻酔科医・臨床工学技士・手術室看護師",
    "title": "低侵襲・ロボット心臓手術の麻酔",
    "sub": "小さい創のぶん、仕事は麻酔側へ移る",
    "compose": "何が変わるのか・分離肺換気・末梢からの送脱血・ロボット固有の問題・術後まで",
    "extra": "全24章／図版9点／コラム7本／参考文献37件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c35_p1.BLOCKS + c35_p2.BLOCKS + c35_p3.BLOCKS)


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
    para(doc, "低侵襲・ロボット心臓手術の", size=24, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "麻酔", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、胸骨を全部切らずに行う心臓手術の麻酔である。"
              "右小開胸、内視鏡、ロボット支援 ── "
              "どれも患者にとっては創が小さくなる手術だが、"
              "麻酔科にとっては仕事が増える手術でもある。")
    para(doc, "増える理由ははっきりしている。"
              "術者が胸骨を開けない分、"
              "肺を虚脱させ、末梢から送脱血し、"
              "器具を TEE で誘導し、体表から除細動する ── "
              "その仕事が麻酔科と臨床工学技士へ移るからである。"
              "本書は「術者が失ったものを、どこで誰が補うか」という"
              "一本の軸で全章を通した。"
              "施設ごとに手順は違う。自施設の手順書と読み合わせて使ってほしい。")
    para(doc, "本書は一回換気量・呼気終末陽圧・酸素濃度の値、"
              "送血圧・脱血の陰圧・灌流量の設定、胸腔内送気圧の上限、"
              "そして薬剤の投与量を本文に書いていない。"
              "術式・装置・施設・症例で変わり、"
              "数字だけが一人歩きしやすいためである。"
              "何を書かなかったかは付録C-5に、"
              "施設で決めておくべき項目は付録Dにまとめた。")
    para(doc, "土台となる心臓麻酔の基礎 ── 弁膜症の血行動態、TEE、"
              "人工心肺の生理、離脱の順番 ── は"
              "㉝『心臓麻酔の基礎』が扱っている。"
              "止血と輸血は㉛『心臓麻酔の止血戦略』、"
              "大血管の神経保護は㉜『大血管手術の脳・脊髄保護』、"
              "急変と補助循環は㉞『心臓麻酔の緊急と補助循環』、"
              "そして経カテーテル治療（TAVI・M-TEER）や"
              "ペースメーカー・透析患者などは"
              "院内資料『高度心臓血管麻酔』の各章にまとまっている。"
              "本書はその隣に「小さい創の手術」を置く巻である。")
    para(doc, "図版9点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた（付録E）。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文では、章ごとの初出で「略語（英語表記：日本語表記）」の形に"
              "展開している。以下はその一覧である。")
    table(doc, None, abbr35.ABBREV[0], abbr35.ABBREV[1])

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
