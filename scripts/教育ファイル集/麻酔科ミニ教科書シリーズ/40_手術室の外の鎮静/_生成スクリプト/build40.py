# -*- coding: utf-8 -*-
"""㊵ 手術室の外の鎮静　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr40
import refs40_extra
import refs40
import c40_p1
import c40_p2
import c40_p3

bookkit.REFS = dict(refs40.REFS)
bookkit.REFS.update(refs40_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "手術室の外の鎮静.docx")

META = {
    "no": "㊵",
    "vol": "40",
    "audience": "麻酔科専攻医・麻酔科医・内視鏡/検査室の医師・看護師・救急医",
    "title": "手術室の外の鎮静",
    "sub": "難しさは手技ではなく、状況のほうにある",
    "compose": "場所が変わるということ・始める前に・薬・起きたときと終わったあと・体制",
    "extra": "全22章／図版7点／コラム6本／参考文献27件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c40_p1.BLOCKS + c40_p2.BLOCKS + c40_p3.BLOCKS)


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
    para(doc, "手術室の外の", size=28, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "鎮静", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、手術室の外で行われる鎮静である。"
              "内視鏡室、放射線検査室、カテーテル室、歯科、救急外来、"
              "そして病棟の処置室 ── "
              "鎮静が行われる場所は広く、"
              "そして多くの場合そこに麻酔科医はいない。")
    para(doc, "この領域は、麻酔科にとって"
              "「簡単な仕事」として扱われがちである。"
              "全身麻酔より薬の量が少なく、気道も確保しない ── "
              "だから難しくないはずだ、という理屈である。"
              "しかし実際には、難しさの多くは手技ではなく状況のほうにある。"
              "モニタが少ない。人手が読めない。患者に手が届かない。"
              "情報が足りない。"
              "そして、深くなったときに戻す手段が近くにない。")
    para(doc, "だから本書は、薬の話より段取りの話が多くなった。"
              "誰が見るか、何をそろえるか、"
              "どこまでの深さをどこで行うか、困ったときに誰を呼ぶか ── "
              "これらが決まっていれば、薬の選択は後から調整できる。"
              "施設ごとに体制は違う。自施設の取り決めと読み合わせて使ってほしい。")
    para(doc, "本書は鎮静薬の投与量と投与速度、絶飲食の具体的な時間、"
              "監視の間隔、帰宅までの観察時間、そして拮抗薬の用量を"
              "本文に書いていない。"
              "薬剤・患者・処置・施設で変わり、"
              "数字だけが一人歩きしやすいためである。"
              "第18章で触れる国内の制度上の扱いについても、"
              "点数・要件・時間区分の具体は書いていない ── "
              "本書の記述は算定や請求の根拠として用いるものではなく、"
              "最新の通知と自施設の医事担当に必ず確認していただきたい。"
              "何を書かなかったかは付録C-5に、"
              "施設で決めておくべき項目は付録Dにまとめた。")
    para(doc, "気道管理そのものは⑬『気道管理』と"
              "㉙『声門上器具と周術期気道トラブル』が、"
              "局所麻酔薬中毒とアナフィラキシーは⑯ が、"
              "そして術前の心血管リスク評価は"
              "㊴『非心臓手術の心血管リスク評価』が扱っている。"
              "小児の処置鎮静、集中治療室での人工呼吸中の鎮静、"
              "緩和ケアにおける鎮静は、本書の対象外である。")
    para(doc, "図版7点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた（付録E）。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文では、章ごとの初出で「略語（英語表記：日本語表記）」の形に"
              "展開している。以下はその一覧である。")
    table(doc, None, abbr40.ABBREV[0], abbr40.ABBREV[1])

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
