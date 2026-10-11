# -*- coding: utf-8 -*-
"""㊴ 非心臓手術の心血管リスク評価　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr39
import refs39_extra
import refs39
import c39_p1
import c39_p2
import c39_p3

bookkit.REFS = dict(refs39.REFS)
bookkit.REFS.update(refs39_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "非心臓手術の心血管リスク評価.docx")

META = {
    "no": "㊴",
    "vol": "39",
    "audience": "麻酔科専攻医・麻酔科医・外科医・内科医・手術室看護師",
    "title": "非心臓手術の心血管リスク評価",
    "sub": "その検査・その薬で、何が変わるのか",
    "compose": "何を決めるための評価か・リスクを測る・検査・薬・併存疾患・術中と術後",
    "extra": "全26章／図版9点／コラム6本／参考文献45件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c39_p1.BLOCKS + c39_p2.BLOCKS + c39_p3.BLOCKS)


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
    para(doc, "非心臓手術の", size=26, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "心血管リスク評価", size=26, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、心臓以外の手術を受ける患者の"
              "心血管リスクをどう評価し、周術期をどう管理するかである。")
    para(doc, "この領域の評価は、しばしば"
              "「手術をしてよいかどうかを決めるもの」と受け取られている。"
              "しかし実際にそう使われる場面は少ない。"
              "評価が答えているのは、"
              "このまま進めてよいか・進める前に直せるものはあるか・"
              "何を見張り何を準備するか、の三つである。"
              "本書は、この三つを分けたうえで"
              "「その検査・その薬で、何が変わるのか」という問いを"
              "全章に通した。")
    para(doc, "そしてこの領域には、もうひとつ特有の事情がある。"
              "指針の改訂が推奨を反転させることがある、という事情である。"
              "周術期のβ遮断薬、予防的な冠動脈血行再建、"
              "抗凝固薬のヘパリン橋渡し ── "
              "いずれも「良さそうに見えたこと」が検証されて位置づけを変えた。"
              "日本循環器学会の該当ガイドラインは2014年版から"
              "2022年改訂版になっている。"
              "米国版も2024年に10年ぶりの全面改訂を受けた。"
              "手元の資料が何年の版かを、確かめてから読んでほしい。")
    para(doc, "本書はリスク指標の点数ごとの発生率、"
              "ステント留置後の待機週数、抗血栓薬の休薬日数、"
              "バイオマーカーの閾値、術中血圧の目標値、"
              "そして薬剤の投与量を本文に書いていない。"
              "指針の版によって変わってきた数値であり、"
              "数字だけが残ると、古い版の推奨に従い続ける原因になるためである。"
              "何を書かなかったかは付録D-5に、"
              "施設で決めておくべき項目は付録Eにまとめた。")
    para(doc, "心臓手術そのものの術前評価は㉝『心臓麻酔の基礎』が、"
              "脊髄幹麻酔と抗血栓薬の時間関係は⑰『区域麻酔と脊髄幹麻酔』が、"
              "肺高血圧と成人先天性心疾患は㊱が、"
              "そして妊婦の術前評価は㊳『産科麻酔』が扱っている。"
              "呼吸器合併症のリスク評価は本書では扱っていない。")
    para(doc, "図版9点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた（付録F）。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文では、章ごとの初出で「略語（英語表記：日本語表記）」の形に"
              "展開している。以下はその一覧である。")
    table(doc, None, abbr39.ABBREV[0], abbr39.ABBREV[1])

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
