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
}


def load(vol):
    v = VOLS[vol]
    src = os.path.join(SERIES, v["dir"], v["src"])
    figdir = os.path.join(HERE, "fig" + vol)
    if src.lower().endswith(".docx"):
        blocks, prof = docx2blocks.convert(src, figdir)
    else:
        import pdf2blocks
        blocks, prof = pdf2blocks.convert(src, figdir)
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
