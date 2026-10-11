# -*- coding: utf-8 -*-
"""残った空白を、図を数段落ぶん後ろへ動かして詰める。

k=1,2,3 と順に試し、章ごとの空白合計が減ったものだけ採用する。
"""
import io, os, sys, importlib, subprocess
import autofit

HERE = autofit.HERE


def blocks_of(n):
    out = []
    for part in ("p1", "p2"):
        m = importlib.import_module("c%d_%s" % (n, part))
        out += list(m.BLOCKS)
    return out


def write_move(mv):
    src = io.open(os.path.join(HERE, "figmove.py"), encoding="utf-8").read()
    head = src.split("MOVE = ")[0]
    tail = src.split("\n\n\ndef reorder", 1)[1]
    body = "MOVE = {\n" + "".join('    "%s": %d,\n' % (k, v) for k, v in sorted(mv.items())) + "}"
    io.open(os.path.join(HERE, "figmove.py"), "w", encoding="utf-8").write(
        head + body + "\n\n\ndef reorder" + tail)


def measure(capmap):
    """章ごとの (空白合計, [(page,gap,fig)])"""
    res = {}
    for n, nm in autofit.NAMES.items():
        hits = autofit.scan(os.path.join(autofit.BASE, nm + ".pdf"), capmap)
        res[n] = (sum(h[1] for h in hits), hits)
    return res


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.path.insert(0, HERE)
    capmap = autofit.fig_map()
    blocks = {n: blocks_of(n) for n in range(1, 8)}
    fig_ch = {}
    nextkind = {}
    for n in range(1, 8):
        for i, b in enumerate(blocks[n]):
            if b[0] == "fig":
                fig_ch[b[1]] = n
                nextkind[b[1]] = blocks[n][i + 1][0] if i + 1 < len(blocks[n]) else "-"

    base = measure(capmap)
    print("開始： 空白合計 %.0fpt / %d 箇所"
          % (sum(v[0] for v in base.values()), sum(len(v[1]) for v in base.values())))
    mv = {}
    for k in (1, 2, 3):
        cand = {}
        for n, (tot, hits) in base.items():
            for pg, gap, fn in hits:
                if nextkind.get(fn) == "p" and mv.get(fn, 0) < k:
                    cand[fn] = k
        if not cand:
            break
        trial = dict(mv); trial.update(cand)
        write_move(trial)
        autofit.rebuild()
        new = measure(capmap)
        print("--- k=%d :" % k)
        keep = dict(mv)
        for n in range(1, 8):
            o, nn = base[n][0], new[n][0]
            ch_figs = [f for f in cand if fig_ch[f] == n]
            if not ch_figs:
                continue
            if nn < o - 20:
                print("   ch%d %.0f→%.0fpt 採用 %s" % (n, o, nn, ch_figs))
                for f in ch_figs:
                    keep[f] = k
            else:
                print("   ch%d %.0f→%.0fpt 不採用" % (n, o, nn))
        mv = keep
        write_move(mv)
        autofit.rebuild()
        base = measure(capmap)
        print("   現在： 空白合計 %.0fpt / %d 箇所"
              % (sum(v[0] for v in base.values()), sum(len(v[1]) for v in base.values())))
    print("\n最終：")
    for n, (tot, hits) in base.items():
        for pg, gap, fn in hits:
            print("   ch%d p%-3d gap=%3.0f %s" % (n, pg, gap, fn))


if __name__ == "__main__":
    main()
