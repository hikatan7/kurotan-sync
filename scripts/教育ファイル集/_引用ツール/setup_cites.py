# -*- coding: utf-8 -*-
"""本の _生成スクリプト に引用機構を仕込む（一冊ぶんの下ごしらえ）。

使い方:
    python setup_cites.py <本の _生成スクリプト のパス> <台帳 xlsx のパス> <シート名>

やること:
  1. citekit.py / citeapply.py / citematch.py をコピー
  2. citeconf.py（台帳の場所とシート名）を書く
  3. その本の bookkit.py に、肩付き番号の描画と reflist を足す
"""
import io
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF_BOOKKIT = os.path.join(
    HERE, "..", "高度心臓血管麻酔", "_生成スクリプト", "bookkit.py")


def patch_bookkit(path):
    ref = io.open(REF_BOOKKIT, encoding="utf-8").read()
    cite_block = ref[ref.index("# ---------------- 引用（肩付き番号） ----------------"):
                     ref.index("def drop_orphan_blanks(doc):")]
    reflist = ref[ref.index("def reflist(doc, rows, size=8.8):"):]

    s = io.open(path, encoding="utf-8").read()
    if "set_cite_resolver" in s:
        print("  bookkit: 既に対応済み")
        return
    i = s.index("def _run(p, text")
    j = s.index("\n\n", s.index("return r", i))
    s = s[:i] + cite_block + s[j + 2:]
    if "\nimport re\n" not in s:
        s = s.replace("import os\n", "import os\nimport re\n", 1)
    s += "\n\n" + reflist
    io.open(path, "w", encoding="utf-8").write(s)
    print("  bookkit: 引用機構と reflist を追加")


def main(dst, ledger, sheet):
    for f in ("citekit.py", "citeapply.py", "citematch.py"):
        shutil.copy(os.path.join(HERE, f), os.path.join(dst, f))
    io.open(os.path.join(dst, "citeconf.py"), "w", encoding="utf-8").write(
        '# -*- coding: utf-8 -*-\n'
        '"""この本の文献台帳の場所とシート名。"""\n'
        'LEDGER = r"%s"\n'
        'SHEETS = {None: "%s"}\n' % (ledger, sheet))
    print("  ツールと citeconf.py を配置")
    bk = os.path.join(dst, "bookkit.py")
    if os.path.exists(bk):
        patch_bookkit(bk)
    else:
        print("  !! bookkit.py が見つからない:", bk)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1], sys.argv[2], sys.argv[3])
