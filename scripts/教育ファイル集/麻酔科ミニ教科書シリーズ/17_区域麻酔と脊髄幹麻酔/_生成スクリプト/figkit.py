# -*- coding: utf-8 -*-
"""教科書図版でくり返し使うレイアウト部品（⑯⑰で共用）"""
from figlib import LH, NAVY, INK


def two_col(cv, W, PTOP, cols, head_sz=12.5, body_sz=10.2, gapx=50, L=64):
    """左右2枚のパネル。cols = [(見出し, 色, 淡色, [行...]), ...]。返り値は下端"""
    PW = (W - L * 2 - gapx) / 2.0
    HH = 54
    BTOP = PTOP + HH + 8
    sz = min(cv.fit_size(["・" + l for c in cols for l in c[3]], PW - 56,
                         body_sz), body_sz)
    nl = max(sum(len(cv.wrap(l, PW - 62, sz)) for l in c[3]) for c in cols)
    BH = 30 + LH(sz, 1.85) * (nl - 1) + LH(sz, 1.0) * 0.5 + 22
    for i, (head, col, fc, lines) in enumerate(cols):
        px = L + i * (PW + gapx)
        cv.box(px, PTOP, PW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(px + PW / 2, PTOP + HH / 2, head, size=head_sz, color="white",
                weight="bold")
        cv.box(px, BTOP, PW, BH, fc=fc, ec=col, lw=1.8, radius=8)
        k = 0
        for ln in lines:
            for j, sub in enumerate(cv.wrap(ln, PW - 62, sz)):
                cv.text(px + 26, BTOP + 30 + LH(sz, 1.85) * k,
                        ("・" if j == 0 else "　") + sub, size=sz, color=INK,
                        ha="left")
                k += 1
    return BTOP + BH


def three_col(cv, W, PTOP, cols, body_sz=10.0, gapx=22, L=48, head_sz=11.4):
    """3枚のパネル。cols = [(見出し, 色, [行...]), ...]。返り値は下端"""
    R = W - L
    CW = (R - L - gapx * 2) / 3
    HH = 52
    BTOP = PTOP + HH + 8
    sz = min(cv.fit_size(["・" + l for c in cols for l in c[2]], CW - 46,
                         body_sz), body_sz)
    nl = max(sum(len(cv.wrap(l, CW - 56, sz)) for l in c[2]) for c in cols)
    BH = 30 + LH(sz, 1.65) * (nl - 1) + LH(sz, 1.0) * 0.5 + 22
    for i, (head, col, lines) in enumerate(cols):
        x = L + i * (CW + gapx)
        cv.box(x, PTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, PTOP + HH / 2, head, size=head_sz, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        k = 0
        for ln in lines:
            for j, sub in enumerate(cv.wrap(ln, CW - 56, sz)):
                cv.text(x + 24, BTOP + 30 + LH(sz, 1.65) * k,
                        ("・" if j == 0 else "　") + sub, size=sz, color=INK,
                        ha="left")
                k += 1
    return BTOP + BH


def rows(cv, W, TOP, data, name_sz=11.0, body_sz=10.0, L=52, gap=14, lh=1.7):
    """左に色つき見出し、右に本文。data=[(見出し,色,[行...]),...]。返り値は下端"""
    R = W - L
    NAMEW = max(cv.measure(d[0], name_sz, weight="bold")[0] for d in data) + 44
    bsz = min(cv.fit_size([l for d in data for l in d[2]],
                          R - L - NAMEW - 80, body_sz), body_sz)
    nl = max(len(d[2]) for d in data)
    RH = 30 + LH(bsz, lh) * (nl - 1) + LH(bsz, 1.0) * 0.5 + 26
    for i, (name, col, lines) in enumerate(data):
        y = TOP + i * (RH + gap)
        cv.box(L, y, R - L, RH, fc="white", ec=col, lw=1.8, radius=8)
        cv.box(L, y, NAMEW, RH, fc=col, ec=col, lw=0, radius=8)
        cv.text(L + NAMEW / 2, y + RH / 2, name, size=name_sz, color="white",
                weight="bold")
        for j, ln in enumerate(lines):
            cv.text(L + NAMEW + 34,
                    y + RH / 2 - LH(bsz, lh) * (len(lines) - 1) / 2
                    + LH(bsz, lh) * j, ln, size=bsz, color=INK, ha="left")
    return TOP + len(data) * (RH + gap) - gap


def note(cv, W, y, text, size=9.8):
    for i, ln in enumerate(cv.wrap(text, W - 150, size)):
        cv.text(W / 2, y + LH(size, 1.45) * i, ln, size=size, color="#5d6875")
    return y + LH(size, 1.45) * len(cv.wrap(text, W - 150, size))


def banner(cv, W, y, msg, col="#c0392b", fc="#fbeeee", tc="#9c2b26", L=52,
           size=12):
    sz = min(cv.fit_size([msg], W - L * 2 - 60, size, weight="bold"), size)
    h = 30 + LH(sz, 1.5)
    cv.box(L, y, W - L * 2, h, fc=fc, ec=col, lw=2.0, radius=8)
    cv.text(W / 2, y + h / 2, msg, size=sz, color=tc, weight="bold")
    return y + h
