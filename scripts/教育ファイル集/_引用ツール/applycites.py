# -*- coding: utf-8 -*-
"""引用位置の json と台帳から、docx に肩付き番号と参考文献を入れる。

    python applycites.py <docx> <台帳 xlsx> <シート名> <cites json> [追記する注記]
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import citedocx

LEAD = ("本文の肩付き番号は、この一覧の番号に対応する。"
        "学術論文は PubMed 識別子（PMID）と DOI を確認した。"
        "台帳は同じフォルダの『%s』にある。")


def load_meta(ledger, sheet):
    import openpyxl
    wb = openpyxl.load_workbook(ledger, read_only=True, data_only=True)
    ws = wb[sheet]
    head = None
    meta = {}
    for row in ws.iter_rows(values_only=True):
        if head is None:
            head = [str(c or "") for c in row]
            idx = {h: i for i, h in enumerate(head)}
            continue
        if not row or not row[0]:
            continue
        def g(k):
            i = idx.get(k)
            v = row[i] if i is not None and i < len(row) else None
            return "" if v is None else str(v).strip()
        m = re.search(r"(\d{4,9})", g("PMID（リンク）"))
        # PMID のない学会資料・行政文書は S-ID をキーにする
        key = m.group(1) if m else g("S-ID")
        if not key:
            continue
        meta[key] = {"year": g("年"), "first": g("筆頭著者/学会"),
                     "title": g("タイトル"), "journal": g("雑誌"),
                     "doi": g("DOI（リンク）"), "pmid": m.group(1) if m else ""}
    wb.close()
    return meta


def main(docx, ledger, sheet, cites_json, note=None):
    meta = load_meta(ledger, sheet)
    cites = json.load(io.open(cites_json, encoding="utf-8"))
    if "cites" in cites:
        cites = cites["cites"]
    order, unused = citedocx.apply(
        docx, cites, meta, out=docx,
        lead_text=LEAD % os.path.basename(ledger), extra_note=note)
    print("引用文献 %d 件 / 対応が外れたキー %d" % (len(order), len(unused)))
    if unused:
        print("  外れたキー:", sorted(unused)[:10])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(*sys.argv[1:])
