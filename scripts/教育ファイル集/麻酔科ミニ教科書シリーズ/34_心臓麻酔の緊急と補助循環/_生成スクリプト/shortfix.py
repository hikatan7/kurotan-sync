# -*- coding: utf-8 -*-
"""短縮版の BLOCKS に本編の図を足し、図番号を振り直す。

short_additions.json（スクリプトと同じフォルダ）:
  [{"after": "見出しの先頭文字列", "fig": "f01_xxx.png"}, ...]
図は、見出しの直後の最初の段落（p）のあとに入る。見出しのすぐ後に表や箇条しかなければ見出しの直後。
キャプションは本編のもの（先頭の「図N-M｜」を外す）。
最後に、図のキャプションを「図1｜」「図2｜」…に振り直し、本文中の「図N」参照も同じ対応で直す。
"""
import glob
import importlib.util
import json
import os
import re
import sys


def _main_captions(here):
    caps = {}
    for p in sorted(glob.glob(os.path.join(here, 'c*_p*.py'))):
        spec = importlib.util.spec_from_file_location(os.path.basename(p)[:-3], p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for b in m.BLOCKS:
            if b[0] == 'fig':
                caps.setdefault(b[1], b[2])
    return caps


def prepare(blocks, here):
    blocks = list(blocks)
    jf = os.path.join(here, 'short_additions.json')
    if os.path.exists(jf):
        adds = json.load(open(jf, encoding='utf-8'))
        caps = _main_captions(here)
        have = {b[1] for b in blocks if b[0] == 'fig'}
        for a in adds:
            if a['fig'] in have:
                continue
            cap = re.sub(r'^図[\d\-－]+[｜|]\s*', '', caps.get(a['fig'], ''))
            # 見出しを探す
            hi = None
            for i, b in enumerate(blocks):
                if b[0] in ('h2', 'h3') and str(b[1]).startswith(a['after']):
                    hi = i
                    break
            if hi is None:
                print('!! anchor not found:', a['after'])
                continue
            pos = hi + 1
            if pos < len(blocks) and blocks[pos][0] == 'p':
                pos += 1
            blocks.insert(pos, ('fig', a['fig'], '図0｜' + cap))
            have.add(a['fig'])
    # 図番号の振り直し
    mapping = {}
    n = 0
    out = []
    for b in blocks:
        if b[0] == 'fig':
            n += 1
            m = re.match(r'^図(\d+)[｜|]', b[2])
            if m and m.group(1) != '0':
                mapping[m.group(1)] = str(n)
            cap = re.sub(r'^図[\d\-－]+([｜|])', '図%d\\1' % n, b[2])
            out.append((b[0], b[1], cap) + tuple(b[3:]))
        else:
            out.append(b)

    def fix(s):
        if not isinstance(s, str):
            return s
        return re.sub(r'図(\d+)(?![\d\-－])', lambda m: '図' + mapping.get(m.group(1), m.group(1)), s)

    res = []
    for b in out:
        if b[0] in ('p', 'lead'):
            res.append((b[0], fix(b[1])) + tuple(b[2:]))
        elif b[0] in ('ul', 'bul'):
            res.append((b[0], [fix(x) for x in b[1]]) + tuple(b[2:]))
        elif b[0] in ('note', 'sum'):
            res.append((b[0], b[1], [fix(x) for x in b[2]]) + tuple(b[3:]))
        else:
            res.append(b)
    return res


def figpath(figdir, name):
    """短縮版用に描き直した図（図版/_専攻医版/）があればそちらを使う。"""
    p = os.path.join(figdir, '_専攻医版', name)
    return p if os.path.exists(p) else os.path.join(figdir, name)
