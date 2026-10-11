# -*- coding: utf-8 -*-
"""蘇生・急変対応ポータル（一次資料込みの横断検索）を作る。

教育ファイル集\\蘇生・急変対応ポータル.html を書き出す。
リンクはすべて教育ファイル集からの相対パス。
"""
import html
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import c26_p1
import c26_p2
import c26_p3
import c26_p4

VOL = os.path.dirname(HERE)                      # 26_...
SERIES = os.path.dirname(VOL)                    # 麻酔科ミニ教科書シリーズ
EDU = os.path.dirname(SERIES)                    # 教育ファイル集
OUT = os.path.join(EDU, "蘇生・急変対応ポータル.html")

VOLDIR = "麻酔科ミニ教科書シリーズ/26_蘇生アルゴリズムの変遷と周術期心停止"
PDF = VOLDIR + "/蘇生アルゴリズムの変遷と周術期心停止.pdf"
DOCX = VOLDIR + "/蘇生アルゴリズムの変遷と周術期心停止.docx"
SRC = "_教材化待ち/一次資料（講義スライド・文献）/01_蘇生・急変対応"

BLOCKS = c26_p1.BLOCKS + c26_p2.BLOCKS + c26_p3.BLOCKS + c26_p4.BLOCKS


# ------------------------------------------------------------ 章を組み立てる
def build_chapters():
    """h2 を 1 件として、本文・小見出し・図・まとめを束ねる。"""
    out, cur, part = [], None, ""
    for b in BLOCKS:
        k = b[0]
        if k == "h1":
            part = b[1]
            continue
        if k == "h2":
            if cur:
                out.append(cur)
            cur = {"title": b[1], "part": part, "subs": [], "text": [],
                   "figs": [], "sums": [], "notes": []}
            continue
        if cur is None:
            continue
        if k == "h3":
            cur["subs"].append(b[1])
            cur["text"].append(b[1])
        elif k == "p":
            cur["text"].append(b[1])
        elif k == "ul":
            cur["text"].extend(b[1])
        elif k == "fig":
            cur["figs"].append({"file": b[1], "cap": b[2]})
            cur["text"].append(b[2])
        elif k == "tbl":
            cur["text"].extend([str(x) for x in b[1]])
            for row in b[2]:
                cur["text"].extend([str(x) for x in row])
        elif k == "sum":
            cur["sums"].extend(b[2])
            cur["text"].extend(b[2])
        elif k == "note":
            cur["notes"].append(b[1])
            cur["text"].append(b[1])
            cur["text"].extend(b[2])
    if cur:
        out.append(cur)
    return out


def page_map(chapters):
    """PDF から各章の開始ページを拾う。見つからなければ 0。"""
    try:
        import fitz
    except ImportError:
        return {}
    p = os.path.join(VOL, "蘇生アルゴリズムの変遷と周術期心停止.pdf")
    if not os.path.exists(p):
        return {}
    doc = fitz.open(p)
    texts = []
    for pg_ in doc:
        t = pg_.get_text()
        # 目次のページ（リーダー点が並ぶ）は本文ではないので除く
        texts.append("" if t.count("...") > 3 else t)
    m = {}
    for ch in chapters:
        key = re.sub(r"\s+", "", ch["title"])
        for i, t in enumerate(texts):
            if not t:
                continue
            if re.sub(r"\s+", "", t).find(key[:14]) >= 0:
                m[ch["title"]] = i + 1
                break
    return m


# ------------------------------------------------------------ 一次資料
SRC_NOTE = {
    "00_テーマ別要約_蘇生・急変対応.docx":
        "収録ファイルを 6 テーマに整理した要約（2026-07-24 作成）",
    "CPR.2024ICU.山田.pdf":
        "ICU 版の院内 CPR 講義 52 枚。開心術後は再開胸／VA-ECMO まで",
    "CPR.2024HCU.山田.pptx":
        "HCU 版。開心術後のフローが「無効なら ICU へ移動」で終わる",
    "開心術後心停止.HCU.A4チャート.pptx":
        "ベッドサイド掲示用の 2 枚。本書 第27章で読み解いている",
    "Guideline for resuscitation in cardiac arrest after cardiac surgery.pdf":
        "EACTS 2009（Dunning ら, Eur J Cardiothorac Surg 2009;36:3-28）。"
        "本書 第24章の原典",
    "Hghlghts_2020ECCGuidelines_Japanese.pdf":
        "AHA 2020 ガイドライン ハイライト（日本語版）。本書 第8章",
    "カテ室急変対応トレーニング.pptx":
        "56 枚。鎮静の安全管理と急変対応。ASA-SED 2018 を下敷きにしている",
    "カテ室アナフィラキシーショックシナリオ①.docx":
        "ワークシート形式のシナリオ教材",
    "RRS_Basic_ver2.pptx": "RRS の基本。4 要素の説明",
    "RRSとは静岡病院.pptx": "当院向けの RRS 説明資料",
    "RRSとは何か.pdf": "RRS の概説",
    "RRS学会推奨.pptx": "学会推奨のまとめ",
    "RRTHandbook.pdf": "RRT 運用のハンドブック",
    "RRS_20100824.pdf": "初期の RRS 資料（2010 年）",
    "Nihon Kyukyu Igakukai Zasshi Journal of Japanese Association for "
    "Acute Medicine - 2017 - Tomotaka Koike - RRS .pdf":
        "日本救急医学会雑誌 2017 の RRS 総説",
    "米国 100k5M キャンペーンの Node とMentor病院の役割.pdf":
        "IHI の 10 万人／500 万人キャンペーン。RRS 普及の起点",
    "ICU RRS, コール表（案）2021,12.pdf": "起動基準のコール表（案）",
    "RRS記録用紙.pdf": "起動事例の記録様式",
    "聖マリRRS記録用紙　2018.7.4.xlsx": "他施設の記録様式",
    "症例1 RRSシナリオ.pdf": "訓練用シナリオ",
    "症例2 RRSシナリオ.pdf": "訓練用シナリオ",
    "カテ室急変対応トレーニングその1ICLS.pptx": "ICLS の内容",
    "手術室カテ室教育研修レジュメ.xlsx": "教育研修の年間レジュメ",
}
SRC_GROUP = {
    "RRS": "院内迅速対応システム",
    "院内急変対応コース": "院内急変対応コース",
}


def scan_sources():
    base = os.path.join(EDU, SRC.replace("/", os.sep))
    items = []
    if not os.path.isdir(base):
        return items
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith("~$")]
        for f in sorted(files):
            if f.startswith("~$") or f.lower().endswith((".jpg", ".jpeg",
                                                         ".png")):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, EDU).replace(os.sep, "/")
            sub = os.path.relpath(root, base).replace(os.sep, "/")
            grp = "蘇生・急変対応（直下）"
            if sub != ".":
                top = sub.split("/")[0]
                grp = SRC_GROUP.get(top, top)
            items.append({
                "name": f,
                "rel": rel,
                "grp": grp,
                "ext": os.path.splitext(f)[1].lower().lstrip("."),
                "size": os.path.getsize(full),
                "note": SRC_NOTE.get(f, ""),
            })
    return items


# ------------------------------------------------------------ 外部の一次文献
EXTERNAL = [
 ("AHA 2025 Part 1　Executive Summary",
  "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001372",
  "760 勧告の内訳、単一の救命の連鎖、用語の整理。本書 第9章"),
 ("AHA 2025 Part 4　Systems of Care",
  "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001378",
  "院内心停止の予防、早期警告システム、迅速対応チーム、safety huddle。第17章"),
 ("AHA 2025 Part 9　Adult Advanced Life Support",
  "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001376",
  "血管路・アドレナリン・多形性 VT・DSED・head-up CPR。第9章・第15章"),
 ("AHA 2025 Part 10　Special Circumstances",
  "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001380",
  "心臓手術後の心停止、カテ室、局所麻酔薬中毒、妊娠。第22〜24章"),
 ("AHA 2025 Part 11　Post-Cardiac Arrest Care",
  "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001375",
  "体温管理 32-37.5 ℃・36 時間以上、ミオクローヌス、予後予測"),
 ("Guidelines 2000 Part 1（歴史の総括）",
  "https://www.ahajournals.org/doi/10.1161/circ.102.suppl_1.I-1",
  "1966・1973・1979・1985・1992 年会議の一覧表。本書 第2〜4章"),
 ("AHA　History of CPR",
  "https://cpr.heart.org/en/resources/history-of-cpr",
  "1530 年代から現在までの年表。本書 第1章"),
 ("STS 専門家合意 2017（全文 PDF）",
  "https://www.annalsthoracicsurgery.org/article/S0003497516314825/pdf",
  "5 分以内の再開胸、10 日目まで、6 つの役割、5 点の器械。第22〜26章"),
 ("日本麻酔科学会　術中心停止に対するプラクティカルガイド",
  "https://anesth.or.jp/files/pdf/practical_guide_for_central_arrest_20211227.pdf",
  "2021 年 2 月 26 日制定。全 12 章。本書 第12〜14章の原典"),
 ("日本集中治療医学会　Rapid Response System 運用指針",
  "https://www.jsicm.org/news/upload/pub_com_RRS_JSICM_20240127.pdf",
  "2024 年 1 月 27 日。4 要素ごとの推奨。本書 第19章の原典"),
 ("JRC 蘇生ガイドライン 2025",
  "https://www.jrc-cpr.org/jrc-guideline-2025/",
  "2025 年 10 月 22 日オンライン版、2026 年 7 月 13 日書籍版。第10章"),
 ("ERC Guidelines 2025",
  "https://www.erc.edu/science-research/guidelines/guidelines-2025/",
  "2025 年 10 月 22 日ロッテルダムで公表"),
]

RELATED = [
 ("⑯ アナフィラキシーと局所麻酔薬中毒",
  "麻酔科ミニ教科書シリーズ/16_アナフィラキシーと局所麻酔薬中毒", "本書 第14章から参照"),
 ("⑰ 区域麻酔と脊髄幹麻酔",
  "麻酔科ミニ教科書シリーズ/17_区域麻酔と脊髄幹麻酔", "第13章 脊髄くも膜下麻酔関連心停止"),
 ("⑱ 呼吸管理と分離肺換気",
  "麻酔科ミニ教科書シリーズ/18_呼吸管理と分離肺換気", "第14章 呼吸の扱い"),
 ("⑲ 循環管理と循環作動薬",
  "麻酔科ミニ教科書シリーズ/19_循環管理と循環作動薬", "第14章 心機能低下"),
 ("⑳ 周術期の心停止と院内急変対応",
  "麻酔科ミニ教科書シリーズ/20_周術期の心停止と院内急変対応",
  "手を動かす順序はこちら。本書と対になる巻"),
 ("㉒ 常位胎盤早期剝離と産科危機的出血",
  "麻酔科ミニ教科書シリーズ/22_常位胎盤早期剝離と産科危機的出血", "母体の心停止"),
 ("周術期アナフィラキシー統合ガイド",
  "周術期アナフィラキシー", "5 資料統合の 127 頁"),
]


# ------------------------------------------------------------ HTML
CSS = """
:root{
  --bg:#f4f6f8; --card:#fff; --ink:#22303f; --grey:#6b7785; --navy:#1b2a49;
  --line:#dde2e8; --teal:#0f6d78; --blue:#2e6da4; --red:#c0392b;
  --green:#2e7d52; --orange:#d98e2b; --purple:#6b4fa0;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font-family:"Meiryo","Yu Gothic",system-ui,sans-serif;line-height:1.7}
header{background:var(--navy);color:#fff;padding:22px 26px 18px}
header h1{margin:0 0 4px;font-size:22px;letter-spacing:.02em}
header p{margin:0;color:#c6d0e0;font-size:13px}
.wrap{max-width:1180px;margin:0 auto;padding:0 18px 60px}
.searchbar{position:sticky;top:0;z-index:20;background:var(--bg);
 padding:14px 0 10px;border-bottom:1px solid var(--line)}
.searchbar input{width:100%;padding:13px 16px;font-size:16px;
 border:2px solid var(--navy);border-radius:10px;background:#fff;
 font-family:inherit}
.searchbar .hint{font-size:12px;color:var(--grey);margin-top:6px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 0}
.chip{border:1.6px solid var(--line);background:#fff;border-radius:999px;
 padding:6px 14px;font-size:13px;cursor:pointer;user-select:none}
.chip.on{background:var(--navy);color:#fff;border-color:var(--navy)}
h2.sec{font-size:17px;margin:30px 0 10px;padding-left:10px;
 border-left:5px solid var(--teal);color:var(--navy)}
.count{font-size:12px;color:var(--grey);font-weight:normal;margin-left:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));
 gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;
 padding:13px 15px}
.card .t{font-weight:bold;color:var(--navy);font-size:14px;margin-bottom:4px}
.card .m{font-size:11.5px;color:var(--grey);margin-bottom:6px}
.card .d{font-size:12.5px}
.card .subs{font-size:11.5px;color:var(--grey);margin-top:6px}
.card a{color:var(--blue);text-decoration:none}
.card a:hover{text-decoration:underline}
.tag{display:inline-block;font-size:10.5px;border-radius:4px;padding:1px 7px;
 margin-right:5px;color:#fff}
.t-I{background:var(--purple)} .t-II{background:var(--blue)}
.t-III{background:var(--green)} .t-IV{background:var(--red)}
.t-V{background:var(--orange)} .t-A{background:var(--grey)}
.ext{font-size:10.5px;border-radius:4px;padding:1px 7px;margin-right:5px;
 background:#eef1f6;color:var(--navy);border:1px solid var(--line)}
.figcard{background:#fff;border:1px solid var(--line);border-radius:10px;
 overflow:hidden}
.figcard img{width:100%;display:block;background:#fff}
.figcard .c{padding:8px 11px;font-size:12px}
.figgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
 gap:12px}
table{width:100%;border-collapse:collapse;background:#fff;font-size:12.5px}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;
 vertical-align:top}
th{background:#eef1f6;color:var(--navy)}
mark{background:#ffe9a8;padding:0 1px}
.empty{color:var(--grey);font-size:13px;padding:10px 2px}
footer{color:var(--grey);font-size:12px;margin-top:40px;
 border-top:1px solid var(--line);padding-top:14px}
.btnrow{margin:14px 0 0;display:flex;gap:10px;flex-wrap:wrap}
.btn{background:var(--teal);color:#fff;border-radius:8px;padding:9px 16px;
 font-size:13px;text-decoration:none;display:inline-block}
.btn.alt{background:var(--navy)}
@media (max-width:640px){.grid{grid-template-columns:1fr}}
"""

JS = r"""
const D = DATA;
const q = document.getElementById("q");
let mode = "all";

function esc(s){ return (s||"").replace(/[&<>"]/g, c =>
  ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }

function hit(txt, k){ return !k || (txt||"").toLowerCase().indexOf(k) >= 0; }

function hl(s, k){
  if(!k) return esc(s);
  const i = (s||"").toLowerCase().indexOf(k);
  if(i < 0) return esc(s);
  return esc(s.slice(0,i)) + "<mark>" + esc(s.slice(i,i+k.length)) + "</mark>"
       + esc(s.slice(i+k.length));
}

function snippet(txt, k){
  if(!k) return esc(txt.slice(0,110)) + (txt.length>110?"…":"");
  const i = txt.toLowerCase().indexOf(k);
  if(i < 0) return esc(txt.slice(0,110)) + (txt.length>110?"…":"");
  const a = Math.max(0, i-45), b = Math.min(txt.length, i+k.length+70);
  return (a>0?"…":"") + hl(txt.slice(a,b), k) + (b<txt.length?"…":"");
}

function partTag(p){
  const m = {"第 I 部":"I","第 II 部":"II","第 III 部":"III",
             "第 IV 部":"IV","第 V 部":"V","付録":"A"};
  for(const key in m){ if((p||"").indexOf(key)===0) return m[key]; }
  return "A";
}

function render(){
  const k = q.value.trim().toLowerCase();
  let n = 0;

  /* 章 */
  const ch = D.chapters.filter(c => mode==="all"||mode==="ch" ? hit(c.blob, k) : false);
  n += ch.length;
  document.getElementById("nCh").textContent = ch.length + " 章";
  document.getElementById("chBox").innerHTML = ch.length ? ch.map(c => {
    const tg = partTag(c.part);
    const pg = c.page ? ('<a href="' + D.pdf + '#page=' + c.page + '">PDF ' + c.page + ' 頁</a>') : "";
    return '<div class="card"><div class="t"><span class="tag t-'+tg+'">'+esc(c.part||"")+'</span>'
      + hl(c.title, k) + '</div>'
      + '<div class="m">' + (c.subs.length ? esc(c.subs.join("　/　")) : "") + '</div>'
      + '<div class="d">' + snippet(c.blob, k) + '</div>'
      + '<div class="subs">' + pg + (c.figs.length ? '　図 ' + c.figs.length + ' 点' : '') + '</div>'
      + '</div>';
  }).join("") : '<div class="empty">該当なし</div>';

  /* 図版 */
  const fg = D.figs.filter(f => mode==="all"||mode==="fig" ? hit(f.cap + " " + f.file + " " + f.ch, k) : false);
  n += fg.length;
  document.getElementById("nFig").textContent = fg.length + " 点";
  document.getElementById("figBox").innerHTML = fg.length ? fg.map(f =>
    '<a class="figcard" href="' + D.figdir + f.file + '" target="_blank">'
    + '<img loading="lazy" src="' + D.figdir + f.file + '">'
    + '<div class="c">' + hl(f.cap, k) + '<br><span style="color:#6b7785;font-size:11px">'
    + esc(f.ch) + '</span></div></a>').join("")
    : '<div class="empty">該当なし</div>';

  /* 一次資料 */
  const sr = D.sources.filter(s => mode==="all"||mode==="src" ? hit(s.name + " " + s.note + " " + s.grp, k) : false);
  n += sr.length;
  document.getElementById("nSrc").textContent = sr.length + " 件";
  document.getElementById("srcBox").innerHTML = sr.length ?
    '<table><thead><tr><th style="width:34%">ファイル</th><th style="width:14%">区分</th>'
    + '<th>内容</th><th style="width:8%">形式</th></tr></thead><tbody>'
    + sr.map(s => '<tr><td><a href="' + s.rel + '">' + hl(s.name, k) + '</a></td>'
      + '<td>' + hl(s.grp, k) + '</td><td>' + hl(s.note, k) + '</td>'
      + '<td>' + esc(s.ext) + '</td></tr>').join("") + '</tbody></table>'
    : '<div class="empty">該当なし</div>';

  /* 外部 */
  const ex = D.external.filter(e => mode==="all"||mode==="ext" ? hit(e[0] + " " + e[2], k) : false);
  n += ex.length;
  document.getElementById("nExt").textContent = ex.length + " 件";
  document.getElementById("extBox").innerHTML = ex.length ? ex.map(e =>
    '<div class="card"><div class="t"><a href="' + e[1] + '" target="_blank">'
    + hl(e[0], k) + '</a></div><div class="d">' + hl(e[2], k) + '</div></div>').join("")
    : '<div class="empty">該当なし</div>';

  /* 関連既刊 */
  const rl = D.related.filter(r => mode==="all"||mode==="rel" ? hit(r[0] + " " + r[2], k) : false);
  n += rl.length;
  document.getElementById("nRel").textContent = rl.length + " 件";
  document.getElementById("relBox").innerHTML = rl.length ? rl.map(r =>
    '<div class="card"><div class="t"><a href="' + r[1] + '">' + hl(r[0], k) + '</a></div>'
    + '<div class="d">' + hl(r[2], k) + '</div></div>').join("")
    : '<div class="empty">該当なし</div>';

  document.getElementById("total").textContent = k ? ("「" + q.value.trim() + "」に一致：" + n + " 件") : "";
  ["ch","fig","src","ext","rel"].forEach(function(id){
    const el = document.getElementById("sec_" + id);
    el.style.display = (mode==="all" || mode===id) ? "" : "none";
  });
}

q.addEventListener("input", render);
q.addEventListener("compositionend", render);
document.querySelectorAll(".chip").forEach(c => c.addEventListener("click", function(){
  document.querySelectorAll(".chip").forEach(x => x.classList.remove("on"));
  c.classList.add("on");
  mode = c.dataset.m;
  render();
}));
document.addEventListener("keydown", function(e){
  if(e.key === "/" && document.activeElement.tagName !== "INPUT"){
    e.preventDefault(); q.focus();
  }
});
render();
"""


def total_pages():
    try:
        import fitz
    except ImportError:
        return "—"
    p = os.path.join(VOL, "蘇生アルゴリズムの変遷と周術期心停止.pdf")
    return fitz.open(p).page_count if os.path.exists(p) else "—"


# ------------------------------------------------------------ 本体ポータル用
# 麻酔資料ポータル（_ポータル生成/2_ポータルを作る.py）が読み込む JSON。
# path はデスクトップ基準（本体ポータルの href() が "../" を付ける）。
GENDIR = os.path.join(EDU, "_ポータル生成")
JSON_OUT = os.path.join(GENDIR, "theme_resus.json")
BASE_PREFIX = "教育ファイル集/"


def theme_rows():
    chapters = build_chapters()
    pg = page_map(chapters)
    rows = []
    for c in chapters:
        page = pg.get(c["title"], 0)
        rows.append({
            "kind": "本文",
            "name": c["title"],
            "sub": "　/　".join(c["subs"]),
            "desc": "　".join(c["text"]),
            "path": BASE_PREFIX + PDF + ("#page=%d" % page if page else ""),
            "meta": (c["part"] or "本書の前置き")
                    + ("・PDF %d 頁" % page if page else ""),
        })
    for c in chapters:
        for f in c["figs"]:
            rows.append({
                "kind": "図版",
                "name": f["cap"],
                "sub": c["title"],
                "desc": c["title"] + "　" + f["cap"],
                "path": BASE_PREFIX + VOLDIR + "/図版/" + f["file"],
                "meta": c["title"],
            })
    for x in scan_sources():
        rows.append({
            "kind": "院内資料",
            "name": x["name"],
            "sub": x["grp"],
            "desc": x["note"],
            "path": BASE_PREFIX + x["rel"],
            "meta": x["grp"] + "・" + (x["ext"] or "-"),
        })
    for t, u, note in EXTERNAL:
        rows.append({"kind": "外部文献", "name": t, "sub": "", "desc": note,
                     "url": u, "meta": "外部リンク"})
    for t, rel, note in RELATED:
        rows.append({"kind": "関連既刊", "name": t, "sub": "", "desc": note,
                     "path": BASE_PREFIX + rel, "meta": "シリーズ内"})
    return rows


def write_json():
    rows = theme_rows()
    io.open(JSON_OUT, "w", encoding="utf-8").write(json.dumps(
        {"title": "蘇生・急変対応（テーマ別）",
         "note": "ミニ教科書㉖の本文・図版と、その一次資料を一括で検索します",
         "pdf": BASE_PREFIX + PDF,
         "rows": rows}, ensure_ascii=False))
    return rows


def main():
    chapters = build_chapters()
    pg = page_map(chapters)
    chs, figs = [], []
    for c in chapters:
        blob = "　".join(c["text"])
        chs.append({"title": c["title"], "part": c["part"],
                    "subs": c["subs"], "figs": [f["file"] for f in c["figs"]],
                    "page": pg.get(c["title"], 0), "blob": blob})
        for f in c["figs"]:
            figs.append({"file": f["file"], "cap": f["cap"],
                         "ch": c["title"]})

    data = {
        "pdf": PDF,
        "docx": DOCX,
        "figdir": VOLDIR + "/図版/",
        "chapters": chs,
        "figs": figs,
        "sources": scan_sources(),
        "external": EXTERNAL,
        "related": RELATED,
    }

    body = """<!DOCTYPE html>
<meta charset="utf-8">
<title>蘇生・急変対応ポータル</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>%(css)s</style>
<header>
  <h1>蘇生・急変対応ポータル</h1>
  <p>麻酔科ミニ教科書シリーズ ㉖『蘇生アルゴリズムの変遷と周術期心停止』と、
     その一次資料を一括で検索します</p>
</header>
<div class="wrap">
  <div class="btnrow">
    <a class="btn" href="%(pdf)s">教科書を開く（PDF・%(pages)s 頁）</a>
    <a class="btn alt" href="%(docx)s">Word 版</a>
    <a class="btn alt" href="麻酔資料ポータル.html">麻酔資料ポータル（全体）</a>
  </div>

  <div class="searchbar">
    <input id="q" placeholder="語を入れると、章の本文・図のキャプション・一次資料・外部文献を同時に探します（例：再開胸／MERIT／アドレナリン／2025）">
    <div class="hint">「/」キーで検索欄にジャンプ。<span id="total"></span></div>
    <div class="chips">
      <span class="chip on" data-m="all">すべて</span>
      <span class="chip" data-m="ch">本文（章）</span>
      <span class="chip" data-m="fig">図版</span>
      <span class="chip" data-m="src">院内の一次資料</span>
      <span class="chip" data-m="ext">外部の一次文献</span>
      <span class="chip" data-m="rel">関連する既刊</span>
    </div>
  </div>

  <section id="sec_ch">
    <h2 class="sec">本文（章）<span class="count" id="nCh"></span></h2>
    <div class="grid" id="chBox"></div>
  </section>

  <section id="sec_fig">
    <h2 class="sec">図版<span class="count" id="nFig"></span></h2>
    <div class="figgrid" id="figBox"></div>
  </section>

  <section id="sec_src">
    <h2 class="sec">院内の一次資料<span class="count" id="nSrc"></span></h2>
    <div id="srcBox"></div>
  </section>

  <section id="sec_ext">
    <h2 class="sec">外部の一次文献<span class="count" id="nExt"></span></h2>
    <div class="grid" id="extBox"></div>
  </section>

  <section id="sec_rel">
    <h2 class="sec">関連する既刊<span class="count" id="nRel"></span></h2>
    <div class="grid" id="relBox"></div>
  </section>

  <footer>
    このページは 教育ファイル集 の直下に置いてあります。
    リンクはすべて相対パスなので、教育ファイル集ごと移動しても動きます。<br>
    作り直すときは <span style="font-family:monospace">麻酔科ミニ教科書シリーズ\\26_…\\_生成スクリプト\\portal26.py</span> を実行してください。
  </footer>
</div>
<script>const DATA = %(json)s;</script>
<script>%(js)s</script>
""" % {"css": CSS, "js": JS,
       "json": json.dumps(data, ensure_ascii=False),
       "pdf": PDF, "docx": DOCX,
       "pages": total_pages()}

    io.open(OUT, "w", encoding="utf-8").write(body)
    return len(chs), len(figs), len(data["sources"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    rows = write_json()
    print("本体ポータル用 JSON:", len(rows), "行 →", JSON_OUT)
    # 単独の HTML は作らない（2026-09-17、本体ポータルの SEC-04 に一本化）。
    # どうしてもこのテーマだけのページが要るときだけ --html を付ける。
    if "--html" in sys.argv:
        print("単独ポータル 章/図/一次資料 =", main())
        print("→", OUT)
