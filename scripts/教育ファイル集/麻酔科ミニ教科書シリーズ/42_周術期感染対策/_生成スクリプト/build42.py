# -*- coding: utf-8 -*-
"""㊷ 周術期感染対策　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr42
import refs42_extra
import refs42
import c42_p1
import c42_p2
import c42_p3

bookkit.REFS = dict(refs42.REFS)
bookkit.REFS.update(refs42_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "周術期感染対策.docx")

META = {
    "no": "㊷",
    "vol": "42",
    "audience": "麻酔科専攻医・麻酔科医・手術室看護師・感染対策にかかわる人",
    "title": "周術期感染対策",
    "sub": "麻酔科が自分で動かしている四つの場所",
    "compose": "どこにいるのか・手術部位感染・手と作業域・自分が入れるもの・まとめかた",
    "extra": "全20章／図版7点／コラム6本／参考文献31件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c42_p1.BLOCKS + c42_p2.BLOCKS + c42_p3.BLOCKS)


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
    para(doc, "周術期", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "感染対策", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、周術期の感染対策のうち"
              "麻酔科が自分で動かしている部分である。")
    para(doc, "この領域は、しばしば"
              "「手術部位感染は外科の問題、"
              "カテーテル関連感染は病棟の問題」と整理されている。"
              "しかし実際には、麻酔科が直接動かしている場所が四つある ── "
              "抗菌薬の投与時刻と追加投与・体温・血糖・酸素、"
              "自分が入れる血管内カテーテル、"
              "自分が行う脊髄幹麻酔と神経ブロック、"
              "そして自分の手と作業域である。"
              "本書はその四つに絞った。"
              "外科の手技や病棟でのカテーテル管理は扱わない。")
    para(doc, "この領域には、新しい発見がほとんど出てこない。"
              "手指衛生も、抗菌薬を切開前に入れることも、"
              "カテーテル挿入時に清潔野を作ることも、"
              "低体温を避けることも、すでに決着している。"
              "つまり課題は知識ではなく、"
              "知っていることを毎日、全例で、"
              "急いでいるときにも実行できるかどうかである。"
              "だから本書は、実行と体制の話に重心を置いた。")
    para(doc, "一方で、いまも動いている推奨もある ── "
              "吸入酸素濃度、血糖の目標値、手術室の服装。"
              "この二種類を混ぜると議論が噛み合わなくなるため、"
              "各章で「どちらの話か」をできるだけ明示した。")
    para(doc, "本書は抗菌薬の薬剤名・投与量・投与時刻の具体・追加投与の間隔、"
              "血糖と体温の目標値、吸入酸素濃度、"
              "カテーテルの留置期間と被覆材の交換間隔、"
              "器材の再処理の具体的な方法を本文に書いていない。"
              "手術・薬剤・施設・製品で変わり、指針の版でも変わってきたためである。"
              "国内の制度・規則の具体も扱っていない ── "
              "自施設の感染対策マニュアルと感染対策チームに確認すること。"
              "何を書かなかったかは付録C-5に、"
              "施設で決めておくべき項目は付録Dにまとめた。")
    para(doc, "血管確保の手技そのものは⑭『血管確保』と"
              "⑥『中心静脈カテーテル・肺動脈カテーテル』が、"
              "脊髄幹麻酔の手技は⑰『区域麻酔と脊髄幹麻酔』が、"
              "手術室の外での清潔操作は㊵『手術室の外の鎮静』が扱っている。")
    para(doc, "図版7点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた（付録E）。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文では、章ごとの初出で「略語（英語表記：日本語表記）」の形に"
              "展開している。以下はその一覧である。")
    table(doc, None, abbr42.ABBREV[0], abbr42.ABBREV[1])

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
