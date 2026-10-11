# -*- coding: utf-8 -*-
"""㉟ 図版の版面検査（figqa を全図に当てる）。"""
import sys
import figqa

mods = []
for name in ("fig35a", "fig35b"):
    try:
        mods.append(__import__(name))
    except ImportError:
        pass

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
