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
                 "_教材化待ち"]
# 患者データ・作業用ファイルは載せない
SKIP_FILE_KEYS = ["患者オーダ情報", "オーダ情報_", "購入明細表", "~$"]
SKIP_FILE_NAMES = ("麻酔資料ポータル.html", "portal_template.html", "portal_template.tpl")

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

# ---------------- テーマ ----------------
THEME_RULES_KEIEI = [
    ("診療報酬・算定",       ["診療報酬", "点数", "改定", "加算", "レセプト", "算定", "包括", "K939", "マスター", "償還"]),
    ("実績データ・分析",     ["実績", "分析ツール", "データセット", "推移", "医事課", "コスト", "材料価格",
                              "収益", "明細", "グラフ集", "オペレーション", "限界利益", "dashboard"]),
    ("手術室運営・経営",     []),   # 経営分野の受け皿
]
THEME_RULES = [
    ("輸液・電解質",       ["輸液", "電解質", "水分"]),
    ("輸血・血液製剤",     ["輸血", "アルブミン", "血液製剤", "凝固", "自己血", "血小板"]),
    ("気道管理",           ["気道", "声門上", "SGA", "挿管", "ソーダライム"]),
    ("産科麻酔",           ["産科", "妊産婦", "妊娠", "胎盤", "早剝", "早期剝離", "早期剥離",
                            "分娩", "無痛分娩", "母体", "DIC診断基準"]),
    ("区域麻酔・ブロック", ["区域麻酔", "脊髄幹", "ブロック", "星状神経節", "帝王切開", "局所麻酔薬", "硬膜外", "くも膜下", "脊椎麻酔"]),
    ("循環・不整脈",       ["心房細動", "心室性", "VPC", "冠動脈", "TEE", "CSFD", "対麻痺", "トルーソー", "血栓"]),
    ("腎臓・ICU",          ["AKI", "AKD", "CRRT", "利尿", "透析", "ICU"]),
    ("モニタリング",       ["BIS", "モニタ"]),
    ("血管アクセス",       ["中心静脈", "CVC", "PAC", "肺動脈カテーテル", "動脈圧", "血管確保", "橈骨動脈", "穿刺", "PICC"]),
    ("術前評価・周術期",   ["術前", "周術期", "体位", "禁煙", "ハイリスク", "麻酔計画"]),
    ("麻酔薬理・鎮静",     ["薬理", "鎮静", "麻酔薬", "ガバペンチン", "Gabapentin", "Precision"]),
    ("医療安全",           ["安全", "アナフィラキシー", "トラブル", "中毒", "合併症", "神経障害"]),
    ("全身麻酔",           ["全身麻酔"]),
    ("学会発表・教育",     ["学会", "プレゼン", "演題", "口演", "ポスター", "スライド", "レビュー",
                            "Perplexity", "講義", "セミナー", "コース", "研究会"]),
]

def theme(path, stem, group):
    s = (stem + " " + path).lower()
    if group == "経営":
        for name, keys in THEME_RULES_KEIEI:
            if not keys or any(k.lower() in s for k in keys):
                return name
    # 教育分野でも診療報酬の話題はそちらに寄せる
    if any(k.lower() in s for k in ["診療報酬", "改定", "算定", "レセプト"]):
        return "診療報酬・算定"
    for name, keys in THEME_RULES:
        if any(k.lower() in s for k in keys):
            return name
    return "その他"

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


STRIP = re.compile(
    r"[_\s　]*(?:専門医版|専門医向け.*|専門家向け.*|専攻医.*|研修医.*|看護師.*|"
    r"要点ガイド|実践ガイド|実践ハンドブック.*|サマリ.*|レクチャー.*|"
    r"講義スライド.*|詰め込み.*|完全ガイド|完全マニュアル|詳細資料|詳説|"
    r"\d+\s*枚版?|\d+\s*頁)$")


def topic_stem(title):
    """版違いをまとめるための、資料名の語幹。

    BISモニター完全ガイド_専門医版 → BISモニター完全ガイド → BISモニター
    """
    t = re.sub(r"[_\s　]*[①-⑳].*$", "", title).strip()
    for _ in range(4):
        n = STRIP.sub("", t).strip("_ 　").strip()
        if n == t or not n:
            break
        t = n
    return t or title


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

    # その文書の代表ファイル（PDF優先）をボタンにし、残りは資料ファイルへ
    fs = sorted(d["files"], key=lambda f: FMT_ORDER.index(f["type"]))
    head, rest = fs[0], fs[1:]
    label = base
    if arch:
        label = base + "（" + arch.split("/")[-1].lstrip("_") + "）"
    it["roles"][r].append(dict(head, label=label, title=base))
    for f in rest:
        it["roles"]["資料ファイル"].append(
            dict(f, label=base + "（" + f["type"] + "）", title=base))
    it["files"].extend(d["files"])

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
    it["theme"] = theme(it["folder"], it["title"] + " " + names, it["group"])
    for r in ROLES:
        it["roles"][r].sort(key=lambda f: f["label"])
    it["files"].sort(key=lambda f: FMT_ORDER.index(f["type"]))
    out.append(it)

dest = os.path.join(DESK, "教育ファイル集", "_portal_data.json")
with open(dest, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print("資料数:", len(out), " （まとめる前の文書数:", len(docs), "）")
print("分野  :", dict(Counter(it["group"] for it in out)))
print("対象者:", dict(Counter(a for it in out for a in it["audience"])))
print("役割  :", dict(Counter(r for it in out for r in ROLES if it["roles"][r])))
print("テーマ:", dict(Counter(it["theme"] for it in out)))
print("→", dest)
