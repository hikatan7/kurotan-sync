# -*- coding: utf-8 -*-
"""既刊PDF（①〜⑫）から本文を取り出し、bookkit のブロック列に戻す。

本文は PDF から取り出したものをそのまま使う。書き換えない。
判断するのは「どの行が見出しで、どの行が本文か」という構造の割り当てだけ。

  フォントサイズと字下げで役割を決める
    大きい太字      → 章見出し（第N章）／部見出し（第X部）
    ■ で始まる太字  → 小見出し
    【…】で始まる行 → 枠（Take Home / Pitfall / コラム など）
    本文サイズ      → 段落。行頭が ・ なら箇条書き
    小さいサイズ    → ページ番号・図表キャプション
  表は pdfplumber の罫線検出に任せ、その y 位置に差し込む。
"""
import os
import re
import statistics
import fitz
import pdfplumber

BOX = re.compile(r"^【([^】]+)】\s*(.*)$")
PART = re.compile(r"^第\s*[IVX]+\s*部")
CHAP = re.compile(r"^第\s*\d+\s*章")
APPX = re.compile(r"^付\s*録\s*[A-Z0-9]")
FIGCAP = re.compile(r"^図\s*(\d+)")
TBLCAP = re.compile(r"^表\s*([\d A-Z-]+)")
SUBH = re.compile(r"^[■◆]\s*")


def join_wrapped(lines):
    """PDF で折り返された行を、もとの1項目につなぎ直す。

    ・で始まる行、番号で始まる行は新しい項目。
    それ以外は、前の行が句点で終わっていなければ続きとみなす。
    """
    out = []
    for t in lines:
        t = t.strip()
        if not t:
            continue
        new = bool(re.match(r"^[・‣▸]|^\d+[．.）)]|^[（(]\d+[）)]", t))
        if out and not new and not re.search(r"[。！？）】」]$", out[-1]):
            out[-1] += t
        else:
            out.append(t)
    return out


def _bold(span):
    return "Bold" in span["font"] or "bold" in span["font"]


def profile(doc):
    """本文サイズと見出しサイズを、出現量から推定する。"""
    cnt = {}
    for p in doc:
        for b in p.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    t = s["text"].strip()
                    if not t:
                        continue
                    k = (round(s["size"], 1), _bold(s))
                    cnt[k] = cnt.get(k, 0) + len(t)
    body = max((k for k in cnt if not k[1]), key=lambda k: cnt[k])[0]
    return {"body": body, "counts": cnt}


def page_items(page, plumber_page, prof, margins):
    """1ページぶんの要素を y 順に並べて返す。"""
    body = prof["body"]
    top, bot = margins
    tables = []
    for t in plumber_page.find_tables():
        rows = [[(c or "").strip().replace("\n", "") for c in r]
                for r in t.extract()]
        rows = [[c for c in r if c != ""] for r in rows]
        rows = [r for r in rows if any(r)]
        if len(rows) >= 2 and len(rows[0]) >= 2:
            # 行ごとに列数がぶれることがあるので、最頻の列数にそろえる
            import collections as _c
            ncol = _c.Counter(len(r) for r in rows).most_common(1)[0][0]
            rows = [(r + [""] * ncol)[:ncol] for r in rows]
            tables.append((t.bbox[1], t.bbox[3], rows))

    items = []
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") == 1:
            items.append((b["bbox"][1], "image", None, b["bbox"]))
            continue
        for l in b.get("lines", []):
            txt = "".join(s["text"] for s in l["spans"])
            t = txt.strip()
            if not t:
                continue
            y0, y1 = l["bbox"][1], l["bbox"][3]
            if y1 < top or y0 > bot:
                continue                      # ヘッダ・フッタ
            if re.fullmatch(r"[-—―‐\s]*\d+[-—―‐\s]*", t):
                continue                      # ページ番号だけの行
            if any(a - 2 <= y0 and y1 <= z + 2 for a, z, _ in tables):
                continue                      # 表の中身は別途拾う
            s0 = l["spans"][0]
            items.append((y0, "text", {
                "text": t, "size": round(s0["size"], 1),
                "bold": _bold(s0), "x": round(l["bbox"][0]),
            }, l["bbox"]))
    for a, z, rows in tables:
        items.append((a, "table", rows, None))
    items.sort(key=lambda x: x[0])
    return items


def convert(pdf_path, figdir=None, fig_prefix="f"):
    doc = fitz.open(pdf_path)
    prof = profile(doc)
    body = prof["body"]
    H = doc[0].rect.height
    margins = (H * 0.055, H * 0.945)

    blocks = []
    buf = []          # 連結中の段落行
    buf_kind = None
    box = None        # 枠を組み立て中

    def flush():
        nonlocal buf, buf_kind
        if not buf:
            return
        txt = "".join(buf)
        if buf_kind == "ul":
            blocks.append(("ul", [x.lstrip("・‣▸ ").strip()
                                  for x in join_wrapped(buf)]))
        else:
            blocks.append(("p", txt))
        buf, buf_kind = [], None

    def close_box():
        nonlocal box
        if box:
            tag, title, lines = box
            lines = [x.lstrip("・‣▸ ") for x in join_wrapped(lines)]
            kind = {"Take Home": "th", "Pitfall": "pf", "Evidence": "ev"}.get(tag)
            if kind is None:
                blocks.append(("colx", tag, title, lines))
            else:
                blocks.append((kind, title or tag, lines))
            box = None

    pl = pdfplumber.open(pdf_path)
    for pno in range(doc.page_count):
        for y, kind, data, bbox in page_items(doc[pno], pl.pages[pno],
                                              prof, margins):
            if kind == "table":
                flush(); close_box()
                hdr, rows = data[0], data[1:]
                blocks.append(("tbl", hdr, rows, None))
                continue
            if kind == "image":
                continue
            t, sz, bd, x = data["text"], data["size"], data["bold"], data["x"]

            m = BOX.match(t)
            if m:
                flush(); close_box()
                box = (m.group(1), m.group(2).strip(), [])
                continue
            if box is not None:
                # 枠の中身は本文より小さいサイズで字下げされている
                if sz < body - 0.3 or (sz <= body and x > 60):
                    box[2].append(t)
                    continue
                close_box()

            if PART.match(t) and bd:
                flush(); blocks.append(("h1", t)); continue
            if (CHAP.match(t) or APPX.match(t)) and bd:
                flush(); blocks.append(("h2", t)); continue
            if SUBH.match(t) and bd:
                flush(); blocks.append(("h3", SUBH.sub("", t))); continue
            if bd and sz > body + 0.8:
                flush(); blocks.append(("h3", t)); continue
            if sz < body - 0.8:
                fm = FIGCAP.match(t)
                if fm and figdir:
                    fn = "%s%02d.png" % (fig_prefix, int(fm.group(1)))
                    if os.path.exists(os.path.join(figdir, fn)):
                        flush(); blocks.append(("fig", fn, t)); continue
                if TBLCAP.match(t):
                    continue                  # 表キャプションは表に付ける
                # 図表キャプション以外の小さい文字（表の注記・参考文献など）は
                # 本文の一部なので落とさずに段落として拾う
                if buf_kind == "p" and buf and not re.search(r"[。）\]]$", buf[-1]):
                    buf[-1] = buf[-1] + t
                else:
                    flush(); buf_kind = "p"; buf = [t]
                continue

            k = "ul" if t.startswith("・") else "p"
            # 箇条書きの途中で折り返した行は、前の項目の続きとして足す
            if buf_kind == "ul" and k == "p" and x > 58:
                buf[-1] = buf[-1] + t
                continue
            if buf_kind and buf_kind != k:
                flush()
            buf_kind = k
            if k == "ul":
                buf.append(t)
            else:
                if buf and not re.search(r"[。：:、]$", buf[-1]):
                    buf[-1] = buf[-1] + t
                else:
                    buf.append(t)
    flush(); close_box()
    pl.close()
    return strip_front(blocks), prof


def strip_front(blocks):
    """表紙・略語表・はじめに・目次を落とし、本文の先頭から返す。

    目次の「第1章 …」は短い副題が続くだけだが、本文の「第1章 …」の直後には
    まとまった長さの段落が来る。これで本文の開始位置を見分ける。
    """
    for i, b in enumerate(blocks):
        if b[0] != "h2" or not re.match(r"^第\s*1\s*章", b[1]):
            continue
        nxt = blocks[i + 1:i + 5]
        if any(k == "p" and len(v) > 80 for k, v, *_ in
               [(x[0], x[1]) if len(x) > 1 else (x[0], "") for x in nxt]):
            return blocks[i:]
    return blocks


if __name__ == "__main__":
    import sys, collections
    p = sys.argv[1]
    fd = sys.argv[2] if len(sys.argv) > 2 else None
    bl, pr = convert(p, fd)
    print("本文サイズ %.1fpt" % pr["body"])
    print(collections.Counter(b[0] for b in bl))
    for b in bl[:40]:
        print("  %-5s %s" % (b[0], str(b[1])[:78]))
