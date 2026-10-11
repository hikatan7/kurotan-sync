# -*- coding: utf-8 -*-
"""第16巻 アナフィラキシーと局所麻酔薬中毒 図版 f11〜f19"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from figlib import Canvas, LH, NAVY, INK, JP
from fig16_a import two_col, note, banner, P

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
plt.rcParams["font.family"] = JP
import fig16_a
fig16_a.OUT = OUT


def PP(n):
    return os.path.join(OUT, n)


def rows(cv, W, TOP, data, name_sz=11.0, body_sz=10.0, L=52, gap=14,
         nlines=1, lh=1.7):
    """左に色つき見出し、右に本文の行。data=[(見出し,色,[行...]),...]"""
    R = W - L
    NAMEW = max(cv.measure(d[0], name_sz, weight="bold")[0] for d in data) + 44
    bsz = min(cv.fit_size([l for d in data for l in d[2]],
                          R - L - NAMEW - 80, body_sz), body_sz)
    RH = 30 + LH(bsz, lh) * (nlines - 1) + LH(bsz, 1.0) * 0.5 + 26
    for i, (name, col, lines) in enumerate(data):
        y = TOP + i * (RH + gap)
        cv.box(L, y, R - L, RH, fc="white", ec=col, lw=1.8, radius=8)
        cv.box(L, y, NAMEW, RH, fc=col, ec=col, lw=0, radius=8)
        cv.text(L + NAMEW / 2, y + RH / 2, name, size=name_sz, color="white",
                weight="bold")
        for j, ln in enumerate(lines):
            cv.text(L + NAMEW + 34,
                    y + RH / 2 - LH(bsz, lh) * (nlines - 1) / 2
                    + LH(bsz, lh) * j, ln, size=bsz, color=INK, ha="left")
    return TOP + len(data) * (RH + gap) - gap


# ---------------------------------------------------------------- f11
def f11():
    W, H = 1520, 640
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "周術期アナフィラキシー —— 麻酔下では、見え方が変わる",
             size=12.5, ha="center")
    y = two_col(cv, W, 90, [
        ("覚醒下で目立つ所見", "#2e6da4", "#eaf1f8",
         ["皮膚の紅潮、蕁麻疹、掻痒感",
          "口唇・眼瞼の浮腫",
          "喘鳴、息苦しさ",
          "腹痛、下痢、嘔気",
          "切迫感（患者本人の訴え）"]),
        ("麻酔下で最初に出る所見", "#c0392b", "#fbeeee",
         ["原因不明の血圧低下、頻脈",
          "気道内圧の上昇（換気しにくい）",
          "呼気終末二酸化炭素分圧の低下",
          "パルスオキシメータの波形の消失",
          "皮膚所見はドレープの下で見えない"]),
    ])
    y = banner(cv, W, y + 26,
               "麻酔下では、患者は何も訴えない。"
               "「原因のわからない低血圧」を見たら候補に入れる")
    note(cv, W, y + 30,
         "※ 皮膚所見は初期には出ていないことがあり、"
         "出ていてもドレープと体位で見えない。"
         "皮膚が正常であることは、アナフィラキシーの否定にならない。")
    cv.save(PP("f11_periop_ana.png"))


# ---------------------------------------------------------------- f12
def f12():
    W, H = 1520, 800
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "周術期に疑う薬剤・物質 —— 時間軸から候補を絞る",
             size=12.5, ha="center")
    DATA = [
        ("抗菌薬", "#c0392b",
         ["執刀前の予防投与が典型。投与開始から数分〜30分で発症する"]),
        ("筋弛緩薬", "#b8760f",
         ["導入直後。ロクロニウム、スキサメトニウムなど。交差反応がある"]),
        ("クロルヘキシジン", "#7b52a8",
         ["皮膚消毒、中心静脈カテーテル、潤滑剤。発症が遅れることがある"]),
        ("ラテックス", "#2e6da4",
         ["手袋、ドレーン、カテーテル。手術開始後しばらくして出る"]),
        ("色素・造影剤", "#1f6b47",
         ["センチネルリンパ節生検の色素など。投与時刻が明確"]),
        ("その他", "#5d6875",
         ["コロイド輸液、血液製剤、骨セメント、プロタミン、オピオイド"]),
    ]
    y = rows(cv, W, 96, DATA)
    y = banner(cv, W, y + 26,
               "「いつ何が入ったか」を時系列で並べると、候補は自然に絞れる",
               col="#2e6da4", fc="#eaf1f8", tc="#174682")
    note(cv, W, y + 30,
         "※ 発症までの時間は物質によって違う。"
         "皮膚消毒や体内に留置される材料は、導入から時間が経ってから発症しうる。"
         "麻酔記録の投与時刻が、あとで最も重要な資料になる。")
    cv.save(PP("f12_triggers.png"))


# ---------------------------------------------------------------- f13
def f13():
    W, H = 1520, 880
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "アナフィラキシーを疑ったときの初期対応",
             size=12.5, ha="center")
    DATA = [
        ("① 止める", "#c0392b",
         ["被疑薬の投与を直ちに中止する。応援を呼ぶ"]),
        ("② 気道", "#8f2b28",
         ["100% 酸素。喉頭浮腫が進む前に気道確保を考える"]),
        ("③ アドレナリン", "#c0392b",
         ["躊躇しない。遅れるほど転帰が悪くなる"]),
        ("④ 輸液", "#2e6da4",
         ["血管透過性亢進で血管内容量が急速に失われる。大量輸液"]),
        ("⑤ 体位", "#1f6b47",
         ["仰臥位で下肢を挙上する。急に起こさない"]),
        ("⑥ 難治なら", "#7b52a8",
         ["アドレナリン持続投与、他の昇圧薬、ECMO を考慮する"]),
        ("⑦ あとで", "#b8760f",
         ["採血（トリプターゼ）と記録。次回のために原因を確定させる"]),
    ]
    y = rows(cv, W, 96, DATA)
    y = banner(cv, W, y + 24,
               "アドレナリンに代わるものはない。抗ヒスタミン薬とステロイドは初期治療ではない")
    note(cv, W, y + 30,
         "※ 投与経路と用量は状況で変わる。"
         "静脈路とモニタがある術中では、少量ずつ静脈内投与して反応をみるのが一般的だが、"
         "施設の手順と指導医の指示に従うこと。")
    cv.save(PP("f13_ana_response.png"))


# ---------------------------------------------------------------- f14
def f14():
    W, H = 1520, 620
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "アドレナリンをためらわせるもの、そのどれもが理由にならない",
             size=12.5, ha="center")
    y = two_col(cv, W, 90, [
        ("ためらう理由として挙がるもの", "#8d97a3", "#f2f5f8",
         ["「まだ皮膚症状が出ていない」",
          "「血圧はまだ 80 ある」",
          "「高齢で虚血性心疾患がある」",
          "「まず輸液で様子を見よう」",
          "「抗ヒスタミン薬を先に」"]),
        ("実際にどうか", "#c0392b", "#fbeeee",
         ["皮膚所見は初期にはないことがある",
          "血圧が下がり切ってからでは遅い",
          "アナフィラキシーそのものが心筋を虚血にする",
          "輸液だけでは血管透過性亢進に追いつかない",
          "抗ヒスタミン薬とステロイドは初期治療ではない"]),
    ], head_sz=11.6)
    y = banner(cv, W, y + 26,
               "死亡例の多くで、アドレナリンの投与が遅れている")
    note(cv, W, y + 30,
         "※ 「打たない判断」には根拠が要る。"
         "「打つ判断」は疑いの段階でよい ── これが臨床上の非対称性である。")
    cv.save(PP("f14_adrenaline.png"))


# ---------------------------------------------------------------- f15
def f15():
    W, H = 1520, 640
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "起きたあと ── 次の麻酔を安全にするための仕事",
             size=12.5, ha="center")
    COLS = [
        ("その場で", "#c0392b",
         ["投与した薬剤とその時刻を、すべて時系列で書き出す",
          "被疑薬の残りとラベル、輸液ボトル、材料を保存する",
          "トリプターゼ採血の時刻を記録する"]),
        ("入院中に", "#b8760f",
         ["家族・本人へ説明し、記録に残す",
          "経過（再燃の有無、遷延した低血圧）を追う",
          "アレルギー科・皮膚科への紹介を準備する"]),
        ("退院までに", "#1f6b47",
         ["原因検索の予定（皮膚テスト等）を立てる",
          "確定するまでは「被疑薬」として扱う",
          "次回の麻酔科医が読める形でカルテに残す"]),
    ]
    L, R = 48, W - 48
    GAP = 22
    CW = (R - L - GAP * 2) / 3
    HTOP, HH = 92, 52
    BTOP = HTOP + HH + 8
    sz = min(cv.fit_size(["・" + l for c in COLS for l in c[2]], CW - 46, 9.9),
             9.9)
    nl = max(sum(len(cv.wrap(l, CW - 56, sz)) for l in c[2]) for c in COLS)
    BH = 30 + LH(sz, 1.6) * (nl - 1) + LH(sz, 1.0) * 0.5 + 22
    for i, (head, col, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.4, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        k = 0
        for ln in lines:
            for j, sub in enumerate(cv.wrap(ln, CW - 56, sz)):
                cv.text(x + 24, BTOP + 30 + LH(sz, 1.6) * k,
                        ("・" if j == 0 else "　") + sub, size=sz, color=INK,
                        ha="left")
                k += 1
    y = banner(cv, W, BTOP + BH + 26,
               "原因を確定させないままにすると、次の麻酔で同じことが起きる",
               col="#b8760f", fc="#fdf1e0", tc="#8a5a0f")
    note(cv, W, y + 30,
         "※ トリプターゼの採血時刻と基準値の採り方は施設の手順に従う。"
         "急性期の1点だけでは解釈できないため、時刻を必ず記録する。")
    cv.save(PP("f15_afterwards.png"))


# ---------------------------------------------------------------- f16
def f16():
    W, H = 1520, 880
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "「キシロカインが使えない」と言われたら、まず分解する",
             size=12.5, ha="center")
    DATA = [
        ("いつ", "#2e6da4", ["何年前に、どこで、何の処置で使ったか"]),
        ("何が起きたか", "#7b52a8",
         ["皮疹か、動悸か、意識消失か、痙攣か。持続時間は"]),
        ("その後", "#b8760f", ["どう対応され、その後どう説明されたか"]),
        ("記録はあるか", "#1f6b47", ["紹介状、母子手帳、歯科の記録、お薬手帳"]),
        ("何と呼ばれたか", "#c0392b",
         ["「アレルギー」なのか「体質」なのか「気分が悪くなった」なのか"]),
    ]
    y = rows(cv, W, 96, DATA)
    y = banner(cv, W, y + 24,
               "「使えない」≠ アレルギー ≠ アナフィラキシー",
               col="#2e6da4", fc="#eaf1f8", tc="#174682")
    y2 = two_col(cv, W, y + 26, [
        ("実際に多い正体", "#8d97a3", "#f2f5f8",
         ["アドレナリン添加による頻脈・血圧上昇",
          "局所麻酔薬中毒の軽い症状",
          "痛みや恐怖による血管迷走神経反射",
          "防腐剤（メチルパラベンなど）への反応"]),
        ("本当のアナフィラキシー", "#c0392b", "#fbeeee",
         ["局所麻酔薬そのものによるものは非常に稀",
          "アレルギーとして報告された症例のうち、",
          "IgE が関与した真のアナフィラキシーは 1% 未満だったという報告がある",
          "（Bhole MV, et al. Br J Anaesth 2012;108:903-11）"]),
    ], head_sz=11.6, body_sz=9.8, L=52, gapx=40)
    cv.save(PP("f16_cannot_use.png"))


# ---------------------------------------------------------------- f17
def f17():
    W, H = 1520, 760
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "代替薬をどう考えるか",
             size=12.5, ha="center")
    DATA = [
        ("アミド型で試す", "#2e6da4",
         ["メピバカイン、ロピバカインなど。リドカインと同じアミド型",
          "交差反応の可能性はあり、危険性はほぼ同じと考える"]),
        ("エステル型", "#b8760f",
         ["プロカインなど。化学構造が大きく異なるので候補にはなる",
          "代謝産物の PABA が抗原性をつくりやすく、アレルギーの可能性は高い"]),
        ("皮膚テスト", "#7b52a8",
         ["万全の体制で増量チャレンジ試験を行う",
          "アレルギー科と連携し、蘇生の準備をしたうえで実施する"]),
        ("全身麻酔", "#c0392b",
         ["真のアレルギーが確認されたなら、全身麻酔を選ぶ",
          "「無理に局所麻酔で通す」ことが最も危険な選択になる"]),
    ]
    y = rows(cv, W, 96, DATA, nlines=2, lh=1.75)
    note(cv, W, y + 30,
         "※ 「化学構造が違うから安全」とは言い切れない。"
         "代替薬の選択は、何に反応したのかを推定できて初めて意味をもつ。"
         "推定できないなら、検査するか、全身麻酔にする。")
    cv.save(PP("f17_alternatives.png"))


# ---------------------------------------------------------------- f18
def f18():
    W, H = 1520, 700
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "局所麻酔薬が効かないとき、量を足す前に考えること",
             size=12.5, ha="center")
    DATA = [
        ("① 時間", "#1f6b47", ["発現時間が来ていないだけではないか"]),
        ("② 部位", "#2e6da4", ["注入した層が違わないか。走行の個体差はないか"]),
        ("③ 病態", "#b8760f",
         ["炎症・発熱で組織が酸性になり、効きにくくなっていないか"]),
        ("④ 蛋白", "#7b52a8",
         ["急性相蛋白の増加で遊離型が減っていないか"]),
        ("⑤ 患者背景", "#c0392b",
         ["痛みの性質が違わないか。不安・恐怖の要素はないか"]),
    ]
    y = rows(cv, W, 96, DATA)
    y = banner(cv, W, y + 24,
               "極量でも痛がるなら、足すのではなく方法を変える")
    note(cv, W, y + 30,
         "※ 30分ほど間隔が開けば追加投与は可能だが、中毒の危険は常にある。"
         "総投与量が多くなりそうな症例では、最初から濃度を薄めておく。"
         "アセトアミノフェンや非ステロイド性抗炎症薬の併用は差し支えない。"
         "オピオイドは中毒の閾値を下げる可能性が示唆されている。")
    cv.save(PP("f18_not_working.png"))


# ---------------------------------------------------------------- f19
def f19():
    W, H = 1520, 760
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "二つを分ける、実務の早見",
             size=12.5, ha="center")
    L, R = 48, W - 48
    HDR = ["", "局所麻酔薬中毒", "アナフィラキシー"]
    ROWS = [
        ("気道", "痙攣→抗痙攣薬で呼吸停止しうる。挿管は必須ではない",
         "数分で喉頭浮腫が進みうる。早期に気道確保する"),
        ("最初の治療", "痙攣の抑制と 20% 脂肪乳剤",
         "アドレナリンと大量輸液"),
        ("使わないもの", "プロポフォール（抗痙攣目的）、Ⅰ群抗不整脈薬、"
                     "バソプレシン、通常量のアドレナリン",
         "抗ヒスタミン薬・ステロイドを初期治療の代わりにしない"),
        ("PCPS の位置づけ", "心血管系への作用で必要になりうる。早期に相談",
         "適正なアドレナリン使用なら通常は不要"),
        ("あとの検査", "血中濃度（測れる施設は限られる）、投与量の記録",
         "トリプターゼ、後日の皮膚テスト"),
    ]
    NAMEW = 260
    CW = (R - L - NAMEW) / 2.0
    TOP, HH = 92, 48
    cv.box(L + NAMEW, TOP, CW, HH, fc="#7b52a8", ec="#7b52a8", lw=0, radius=7)
    cv.text(L + NAMEW + CW / 2, TOP + HH / 2, HDR[1], size=11.6, color="white",
            weight="bold")
    cv.box(L + NAMEW + CW, TOP, CW, HH, fc="#c0392b", ec="#c0392b", lw=0,
           radius=7)
    cv.text(L + NAMEW + CW * 1.5, TOP + HH / 2, HDR[2], size=11.6,
            color="white", weight="bold")
    bsz = min(cv.fit_size([r[1] for r in ROWS] + [r[2] for r in ROWS],
                          CW - 40, 9.8), 9.8)
    nl = max(max(len(cv.wrap(r[1], CW - 40, bsz)),
                 len(cv.wrap(r[2], CW - 40, bsz))) for r in ROWS)
    RH = 26 + LH(bsz, 1.45) * (nl - 1) + LH(bsz, 1.0) * 0.5 + 24
    y0 = TOP + HH + 8
    for i, (name, a, b) in enumerate(ROWS):
        y = y0 + i * (RH + 10)
        cv.box(L, y, NAMEW, RH, fc="#eef1f5", ec="#9aa4b0", lw=1.4, radius=7)
        cv.text(L + NAMEW / 2, y + RH / 2, name,
                size=min(cv.fit_size([r[0] for r in ROWS],
                                     NAMEW - 30, 10.4), 10.4),
                color=NAVY,
                weight="bold")
        for k, (txt, col) in enumerate(((a, "#7b52a8"), (b, "#c0392b"))):
            x = L + NAMEW + CW * k
            cv.box(x, y, CW, RH, fc="white", ec=col, lw=1.4, radius=7)
            lines = cv.wrap(txt, CW - 40, bsz)
            for j, sub in enumerate(lines):
                cv.text(x + CW / 2,
                        y + RH / 2 - LH(bsz, 1.45) * (len(lines) - 1) / 2
                        + LH(bsz, 1.45) * j, sub, size=bsz, color=INK)
    note(cv, W, y0 + 5 * (RH + 10) + 18,
         "※ 用量・手順は施設の指示に従う。"
         "迷ったら「どちらでもありうる」として、両方に備えた準備をする。")
    cv.save(PP("f19_side_by_side.png"))


for fn in (f11, f12, f13, f14, f15, f16, f17, f18, f19):
    fn()
    print("ok", fn.__name__)
