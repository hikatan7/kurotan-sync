# -*- coding: utf-8 -*-
"""アカウンティングⅠの架空例の計算。本文の数字はすべてここから取る（手で書き写さない）。

単位は百万円。病院・数字はすべて架空。比率は期末の残高で計算する。
    python calc.py   → 主要な数字を一覧で出す（検算用）
"""

TAX = 0.30        # 法人税等の実効税率（架空の前提）
BEDS = 400        # 一般病床数

# ---------------------------------------------------------------- 第1章 A病院の損益計算書（前期 Y1・当期 Y2）
PL = {
    "Y1": dict(inpt=8600.0, outpt=3000.0, other=400.0,
               salary=6240.0, material=3000.0, outsrc=720.0, equip=1200.0, dep=720.0, expense=360.0,
               nonop_in=150.0, interest=90.0, occ=0.85),
    "Y2": dict(inpt=9050.0, outpt=3150.0, other=400.0,
               salary=6700.0, material=3280.0, outsrc=760.0, equip=1320.0, dep=820.0, expense=380.0,
               nonop_in=160.0, interest=110.0, occ=0.84),
}
for _p in PL.values():
    _p["rev"] = _p["inpt"] + _p["outpt"] + _p["other"]
    _p["cost"] = _p["salary"] + _p["material"] + _p["outsrc"] + _p["equip"] + _p["expense"]
    _p["op"] = _p["rev"] - _p["cost"]                    # 医業利益
    _p["ord"] = _p["op"] + _p["nonop_in"] - _p["interest"]   # 経常利益（臨時損益はなし）
    _p["tax"] = _p["ord"] * TAX
    _p["ni"] = _p["ord"] - _p["tax"]
    _p["ebitda"] = _p["op"] + _p["dep"]
    _p["days"] = BEDS * _p["occ"] * 365                  # 延べ入院患者数（人日）
    _p["unit"] = _p["inpt"] * 1e6 / _p["days"]           # 入院1日あたり単価（円）
P1, P2 = PL["Y1"], PL["Y2"]

# ---------------------------------------------------------------- 第1章 貸借対照表（Y1期末・Y2期末）
CAPEX = 1700.0       # Y2 の設備投資（医療機器の更新と手術室の改修）
NEW_LOAN = 1000.0    # Y2 の新規の長期借入
REPAY = 600.0        # Y2 の約定返済（Y1 期末の1年以内返済分）

B1 = dict(cash=1500.0, ar=2100.0, inv=200.0, oca=100.0, ppe=9000.0, ofa=600.0,
          ap=700.0, std=600.0, ocl=900.0, ltd=5600.0, ret=700.0, na=5000.0)

# Y2 の動き（現金以外）
B2 = dict(ar=2300.0, inv=240.0, oca=100.0, ofa=600.0, ap=760.0, ocl=960.0, ret=740.0)
B2["ppe"] = B1["ppe"] + CAPEX - P2["dep"]
_debt2 = B1["std"] + B1["ltd"] + NEW_LOAN - REPAY
B2["std"] = 650.0
B2["ltd"] = _debt2 - B2["std"]
B2["na"] = B1["na"] + P2["ni"]                          # 医療法人は配当しない

# ---------------------------------------------------------------- 第6章 キャッシュフロー計算書（間接法、Y2）
CF = dict(
    pretax=P2["ord"], dep=P2["dep"], d_ret=B2["ret"] - B1["ret"],
    d_ar=-(B2["ar"] - B1["ar"]), d_inv=-(B2["inv"] - B1["inv"]), d_oca=-(B2["oca"] - B1["oca"]),
    d_ap=B2["ap"] - B1["ap"], d_ocl=B2["ocl"] - B1["ocl"], taxpaid=-P2["tax"],
)
CF_OP = sum(CF.values())
CF_INV = -CAPEX
CF_FIN = NEW_LOAN - REPAY
CF_NET = CF_OP + CF_INV + CF_FIN
FCF = CF_OP + CF_INV
B2["cash"] = B1["cash"] + CF_NET


def _tot(b):
    ca = b["cash"] + b["ar"] + b["inv"] + b["oca"]
    fa = b["ppe"] + b["ofa"]
    cl = b["ap"] + b["std"] + b["ocl"]
    fl = b["ltd"] + b["ret"]
    return dict(ca=ca, fa=fa, ta=ca + fa, cl=cl, fl=fl, tl=cl + fl, debt=b["std"] + b["ltd"],
                tle=cl + fl + b["na"])


for _b in (B1, B2):
    _b.update(_tot(_b))
    assert abs(_b["ta"] - _b["tle"]) < 1e-6, "貸借が一致しない"

# ---------------------------------------------------------------- 第2〜5章 指標
def ratios(p, b):
    r = {}
    r["op_m"] = p["op"] / p["rev"] * 100
    r["ord_m"] = p["ord"] / p["rev"] * 100
    r["ni_m"] = p["ni"] / p["rev"] * 100
    r["ebitda_m"] = p["ebitda"] / p["rev"] * 100
    for k in ("salary", "material", "outsrc", "equip", "dep", "expense"):
        r[k] = p[k] / p["rev"] * 100
    r["at"] = p["rev"] / b["ta"]
    r["ft"] = p["rev"] / b["fa"]
    r["ar_days"] = b["ar"] / p["rev"] * 365
    r["inv_days"] = b["inv"] / p["material"] * 365
    r["ap_days"] = b["ap"] / p["material"] * 365
    r["cur"] = b["ca"] / b["cl"] * 100
    r["quick"] = (b["cash"] + b["ar"]) / b["cl"] * 100
    r["eq"] = b["na"] / b["ta"] * 100
    r["fix_lt"] = b["fa"] / (b["na"] + b["fl"]) * 100
    r["de"] = b["debt"] / b["na"]
    r["repay_yrs"] = b["debt"] / (p["ni"] + p["dep"])
    r["icr"] = p["op"] / p["interest"]
    r["cash_days"] = b["cash"] / ((p["cost"] - p["dep"]) / 365)
    r["roa"] = p["ord"] / b["ta"] * 100
    r["roe"] = p["ni"] / b["na"] * 100
    r["lev"] = b["ta"] / b["na"]
    return r


R1, R2 = ratios(P1, B1), ratios(P2, B2)

# デュポン：Y1→Y2 の ROE の変化を3要因に分ける（順に置き換える）
_m1, _m2 = R1["ni_m"] / 100, R2["ni_m"] / 100
DP_STEPS = [
    ("純利益率", R1["at"] * R1["lev"] * (_m2 - _m1) * 100),
    ("総資産回転率", _m2 * R1["lev"] * (R2["at"] - R1["at"]) * 100),
    ("財務レバレッジ", _m2 * R2["at"] * (R2["lev"] - R1["lev"]) * 100),
]
assert abs(sum(s[1] for s in DP_STEPS) - (R2["roe"] - R1["roe"])) < 1e-9

# 比較の3病院（架空）：ROE は近いが、たどる道が違う
PEERS = [
    # 名前, 純利益率%, 総資産回転率, 財務レバレッジ
    ("A病院（当期）", R2["ni_m"], R2["at"], R2["lev"]),
    ("B病院（回転型）", 1.6, 1.30, 1.60),
    ("C病院（借入型）", 1.0, 0.85, 4.00),
    ("D病院（利益率型）", 3.0, 0.70, 1.55),
]
PEERS = [(n, m, t, l, m * t * l) for n, m, t, l in PEERS]

# ---------------------------------------------------------------- 第7章 CF の組み合わせ（架空の4病院）
CF_PATTERNS = [
    ("A病院（当期）", CF_OP, CF_INV, CF_FIN),
    ("E病院", 900.0, -500.0, -350.0),
    ("F病院", -200.0, 300.0, 250.0),
    ("G病院", -150.0, -80.0, 400.0),
]

# ---------------------------------------------------------------- 第8章 CVP（当期 Y2）
VAR_OUTSRC = 0.30     # 委託費のうち件数に比例する部分（検体検査の外注など）
VC = P2["material"] + P2["outsrc"] * VAR_OUTSRC
FC = P2["cost"] - VC
CM = P2["rev"] - VC
CMR = CM / P2["rev"]
BEP = FC / CMR
MOS = (P2["rev"] - BEP) / P2["rev"] * 100
DOL = CM / P2["op"]
FC_SHARE = FC / P2["cost"] * 100
TARGET_OP = 500.0
TARGET_REV = (FC + TARGET_OP) / CMR
# 収益が1%減ったときの医業利益
DROP1 = P2["op"] - CM * 0.01

# ---------------------------------------------------------------- 第9章 診療科別損益と配賦
DEPTS = ["外科", "内科", "小児科"]
D_REV = [2400.0, 2000.0, 600.0]
D_VC = [900.0, 500.0, 100.0]
D_DFC = [700.0, 800.0, 420.0]       # 直接固定費（専従の医師・スタッフ、専用機器）
D_CM = [r - v - f for r, v, f in zip(D_REV, D_VC, D_DFC)]    # 貢献利益（部門の直接の利益）
COMMON = 1300.0
BASES = [
    ("医業収益", D_REV),
    ("延べ患者数", [60000, 90000, 30000]),
    ("延床面積", [4000, 5000, 3000]),
]
ALLOC = []
for _n, _w in BASES:
    _s = sum(_w)
    _a = [COMMON * x / _s for x in _w]
    ALLOC.append((_n, _a, [c - a for c, a in zip(D_CM, _a)]))
TOTAL3 = sum(D_CM) - COMMON
AVOID = 30.0                        # 小児科をやめると減らせる共通費（病棟の一部の夜勤体制など）
TOTAL_CLOSE = sum(D_CM[:2]) - (COMMON - AVOID)

# 手術室の時間主導型 ABC（TDABC）
OR_COST = 1500.0       # 手術室の年間費用（人件費・設備・保守など）
OR_ROOMS, OR_DAYS, OR_MIN = 10, 245, 480
OR_PRACT = 0.85        # 実際に使える割合（清掃・準備・保守）
OR_CAP = OR_ROOMS * OR_DAYS * OR_MIN * OR_PRACT
OR_RATE = OR_COST * 1e6 / OR_CAP       # 円／分
OR_CASES = [
    # 手術, 1件の収益(百万円), 入室〜退室の分
    ("ロボット支援前立腺全摘", 1.60, 240),
    ("腹腔鏡下胆嚢摘出", 0.60, 150),
    ("白内障手術", 0.20, 25),
]
OR_REV_TOTAL = 6000.0     # 手術関連の年間収益（収益比で配る場合の分母、架空）
OR_ALLOC = [(n, rev, m, OR_COST * rev / OR_REV_TOTAL * 1e6, m * OR_RATE) for n, rev, m in OR_CASES]

# ---------------------------------------------------------------- 第10章 関連原価
# (1) 検体検査の外注か内製か
LAB_N = 200000
LAB_OUT = 600          # 外注の単価（円）
LAB_REAGENT = 250      # 内製の試薬（円/件）
LAB_LEASE = 25.0       # 機器のリース（百万円/年）
LAB_STAFF = 16.0       # 内製に必要な技師2名（百万円/年）
LAB_COMMON = 30.0      # 内製の検査室に配賦される共通費（増減しない）
LAB_OUT_TOTAL = LAB_N * LAB_OUT / 1e6
LAB_IN_REL = LAB_N * LAB_REAGENT / 1e6 + LAB_LEASE + LAB_STAFF
LAB_IN_FULL = LAB_IN_REL + LAB_COMMON
LAB_SPACE = 35.0       # 検査室を空ければ外来化学療法室を広げられ、得られる限界利益（機会原価）

# (2) 手術室の時間が足りないとき：1分あたりの限界利益
OR_MIX = [
    # 手術, 1件の収益, 1件の変動費, 分
    ("ロボット支援前立腺全摘", 1.60, 0.75, 240),
    ("腹腔鏡下胆嚢摘出", 0.60, 0.18, 150),
    ("人工膝関節置換", 1.30, 0.62, 150),
]
OR_MIX = [(n, r, v, m, r - v, (r - v) * 1e6 / m) for n, r, v, m in OR_MIX]

# ---------------------------------------------------------------- 第11章 予算差異（入院収益、Y2）
BUD_OCC = 0.87
BUD_UNIT = 72000.0
BUD_DAYS = BEDS * BUD_OCC * 365
BUD_INPT = BUD_DAYS * BUD_UNIT / 1e6
VOL_VAR = (P2["days"] - BUD_DAYS) * BUD_UNIT / 1e6
PRICE_VAR = (P2["unit"] - BUD_UNIT) * P2["days"] / 1e6
assert abs(BUD_INPT + VOL_VAR + PRICE_VAR - P2["inpt"]) < 1e-6


def f0(x):
    v = round(x)
    return ("−" if v < 0 else "") + format(abs(v), ",")


def f1(x):
    return ("−" if x < -0.05 else "") + "%.1f" % abs(x)


def sg(x, fmt=f0):
    """符号つき（＋／−）"""
    return ("＋" if x >= 0 else "−") + fmt(abs(x))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for y, p in PL.items():
        print(y, {k: round(v, 1) for k, v in p.items()})
    for y, b in (("B1", B1), ("B2", B2)):
        print(y, {k: round(v, 1) for k, v in b.items()})
    print("CF", {k: round(v, 1) for k, v in CF.items()}, "OP", CF_OP, "INV", CF_INV, "FIN", CF_FIN, "NET", CF_NET, "FCF", FCF)
    for k in R1:
        print("%-10s %8.2f %8.2f" % (k, R1[k], R2[k]))
    print("DP", [(n, round(v, 2)) for n, v in DP_STEPS])
    print("PEERS", [(n, round(r, 2)) for n, m, t, l, r in PEERS])
    print("VC %.0f FC %.0f CMR %.3f BEP %.0f MOS %.2f DOL %.1f FCshare %.1f target %.0f drop1 %.1f" % (VC, FC, CMR, BEP, MOS, DOL, FC_SHARE, TARGET_REV, DROP1))
    print("D_CM", D_CM, "TOTAL3", TOTAL3, "CLOSE", TOTAL_CLOSE)
    for n, a, pr in ALLOC:
        print(n, [round(x) for x in a], [round(x) for x in pr])
    print("OR rate %.0f yen/min cap %.0f" % (OR_RATE, OR_CAP))
    for n, rev, m, a1, a2 in OR_ALLOC:
        print(n, round(a1 / 1e4) / 100, round(a2 / 1e4) / 100)
    print("LAB out %.1f inrel %.1f infull %.1f" % (LAB_OUT_TOTAL, LAB_IN_REL, LAB_IN_FULL))
    for x in OR_MIX:
        print(x[0], round(x[4], 2), round(x[5]))
    print("BUD", round(BUD_INPT, 1), "VOL", round(VOL_VAR, 1), "PRICE", round(PRICE_VAR, 1), "units", round(P1["unit"]), round(P2["unit"]))
