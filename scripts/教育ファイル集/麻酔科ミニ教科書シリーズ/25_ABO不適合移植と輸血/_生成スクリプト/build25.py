# -*- coding: utf-8 -*-
"""㉕ ABO不適合移植と輸血 を組む。体裁は㉒㉓㉔と同じ。"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_restored
import c25_p1
import c25_p2
import col25
from sum25 import SUMMARIES

META = {
    "no": "㉕", "vol": "25",
    "audience": "麻酔科専攻医・専門医のための",
    "title": "ABO不適合移植と輸血",
    "sub": "血液型という圧縮ファイルを、一度だけ解いてみる",
    "compose": "全 5 部・23 章／付録 A〜C",
    "extra": "ABO抗原の生化学・accommodation・製剤選択・PLS・RhD",
    "date": "2026年9月17日",
}

ABBREV = (None,
 ["略語", "英語表記", "日本語表記"],
 [["ABMR", "antibody-mediated rejection", "抗体関連型拒絶"],
  ["ABO", "─", "ABO 血液型（histo-blood group ABO）"],
  ["ADCC", "antibody-dependent cellular cytotoxicity",
   "抗体依存性細胞傷害"],
  ["C4d", "complement component 4d", "補体 C4 の分解産物"],
  ["CD55", "decay accelerating factor（DAF）", "崩壊促進因子"],
  ["CD59", "protectin", "プロテクチン（MAC 阻害因子）"],
  ["DAT", "direct antiglobulin test",
   "直接抗グロブリン試験（直接クームス試験）"],
  ["DFPP", "double filtration plasmapheresis", "二重濾過血漿交換"],
  ["FFP", "fresh frozen plasma", "新鮮凍結血漿"],
  ["FUT1", "fucosyltransferase 1", "フコース転移酵素 1（H 遺伝子）"],
  ["FUT2", "fucosyltransferase 2", "フコース転移酵素 2（Se 遺伝子）"],
  ["GalNAc", "N-acetylgalactosamine", "N-アセチルガラクトサミン"],
  ["HLA", "human leukocyte antigen", "ヒト白血球抗原"],
  ["HSCT", "hematopoietic stem cell transplantation", "造血幹細胞移植"],
  ["IgG", "immunoglobulin G", "免疫グロブリン G"],
  ["IgM", "immunoglobulin M", "免疫グロブリン M"],
  ["IVIG", "intravenous immunoglobulin", "免疫グロブリン大量静注療法"],
  ["LDH", "lactate dehydrogenase", "乳酸脱水素酵素"],
  ["MAC", "membrane attack complex", "膜侵襲複合体（C5b-9）"],
  ["NK 細胞", "natural killer cell", "ナチュラルキラー細胞"],
  ["PAS", "platelet additive solution", "血小板添加液"],
  ["PC", "platelet concentrate", "濃厚血小板"],
  ["PE", "plasma exchange", "血漿交換"],
  ["PLS", "passenger lymphocyte syndrome",
   "パッセンジャーリンパ球症候群"],
  ["RBC", "red blood cell", "赤血球（製剤としては赤血球液）"],
  ["RhAG", "Rh-associated glycoprotein", "Rh 関連糖蛋白"],
  ["RhD", "Rh blood group D antigen", "Rh 血液型 D 抗原"],
  ["TA-GVHD", "transfusion-associated graft-versus-host disease",
   "輸血後移植片対宿主病"],
  ["vWF", "von Willebrand factor", "フォン・ヴィレブランド因子"]])


def main():
    blocks = list(c25_p1.BLOCKS) + list(c25_p2.BLOCKS)
    n0 = len(blocks)
    blocks = col25.apply(blocks)
    print("コラム %d 本" % (len(blocks) - n0))

    keys = {re.sub(r"\s+", "", b[1]) for b in blocks if b[0] == "h2"}
    miss = [k for k in SUMMARIES if k not in keys]
    if miss:
        print("!! まとめのキーが本文に無い:", miss)

    figdir = os.path.join(HERE, "fig")
    want = [b[1] for b in blocks if b[0] == "fig"]
    lost = [f for f in want if not os.path.exists(os.path.join(figdir, f))]
    if lost:
        print("!! 図版が無い:", lost)

    print(dict(collections.Counter(b[0] for b in blocks)))
    blocks = build_restored.rebuild(blocks, SUMMARIES)
    out = os.path.join(os.path.dirname(HERE), "ABO不適合移植と輸血.docx")
    n = build_restored.build(META, blocks, figdir, out, abbrev=ABBREV)
    print("→", os.path.basename(out), n)

    cur, ok, gap = None, False, []
    for b in blocks:
        if b[0] == "h2":
            if cur and not ok:
                gap.append(cur)
            cur, ok = b[1], False
        elif b[0] == "sum" and cur:
            ok = True
    if cur and not ok:
        gap.append(cur)
    print("まとめ無し:", [g[:28] for g in gap])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
