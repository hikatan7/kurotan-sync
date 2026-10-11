# -*- coding: utf-8 -*-
"""第13巻 f03 内径と気流抵抗"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import JP, INK

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
W, H, DPI = 1520, 800, 200
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False

fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0.155, 0.235, 0.815, 0.625])

D = np.array([8, 7, 6, 5, 4, 3], dtype=float)
lam = (8.0 / D) ** 4
turb = (8.0 / D) ** 5
LAB = ["8 mm\n成人気管", "7 mm", "6 mm\n浮腫 1 mm", "5 mm",
       "4 mm\n浮腫 2 mm", "3 mm"]
x = np.arange(len(D))
w = 0.36
ax.bar(x - w / 2, lam, w, color="#2e6da4", label="層流：抵抗 ∝ 1/r⁴")
ax.bar(x + w / 2, turb, w, color="#c0392b", label="乱流：抵抗 ∝ 1/r⁵")
for xi, v in zip(x - w / 2, lam):
    ax.annotate(f"{v:.1f}", (xi, v), textcoords="offset points",
                xytext=(0, 6), ha="center", fontsize=10, color="#1b4f86")
for xi, v in zip(x + w / 2, turb):
    ax.annotate(f"{v:.0f}" if v >= 10 else f"{v:.1f}", (xi, v),
                textcoords="offset points", xytext=(0, 6), ha="center",
                fontsize=10, color="#9c2b26")

ax.set_yscale("log")
ax.set_ylim(0.7, 700)
ax.set_yticks([1, 10, 100])
ax.set_yticklabels(["1 倍", "10 倍", "100 倍"])
ax.set_xticks(x)
ax.set_xticklabels(LAB, fontsize=10.5, color=INK, linespacing=1.6)
ax.set_ylabel("気流抵抗（内径 8 mm を 1 とした相対値）", fontsize=11.5,
              color=INK, labelpad=10)
ax.set_title("1 mm の浮腫が、なぜ致命的になりうるか", fontsize=13,
             color="#0A1830", weight="bold", pad=16)
ax.legend(fontsize=11, loc="upper left", frameon=True, framealpha=1.0,
          edgecolor="#c3ccd6")
ax.grid(axis="y", color="#eceff2", lw=1.0, which="both")
ax.set_axisbelow(True)
ax.tick_params(labelsize=11, colors=INK)
for s in ax.spines.values():
    s.set_color("#7c8894")

for i, ln in enumerate([
        "※ 内径が半分になれば層流でも 16 倍、乱流では 32 倍。",
        "　 小児は基準となる内径が小さいぶん、同じ 1 mm でも影響が桁違いに大きい。"]):
    fig.text(0.5, 0.075 - i * 0.042, ln, fontsize=9.8, color="#8d97a3",
             ha="center", va="center")
fig.savefig(os.path.join(OUT, "f03_resistance.png"), dpi=DPI, facecolor="white")
print("ok f03")
