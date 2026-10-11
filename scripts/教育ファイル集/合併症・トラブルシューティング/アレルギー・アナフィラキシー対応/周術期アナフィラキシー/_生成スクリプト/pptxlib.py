# -*- coding: utf-8 -*-
"""教育ファイル集「①専門医版20枚」と同じ体裁でスライドを組む自作ビルダー。

既刊（09_術中の自己血輸血_①専門医版20枚.pptx）から抽出した
配色・寸法・フォントに合わせてある。16:9（13.333×7.5 inch）・Meiryo。

設計上の約束（過去に踏んだ落とし穴の対策）
1. 積み上げカーソル … Slide が _cur を持ち、ブロックを置くたび下へ進める。
   body_rect() が毎回先頭を返す実装だと2つ目が1つ目を塗り潰す。
2. 行高の見積り … PowerPoint の％行間はフォント固有の行高に掛かる。
   Meiryo は約1.30em なので LH = size * 1.30 * spacing で計算する。
   太字は字幅が約1.06倍になるので幅計算にも係数を入れる。
3. 枠は中身に合わせて詰める … 各ブロックが必要高を返し、呼び出し側が
   余白を最下部の一箇所に集める。
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

FONT = "Meiryo"

# ---- 配色（既刊から抽出） ----
TEAL = RGBColor(0x00, 0xA3, 0xB8)
NAVY = RGBColor(0x0A, 0x18, 0x30)
INK = RGBColor(0x1B, 0x25, 0x30)
GREY = RGBColor(0x5A, 0x66, 0x75)
MUTE = RGBColor(0x92, 0x9C, 0xAA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLUE = RGBColor(0x1B, 0x55, 0x9C)
BLUE_L = RGBColor(0xE8, 0xF1, 0xFF)
GREEN = RGBColor(0x00, 0x79, 0x64)
GREEN_L = RGBColor(0xE2, 0xF2, 0xEB)
RED = RGBColor(0xB5, 0x32, 0x38)
RED_L = RGBColor(0xFB, 0xE8, 0xE8)
ORANGE = RGBColor(0xC3, 0x6C, 0x12)
ORANGE_L = RGBColor(0xFF, 0xF3, 0xE4)
PURPLE = RGBColor(0x5B, 0x3F, 0x8F)
PURPLE_L = RGBColor(0xF0, 0xEB, 0xF9)
PANEL = RGBColor(0xF7, 0xFA, 0xFC)
NEUT = RGBColor(0xEE, 0xF2, 0xF7)

PAIRS = {
    "blue": (BLUE, BLUE_L), "green": (GREEN, GREEN_L),
    "red": (RED, RED_L), "orange": (ORANGE, ORANGE_L),
    "purple": (PURPLE, PURPLE_L), "navy": (NAVY, NEUT),
    "teal": (TEAL, RGBColor(0xE3, 0xF5, 0xF8)),
}

# ---- 版面（inch） ----
L = 0.58            # 左マージン
CW = 12.17          # 本文幅
BODY_TOP = 1.32     # 本文開始
BODY_BOT = 6.36     # 本文下端（出典行の上）
SRC_TOP = 6.44
KEY_TOP = 6.72
KEY_H = 0.56
FOOT_TOP = 7.30


# ================================================================ 計測
def _em(ch):
    """1文字の幅（em）。CJK・全角記号は1.0、半角は0.5。"""
    o = ord(ch)
    if o < 0x2000:
        return 0.5
    if 0x2000 <= o < 0x2E80:      # 一般句読点・記号（─ ※ ± など）
        return 1.0 if o > 0x2100 else 0.55
    return 1.0


def text_w(s, size, bold=False):
    """文字列幅（pt）"""
    w = sum(_em(c) for c in s) * size
    return w * (1.06 if bold else 1.0)


def wrap(s, width_in, size, bold=False):
    """width_in インチに収まるよう折り返した行のリスト。\n は強制改行。"""
    limit = width_in * 72.0
    out = []
    for hard in s.split("\n"):
        cur = ""
        for ch in hard:
            if text_w(cur + ch, size, bold) > limit and cur:
                if ch in "、。）」』】・，．":       # 行頭禁則
                    cur += ch
                    out.append(cur)
                    cur = ""
                    continue
                out.append(cur)
                cur = ch
            else:
                cur += ch
        out.append(cur)
    return out or [""]


def lh(size, spacing=1.0):
    """行送り（pt）。Meiryo の固有行高 1.30em を掛ける。"""
    return size * 1.30 * spacing


def text_h(s, width_in, size, bold=False, spacing=1.0):
    """折り返し後の高さ（inch）"""
    return len(wrap(s, width_in, size, bold)) * lh(size, spacing) / 72.0


# ================================================================ 本体
class Slide:
    def __init__(self, deck, s, theme_footer, page):
        self.deck = deck
        self.s = s
        self._cur = BODY_TOP
        self._bfloor = BODY_BOT
        self.page = page
        self.theme_footer = theme_footer

    # ---------- 低レベル ----------
    def box(self, x, y, w, h, fill=None, line=None, rounded=True, adj=0.06):
        shp = self.s.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h))
        if fill is None:
            shp.fill.background()
        else:
            shp.fill.solid()
            shp.fill.fore_color.rgb = fill
        if line is None:
            shp.line.fill.background()
        else:
            shp.line.color.rgb = line
            shp.line.width = Pt(1.0)
        if rounded:
            try:
                shp.adjustments[0] = adj
            except Exception:
                pass
        shp.shadow.inherit = False
        return shp

    def text(self, x, y, w, h, runs, size=9.0, color=INK, bold=False,
             align=PP_ALIGN.LEFT, spacing=1.0, anchor=MSO_ANCHOR.TOP,
             wrap_text=True):
        tb = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = wrap_text
        tf.margin_left = tf.margin_right = 0
        tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = anchor
        if isinstance(runs, str):
            runs = [(runs, {})]
        p = tf.paragraphs[0]
        p.alignment = align
        p.line_spacing = spacing
        for t, opt in runs:
            r = p.add_run()
            r.text = t
            f = r.font
            f.name = FONT
            f.size = Pt(opt.get("size", size))
            f.bold = opt.get("bold", bold)
            f.color.rgb = opt.get("color", color)
        return tb

    # ---------- カーソル ----------
    def gap(self, h=0.14):
        self._cur += h

    def remaining(self, reserved=0.0):
        return BODY_BOT - self._cur - reserved

    # ---------- ブロック ----------
    def panel(self, title, height, width=CW, x=None, y=None, fill=PANEL,
              advance=True):
        """見出しつきの薄い枠。返り値は (内側x, 内側y, 内側w, 内側下端)"""
        x = L if x is None else x
        y = self._cur if y is None else y
        self.box(x, y, width, height, fill=fill)
        if title:
            self.text(x + 0.12, y + 0.06, width - 0.24, 0.24, title,
                      size=10.0, bold=True, color=NAVY)
            inner_y = y + 0.34
        else:
            inner_y = y + 0.10
        if advance:
            self._cur = y + height
        return (x + 0.20, inner_y, width - 0.40, y + height - 0.10)

    def row_heights(self, cols, rows, size=9.0, rowh=0.48):
        hs = []
        for row in rows:
            need = rowh
            for c, cell in enumerate(row):
                sz = size + (2.0 if c == 0 else 0.0)
                need = max(need, text_h(str(cell), cols[c] - 0.28, sz,
                                        bold=(c == 0), spacing=1.0) + 0.16)
            hs.append(need)
        return hs

    def grid(self, cols, rows, x=None, y=None, width=CW, rowh=0.48, gap=0.08,
             colors=None, size=9.0, advance=True, heights=None):
        """左列が色つきラベルの表。cols=[列幅(inch)...]、rows=[[c1,c2,...],...]"""
        x = L + 0.22 if x is None else x
        y = self._cur if y is None else y
        colors = colors or ["blue"] * len(rows)
        heights = heights or self.row_heights(cols, rows, size, rowh)
        cy = y
        for r, row in enumerate(rows):
            strong, light = PAIRS[colors[r % len(colors)]]
            cx = x
            need = heights[r]
            for c, cell in enumerate(row):
                fill = strong if c == 0 else (light if c == 1 else NEUT)
                col = WHITE if c == 0 else INK
                self.box(cx, cy, cols[c], need, fill=fill)
                self.text(cx + 0.14, cy, cols[c] - 0.28, need, str(cell),
                          size=size + (2.0 if c == 0 else 0.0),
                          bold=(c == 0), color=col, anchor=MSO_ANCHOR.MIDDLE)
                cx += cols[c] + gap
            cy += need + gap
        if advance:
            self._cur = cy
        return cy


    # ---------- 計測つきブロック ----------
    def grid_h(self, cols, rows, size=9.0, rowh=0.48, gap=0.08):
        """grid() が必要とする高さ（inch）を先に返す"""
        tot = 0.0
        for row in rows:
            need = rowh
            for c, cell in enumerate(row):
                sz = size + (2.0 if c == 0 else 0.0)
                need = max(need, text_h(str(cell), cols[c] - 0.28, sz,
                                        bold=(c == 0), spacing=1.0) + 0.16)
            tot += need + gap
        return tot

    def panel_grid(self, title, cols, rows, colors=None, size=9.0, rowh=0.40,
                   gap=0.08, width=CW, x=None, y=None, extra=0.0, fill=False):
        """枠を中身の高さに合わせて描き、その中に grid を置く。返り値は下端。"""
        x = L if x is None else x
        y = self._cur if y is None else y
        inner_w = width - 0.40
        span = sum(cols) + gap * (len(cols) - 1)
        cols = [c * inner_w / span for c in cols]      # 内側幅にそろえる
        hs = self.row_heights(cols, rows, size, rowh)
        head = 0.34 if title else 0.10
        ph = head + sum(hs) + gap * (len(hs) - 1) + 0.12 + extra
        if fill:
            room = (self._bfloor - y) - ph
            if room > 0:
                hs = [h + room / len(hs) for h in hs]
                ph = head + sum(hs) + gap * (len(hs) - 1) + 0.12 + extra
        self.box(x, y, width, ph, fill=PANEL)
        if title:
            self.text(x + 0.12, y + 0.06, width - 0.24, 0.24, title,
                      size=10.0, bold=True, color=NAVY)
        self.grid(cols, rows, x=x + 0.20, y=y + head, colors=colors,
                  size=size, rowh=rowh, gap=gap, advance=False, heights=hs)
        self._cur = y + ph
        return y + ph

    def cards_h(self, items, width=CW, gap=0.16, height=1.40):
        n = len(items)
        cw = (width - gap * (n - 1)) / n
        need = 0.0
        for head, body, key in items:
            need = max(need, 0.30 + text_h(body, cw - 0.46, 8.8, spacing=1.05)
                       + 0.26)
        return max(height, need)

    def cards(self, items, x=None, y=None, width=CW, height=1.40, gap=0.16,
              advance=True, bottom=False):
        """左に色帯の付いたカードを横並び。items=[(見出し,本文,色key),...]"""
        x = L if x is None else x
        y = self._cur if y is None else y
        n = len(items)
        cw = (width - gap * (n - 1)) / n
        need = 0.0
        for head, body, key in items:
            need = max(need, 0.30 + text_h(body, cw - 0.46, 8.8, spacing=1.05)
                       + 0.26)
        h = max(height, need)
        if bottom:
            h = need
            y = self._bfloor - h
            self._bfloor = y - 0.16
        for i, (head, body, key) in enumerate(items):
            strong, light = PAIRS[key]
            cx = x + i * (cw + gap)
            self.box(cx, y, cw, h, fill=light)
            self.box(cx, y, 0.06, h, fill=strong, rounded=False)
            self.text(cx + 0.16, y + 0.11, cw - 0.32, 0.28, head,
                      size=11.5, bold=True, color=strong)
            self.text(cx + 0.16, y + 0.43, cw - 0.32, h - 0.55, body,
                      size=8.8, color=INK, spacing=1.05)
        if advance and not bottom:
            self._cur = y + h
        return y + h

    def bullets(self, items, x, y, w, size=9.0, spacing=1.12, color=INK,
                marker="・"):
        """箇条書き。返り値は消費した高さ（inch）"""
        cy = y
        for it in items:
            body = marker + it if marker else it
            hh = text_h(body, w, size, spacing=spacing)
            self.text(x, cy, w, hh + 0.04, body, size=size, color=color,
                      spacing=spacing)
            cy += hh + 0.05
        return cy - y

    def para(self, s, x, y, w, size=9.0, spacing=1.12, color=INK, bold=False):
        hh = text_h(s, w, size, bold, spacing)
        self.text(x, y, w, hh + 0.04, s, size=size, color=color,
                  bold=bold, spacing=spacing)
        return hh + 0.05

    def strip(self, text, key="navy", x=None, y=None, width=CW, h=0.44,
              bottom=False):
        """1行の帯（枠内の強調）"""
        x = L if x is None else x
        if bottom:
            y = self._bfloor - h
            self._bfloor = y - 0.12
        elif y is None:
            y = self._cur
        strong, light = PAIRS[key]
        self.box(x, y, width, h, fill=light)
        self.box(x, y, 0.05, h, fill=strong, rounded=False)
        self.text(x + 0.16, y, width - 0.32, h, text, size=10.0, bold=True,
                  color=strong, anchor=MSO_ANCHOR.MIDDLE)
        if not bottom:
            self._cur = y + h
        return y + h

    # ---------- 固定位置 ----------
    def source(self, text):
        self.text(L, SRC_TOP, CW, 0.22, "出典：" + text, size=8.0, color=MUTE)

    def keymsg(self, lead, strong, tail=""):
        self.box(L, KEY_TOP, CW, KEY_H, fill=NAVY)
        runs = [("KEY MESSAGE：　", {"size": 10.0, "bold": True, "color": TEAL}),
                (lead, {"size": 11.0, "bold": False, "color": WHITE}),
                (strong, {"size": 11.0, "bold": True, "color": TEAL})]
        if tail:
            runs.append((tail, {"size": 11.0, "bold": False, "color": WHITE}))
        self.text(L + 0.25, KEY_TOP, CW - 0.50, KEY_H, runs,
                  anchor=MSO_ANCHOR.MIDDLE)

    def footer(self):
        self.text(L, FOOT_TOP, CW, 0.18,
                  "静岡市立静岡病院 麻酔科｜%s｜%d" % (self.theme_footer, self.page),
                  size=7.0, color=MUTE)


class Deck:
    def __init__(self, theme_footer, header):
        self.p = Presentation()
        self.p.slide_width = Inches(13.3333)
        self.p.slide_height = Inches(7.5)
        self.blank = self.p.slide_layouts[6]
        self.theme_footer = theme_footer
        self.header = header
        self.n = 0

    def _new(self):
        return self.p.slides.add_slide(self.blank)

    def title_slide(self, series, no, title, sub, lead, cards, toc, note,
                    badge):
        s = Slide(self, self._new(), self.theme_footer, 1)
        s.box(0, 0, 13.3333, 0.06, fill=TEAL, rounded=False)
        s.text(L, 0.24, 9.60, 0.42,
               [(self.header, {"size": 9.0, "color": GREY})], size=9.0)
        s.text(L, 1.15, 6.60, 0.30, "%s ｜ %s" % (series, no),
               size=12.0, bold=True, color=TEAL)
        s.text(L, 1.62, 6.90, 1.05, title, size=32.0, bold=True, color=NAVY)
        ln = s.s.shapes.add_connector(1, Inches(L), Inches(2.86),
                                      Inches(L + 1.6), Inches(2.86))
        ln.line.color.rgb = TEAL
        ln.line.width = Pt(2.5)
        s.text(L, 3.02, 6.30, 0.40, sub, size=15.0, bold=True, color=INK,
               spacing=1.15)
        s.text(L, 3.52, 6.30, 0.90, lead, size=11.0, color=GREY, spacing=1.25)
        cy = 4.55
        cwid = (6.30 - 0.16 * (len(cards) - 1)) / len(cards)
        for i, (h, b, k) in enumerate(cards):
            strong, light = PAIRS[k]
            cx = L + i * (cwid + 0.16)
            s.box(cx, cy, cwid, 1.30, fill=light)
            s.box(cx, cy, 0.06, 1.30, fill=strong, rounded=False)
            s.text(cx + 0.16, cy + 0.11, cwid - 0.32, 0.29, h,
                   size=11.5, bold=True, color=strong)
            s.text(cx + 0.16, cy + 0.44, cwid - 0.32, 0.76, b,
                   size=8.8, color=INK, spacing=1.10)
        s.box(L, 6.10, 4.90, 0.52, fill=NAVY)
        s.text(L, 6.10, 4.90, 0.52, badge, size=12.0, bold=True, color=WHITE,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 右カラム：構成
        s.box(7.30, 1.15, 5.45, 5.45, fill=PANEL)
        s.text(7.30, 1.27, 5.45, 0.26, "20枚の構成", size=11.5, bold=True,
               color=NAVY, align=PP_ALIGN.CENTER)
        ty = 1.69
        for rng, txt in toc:
            s.box(7.60, ty, 4.85, 0.81, fill=NEUT)
            s.box(7.60, ty, 0.06, 0.81, fill=TEAL, rounded=False)
            s.text(7.74, ty, 1.15, 0.81, rng, size=11.0, bold=True,
                   color=TEAL, anchor=MSO_ANCHOR.MIDDLE)
            s.text(8.92, ty, 3.45, 0.81, txt, size=9.0, color=INK,
                   spacing=1.10, anchor=MSO_ANCHOR.MIDDLE)
            ty += 0.90
        s.text(7.60, 6.26, 4.85, 0.26, note, size=7.5, color=MUTE)
        self.n = 1
        return s

    def slide(self, eyebrow, title_a, title_b):
        self.n += 1
        s = Slide(self, self._new(), self.theme_footer, self.n)
        s.box(L, 0.30, CW, 0.04, fill=TEAL, rounded=False)
        s.text(L, 0.40, CW, 0.26, eyebrow, size=10.0, bold=True, color=TEAL)
        s.text(L, 0.62, CW, 0.55,
               [(title_a, {"size": 23.5, "bold": True, "color": GREEN}),
                (title_b, {"size": 23.5, "bold": True, "color": NAVY})])
        s.footer()
        return s

    def save(self, path):
        self.p.save(path)
        return path
