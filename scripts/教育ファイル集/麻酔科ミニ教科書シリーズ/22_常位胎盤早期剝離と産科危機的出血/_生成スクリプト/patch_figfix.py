# -*- coding: utf-8 -*-
"""figqa.py が拾った版面の不具合をまとめて直す。"""
import io


def ed(path, pairs):
    s = io.open(path, encoding="utf-8").read()
    for a, b in pairs:
        assert a in s, (path, a[:70])
        s = s.replace(a, b, 1)
    io.open(path, "w", encoding="utf-8").write(s)
    print("patched", path)


ed("fig22_a.py", [
    # --- f03：基準域の帯と「200：実務上の分水嶺」が重なっていた
    ('''    for y, lo, hi, col, lab in ((196, 150, 350, "#8d97a3", "非妊娠時の基準域 150–350"),
                                (246, 300, 600, "#2e6da4", "妊娠後期の基準域 300–600")):''',
     '''    for y, lo, hi, col, lab in ((138, 150, 350, "#8d97a3", "非妊娠時の基準域 150–350"),
                                (190, 300, 600, "#2e6da4", "妊娠後期の基準域 300–600")):'''),
    # --- f03：黄信号の帯が明るすぎて白文字が沈んでいた
    ('(200, 300, "#e0b955", "黄信号")', '(200, 300, "#c8971f", "黄信号")'),
])

ed("fig22_b.py", [
    # --- f13：枠の実高を受け取り、注記をその下に置く
    ('''    y2 = y + 210
    textbox(cv, 40, y2, 940,
            ["体重 70 kg、現在 100 mg/dL、目標 200 mg/dL",''',
     '''    y2 = y + 210
    h13 = textbox(cv, 40, y2, 940,
            ["体重 70 kg、現在 100 mg/dL、目標 200 mg/dL",'''),
    ('''    textbox(cv, 1020, y2, 940,
            ["理論上、すでに 3 g では足りない。",''',
     '''    h13 = max(h13, textbox(cv, 1020, y2, 940,
            ["理論上、すでに 3 g では足りない。",'''),
    ('''            14, style="red", title="ここから分かること", title_size=16,
            pad_y=22, min_h=280)

    textbox(cv, 40, y2 + 320, W - 80,''',
     '''            14, style="red", title="ここから分かること", title_size=16,
            pad_y=22, min_h=280))

    textbox(cv, 40, y2 + h13 + 46, W - 80,'''),
    # --- f15：最後の枠が下端からはみ出していた
    ('    cv = Canvas(W, 1350)\n    cv.title(40, 52, "大量輸血戦略の振り子',
     '    cv = Canvas(W, 1700)\n    cv.title(40, 52, "大量輸血戦略の振り子'),
    # --- f16：2行のセルが行高に収まっていなかった
    ('''    y = 165
    for lab, tgt, note, st in rows:
        cv.rect(40, y, 400, 92, fc=FILL[st][1])
        cv.text(240, y + 46, lab, size=14.5, color="white", weight="bold", z=6)
        cv.rect(452, y, 560, 92, fc=FILL[st][0], ec=FILL[st][1], lw=1.3)
        cv.block(468, y + 46 - 26 * tgt.count("\\n") - 13, 528,
                 tgt.split("\\n"), 13.5, color=FILL[st][1], weight="bold")
        cv.text(1036, y + 46, note, size=12.5, color=INK, ha="left")
        y += 102''',
     '''    y = 165
    for lab, tgt, note, st in rows:
        lines = tgt.split("\\n")
        rh = 92 if len(lines) == 1 else 124      # 2行のセルは行高を広げる
        cv.rect(40, y, 400, rh, fc=FILL[st][1])
        cv.text(240, y + rh / 2, lab, size=14.5, color="white",
                weight="bold", z=6)
        cv.rect(452, y, 560, rh, fc=FILL[st][0], ec=FILL[st][1], lw=1.3)
        cv.block(468, y + rh / 2 - 27 * len(lines), 528, lines, 13.5,
                 color=FILL[st][1], weight="bold")
        cv.text(1036, y + rh / 2, note, size=12.5, color=INK, ha="left")
        y += rh + 10'''),
    # --- f17：左の見出しがキャンバスの外へ出ていた
    ('    x0, x1 = 300, 1930\n\n    def px(h):',
     '    x0, x1 = 490, 1930\n\n    def px(h):'),
    ('        cv.text(285, y + 30, lab, size=13.5, color=FILL[st][1],\n'
     '                weight="bold", ha="right")',
     '        cv.text(470, y + 30, lab, size=13.5, color=FILL[st][1],\n'
     '                weight="bold", ha="right")'),
])

# --- 検査側：矢印は枠ではないので、またぎ判定から外す
ed("figqa.py", [
    ('''    patches = []
    for pt in cv.ax.patches:''',
     '''    from matplotlib.patches import FancyArrowPatch
    patches = []
    for pt in cv.ax.patches:
        if isinstance(pt, FancyArrowPatch):    # 矢印は枠ではない
            continue'''),
])
print("all done")
