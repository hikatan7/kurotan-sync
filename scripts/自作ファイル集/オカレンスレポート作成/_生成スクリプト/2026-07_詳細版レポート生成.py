# -*- coding: utf-8 -*-
"""手術室オカレンス・マンスリーレポート 2026年7月度 生成"""
import copy, os
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
OUT = os.path.join(BASE, "手術室オカレンス・マンスリーレポート_2026年7月度配布用.docx")

# ---------------- データ ----------------
months = ["2025/4","2025/5","2025/6","2025/7","2025/8","2025/9","2025/10","2025/11","2025/12",
          "2026/1","2026/2","2026/3","2026/4","2026/5","2026/6","2026/7"]
anes = [62,85,101,104,72,61,71,62,51,80,68,71,78,52,96,69]
ce   = [46,40,39,37,36,40,45,36,38,41,31,33,30,24,23,38]
ns   = [None,None,44,43,39,33,19,31,26,21,23,19,21,8,11,21]

# ---------------- グラフ ----------------
def trend_chart(path):
    fig, ax = plt.subplots(figsize=(9.2, 3.6), dpi=200)
    x = range(len(months))
    ax.plot(x, anes, marker="o", lw=2, color="#1f4e79", label="麻酔科")
    ax.plot(x, ce, marker="s", lw=2, color="#c00000", label="CE")
    ax.plot(x, [v if v is not None else float("nan") for v in ns],
            marker="^", lw=2, color="#2e7d32", label="NS")
    tot = [(a or 0)+(c or 0)+(n or 0) for a,c,n in zip(anes,ce,ns)]
    ax.plot(x, tot, lw=1.4, ls="--", color="#7f7f7f", label="合計")
    ax.set_xticks(list(x)); ax.set_xticklabels(months, rotation=45, fontsize=8)
    ax.set_ylabel("報告件数", fontsize=9)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(axis="y", ls=":", color="#cccccc")
    ax.legend(fontsize=8, ncol=4, loc="upper center", frameon=False)
    ax.set_ylim(0, max(tot)+40)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    fig.tight_layout(); fig.savefig(path); plt.close(fig)

pareto = [("機器トラブル",48),("確認不足・準備不足",35),("その他（皮膚障害・気道・物品等）",17),
          ("体制・運用",12),("薬剤関連",9),("コミュニケーション",7)]

def pareto_chart(path):
    total = sum(v for _,v in pareto)
    labels = [k for k,_ in pareto]; vals = [v for _,v in pareto]
    cum = []; s = 0
    for v in vals:
        s += v; cum.append(s/total*100)
    fig, ax = plt.subplots(figsize=(9.2, 3.4), dpi=200)
    ax.bar(labels, vals, color="#4472c4")
    ax.set_ylabel("件数", fontsize=9); ax.tick_params(labelsize=8)
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

trend_png = os.path.join(SCR, "trend_202607.png")
pareto_png = os.path.join(SCR, "pareto_202607.png")
trend_chart(trend_png); pareto_chart(pareto_png)

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
    tblPr = tbl._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top","left","bottom","right","insideH","insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"),"single"); e.set(qn("w:sz"),"4")
        e.set(qn("w:space"),"0"); e.set(qn("w:color"),color)
        b.append(e)
    tblPr.append(b)

def shade(cell, color):
    sh = OxmlElement("w:shd"); sh.set(qn("w:val"),"clear")
    sh.set(qn("w:fill"), color); cell._tc.get_or_add_tcPr().append(sh)

def table(rows, header=True, size=9.5, widths=None, headfill="DDEBF7"):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = doc.styles["Normal Table"]
    borders(t)
    for r in t.rows:  # 行の途中でページを跨がせない
        trPr = r._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.text = ""
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

# --- タイトル ---
p = para("📘 手術室オカレンス・マンスリーレポート（2026年7月度）", 16, True, "1F4E79", space_after=2)
para("集計対象：麻酔科オカレンスレポート（7月分）／CEオカレンスレポート（2026年7月分）／NSオカレンスレポート（2026年7月分）　　作成日：2026年8月5日",
     9, color="595959", space_after=8)

# --- 1. 概況 ---
h1("1. 概況（総括）")
table([
    ["総オカレンス件数", "128 件（前月 130 件）", "内訳", "麻酔科: 69　CE: 38　NS: 21"],
    ["全手術件数", "617 件（麻酔科管理 388 件）", "報告率", "20.7 ％（前月比 −3.2pt）"],
    ["100手術あたり発生率", "20.7 件（前月 23.9 件）", "重大度(Lv3a以上)", "― 件（未評価）"],
], header=False, widths=[4.2,5.6,3.0,5.4])
para("※麻酔科は「総計369件－オカレンスなし300件（81.3％）」から実報告69件として計上。7/27 10roomのLAN障害はCE・NS双方から報告されており、事象ベースの実件数は127件。",
     8.5, color="595959", space_after=6)

bullet("7月の手術件数は617件（麻酔科管理388件）で、6月545件から＋72件（＋13.2％）と直近で最も多い月となった。一方でオカレンス件数は130→128件と横ばいのため、100手術あたり発生率は23.9→20.7件へ低下している。", size=10)
bullet("総件数は130件→128件とほぼ横ばいだが、職種構成が大きく入れ替わった。麻酔科96→69件（−27）、CE 23→38件（＋15、2025年4月以降で最多）、NS 11→21件（＋10、報告水準が回復）。", size=10)
bullet("麻酔科の減少は「34.手術準備不足」43→27件（−16）が主因。6月に着手した麻酔準備チェックリスト改訂・欠品品目の定数化が一定の効果を示した可能性がある。ただし準備不足は依然として単独最多分類（麻酔科実件数の39.1％）であり、達成ではなく途上と捉える。", size=10)
bullet("CEの増加は電気メス（VIO3・BiSect）、内視鏡システム（エリートⅢ／Ⅱ）、ロボット（DaVinci）に集中。機器分類は3職種合算48件（全体の37.5％）となり、今月は最大分類が「確認不足」から「機器」へ交代した。", size=10)
bullet("患者に到達した事象として、7/27 眼科アイリーアの伝票と薬剤の相違による誤量投与（対応中）があり、今月の最重要案件。ほかに『SpO2モニター未装着のまま麻酔導入』『義歯装着のまま入室』など、バリア（タイムアウト・チェックリスト）が機能しなかった事象が複数報告された。", size=10)

# --- 2. 月別推移 ---
h1("2. 月別推移")
para("【手術件数と発生率】", 10.5, True, space_after=2)
table([
    ["月","手術件数","オカレンス件数","100手術あたり発生率"],
    ["2026/4","531（麻酔科管理 371）","129（概数）","24.3"],
    ["2026/5","448（麻酔科管理 297）","84（概数）","18.8"],
    ["2026/6","545（麻酔科管理 397）","130","23.9"],
    ["2026/7","617（麻酔科管理 388）","128","20.7"],
], widths=[2.6,5.4,4.2,6.0])
para("【職種別報告率】麻酔科 17.8％（69件÷麻酔科管理388件、前月24.2％）／CE 6.2％（38件÷617件、前月4.2％）／NS 3.4％（21件÷617件、前月2.0％）。※報告率＝報告件数÷手術件数",
     9, color="595959", space_after=6)

para("【職種別オカレンスレポート報告件数の推移（2025年4月〜2026年7月）】", 10.5, True, space_after=2)
rows = [["月","麻酔科","CE","NS","合計","","月","麻酔科","CE","NS","合計"]]
half = 8
for i in range(half):
    l = i; r = i + half
    def row(k):
        if k >= len(months): return ["","","","",""]
        n = ns[k]
        tot = anes[k] + ce[k] + (n or 0)
        return [months[k], anes[k], ce[k], (n if n is not None else "―"), tot]
    rows.append(row(l) + [""] + row(r))
table(rows, size=9, widths=[1.7,1.5,1.2,1.2,1.4,0.4,1.7,1.5,1.2,1.2,1.4])
doc.add_picture(trend_png, width=Cm(17.0))
doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

para("● コメント（推移の解釈）", 10.5, True, space_after=2)
bullet("麻酔科：月50〜100件の高水準で推移し報告文化は良好。7月は69件で6月比−27件、直近12か月平均（70.6件）並みに戻った。麻酔科管理件数あたりでは24.2→17.8件/100件と低下しており、件数・率の双方で減少している。減少幅の大半が準備不足であり、対策の効果と月変動の双方を含むと考えられる。")
bullet("CE：2026年に入り20〜30件台で推移していたが、7月は38件と急増。手術件数あたりでも4.2→6.2件/100件と上昇しており、稼働増だけでは説明できない。増加の中身は「接続・電源の外れ／抜け」8件と「設定・操作条件」11件で、故障よりも使用前後の取り扱いに起因するものが過半。機器の経年化とロボット・エネルギーデバイスの使用拡大も背景にある。")
bullet("NS：5月8件→6月11件→7月21件と回復し、2025年度水準（月20件台）に復した。手術件数が617件と最多であった月に報告が戻った点は、現場の余裕の回復とも読める。ただし内容は準備・確認段階と情報伝達に集中しており、実質的なリスクが顕在化している点に注意が必要。")

# --- 3. クロス集計 ---
h1("3. 職種別 × 分類別件数（クロス集計）")
table([
    ["職種","確認不足・準備不足","機器","薬剤","コミュニケーション","体制・運用","その他","計"],
    ["麻酔科","27","8","8","4","8","14","69"],
    ["CE","0","38","0","0","0","0","38"],
    ["NS","8","2","1","3","4","3","21"],
    ["合計","35","48","9","7","12","17","128"],
], size=9, widths=[2.0,3.0,1.6,1.5,3.0,2.2,1.6,1.4])
para("※麻酔科の分類対応：34.手術準備不足→確認不足・準備不足／28.ME機器・ディスポ不良→機器／22.薬剤・輸液・ライン→薬剤／3.入退室に関すること→体制・運用／43.その他のうちチーム間の言動・介入4件→コミュニケーション／36.皮膚障害4件・43その他3件・分類3件未満の報告7件→その他。CEは全件を機器主管の報告として機器に計上（内訳は第4章）。",
     8.5, color="595959", space_after=6)

para("● CE報告38件の内訳（性質別）", 10.5, True, space_after=2)
table([
    ["区分","件数","主な内容"],
    ["設定・操作条件","11","VIO300Dのエフェクト／パワー設定、カメラのAF・アイリスがマニュアル、SpO2波形スケール、気腹装置のモード選択で停止、ツリウムレーザーの緊急停止押込み・200V化"],
    ["機器故障・不良（交換／修理）","11","日本光電ABPユニット故障、erbe BiSect術中通電不良、DaVinciシュアフォームリロード不良・Vesselシーラ認識不良、麻酔器リーク（蛇管交換）、ノートPC起動不良"],
    ["接続・電源の外れ／抜け","8","シーリングLAN半抜け、呼気センサケーブル外れ、フローセンサーコード抜け、サブモニタ電源コード抜け、トロリー電源ケーブル抜けかけ、顕微鏡配線"],
    ["構成・準備・在庫","5","エリートⅢに12G非対応モニタを接続、前日準備の初期配置が逆、シュアフォームBlackリロード在庫3個（他院より借用）"],
    ["IT・ネットワーク","3","電子カルテの患者認証エラー（前日の退床ミス）、麻酔チャートへのモニタ情報未転記、落雷によるUPS故障で10roomの有線LAN不通"],
], size=9, widths=[4.0,1.4,12.0])

# --- 4. 時間帯・診療科 ---
h1("4. 時間帯別・診療科別（CE報告38件・NS報告21件）")
table([
    ["時間帯（CE）","件数","","診療科（CE）","件数","診療科（NS）","件数"],
    ["午前（〜12時）","22","","外科","11","心臓血管外科","4"],
    ["午後（12〜17時）","16","","麻酔科","9","整形外科","4"],
    ["夕方（17時〜）","0","","看護部","5","眼科","3"],
    ["","","","呼吸器外科／泌尿器科／耳鼻科","各3","脳神経外科／消化器外科","各3"],
    ["","","","婦人科2／整形外科1／CE1","4","口腔外科／皮膚科／外科／泌尿器科","各1"],
], size=9, widths=[3.4,1.3,0.4,4.6,1.3,4.6,1.3])
bullet("CEは午前帯が22件（57.9％）で、内訳は8〜10時台の始業点検・入室準備帯に集中。午後は12〜15時台の症例入れ替え時に再上昇する二峰性。人と機器の同時立ち上げが重なる時間帯にコールが集中している。")
bullet("診療科別では外科11件・麻酔科9件で全体の過半。外科は電気メス／内視鏡システム／気腹装置と使用機器数が多く、件数の多さは使用量に比例した面がある。")

# --- 5. 傾向分析 ---
h1("5. 傾向分析（職種 × 場面 × 要因）")
para("● 多発場面", 10.5, True, space_after=2)
para("今月も【術前準備〜麻酔導入前】が最大のリスク場面。麻酔科「手術準備不足」27件、NSの準備・確認段階8件、CEの午前帯22件が同一の時間帯に重なる。加えて今月は【術中の機器トラブル】が増加し（電気メス通電不良、DaVinciリロード不良・Vesselシーラ認識不良、ナビゲーション映像欠落）、術中の代替手段確保が新たな論点となった。",
     10, space_after=4)

para("● エラー誘発要因（SHELLモデル＋体制・環境）", 10.5, True, space_after=2)
bullet("S（ソフト：手順）：準備チェックリストの網羅性不足（欠品27件）、導入前タイムアウトでモニター装着確認がスルー、ナビ常時充電ルール・器械たき回しルールの不遵守、TAVI室内配置がマニュアルと相違。")
bullet("H（ハード：機器）：機器起因48件。接続・電源の外れ8件は使用前確認で捕捉可能な範囲。経年機器（fabius tiro、日本光電モニタ、ツリウムレーザー）の不具合が続く。")
bullet("E（環境）：落雷によるUPS故障で10roomの有線LAN不通（電子カルテ・LITERA使用不可）、Cアーム操作要員未確保で毎回20〜30分の待機、定時超過下での進行。")
bullet("L-L／L-O（人と人・組織）：病棟⇔手術室（義歯・抗菌薬・ライン漏れ・靴下紛失）、麻酔科⇔看護（ブロックの直前指示、抜管前の帰室指示）、業者⇔手術室（たき回し器械の写真・氏名提示ルール不履行）。7/17カテ室の「おかしいと言い合える関係性ができていない」という報告は、個別事象ではなく文化面の課題として扱う必要がある。")
bullet("L（当事者）：確認行為そのものの省略（伝票と薬剤の照合、検体処理の確認、刃の取り外し）。単独作業・時間切迫下で発生している。")

# --- 6. Pareto ---
h1("6. Pareto分析（3職種合算・128件）")
cum = 0; prows = [["項目","件数","構成比","累積％"]]
for k, v in pareto:
    cum += v
    prows.append([k, str(v), f"{v/128*100:.1f}％", f"{cum/128*100:.1f}％"])
table(prows, size=9, widths=[7.4,1.8,2.4,2.4])
doc.add_picture(pareto_png, width=Cm(17.0))
doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
para("→ 上位2項目（機器＋確認不足・準備不足）で全体の64.8％。前月（確認不足＋機器で63.0％）と上位2領域は同一だが順位が逆転した。対策資源は引き続きこの2領域に集中投下するのが合理的で、今月は特に機器の「使用前確認」と「術中の代替手段」に重心を移す。",
     10, space_after=4)

# --- 7. 注目事象 ---
h1("7. 注目事象（安全上の重点）")
table([
    ["発生日","部署","事象","評価・必要な対応"],
    ["7/27","眼科（NS）","眼内注射用アイリーアの伝票と薬剤が相違し、誤った量を投与（医師と確認のうえ術野に出していた）","患者到達事象。今月最重要。薬剤・伝票・投与量の照合手順の明文化と、術野に出す前の声出し確認を必須化"],
    ["7月","麻酔科","SpO2モニター未装着のまま麻酔導入を開始（導入前タイムアウトでモニター装着確認がスルーされた）","バリアの機能不全。タイムアウト項目にモニター装着の実測確認を組込む"],
    ["7月","麻酔科","病棟からの連絡で義歯装着のまま入室と判明。入室チェックリストに記載なく申し送りもなし","二重の伝達欠落。チェックリストへの義歯欄追加と病棟申し送り様式の統一"],
    ["7/16","皮膚科（NS）","メスの刃を外さずに洗浄・組立て室へ返却。委託業者がセット組立時に発見（けがなし）","鋭利器材による受傷リスク。返却前の刃の取り外し確認を再周知し、委託業者と合同確認"],
    ["7/10","口腔外科（NS）","超音波切開装置（PIEZO）の冷却チューブのコネクタ閉塞により先端が発熱し、チップが破損","熱傷リスク。使用前の冷却水流出確認を手順化"],
    ["7月","麻酔科","術後コンパートメント症候群となり減張切開","体位・阻血リスク。長時間症例の体位再評価と記録"],
    ["7/13","脳神経外科（NS）","V-Pシャントのパッサーに水滴付着（滅菌不十分）で再滅菌。患者入室後の発覚のため一度帰室","滅菌工程と入室前確認。中材との検証"],
    ["7/18","外科（NS）","日曜緊急手術の検体が室内に放置（1検体が未処理のまま）","検体紛失リスク。サインアウト時の検体数読み上げを徹底"],
    ["7/17","心臓血管外科（NS）","抜管前の患者を帰室させるよう指示があり、看護師が対応に苦慮。「おかしいと言い合える関係性ができていない」","Speak up文化の課題。症例前ブリーフィングと部門間の対話の場を設定"],
    ["7/27","看護部・消化器外科","落雷によるUPS故障で10roomの有線LAN不通。電子カルテ・LITERA使用不可となり手術出しを一時保留（無線で復旧）","BCP課題。UPSの点検周期と代替回線運用の明文化"],
], size=8.5, widths=[1.6,2.6,7.4,5.4])

# --- 8. Good Job ---
h1("8. Good Job / Good Catch 事例")
bullet("【術前・枠管理】7/10 泌尿器科が割当のない手術枠に申し込んでいたことを締切時点で発見し是正（NS報告でも「Good」評価）。当日の混乱を未然に回避。")
bullet("【始業点検】7/9 麻酔器（Fabius）の呼気センサケーブル外れを始業点検で発見。センサ交換後にCal不能となったが、再起動と自己診断でリセットし復旧させ、臨床使用前に完結（CE）。")
bullet("【症例間点検】7/16 麻酔器（Atlan）のリークテストでリークを検知。フローセンサ増し締め後も再現したため蛇管交換で解消し、患者使用前に是正（CE）。")
bullet("【器械準備】7/19 眼科でIAチップとUSチップの取り違えセットアップを、医師が準備時に発見し交換のうえ手術実施（NS）。")
bullet("【術中の代替確保】7/16 DaVinciシュアフォーム45のブラックリロードでエラーが再現したため、シグニアへ切り替えて臨床継続（CE・呼吸器外科）。")
bullet("【スケジュール復旧】7/27 金曜に月曜使用予定の器械を預かった際、手術予約がないことに気づき医師に確認。6時間の手術入力漏れが判明したが、麻酔科の調整により予定時間どおり実施（NS・脳神経外科）。")

# --- 9. PDCA ---
h1("9. 安全対策のPDCA（ネクストアクション）")
table([
    ["#","重点課題","具体策","主担当","期限"],
    ["1","眼内注射薬剤の誤投与","伝票・薬剤・投与量の3点照合を術野に出す前の声出しダブルチェックとして手順化。眼科の薬剤準備フローを図示化して掲示","眼科・手術室NS","8月中"],
    ["2","導入前タイムアウトの実効性","タイムアウト項目に「モニター装着（SpO2・心電図・血圧）の実測確認」を明記し、読み上げ担当を固定","麻酔科","8月中"],
    ["3","病棟⇔手術室の申し送り","入室チェックリストに義歯欄を追加。抗菌薬・持参薬・ライン状態の申し送り様式を統一","NS・病棟師長会","8月中"],
    ["4","麻酔準備の欠品（27件）","上位品目（挿管チューブ4・マジック4・胃管3・ハサミ3・体温プローベ3・BISモニター2・カフ圧計2・延長チューブ2・針ボックス2・黄色シリンジ2）を定数化・トレイ化し、部屋別の残数確認を朝の役割に組込む","手術室NS・麻酔科","継続（9月評価）"],
    ["5","機器の使用前確認（接続8件）","始業点検・症例間点検に「電源コード／センサケーブル／LANの固定確認」を追加。抜けやすい箇所は写真付き手順書に","CE","8月中"],
    ["6","術中の機器代替手段","電気メス・ロボットデバイス・ナビの代替機／代替手順を機種別に一覧化し各室に掲示","CE・外科・呼吸器外科","9月"],
    ["7","ロボット消耗品の在庫","シュアフォームBlackリロード等の在庫下限を設定し、下限到達で自動発注。他院借用は例外手続きとして記録","CE・材料部門","8月中"],
    ["8","鋭利器材の返却","刃を外してから洗浄依頼するルールを再周知し、委託業者との合同確認を1回実施","NS・中材・委託業者","8月中"],
    ["9","停電・落雷時のBCP","LAN用UPSの点検周期を設定し、無線への切替手順と手術出し判断のフローを明文化","CE・情報係","9月"],
    ["10","Speak up文化","症例前ブリーフィングの定着と、疑義を伝えた事例の共有（カテ室を含む）。指示変更は原則前日までに伝達","麻酔科・心臓血管外科・NS","継続"],
], size=8.5, widths=[0.8,3.4,7.6,3.4,2.0])

# --- 付記 ---
h1("【付記】集計・指標の定義と限界")
bullet("麻酔科の件数は「総計369件－99.オカレンスなし300件」＝69件を実報告件数とした。分類別の％表記は原資料に合わせ総計369件を分母としている（例：手術準備不足27件＝7.3％）。", 9)
bullet("報告率および100手術あたり発生率＝報告件数÷手術件数。7月は総手術617件・麻酔科管理388件（医事課提供値）を用いた。麻酔科の率のみ麻酔科管理件数を分母、CE・NSは総手術件数を分母としている。", 9)
bullet("職種間で同一事象が重複報告される場合がある（今月は7/27のLAN障害1件）。事象ベースの実件数は127件。", 9)
bullet("報告件数の増減は安全性の向上・悪化を直接示さない。減少は過少報告、増加は報告文化の定着を意味する場合がある。重大度評価（Level分類）は未実施であり、次年度に向けて導入を検討する。", 9)

doc.save(OUT)
print("saved:", OUT, os.path.getsize(OUT))
