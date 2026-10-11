# -*- coding: utf-8 -*-
"""ch8.py の表セル内で、リテラル改行になってしまった箇所を \n エスケープに戻す。"""
import io, re

PAIRS = [
    ("Duke Activity Status Index\nデューク活動状態指数",
     "Duke Activity Status Index\\nデューク活動状態指数"),
    ("Revised Cardiac Risk Index\n改訂心臓リスク指数",
     "Revised Cardiac Risk Index\\n改訂心臓リスク指数"),
    ("Hugh-Jones classification\nヒュー・ジョーンズ分類",
     "Hugh-Jones classification\\nヒュー・ジョーンズ分類"),
    ("Clinical Frailty Scale\n臨床虚弱スケール／Fried基準",
     "Clinical Frailty Scale\\n臨床虚弱スケール／Fried基準"),
    ("Cause・GFR・Albuminuria\n原因＋濾過能＋アルブミン尿",
     "Cause・GFR・Albuminuria\\n原因＋濾過能＋アルブミン尿"),
    ("Child-Pugh classification\n肝硬変の機能的重症度分類",
     "Child-Pugh classification\\n肝硬変の機能的重症度分類"),
    ("Model for End-stage Liver Disease-Sodium\n終末期肝疾患モデル（Na補正）",
     "Model for End-stage Liver Disease-Sodium\\n終末期肝疾患モデル（Na補正）"),
]

p = "ch8.py"
s = io.open(p, encoding="utf-8").read()
n = 0
for a, b in PAIRS:
    if a in s:
        s = s.replace(a, b)
        n += 1
    else:
        print("MISS:", a.split("\n")[0])
io.open(p, "w", encoding="utf-8").write(s)
print("fixed", n, "/", len(PAIRS))
