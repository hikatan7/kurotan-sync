# -*- coding: utf-8 -*-
"""㊸ 術後鎮痛と体幹の区域麻酔　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr48
import refs48_extra
import refs48
import c48_p1
import c48_p2
import c48_p3
import volno

bookkit.REFS = dict(refs48.REFS)
bookkit.REFS.update(refs48_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "術後鎮痛と体幹の区域麻酔.docx")

META = {
    "no": volno.circled(48),
    "vol": "48",
    "audience": "麻酔科専攻医・麻酔科医・病棟/手術室看護師",
    "title": "術後鎮痛と体幹の区域麻酔",
    "sub": "薬を選ぶのではなく、時間と場所を設計する",
    "compose": "術後鎮痛という設計・土台をつくる・体幹の区域麻酔・組み立てと運用",
    "extra": "全18章／図版7点／コラム1本／参考文献17件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c48_p1.BLOCKS + c48_p2.BLOCKS + c48_p3.BLOCKS)


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
    para(doc, "術後鎮痛と", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "体幹の区域麻酔", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、術後鎮痛の設計と、体幹の区域麻酔である。")
    para(doc, "術後鎮痛の話は、たいてい薬の名前から始まる。"
              "しかし手術室を出たあとに患者が痛がっているとき、"
              "原因が「薬の選択を間違えた」ことであるのは、実は多くない。"
              "多いのは設計の問題である ── "
              "効き始める時刻がずれている、"
              "ブロックが切れる時間帯に次の手が置かれていない、"
              "病棟で実行できない指示になっている、"
              "副作用で結局使えていない。"
              "つまり術後鎮痛は、薬を選ぶ仕事ではなく、"
              "時間と場所を設計する仕事である。")
    para(doc, "この巻には、もう一つの軸がある ── 痛みを三つに分けることである。"
              "体性痛、内臓痛、神経障害性の痛み。"
              "この区別が実務で効くのは、"
              "筋膜面ブロックが内臓痛に届かないという一点による。"
              "腹壁のブロックを入れたのに患者が痛がるとき、"
              "「ブロックが効いていない」のか"
              "「ブロックが届かない痛みが残っている」のか ── "
              "この二つは次の手がまったく違う。")
    para(doc, "そして目標は「痛みをゼロにする」ことではない。"
              "ゼロにするにはオピオイドを増やすしかなく、"
              "増やせば眠くなり、吐き、腸が動かなくなり、結局は回復が遅れる。"
              "術後回復強化の枠組みが示したのは、"
              "鎮痛の目標が動けることにあるという見方である ── "
              "咳ができる、深呼吸ができる、座れる、歩ける。"
              "この順に達成できているかを見れば、鎮痛が足りているかが判断できる。")
    para(doc, "本書は薬剤名・用量・濃度・投与速度を書かない。"
              "ブロックの穿刺部位と描出も扱わない ── "
              "手技は⑰『区域麻酔と脊髄幹麻酔』が、"
              "局所麻酔薬中毒は⑯が、それぞれ一冊を使って書いている。"
              "何を書かなかったかは付録Cに、"
              "施設で決めておきたい事柄は付録Dにまとめた。"
              "付録Dは、病棟と一緒に読む材料として作ってある ── "
              "手術室で完璧な鎮痛を作っても、病棟で実行されなければ意味がないからである。")
    para(doc, "図版7点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた。"
              "引用した17件は、"
              "PubMed の書誌情報と題名を一件ずつ照合して確定している。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文は原則として日本語表記で書いてある。"
              "以下は、同じ事柄を英語の文献で探すときの手がかりである。")
    table(doc, None, abbr48.ABBREV[0], abbr48.ABBREV[1])

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
