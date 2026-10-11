# -*- coding: utf-8 -*-
"""巻番号の丸数字。符号位置を取り違えた事故が過去にあったので、ここに一本化する。

本文には ##18 のように書き、fix() で ⑱ に置き換える。
①=U+2460…⑳=U+2473／㉑=U+3251…㉟=U+325F／㊱=U+32B1…㊿=U+32BF

**丸数字は ㊿（50）で打ち止め。** Unicode に 51 以降の丸数字は無い。
51 巻以降は 〔51〕 のように亀甲括弧で表す（暫定。変えるならここ一箇所）。
"""
import re


def circled(n):
    if 1 <= n <= 20:
        return chr(0x245F + n)
    if 21 <= n <= 35:
        return chr(0x3250 + n - 20)
    if 36 <= n <= 50:
        return chr(0x32B0 + n - 35)
    if n >= 51:
        return u"\u3014%d\u3015" % n          # 〔51〕
    raise ValueError(n)


def _sub(m):
    return circled(int(m.group(1)))


def fix(o):
    """文字列・リスト・タプルの中の ##nn をすべて巻番号の表記にする。"""
    if isinstance(o, str):
        return re.sub(r"##(\d+)", _sub, o)
    if isinstance(o, list):
        return [fix(x) for x in o]
    if isinstance(o, tuple):
        return tuple(fix(x) for x in o)
    return o
