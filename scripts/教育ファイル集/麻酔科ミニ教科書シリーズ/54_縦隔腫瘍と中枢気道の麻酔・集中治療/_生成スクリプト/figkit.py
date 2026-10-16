# -*- coding: utf-8 -*-
"""図版の定型レイアウト。横並び2枠・横並びn枠・縦積みの三つだけ。

textbox の title に改行を入れると高さが見積もれず版面検査に落ちるので、
タイトルは必ず一行にすること。
"""
from figlib import textbox


def two(cv, W, y, t1, s1, l1, t2, s2, l2, size=14, ts=17, mh=320):
    bw = (W - 112 - 40) / 2
    h1 = textbox(cv, 56, y, bw, l1, size, style=s1, title=t1,
                 title_size=ts, min_h=mh)
    h2 = textbox(cv, 56 + bw + 40, y, bw, l2, size, style=s2, title=t2,
                 title_size=ts, min_h=mh)
    return max(h1, h2)


def cols(cv, W, y, items, size=12.5, ts=14.5, mh=270, gap=22):
    bw = (W - 112 - (len(items) - 1) * gap) / len(items)
    hs = []
    for i, (ttl, st, lines) in enumerate(items):
        hs.append(textbox(cv, 56 + i * (bw + gap), y, bw, lines, size,
                          style=st, title=ttl, title_size=ts, min_h=mh))
    return max(hs)


def rows(cv, W, y, items, size=13.5, ts=14.5, gap=14):
    yy = y
    for ttl, st, body in items:
        h = textbox(cv, 56, yy, W - 112, [body], size, style=st,
                    title=ttl, title_size=ts)
        yy += h + gap
    return yy - y


def band(cv, W, y, lines, style="navy", title=None, size=14.5, ts=17, mh=None):
    return textbox(cv, 56, y, W - 112, lines, size, style=style,
                   title=title, title_size=ts, min_h=mh)
