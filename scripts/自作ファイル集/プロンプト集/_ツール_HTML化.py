# -*- coding: utf-8 -*-
"""プロンプト集の .md を1枚の HTML にまとめる。

使い方: このフォルダで  python _ツール_HTML化.py
出力  : プロンプト集.html （ダブルクリックでブラウザが開く）
.md を書き換えたら、もう一度これを実行すれば作り直される。
"""
import io
import os
import re
import glob
import json
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "プロンプト集.html")


# ---------------- 簡易 Markdown → HTML ----------------

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def flush_para(buf, out):
    if buf:
        out.append("<p>" + "<br>".join(inline(x) for x in buf) + "</p>")
        del buf[:]


def flush_list(items, kind, out):
    if items:
        tag = "ol" if kind == "ol" else "ul"
        out.append("<" + tag + ">" + "".join("<li>" + inline(x) + "</li>" for x in items) + "</" + tag + ">")
        del items[:]


def flush_table(rows, out):
    if not rows:
        return
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    body = cells[:]
    head = None
    if len(cells) >= 2 and all(re.match(r"^:?-{2,}:?$", c) for c in cells[1] if c):
        head = cells[0]
        body = cells[2:]
    h = ""
    if head:
        h = "<thead><tr>" + "".join("<th>" + inline(c) + "</th>" for c in head) + "</tr></thead>"
    b = "<tbody>" + "".join(
        "<tr>" + "".join("<td>" + inline(c) + "</td>" for c in r) + "</tr>" for r in body) + "</tbody>"
    out.append('<div class="tw"><table>' + h + b + "</table></div>")
    del rows[:]


def md2html(text):
    out = []
    para = []
    items = []
    kind = None
    table = []
    code = []
    in_code = False
    lang = ""

    for raw in text.split("\n"):
        line = raw.rstrip("\r")

        if line.strip().startswith("```"):
            if in_code:
                out.append('<div class="cb"><button class="cp">コピー</button><pre><code>'
                           + esc("\n".join(code)) + "</code></pre></div>")
                del code[:]
                in_code = False
                lang = ""
            else:
                flush_para(para, out)
                flush_list(items, kind, out)
                flush_table(table, out)
                in_code = True
                lang = line.strip()[3:]
            continue
        if in_code:
            code.append(line)
            continue

        st = line.strip()

        if st.startswith("|") and st.endswith("|") and st.count("|") >= 2:
            flush_para(para, out)
            flush_list(items, kind, out)
            table.append(st)
            continue
        flush_table(table, out)

        if not st:
            flush_para(para, out)
            flush_list(items, kind, out)
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", st)
        if m:
            flush_para(para, out)
            flush_list(items, kind, out)
            lv = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lv, inline(m.group(2)), lv))
            continue

        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", st):
            flush_para(para, out)
            flush_list(items, kind, out)
            out.append("<hr>")
            continue

        m = re.match(r"^[-*+]\s+(.*)$", st)
        if m:
            flush_para(para, out)
            if kind != "ul":
                flush_list(items, kind, out)
                kind = "ul"
            items.append(m.group(1))
            continue

        m = re.match(r"^(\d+)[.)]\s+(.*)$", st)
        if m:
            flush_para(para, out)
            if kind != "ol":
                flush_list(items, kind, out)
                kind = "ol"
            items.append(m.group(2))
            continue

        if st.startswith(">"):
            flush_para(para, out)
            flush_list(items, kind, out)
            out.append("<blockquote>" + inline(st.lstrip("> ").rstrip()) + "</blockquote>")
            continue

        flush_list(items, kind, out)
        para.append(st)

    if in_code and code:
        out.append('<div class="cb"><button class="cp">コピー</button><pre><code>'
                   + esc("\n".join(code)) + "</code></pre></div>")
    flush_para(para, out)
    flush_list(items, kind, out)
    flush_table(table, out)
    return "\n".join(out)


# ---------------- ここから組み立て ----------------

def _key(path):
    b = os.path.basename(path)
    m = re.match(r"^(\d+)", b)
    return (int(m.group(1)) if m else 999, b)


files = sorted(glob.glob(os.path.join(HERE, "*.md")), key=_key)
docs = []
for p in files:
    name = os.path.splitext(os.path.basename(p))[0]
    with io.open(p, "r", encoding="utf-8") as f:
        raw = f.read()
    docs.append({"id": "d%d" % len(docs), "name": name, "html": md2html(raw),
                 "text": re.sub(r"\s+", " ", raw)})

# 目次に載せる xlsx も拾う（本文は持たないが、場所が分かるように）
xlsx = sorted(os.path.basename(p) for p in glob.glob(os.path.join(HERE, "*.xlsx")))

nav = []
for d in docs:
    nav.append('<a class="nv" data-id="%s" href="#%s">%s</a>' % (d["id"], d["id"], esc(d["name"])))
nav_html = "\n".join(nav)

xnav = "".join('<div class="xl">%s</div>' % esc(x) for x in xlsx)

secs = []
for d in docs:
    body = d["html"]
    if d["name"].startswith("00_"):
        body = body.replace('<button class="cp">コピー</button>', "")
        body = ('<div class="note">このページは<b>読むための早見表</b>です。'
                'Gensparkに貼るものはありません。貼る枠は左の目次から各ファイルを開いてください。</div>') + body
    secs.append('<section id="%s" class="doc">%s</section>' % (d["id"], body))
secs_html = "\n".join(secs)

index = json.dumps([{"id": d["id"], "name": d["name"], "text": d["text"]} for d in docs],
                   ensure_ascii=False)

today = datetime.date.today().strftime("%Y年%-m月%-d日") if os.name != "nt" else \
    datetime.date.today().strftime("%Y年%m月%d日").replace("年0", "年").replace("月0", "月")

CSS = """
:root{--navy:#0A1830;--teal:#407A8A;--gray:#555A6E;--line:#DCE3E8;--bg:#FFFFFF;--side:#F4F7F9;}
*{box-sizing:border-box;}
body{margin:0;font-family:"游ゴシック","Yu Gothic",Meiryo,sans-serif;color:#223037;background:var(--bg);}
#wrap{display:flex;min-height:100vh;}
#side{width:310px;flex:0 0 310px;background:var(--side);border-right:1px solid var(--line);
      padding:18px 14px;position:sticky;top:0;height:100vh;overflow-y:auto;}
#side h1{font-size:15px;color:var(--navy);margin:0 0 4px;}
#side .sub{font-size:11px;color:var(--gray);margin-bottom:14px;}
#q{width:100%;padding:7px 9px;border:1px solid var(--line);border-radius:6px;font-size:13px;
   margin-bottom:12px;font-family:inherit;}
a.nv{display:block;padding:7px 9px;margin-bottom:2px;border-radius:6px;text-decoration:none;
     color:#223037;font-size:12.5px;line-height:1.45;border-left:3px solid transparent;}
a.nv:hover{background:#E6EDF1;}
a.nv.on{background:#fff;border-left-color:var(--teal);color:var(--navy);font-weight:700;
        box-shadow:0 1px 3px rgba(0,0,0,.06);}
.xlh{font-size:11px;color:var(--gray);margin:16px 0 6px;border-top:1px solid var(--line);padding-top:12px;}
.xl{font-size:12px;color:var(--gray);padding:4px 9px;}
#main{flex:1;min-width:0;padding:34px 46px 90px;max-width:1000px;}
.doc{display:none;}
.doc.on{display:block;}
h1,h2,h3,h4{color:var(--navy);line-height:1.4;}
h1{font-size:24px;border-bottom:2px solid var(--teal);padding-bottom:10px;margin:0 0 20px;}
h2{font-size:18px;margin:34px 0 12px;border-left:5px solid var(--teal);padding-left:11px;}
h3{font-size:15px;margin:24px 0 8px;color:var(--teal);}
p{line-height:1.85;font-size:14px;margin:10px 0;}
li{line-height:1.8;font-size:14px;margin:4px 0;}
code{background:#EEF3F6;padding:1px 5px;border-radius:4px;font-size:12.5px;
     font-family:Consolas,"ＭＳ ゴシック",monospace;color:#0A1830;}
strong{color:var(--navy);}
a{color:var(--teal);}
hr{border:0;border-top:1px solid var(--line);margin:28px 0;}
blockquote{border-left:4px solid var(--line);margin:12px 0;padding:4px 14px;color:var(--gray);font-size:13.5px;}
.tw{overflow-x:auto;margin:14px 0;}
table{border-collapse:collapse;font-size:13px;width:100%;}
th{background:var(--navy);color:#fff;padding:8px 10px;text-align:left;font-weight:600;
   border:1px solid var(--navy);white-space:nowrap;}
td{border:1px solid var(--line);padding:7px 10px;vertical-align:top;line-height:1.7;}
tbody tr:nth-child(even){background:#F8FAFB;}
.cb{position:relative;margin:14px 0;}
.cb pre{background:#F4F7F9;border:1px solid var(--line);border-left:4px solid var(--teal);
        border-radius:6px;padding:14px 16px;overflow-x:auto;margin:0;}
.cb code{background:none;padding:0;font-size:12.5px;line-height:1.75;display:block;
         white-space:pre;color:#1B2A33;}
.cp{position:absolute;top:8px;right:8px;background:var(--teal);color:#fff;border:0;
    border-radius:5px;padding:5px 12px;font-size:11.5px;cursor:pointer;font-family:inherit;opacity:.85;}
.cp:hover{opacity:1;}
.cp.done{background:#2E7D5B;}
.note{background:#FFF6E0;border:1px solid #E8D9A8;border-left:5px solid #D9A72C;
      border-radius:6px;padding:11px 14px;font-size:13px;line-height:1.7;margin:0 0 22px;color:#5A4A1E;}
#hint{font-size:11.5px;color:var(--gray);margin-top:18px;line-height:1.7;}
@media (max-width:1000px){#side{width:230px;flex:0 0 230px;}#main{padding:24px 20px 80px;}}
@media print{#side{display:none;} #main{max-width:none;} .doc{display:block!important;}}
"""

JS = """
var DOCS = __INDEX__;
var navs = document.querySelectorAll('a.nv');
var secs = document.querySelectorAll('section.doc');

function show(id){
  for(var i=0;i<secs.length;i++){ secs[i].className = (secs[i].id===id)?'doc on':'doc'; }
  for(var j=0;j<navs.length;j++){
    navs[j].className = (navs[j].getAttribute('data-id')===id)?'nv on':'nv';
  }
  window.scrollTo(0,0);
  try{ localStorage.setItem('pk_last', id); }catch(e){}
}
for(var k=0;k<navs.length;k++){
  navs[k].addEventListener('click', function(e){ e.preventDefault(); show(this.getAttribute('data-id')); });
}

var q = document.getElementById('q');
q.addEventListener('input', function(){
  var v = this.value.trim().toLowerCase();
  for(var i=0;i<DOCS.length;i++){
    var hit = !v || DOCS[i].name.toLowerCase().indexOf(v)>=0 || DOCS[i].text.toLowerCase().indexOf(v)>=0;
    var el = document.querySelector('a.nv[data-id="'+DOCS[i].id+'"]');
    if(el) el.style.display = hit ? 'block' : 'none';
  }
});

document.addEventListener('click', function(e){
  if(e.target && e.target.className.indexOf('cp')>=0){
    var pre = e.target.parentNode.querySelector('code');
    var t = pre.innerText;
    var ok = function(){ e.target.textContent='コピーしました'; e.target.className='cp done';
      setTimeout(function(){ e.target.textContent='コピー'; e.target.className='cp'; },1400); };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(t).then(ok, function(){ fallback(t, ok); });
    } else { fallback(t, ok); }
  }
});
function fallback(t, ok){
  var ta=document.createElement('textarea'); ta.value=t;
  ta.style.position='fixed'; ta.style.opacity='0';
  document.body.appendChild(ta); ta.select();
  try{ document.execCommand('copy'); ok(); }catch(e){ alert('コピーできませんでした。手で選択してください。'); }
  document.body.removeChild(ta);
}

var hash = (location.hash || '').replace('#','');
var last = null;
try{ last = localStorage.getItem('pk_last'); }catch(e){}
var first = navs.length ? navs[0].getAttribute('data-id') : null;
if(hash && document.getElementById(hash)){ show(hash); }
else if(last && document.getElementById(last)){ show(last); }
else if(first){ show(first); }
"""

JS = JS.replace("__INDEX__", index)

html = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>プロンプト集</title>
<style>""" + CSS + """</style>
</head>
<body>
<div id="wrap">
  <nav id="side">
    <h1>プロンプト集</h1>
    <div class="sub">自作ファイル集 &gt; プロンプト集<br>""" + today + """ 時点／""" + str(len(docs)) + """件</div>
    <input id="q" type="search" placeholder="本文もまとめて検索">
""" + nav_html + """
    <div class="xlh">Excelのファイル（別途開いてください）</div>
""" + xnav + """
    <div id="hint">コードの枠は右上の「コピー」で丸ごと取れます。<br>
    .md を直したら <code>_ツール_HTML化.py</code> を実行し直してください。</div>
  </nav>
  <main id="main">
""" + secs_html + """
  </main>
</div>
<script>""" + JS + """</script>
</body>
</html>
"""

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("saved:", OUT)
print("docs :", len(docs), "files /", len(html), "chars")
