# -*- coding: utf-8 -*-
"""〔54〕図版の版面検査。"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import figqa                      # noqa: F401
import fig54a as mod
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
