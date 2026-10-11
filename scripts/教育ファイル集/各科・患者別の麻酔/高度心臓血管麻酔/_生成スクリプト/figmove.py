# -*- coding: utf-8 -*-
"""図の位置を、後ろの段落いくつ分だけ下げる。

縦長の図が手前のページに入りきらないとき、図の後ろの段落を
図より前に出すと、手前のページの空白が埋まる。
移動できるのは「段落（p）」を越えるときだけで、
見出し・表・まとめ枠・箇条書きは越えない。値は autofit2.py が決める。
"""

MOVE = {
    "f09_oversensing.png": 1,
    "g07_monitors.png": 1,
    "g08_rso2_differential.png": 2,
    "h07_delayed_paraplegia.png": 1,
    "n06_cep.png": 1,
    "n11_rv_failure.png": 1,
    "q10_revascularization_rrt.png": 2,
    "r02_framework.png": 1,
    "r12_alg_bleeding.png": 1,
    "s06_tcd.png": 2,
    "s12_depth_trials.png": 5,
    "s13_volatile_tiva.png": 2,
    "s14_delirium_trials.png": 7,
    "s16_measure_vs_outcome.png": 7,
}


def reorder(blocks):
    out = list(blocks)
    for fn, k in MOVE.items():
        idx = [i for i, b in enumerate(out) if b[0] == "fig" and b[1] == fn]
        if not idx:
            continue
        i = idx[0]
        b = out.pop(i)
        j = i
        moved = 0
        while moved < k and j < len(out) and out[j][0] == "p":
            j += 1
            moved += 1
        out.insert(j, b)
    return out
