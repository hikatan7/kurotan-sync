# -*- coding: utf-8 -*-
"""㉓ 急性腎障害（AKI）を組む。

本文は c23_p1 / c23_p2、章のまとめは sum23 にある。
体裁は㉒以降と同じ（bookkit ＋ build_restored）。
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESTORE = os.path.join(os.path.dirname(HERE), "restore")
sys.path.insert(0, RESTORE)
sys.path.insert(0, HERE)

import build_restored
import c23_p1
import c23_p2
import col23
from sum23 import SUMMARIES

META = {
    "no": "㉓", "vol": "23",
    "audience": "麻酔科専攻医・専門医のための",
    "title": "急性腎障害（AKI）",
    "sub": "流入・腎実質・流出で読み解く",
    "compose": "全 6 部・25 章／付録 A〜D",
    "extra": "機序・病態生理・phenotype・治療・エビデンス",
    "date": "2026年9月14日",
}


def main():
    blocks = list(c23_p1.BLOCKS) + list(c23_p2.BLOCKS)
    n0 = len(blocks)
    blocks = col23.apply(blocks)
    print("コラム %d 本" % (len(blocks) - n0))
    # 数式などの囲みは、注意書きと同じ見た目に寄せる
    blocks = [("note", b[1], b[2]) if b[0] == "boxed" else b for b in blocks]

    keys = {__import__("re").sub(r"\s+", "", b[1]) for b in blocks if b[0] == "h2"}
    miss = [k for k in SUMMARIES if k not in keys]
    if miss:
        print("!! まとめのキーが本文に無い:", miss)

    print(dict(collections.Counter(b[0] for b in blocks)))
    blocks = build_restored.rebuild(blocks, SUMMARIES)
    out = os.path.join(RESTORE, "v23.docx")
    n = build_restored.build(META, blocks, os.path.join(HERE, "fig"), out)
    print("→", os.path.basename(out), n)

    # まとめが付いていない章を出す
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
    print("まとめ無し:", [g[:24] for g in gap])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
