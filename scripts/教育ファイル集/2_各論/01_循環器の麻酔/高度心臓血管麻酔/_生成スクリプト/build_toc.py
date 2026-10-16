# -*- coding: utf-8 -*-
"""高度心臓血管麻酔　総目次・図版一覧 docx を組む。

各章の PDF から見出しと図の実ページを拾った toc_index.json を使う。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     page_break, heading, figure, table, bullets, summary,
                     note, NAVY, GREY, TEAL)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "高度心臓血管麻酔_総目次と図版一覧.docx")
IDX = json.load(open(os.path.join(HERE, "toc_index.json"), encoding="utf-8"))

TITLES = {
    1: ("第Ⅰ章", "ペースメーカー・ICD と周術期麻酔"),
    2: ("第Ⅱ章", "大血管手術の脳保護"),
    3: ("第Ⅲ章", "脊髄保護と髄液ドレナージ"),
    4: ("第Ⅳ章", "M-TEER と僧帽弁インターベンション"),
    5: ("第Ⅴ章", "TAVI と三尖弁インターベンション"),
    6: ("第Ⅵ章", "透析患者の心大血管手術"),
    7: ("第Ⅶ章", "人工心肺・出血と輸血・循環の目標"),
    8: ("第Ⅷ章", "心臓麻酔と神経モニタリング"),
}

SUB = {
    1: "止めるべきものが二つある",
    2: "方法ではなく、届いているか",
    3: "引き算で守る",
    4: "逆流を止めた瞬間に、条件が変わる",
    5: "開く弁と、閉じない弁",
    6: "腎臓の仕事が、六つ止まっている",
    7: "測れることと、転帰が変わること",
    8: "脳を見る機械と、そのときの麻酔",
}

LEDGER = [
    ["Ⅰ_CIED", "28", "植込み型デバイス、電磁干渉、リード抜去、周術期の設定"],
    ["Ⅱ_大動脈・脳保護", "30", "弓部手術、循環停止、選択的脳灌流、NIRS、送血部位"],
    ["Ⅲ_脊髄保護・CSFD", "40", "対麻痺、髄液ドレナージ、脊髄灌流圧、誘発電位、分節動脈"],
    ["Ⅳ_M-TEER", "40", "僧帽弁逆流、経皮的縁端形成、四つの無作為化試験、TEE"],
    ["Ⅴ_TAVI・構造的心疾患", "30", "大動脈弁、三尖弁、塞栓防止デバイス、右室不全"],
    ["Ⅵ_透析患者", "28", "末期腎不全、カリウム、シャント、腎代替療法、弁の選択"],
    ["Ⅶ_横断（CPB・PBM・TEE）", "14", "人工心肺、患者血液管理、輸血閾値、補助循環"],
    ["Ⅷ_神経モニタリング", "74", "脳波と処理脳波指数、NIRS、自動調節能、術中覚醒、せん妄"],
]


def split_cap(s):
    """「図 1-1　題名」を（図番号, 題名）に分ける"""
    m = re.match(r"^(図\s*[0-9]+-[0-9]+)　?(.*)$", s)
    if m:
        return m.group(1).replace(" ", ""), m.group(2)
    return "", s


def build():
    doc = new_document()
    set_footer(doc, "高度心臓血管麻酔　総目次と図版一覧　　")

    # ---------------- 表紙
    for _ in range(2):
        para(doc)
    para(doc, "高度心臓血管麻酔", size=12, bold=True, color=TEAL,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "全 8 章", size=11, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "麻酔科医・臨床工学技士・手術室看護師", size=13, color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "総目次と図版一覧", size=22, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=6)
    para(doc, "── 263 頁をどこから読むか ──", size=12.5,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc)
    para(doc, "全 8 章・263 頁・図版 115 点・表 20 点",
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "本文の肩付き番号と章末の参考文献一覧で 284 件を引用",
         align=WD_ALIGN_PARAGRAPH.CENTER)
    for _ in range(4):
        para(doc)
    para(doc, "作成日　2026 年 9 月 17 日", color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "静岡市立静岡病院　麻酔科　玉里順子", size=11.5, bold=True,
         color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)

    # ---------------- 本書について
    heading(doc, "本書について", 1)
    para(doc, "本書は、心臓血管麻酔のうち、"
              "教科書の総論では足りない領域を八つ選んで書いたものである。"
              "各章は独立して読めるが、"
              "同じ一つの主題が全章を貫いている。")
    para(doc, "扱わないと決めたことがある。"
              "人工心肺の運転そのもの（回路構成・充填量・流量計算）は"
              "臨床工学技士の領分として扱わない。"
              "薬剤の具体的な投与量も書いていない。"
              "投与量は患者の状態と施設の基準で決まるものであり、"
              "書物が決めるものではないからである。")
    para(doc, "引用は番号方式である。"
              "本文の該当箇所に肩付きの番号を打ち、"
              "各章の最後に番号順の参考文献一覧を置いた。"
              "引用した文献は、著者・雑誌・年・PMID・DOI まで"
              "確認できたものに限った。"
              "確認できなかった資料は、各章の付録に"
              "「確認できなかった資料」として記録し、本文では使っていない。"
              "数値はすべて、抄録の結果・結論の記載から採っている。")

    figure(doc, os.path.join(FIGDIR, "t01_book_map8.png"),
           "図 0-1　本書の八つの章")

    heading(doc, "番号の付け方", 2)
    para(doc, "図は「章番号-通し番号」で付けている。"
              "図 3-12 であれば第Ⅲ章の 12 番目の図である。"
              "アルゴリズム図には、図番号に加えて"
              "「アルゴリズム 1」「アルゴリズム 2」の副題を付けた。")
    para(doc, "本文の肩付き番号は章ごとに 1 から振り直す。"
              "同じ文献が複数の章に出てくるときは、章ごとに別の番号になる。"),
    para(doc, "文献は台帳の S-ID でも管理している。"
              "Ⅷ-14 であれば「Ⅷ_神経モニタリング」シートの 14 番目である。"
              "本文の番号から台帳へ戻るときは、章末の参考文献一覧に"
              "PMID と DOI が書いてあるので、それで引ける。")

    # ---------------- 本書を貫く主題
    heading(doc, "本書を貫く主題", 1)
    para(doc, "八つの章を書き終えて残ったのは、一つの単純な区別である。")
    para(doc, "「それは測れるか」「測れたとして、できることがあるか」"
              "「できたとして、転帰は変わるか」。"
              "この三つは別の問いであり、"
              "前の二つに答えられても、三つ目に答えられるとは限らない。")

    figure(doc, os.path.join(FIGDIR, "t02_thesis.png"),
           "図 0-2　「測れること」「できること」と「転帰が変わること」")

    para(doc, "この一覧で、転帰の側にも届いていたのは最後の一行だけである。"
              "自動調節能を測って、その患者の血圧の目標値を決め、"
              "そこに置き続けたときに、せん妄が減った。")
    para(doc, "違いは介入の形にある。"
              "「異常が出たら戻す」型の介入は、"
              "異常が出た時点ですでに何かが起きているので遅い。"
              "「あらかじめ目標値を決めて、そこに置き続ける」型の介入は、"
              "異常そのものを減らすので間に合う。")
    para(doc, "この表は、モニタを外す理由ではない。"
              "そのモニタが答える問いを決め、"
              "外れたときに誰が何をするかを先に決めておくための表である。")

    note(doc, "各章の付録に共通して置いたもの",
         ["「施設で決めておくこと」── チェックリスト形式。"
          "決めてあれば、その場で議論せずに動ける。",
          "「主要文書の位置づけ」── ガイドラインか、勧告か、監査か。"
          "文書の性格が違えば、使い方も違う。",
          "「確認できなかった資料」── 他の資料に引用されていながら"
          "一次情報に当たれなかったものの記録。"])

    # ---------------- どこから読むか
    heading(doc, "どこから読むか", 1)
    figure(doc, os.path.join(FIGDIR, "t03_how_to_read.png"),
           "図 0-3　三つの入口")

    # ---------------- 全章一覧
    heading(doc, "全 8 章の一覧", 1)
    rows = []
    tot_p = tot_f = tot_t = 0
    for n in range(1, 9):
        d = IDX[str(n)]
        nf = sum(1 for k, _, _ in d["items"] if k == "fig")
        nh1 = sum(1 for k, _, _ in d["items"] if k == "h1")
        nh2 = sum(1 for k, _, _ in d["items"] if k == "h2")
        rows.append([TITLES[n][0], TITLES[n][1], SUB[n],
                     "%d" % d["pages"], "%d/%d" % (nh1, nh2),
                     "%d/%d" % (nf, d["ntbl"])])
        tot_p += d["pages"]
        tot_f += nf
        tot_t += d["ntbl"]
    rows.append(["合計", "8 章", "", "%d" % tot_p, "",
                 "%d/%d" % (tot_f, tot_t)])
    table(doc, "表 0-1　全 8 章の構成",
          ["章", "主題", "この章の一行", "頁", "部/章", "図/表"], rows,
          widths=[1.5, 4.2, 5.3, 1.1, 1.5, 1.4], size=8.6)

    # ---------------- 章別目次
    heading(doc, "章別の目次", 1)
    para(doc, "各章の「部」と「章」の見出しに、その章の中での頁を添えた。"
              "頁は各章の PDF の通し頁である。")

    for n in range(1, 9):
        d = IDX[str(n)]
        h = heading(doc, "%s　%s（%d 頁）" % (TITLES[n][0], TITLES[n][1],
                                            d["pages"]), 2)
        if n > 1:
            h.paragraph_format.page_break_before = True
        rows = []
        for kind, label, pg in d["items"]:
            if kind == "h1":
                rows.append(["■ " + label, str(pg) if pg else "—"])
            elif kind == "h2":
                rows.append(["　" + label, str(pg) if pg else "—"])
        table(doc, None, ["見出し", "頁"], rows,
              widths=[14.8, 1.8], size=8.8)

    # ---------------- 図版一覧
    heading(doc, "図版一覧（115 点）", 1)
    para(doc, "図の題名は、本文中の説明文をそのまま用いている。"
              "頁はその図が置かれている頁である。")
    rows = []
    for n in range(1, 9):
        for kind, label, pg in IDX[str(n)]["items"]:
            if kind != "fig":
                continue
            no, ttl = split_cap(label)
            rows.append([TITLES[n][0], no, ttl, str(pg) if pg else "—"])
    table(doc, "表 0-2　全 115 点の図版",
          ["章", "図番号", "題名", "頁"], rows,
          widths=[1.5, 1.7, 11.6, 1.4], size=8.4)

    # ---------------- 台帳
    heading(doc, "文献台帳の構成", 1)
    para(doc, "本文で数値を引用した文献は、"
              "『高度心臓血管麻酔_SourceLedger_v1.xlsx』にまとめてある。"
              "シートは章に対応し、各行に対象・症例数、介入と比較、"
              "主要結果、教科書での用途、Tier、PMID と DOI のリンクを持つ。")
    table(doc, "表 0-3　文献台帳のシート構成",
          ["シート", "件数", "主な内容"], LEDGER + [["合計", "284", ""]],
          widths=[4.6, 1.6, 10.4], size=8.8)
    para(doc, "このほかに、使い方と集計のシート、検証結果のシート、"
              "図表とアルゴリズムの設計シート、"
              "不足領域と補完のシートがある。"
              "検証結果のシートには、"
              "他の資料に引用されていながら実在を確認できなかった文献と、"
              "誤って帰属されていた文献を記録してある。")

    note(doc, "台帳の Tier の意味",
         ["Tier1　無作為化試験・大規模レジストリ・学会ガイドライン。"
          "本文で数値を断定的に引用してよい。",
          "Tier2　観察研究・小規模試験・系統的レビュー。"
          "条件を添えて引用する。",
          "Tier3　総説・解説・症例報告。"
          "考え方の枠組みとして使い、数値は引用しない。"])

    # ---------------- ファイル一覧
    heading(doc, "ファイル一覧", 1)
    para(doc, "すべて「教育ファイル集\\高度心臓血管麻酔」に置いてある。")
    frows = []
    for n in range(1, 9):
        frows.append(["%s_%s.docx / .pdf" % (TITLES[n][0],
                                             TITLES[n][1].replace("・", "・")),
                      "%d 頁" % IDX[str(n)]["pages"]])
    frows.append(["高度心臓血管麻酔_総目次と図版一覧.docx / .pdf", "本冊子"])
    frows.append(["高度心臓血管麻酔_SourceLedger_v1.xlsx", "文献台帳 284 件"])
    frows.append(["図版（フォルダ）", "PNG 118 点（本文 115 点＋本冊子 3 点）"])
    frows.append(["_生成スクリプト（フォルダ）", "docx と図版の生成・検査用"])
    table(doc, "表 0-4　ファイルの置き場所", ["ファイル", "内容"], frows,
          widths=[11.4, 5.2], size=8.8)

    summary(doc, "この冊子のまとめ",
            ["全 8 章・246 頁・図版 115 点・表 28 点・文献 284 件",
             "各章は独立して読めるが、一つの主題が全章を貫いている",
             "「測れること」「できること」は「転帰が変わること」とは別である",
             "転帰に届いたのは「目標値を先に決めて置き続ける」型の介入だけだった",
             "確認できない資料は書かない。書いたものは出典まで戻れるようにした"])

    drop_orphan_blanks(doc)
    doc.save(OUT)
    return {"pages_total": tot_p, "figs": tot_f, "tbls": tot_t}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(build())
    print("saved:", os.path.abspath(OUT))
