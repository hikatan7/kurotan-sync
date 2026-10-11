# -*- coding: utf-8 -*-
"""㊸ 麻酔科医の臨床推論　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr44
import refs44_extra
import refs44
import c44_p1
import c44_p2
import c44_p3
import volno

bookkit.REFS = dict(refs44.REFS)
bookkit.REFS.update(refs44_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "麻酔科医の臨床推論.docx")

META = {
    "no": volno.circled(44),
    "vol": "44",
    "audience": "麻酔科専攻医・麻酔科医",
    "title": "麻酔科医の臨床推論",
    "sub": "数字が動いたときに、何を順に考えるか",
    "compose": "考え方の枠組み・数字が動いたとき・像と波形・不確実ななかで決める・決めたあと",
    "extra": "全22章／図版8点／コラム7本／参考文献33件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c44_p1.BLOCKS + c44_p2.BLOCKS + c44_p3.BLOCKS)


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
    para(doc, "麻酔科医の", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "臨床推論", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、手術室で異常に気づいてから動き出すまでの"
              "「考え方」そのものである。")
    para(doc, "内科の臨床推論は、病名にたどり着くことを目標にしている。"
              "麻酔科の推論は、そこが違う。"
              "血圧が落ちたときに最初に知りたいのは病名ではなく、"
              "いま何をすればよいかである。"
              "原因が確定していなくても、"
              "前負荷なのか、後負荷なのか、収縮なのか、リズムなのかが分かれば手は打てる。"
              "そして打った手への反応が、次の推論の材料になる。"
              "つまり麻酔科の推論は、診断してから治療するのではなく、"
              "介入しながら診断を絞るという順序で動いている。")
    para(doc, "本書はこの順序を、三つの問い ── いま危ないか／何が変わったか／"
              "確かめる手はあるか ── に整理したうえで、"
              "手術室で頻繁に立てられる問い（血圧・酸素化・気道内圧・脈・尿量・"
              "乳酸・呼気終末二酸化炭素分圧）を、"
              "臓器別ではなく機序別の「箱」に並べ直している。"
              "箱で並べると、鑑別の各項目がそのまま打つ手に対応し、"
              "空いている箱を見れば「まだ考えていないこと」が分かる。")
    para(doc, "後半は、推論そのものより推論を支える仕組みを扱う ── "
              "情報が足りないまま決めること、検査前確率、思考の型が生む誤り、"
              "そして声に出す・呼ぶ・引き継ぐ・振り返るという行動である。"
              "本書がこれらに紙数を割くのは、"
              "振り返りで最も多い結論が"
              "「診断は間違っていなかったが、たどり着くのが遅かった」だからである。"
              "この形の失敗は、知識を増やしても減らない。")
    para(doc, "本書は、個々の病態の知識を扱わない。"
              "アナフィラキシーの診断と治療は⑯が、急性腎障害は㉓が、"
              "心停止は⑳と㉖が、気道のトラブルは⑬と㉙が、"
              "それぞれ一冊を使って書いている。"
              "本書が扱うのは、その手前 ── どの引き出しを開けるかを決める部分である。"
              "だから本書は既刊への参照が多く、"
              "付録Bの対応表が実質的な骨格になっている。"
              "本書だけでは何も診断できない。")
    para(doc, "本書は、血圧・心拍数・酸素飽和度・体温・乳酸などの具体的な閾値と目標値、"
              "薬剤名と投与量、個々の病態の診断基準と治療手順を本文に書いていない。"
              "何を書かなかったかは付録Cに、"
              "施設で決めておきたい事柄は付録Dにまとめた。"
              "付録Dは、一人で読むより誰かと一緒に読む材料として使ってほしい ── "
              "本書が推奨することの多くは、個人ではなくチームの性質に依存するからである。")
    para(doc, "図版8点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた。"
              "引用した33件は、PubMed の書誌情報と題名を一件ずつ照合して確定している"
              "（書誌が取得できない報告書1件のみ手で記載した）。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文は原則として日本語表記で書いてある。"
              "以下は、同じ事柄を英語の文献で探すときの手がかりである。")
    table(doc, None, abbr44.ABBREV[0], abbr44.ABBREV[1])

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
