# -*- coding: utf-8 -*-
"""手術室オカレンス 会議配布用サマリー（2ページ） 2026年7月度"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
import docx
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

rcParams["font.family"] = "Yu Gothic"
rcParams["axes.unicode_minus"] = False

SCR = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:\Users\junch\OneDrive\デスクトップ\自作ファイル集\オカレンスレポート作成"
SRC = os.path.join(BASE, "手術室オカレンス・マンスリーレポート_2026年6月度配布用.docx")
OUT = os.path.join(BASE, "手術室オカレンス_会議用サマリー_2026年7月度.docx")

months = ["2025/4","2025/5","2025/6","2025/7","2025/8","2025/9","2025/10","2025/11","2025/12",
          "2026/1","2026/2","2026/3","2026/4","2026/5","2026/6","2026/7"]
anes = [62,85,101,104,72,61,71,62,51,80,68,71,78,52,96,69]
ce   = [46,40,39,37,36,40,45,36,38,41,31,33,30,24,23,38]
ns   = [None,None,44,43,39,33,19,31,26,21,23,19,21,8,11,21]
tot  = [(a or 0)+(c or 0)+(n or 0) for a,c,n in zip(anes,ce,ns)]

# ---- グラフ1：職種別推移＋合計 ----
trend_png = os.path.join(SCR, "sum_trend_202607.png")
fig, ax = plt.subplots(figsize=(9.6, 2.9), dpi=220)
x = list(range(len(months)))
ax.bar(x, tot, color="#e8eef7", label="合計", width=0.62)
ax.plot(x, anes, marker="o", ms=4, lw=1.8, color="#1f4e79", label="麻酔科")
ax.plot(x, ce, marker="s", ms=4, lw=1.8, color="#c00000", label="CE")
ax.plot(x, [v if v is not None else float("nan") for v in ns], marker="^", ms=4, lw=1.8,
        color="#2e7d32", label="NS")
for i in (len(months)-1,):
    ax.annotate(f"合計{tot[i]}", (i, tot[i]), textcoords="offset points", xytext=(0,4),
                ha="center", fontsize=8.5, color="#404040")
ax.set_xticks(x); ax.set_xticklabels(months, rotation=45, fontsize=8)
ax.set_ylabel("報告件数", fontsize=9); ax.tick_params(axis="y", labelsize=8)
ax.set_ylim(0, max(tot)+35)
ax.grid(axis="y", ls=":", color="#cccccc")
ax.legend(fontsize=8.5, ncol=4, loc="upper center", frameon=False)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(trend_png); plt.close(fig)

# ---- グラフ2：分類別×職種（積み上げ横棒） ----
cat_png = os.path.join(SCR, "sum_cat_202607.png")
cats = ["機器","確認不足・準備不足","その他","体制・運用","薬剤","コミュニケーション"]
v_an = [8, 27, 14, 8, 8, 4]
v_ce = [38, 0, 0, 0, 0, 0]
v_ns = [2, 8, 3, 4, 1, 3]
fig, ax = plt.subplots(figsize=(9.6, 2.5), dpi=220)
y = list(range(len(cats)))[::-1]
ax.barh(y, v_an, color="#1f4e79", label="麻酔科", height=0.6)
ax.barh(y, v_ce, left=v_an, color="#c00000", label="CE", height=0.6)
ax.barh(y, v_ns, left=[a+c for a,c in zip(v_an,v_ce)], color="#2e7d32", label="NS", height=0.6)
for i, yy in enumerate(y):
    t = v_an[i]+v_ce[i]+v_ns[i]
    ax.text(t+1, yy, f"{t}件（{t/128*100:.1f}％）", va="center", fontsize=8.5)
ax.set_yticks(y); ax.set_yticklabels(cats, fontsize=9)
ax.set_xlim(0, 62); ax.set_xlabel("件数", fontsize=9); ax.tick_params(axis="x", labelsize=8)
ax.legend(fontsize=8.5, ncol=3, loc="lower right", frameon=False)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(cat_png); plt.close(fig)

# ---------------- Word ----------------
doc = docx.Document(SRC)
body = doc.element.body
for child in list(body):
    if not child.tag.endswith("}sectPr"):
        body.remove(child)
sec = doc.sections[0]
sec.top_margin = Cm(1.2); sec.bottom_margin = Cm(1.2)
sec.left_margin = Cm(1.3); sec.right_margin = Cm(1.3)

def setfont(run, size=10, bold=False, color=None, name="Yu Gothic"):
    run.font.size = Pt(size); run.bold = bold; run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    if color: run.font.color.rgb = RGBColor.from_string(color)

def para(text="", size=10, bold=False, color=None, space_after=3, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    if align: p.alignment = align
    if text: setfont(p.add_run(text), size, bold, color)
    return p

def h1(text, size=11.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.0
    setfont(p.add_run(text), size, True, "1F4E79")
    pPr = p._element.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
    bt.set(qn("w:val"), "single"); bt.set(qn("w:sz"), "8")
    bt.set(qn("w:space"), "1"); bt.set(qn("w:color"), "1F4E79")
    pbdr.append(bt); pPr.append(pbdr)
    return p

def bullet(text, size=9.5, bold=False, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(1.5); p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.left_indent = Cm(0.45)
    p.paragraph_format.first_line_indent = Cm(-0.45)
    p.paragraph_format.line_spacing = 1.0
    setfont(p.add_run("・" + text), size, bold, color)
    return p

def borders(tbl, color="808080"):
    b = OxmlElement("w:tblBorders")
    for edge in ("top","left","bottom","right","insideH","insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"),"single"); e.set(qn("w:sz"),"4")
        e.set(qn("w:space"),"0"); e.set(qn("w:color"),color)
        b.append(e)
    tbl._tbl.tblPr.append(b)

def shade(cell, color):
    sh = OxmlElement("w:shd"); sh.set(qn("w:val"),"clear")
    sh.set(qn("w:fill"), color); cell._tc.get_or_add_tcPr().append(sh)

def table(rows, header=True, size=9, widths=None, headfill="DDEBF7", after=2):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = doc.styles["Normal Table"]
    borders(t)
    for r in t.rows:
        r._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j); c.text = ""
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0.5); p.paragraph_format.space_before = Pt(0.5)
            p.paragraph_format.line_spacing = 1.0
            setfont(p.add_run(str(val)), size, bold=(header and i == 0))
            if header and i == 0: shade(c, headfill)
    if widths:
        for j, w in enumerate(widths):
            for row in t.rows:
                row.cells[j].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(after)
    return t

def pict(path, cm=18.4):
    doc.add_picture(path, width=Cm(cm))
    p = doc.paragraphs[-1]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)

# ===== 1ページ目 =====
para("手術室オカレンス・サマリー（2026年7月度）", 15, True, "1F4E79", space_after=1)
para("集計対象：麻酔科／CE／NS オカレンスレポート 2026年7月分　　業務委員会 配布資料　　作成日：2026年8月5日　　※詳細版レポート（全6頁）別添",
     8.5, color="595959", space_after=5)

kpi = table([
    ["総手術件数","617 件\n（麻酔科管理 388 件）","総オカレンス件数","128 件\n（前月 130 件）",
     "100手術あたり発生率","20.7 件\n（前月 23.9 件）"],
], header=False, size=10, widths=[2.4,3.4,3.0,2.8,3.4,3.2], after=2)
for j in (0, 2, 4):
    shade(kpi.cell(0, j), "DDEBF7")
    for r in kpi.cell(0, j).paragraphs:
        for run in r.runs: run.bold = True
table([
    ["職種","麻酔科","CE","NS","合計"],
    ["7月","69（前月96）","38（前月23）","21（前月11）","128（前月130）"],
    ["報告率","17.8％（÷麻酔科管理388）","6.2％（÷617）","3.4％（÷617）","20.7％（÷617）"],
], size=9, widths=[1.8,5.0,3.8,3.8,4.0], after=4)

h1("1. 月別推移（2025年4月〜2026年7月）")
pict(trend_png)

h1("2. 分類別 × 職種別（7月・計128件）")
pict(cat_png)

h1("3. 今月のポイント")
bullet("手術件数は545→617件（＋13.2％）と直近で最多。報告は128件で横ばいのため、100手術あたり発生率は23.9→20.7件へ低下。", 9.5)
bullet("麻酔科は96→69件（率24.2→17.8件/100件）。「手術準備不足」43→27件の減少が主因で、6月からの準備チェックリスト改訂・欠品品目の定数化の効果とみられる。", 9.5)
bullet("CEは23→38件と急増（率4.2→6.2件/100件）。中身は接続・電源の外れ8件、設定・操作条件11件で、故障より使用前後の取り扱いが過半。今月は「機器」が最多分類（48件・37.5％）となり、前月まで最多だった「確認不足」と順位が逆転した。", 9.5)
bullet("NSは11→21件と回復し2025年度水準に復帰。報告文化の再定着として評価できる。", 9.5)
bullet("上位2分類（機器48＋確認不足35）で全体の64.8％。対策資源はこの2領域に集中する。", 9.5, bold=True)

# ===== 2ページ目 =====
doc.add_page_break()

h1("4. Good Job / Good Catch（患者に到達する前に止められた事例）")
table([
    ["発生日","部署","内容","評価"],
    ["7/9","CE・麻酔科","麻酔器（Fabius）の呼気センサケーブル外れを始業点検で発見。センサ交換後のCal不能も再起動・自己診断で復旧させ、臨床使用前に完結","Good Catch"],
    ["7/16","CE・麻酔科","麻酔器（Atlan）のリークテストでリークを検知。フローセンサ増し締め後も再現したため蛇管交換で解消し、患者使用前に是正","Good Catch"],
    ["7/19","NS・眼科","IAチップとUSチップの取り違えセットアップを、医師が準備時に発見し交換のうえ手術実施","Good Catch"],
    ["7/10","NS・泌尿器科","割当のない手術枠への申し込みを締切時点で発見し是正。当日の混乱を未然に回避","Good Job"],
    ["7/16","CE・呼吸器外科","DaVinciシュアフォーム45のブラックリロードでエラーが再現したため、シグニアへ切り替えて臨床継続","Good Job"],
    ["7/27","NS・脳神経外科","器械を預かった際に手術予約がないことに気づき医師に確認。6時間の手術入力漏れが判明したが、麻酔科の調整で予定時間どおり実施","Good Job"],
], size=8.5, widths=[1.5,2.6,11.0,1.8])
para("→ 始業点検・症例間点検・器械準備の3場面で確実に捕捉できている。この検出力を維持することが最大の防御線。",
     9, color="1F4E79", space_after=4)

h1("5. 注目事象（安全上の重点・上位5件）")
table([
    ["発生日","部署","事象","必要な対応"],
    ["7/27","眼科","眼内注射用アイリーアの伝票と薬剤が相違し、誤った量を投与（患者到達事象・対応中）","伝票・薬剤・投与量の3点照合を術野に出す前の声出し確認として必須化"],
    ["7月","麻酔科","SpO2モニター未装着のまま麻酔導入を開始（導入前タイムアウトで装着確認がスルー）","タイムアウト項目にモニター装着の実測確認を明記し読み上げ担当を固定"],
    ["7月","麻酔科","義歯装着のまま入室（入室チェックリストに記載なく申し送りもなし）","チェックリストへの義歯欄追加と病棟申し送り様式の統一"],
    ["7/16","皮膚科","メスの刃を外さずに洗浄・組立て室へ返却。委託業者がセット組立時に発見（けがなし）","返却前の刃の取り外し確認を再周知し、委託業者と合同確認"],
    ["7/27","看護部・消化器外科","落雷によるUPS故障で10roomの有線LANが不通。電子カルテ・LITERA使用不可となり手術出しを一時保留","UPSの点検周期を設定し、無線切替と手術出し判断のフローを明文化"],
], size=8.5, widths=[1.4,2.4,7.4,5.7])

h1("6. 今月の重点対策（8〜9月）")
table([
    ["#","重点課題","具体策","主担当","期限"],
    ["1","眼内注射薬剤の誤投与","伝票・薬剤・投与量の3点照合を声出しダブルチェックとして手順化","眼科・手術室NS","8月中"],
    ["2","導入前タイムアウトの実効性","「モニター装着（SpO2・心電図・血圧）の実測確認」を項目に明記","麻酔科","8月中"],
    ["3","病棟⇔手術室の申し送り","入室チェックリストに義歯欄を追加、申し送り様式を統一","NS・病棟師長会","8月中"],
    ["4","麻酔準備の欠品（27件）","上位品目（挿管チューブ・マジック・胃管・ハサミ・体温プローベ等）を定数化・トレイ化","手術室NS・麻酔科","継続（9月評価）"],
    ["5","機器の使用前確認（接続8件）","始業点検・症例間点検に「電源コード／センサケーブル／LANの固定確認」を追加","CE","8月中"],
    ["6","術中の機器代替手段","電気メス・ロボットデバイス・ナビの代替機／代替手順を機種別に一覧化し各室に掲示","CE・外科・呼吸器外科","9月"],
], size=8.5, widths=[0.7,3.2,8.0,3.2,1.8])

para("※麻酔科の件数は「総計369件－オカレンスなし300件」＝69件。7/27のLAN障害はCE・NS双方からの報告のため、事象ベースの実件数は127件。重大度（Level分類）は未評価。詳細は別添の詳細版レポート（全6頁）参照。",
     8, color="595959", space_after=0)

doc.save(OUT)
print("saved:", OUT, os.path.getsize(OUT))
