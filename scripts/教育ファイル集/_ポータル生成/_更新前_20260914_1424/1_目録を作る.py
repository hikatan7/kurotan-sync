# -*- coding: utf-8 -*-
"""麻酔・手術室経営ポータルの目録（_portal_data.json）を作る。
   デスクトップ配下の対象フォルダを走査し、1資料＝1件（docx/pdf/pptx等はまとめて files[]）にする。"""

import os, json, re
from collections import OrderedDict

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
SKIP_DIR_KEYS = ["_編集用原本", "図版", "_重複", "引用済み", "統合済み", "_ポータル生成", "_旧版", "グラフ画像"]
# 患者データ・作業用ファイルは載せない
SKIP_FILE_KEYS = ["患者オーダ情報", "オーダ情報_", "購入明細表", "~$"]
SKIP_FILE_NAMES = ("麻酔資料ポータル.html", "portal_template.html", "portal_template.tpl")

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

def add(items, full, group):
    stem, ext = os.path.splitext(os.path.basename(full))
    ext = ext.lower()
    if ext not in DOC_EXT:
        return
    fn = os.path.basename(full)
    if fn in SKIP_FILE_NAMES or any(k in fn for k in SKIP_FILE_KEYS):
        return
    dirpath = os.path.dirname(full)
    rel = os.path.relpath(full, DESK).replace("\\", "/")
    folder = os.path.relpath(dirpath, DESK).replace("\\", "/")
    if folder.endswith("_PDF（閲覧用）"):
        folder = folder.rsplit("/", 1)[0]
    base = re.sub(r"\s*\(\d+\)$", "", stem)
    key = folder + "|" + base
    it = items.setdefault(key, {
        "title": base,
        "folder": folder,
        "group": group,
        "audience": audience(folder, base, group),
        "theme": theme(folder, base, group),
        "files": [],
    })
    it["files"].append({"type": kind(ext), "path": rel,
                        "size_kb": round(os.path.getsize(full) / 1024)})

items = OrderedDict()
for root, group in ROOTS:
    if not os.path.isdir(root):
        print("!! 見つかりません:", root)
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not any(k in d for k in SKIP_DIR_KEYS)]
        for fn in filenames:
            add(items, os.path.join(dirpath, fn), group)
for f, group in SINGLE_FILES:
    if os.path.isfile(f):
        add(items, f, group)

out = list(items.values())
order = ["Word", "PDF", "スライド", "Excel", "HTML", "動画", "テキスト"]
for it in out:
    it["files"].sort(key=lambda f: order.index(f["type"]))

dest = os.path.join(DESK, "教育ファイル集", "_portal_data.json")
with open(dest, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

from collections import Counter
print("資料数:", len(out))
print("分野  :", dict(Counter(it["group"] for it in out)))
print("対象者:", dict(Counter(a for it in out for a in it["audience"])))
print("テーマ:", dict(Counter(it["theme"] for it in out)))
print("→", dest)
