"""経営学ポータルをテーマ別に1本化するためのデータ作り（2026-09-24）
同じ語句は1行にまとめ、復習ノート（どの科目のどのDay）・事典・テキストの章・勉強ノートを「出てくる場所」として束ねる。"""
import os, re
from collections import Counter, defaultdict
from notekit import sort_key

THEMES = [
    ("think", "思考・問題解決", "クリティカル・シンキング", "var(--c-crt)"),
    ("strat", "経営戦略", "戦略策定・事業経済性・全社戦略", "var(--c-ems)"),
    ("mkt", "マーケティング", "STP・4P・顧客体験・デジタル", "var(--c-mkt)"),
    ("org", "組織行動とリーダーシップ", "リーダーシップ・組織変革・チーム", "var(--c-obh)"),
    ("hrm", "人材マネジメント", "評価・報酬・採用・配置・D&I", "var(--c-hrm)"),
    ("acc", "アカウンティング", "財務三表・指標分析・管理会計", "var(--c-acc)"),
    ("fin", "ファイナンス", "DCF・NPV・WACC・企業価値", "var(--c-fin)"),
    ("etc", "アナリティクス・テクノベート・共通", "データ分析・テクノロジー・倫理・オペレーション", "var(--sumi-1)"),
]
NOTE_THEME = {"crt": "think", "obh": "org", "hrm": "hrm", "mkt": "mkt", "acc": "acc", "fin": "fin"}
EMS_THEME = {1: "strat", 2: "strat", 3: "strat", 4: "mkt", 5: "mkt", 6: "strat"}
DICT_THEME = {"sen": "strat", "mkt": "mkt", "acc": "acc", "fin": "fin", "org": "org", "hrm": "hrm", "thi": "think",
              "ba": "etc", "tec": "etc", "ops": "etc", "eth": "etc"}
ORDER = [t[0] for t in THEMES]


def note_theme(course, day):
    return EMS_THEME[day] if course == "ems" else NOTE_THEME[course]


def norm(t):
    t = re.sub(r"[（(][^）)]*[）)]", "", str(t))
    return re.sub(r"[\s・\-－ー＝=／/「」『』]", "", t).lower()


def keys_of(term):
    """(外側の語, 中の語の集合, 外側が英字略語か) を返す"""
    outer = norm(term)
    inners = set()
    for inner in re.findall(r"[（(]([^）)]*)[）)]", str(term)):
        for part in re.split(r"[、,，／/]", inner):
            k = norm(part)
            if len(k) >= 2 and not re.search(r"\d{4}|年|p\d|例", k):
                inners.add(k)
    return outer, inners - {outer}, bool(re.fullmatch(r"[a-z0-9&]+", outer))


def book_theme(n):
    for k, pat in (("think", "クリティカル"), ("mkt", "マーケティング"), ("strat", "経営戦略"),
                   ("org", "組織行動"), ("org", "リーダーシップ"), ("hrm", "人材"),
                   ("acc", "アカウンティング"), ("fin", "ファイナンス")):
        if pat in n:
            return k
    return "etc"


def study_theme(rel):
    top = rel.split(os.sep)[0] if os.sep in rel else rel
    m = re.match(r"(\d\d)_", top)
    if m:
        return {"00": "etc", "01": "think", "02": "strat", "03": "mkt", "04": "org", "05": "hrm",
                "06": "acc", "07": "fin"}.get(m.group(1), "etc")
    if "マーケティング" in rel:
        return "mkt"
    if "accounting" in rel.lower() or "MBAコース作成" in rel:
        return "acc"
    return "etc"


def build(courses, dic, texts, study_items):
    """courses: build_portal の courses、dic: 事典、texts: テキスト、study_items: [{n,h,rel,s}]"""
    # ---- 語句を束ねる：かっこの外と中のどちらの言い方でもつながるよう、キーを共有する語をまとめる
    entries = []   # (keys_of の結果, kind, payload)
    for c in courses:
        for d in c["days"]:
            if d.get("id"):
                for t in d["_terms"]:
                    entries.append((keys_of(t["term"]), "note", (c["key"], d["day"], t)))
    for x in dic["items"]:
        o, ins, asc = keys_of(x["name"])
        if x.get("en"):
            ins = ins | {norm(x["en"])}
        entries.append(((o, ins, asc), "dict", x))
    parent = list(range(len(entries)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    def union(i, j):
        parent[find(i)] = find(j)
    # 規則：外側どうしは結ぶ。中の語が別の語の外側と同じなら結ぶ。
    # 中の語どうしは、両方とも外側が和語のときだけ結ぶ（ROIとROICのように略語どうしは結ばない）
    outer_owner, inner_owner = {}, {}
    for i, ((o, ins, asc), kind, pl) in enumerate(entries):
        if o in outer_owner:
            union(i, outer_owner[o])
        else:
            outer_owner[o] = i
    for i, ((o, ins, asc), kind, pl) in enumerate(entries):
        for k in ins:
            if k in outer_owner:
                union(i, outer_owner[k])
            if not asc:
                if k in inner_owner:
                    union(i, inner_owner[k])
                else:
                    inner_owner[k] = i
    groups = defaultdict(lambda: {"refs": [], "dict": None, "names": Counter(), "yomi": "", "key": ""})
    for i, (kk, kind, pl) in enumerate(entries):
        g = groups[find(i)]
        if kind == "note":
            ck, day, t = pl
            g["refs"].append({"c": ck, "d": day, "p": t["pages"], "e": t["expl"]})
            g["names"][t["term"]] += 1
            if t["yomi"] and not g["yomi"]:
                g["yomi"] = t["yomi"]
            g["key"] = g["key"] or norm(t["term"])
        elif not g["dict"]:
            g["dict"] = pl["id"]
            if not g["names"]:
                g["names"][pl["name"]] += 1
            g["key"] = g["key"] or norm(pl["name"])
    dmap = {x["id"]: x for x in dic["items"]}

    # テキストの章・節と勉強ノートの話題を、名前で引けるように
    tx_index = []
    for bi, b in enumerate(texts):
        for c in b["ch"]:
            tx_index.append((norm(c["t"]), bi, c))
    concepts = []
    for gi, g in groups.items():
        k = g["key"]
        if not k:
            continue
        if g["dict"]:
            x = dmap[g["dict"]]
            name = x["name"] if not g["names"] else g["names"].most_common(1)[0][0]
            th = DICT_THEME.get(x["cat"], "etc")
        else:
            name = g["names"].most_common(1)[0][0]
            cnt = Counter(note_theme(r["c"], r["d"]) for r in g["refs"])
            # 思考（CRT）の演習で出ただけの語は、他のテーマがあればそちらへ
            best = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0] == "think", ORDER.index(kv[0])))
            th = best[0][0]
        core = k
        tx = []
        if len(core) >= 3 or (re.fullmatch(r"[a-z0-9&]+", core) and len(core) >= 2):
            for nk, bi, c in tx_index:
                if core in nk:
                    tx.append({"b": bi, "t": c["t"], "p": c["p"]})
                    if len(tx) >= 4:
                        break
        st = [i for i, s in enumerate(study_items) if s.get("topic") and len(core) >= 2
              and (core in norm(s["topic"]) or norm(s["topic"]) in core)]
        y = g["yomi"] or name
        concepts.append({"n": name, "y": g["yomi"], "th": th, "refs": g["refs"], "dict": g["dict"],
                         "tx": tx, "st": st, "k": list(sort_key(name, g["yomi"]))})
    concepts.sort(key=lambda c: (c["k"][0], c["k"][1]))
    for c in concepts:
        del c["k"]

    # ---- テーマごとに束ねる
    themes = []
    for key, label, sub, color in THEMES:
        notes = [[c["key"], d["day"]] for c in courses for d in c["days"]
                 if (d.get("id") or d.get("none")) and note_theme(c["key"], d["day"]) == key
                 and not (d.get("none") and "保存されていません" in d.get("none", ""))]
        themes.append({"key": key, "label": label, "sub": sub, "color": color, "notes": notes,
                       "books": [i for i, b in enumerate(texts) if book_theme(b["n"]) == key],
                       "study": [i for i, s in enumerate(study_items) if study_theme(s["rel"]) == key],
                       "nc": sum(1 for c in concepts if c["th"] == key)})
    return themes, concepts
