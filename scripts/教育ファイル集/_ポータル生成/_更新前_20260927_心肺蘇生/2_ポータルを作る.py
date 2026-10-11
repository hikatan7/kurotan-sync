# -*- coding: utf-8 -*-
import json, os, io, re, datetime, collections

import book_toc

# 資料の基準フォルダ = このスクリプトの2つ上（教育ファイル集\_ポータル生成\ の親の親）。
# デスクトップ決め打ちをやめたので、フォルダごと移動しても正しく動く。
DESK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC  = os.path.join(DESK, "教育ファイル集", "_portal_data.json")
OUT  = os.path.join(DESK, "教育ファイル集", "麻酔資料ポータル.html")

items = json.load(io.open(SRC, encoding="utf-8"))

# ---- テーマ別ポータル（蘇生・急変対応）----
# 26_… の _生成スクリプト/portal26.py が書き出す。無ければ節ごと出さない。
RESUS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme_resus.json")
resus = json.load(io.open(RESUS_JSON, encoding="utf-8")) if os.path.exists(RESUS_JSON) else None
n_resus = len(resus["rows"]) if resus else 0

AUD = ["専門医", "専攻医・研修医", "看護師", "手術室経営", "共通"]
AUD_LABEL = {"専門医": "専門医向け", "専攻医・研修医": "専攻医・研修医向け", "看護師": "看護師向け",
             "手術室経営": "手術室経営", "共通": "共通・その他"}
AUD_VAR = {"専門医": "--accent", "専攻医・研修医": "--pos", "看護師": "--violet",
           "手術室経営": "--amber", "共通": "--sumi-2"}
FMT = ["Word", "PDF", "スライド", "Excel", "HTML", "動画", "テキスト"]
FMT_COLOR = {"Word": "--accent", "PDF": "--neg", "スライド": "--amber", "Excel": "--pos",
             "HTML": "--cyan", "動画": "--violet", "テキスト": "--sumi-2"}
# テーマの並びと、その下の小項目の並びは book_toc.py（麻酔教科書の目次）が持つ。
# テーマ＝目次の大項目（部）、小項目＝章。目録側（1_目録を作る.py）も同じものを読む。
THEME_ORDER = book_toc.THEME_ORDER
DOMAIN = ["教育", "経営"]
DOM_LABEL = {"教育": "麻酔・周術期の教育", "経営": "手術室経営"}
DOM_VAR = {"教育": "--accent", "経営": "--amber"}

n_aud = collections.Counter(a for it in items for a in it["audience"])
n_fmt = collections.Counter(f["type"] for it in items for f in it["files"])
n_thm = collections.Counter(it["theme"] for it in items)
n_dom = collections.Counter(it["group"] for it in items)
themes = [t for t in THEME_ORDER if n_thm.get(t)]
missing = [t for t in n_thm if t not in THEME_ORDER]
if missing:
    print("!! THEME_ORDER に未登録のテーマがあります（タイルが出ません）:", missing)

# ---- ミニ教科書シリーズ ----
# 目録側で 1巻＝1件にまとめてあるので、巻番号で拾うだけでよい。
# 小項目はテーマごとに数える。目次に無い小項目が出たら並び順が決まらないので警告する。
n_sub = collections.Counter((it["theme"], it.get("sub"))
                           for it in items if it.get("sub"))
subs = {}
for t in themes:
    order = book_toc.SUB_ORDER.get(t, [])
    have = [x for x in order if n_sub.get((t, x))]
    extra = [x for (tt, x) in n_sub if tt == t and x not in order]
    if extra:
        print("!! 目次に無い小項目:", t, extra)
    if have or extra:
        subs[t] = have + sorted(extra)

vols = sorted([it for it in items if it.get("vol") and it["vol"] != "00"],
              key=lambda it: it["vol"])

idx = {id(it): i for i, it in enumerate(items)}
data = {"items": items, "themes": themes, "resus": resus,
        "subs": subs,
        "vols": [{"no": v["vol"], "name": v["title"], "i": idx[id(v)]} for v in vols]}

d = datetime.date.today()
today = "%d年%d月%d日" % (d.year, d.month, d.day)

SEC = [
    ("sec1", "対象者別サマリ", None, None,
     '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 20h16"/><rect x="6" y="10" width="3" height="10"/><rect x="11" y="6" width="3" height="14"/><rect x="16" y="13" width="3" height="7"/></svg>'),
    ("sec2", "テーマ別インデックス", None, len(themes),
     '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 6h16M4 12h16M4 18h10"/><circle cx="20" cy="18" r="1.4"/></svg>'),
    ("sec3", "ミニ教科書シリーズ", None, len(vols),
     '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 5h7v15H4z"/><path d="M13 5h7v15h-7z"/><path d="M4 9h7M13 9h7"/></svg>'),
    ("sec3b", "蘇生・急変対応", None, None,
     '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 12h4l2-5 3 10 2-5h7"/></svg>'),
    ("sec4", "専門医向け", "専門医", None,
     '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/><path d="M9 12l2 2 4-4"/></svg>'),
    ("sec5", "専攻医・研修医向け", "専攻医・研修医", None,
     '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 8l9-4 9 4-9 4z"/><path d="M7 11v5c0 1 2.2 2.5 5 2.5s5-1.5 5-2.5v-5"/></svg>'),
    ("sec6", "看護師向け", "看護師", None,
     '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><path d="M12 7v10M7 12h10"/></svg>'),
    ("sec7", "手術室経営", "手術室経営", None,
     '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 20V9l8-5 8 5v11z"/><path d="M9 20v-6h6v6"/></svg>'),
    ("sec8", "共通・その他", "共通", None,
     '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="4" y="4" width="16" height="16" rx="1"/><path d="M4 9h16M9 4v16"/></svg>'),
    ("sec9", "使い方", None, None,
     '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 113.2 2.4c-.7.3-1.2.9-1.2 1.6v.5"/><circle cx="12" cy="17" r=".6" fill="currentColor"/></svg>'),
]

nav = []
for sid, name, aud, cnt, ic in SEC:
    if aud:
        badge = '<span class="nav-badge num">%d</span>' % n_aud.get(aud, 0)
    elif cnt:
        badge = '<span class="nav-badge num">%d</span>' % cnt
    elif sid == "sec3b":
        badge = '<span class="nav-badge num">%d</span>' % n_resus
    else:
        badge = ""
    nav.append('      <a href="#%s" data-nav="%s">%s%s%s</a>' % (sid, sid, ic, name, badge))
nav_html = "\n".join(nav)

tpl_sec = """
    <section class="section" id="{sid}" data-sec="{aud}">
      <div class="sec-head">
        <div>
          <div class="sec-title-wrap">
            <span class="sec-num">SEC — {num}</span>
            <div class="sec-title">{name}</div>
          </div>
          <div class="sec-sub">{note}　<span class="hit num" data-hit="{aud}"></span></div>
        </div>
        <div class="sec-actions"><span class="legend-dot" style="background:var({color})"></span>{label}</div>
      </div>
      <div class="table-wrap tall">
        <table class="mise" data-table="{aud}">
          <thead><tr>
            <th class="sortable" data-sort="title">資料名<span class="arrow"></span></th>
            <th>対象者</th><th>形式</th>
            <th class="r sortable" data-sort="size">サイズ (MB)<span class="arrow"></span></th>
            <th>場所</th>
          </tr></thead>
          <tbody></tbody>
        </table>
      </div>
    </section>"""

NOTES = {
    "専門医": "詳説・完全マニュアル・専門医版のスライドと教科書",
    "専攻医・研修医": "要点ガイド・レクチャー・研修医読本・実践ガイド",
    "看護師": "術前外来と病棟向けの説明資料",
    "手術室経営": "手術室の実績分析・運営・診療報酬",
    "共通": "対象者を限定していない資料と動画・文献",
}
secs = []
for i, (sid, name, aud, cnt, ic) in enumerate(SEC):
    if not aud:
        continue
    secs.append(tpl_sec.format(sid=sid, num="%02d" % (i + 1), name=name, aud=aud,
                               note=NOTES[aud], color=AUD_VAR[aud], label=AUD_LABEL[aud]))
sec_html = "\n".join(secs)

mx = max(n_aud.values())
aud_bars = "\n            ".join(
    '<div class="bar-row"><div class="bar-lbl">%s</div>'
    '<div class="bar-track"><div class="bar-fill" style="width:%.1f%%;background:var(%s)"></div></div>'
    '<div class="bar-val num">%d</div></div>'
    % (AUD_LABEL[a], 100.0 * n_aud.get(a, 0) / mx, AUD_VAR[a], n_aud.get(a, 0)) for a in AUD)

fmt_total = sum(n_fmt.values())
fmt_seg = "".join('<div class="seg" style="width:%.2f%%;background:var(%s)" title="%s %d"></div>'
                  % (100.0 * n_fmt[f] / fmt_total, FMT_COLOR[f], f, n_fmt[f]) for f in FMT if n_fmt.get(f))
fmt_leg = "".join('<span class="leg"><span class="legend-dot" style="background:var(%s)"></span>%s <b class="num">%d</b></span>'
                  % (FMT_COLOR[f], f, n_fmt[f]) for f in FMT if n_fmt.get(f))

kpis = [("総資料数", len(items), "麻酔教育＋手術室経営を統合"),
        ("麻酔・周術期の教育", n_dom.get("教育", 0), "教科書・スライド・動画・文献"),
        ("手術室経営", n_dom.get("経営", 0), "運営・診療報酬・実績データ"),
        ("専門医向け", n_aud.get("専門医", 0), "詳説・完全マニュアル・専門医版"),
        ("専攻医・研修医向け", n_aud.get("専攻医・研修医", 0), "要点ガイド・レクチャー・読本")]
kpi_html = "\n".join('      <div class="kpi"><div class="k-label">%s</div>'
                     '<div class="k-value num">%d<span class="unit">件</span></div>'
                     '<div class="k-foot">%s</div></div>' % k for k in kpis)

chips_fmt = "".join('<span class="chip on" data-chip="fmt" data-val="%s">%s<b class="num">%d</b></span>'
                    % (f, f, n_fmt[f]) for f in FMT if n_fmt.get(f))

tiles_dom = ('<div class="tile all" data-pick="dom"><span class="tn">すべて</span>'
             '<span class="tc">%d</span></div>' % len(items)) +             "".join('<div class="tile aud-tile" data-pick="dom" data-val="%s" style="--bar:var(%s)">'
                    '<span class="tn">%s</span><span class="tc">%d</span></div>'
                    % (g, DOM_VAR[g], DOM_LABEL[g], n_dom.get(g, 0)) for g in DOMAIN)

tiles_aud = ('<div class="tile all" data-pick="aud"><span class="tn">すべて</span>'
             '<span class="tc">%d</span></div>' % len(items)) + \
            "".join('<div class="tile aud-tile" data-pick="aud" data-val="%s" style="--bar:var(%s)">'
                    '<span class="tn">%s</span><span class="tc">%d</span></div>'
                    % (a, AUD_VAR[a], AUD_LABEL[a], n_aud.get(a, 0)) for a in AUD)

tiles_thm = ('<div class="tile all" data-pick="thm"><span class="tn">すべてのテーマ</span>'
             '<span class="tc">%d</span></div>' % len(items)) + \
            "".join('<div class="tile" data-pick="thm" data-val="%s">'
                    '<span class="tn">%s</span><span class="tc">%d</span></div>'
                    % (t, t, n_thm[t]) for t in themes)

toc = [it for it in items if it.get("vol") == "00"]
toc_files = toc[0]["roles"]["詳細版"] if toc else []
toc_href = "../" + toc_files[0]["path"] if toc_files else "#"

RKINDS = ["本文", "図版", "院内資料", "外部文献", "関連既刊"]
if resus:
    n_rk = collections.Counter(r["kind"] for r in resus["rows"])
    resus_chips = ('<span class="chip on" data-rk="all">すべて<b class="num">%d</b></span>'
                   % n_resus) + "".join(
        '<span class="chip off" data-rk="%s">%s<b class="num">%d</b></span>'
        % (k, k, n_rk.get(k, 0)) for k in RKINDS if n_rk.get(k))
else:
    resus_chips = ""

TPL = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "portal_template.tpl"),
              encoding="utf-8").read()

html = (TPL
        .replace("__NAV__", nav_html)
        .replace("__KPI__", kpi_html)
        .replace("__CHIPS_FMT__", chips_fmt)
        .replace("__TILES_DOM__", tiles_dom)
        .replace("__TILES_AUD__", tiles_aud)
        .replace("__TILES_THM__", tiles_thm)
        .replace("__AUD_BARS__", aud_bars)
        .replace("__FMT_SEG__", fmt_seg)
        .replace("__FMT_LEG__", fmt_leg)
        .replace("__SECTIONS__", sec_html)
        .replace("__RESUS_TITLE__", resus["title"] if resus else "")
        .replace("__RESUS_NOTE__", resus["note"] if resus else "")
        .replace("__RESUS_PDF__", ("../" + resus["pdf"]) if resus else "#")
        .replace("__RESUS_CHIPS__", resus_chips)
        .replace("__NVOL__", str(len(vols)))
        .replace("__NTHEME__", str(len(themes)))
        .replace("__TOC__", toc_href)
        .replace("__TODAY__", today)
        .replace("__N__", str(len(items)))
        .replace("__DATA__", json.dumps(data, ensure_ascii=False)))

io.open(OUT, "w", encoding="utf-8").write(html)
print("written", len(html), "chars ->", OUT)
print("items", len(items), "vols", len(vols), "themes", len(themes))
print("小項目のあるテーマ:", ", ".join("%s(%d)" % (t, len(v)) for t, v in subs.items()))
