# -*- coding: utf-8 -*-
"""麻酔科ミニ教科書シリーズ 用 docx ビルダー

既刊（第11巻）の docx をテンプレートとして開き、本文を差し替える。
スタイル・ページ設定・フォントは既刊と同一になる。
"""
import copy
import os
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image, ImageFont

# 既刊テンプレート（第11巻 docx）は PDF 化後に削除されているため、
# 版面・スタイルをコードで再現する。A4／Meiryo／既刊と同じ余白。
A4_W, A4_H = 21.0, 29.7          # cm
MARGIN = dict(top=2.20, bottom=2.00, left=2.20, right=2.20)

NAVY = RGBColor(0x0A, 0x18, 0x30)
GREY = RGBColor(0x55, 0x60, 0x6E)
TEAL = RGBColor(0x00, 0x7A, 0x8A)
GREEN = RGBColor(0x00, 0x5F, 0x4F)
BLUE = RGBColor(0x17, 0x46, 0x82)
PURPLE = RGBColor(0x4E, 0x38, 0x7A)
RED = RGBColor(0x9C, 0x2B, 0x26)
INK = RGBColor(0x22, 0x30, 0x3F)

BODY_FONT = "Meiryo"

# 行送り。1.0 が「行の高さそのまま」。数字を下げるほど詰まる。
# 既刊は 1.37。㉒からは 1.18（余裕分を約半分に）に詰めた。
LINE = 1.18
LINE_TIGHT = 1.14          # 箇条書き・まとめ・枠の中
SPACE_AFTER = 4            # 段落の後ろの空き(pt)


def _east_asian(style, name=BODY_FONT):
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), name)


def new_document():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(A4_W)
    sec.page_height = Cm(A4_H)
    sec.top_margin = Cm(MARGIN["top"])
    sec.bottom_margin = Cm(MARGIN["bottom"])
    sec.left_margin = Cm(MARGIN["left"])
    sec.right_margin = Cm(MARGIN["right"])
    sec.footer_distance = Cm(1.25)

    st = doc.styles["Normal"]
    st.font.name = BODY_FONT
    st.font.size = Pt(10.5)
    st.font.color.rgb = INK
    _east_asian(st)
    pf = st.paragraph_format
    pf.space_after = Pt(SPACE_AFTER)
    pf.line_spacing = LINE

    for lv, size in ((1, 17), (2, 14), (3, 12)):
        hs = doc.styles["Heading %d" % lv]
        hs.font.name = BODY_FONT
        hs.font.size = Pt(size)
        hs.font.bold = True
        hs.font.color.rgb = NAVY
        _east_asian(hs)
        hpf = hs.paragraph_format
        hpf.space_before = Pt(16 if lv == 1 else (12 if lv == 2 else 9))
        hpf.space_after = Pt(6 if lv == 1 else 4)
        hpf.line_spacing = 1.25
        hpf.keep_with_next = True

    # 章見出しの下線（第1〜2水準）
    for lv, col in ((1, "0A1830"), (2, "9AA6B4")):
        hs = doc.styles["Heading %d" % lv]
        pbdr = OxmlElement("w:pBdr")
        bot = OxmlElement("w:bottom")
        bot.set(qn("w:val"), "single")
        bot.set(qn("w:sz"), "12" if lv == 1 else "6")
        bot.set(qn("w:space"), "4")
        bot.set(qn("w:color"), col)
        pbdr.append(bot)
        hs.element.get_or_add_pPr().append(pbdr)

    _footer_field(doc)
    return doc


def _footer_field(doc):
    """フッターに『テーマ名　　- n -』の PAGE フィールドを置く。"""
    f = doc.sections[0].footer
    p = f.paragraphs[0] if f.paragraphs else f.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = p.add_run("")
    r0.font.size = Pt(8.5)
    r0.font.color.rgb = GREY
    r0.font.name = BODY_FONT
    r1 = p.add_run()
    b = OxmlElement("w:fldChar")
    b.set(qn("w:fldCharType"), "begin")
    r1._r.append(b)
    r2 = p.add_run()
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = " PAGE "
    r2._r.append(it)
    r3 = p.add_run()
    e = OxmlElement("w:fldChar")
    e.set(qn("w:fldCharType"), "end")
    r3._r.append(e)
    for r in (r1, r2, r3):
        r.font.size = Pt(8.5)
        r.font.color.rgb = GREY
        r.font.name = BODY_FONT


def set_footer(doc, text):
    """フッター先頭のテーマ名ランを差し替える（PAGE フィールドは保持）。"""
    for sec in doc.sections:
        f = sec.footer
        if f is None or not f.paragraphs:
            continue
        runs = f.paragraphs[0].runs
        if runs:
            runs[0].text = text


# ---------------- 低レベル ----------------
# ---------------- 引用（肩付き番号） ----------------
# 本文中に {{30721296}} や {{30721296,38857019}} と PMID を書いておくと、
# 出現順に番号を振って肩付きで表示し、章末に番号順の参考文献一覧を出す。
CITE_RE = re.compile(r"\{\{([0-9,\s]+)\}\}")
_CITE_RESOLVER = None


def set_cite_resolver(fn):
    """fn(pmid のリスト) -> 肩付きに出す文字列（例 "1,3-5"）"""
    global _CITE_RESOLVER
    _CITE_RESOLVER = fn


# ---------------- 低レベル ----------------
def _run(p, text, size=None, bold=False, color=None, italic=False):
    if _CITE_RESOLVER is not None and text and "{{" in text:
        return _run_with_cites(p, text, size, bold, color, italic)
    r = p.add_run(text)
    if size:
        r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    if color is not None:
        r.font.color.rgb = color
    return r


def _run_with_cites(p, text, size, bold, color, italic):
    last = None
    pos = 0
    for m in CITE_RE.finditer(text):
        if m.start() > pos:
            last = _plain(p, text[pos:m.start()], size, bold, color, italic)
        ids = [x.strip() for x in m.group(1).split(",") if x.strip()]
        mark = _CITE_RESOLVER(ids)
        if mark:
            r = p.add_run(mark)
            r.font.size = Pt((size or 10.5) * 0.92)
            r.font.superscript = True
            r.bold = bold
            if color is not None:
                r.font.color.rgb = color
            last = r
        pos = m.end()
    if pos < len(text):
        last = _plain(p, text[pos:], size, bold, color, italic)
    return last


def _plain(p, text, size, bold, color, italic):
    r = p.add_run(text)
    if size:
        r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    if color is not None:
        r.font.color.rgb = color
    return r



def drop_orphan_blanks(doc):
    """改頁直前の空段落を取り除く。

    boxed() は枠の後ろに余白用の空段落を置く。これが版面の切れ目に来ると、
    次の見出しの pageBreakBefore と重なって白紙ページが1枚生まれる。
    中身のない段落が「改頁付きの段落」の直前にあるときだけ削除する。
    """
    body = doc.element.body
    ps = body.findall(qn("w:p"))
    removed = 0
    for i, p in enumerate(ps[:-1]):
        if "".join(t.text or "" for t in p.iter(qn("w:t"))).strip():
            continue
        if p.find(qn("w:pPr")) is not None:
            nxt = ps[i + 1].find(qn("w:pPr"))
            if nxt is not None and nxt.find(qn("w:pageBreakBefore")) is not None:
                p.getparent().remove(p)
                removed += 1
    return removed


def para(doc, text="", size=None, bold=False, color=None, align=None,
         space_before=None, space_after=None, line=LINE, indent=None,
         keep_with_next=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    if align is not None:
        p.alignment = align
    if space_before is not None:
        pf.space_before = Pt(space_before)
    if space_after is not None:
        pf.space_after = Pt(space_after)
    if line:
        pf.line_spacing = line
    if indent is not None:
        pf.left_indent = Cm(indent)
    pf.keep_with_next = keep_with_next
    if text:
        _run(p, text, size=size, bold=bold, color=color)
    return p


def page_break(doc):
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)


def heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    for r in h.runs:
        r.font.color.rgb = NAVY
        if level == 1:
            r.font.size = Pt(17)
        elif level == 2:
            r.font.size = Pt(14)
        else:
            r.font.size = Pt(12)
    h.paragraph_format.keep_with_next = True
    return h


def toc_field(doc):
    p = doc.add_paragraph()
    r = p.add_run()
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "begin")
    r._r.append(fld)
    r2 = p.add_run()
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = r' TOC \o "1-2" \h \z \u '
    r2._r.append(instr)
    r3 = p.add_run()
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    r3._r.append(sep)
    r4 = p.add_run("（Word で開き Ctrl+A → F9 でページ番号が入ります）")
    r4.font.size = Pt(9)
    r4.font.color.rgb = GREY
    r5 = p.add_run()
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    r5._r.append(end)


def shaded(p, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    p._p.get_or_add_pPr().append(shd)


def left_bar(p, color, size=18):
    pbdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), str(size))
    left.set(qn("w:space"), "8")
    left.set(qn("w:color"), color)
    pbdr.append(left)
    p._p.get_or_add_pPr().append(pbdr)


# ---------------- ブロック ----------------
def figure(doc, path, caption, width_cm=16.0):
    w, h = Image.open(path).size
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(path, width=Cm(width_cm))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_after = Pt(10)
    _run(c, caption, size=9.5, bold=True, color=NAVY)


def boxed(doc, tag, title, lines, color, fill, bar):
    """【Take Home】【Pitfall】【Evidence】など"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = LINE_TIGHT
    p.paragraph_format.keep_with_next = True
    shaded(p, fill)
    left_bar(p, bar)
    _run(p, "【%s】" % tag, size=9.5, bold=True, color=color)
    _run(p, title, bold=True, color=color)
    for i, ln in enumerate(lines):
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(2)
        q.paragraph_format.line_spacing = LINE_TIGHT
        q.paragraph_format.left_indent = Cm(0.4)
        q.paragraph_format.keep_with_next = (i < len(lines) - 1)
        shaded(q, fill)
        left_bar(q, bar)
        _run(q, ln, size=10.5, color=INK)
    tail = doc.add_paragraph()
    tail.paragraph_format.space_after = Pt(10)


def outline(p, level):
    """段落にアウトラインレベルを与える。
    見出しスタイルを使わずに目次へ載せたいとき（コラム）に使う。"""
    ol = OxmlElement("w:outlineLvl")
    ol.set(qn("w:val"), str(level))
    p._p.get_or_add_pPr().append(ol)


def summary(doc, title, lines):
    """章や部の最後に置くまとめ。左に縦線を引くだけで、枠では囲まない。
    目次には載せない。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(13)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    left_bar(p, "0A1830", size=20)
    _run(p, title, size=10.5, bold=True, color=NAVY)
    for i, ln in enumerate(lines):
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(2)
        q.paragraph_format.line_spacing = LINE_TIGHT
        q.paragraph_format.left_indent = Cm(0.55)
        q.paragraph_format.first_line_indent = Cm(-0.45)
        q.paragraph_format.keep_with_next = (i < len(lines) - 1)
        left_bar(q, "0A1830", size=20)
        _run(q, "・" + ln, size=9.5, color=INK)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)


def note(doc, title, lines):
    """本文中の注意書き。枠で囲まず、太字の導入＋箇条書きにする。"""
    if title:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        _run(p, "◆　" + title, size=11, bold=True, color=RED)
    for i, ln in enumerate(lines):
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(2)
        q.paragraph_format.line_spacing = LINE_TIGHT
        q.paragraph_format.left_indent = Cm(0.55)
        q.paragraph_format.first_line_indent = Cm(-0.45)
        q.paragraph_format.keep_with_next = (i < len(lines) - 1)
        _run(q, "・" + ln, size=10.5, color=INK)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def column(doc, no, title, paras):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    shaded(p, "F3F0F8")
    left_bar(p, "4E387A")
    _run(p, "コラム%d　%s" % (no, title), bold=True, color=PURPLE)
    outline(p, 1)
    for i, t in enumerate(paras):
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(3)
        q.paragraph_format.line_spacing = LINE_TIGHT
        q.paragraph_format.left_indent = Cm(0.4)
        q.paragraph_format.keep_with_next = (i < len(paras) - 1)
        shaded(q, "F3F0F8")
        left_bar(q, "4E387A")
        _run(q, t, size=10.5, color=INK)
    doc.add_paragraph().paragraph_format.space_after = Pt(10)


# 本文の版面幅（cm）。A4 21.0 − 左右余白 2.2×2。
TEXT_W = A4_W - MARGIN["left"] - MARGIN["right"]


def _em(ch):
    """1文字の幅（全角を 1.0 とした比）。

    Meiryo の欧文は半角ぴったりではなく、やや広い。0.5 で数えると
    ラベルが1文字ぶん溢れるので 0.56 を使う。"""
    o = ord(ch)
    if o < 0x2000:
        return 0.62 if "A" <= ch <= "Z" else 0.56
    if 0x2000 <= o < 0x2100:
        return 0.55
    return 1.0


_FONT = {}
_UNIT = 256


def _font(bold):
    """Meiryo の実物。字送りを測るためだけに使う。"""
    k = bool(bold)
    if k not in _FONT:
        d = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
        _FONT[k] = ImageFont.truetype(
            os.path.join(d, "meiryob.ttc" if k else "meiryo.ttc"), _UNIT)
    return _FONT[k]


def _emw(s, bold=False):
    """全角1文字を 1.0 とした文字列の幅。

    以前は1文字ずつの推定値を足していたが、「Ca/Mg」で 11% 低く出て
    見出しが2段になった。Meiryo を実際に読んで測る。
    フォントが読めない環境では従来の推定に戻す。
    """
    try:
        return _font(bold).getlength(str(s)) / float(_UNIT)
    except Exception:
        w = sum(_em(c) for c in str(s))
        return w * 1.08 if bold else w


def _longest_token(s, bold=False):
    """途中で折り返せない最長の語（英数字・記号のかたまり）の幅。"""
    best, cur = 0.0, ""
    for ch in str(s):
        if ord(ch) < 0x2000 and ch not in " 　":
            cur += ch
            best = max(best, _emw(cur, bold))
        else:
            cur = ""
    return best


def auto_widths(header, rows, total=None, size=9.0,
                min_cm=1.0, narrow_cm=4.8, cap_em=26.0):
    """列ごとの必要量から幅（cm）を決める。

    考え方：折り返さなくても収まる「短い列」には必要な幅だけを与え、
    残りの幅を、長文が入る列どうしで分け合う。
    均等割りだと「段」のような数字だけの列と長文の列が同じ幅になってしまう。
    """
    total = total if total is not None else TEXT_W
    em = size / 72.0 * 2.54          # 1文字（全角）の幅(cm)
    pad = 0.30                       # セルの左右余白 0.10cm×2 ＋ 余裕
    n = len(header)

    nat = []
    for i in range(n):
        # 見出しは太字。太字は同じ文字でも広いので、太字の字送りで測る。
        head = _emw(header[i], True) if header else 0.0
        body = max([_emw(r[i]) for r in rows], default=0.0)
        tok = max([_longest_token(r[i]) for r in rows] + [0.0])
        tok = max(tok, _longest_token(header[i], True) if header else 0.0)
        nat.append(max(head, min(body, cap_em), tok) * em + pad)

    w = [0.0] * n
    if sum(nat) <= total:
        # 全部の列が自然な幅で収まる。余りは全列で分け合う。
        # 長文列だけに余りを寄せると、短い列が不必要に痩せて折り返す。
        extra = total - sum(nat)
        ssum = sum(nat) or 1.0
        for i in range(n):
            w[i] = nat[i] + extra * nat[i] / ssum
    else:
        # 収まらない。折り返さずに済む短い列は確保し、長文列だけを詰める。
        narrow = [i for i, x in enumerate(nat) if x <= narrow_cm]
        wide = [i for i in range(n) if i not in narrow]
        if wide:
            for i in narrow:
                w[i] = max(min_cm, nat[i])
            rest = total - sum(w[i] for i in narrow)
            if rest < len(wide) * min_cm:
                ssum = sum(nat) or 1.0
                w = [total * x / ssum for x in nat]
            else:
                wsum = sum(nat[i] for i in wide) or 1.0
                for i in wide:
                    w[i] = rest * nat[i] / wsum
        else:
            ssum = sum(nat) or 1.0
            w = [total * x / ssum for x in nat]

    # 見出しは必ず1行に収める。折り返した見出しは表全体が読みにくくなる。
    # ぴったり必要量だけ与えると、字送りの丸めで1文字はみ出すことがある。
    # わずかに余裕（0.06cm）を足す。全部には足せないときは余裕なしで試す。
    def _need(slack):
        return [(_emw(header[i], True) * em + pad + slack) if header else 0.0
                for i in range(n)]
    need = _need(0.06)
    if sum(need) > total:
        need = _need(0.0)
    if sum(need) <= total:
        for _ in range(6):
            short = [i for i in range(n) if w[i] < need[i] - 0.01]
            if not short:
                break
            lack = sum(need[i] - w[i] for i in short)
            donors = [i for i in range(n) if w[i] > need[i] + 0.01]
            slack = sum(w[i] - need[i] for i in donors) or 1.0
            for i in short:
                w[i] = need[i]
            for i in donors:
                w[i] -= lack * (w[i] - need[i]) / slack

    w[-1] += total - sum(w)                   # 丸め誤差は最後の列で吸収
    return w


def _fixed_layout(t, widths):
    """列幅を固定する。

    固定レイアウトのとき Word が実際に見るのは w:tblGrid の値である。
    セル側の幅だけ設定してもグリッドが等分のままだと、そちらが優先されて
    指定が効かない。グリッドと表全体の幅も合わせて書き換える。
    """
    tbl = t._tbl
    tblPr = tbl.tblPr
    for tag in ("w:tblLayout", "w:tblW"):
        el = tblPr.find(qn(tag))
        if el is not None:
            tblPr.remove(el)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)
    total = OxmlElement("w:tblW")
    total.set(qn("w:w"), str(int(sum(widths) * 567)))    # 1cm = 567 twip
    total.set(qn("w:type"), "dxa")
    tblPr.append(total)

    # セルの左右余白を詰める（既定 0.19cm×2 は表では広すぎる）
    old = tblPr.find(qn("w:tblCellMar"))
    if old is not None:
        tblPr.remove(old)
    mar = OxmlElement("w:tblCellMar")
    for side, cm in (("left", 0.10), ("right", 0.10),
                     ("top", 0.04), ("bottom", 0.04)):
        e = OxmlElement("w:" + side)
        e.set(qn("w:w"), str(int(cm * 567)))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tblPr.append(mar)

    grid = tbl.find(qn("w:tblGrid"))
    if grid is None:
        grid = OxmlElement("w:tblGrid")
        tbl.insert(1, grid)
    for c in list(grid.findall(qn("w:gridCol"))):
        grid.remove(c)
    for wcm in widths:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(int(wcm * 567)))
        grid.append(gc)


def table(doc, caption, header, rows, widths=None, size=9.0):
    if caption:
        c = doc.add_paragraph()
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraph_format.space_before = Pt(10)
        c.paragraph_format.space_after = Pt(3)
        c.paragraph_format.keep_with_next = True
        _run(c, caption, size=9.5, bold=True, color=NAVY)
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    for i, htxt in enumerate(header):
        cell = t.rows[0].cells[i]
        cell.text = ""
        pp = cell.paragraphs[0]
        pp.paragraph_format.space_after = Pt(1)
        pp.paragraph_format.line_spacing = 1.15
        _run(pp, htxt, size=size, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        shaded(pp, "2F4A6B")
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:fill"), "2F4A6B")
        tcPr.append(shd)
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            cells[i].text = ""
            pp = cells[i].paragraphs[0]
            pp.paragraph_format.space_after = Pt(1)
            pp.paragraph_format.line_spacing = 1.15
            _run(pp, str(v), size=size, color=INK)
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn("w:cantSplit")) is None:
            cs = OxmlElement("w:cantSplit")
            trPr.insert(0, cs)
    # 見出し行だけがページ末に取り残されないよう、
    # 1行目に「次の行と離さない」を付ける。
    for p0 in t.rows[0].cells[0].paragraphs:
        p0.paragraph_format.keep_with_next = True
    # 見出し行は、ページをまたいだときに次ページの先頭で繰り返す
    trPr = t.rows[0]._tr.get_or_add_trPr()
    if trPr.find(qn("w:tblHeader")) is None:
        th = OxmlElement("w:tblHeader")
        trPr.append(th)
    if widths is None:
        widths = auto_widths(header, rows)
    t.autofit = False
    _fixed_layout(t, widths)
    for row in t.rows:
        for i, wcm in enumerate(widths):
            row.cells[i].width = Cm(wcm)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    return t


def bullets(doc, items, size=10.5, indent=0.5):
    for it in items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = LINE_TIGHT
        p.paragraph_format.left_indent = Cm(indent)
        p.paragraph_format.first_line_indent = Cm(-0.45)
        _run(p, "・" + it, size=size, color=INK)


def lead(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = LINE_TIGHT
    shaded(p, "F2F4F6")
    left_bar(p, "8D97A3", size=12)
    _run(p, text, size=10.5, color=RGBColor(0x3D, 0x4A, 0x5A))


def reflist(doc, rows, size=8.8):
    """番号つき参考文献一覧。rows は [番号, 記述, PMID, DOI]。

    ぶら下げインデントにして、折り返しても番号が飛び出して見えるようにする。
    """
    for no, desc, pmid, doi in rows:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(3)
        pf.line_spacing = LINE_TIGHT
        pf.left_indent = Cm(0.95)
        pf.first_line_indent = Cm(-0.95)
        _run(p, "%s) " % no, size=size, bold=True, color=NAVY)
        _run(p, desc, size=size)
        tail = []
        if pmid:
            tail.append("PMID %s" % pmid)
        if doi:
            tail.append("doi:%s" % doi)
        if tail:
            _run(p, "　" + "　".join(tail), size=size - 0.6, color=GREY)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
