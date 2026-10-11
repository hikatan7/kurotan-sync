# PowerPoint COM で実測しながら、枠に収まる最大サイズまで本文文字を拡大する
import sys, os, time
import win32com.client as wc

MAX_BODY = 18.0      # 本文の上限
SKIP_AT  = 14.0      # これ以上の文字を含む図形（見出し・題）は触らない
PAD      = 5.0       # 容器の下端に残す余白
HEAD     = 90.0      # これより上は見出し帯（540pt高さ基準）

def rect(sh):
    return (sh.Left, sh.Top, sh.Left + sh.Width, sh.Top + sh.Height)

def contains(a, b, tol=2.0):
    return a[0] - tol <= b[0] and a[1] - tol <= b[1] and a[2] + tol >= b[2] and a[3] + tol >= b[3]

def hov(a, b):
    return min(a[2], b[2]) - max(a[0], b[0])

def process_slide(sl, W, H, log):
    shapes = [sl.Shapes(i) for i in range(1, sl.Shapes.Count + 1)]
    rects = [rect(s) for s in shapes]
    changed = 0
    done = []   # (idx, mx, best, setf, fits)
    for idx, sh in enumerate(shapes):
        try:
            if sh.Type == 6 or not sh.HasTextFrame:
                continue
            tf = sh.TextFrame2
            if not tf.HasText:
                continue
            r0 = rects[idx]
            if r0[1] < HEAD * H / 540 or r0[1] > H - 20:
                continue
            tr = tf.TextRange
            if tf.AutoSize != 0:
                tf.AutoSize = 0
                sh.Top = r0[1]; sh.Height = r0[3] - r0[1]
            try:
                tr.LanguageID = 1041
                tr.ParagraphFormat.FarEastLineBreakLevel = -1   # 行頭禁則
            except Exception:
                pass
            segs = []
            for i in range(1, tr.Runs.Count + 1):
                r = tr.Runs.Item(i)
                segs.append((r.Start, r.Length, r.Font.Size))
            sizes = [s for _, _, s in segs if s and 0 < s < 200]
            if not sizes:
                continue
            mx = max(sizes)
            if mx >= SKIP_AT:
                continue
            conts = [rects[j] for j in range(len(shapes))
                     if j != idx and rects[j] != r0 and contains(rects[j], r0)
                     and (rects[j][2]-rects[j][0])*(rects[j][3]-rects[j][1]) < 0.9*W*H]
            limit = H - 14
            if conts:
                c = min(conts, key=lambda r: (r[2]-r[0])*(r[3]-r[1]))
                limit = min(limit, c[3] - PAD)
            for j in range(len(shapes)):
                if j == idx: continue
                rj = rects[j]
                if contains(rj, r0): continue
                if hov(rj, r0) > 2 and rj[1] >= r0[1] + 2:
                    limit = min(limit, rj[1] - 2)
            limit = max(limit, r0[3])
            h0 = r0[3] - r0[1]
            new_h = (limit - r0[1]) if tf.VerticalAnchor == 1 else h0
            avail = new_h - tf.MarginTop - tf.MarginBottom
            availw = sh.Width - tf.MarginLeft - tf.MarginRight
            base_lines = tr.Lines.Count
            paras = [tr.Paragraphs.Item(k).Text.strip() for k in range(1, tr.Paragraphs.Count + 1)]
            # 折り返していない「短い項目」（見出し・ラベル・数値）だけ行数を保つ。長い文は折り返してよい
            nowrap = (base_lines <= len(paras) and max((len(p) for p in paras), default=0) <= 22)                      or (base_lines == 1 and avail < 2.6 * mx)   # 1 行分の高さしかない帯（KEY MESSAGE など）
            sh.Height = new_h

            uniform = len({s for _, _, s in segs}) == 1

            def setf(f, tr=tr, segs=segs, uniform=uniform):
                if uniform:
                    tr.Font.Size = round(segs[0][2] * f * 2) / 2
                    return
                for st, ln, s in segs:
                    if s and 0 < s < 200:
                        tr.GetCharacters(st, ln).Font.Size = round(s * f * 2) / 2

            def fits(tr=tr, avail=avail, availw=availw, nowrap=nowrap, base_lines=base_lines):
                if tr.BoundHeight > avail + 0.5: return False
                if tr.BoundWidth > availw + 1.0: return False
                if nowrap and tr.Lines.Count > base_lines: return False
                return True

            fmax = MAX_BODY / mx
            bh, bw = tr.BoundHeight, tr.BoundWidth
            if nowrap:
                est = min(avail / max(bh, 1), availw / max(bw, 1))
            else:
                est = (avail / max(bh, 1)) ** 0.5
            f = min(fmax, est * 1.02)
            best = 1.0
            tries = 0
            while f >= 1.05 and tries < 8:
                setf(f); tries += 1
                if fits():
                    best = f; break
                f *= 0.95
            if best < 1.05:
                setf(1.0)
                sh.Height = h0
                done.append((idx, mx, 1.0, setf, fits))   # 同格の組を揃えるために残す
                continue
            changed += 1
            done.append((idx, mx, best, setf, fits))
            log.append((round(mx, 1), round(best, 2)))
        except Exception as e:
            log.append('ERR:%s' % e)
    # 2 巡目：同じ行・列に並ぶ同格の枠（表のセル・横並びカード）は倍率を揃える
    par = list(range(len(done)))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for a in range(len(done)):
        for b in range(a + 1, len(done)):
            ia, ib = done[a][0], done[b][0]
            ra, rb = rects[ia], rects[ib]
            if abs(done[a][1] - done[b][1]) > 1.5: continue
            same_row = abs(ra[1] - rb[1]) < 2 and abs((ra[3]-ra[1]) - (rb[3]-rb[1])) < 3
            if same_row:
                par[find(a)] = find(b)
    cur = [d[2] for d in done]
    comp = {}
    for a in range(len(done)):
        comp.setdefault(find(a), []).append(a)
    # 一度も拡大されなかった同格の枠があれば、その組は 1.0 に揃う（=拡大しない）ことになるので、
    # 拡大できなかった枠は組に入れていない（done に無い）。組の最小倍率に合わせる。
    for members in comp.values():
        if len(members) < 2: continue
        target = min(done[m][1] * done[m][2] for m in members)   # 仕上がりの文字サイズを揃える
        for m in members:
            idx, mx, best, setf, fits = done[m]
            f = max(1.0, target / mx)
            if abs(f - best) > 0.01:
                setf(f); cur[m] = f
    # 最終確認：溢れていたら収まるまで下げる
    for m, (idx, mx, best, setf, fits) in enumerate(done):
        f = cur[m]
        k = 0
        while not fits() and f > 1.0 and k < 12:
            f = max(1.0, f * 0.95); setf(f); k += 1
    return changed

def run(pptx, pdf_out=None, save=True):
    app = wc.gencache.EnsureDispatch('PowerPoint.Application')
    pres = app.Presentations.Open(os.path.abspath(pptx), False, False, False)
    try:
        W = pres.PageSetup.SlideWidth; H = pres.PageSetup.SlideHeight
        log = []; total = 0
        for i in range(1, pres.Slides.Count + 1):
            total += process_slide(pres.Slides(i), W, H, log)
        if save:
            pres.Save()
        if pdf_out:
            pres.SaveAs(os.path.abspath(pdf_out), 32)
        return total, log
    finally:
        pres.Close()

if __name__ == '__main__':
    t = time.time()
    n, log = run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    errs = [x for x in log if isinstance(x, str)]
    print('changed', n, 'errors', len(errs), errs[:3], '%.0fs' % (time.time() - t))
