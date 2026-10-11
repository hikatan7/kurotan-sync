# -*- coding: utf-8 -*-
"""㊹ 図版の版面検査（figqa を全図に当てる）。name はタプルで渡すこと。"""
import sys
import figqa                      # noqa: F401  （import で save に割り込む）

mods = [__import__(name) for name in ("fig44a",)]
for mod in mods:
    for n in sorted(d for d in dir(mod) if d.startswith("f") and d[1:].isdigit()):
        getattr(mod, n)()

print("\n" + "=" * 66)
if not figqa.report:
    print("版面の問題は検出されなかった。")
else:
    for name, issues in figqa.report:
        print("\n■ %s  （%d件）" % (name, len(issues)))
        for i in issues:
            print("   -", i)
    print("\n合計 %d図 / %d件" % (len(figqa.report),
                                sum(len(i) for _, i in figqa.report)))
sys.exit(1 if figqa.report else 0)
