"""経営学ポータル.html を作る。
python build_portal.py
index/*.json（復習ノート）と、各科目フォルダ・経営学テキスト・勉強ノートのファイル一覧を
1枚のHTMLに埋め込む。リンクは 経営学 フォルダからの相対パス。"""
import glob, json, os, re, datetime
from urllib.parse import quote
from notekit import sort_key
from check_pages import SRC
import portal_extra

HERE = os.path.dirname(os.path.abspath(__file__))
MBA = os.path.dirname(HERE)                 # グロービズMBAコース
TOP = os.path.dirname(MBA)                  # 経営学
OUT = os.path.join(TOP, "経営学ポータル.html")

COURSES = [  # (key, フォルダ, 表示名, 期, Dayフォルダ名の形)
    ("crt", "クリティカルシンキング", "クリティカル・シンキング", "2601期", "Day{}教材"),
    ("ems", "マーケティング経営戦略基礎", "マーケティング・経営戦略基礎", "2601期", "Day{}"),
    ("obh", "組織行動とリーダーシップ", "組織行動とリーダーシップ", "2604期", "Day{}"),
    ("hrm", "人材マネジメント", "人材マネジメント", "2604・2607期", "Day{}"),
    ("mkt", "マーケティング", "マーケティング", "2607期", "Day{}"),
    ("acc", "アカウンティング基礎", "アカウンティング基礎", "2607期", "Day{}"),
    ("fin", "ファイナンス基礎", "ファイナンス基礎", "2607期", "Day{}"),
]
# ノートがない日の理由と、フォルダの注意書き
NO_NOTE = {
    ("obh", 2): "Day2の講義スライドは保存されていません（ケース・課題のみ）。",
    ("mkt", 6): "Day6は授業前です（ケース・課題を配布済み）。授業後にスライドが届いたらノートを作ります。",
    ("acc", 6): "Day6は授業前です（HLGケース・予測FSデータ・課題を配布済み）。授業後にスライドが届いたらノートを作ります。",
    ("fin", 6): "Day6は授業前です（IP社ケース・テキスト・課題を配布済み）。授業後にスライドが届いたらノートを作ります。",
}
DAY_NOTES = {
    ("hrm", 3): "2607期版と2604期版の2本あり（2604期版は2026-09-24に組織行動Day2から移動）。",
    ("hrm", 5): "2604期版のスライドのみ（2607期版はフォルダになし）。",
    ("hrm", 6): "2604期版のスライドのみ（2607期版はフォルダになし）。",
    ("acc", 4): "2本目のPDF（カゴメ決算短信の抜粋）は1頁目が文字化け。",
    ("acc", 5): "有価証券報告書の抜粋PDFは画像のみで、文字検索できません。",
}
MISSING = [
    ("マーケティング Day6", "授業前", "ケース（MKT_Day6_CASE_000084-J）・課題・振り返りアサインメントのみ"),
    ("アカウンティング基礎 Day6", "授業前", "HLGケース（9B11BJ009）・［配付1］HLG-Baseシナリオ・予測FSデータ・課題のみ"),
    ("ファイナンス基礎 Day6", "授業前", "IP社ケース・テキスト（IEF_Day6_TXT）・課題のみ"),
    ("人材マネジメント Day5・Day6", "2607期版なし", "2604期（平康講師）のスライドのみ。Day1〜4は2607期版あり"),
    ("置き場所違い（解消済み）", "2026-09-24移動", "HRM Day3の2604期スライド→人材マネジメント／Day3、EMS Day4・Day6のスライドとチェキ(B)ケース→マーケティング経営戦略基礎／Day4・Day6"),
    ("アカウンティング基礎 Day4", "一部読めない", "…195135500（カゴメ決算短信の抜粋）の1頁目は文字化け、2〜4頁は読める"),
    ("アカウンティング基礎 Day5", "文字データなし", "…091915687（サイゼリヤ有価証券報告書の抜粋）は画像のみ"),
]
SKIP_EXT = {".png", ".jpg", ".jpeg", ".csv", ".ini", ".exe", ".txt", ".tmp"}


def href(abs_path):
    rel = os.path.relpath(abs_path, TOP).replace("\\", "/")
    return "/".join(quote(p) for p in rel.split("/"))


def kind(name):
    n = name
    if "_復習ノート" in n:
        return "note"
    if re.search(r"jpi[a-z]+\d{4}", n) or re.match(r"(IEA|IEF)_Day\d_jpi", n):
        return "slide"
    if re.search(r"課題|振り返り|アサインメント|GW|Room|room|グループ|解答", n):
        return "work"
    if re.search(r"CASE|TXT|WS_|\d{3}-\d?Z\d|9B11|\d{6}-J|配付|配布|ケース", n):
        return "case"
    return "other"


def day_files(folder):
    out = []
    if not os.path.isdir(folder):
        return out
    for f in sorted(os.listdir(folder)):
        p = os.path.join(folder, f)
        if os.path.isdir(p) or f.startswith("~$"):
            continue
        ext = os.path.splitext(f)[1].lower()
        if ext in SKIP_EXT:
            continue
        out.append({"n": f, "h": href(p), "k": kind(f), "x": ext[1:]})
    return out


def main():
    notes = {}
    for f in glob.glob(os.path.join(HERE, "index", "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        notes[d["id"]] = d

    courses, terms = [], []
    for key, folder, label, term, dayfmt in COURSES:
        days = []
        for day in range(1, 7):
            nid = f"{key}{day}"
            dfolder = os.path.join(MBA, folder, dayfmt.format(day))
            item = {"day": day, "files": day_files(dfolder), "folder": href(dfolder),
                    "memo": DAY_NOTES.get((key, day), "")}
            n = notes.get(nid)
            if n:
                base = os.path.join(MBA, n["dir"], n["file"])
                item.update(id=nid, title=n["title"], case=n["case"], lecturer=n["lecturer"],
                            sources=n["sources"], lead=n["lead"], nterms=len(n["terms"]),
                            pdf=href(base + ".pdf"), docx=href(base + ".docx"),
                            heads=[s if isinstance(s, str) else s[0] for s in n["sections"]])
                if nid in SRC:
                    item["slide"] = href(os.path.join(MBA, SRC[nid]))
                    item["slidename"] = os.path.basename(SRC[nid])
                for t in n["terms"]:
                    terms.append({"t": t["term"], "y": t["yomi"], "e": t["expl"], "p": t["pages"],
                                  "c": key, "d": day, "k": list(sort_key(t["term"], t["yomi"]))})
            else:
                item["none"] = NO_NOTE.get((key, day), "復習ノート未作成")
            days.append(item)
        courses.append({"key": key, "label": label, "term": term, "days": days,
                        "folder": href(os.path.join(MBA, folder))})
    terms.sort(key=lambda x: (x["k"][0], x["k"][1], x["c"], x["d"]))
    for t in terms:
        del t["k"]

    # 教材・勉強ノート・ツール
    lib = []
    tx = os.path.join(TOP, "経営学テキスト")
    tools = [("MBA用語・フレームワーク事典.html", "MBA用語・フレームワーク事典（既存）"),
             ("mba-knowledge-dashboard.html", "MBA知識ダッシュボード（既存）"),
             ("経営学チェックノート.xlsx", "経営学チェックノート（勉強ノートの目次）"),
             ("S01_t01_GMAP_AI_tebiki.pdf", "GMAP AI手引き")]
    lib.append({"g": "ツール・台帳", "items": [
        {"n": lab, "h": href(os.path.join(TOP, f)), "x": os.path.splitext(f)[1][1:]}
        for f, lab in tools if os.path.exists(os.path.join(TOP, f))]})
    tpl = [f for f in sorted(os.listdir(MBA)) if f.lower().endswith((".docx", ".pptx"))]
    syl = os.path.join(MBA, "クリティカルシンキング", "シラバス、総合教材")
    lib.append({"g": "課題テンプレート・シラバス", "items":
        [{"n": f, "h": href(os.path.join(MBA, f)), "x": os.path.splitext(f)[1][1:]} for f in tpl] +
        [{"n": "CRT " + f, "h": href(os.path.join(syl, f)), "x": "pdf"} for f in sorted(os.listdir(syl)) if f.lower().endswith(".pdf")]})
    sn = os.path.join(TOP, "勉強ノート")
    for sub in sorted(os.listdir(sn)):
        p = os.path.join(sn, sub)
        items = []
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for f in sorted(files):
                    if os.path.splitext(f)[1].lower() in SKIP_EXT:
                        continue
                    topic = os.path.relpath(root, p)
                    items.append({"n": f, "h": href(os.path.join(root, f)), "x": os.path.splitext(f)[1][1:],
                                  "s": "" if topic == "." else re.sub(r"^\d+-\d+_", "", topic)})
            if items:
                lib.append({"g": "勉強ノート｜" + re.sub(r"^\d+_", "", sub), "items": items})
    loose = [f for f in sorted(os.listdir(sn)) if os.path.isfile(os.path.join(sn, f))
             and os.path.splitext(f)[1].lower() not in SKIP_EXT]
    if loose:
        lib.append({"g": "勉強ノート｜直下の資料", "items": [
            {"n": f, "h": href(os.path.join(sn, f)), "x": os.path.splitext(f)[1][1:]} for f in loose]})

    texts = portal_extra.text_books(tx, href)
    dic = portal_extra.dictionary(os.path.join(TOP, "MBA用語・フレームワーク事典.html"))
    dic["h"] = href(os.path.join(TOP, "MBA用語・フレームワーク事典.html"))
    data = {"courses": courses, "terms": terms, "lib": lib, "texts": texts, "dict": dic,
            "missing": [{"w": a, "s": b, "d": c} for a, b, c in MISSING],
            "made": datetime.date.today().isoformat()}
    tpl = open(os.path.join(HERE, "portal_template.html"), encoding="utf-8").read()
    css = open(os.path.join(HERE, "portal_base.css"), encoding="utf-8").read()
    html = tpl.replace("/*BASECSS*/", css).replace("/*DATA*/", json.dumps(data, ensure_ascii=False))
    open(OUT, "w", encoding="utf-8").write(html)
    nn = sum(1 for c in courses for d in c["days"] if d.get("id"))
    print(f"{OUT}\n ノート{nn}本 語句{len(terms)} 教材グループ{len(lib)}")


# 見た目は portal_template.html（麻酔資料ポータルの色違い）と portal_base.css（麻酔資料ポータルのCSSを複写）


if __name__ == "__main__":
    main()
