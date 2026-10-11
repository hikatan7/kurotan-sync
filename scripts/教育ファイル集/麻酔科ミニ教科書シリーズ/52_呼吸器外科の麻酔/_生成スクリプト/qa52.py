# -*- coding: utf-8 -*-
"""〔52〕図版の版面検査。"""
import sys
import figqa                      # noqa: F401
for mod in [__import__(n) for n in ("fig52a",)]:
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
sys.exit(1 if figqa.report else 0)
