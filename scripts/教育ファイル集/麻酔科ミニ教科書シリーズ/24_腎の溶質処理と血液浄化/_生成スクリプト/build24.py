# -*- coding: utf-8 -*-
"""㉔ 腎の溶質処理と血液浄化 を組む。体裁は㉒㉓と同じ。"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_restored
import c24_p1
import c24_p2
import col24
from sum24 import SUMMARIES

META = {
    "no": "㉔", "vol": "24",
    "audience": "麻酔科専攻医・専門医のための",
    "title": "腎の溶質処理と血液浄化",
    "sub": "分子量・経路と、クレアチニンが語らないこと",
    "compose": "全 5 部・26 章／付録 A〜D",
    "extra": "溶質の物性・尿細管・AKI 回復期・CRRT",
    "date": "2026年9月16日",
}

ABBREV = (None,
 ["略語", "英語表記", "日本語表記"],
 [["AKD", "acute kidney disease", "急性腎臓病"],
  ["AKI", "acute kidney injury", "急性腎障害"],
  ["ADQI", "Acute Disease Quality Initiative", "─"],
  ["ADH", "antidiuretic hormone", "抗利尿ホルモン（バソプレシン）"],
  ["AG", "anion gap", "アニオンギャップ"],
  ["BUN", "blood urea nitrogen", "血中尿素窒素"],
  ["CAVH", "continuous arteriovenous hemofiltration", "持続的動静脈血液濾過"],
  ["CKD", "chronic kidney disease", "慢性腎臓病"],
  ["CMPF", "3-carboxy-4-methyl-5-propyl-2-furanpropionic acid", "─"],
  ["CRRT", "continuous renal replacement therapy", "持続的腎代替療法"],
  ["CVVH", "continuous venovenous hemofiltration", "持続的静静脈血液濾過"],
  ["CVVHD", "continuous venovenous hemodialysis", "持続的静静脈血液透析"],
  ["CVVHDF", "continuous venovenous hemodiafiltration", "持続的静静脈血液濾過透析"],
  ["ENaC", "epithelial sodium channel", "上皮性ナトリウムチャネル"],
  ["FENa", "fractional excretion of sodium", "ナトリウム排泄分画"],
  ["FGF23", "fibroblast growth factor 23", "線維芽細胞増殖因子 23"],
  ["FLC", "free light chain", "遊離軽鎖"],
  ["FST", "furosemide stress test", "フロセミド負荷試験"],
  ["GFR", "glomerular filtration rate", "糸球体濾過量"],
  ["HD", "hemodialysis", "血液透析"],
  ["HDF", "hemodiafiltration", "血液濾過透析"],
  ["HDx", "expanded hemodialysis", "拡大血液透析"],
  ["HCO", "high cut-off", "ハイカットオフ（膜）"],
  ["IL-6", "interleukin-6", "インターロイキン 6"],
  ["KDIGO", "Kidney Disease: Improving Global Outcomes", "─"],
  ["KIM-1", "kidney injury molecule-1", "腎障害分子 1"],
  ["MATE", "multidrug and toxin extrusion protein", "多剤・毒物排出蛋白"],
  ["MCO", "medium cut-off", "ミディアムカットオフ（膜）"],
  ["MRP", "multidrug resistance-associated protein", "多剤耐性関連蛋白"],
  ["MWCO", "molecular weight cut-off", "分子量カットオフ"],
  ["MWRO", "molecular weight retention onset", "分子量遮断開始点"],
  ["NAG", "N-acetyl-β-D-glucosaminidase", "─"],
  ["NaPi-II", "sodium-phosphate cotransporter type II",
   "II 型ナトリウム・リン共輸送体"],
  ["NCC", "sodium-chloride cotransporter", "ナトリウム・塩素共輸送体"],
  ["NGAL", "neutrophil gelatinase-associated lipocalin", "─"],
  ["NHE3", "sodium-hydrogen exchanger 3", "ナトリウム・水素交換体 3"],
  ["NKCC2", "sodium-potassium-2-chloride cotransporter",
   "ナトリウム・カリウム・2 塩素共輸送体"],
  ["OAT", "organic anion transporter", "有機アニオントランスポーター"],
  ["OCT", "organic cation transporter", "有機カチオントランスポーター"],
  ["PTH", "parathyroid hormone", "副甲状腺ホルモン"],
  ["RAAS", "renin-angiotensin-aldosterone system",
   "レニン・アンジオテンシン・アルドステロン系"],
  ["RBP", "retinol binding protein", "レチノール結合蛋白"],
  ["RCA", "regional citrate anticoagulation", "局所クエン酸抗凝固"],
  ["RKF", "residual kidney function", "残存腎機能"],
  ["RRT", "renal replacement therapy", "腎代替療法"],
  ["SCUF", "slow continuous ultrafiltration", "緩徐持続的限外濾過"],
  ["SGLT", "sodium-glucose cotransporter", "ナトリウム・グルコース共輸送体"],
  ["TAL", "thick ascending limb", "（ヘンレ係蹄の）太い上行脚"],
  ["TDM", "therapeutic drug monitoring", "薬物血中濃度モニタリング"],
  ["TRPM6", "transient receptor potential melastatin 6", "─"],
  ["TRPV5", "transient receptor potential vanilloid 5", "─"],
  ["UT-A", "urea transporter A", "尿素輸送体 A"],
  ["β2M", "beta-2 microglobulin", "β2-ミクログロブリン"]])


def main():
    blocks = list(c24_p1.BLOCKS) + list(c24_p2.BLOCKS)
    n0 = len(blocks)
    blocks = col24.apply(blocks)
    print("コラム %d 本" % (len(blocks) - n0))

    keys = {re.sub(r"\s+", "", b[1]) for b in blocks if b[0] == "h2"}
    miss = [k for k in SUMMARIES if k not in keys]
    if miss:
        print("!! まとめのキーが本文に無い:", miss)

    print(dict(collections.Counter(b[0] for b in blocks)))
    blocks = build_restored.rebuild(blocks, SUMMARIES)
    out = os.path.join(os.path.dirname(HERE), "腎の溶質処理と血液浄化.docx")
    n = build_restored.build(META, blocks, os.path.join(HERE, "fig"), out,
                             abbrev=ABBREV)
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
