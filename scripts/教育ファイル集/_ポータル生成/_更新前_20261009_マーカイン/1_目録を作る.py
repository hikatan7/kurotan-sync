# -*- coding: utf-8 -*-
"""麻酔・手術室経営ポータルの目録（_portal_data.json）を作る。

1件＝1つの「資料（テーマ）」。同じテーマの版違いは1件にまとめ、
役割ごとのボタンに振り分ける（2026-09-14 改訂）。

    詳細版          … その資料の本体。専門医版・完全ガイド・詳説もここに含める
    研修医テキスト  … 専攻医・研修医・看護師向けの短い版
    要点解説プレゼン… スライド
    資料ファイル    … Word/PowerPoint の原本、旧版、その他の関連ファイル

以前は 1ファイル群＝1件だったため、BIS のように版が多い資料が
ポータルに7行も並んで探しにくかった。
"""

import os, json, re
from collections import OrderedDict, Counter

# 資料の基準フォルダ = このスクリプトの2つ上（教育ファイル集\_ポータル生成\ の親の親）。
# デスクトップ決め打ちをやめたので、フォルダごと移動しても正しく動く。
DESK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# (フォルダ, 分野)  分野＝"教育" / "経営"
ROOTS = [
    (os.path.join(DESK, "教育ファイル集"),                        "教育"),
    (os.path.join(DESK, "手術室経営分析"),                        "経営"),
    (os.path.join(DESK, "病院経営学", "手術室経営"),              "経営"),
    (os.path.join(DESK, "病院経営学", "診療報酬点数"),            "経営"),
    (os.path.join(DESK, "自作ファイル集", "手術件数推移"),        "経営"),
    (os.path.join(DESK, "呼外プレゼン資料作成", "5_分析レポート"), "経営"),
]
# 単体で拾うファイル（デスクトップ直下）
SINGLE_FILES = [(os.path.join(DESK, "医事課_月次推移分析.xlsm"), "経営")]

DOC_EXT = {".docx", ".doc", ".pdf", ".pptx", ".ppt", ".xlsx", ".xlsm",
           ".html", ".mp4", ".mov", ".txt"}
SKIP_DIR_KEYS = ["_編集用原本", "図版", "_重複", "引用済み", "統合済み", "_ポータル生成",
                 "_旧版", "グラフ画像", "_生成スクリプト",
                 # デスクトップから統合したときの控え（名簿・議事録・試験問題など）
                 "_デスクトップコピー統合",
                 # まだテキスト／プレゼンにしていない一次資料の置き場
                 "_教材化待ち",
                 # 症例・問題を削除する前の控え（2026-10-08）。旧版としても載せない
                 "_症例削除前", "_頁数制限解除前", "_文字拡大前", "_元_20261008"]
# 患者データ・作業用ファイルは載せない
SKIP_FILE_KEYS = ["患者オーダ情報", "オーダ情報_", "購入明細表", "~$"]
SKIP_FILE_NAMES = ("麻酔資料ポータル.html", "portal_template.html", "portal_template.tpl",
                   "_link_report.txt")

# 先頭が "_" のフォルダは原則「控え（旧版）」とみなし、資料ファイル送りにする。
# ただし次の3つは通常のフォルダとして扱う。
KEEP_UNDERSCORE = {"_PDF（閲覧用）", "_スライド版"}

ROLES = ["詳細版", "研修医テキスト", "要点解説プレゼン", "資料ファイル"]

# ---------------- 役割 ----------------
SLIDE_KEYS = ["スライド", "プレゼン", "デッキ", "deck", "podium", "講義", "レクチャー枚"]
JUNIOR_KEYS = ["専攻医", "研修医", "看護師", "要点ガイド", "実践ガイド", "読本",
               "実践ハンドブック", "サマリ", "レクチャー", "ハンドアウト", "入門"]


def role_of(title, folder, types):
    """1つの文書がどのボタンに入るかを決める。

    「専門医」「完全ガイド」などは詳細版に寄せる（別ボタンにしない）。
    スライドを先に見るのは、"②専攻医向け6枚" のように
    対象者の語とスライドの語が両方入る資料があるため。
    """
    s = (title + " " + folder).lower()
    if "スライド" in types or re.search(r"\d+\s*枚", title) \
            or any(k.lower() in s for k in SLIDE_KEYS):
        return "要点解説プレゼン"
    if any(k in title + " " + folder for k in JUNIOR_KEYS):
        return "研修医テキスト"
    return "詳細版"


# ---------------- 対象者 ----------------
def audience(path, stem, group):
    s = path + "/" + stem
    # 経営分野は「手術室経営」に一本化する（完全ガイド等の語で専門医向けに混ざるのを防ぐ）
    if group == "経営":
        return ["手術室経営"]
    a = []
    if any(k in s for k in ["専門医", "完全マニュアル", "詳説", "専門家向け", "完全ガイド", "アドバンス", "ultra_dense"]):
        a.append("専門医")
    if any(k in s for k in ["専攻医", "研修医", "レクチャー", "要点ガイド", "読本", "ベーシック", "実践ガイド",
                            "ハンドブック", "屋根瓦", "コース", "セミナー", "ワークショップ", "講義", "レジメ"]):
        a.append("専攻医・研修医")
    if any(k in s for k in ["看護師", "nursing", "ナース"]):
        a.append("看護師")
    if group == "経営" or any(k in s for k in ["経営", "運営", "診療報酬", "改定", "分析", "充足", "手術麻酔_1手術1行"]):
        a.append("手術室経営")
    return a or ["共通"]

import book_toc

# ---------------- テーマ ----------------
THEME_RULES_KEIEI = [
    ("診療報酬・算定",       ["診療報酬", "点数", "改定", "加算", "レセプト", "算定", "包括", "K939", "マスター", "償還"]),
    ("実績データ・分析",     ["実績", "分析ツール", "データセット", "推移", "医事課", "コスト", "材料価格",
                              "収益", "明細", "グラフ集", "オペレーション", "限界利益", "dashboard"]),
    ("手術室運営・経営",     []),   # 経営分野の受け皿
]
# 教育分野のテーマは、麻酔教科書の目次の大項目（部）をそのまま使う。
# 部と章、そこへ振り分けるキーワードは book_toc.py にまとめてある。


def theme(path, stem, group, title):
    """(テーマ, 小項目) を返す。

    経営と診療報酬の判定には stem（資料名＋配下のファイル名）を使う。
    教育分野の部・章の判定は「資料名＋フォルダ」だけを見る（book_toc.classify）。
    """
    s = (stem + u" " + path).lower()
    if group == u"経営":
        for name, keys in THEME_RULES_KEIEI:
            if not keys or any(k.lower() in s for k in keys):
                return name, u""
    # 教育分野でも診療報酬の話題はそちらに寄せる
    if any(k.lower() in s for k in [u"診療報酬", u"改定", u"算定", u"レセプト"]):
        return book_toc.T_HOSHU, u""
    part, chap = book_toc.classify(path, title)
    if part is None:
        return book_toc.T_SONOTA, u""
    return part, chap

def kind(ext):
    return {".docx": "Word", ".doc": "Word", ".pdf": "PDF",
            ".pptx": "スライド", ".ppt": "スライド", ".xlsx": "Excel",
            ".xlsm": "Excel", ".html": "HTML", ".mp4": "動画", ".mov": "動画",
            ".txt": "テキスト"}[ext]


# ---------------- フォルダの分解 ----------------
def split_archive(folder):
    """フォルダを「本体」と「控え」に分ける。

    .../12_BISモニター/_略語対応前  →  (.../12_BISモニター, "_略語対応前")
    控えの中の資料は、本体と同じテーマに属する旧版として扱う。
    """
    keep, arch = [], []
    for p in folder.split("/"):
        if arch or (p.startswith("_") and p not in KEEP_UNDERSCORE):
            arch.append(p)
        else:
            keep.append(p)
    return "/".join(keep), "/".join(arch)


# 版を表す末尾だけを落とす。「麻酔科研修医講義：…」のように
# 題名の途中に対象者の語が入るものまで削ってしまわないよう、語形を絞ってある。
STRIP = re.compile(
    r"[_\s　]*(?:専門医版|専門医向け[^_]*|専門家向け[^_]*|"
    r"研修医・専攻医(?:のための|向け|版)?[^_]*|専攻医・研修医(?:のための|向け|版)?[^_]*|"
    r"専攻医(?:のための|向け|版)[^_]*|専攻医版|"
    r"研修医(?:のための|向け|版)[^_]*|研修医専攻医[^_]*|"
    r"看護師(?:のための|向け|版)[^_]*|"
    r"要点ガイド|実践ガイド|実践ハンドブック[^_]*|サマリ[^_]*|レクチャー[^_]*|"
    r"講義スライド[^_]*|詰め込み[^_]*|完全ガイド|完全マニュアル|詳細資料|詳説|"
    r"\d+\s*枚版?|\d+\s*頁(?:テキスト|ミニテキスト|読本)?)$")

# 資料名そのものの直し（日本語の誤り・配布日・行き場のない接頭辞）
TITLE_FIX = [
    (re.compile(r"周術期のおける"), "周術期における"),
    (re.compile(r"[_\s　]*(?:HY|hy)?_?\d{8}$"), ""),      # …HY_20230116 / …20150727
    (re.compile(r"^\d{4}[._]\d{2}[_\s　]*"), ""),         # 2023.02脊髄幹…
    (re.compile(r"について$"), ""),
    (re.compile(r"[_\s　]*\d{4}-\d{2}-\d{2}$"), ""),        # …_2026-09-24
    (re.compile(r"_ガイドライン照合$"), ""),
]


def clean_title(t):
    for pat, rep in TITLE_FIX:
        t = pat.sub(rep, t)
    return re.sub(r"[\s　]{2,}", " ", t).strip()


def topic_stem(title):
    """版違いをまとめるための、資料名の語幹。

    BISモニター完全ガイド_専門医版 → BISモニター完全ガイド → BISモニター
    """
    t = re.sub(r"[_\s　]*[①-⑳].*$", "", clean_title(title)).strip()
    for _ in range(4):
        n = STRIP.sub("", t).strip("_ 　").strip()
        n = re.sub(r"[_\s　]*初期$", "", n)          # 「…：初期」研修医向け の削り残し
        n = re.sub(r"[_\s　：:・、]+$", "", n)
        if n == t or not n:
            break
        t = n
    return t or clean_title(title)


# 1フォルダ＝1つの資料とみなすフォルダ（末尾の名前で判定）。
# 中の原典・ガイドライン・版違いを別々の行にせず、1行にまとめる。
TOPIC_DIRS = {
    "宗教的輸血拒否（エホバの証人）": "宗教的輸血拒否（エホバの証人）",
    "周術期アナフィラキシー": "周術期アナフィラキシー",
    "01_村中_CSFD対麻痺": "CSFD と対麻痺（村中演題のレビュー）",
    "02_押坂_巨大冠動脈瘤とTEE": "巨大冠動脈瘤と TEE（押坂演題のレビュー）",
    "03_文献検索": "JSCVA2026 演題の文献検索",
    "呼吸器外科　限界利益比較用ファイル": "呼吸器外科 限界利益・材料コスト一式",
    "マスターデータ2026年": "診療報酬マスターデータ 2026年",
    "心臓手術後の心停止（CALS）": "心臓手術後の心停止（CALS）── ICLS と何が違うか",
    "静脈・動脈ルート確保": "静脈・動脈ルート確保 ── 神経損傷・器材選択・静脈炎・動脈圧ライン",
}

SERIES = "麻酔科ミニ教科書シリーズ"
VOLDIR = re.compile(r"^(\d\d)_(.+)$")


def topic_of(keep_folder, title):
    """(まとめキー, 表示名, 巻番号, 名前がフォルダ由来か) を返す。

    巻の名前は "12_BISモニター" というフォルダ名を正とする。
    _スライド版 の中の "01_..._②研修医版10枚" が先に来ても、
    そちらの長い名前が巻のタイトルにならないようにするため。
    """
    parts = keep_folder.split("/")
    if SERIES in parts:
        i = parts.index(SERIES)
        tail = parts[i + 1:]
        if tail:
            m = VOLDIR.match(tail[0])
            if m:                       # .../麻酔科ミニ教科書シリーズ/12_BISモニター
                return ("vol:" + m.group(1), m.group(2), m.group(1), True)
        m = VOLDIR.match(title)         # 総目次 と _スライド版 の中身
        if m:
            return ("vol:" + m.group(1), topic_stem(m.group(2)), m.group(1), False)
    last = parts[-1] if parts else ""
    if last in TOPIC_DIRS:
        return ("dir:" + keep_folder, TOPIC_DIRS[last], None, True)
    return (keep_folder + "|" + topic_stem(title), topic_stem(title), None, False)


# ---------------- 収集 ----------------
docs = OrderedDict()     # (keep_folder, archive, base) → 文書

def add(full, group):
    stem, ext = os.path.splitext(os.path.basename(full))
    ext = ext.lower()
    if ext not in DOC_EXT:
        return
    fn = os.path.basename(full)
    if fn in SKIP_FILE_NAMES or any(k in fn for k in SKIP_FILE_KEYS):
        return
    rel = os.path.relpath(full, DESK).replace("\\", "/")
    folder = os.path.relpath(os.path.dirname(full), DESK).replace("\\", "/")
    if folder.endswith("_PDF（閲覧用）"):
        folder = folder.rsplit("/", 1)[0]
    keep, arch = split_archive(folder)
    base = re.sub(r"\s*\(\d+\)$", "", stem)
    # "ICUにおける心房細動 完全マニュアル" と "…心房細動完全マニュアル" のように
    # 空白の有無だけが違う同じ文書を1本にまとめる
    d = docs.setdefault((keep, arch, re.sub(r"[ 　]", "", base)), {
        "title": base, "folder": keep, "archive": arch,
        "group": group, "files": []})
    base = d["title"]
    d["files"].append({"type": kind(ext), "path": rel,
                       "size_kb": round(os.path.getsize(full) / 1024)})


for root, group in ROOTS:
    if not os.path.isdir(root):
        print("!! 見つかりません:", root)
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not any(k in d for k in SKIP_DIR_KEYS)]
        for fn in filenames:
            add(os.path.join(dirpath, fn), group)
for f, group in SINGLE_FILES:
    if os.path.isfile(f):
        add(f, group)

# 「_PDF（閲覧用）」に置いた書き出しPDFを、本体（pptx/docx）の文書に合流させる。
# 本体が別フォルダにあると、そのままでは同じ資料が2件に割れてしまう。
VIEW = "/_PDF（閲覧用）/"
_by_base = {}
for k, d in docs.items():
    if not any(VIEW in f["path"] for f in d["files"]):
        _by_base.setdefault(k[2], []).append(d)
for k in [k for k, d in docs.items() if any(VIEW in f["path"] for f in d["files"])]:
    tgt = _by_base.get(k[2])
    if tgt and len(tgt) == 1:
        tgt[0]["files"].extend(docs.pop(k)["files"])

# ---------------- 資料（テーマ）にまとめる ----------------
FMT_ORDER = ["PDF", "スライド", "Word", "Excel", "HTML", "動画", "テキスト"]

items = OrderedDict()
for (keep, arch, base), d in docs.items():
    key, name, vol, sure = topic_of(keep, base)
    it = items.setdefault(key, {
        "title": name, "folder": keep, "group": d["group"],
        "vol": vol, "roles": {r: [] for r in ROLES}, "files": [], "_sure": False,
    })
    if sure and not it["_sure"]:
        it["title"], it["folder"], it["_sure"] = name, keep, True
    types = [f["type"] for f in d["files"]]
    r = "資料ファイル" if arch else role_of(base, keep, types)
    if set(types) <= {"テキスト"}:      # 検索ログなどの .txt はボタンにしない
        r = "資料ファイル"

    # その文書の代表ファイル（PDF優先）をボタンにし、残りは資料ファイルへ
    fs = sorted(d["files"], key=lambda f: FMT_ORDER.index(f["type"]))
    head, rest = fs[0], fs[1:]
    label = clean_title(base) or base
    m = re.search(r"(\d{8})$", base)
    if m and m.group(1) not in label:      # 同じ名前の配布日違いを見分けられるように
        label += "（" + m.group(1) + "）"
    if arch:
        label = label + "（" + arch.split("/")[-1].lstrip("_") + "）"
    it["roles"][r].append(dict(head, label=label, title=base))
    for f in rest:
        it["roles"]["資料ファイル"].append(
            dict(f, label=base + "（" + f["type"] + "）", title=base))
    it["files"].extend(d["files"])

# ---------------- 名前がよく似た資料を1行にまとめる ----------------
# 「声門上器具と周術期気道トラブル」と「…_10頁テキスト」、
# 「手術室経営と診療報酬_統合詳説2026_最終版」と「…_プレゼンテーション」のように、
# 同じフォルダで名前の頭が長く一致するものは、同じ資料の版違いとして1行にする。
BOUND = "_　 ：:・（(【"
MIN_HEAD = 8           # 語の切れ目まで戻した共通の頭が、これ以上なら同じ資料とみなす
MIN_RAW = 14           # 切れ目が無くても、これ以上一致していれば同じ資料とみなす
MIN_WHOLE = 6          # 片方が丸ごと他方の頭になっている場合の下限
TAIL = "とのにがはでをや、，・_　 "


def _head(a, b):
    """a と b の共通の頭を、語の切れ目まで戻して返す。"""
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    if n == len(a) or n == len(b):      # 片方が丸ごと頭になっている
        return a[:n]
    raw = n
    while n and a[n - 1] not in BOUND:
        n -= 1
    h = a[:n].rstrip(BOUND)
    if len(h) < MIN_HEAD and raw >= MIN_RAW:
        h = a[:raw].rstrip(TAIL)        # 「…の拡大と戦略的改善／…の拡大と改善策」
    return h


def merge_alike(items):
    keys = [k for k in items if not k.startswith(("vol:", "dir:"))]
    dead = set()
    for i, ka in enumerate(keys):
        if ka in dead:
            continue
        for kb in keys[i + 1:]:
            if kb in dead:
                continue
            a, b = items[ka], items[kb]
            if a["folder"] != b["folder"] or a["group"] != b["group"]:
                continue
            h = _head(a["title"], b["title"])
            whole = h in (a["title"], b["title"])
            if len(h) < (MIN_WHOLE if whole else MIN_HEAD):
                continue
            a["title"] = h                      # 短いほうの名前に寄せる
            for r in ROLES:
                a["roles"][r].extend(b["roles"][r])
            a["files"].extend(b["files"])
            dead.add(kb)
    for k in dead:
        items.pop(k)
    return len(dead)


n_merged = merge_alike(items)

# ---------------- 散らばった資料を明示的にまとめる（2026-10-07） ----------------
# merge_alike は「同じフォルダで名前の頭が一致する」ものしか拾えない。
# 別フォルダの姉妹編や、名前の頭が違う同じ話題はここで1行にする。
#
# GROUPS : (表示名, [題名の正規表現…])  … 当たった資料を1行にまとめ、表示名を付ける
# ATTACH : (子の正規表現, 親の正規表現)  … 子のファイルを全部、親の「資料ファイル」へ
# JUNIOR : (子の正規表現, 親の正規表現)  … 子の本文を親の「研修医テキスト」へ（姉妹編）
# MAKING : 制作途中の部品（査読キット・貼り付け用の全文など）。付録＞制作用リストへ
GROUPS = [
    ("周術期アナフィラキシー", [r"^周術期アナフィラキシー$", r"^10_周術期アナフィラキシー$"]),
    ("周術期の禁煙", [r"^周術期禁煙ガイドライン$", r"^手術前禁煙の効果$"]),
    ("静岡病院 気道管理コース", [r"^静岡病院気道管理コース$", r"^気道管理コース改変配布資料"]),
    ("脊髄幹麻酔セミナー・ワークショップ", [r"^脊髄幹ブロックワークショップ", r"^脊髄幹麻酔セミナー"]),
    ("学会発表の基本と方法論（口演・ポスター）", [r"^学会発表の基本_", r"^学会発表の方法論_"]),
    ("手術実績データ（匿名化）", [r"^\d{4}年手術実績_匿名化$"]),
    ("2025年度 手術件数（感染管理用）", [r"^2025年度_手術件数"]),
    ("呼吸器外科ロボット手術（RATS）の収益分析",
     [r"^呼吸器外科_RATS収益分析$", r"^呼吸器外科ロボット手術の収益分析"]),
    ("ICU加算と2026年度改定", [r"ICU加算", r"^ICU報酬2026年改定"]),
    ("ラパヘル（腹腔鏡下鼠径ヘルニア）の算定試算", [r"^ラパヘル"]),
    ("心臓血管外科入院の算定試算", [r"^上行置換レセプト$", r"^心外"]),
]
ATTACH = [
    (r"^\d+巻版$", r"^麻酔科ミニ教科書シリーズ_総目次$"),
    (r"^橈骨動脈穿刺_SourceLedger$", r"^橈骨動脈穿刺と動脈圧ライン確保"),
    (r"^硬膜外穿刺テキスト_SourceLedger$", r"^硬膜外穿刺とカテーテル挿入"),
    (r"^二十億回の拍動_SourceLedger$", r"^二十億回の拍動_サイズ"),
]
JUNIOR = [
    (r"^アルブミン製剤と輸血$", r"^血液製剤とアルブミン$"),
]
MAKING = [r"^教材\d_", r"査読キット", r"^最初に貼る全文$", r"^本文_\d回目$"]


def _find(pat):
    return [k for k, it in items.items() if re.search(pat, it["title"])]


def _absorb(dst, src, to_role=None):
    a, b = items[dst], items[src]
    for r in ROLES:
        a["roles"][to_role or r].extend(b["roles"][r])
    a["files"].extend(b["files"])
    items.pop(src)


n_grouped = 0
for name, pats in GROUPS:
    ks = []
    for p in pats:
        ks += [k for k in _find(p) if k not in ks]
    if not ks:
        continue
    # 1フォルダ＝1資料（dir:）や巻（vol:）があればそれを親にする
    ks.sort(key=lambda k: (not k.startswith(("dir:", "vol:")), k))
    for k in ks[1:]:
        _absorb(ks[0], k)
        n_grouped += 1
    items[ks[0]]["title"] = name
for child, parent in ATTACH:
    ps = _find(parent)
    for k in _find(child):
        if ps and k not in ps:
            _absorb(ps[0], k, "資料ファイル")
            n_grouped += 1
for child, parent in JUNIOR:
    ps = _find(parent)
    for k in _find(child):
        if not ps or k in ps:
            continue
        b = items[k]
        # 姉妹編の本文（詳細版・研修医テキスト）は親の研修医テキストへ、残りは資料ファイルへ
        b["roles"]["研修医テキスト"] = b["roles"]["詳細版"] + b["roles"]["研修医テキスト"]
        b["roles"]["詳細版"] = []
        _absorb(ps[0], k)
        n_grouped += 1

# 本編テキストしか無い資料（例：AKIと利尿薬_専攻医のための教科書）は、
# 研修医テキストではなく詳細版に置く。
# スライドだけの資料は繰り上げない ── ①専門医版が「詳細版」と名乗ると
# 「本があるのか」と紛らわしく、実際はどちらもスライドだから。
for it in items.values():
    if it["roles"]["詳細版"] or not it["roles"]["研修医テキスト"]:
        continue
    best = max(it["roles"]["研修医テキスト"], key=lambda f: f["size_kb"])
    it["roles"]["研修医テキスト"].remove(best)
    it["roles"]["詳細版"].append(best)

out = []
for it in items.values():
    names = " ".join(sorted({f["title"] for r in ROLES for f in it["roles"][r]}))
    it["audience"] = audience(it["folder"], it["title"] + " " + names, it["group"])
    if it["vol"] and it["vol"] != "00" and it["roles"]["詳細版"]             and "専門医" not in it["audience"]:
        it["audience"] = ["専門医"] + [a for a in it["audience"] if a != "共通"]
    it.pop("_sure", None)
    it["theme"], it["sub"] = theme(it["folder"], it["title"] + " " + names,
                                   it["group"], it["title"])
    for r in ROLES:
        it["roles"][r].sort(key=lambda f: f["label"])
    it["files"].sort(key=lambda f: FMT_ORDER.index(f["type"]))
    out.append(it)

for it in out:
    if any(re.search(p, it["title"]) for p in MAKING):
        it["theme"], it["sub"] = book_toc.P99, u"制作用リスト"

dest = os.path.join(DESK, "教育ファイル集", "_portal_data.json")
with open(dest, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print("資料数:", len(out), " （まとめる前の文書数:", len(docs),
      "／似た名前をまとめた件数:", n_merged, "／規則でまとめた件数:", n_grouped, "）")
print("分野  :", dict(Counter(it["group"] for it in out)))
print("対象者:", dict(Counter(a for it in out for a in it["audience"])))
print("役割  :", dict(Counter(r for it in out for r in ROLES if it["roles"][r])))
print("テーマ:", dict(Counter(it["theme"] for it in out)))
print("小項目なし:", sum(1 for it in out if not it["sub"]), "件")
print("→", dest)
