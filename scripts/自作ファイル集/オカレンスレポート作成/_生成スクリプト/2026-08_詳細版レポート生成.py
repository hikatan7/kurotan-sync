# -*- coding: utf-8 -*-
"""手術室オカレンス・マンスリーレポート 2026年8月度 詳細版"""
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
OUT = os.path.join(BASE, "手術室オカレンス・マンスリーレポート_2026年8月度配布用.docx")

months = ["2025/4","2025/5","2025/6","2025/7","2025/8","2025/9","2025/10","2025/11","2025/12",
          "2026/1","2026/2","2026/3","2026/4","2026/5","2026/6","2026/7","2026/8"]
anes = [62,85,101,104,72,61,71,62,51,80,68,71,78,52,96,69,84]
ce   = [46,40,39,37,36,40,45,36,38,41,31,33,30,24,23,38,36]
ns   = [None,None,44,43,39,33,19,31,26,21,23,19,21,8,11,21,23]
tot  = [(a or 0)+(c or 0)+(n or 0) for a,c,n in zip(anes,ce,ns)]

# ---------------- グラフ ----------------
def trend_chart(path):
    fig, ax = plt.subplots(figsize=(9.2, 3.6), dpi=200)
    x = range(len(months))
    ax.plot(x, anes, marker="o", lw=2, color="#1f4e79", label="麻酔科")
    ax.plot(x, ce, marker="s", lw=2, color="#c00000", label="CE")
    ax.plot(x, [v if v is not None else float("nan") for v in ns],
            marker="^", lw=2, color="#2e7d32", label="NS")
    ax.plot(x, tot, lw=1.4, ls="--", color="#7f7f7f", label="合計")
    ax.set_xticks(list(x)); ax.set_xticklabels(months, rotation=45, fontsize=8)
    ax.set_ylabel("報告件数", fontsize=9)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(axis="y", ls=":", color="#cccccc")
    ax.legend(fontsize=8, ncol=4, loc="upper center", frameon=False)
    ax.set_ylim(0, max(tot)+40)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(path); plt.close(fig)

# 発生率の推移（100手術あたり）
def rate_chart(path):
    rm = ["2026/4","2026/5","2026/6","2026/7","2026/8"]
    ops = [531,448,545,617,524]
    occ = [129,84,130,128,143]
    rate = [o/s*100 for o,s in zip(occ,ops)]
    fig, ax = plt.subplots(figsize=(9.2, 2.6), dpi=200)
    ax.bar(rm, ops, color="#dce6f1", label="手術件数")
    ax.set_ylabel("手術件数", fontsize=9); ax.tick_params(labelsize=8)
    ax.set_ylim(0, max(ops)+150)
    for i,v in enumerate(ops):
        ax.text(i, v-30, str(v), ha="center", va="top", fontsize=8, color="#404040")
    ax2 = ax.twinx()
    ax2.plot(rm, rate, marker="o", color="#c00000", lw=2, label="100手術あたり報告件数")
    ax2.set_ylabel("100手術あたり報告件数", fontsize=9); ax2.tick_params(labelsize=8)
    ax2.set_ylim(0, max(rate)+10)
    for i,v in enumerate(rate):
        ax2.text(i, v+1.6, f"{v:.1f}", ha="center", fontsize=8.5, color="#c00000")
    for s in ("top",): ax.spines[s].set_visible(False); ax2.spines[s].set_visible(False)
    h1_, l1_ = ax.get_legend_handles_labels(); h2_, l2_ = ax2.get_legend_handles_labels()
    ax.legend(h1_+h2_, l1_+l2_, fontsize=8, ncol=2, loc="upper left", frameon=False)
    fig.tight_layout(); fig.savefig(path); plt.close(fig)

pareto = [("機器トラブル",55),("確認不足・準備不足",41),("その他（皮膚障害・気道・職業感染等）",15),
          ("体制・運用",14),("薬剤関連",12),("コミュニケーション",7)]

def pareto_chart(path):
    total = sum(v for _,v in pareto)
    labels = [k for k,_ in pareto]; vals = [v for _,v in pareto]
    cum = []; s = 0
    for v in vals:
        s += v; cum.append(s/total*100)
    fig, ax = plt.subplots(figsize=(9.2, 3.4), dpi=200)
    ax.bar(labels, vals, color="#4472c4")
    ax.set_ylabel("件数", fontsize=9); ax.tick_params(labelsize=8)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=12, fontsize=8)
    for i,v in enumerate(vals):
        ax.text(i, v+0.8, str(v), ha="center", fontsize=8)
    ax2 = ax.twinx()
    ax2.plot(labels, cum, marker="o", color="#c00000", lw=1.6)
    ax2.set_ylim(0,112); ax2.set_ylabel("累積％", fontsize=9); ax2.tick_params(labelsize=8)
    for i,v in enumerate(cum):
        ax2.text(i, v+4, f"{v:.1f}%", ha="center", fontsize=7.5, color="#c00000",
                 bbox=dict(fc="white", ec="none", pad=0.8, alpha=0.85))
    for s_ in ("top",): ax.spines[s_].set_visible(False); ax2.spines[s_].set_visible(False)
    fig.tight_layout(); fig.savefig(path); plt.close(fig)

trend_png = os.path.join(SCR, "aug_trend.png")
rate_png = os.path.join(SCR, "aug_rate.png")
pareto_png = os.path.join(SCR, "aug_pareto.png")
trend_chart(trend_png); rate_chart(rate_png); pareto_chart(pareto_png)

# ---------------- Word ----------------
doc = docx.Document(SRC)
body = doc.element.body
for child in list(body):
    if not child.tag.endswith("}sectPr"):
        body.remove(child)

def setfont(run, size=10.5, bold=False, color=None, name="Yu Gothic"):
    run.font.size = Pt(size); run.bold = bold; run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    if color: run.font.color.rgb = RGBColor.from_string(color)

def para(text="", size=10.5, bold=False, color=None, space_after=4, align=None, style=None):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    if align: p.alignment = align
    if text:
        setfont(p.add_run(text), size, bold, color)
    return p

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(4)
    setfont(p.add_run(text), 12.5, True, "1F4E79")
    pPr = p._element.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
    bt.set(qn("w:val"), "single"); bt.set(qn("w:sz"), "8")
    bt.set(qn("w:space"), "1"); bt.set(qn("w:color"), "1F4E79")
    pbdr.append(bt); pPr.append(pbdr)
    return p

def bullet(text, size=10.5, bold=False):
    p = doc.add_paragraph(style="List Paragraph")
    p.paragraph_format.space_after = Pt(2); p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.left_indent = Cm(0.6)
    setfont(p.add_run("・" + text), size, bold)
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

def table(rows, header=True, size=9.5, widths=None, headfill="DDEBF7"):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = doc.styles["Normal Table"]
    borders(t)
    for r in t.rows:
        r._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j); c.text = ""
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(1); p.paragraph_format.space_before = Pt(1)
            setfont(p.add_run(str(val)), size, bold=(header and i == 0))
            if header and i == 0: shade(c, headfill)
    if widths:
        for j, w in enumerate(widths):
            for row in t.rows:
                row.cells[j].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t

def pict(path, cm=17.0):
    doc.add_picture(path, width=Cm(cm))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

# --- タイトル ---
para("📘 手術室オカレンス・マンスリーレポート（2026年8月度）", 16, True, "1F4E79", space_after=2)
para("集計対象：麻酔科オカレンスレポート（8月分）／CEオカレンスレポート（2026年8月分）／NSオカレンスレポート（2026年8月分）　　作成日：2026年9月7日",
     9, color="595959", space_after=8)

# --- 1. 概況 ---
h1("1. 概況（総括）")
table([
    ["総オカレンス件数", "143 件（前月 128 件）", "内訳", "麻酔科: 84　CE: 36　NS: 23"],
    ["全手術件数", "524 件（麻酔科管理 332 件）", "報告率", "27.3 ％（前月比 ＋6.6pt）"],
    ["100手術あたり報告件数", "27.3 件（前月 20.7 件）", "重大度(Lv3a以上)", "― 件（未評価）"],
], header=False, widths=[4.2,5.6,3.0,5.4])
para("※麻酔科は「総計320件－オカレンスなし236件（73.8％）」から実報告84件として計上。手術件数は医事課提供値。",
     8.5, color="595959", space_after=6)

bullet("手術件数が617→524件（−93件、−15.1％）と減少するなかで、報告は128→143件（＋15件）と増加した。100手術あたり27.3件は2026年度で最も多く報告が集まった水準である。オカレンスレポートはアクシデント報告と異なり、件数の増加は現場のヒアリング文化・報告文化が機能していることを示すものとして肯定的に評価する。", size=10, bold=True)
bullet("増加の中心は麻酔科（69→84件、率17.8→25.3件/100件）。「34.手術準備不足」が27→35件となり、欠品が確実に拾い上げられている。内容はBISモニター6件・ボールペン5件・ハサミ5件・挿管チューブ4件と7月と同じ品目の反復であり、報告が集まっている今が定数化の効果を出す好機である。", size=10)
bullet("CEは38→36件と横ばいだが、うち麻酔器関連が12件（33.3％）を占める。特にドレーゲルAtlanのフロー計測不良・リークテスト不合格が8/5・8/13・8/18・8/19・8/24・8/25・8/27と反復し、複数事例で「回路内の水滴」が共通要因として指摘されている。単発の故障ではなく系統的な課題として扱う必要がある。", size=10)
bullet("NSは21→23件と2か月連続で2025年度水準を維持し、報告文化の再定着が続いている。そのうえで個別の事象としては、左右確認後に反対側の目を消毒（患者の指摘で発覚）、5本抜歯の予定が4本で終了（帰室時に患者の指摘で発覚）の2件が、院内のバリアではなく患者本人によって発見されており、重点的な対応を要する。", size=10, bold=True)
bullet("加えて、麻薬の管理不備2件（時間外に金庫へ返却せず一晩保管／1人分不足に気づきながら未確認のまま帰宅）と、針刺し3件（研修医が2週連続、カテ室片付け時）が発生。前者は法令順守、後者は職業感染対策として、件数の多寡と切り離して対応が必要。", size=10)

# --- 2. 月別推移 ---
h1("2. 月別推移")
para("【手術件数と報告件数】", 10.5, True, space_after=2)
table([
    ["月","手術件数","オカレンス件数","100手術あたり報告件数"],
    ["2026/4","531（麻酔科管理 371）","129（概数）","24.3"],
    ["2026/5","448（麻酔科管理 297）","84（概数）","18.8"],
    ["2026/6","545（麻酔科管理 397）","130","23.9"],
    ["2026/7","617（麻酔科管理 388）","128","20.7"],
    ["2026/8","524（麻酔科管理 332）","143","27.3"],
], widths=[2.6,5.4,4.2,6.0])
para("【職種別報告率】麻酔科 25.3％（84件÷麻酔科管理332件、前月17.8％）／CE 6.9％（36件÷524件、前月6.2％）／NS 4.4％（23件÷524件、前月3.4％）。3職種すべてで前月より上昇。",
     9, color="595959", space_after=6)
pict(rate_png)

para("【職種別オカレンスレポート報告件数の推移（2025年4月〜2026年8月）】", 10.5, True, space_after=2)
rows = [["月","麻酔科","CE","NS","合計","","月","麻酔科","CE","NS","合計"]]
half = 9
for i in range(half):
    def row(k):
        if k >= len(months): return ["","","","",""]
        n = ns[k]
        return [months[k], anes[k], ce[k], (n if n is not None else "―"), tot[k]]
    rows.append(row(i) + [""] + row(i + half))
table(rows, size=9, widths=[1.7,1.5,1.2,1.2,1.4,0.4,1.7,1.5,1.2,1.2,1.4])
pict(trend_png)

para("● コメント（推移の解釈）", 10.5, True, space_after=2)
bullet("麻酔科：84件は2026年に入って1月（80件）・6月（96件）に次ぐ高水準。手術件数が減った月に報告が増えており、稼働量に左右されずに報告が上がる習慣が定着してきたと読める。内訳は準備不足35件（実報告84件の41.7％）が中心。")
bullet("CE：36件で3か月連続30件超。7月に指摘した「接続・電源の外れ」は8→6件へ減ったが、代わりに麻酔器本体（フロー計測・リークテスト）と日本光電モニタ（6件）に集中した。")
bullet("NS：23件と微増。2025年度水準（月20件台）を2か月連続で維持しており、報告文化の再定着が続いている。報告の中身をみると確認不足6件のうち2件が患者に影響した事象であり、件数とは切り離して重点対応する。")
bullet("3職種合算では143件と2026年1月（142件）を上回り、直近14か月で最多。手術件数あたりでも27.3件/100件と、2026年度で最も多く報告が集まった月となった。現場が事象を拾い上げ、共有できている状態として評価する。", bold=True)

# --- 3. クロス集計 ---
h1("3. 職種別 × 分類別件数（クロス集計）")
table([
    ["職種","確認不足・準備不足","機器","薬剤","コミュニケーション","体制・運用","その他","計"],
    ["麻酔科","35","18","10","2","9","11","85"],
    ["CE","0","36","0","0","0","0","36"],
    ["NS","6","1","2","5","5","4","23"],
    ["合計","41","55","12","7","14","15","144"],
], size=9, widths=[2.0,3.0,1.6,1.5,3.0,2.2,1.6,1.4])
para("※麻酔科の分類対応：34.手術準備不足→確認不足・準備不足／28.ME機器・ディスポ不良→機器／22.薬剤・輸液・ライン→薬剤／3.入退室6件＋19.手術時間の延長3件→体制・運用／43.その他のうち他科コンサル漏れ等2件→コミュニケーション／36.皮膚障害3件＋43.その他8件→その他。麻酔科の分類別合計は85件で実報告84件を1件上回るが、これは原資料の分類集計値をそのまま用いたためで、1件は複数分類にまたがると考えられる（総オカレンス件数は実報告ベースの143件を用いている）。CEは全件を機器主管の報告として機器に計上（内訳は下表）。",
     8.5, color="595959", space_after=6)

para("● CE報告36件の内訳（性質別）", 10.5, True, space_after=2)
table([
    ["区分","件数","主な内容"],
    ["機器故障・不良（交換／修理・メーカー対応）","19","Apollo麻酔器のリークテスト不合格（Fabiusと交換・メーカー依頼）、AtlanのTV in/out不一致とフローバランス異常、NIM Stim2無反応、SpO2中継ケーブル断線、内視鏡録画エラー、アイソレーションモニタ絶縁警報（原因特定できず）"],
    ["設定・操作条件","8","エリートトロリーの輝度設定、麻酔器GSプレミアムのAPL設定、内視鏡のSDI選択・3D設定、気道内圧アラームの設定値、ツリウムレーザーの温度上昇（室温）"],
    ["接続・電源の外れ／抜け","6","CO2マルチガスユニットの電源未投入＋背部ケーブル抜けかけ、麻酔器の呼気センサ部品外れ、NIMのケーブル挿し場所間違い、電カルモニタとPCの電源ケーブル抜け、BIS接続ケーブル外れ"],
    ["保守（水滴・消耗部品）","2","症例入れ替え時に麻酔器回路・フィルタの水滴を発見し部品全交換、Atlan始業点検で水滴付着顕著によりアブソーバ・フィルタ交換"],
    ["準備・充電","1","新生児室の搬送用モニタがバッテリー未充電で電源投入できず（オペ室の搬送用モニタで代替）"],
], size=9, widths=[4.6,1.3,11.5])
para("※機器別では麻酔器12件（33.3％）・日本光電モニタ6件・PC/電子カルテ4件・NIM3件。麻酔器12件のうち8件がAtlanで、水滴（ソーダライム／呼気センサ周囲）を原因とする記載が複数ある。",
     8.5, color="595959", space_after=4)

# --- 4. 時間帯・診療科 ---
h1("4. 時間帯別・診療科別（CE報告36件・NS報告23件）")
table([
    ["時間帯（CE）","件数","","診療科（CE）","件数","診療科（NS）","件数"],
    ["午前（〜12時）","14","","麻酔科","15","看護部（部署報告）","4"],
    ["午後（12〜17時）","21","","看護部","7","循環器内科／整形外科","各3"],
    ["夕方（17時〜）","1","","耳鼻科／脳外","各3","消化器外科／眼科／口腔外科／心臓血管外科","各2"],
    ["","","","婦人科／CE／泌尿器科","各2","中材／形成外科／腎臓内科／病棟／記載なし","各1"],
    ["","","","外科／小児科","各1","",""],
], size=9, widths=[3.4,1.3,0.4,4.6,1.3,4.6,1.3])
bullet("CEは7月と逆に午後帯（21件・58.3％）が多い。12〜15時台の症例入れ替え時に麻酔器の点検・交換対応が集中したためで、麻酔器12件のうち8件が12時以降に発生している。")
bullet("診療科別では麻酔科15件（41.7％）が突出。麻酔器・生体情報モニタという主要機器の不具合が集中していることを示す。")

# --- 5. 傾向分析 ---
h1("5. 傾向分析（職種 × 場面 × 要因）")
para("● 多発場面", 10.5, True, space_after=2)
para("今月は場面が二極化した。①【術前準備〜麻酔導入前】…麻酔科の準備不足35件、CEの午前帯14件。②【症例入れ替え〜術中】…CEの午後21件（麻酔器の交換・点検8件）、術中の機器不良、術式の完遂確認漏れ。特に②では、患者が入室・麻酔中の状態で麻酔器を交換した事例（8/3 Apollo→Fabius、8/19 Atlan→Fabius）が2件あり、代替機の確保が実際に手術継続を支えている。",
     10, space_after=4)

para("● エラー誘発要因（SHELLモデル＋体制・環境）", 10.5, True, space_after=2)
bullet("S（ソフト：手順）：サインイン後・消毒前の左右確認が機能せず（眼科）、予定術式の完遂確認がサインアウトに含まれていない（口腔外科：5本→4本）。時間外の麻薬返却手順も守られていない。")
bullet("H（ハード：機器）：機器起因55件（全体の38.2％）。Atlan麻酔器の水滴に起因するフロー計測不良が反復し、朝の点検を通過した後に発生する事例（8/13 呼気センサ部品外れ）もあり、始業点検のみでは捕捉できない。")
bullet("E（環境）：低流量麻酔での結露、9roomのアイソレーション絶縁警報（多数のタップ使用・原因特定できず）、ツリウムレーザーの温度上昇（室温）。加えて8/3には10roomで再びLANケーブル／無停電装置に起因する通信障害が発生し、7/27に続き2か月連続となった。設備・環境側の要因が今月は目立つ。")
bullet("L-L／L-O（人と人・組織）：術式変更やCT追加の情報が手術室に届かない（8/20 心外）、ME機器デモの連絡がない（8/25 消化器外科）、PM植込み患者の局所麻酔でCEへの連絡がない（8/25 形成外科）、借り物器械が当日朝に突然届く（8/24）。いずれも「決まっているはずの事前連絡」が実行されていない。")
bullet("L（当事者）：確認行為の省略（消毒側、抜歯本数、インプラントのサイズ、ガーゼカウント、採血ラベル）。加えて針刺し3件（うち研修医2週連続）は、手技習熟と鋭利物の受け渡し・片付け手順の両面の課題。")

# --- 6. Pareto ---
h1("6. Pareto分析（3職種合算・延べ144件）")
cum = 0; prows = [["項目","件数","構成比","累積％"]]
for k, v in pareto:
    cum += v
    prows.append([k, str(v), f"{v/144*100:.1f}％", f"{cum/144*100:.1f}％"])
table(prows, size=9, widths=[7.4,1.8,2.4,2.4])
pict(pareto_png)
para("→ 上位2項目（機器55＋確認不足・準備不足41）で全体の66.7％。7月（64.8％）とほぼ同じ構造で、順位も同じ。ただし機器の中身は「接続の抜け」から「麻酔器本体の計測系」へ、確認不足の中身は「欠品」に加えて「患者に到達する確認漏れ」へと質的に変化している。",
     10, space_after=4)

# --- 7. 注目事象 ---
h1("7. 注目事象（安全上の重点）")
table([
    ["発生日","部署","事象","評価・必要な対応"],
    ["8/7","眼科（NS）","サインインで左右を確認したが、手術する側と反対の目を消毒した。患者に言われて気付いた","左右間違いの一歩手前。院内のバリアではなく患者が発見している点が重大。消毒直前の左右読み上げを必須化"],
    ["8/19","口腔外科（NS）","5本抜歯するところ4本抜歯で手術終了。帰室時に患者に聞かれ発覚","予定術式の未完遂。サインアウトに「本数・個数の読み上げ」を追加"],
    ["8/3・8/4","看護部（NS）","時間外に使用後の麻薬を金庫へ返却せず机の引き出しに入れたまま帰宅し、一晩施錠されない場所に保管／麻薬が1人分不足しているのに気付きながら担当者に確認せず帰宅（夜勤リーダー）","麻薬管理の法令順守事項。時間外の返却手順と、数量不一致時の当日中の報告ルールを明文化・再教育"],
    ["8/31","心臓血管外科・カテ室（NS）","研修医が2週続けて縫合針で針刺し事故／カテ室で片付け時に針刺し事故","職業感染。研修医への縫合針取扱い教育と、ハンズフリーパス・鋭利物廃棄の手順徹底"],
    ["8/25","整形外科（NS）","インプラントの出し間違い（骨頭サイズ28に対し22のネックで確認）、業者立ち会いなし","サイズ確認の二重化と、業者立ち会いが必要な症例の基準明確化"],
    ["8/25","整形外科（NS）","化膿性関節炎の手術で「置いておいて」と指示された組織を確認せず不潔に下ろし、培養に提出できなくなった","検体の取り扱い。指示の復唱と検体確保の優先確認"],
    ["8月","麻酔科","声門上器具の抜去時に声門閉鎖で換気不能／抜管後の循環虚脱／低体温で抜管できず","覚醒・抜管期の有害事象が複数。抜管基準と人員配置の再確認"],
    ["8月","麻酔科","繋いでいないラインから抗菌薬を投与し床に半分滴下／デキサート重複投与／アレルギー対象の抗菌薬の持ち込み","薬剤投与の3事象。ライン接続確認と投与前のアレルギー・重複チェック"],
    ["8月","麻酔科","輸血の同意書なし／緊急手術で同意書なし","同意取得の運用。緊急時の代替手順を明文化"],
    ["8/5〜8/27","CE・麻酔科","ドレーゲルAtlanのフロー計測不良・リークテスト不合格が反復（8/5, 8/13, 8/18, 8/19, 8/24, 8/25, 8/27）。複数事例で回路内・ソーダライム・呼気センサ周囲の水滴が共通要因として記載","単発故障ではなく系統的課題。低流量麻酔時の結露対策と点検周期の見直しをメーカーと協議"],
], size=8.5, widths=[1.6,2.6,7.4,5.4])

# --- 8. Good Job ---
h1("8. Good Job / Good Catch 事例")
bullet("【始業点検】8/3 Apollo麻酔器の始業点検でリークテスト不合格を検出。回路交換でも通過しなかったため、患者入室・麻酔中であったが2BのFabiusと交換して手術を継続し、本体はメーカーメンテナンスへ（CE）。")
bullet("【始業点検】8/13 麻酔器のリークテスト不通過から呼気センサ部品の外れを発見し、正しい位置に修正してテスト通過（CE）。朝の点検リストは通過していたことから、点検後に外れた可能性まで記録されている点が良い。")
bullet("【症例間点検】8/14 症例入れ替え時に麻酔器回路内・呼気吸気フィルターの水滴を発見。低流量麻酔の影響を考慮して回路・フィルタ・アブソーバを全交換し、フル始業点検を実施（CE）。")
bullet("【症例間点検】8/25 Atlanの始業点検で水滴付着が顕著と判断し、アブソーバ・フィルタを交換のうえ点検実施（CE）。8/19の事象を踏まえた予防的交換。")
bullet("【術中の代替確保】8/19 Atlanのフローバランス異常に対し、旧HCU機在庫のFabiusを持ち込んで麻酔器を切り替え、手術を継続（CE）。")
bullet("【多職種連携】8/25 ペースメーカー植込み中の患者の局所麻酔手術でCEへの連絡がなかったが、気付いた外回り看護師がCEに相談。電気メスは不使用だがICDが作動する可能性のある機種と判明し、術中設定を変更して実施（NS・形成外科）。")
bullet("【再発防止の即実施】8/14 NIMの通電不良がケーブルの挿し場所間違いと判明し、その場でテプラを貼付して再発防止（CE・耳鼻科）。")
bullet("【患者影響の回避】8/1 TRバンドの止血開始時間を誤って申し送ったが、すぐに気付いて正しい時間で対応（NS・循環器内科）。")

# --- 9. PDCA ---
h1("9. 安全対策のPDCA（ネクストアクション）")
table([
    ["#","重点課題","具体策","主担当","期限"],
    ["1","手術部位（左右）の確認","サインインとは別に、消毒直前に術者・看護師で左右を声に出して読み合わせる手順を追加。眼科は点眼・消毒トレイの左右分離も検討","眼科・手術室NS","9月中"],
    ["2","予定術式の完遂確認","サインアウトに「予定と実施の突合（本数・個数・部位）」を追加し、読み上げ担当を固定","口腔外科・手術室NS","9月中"],
    ["3","麻薬管理（法令順守）","時間外の返却手順を明文化し、返却時の相互確認を必須化。数量不一致は当日中に責任者へ報告するルールを周知徹底","手術室NS・薬剤部","9月中（最優先）"],
    ["4","針刺し防止","研修医への縫合針取扱い教育を実施。ニードルカウンター／ハンズフリーパスの運用と、片付け時の鋭利物処理手順を再周知","医療安全・心臓血管外科・NS","9月中"],
    ["5","麻酔器（Atlan）の水滴対策","低流量麻酔時の結露を前提に、症例間の水滴確認を点検項目へ追加。アブソーバ・フィルタの交換基準を明文化し、メーカーと点検周期を協議。予備機（Fabius）の配置を維持","CE・麻酔科","9月中"],
    ["6","麻酔準備の欠品（35件）","7月からの継続課題。BISモニター・ボールペン・ハサミ・挿管チューブ・人工鼻など反復品目を部屋別定数化し、朝の残数確認を役割として固定。9月末に件数で効果判定","手術室NS・麻酔科","継続（9月末評価）"],
    ["7","事前連絡ルールの実効化","術式変更・CT追加・借り物器械・デモ機器・PM/ICD症例について、手術室への連絡先と期限（原則前日まで）を1枚に整理して各科へ配布","手術室NS・各診療科","9月中"],
    ["8","薬剤投与の安全","ライン接続の確認と、アレルギー・重複投与のチェックを導入前タイムアウトに組込み","麻酔科","9月中"],
    ["9","覚醒・抜管期の管理","抜管基準の再確認と、抜管時の人員確保（声門上器具抜去時の換気不能・抜管後循環虚脱を受けて）","麻酔科","継続"],
    ["10","設備・環境（LAN・電源）","10roomのLAN／無停電装置に起因する通信障害が7/27・8/3と2か月連続で発生。UPSの点検周期と無線切替の運用手順を明文化する。9roomのアイソレーション絶縁警報は朝の点検時に重点確認し、タップ使用の制限と黒コンセント使用を周知","CE・情報係・施設","9月中"],
], size=8.5, widths=[0.8,3.4,7.6,3.4,2.0])

# --- 付記 ---
h1("【付記】集計・指標の定義と限界")
bullet("麻酔科の件数は「総計320件－99.オカレンスなし236件」＝84件を実報告件数とした。分類別の％表記は原資料に合わせ総計320件を分母としている（例：手術準備不足35件＝10.9％）。", 9)
bullet("原資料の「3.入退室に関すること」は6件と記載されているが、併記された比率2.2％は7件に相当する。本報告では記載どおり6件として集計した。", 9)
bullet("報告率および100手術あたり報告件数＝報告件数÷手術件数。8月は総手術524件・麻酔科管理332件（医事課提供値）を用いた。麻酔科の率のみ麻酔科管理件数を分母、CE・NSは総手術件数を分母としている。従来「発生率」と表記していた指標は、報告そのものを評価する趣旨から今月より「100手術あたり報告件数」と改称した（定義は従来と同じ）。", 9)
bullet("NSオカレンスの「8/3 10roomのLANケーブル使用不可」は、7/27の同種事象とは別に8月に発生した事象であることを原本で確認済み（8月の実件数23件、3職種合計143件で確定）。10roomでは2か月連続でLAN／無停電装置に起因する通信障害が生じている。", 9)
bullet("オカレンスレポートはアクシデント報告と異なり、報告件数の増加は現場のヒアリング文化・報告文化が定着していることを示すものとして肯定的に評価する。逆に件数の減少はまず過少報告を疑う。安全性の評価は件数の多寡ではなく、個々の事象の重大性と再発の有無で行う。重大度評価（Level分類）は未実施であり、次年度に向けて導入を検討する。", 9)

doc.save(OUT)
print("saved:", OUT, os.path.getsize(OUT))
