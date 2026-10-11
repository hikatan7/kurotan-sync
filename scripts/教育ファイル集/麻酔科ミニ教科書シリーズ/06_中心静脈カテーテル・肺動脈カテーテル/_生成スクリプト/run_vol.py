# -*- coding: utf-8 -*-
"""既刊の docx（または PDF）を、㉒と同じ体裁の docx に組み直す。

    python run_vol.py 01        … 巻01 を作る（scratchpad に v01.docx）

元にするファイルは VOLS に書いてある。docx が最新の巻は docx から、
略語対応前の docx しか無い巻（⑤⑪）は PDF から戻す。
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SERIES = (r"C:\Users\junch\OneDrive\_旧デスクトップ\教育ファイル集"
          r"\麻酔科ミニ教科書シリーズ")

import abbrev
import build_restored
import docx2blocks

# 巻 → (フォルダ, 元ファイル, 表紙の情報)
VOLS = {
    "01": dict(
        dir="01_麻酔中の輸液管理_ベーシック",
        src=r"_空白ページ修正前\麻酔中の輸液管理_ベーシック.docx",
        no="①", title="麻酔中の輸液管理　ベーシック",
        sub="体液生理から尿量の読み方、術中戦略まで",
        audience="麻酔科専攻医のための",
        compose="全 5 部・16 章／付録 A〜E",
        extra="図版 22 点",
    ),
    "02": dict(
        dir="02_麻酔中の輸液管理_アドバンス",
        src=r"_空白ページ修正前\麻酔中の輸液管理_アドバンス.docx",
        no="②", title="麻酔中の輸液管理　アドバンス",
        sub="コロイド・Na・酸塩基・耐容性・大量出血 ── 上限値とその根拠",
        audience="麻酔科専攻医のための",
        compose="全 5 部・付録 A〜D", extra="図版 13 点",
    ),
    "03": dict(
        dir="03_血液製剤とアルブミン",
        src=r"_空白ページ修正前\血液製剤とアルブミン.docx",
        no="③", title="血液製剤とアルブミン",
        sub="袋の中身から、患者の体内で起きることまで",
        audience="麻酔科専攻医のための",
        compose="全 6 部・付録 A〜E", extra="図版 28 点",
    ),
    "04": dict(
        dir="04_AKIと利尿薬",
        src=r"_空白ページ修正前\AKIと利尿薬_専攻医のための教科書.docx",
        no="④", title="AKI における利尿薬の使い方",
        sub="強制利尿からうっ血解除へ：歴史・エビデンス・実践",
        audience="麻酔科専攻医のための",
        compose="全 15 章・付録 A〜D", extra="",
    ),
    "07": dict(
        dir="07_麻酔薬理ハンドブック",
        src=r"_空白ページ修正前\麻酔薬理ハンドブック.docx",
        no="⑦", title="麻酔薬理ハンドブック",
        sub="効くまでの時間と、切れるまでの時間で考える",
        audience="麻酔科専攻医のための",
        compose="全 15 章", extra="図版 26 点",
    ),
    "09": dict(
        dir="09_術中の自己血輸血",
        src=r"_空白ページ修正前\術中の自己血輸血.docx",
        no="⑨", title="術中の自己血輸血",
        sub="回収式・希釈式・貯血式を、適応と算定まで",
        audience="麻酔科専攻医のための",
        compose="全 5 部", extra="",
    ),
    "05": dict(
        dir="05_AKD期管理とCRRT意思決定",
        src=r"_略語対応前\AKD期管理とCRRT意思決定_専門家向け詳細資料.docx",
        abbrev_pdf="AKD期管理とCRRT意思決定_専門家向け詳細資料.pdf",
        no="⑤", title="AKD 期の管理と CRRT をめぐる意思決定",
        sub="始めない／続ける／やめる を、医学的根拠と生命倫理の両輪で",
        audience="専門家向け",
        compose="全 8 章・付録", extra="",
    ),
    "06": dict(
        dir="06_中心静脈カテーテル・肺動脈カテーテル",
        src="中心静脈カテーテル・肺動脈カテーテル完全マニュアル_専門医版.docx",
        no="⑥", title="中心静脈カテーテル・肺動脈カテーテル 完全マニュアル",
        sub="適応・挿入・管理・抜去のすべて",
        audience="専門医向け",
        compose="全 5 部", extra="",
    ),
    "08": dict(
        dir="08_星状神経節ブロック",
        src="星状神経節ブロック_難治性心室性不整脈_専門医向け教科書.docx",
        no="⑧", title="星状神経節ブロック（SGB）",
        sub="難治性心室性不整脈・電気的ストームに対する総合テキスト",
        audience="専門医向け",
        compose="全 9 章・付録", extra="",
    ),
    "10": dict(
        dir="10_ICUにおける心房細動",
        src="ICUにおける心房細動 完全マニュアル.docx",
        no="⑩", title="ICU における心房細動",
        sub="不整脈ではなく、全身病態の表現型として読む",
        audience="専門医向け",
        compose="全 6 部", extra="",
    ),
    "11": dict(
        dir="11_術前評価と麻酔計画",
        src=r"_略語対応前\術前評価と麻酔計画.docx",
        abbrev_pdf="術前評価と麻酔計画.pdf",
        no="⑪", title="術前評価と麻酔計画",
        sub="リスクを言葉にし、計画に変える",
        audience="麻酔科専攻医のための",
        compose="全 5 部・17 章／付録 A〜F", extra="図版 26 点",
    ),
}


def load(vol):
    v = VOLS[vol]
    src = os.path.join(SERIES, v["dir"], v["src"])
    figdir = os.path.join(HERE, "fig" + vol)
    if src.lower().endswith(".docx"):
        blocks, prof = docx2blocks.convert(src, figdir)
    else:
        import pdf2blocks
        figdir = os.path.join(SERIES, v["dir"], "図版")
        blocks, prof = pdf2blocks.convert(src, figdir)

    # ⑤⑪は「略語対応前」の docx しか残っていない。
    # 巻頭一覧を PDF から取り、章ごとの初出展開を掛け直す。
    if v.get("abbrev_pdf"):
        # 配置すると巻フォルダの PDF は新しいものに置き換わるので、
        # 退避してある元の PDF があればそちらを読む。
        stem = os.path.splitext(v["abbrev_pdf"])[0]
        cand = [os.path.join(SERIES, v["dir"], "_旧レイアウト", stem + "_旧.pdf"),
                os.path.join(SERIES, v["dir"], v["abbrev_pdf"])]
        src_pdf = next((c for c in cand if os.path.isfile(c)), cand[-1])
        rows = abbrev.from_pdf(src_pdf)
        if rows:
            blocks = abbrev.expand(blocks, rows)
            prof["abbrev"] = ("tbl", ["略語", "英語", "日本語"], rows, None)
            print("略語 %d 件を展開" % len(rows))
    # 巻ごとの増補（addNN.py）があれば適用する
    try:
        add = __import__("add" + vol)
    except ImportError:
        add = None
    if add:
        n0 = len(blocks)
        blocks = add.apply(blocks)
        print("増補 %d ブロックを追加" % (len(blocks) - n0))
    return v, blocks, prof, figdir


def main(vol, summaries=None):
    v, blocks, prof, figdir = load(vol)
    print("元: %s" % v["src"])
    print("本文 %.1fpt  %s" % (prof["body"],
                              dict(collections.Counter(b[0] for b in blocks))))
    blocks = build_restored.rebuild(blocks, summaries or {})
    meta = {
        "no": v["no"], "vol": str(int(vol)), "audience": v["audience"],
        "title": v["title"], "sub": v["sub"], "compose": v["compose"],
        "extra": v["extra"], "date": "2026年9月14日",
    }
    out = os.path.join(HERE, "v%s.docx" % vol)
    n = build_restored.build(meta, blocks, figdir, out,
                             abbrev=prof.get("abbrev"))
    print("→ %s  %s" % (os.path.basename(out), n))


def summaries_for(vol):
    """sumNN.py があれば、補ったまとめとして読み込む。"""
    try:
        mod = __import__("sum" + vol)
    except ImportError:
        return {}
    return mod.SUMMARIES


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1], summaries_for(sys.argv[1]))
