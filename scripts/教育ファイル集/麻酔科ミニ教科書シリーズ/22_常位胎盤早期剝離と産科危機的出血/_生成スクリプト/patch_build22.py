# -*- coding: utf-8 -*-
"""build22.py を組み替える。

  ・Take Home / Pitfall の枠を廃止し、章末の「まとめ」に集約する
  ・コラム番号を本文に現れる順で 1 から振り直す
  ・目次は部・章・コラムだけ（小見出しは本文のみ）
"""
import io

p = "build22.py"
s = io.open(p, encoding="utf-8").read()

s = s.replace(
    "from bookkit import (drop_orphan_blanks, new_document,",
    "from bookkit import (drop_orphan_blanks, new_document, summary, note,")
s = s.replace("import c22_p4\n", "import c22_p4\nimport c22_sum\n")

OLD = '''BLOCKS = c22_p1.BLOCKS + c22_p2.BLOCKS + c22_p3.BLOCKS + c22_p4.BLOCKS
'''
NEW = '''BLOCKS = c22_p1.BLOCKS + c22_p2.BLOCKS + c22_p3.BLOCKS + c22_p4.BLOCKS


def _rebuild(blocks):
    """枠の廃止・章末まとめの挿入・コラム番号の振り直しをまとめて行う。"""
    # --- コラムは本文に現れる順に 1 から振り直す
    col_no = 0
    tmp = []
    for b in blocks:
        if b[0] == "col":
            col_no += 1
            tmp.append(("col", col_no, b[2], b[3]))
        else:
            tmp.append(b)
    blocks = tmp

    # --- 章末まとめを差し込む位置を決める
    #     章（h2）の中身が終わる直前＝次の h1／h2／pb の手前。
    out = []
    cur_ch = None          # いま開いている章の見出し
    pending = None         # まだ出していないまとめ

    def flush():
        nonlocal pending
        if pending:
            out.append(("sum", "この章のまとめ", pending))
            pending = None

    for i, b in enumerate(blocks):
        kind = b[0]
        if kind in ("h1", "h2", "pb"):
            flush()
            if kind == "h2":
                cur_ch = b[1]
                pending = c22_sum.SUMMARIES.get(cur_ch)
            out.append(b)
            continue
        # Take Home / Pitfall の枠をやめる
        if kind == "th":
            title = b[1]
            if title.endswith("部の要点"):
                out.append(("sum", title.replace("の要点", "のまとめ"), b[2]))
            elif title.endswith("章の要点"):
                pass                      # 章末まとめに統合済み
            else:
                out.append(("note", title, b[2]))
            continue
        if kind == "pf":
            out.append(("note", b[1], b[2]))
            continue
        out.append(b)
    flush()
    return out


BLOCKS = _rebuild(BLOCKS)
'''
assert OLD in s
s = s.replace(OLD, NEW, 1)

# --- 描画側
s = s.replace('''    elif kind == "th":
        boxed(doc, "Take Home", blk[1], blk[2], GREEN, "EAF3F0", "005F4F")
    elif kind == "pf":
        boxed(doc, "Pitfall", blk[1], blk[2], RED, "FBEEEC", "9C2B26")
    elif kind == "ev":''',
'''    elif kind == "sum":
        summary(doc, blk[1], blk[2])
        SUMCOUNT += 1
    elif kind == "note":
        note(doc, blk[1], blk[2])
    elif kind == "ev":''')
s = s.replace("COLCOUNT = 0", "COLCOUNT = 0\nSUMCOUNT = 0")
s = s.replace('print("saved", OUT, "／図版", FIGCOUNT, "点・表", TBLCOUNT, "点・コラム",\n      COLCOUNT, "本")',
              'print("saved", OUT, "／図版", FIGCOUNT, "点・表", TBLCOUNT,\n'
              '      "点・コラム", COLCOUNT, "本・まとめ", SUMCOUNT, "本")')

io.open(p, "w", encoding="utf-8").write(s)
print("build22 patched")
