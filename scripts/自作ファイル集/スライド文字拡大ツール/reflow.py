# スライドごとに本文倍率を 1 つ決め、伸びた文字の分だけ下の図形を押し下げて組み直す。
# 収まらなければ帯（横一列のブロック）の境目で 2 枚に分ける。
import sys, os, re, time
import win32com.client as wc

TARGET  = 13.0   # 本文（文字加重中央値）の目標
CAP     = 20.0   # 1 ランの上限
SKIP_AT = 14.5   # これ以上の文字しか無い図形は拡大対象外（見出し）
MIN_CHARS = 60

def R(sh):
    return [sh.Left, sh.Top, sh.Left + sh.Width, sh.Top + sh.Height]

def contains(a, b, tol=1.5):
    if a == b: return False
    if not (a[0]-tol <= b[0] and a[2]+tol >= b[2]): return False
    if a[1]-tol <= b[1] and a[3]+tol >= b[3]: return True
    # 表のセル：行の背景よりわずかに背が高い文字枠も「中」とみなす
    cy = (b[1] + b[3]) / 2
    return a[1]-tol <= b[1] and a[1] <= cy <= a[3] and (b[3] - a[3]) < 0.5 * (b[3] - b[1])

def hov(a, b):
    return min(a[2], b[2]) - max(a[0], b[0])

class Slide:
    def __init__(self, sl, W, H):
        self.sl, self.W, self.H = sl, W, H
        self.load()

    def load(self):
        sl, W, H = self.sl, self.W, self.H
        self.items = []
        for i in range(1, sl.Shapes.Count + 1):
            sh = sl.Shapes(i)
            r = R(sh)
            it = dict(sh=sh, r=r, text=False, segs=[], role='body')
            if r[1] < 90 * H / 540 and r[3] <= 96 * H / 540: it['role'] = 'head'
            elif r[1] > H - 20: it['role'] = 'foot'
            elif (r[2]-r[0]) * (r[3]-r[1]) > 0.85 * W * H: it['role'] = 'bg'
            try:
                if sh.HasTextFrame and sh.TextFrame2.HasText:
                    tf = sh.TextFrame2; tr = tf.TextRange
                    segs = []
                    for k in range(1, tr.Runs.Count + 1):
                        rn = tr.Runs.Item(k)
                        segs.append((rn.Start, rn.Length, rn.Font.Size, len(rn.Text.strip())))
                    it['segs'] = segs
                    it['text'] = True
            except Exception:
                pass
            it['free'] = sh.Type in (5,) or (sh.Type == 9 and False)
            self.items.append(it)
        body = [it for it in self.items if it['role'] == 'body']
        # 入れ子（容器）
        def area(r): return (r[2]-r[0]) * (r[3]-r[1])
        for n, it in enumerate(body): it['n'] = n
        def holds(a, b):   # a が b を含む（同じ大きさなら先に描かれた方が親）
            if a is b or not contains(a['r'], b['r']) and a['r'] != b['r']: return False
            if a['r'] == b['r'] or abs(area(a['r']) - area(b['r'])) < 1:
                return a['n'] < b['n'] and not b['text'] if a['text'] is False else False
            return area(a['r']) > area(b['r'])
        for it in body:
            it['kids'] = [o for o in body if holds(it, o)]
            it['parent'] = None
        for it in body:
            ps = [o for o in body if it in o['kids']]
            if ps:
                it['parent'] = min(ps, key=lambda o: (o['r'][2]-o['r'][0]) * (o['r'][3]-o['r'][1]))
        # 図（折れ線などの自由図形を含む容器）は硬い塊として扱う
        def inter(a, b):
            return min(a[2], b[2]) - max(a[0], b[0]) > 2 and min(a[3], b[3]) - max(a[1], b[1]) > 2
        for it in body:
            ks = it['kids']
            rigid = any(k['sh'].Type == 5 for k in ks)
            if not rigid:
                txt = [k for k in ks if k['text']]
                drw = [k for k in ks if not k['text'] and not k['kids'] and (k['r'][2]-k['r'][0]) > 8 and (k['r'][3]-k['r'][1]) > 8]
                for a in txt:
                    for b in drw:
                        if inter(a['r'], b['r']) and not contains(b['r'], a['r']) and not contains(a['r'], b['r']):
                            rigid = True; break
                    if rigid: break
            it['rigid'] = rigid
        for it in body:
            p = it['parent']; it['in_rigid'] = False
            while p is not None:
                if p['rigid']: it['in_rigid'] = True; break
                p = p['parent']
        # 拡大対象のテキスト
        for it in body:
            sz = [s for _, _, s, n in it['segs'] if s and 0 < s < 200 and n]
            it['scal'] = bool(it['text'] and sz and max(sz) < SKIP_AT and not it['in_rigid'])
            if it['scal']:
                sh = it['sh']; tf = sh.TextFrame2; tr = tf.TextRange
                try:
                    tr.LanguageID = 1041
                    tr.ParagraphFormat.FarEastLineBreakLevel = -1
                except Exception:
                    pass
                if tf.AutoSize != 0:
                    tf.AutoSize = 0
                    sh.Top = it['r'][1]; sh.Height = it['r'][3] - it['r'][1]
                it['mT'] = tf.MarginTop + tf.MarginBottom
                it['availw'] = sh.Width - tf.MarginLeft - tf.MarginRight
                paras = [tr.Paragraphs.Item(k).Text.strip() for k in range(1, tr.Paragraphs.Count + 1)]
                it['lines0'] = tr.Lines.Count
                it['plen'] = max((len(p) for p in paras), default=0)
                it['short'] = it['lines0'] <= len(paras) and it['plen'] <= 12
                it['bw0'] = tr.BoundWidth
                it['bh0'] = tr.BoundHeight
                it['uniform'] = len({s for _, _, s, _ in it['segs']}) == 1
                it['mx'] = max(sz)
        self.body = body
        self.find_grids()
        self.base_size()

    def find_grids(self):
        """表：同じ祖先の中で、左端と幅が揃ったセルの列が 2 本以上あるもの"""
        def root(x):
            while x['parent'] is not None: x = x['parent']
            return x
        sc = [it for it in self.body if it['scal']]
        byroot = {}
        for it in sc:
            byroot.setdefault(id(root(it)), []).append(it)
        self.grids = []
        for cells in byroot.values():
            cols = []
            for it in cells:
                for c in cols:
                    a = c[0]
                    if abs(a['r'][0] - it['r'][0]) < 2 and abs((a['r'][2]-a['r'][0]) - (it['r'][2]-it['r'][0])) < 3:
                        c.append(it); break
                else:
                    cols.append([it])
            cols = [c for c in cols if len(c) >= 2
                    and all(it['parent'] is None or (it['parent']['r'][2] - it['parent']['r'][0]) > 1.6 * (it['r'][2] - it['r'][0]) for it in c)]
            cols.sort(key=lambda c: c[0]['r'][0])
            # 横に重ならない列だけ
            ok = all(cols[i][0]['r'][2] <= cols[i+1][0]['r'][0] + 1 for i in range(len(cols) - 1))
            if len(cols) >= 2 and ok:
                for c in cols:
                    for it in c:
                        it['L0'] = it['sh'].Left; it['W0'] = it['sh'].Width
                        it['mLR'] = it['sh'].Width - it['availw']
                        if it['plen'] > 8: it['short'] = False
                self.grids.append(cols)

    def relayout_grids(self, f):
        for cols in self.grids:
            x0 = cols[0][0]['L0']; x1 = cols[-1][0]['L0'] + cols[-1][0]['W0']
            gaps = sum(cols[i+1][0]['L0'] - (cols[i][0]['L0'] + cols[i][0]['W0']) for i in range(len(cols) - 1))
            span = x1 - x0 - gaps
            ow = [c[0]['W0'] for c in cols]
            def needs(ff):
                out = []
                for c, w in zip(cols, ow):
                    n = 0.55 * w
                    for it in c:
                        if it['short'] and it['plen'] <= 8:
                            g = min(ff, CAP / it['mx'])
                            n = max(n, it['bw0'] * g * 1.04 + it['mLR'] + 2)
                    out.append(n)
                return out
            need = needs(f)
            if sum(need) > span:
                lo, hi = 1.0, f
                for _ in range(12):
                    mid = (lo + hi) / 2
                    if sum(needs(mid)) <= span: lo = mid
                    else: hi = mid
                need = needs(lo)
            if sum(need) <= span:
                extra = span - sum(need)
                ws = [n + extra * w / sum(ow) for n, w in zip(need, ow)]
            else:
                ws = ow[:]   # 広げきれない：元の幅（短い項目は文字の方を抑える）
            x = x0
            for i, (c, w) in enumerate(zip(cols, ws)):
                for it in c:
                    if abs(it['sh'].Left - x) > 0.1: it['sh'].Left = x
                    if abs(it['sh'].Width - w) > 0.1: it['sh'].Width = w
                    it['availw'] = w - it['mLR']
                if i + 1 < len(cols):
                    x += w + (cols[i+1][0]['L0'] - (c[0]['L0'] + c[0]['W0']))

    def base_size(self):
        b = self._base_size()
        self._base = b[0] if b[1] else 10
        return b

    def _base_size(self):
        acc = sorted((s, n) for it in self.body if it['scal'] for _, _, s, n in it['segs'] if s and n)
        tot = sum(n for _, n in acc)
        if not tot: return 99, 0
        c = 0
        for s, n in acc:
            c += n
            if c >= tot / 2: return s, tot

    def fcap(self, it, f):
        if it['short'] and it['bw0'] > 0:
            f = min(f, max(1.0, it['availw'] / it['bw0'] * 0.97))
        return min(f, CAP / it['mx'])

    def rows(self):
        if hasattr(self, '_rows'): return self._rows
        sc = [it for it in self.body if it['scal']]
        def root(x):
            while x['parent'] is not None: x = x['parent']
            return x
        par = {id(it): id(it) for it in sc}
        def find(a):
            while par[a] != a: a = par[a]
            return a
        for i, a in enumerate(sc):
            for b in sc[i+1:]:
                if abs(a['mx'] - b['mx']) >= 0.8: continue
                same_row = abs(a['r'][1] - b['r'][1]) < 2.5 and abs((a['r'][3]-a['r'][1]) - (b['r'][3]-b['r'][1])) < 4
                same_col = root(a) is root(b) and a['parent'] is not None                     and abs(a['r'][0] - b['r'][0]) < 2 and abs((a['r'][2]-a['r'][0]) - (b['r'][2]-b['r'][0])) < 3                     and max(a['r'][3]-a['r'][1], b['r'][3]-b['r'][1]) < 40
                if same_row or same_col:
                    par[find(id(a))] = find(id(b))
        self._rows = {id(it): find(id(it)) for it in sc}
        return self._rows

    def apply_sizes(self, f):
        self.relayout_grids(f)
        rows = self.rows()
        gmin = {}
        for it in self.body:
            if it['scal']:
                k = rows[id(it)]
                gmin[k] = min(gmin.get(k, 99), self.fcap(it, f) * it['mx'])
        for it in self.body:
            if not it['scal']: continue
            g = gmin[rows[id(it)]] / it['mx']
            floor = 0 if it['short'] else 0.9 * f * self._base
            def sz(s):
                return round(min(CAP, max(s * g, min(floor, s * g * 1.6))) * 2) / 2
            tr = it['sh'].TextFrame2.TextRange
            if it['uniform']:
                tr.Font.Size = sz(it['segs'][0][2])
            else:
                for st, ln, s, _ in it['segs']:
                    if s and 0 < s < 200:
                        tr.GetCharacters(st, ln).Font.Size = sz(s)

    def layout(self, f):
        """f を当てたときの各図形の新しい上端・下端を計算（まだ動かさない）"""
        self.apply_sizes(f)
        req = {}
        for it in self.body:
            if it['scal']:
                tr = it['sh'].TextFrame2.TextRange
                sh = it['sh']; w = sh.Width
                sh.Width = w * 0.95            # PDF 書き出しとの改行ずれに備えて狭めて測る
                req[id(it)] = tr.BoundHeight + it['mT'] + 4
                sh.Width = w
        order = sorted(self.body, key=lambda it: (it['r'][1], -(it['r'][3])))
        if not hasattr(self, '_peers'):
            for a in self.body:
                a['peers'] = [b for b in self.body if b is not a and b['parent'] is a['parent']
                              and abs(a['r'][1] - b['r'][1]) < 2.5 and abs(a['r'][3] - b['r'][3]) < 4
                              and hov(a['r'], b['r']) <= 1 and not a['kids'] and not b['kids']
                              and (a['r'][3]-a['r'][1]) < 60]
            self._peers = True
        newT, newB = {}, {}
        memo = {}

        peerD = {}
        def D(p):   # 下端の移動量
            k = id(p)
            if k in memo: return max(memo[k], peerD.get(k, -1e9))
            memo[k] = 0.0
            place(p)
            memo[k] = newB[k] - p['r'][3]
            return max(memo[k], peerD.get(k, -1e9))

        def shift(s):
            m = 0.0
            for p in self.body:
                if p is s or s in p['kids'] or p in s['kids']: continue
                if p['r'][3] <= s['r'][1] + 1 and hov(p['r'], s['r']) > 1:
                    m = max(m, D(p))
            # 容器の中の図形は、容器が下がった分も下がる
            if s['parent'] is not None:
                m = max(m, shift_of(s['parent']))
            return m

        shift_cache = {}
        def shift_of(s):
            k = id(s)
            if k not in shift_cache:
                shift_cache[k] = 0.0
                shift_cache[k] = shift(s)
            return shift_cache[k]

        def place(it):
            k = id(it)
            if k in newB: return
            if it.get('peers'):
                # 表の同じ行：全員を置いてから下端を最大に揃える
                grp = [it] + it['peers']
                for g in grp:
                    place1(g)
                mb = max(newB[id(g)] - g['r'][3] for g in grp)
                for g in grp:
                    newB[id(g)] = g['r'][3] + mb if not g['scal'] else max(newB[id(g)], newT[id(g)] + (g['r'][3]-g['r'][1]))
                    peerD[id(g)] = mb
                return
            place1(it)

        def place1(it):
            k = id(it)
            if k in newB: return
            t = it['r'][1] + shift_of(it)
            h = it['r'][3] - it['r'][1]
            if it['scal']:
                h = max(h, req[k])
            newT[k] = t; newB[k] = t + h
            if it['kids'] and not it['rigid']:
                full = []
                for c in it['kids']:
                    if c['parent'] is not it: continue
                    ch = c['r']
                    if abs(ch[1] - it['r'][1]) < 2 and abs(ch[3] - it['r'][3]) < 2 and not c['scal']:
                        full.append(c); continue   # 縁取りの帯は後で伸ばす
                    place(c)
                    gap = it['r'][3] - ch[3]
                    newB[k] = max(newB[k], newB[id(c)] + gap)
                for c in full:
                    newT[id(c)] = newT[k]; newB[id(c)] = newB[k]
                    memo[id(c)] = newB[k] - c['r'][3]
            elif it['kids'] and it['rigid']:
                s0 = newT[k] - it['r'][1]
                for c in it['kids']:
                    newT[id(c)] = c['r'][1] + s0; newB[id(c)] = c['r'][3] + s0
                    memo[id(c)] = s0

        for it in order:
            D(it)
        bottom = max((newB[id(it)] for it in self.body), default=0)
        return newT, newB, bottom

    def commit(self, newT, newB):
        for it in self.body:
            k = id(it)
            if k not in newT: continue
            sh = it['sh']
            try:
                if sh.Type == 9 and abs(it['r'][3] - it['r'][1]) < 1:
                    sh.Top = newT[k]
                else:
                    sh.Top = newT[k]
                    h = newB[k] - newT[k]
                    if abs(h - (it['r'][3] - it['r'][1])) > 0.2:
                        sh.Height = h
            except Exception:
                pass

    def limit(self):
        return self.H - 16 * self.H / 540

    def best_f(self):
        base, n = self.base_size()
        if n < 1: return 1.0, base
        fmax = max(1.0, min(TARGET * 1.25 / base, CAP / base))
        lo, hi = 1.0, fmax
        _, _, b = self.layout(hi)
        if b <= self.limit():
            return hi, base
        for _ in range(5):
            mid = (lo + hi) / 2
            _, _, b = self.layout(mid)
            if b <= self.limit(): lo = mid
            else: hi = mid
        return lo, base

    def finish(self, f):
        nT, nB, b = self.layout(f)
        if b > self.limit() + 0.5 and f > 1.0:
            nT, nB, b = self.layout(1.0)
        self.commit(nT, nB)
        return b

def bands_of(S):
    top = [it for it in S.body if it['parent'] is None]
    iv = sorted(top, key=lambda it: it['r'][1])
    out = []
    for it in iv:
        t, b = it['r'][1], it['r'][3]
        if out and t < out[-1][1] + 4:   # 重なる・接している（表の行）は同じ帯
            out[-1][1] = max(out[-1][1], b); out[-1][2].append(it)
        else:
            out.append([t, b, [it]])
    return out

def members(it):
    res = [it]
    for k in it['kids']:
        res.append(k)
    return res

def compact(S, keep_ids, H):
    """残す帯を本文領域の上から詰めて並べ直す"""
    y = 95 * H / 540
    prev_b = None
    for t, b, tops in sorted(keep_ids, key=lambda x: x[0]):
        gap = 0 if prev_b is None else max(6, min(14, t - prev_b))
        y += gap
        dy = y - t
        for it in tops:
            for m in members(it):
                m['sh'].Top = m['r'][1] + dy
        y += b - t
        prev_b = b

def tag_kicker(sl, H, tag):
    for k in range(1, sl.Shapes.Count + 1):
        sh = sl.Shapes(k)
        if sh.Top < 45 * H / 540 and sh.HasTextFrame and sh.TextFrame2.HasText:
            tr = sh.TextFrame2.TextRange
            if tr.Font.Size < 14:
                t = re.sub(r'\s*（\d/\d）$', '', tr.Text)
                tr.Text = t + ' ' + tag
            return

def process_slide(pres, i, W, H, depth=0):
    """スライド i を処理。増えた枚数を返す"""
    sl = pres.Slides(i)
    if i == 1 and depth == 0:
        return 0, 'title'
    S = Slide(sl, W, H)
    base, n = S.base_size()
    if n < 1 or base >= TARGET:
        return 0, None
    f, base = S.best_f()
    bs = bands_of(S)
    if f * base >= TARGET - 0.25 or len(bs) < 2 or n < MIN_CHARS or depth >= 2:
        S.finish(f)
        return 0, round(f * base, 1)
    # 2 枚に分ける
    hs = [b[1] - b[0] for b in bs]; tot = sum(hs)
    k = min(range(1, len(bs)), key=lambda j: abs(sum(hs[:j]) - tot / 2))
    g1, g2 = bs[:k], bs[k:]
    S.apply_sizes(1.0)
    ids = [id(it) for it in S.items]
    dup = sl.Duplicate().Item(1)
    # dup は同じ並び順
    in1 = {id(m) for _, _, tops in g1 for it in tops for m in members(it)}
    in2 = {id(m) for _, _, tops in g2 for it in tops for m in members(it)}
    idx1 = [j + 1 for j, it in enumerate(S.items) if id(it) in in1]
    idx2 = [j + 1 for j, it in enumerate(S.items) if id(it) in in2]
    for j in sorted(idx2, reverse=True): sl.Shapes(j).Delete()
    for j in sorted(idx1, reverse=True): dup.Shapes(j).Delete()
    for s_, grp in ((sl, g1), (dup, g2)):
        T = Slide(s_, W, H)
        # 帯を上に詰める
        tb = bands_of(T)
        compact(T, tb, H)
    old = sl.Shapes.Count
    tag_kicker(sl, H, '（1/2）'); tag_kicker(dup, H, '（2/2）')
    a1, _ = process_slide(pres, i, W, H, depth + 1)
    a2, _ = process_slide(pres, i + 1 + a1, W, H, depth + 1)
    return 1 + a1 + a2, 'split'

def renumber(pres, H):
    for k in range(1, pres.Slides.Count + 1):
        s_ = pres.Slides(k)
        for j in range(1, s_.Shapes.Count + 1):
            sh = s_.Shapes(j)
            try:
                if sh.Top > H - 20 and sh.HasTextFrame and sh.TextFrame2.HasText:
                    tr = sh.TextFrame2.TextRange
                    m = re.search(r'[｜|]\s*(\d+)\s*$', tr.Text)
                    if m:
                        tr.GetCharacters(m.start(1) + 1, len(m.group(1))).Text = str(k)
            except Exception:
                pass

def run(pptx, pdf_out=None, save=True):
    app = wc.gencache.EnsureDispatch('PowerPoint.Application')
    pres = app.Presentations.Open(os.path.abspath(pptx), False, False, False)
    rep = []
    try:
        W = pres.PageSetup.SlideWidth; H = pres.PageSetup.SlideHeight
        n0 = pres.Slides.Count
        i = 1
        while i <= pres.Slides.Count:
            try:
                add, info = process_slide(pres, i, W, H)
            except Exception as e:
                add, info = 0, 'ERR %s' % e
            rep.append((i, info))
            i += 1 + add
        renumber(pres, H)
        if save: pres.Save()
        if pdf_out: pres.SaveAs(os.path.abspath(pdf_out), 32)
        return n0, pres.Slides.Count, rep
    finally:
        pres.Close()

if __name__ == '__main__':
    t = time.time()
    n0, n1, rep = run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    errs = [r for r in rep if isinstance(r[1], str) and r[1].startswith('ERR')]
    print('slides', n0, '->', n1, 'errors', len(errs), errs[:3], '%.0fs' % (time.time() - t))
    print(rep)
