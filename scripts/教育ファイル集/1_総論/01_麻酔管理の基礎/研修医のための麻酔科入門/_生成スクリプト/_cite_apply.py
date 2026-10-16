# -*- coding: utf-8 -*-
"""_cite_plan.py の割り当てを本文に入れ、初出順に番号を振り、巻末の参考文献を作る。"""
import io, os, re, json, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _cite_plan import PLAN, REFS

C = json.load(open(os.path.join(HERE, "..", "corpus.json"), encoding="utf-8"))
ALL = list(dict.fromkeys(r for c in C for r in c["refs"]))


def clean(r):
    r = r.replace("　", " ").strip()
    r = re.sub(r"\s+PMID[:：]?\s*(\d+)\s*", r" PMID: \1. ", r)
    r = re.sub(r"\s+doi[:：]?\s*", " doi:", r)
    r = re.sub(r"\s{2,}", " ", r).strip()
    r = r.replace(". .", ".")
    return r


res = {}
for k, v in REFS.items():
    if v.startswith("cs:"):
        rx = re.compile(v[3:])
        hit = [r for r in ALL if rx.search(r)]
        if not hit:
            raise SystemExit("REF NOT FOUND: %s" % k)
        res[k] = clean(max(hit, key=len))          # 巻号・頁まで入った長い方を採る
    else:
        res[k] = v

ORDER = ["ch1.py", "ch2.py", "ch3.py", "ch4.py", "ch5.py", "ch6.py", "ch7.py", "ch8.py"]
src = {f: io.open(os.path.join(HERE, f), encoding="utf-8").read() for f in ORDER}
items = []
for f, a, keys in PLAN:
    s = src[f]
    n = s.count(a)
    if n == 0:
        raise SystemExit("ANCHOR NOT FOUND %s: %s" % (f, a))
    if n > 1:
        print("warn: %d hits in %s: %s (先頭を使う)" % (n, f, a))
    pos = s.index(a)
    items.append((ORDER.index(f), pos, f, a, keys))
items.sort()
num = {}
for _, _, f, a, keys in items:
    for k in keys:
        if k not in num:
            num[k] = len(num) + 1


def label(ns):
    ns = sorted(set(ns))
    out, i = [], 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1:
            j += 1
        out.append("%d–%d" % (ns[i], ns[j]) if j - i >= 2 else ",".join(str(x) for x in ns[i:j + 1]))
        i = j + 1
    return ",".join(out)


for f in ORDER:
    s = src[f]
    its = sorted([it for it in items if it[2] == f], key=lambda x: -x[1])
    for _, pos, _, a, keys in its:
        sup = "^%s^" % label(num[k] for k in keys)
        end = pos + len(a)
        if a.endswith("。"):
            s = s[:end - 1] + sup + s[end - 1:]
        else:
            s = s[:end] + sup + s[end:]
    io.open(os.path.join(HERE, f), "w", encoding="utf-8").write(s)

refs = sorted(num.items(), key=lambda x: x[1])
html_items = "".join("<li>%s</li>" % __import__("html").escape(res[k]) for k, _ in refs)
io.open(os.path.join(HERE, "_refs_html.py"), "w", encoding="utf-8").write(
    "# -*- coding: utf-8 -*-\n# _cite_apply.py が生成\n"
    "REFS = %r\n\n\ndef refs_html():\n"
    "    return ('<h2><span class=\"en\">REFERENCES</span>参考文献</h2>'\n"
    "            '<ol class=\"refs\">' + %r + '</ol>')\n" % ([res[k] for k, _ in refs], html_items))
print("refs", len(refs), "anchors", len(items))
