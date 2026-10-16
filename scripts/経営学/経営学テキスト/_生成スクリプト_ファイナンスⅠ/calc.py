# -*- coding: utf-8 -*-
"""ファイナンスⅠの架空例の計算。本文の数字はすべてここから取る（手で書き写さない）。

単位は百万円。病院・数字はすべて架空。
    python calc.py   → 主要な数字を一覧で出す（検算用）
"""

# ---------------------------------------------------------------- 第7章 資本コスト
RF = 3.0          # 10年国債利回り（%）。財務省 国債金利情報 2026-10-14 の 3.015% を丸めた
MRP = 6.0         # 市場リスクプレミアム（%）。仮定
BETA_U = 0.70     # 類似の上場企業のアンレバード・ベータ（架空）
DV = 0.40         # 目標とする負債比率 D/V
RD = 3.5          # 借入金利（%）（架空）
TAX = 0.30        # 実効税率（架空の前提）

DE = DV / (1 - DV)
BETA_L = BETA_U * (1 + (1 - TAX) * DE)
RE = RF + BETA_L * MRP
RD_AT = RD * (1 - TAX)
WACC_RAW = DV * RD_AT + (1 - DV) * RE
WACC = round(WACC_RAW * 2) / 2          # 0.5% 刻みに丸めて使う
R = WACC / 100

# ---------------------------------------------------------------- 第2章 ロボット導入（A案）
YEARS = 6
INV = 350.0       # 機器 300 ＋ 手術室改修 50
SUNK = 5.0        # 昨年の導入可否調査費（埋没費用）
ALLOC = 20.0      # 共通費の配賦額（増えない費用）
NEW_N = 130       # 新たに獲得する症例（件/年）
NEW_REV = 1.80    # 1件あたり入院収益
NEW_VC = 0.70     # 1件あたり変動費（材料・薬剤・専用器具）
REP_N = 80        # 腹腔鏡からの置き換え（件/年）
REP_REV = 0.15    # 置き換え1件あたりの収益増
REP_VC = 0.25     # 置き換え1件あたりの変動費増
STAFF = 15.0      # 追加の人件費
MAINT = 20.0      # 保守契約
STORE = 3.0       # 改修で失う倉庫の代わりの外部倉庫（機会費用）
WC_MONTHS = 2     # 未収金＝増分収益の2か月分


def project(new_n=NEW_N, new_rev=NEW_REV, new_vc=NEW_VC, inv=INV, maint=MAINT,
            rep_n=REP_N, rate=None, years=YEARS):
    rate = R if rate is None else rate
    rev = new_n * new_rev + rep_n * REP_REV
    vc = new_n * new_vc + rep_n * REP_VC
    fixed = STAFF + maint + STORE
    ebitda = rev - vc - fixed
    dep = inv / years
    ebit = ebitda - dep
    tax = ebit * TAX
    nopat = ebit - tax
    fcf = nopat + dep
    wc = rev * WC_MONTHS / 12
    cfs = [-(inv + wc)] + [fcf] * years
    cfs[-1] += wc
    return dict(rev=rev, vc=vc, fixed=fixed, ebitda=ebitda, dep=dep, ebit=ebit,
                tax=tax, nopat=nopat, fcf=fcf, wc=wc, cfs=cfs, npv=npv(cfs, rate))


def npv(cfs, r):
    return sum(c / (1 + r) ** t for t, c in enumerate(cfs))


def irr(cfs, lo=-0.9, hi=1.0):
    f = lambda r: npv(cfs, r)
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def payback(cfs, r=None):
    cum = 0.0
    for t, c in enumerate(cfs):
        cc = c if r is None else c / (1 + r) ** t
        if t > 0 and cum < 0 <= cum + cc:
            return t - 1 + (-cum) / cc
        cum += cc
    return None


A = project()
A_IRR = irr(A["cfs"])
A_PB = payback(A["cfs"])
A_DPB = payback(A["cfs"], R)

# 埋没費用・配賦費を誤って入れた場合
A_WRONG = npv([A["cfs"][0] - SUNK] + [c - ALLOC * (1 - TAX) for c in A["cfs"][1:]], R)

# 損益分岐の新規症例数（NPV＝0）
_per_case = (NEW_REV - NEW_VC) * (1 + WC_MONTHS / 12 * 0)   # 目安（下で正確に二分法）


def breakeven_cases():
    lo, hi = 0.0, 300.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if project(new_n=mid)["npv"] < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


BE_N = breakeven_cases()

# ---------------------------------------------------------------- 第3章 B案（腹腔鏡システム更新）との比較
B_INV = 60.0
B_FCF = 15.0
B_CFS = [-B_INV] + [B_FCF] * YEARS
B_NPV = npv(B_CFS, R)
B_IRR = irr(B_CFS)
B_PB = payback(B_CFS)


def crossover():
    diff = [a - b for a, b in zip(A["cfs"], B_CFS)]
    return irr(diff)


CROSS = crossover()
PI_A = (npv(A["cfs"], R) - A["cfs"][0]) / -A["cfs"][0]
PI_B = (B_NPV + B_INV) / B_INV

# 複数のIRR：撤去・原状回復費用が最後に大きく出る例
M_CFS = [-100.0, 230.0, -132.0]


def irr_all(cfs, lo=-0.5, hi=1.5, steps=4000):
    out, prev = [], None
    for i in range(steps + 1):
        r = lo + (hi - lo) * i / steps
        v = npv(cfs, r)
        if prev is not None and (prev[1] == 0 or prev[1] * v < 0):
            out.append(irr(cfs, prev[0], r))
        prev = (r, v)
    return out


M_IRRS = irr_all(M_CFS)

# ---------------------------------------------------------------- 第4章 感度・シナリオ
SENS = [
    ("新規症例数 ±20%", project(new_n=NEW_N * 0.8)["npv"], project(new_n=NEW_N * 1.2)["npv"]),
    ("1件あたり収益 ±10%", project(new_rev=NEW_REV * 0.9)["npv"], project(new_rev=NEW_REV * 1.1)["npv"]),
    ("1件あたり変動費 ±10%", project(new_vc=NEW_VC * 1.1)["npv"], project(new_vc=NEW_VC * 0.9)["npv"]),
    ("投資額 ±10%", project(inv=INV * 1.1)["npv"], project(inv=INV * 0.9)["npv"]),
    ("割引率 ±1ポイント", project(rate=R + 0.01)["npv"], project(rate=R - 0.01)["npv"]),
    ("保守費 ±20%", project(maint=MAINT * 1.2)["npv"], project(maint=MAINT * 0.8)["npv"]),
]
SENS.sort(key=lambda s: -(s[2] - s[1]))

SCEN = [("悲観", 0.25, 100), ("基本", 0.50, NEW_N), ("楽観", 0.25, 155)]
SCEN_NPV = [(n, p, c, project(new_n=c)["npv"]) for n, p, c in SCEN]
E_NPV = sum(p * v for _, p, _, v in SCEN_NPV)

# ---------------------------------------------------------------- 第5章 待つオプション
# 1年後に紹介元の再編（近隣病院の外科縮小）が決まる。決まれば新規 165 件、決まらなければ 95 件。確率は半々。
P_GOOD = 0.5
GOOD_N, BAD_N = 165, 95
NOW_GOOD = project(new_n=GOOD_N)["npv"]
NOW_BAD = project(new_n=BAD_N)["npv"]
NOW_E = P_GOOD * NOW_GOOD + (1 - P_GOOD) * NOW_BAD
# 1年待つと、良い場合だけ投資する（1年遅れるので1年分割り引く）。悪い場合は投資しない（0）
WAIT_E = P_GOOD * max(NOW_GOOD, 0) / (1 + R) + (1 - P_GOOD) * max(NOW_BAD, 0) / (1 + R)
OPT_VALUE = WAIT_E - max(NOW_E, 0)

# 撤退オプション：3年目末に中古で売却できる（売却額 180＝機器300の6割）。悪い場合だけ使う
SALVAGE = 180.0


def abandon_npv(new_n):
    p = project(new_n=new_n)
    cf = p["cfs"][:4]
    # 3年目末に売却：簿価 175 との差額（売却益）には税がかかる。運転資本も回収
    book = INV - p["dep"] * 3
    cf[3] += SALVAGE + (book - SALVAGE) * TAX + p["wc"]
    return npv(cf, R)


ABN_BAD = abandon_npv(BAD_N)
ABN_E = P_GOOD * NOW_GOOD + (1 - P_GOOD) * max(NOW_BAD, ABN_BAD)
ABN_VALUE = ABN_E - NOW_E

# ---------------------------------------------------------------- 第6章 CAPM の例
CAPM_ROWS = [(b, RF + b * MRP) for b in (0.5, 0.7, 1.0, 1.3)]

# ---------------------------------------------------------------- 第8章 DCF（C病院の事業譲受）
C_WACC = 7.0
C_G = 0.5
C_FCF = [110.0, 135.0, 155.0, 165.0, 170.0]
C_DEBT = 1200.0       # 引き継ぐ有利子負債
C_CASH = 150.0


def dcf(wacc=C_WACC, g=C_G):
    r, gg = wacc / 100, g / 100
    pv = sum(f / (1 + r) ** (t + 1) for t, f in enumerate(C_FCF))
    tv = C_FCF[-1] * (1 + gg) / (r - gg)
    pv_tv = tv / (1 + r) ** len(C_FCF)
    return dict(pv=pv, tv=tv, pv_tv=pv_tv, ev=pv + pv_tv)


C = dcf()
C_EQ = C["ev"] - C_DEBT + C_CASH
C_TV_SHARE = C["pv_tv"] / C["ev"]
C_GRID = [[dcf(w, g)["ev"] for g in (0.0, 0.5, 1.0)] for w in (6.0, 7.0, 8.0)]

# ---------------------------------------------------------------- 第9章 マルチプル
C_EBITDA = 330.0       # C病院の今期 EBITDA（架空）
MULT = (6.0, 7.5, 9.0)  # 類似取引の EV/EBITDA（架空）
C_EV_MULT = [m * C_EBITDA for m in MULT]
C_IMPLIED = C["ev"] / C_EBITDA

# ---------------------------------------------------------------- 第10章 資本構成（MM）
MM_EBIT = 600.0        # 毎年一定の営業利益（永久）
MM_RU = 7.0            # 負債がないときの資本コスト（%）
MM_D = 3000.0
MM_RD = 3.5
VU = MM_EBIT * (1 - TAX) / (MM_RU / 100)
TS = TAX * MM_D
VL = VU + TS
MM_ROWS = []
for d in (0.0, 1500.0, 3000.0, 4500.0):
    e = VU + TAX * d - d
    re = MM_RU + (MM_RU - MM_RD) * (1 - TAX) * d / e
    w = (d * MM_RD * (1 - TAX) + e * re) / (d + e)
    MM_ROWS.append((d, e, re, w))


def f0(x):
    return format(round(x), ",")


def f1(x):
    return "%.1f" % x


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("βL=%.3f re=%.2f rd_at=%.2f WACC=%.3f→%.1f" % (BETA_L, RE, RD_AT, WACC_RAW, WACC))
    for k in ("rev", "vc", "fixed", "ebitda", "dep", "ebit", "tax", "nopat", "fcf", "wc", "npv"):
        print(k, round(A[k], 2))
    print("cfs", [round(c, 1) for c in A["cfs"]])
    print("IRR %.2f%% PB %.2f DPB %s wrongNPV %.1f BE_N %.1f" % (A_IRR * 100, A_PB, A_DPB and round(A_DPB, 2), A_WRONG, BE_N))
    print("B NPV %.1f IRR %.2f%% PB %.2f cross %.2f%% PI_A %.3f PI_B %.3f" % (B_NPV, B_IRR * 100, B_PB, CROSS * 100, PI_A, PI_B))
    print("M IRRs", [round(x * 100, 2) for x in M_IRRS], [round(npv(M_CFS, r), 2) for r in (0, .1, .2, .3)])
    for s in SENS:
        print("sens", s[0], round(s[1], 1), round(s[2], 1))
    for s in SCEN_NPV:
        print("scen", s[0], s[1], s[2], round(s[3], 1))
    print("E_NPV", round(E_NPV, 1))
    print("good %.1f bad %.1f nowE %.1f waitE %.1f opt %.1f" % (NOW_GOOD, NOW_BAD, NOW_E, WAIT_E, OPT_VALUE))
    print("abandon bad %.1f E %.1f value %.1f" % (ABN_BAD, ABN_E, ABN_VALUE))
    print("CAPM", CAPM_ROWS)
    print("DCF", {k: round(v, 1) for k, v in C.items()}, "EQ", round(C_EQ, 1), "TV share", round(C_TV_SHARE, 3))
    print("grid", [[round(x) for x in r] for r in C_GRID])
    print("mult", C_EV_MULT, "implied", round(C_IMPLIED, 2))
    print("VU %.0f TS %.0f VL %.0f" % (VU, TS, VL))
    for r in MM_ROWS:
        print("MM D=%.0f E=%.0f re=%.2f wacc=%.2f" % r)
