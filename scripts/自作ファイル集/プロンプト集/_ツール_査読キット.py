# -*- coding: utf-8 -*-
"""Genspark 用の査読キット（コピーボタン付き HTML）を作る。

使い方: python _ツール_査読キット.py <教材フォルダ> <医学|経営学> <題名>
  教材フォルダに 教材1_….txt 〜 教材N_….txt を置いておく。
  規約とジョブは 24_Gensparkに連続ジョブを流す.md から読み込む（md を直せばキットも変わる）。
出力: <教材フォルダ>/査読キット_<題名>.html と 最初に貼る全文.txt
"""
import glob
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "24_Gensparkに連続ジョブを流す.md")


def load_parts(jobset):
    md = open(MD, encoding="utf-8").read()
    common = re.search(r"## 2\..*?```\n(.*?)```", md, re.S).group(1).strip()
    head = {"医学": "### 医学教材用", "経営学": "### 経営学教材用"}[jobset]
    jobs = re.search(re.escape(head) + r".*?```\n(.*?)```", md, re.S).group(1).strip()
    return common, jobs


def card(i, title, body, note=""):
    rows = 3 if len(body) < 200 else 10
    return (f'<section class="card"><div class="hd"><h2>{html.escape(title)}</h2>'
            f'<button onclick="cp({i},this)">コピー</button></div>'
            f'<p class="note">{html.escape(note)}</p>'
            f'<textarea id="t{i}" readonly rows="{rows}">{html.escape(body)}</textarea></section>')


def main():
    folder, jobset, title = sys.argv[1], sys.argv[2], sys.argv[3]
    common, jobs = load_parts(jobset)
    files = sorted(glob.glob(os.path.join(folder, "教材*_*.txt")),
                   key=lambda p: int(re.search(r"教材(\d+)", os.path.basename(p)).group(1)))
    n = len(files)
    texts = [open(f, encoding="utf-8").read().strip() for f in files]
    names = [os.path.basename(f)[:-4] for f in files]
    listing = f"【教材一覧】全{n}本。返信は教材ごとに1回、最後にジョブZで1回（合計{n + 1}回）\n" + \
        "\n".join(f"【教材{i}】{re.sub(r'^教材\d+_', '', s)}" for i, s in enumerate(names, 1))
    rule = common + "\n\n■ ジョブ（1回の返信でこの順に全部）\n" + jobs
    full = rule + "\n\n" + listing + "\n\nでは、ここから本文です。教材1から始めてください。\n\n" + "\n\n".join(texts)
    open(os.path.join(folder, "最初に貼る全文.txt"), "w", encoding="utf-8").write(full)

    items = [
        ("① 最初に1回だけ貼る（規約＋全教材）", full, f"{len(full):,}字。入力欄に入りきらなければ、いちばん下の分割版へ。"),
        ("② 通常はこれだけ送る", "次", f"「▶ 次は…」が出たら送る。全部で {n} 回。"),
        ("③ 返信が途中で切れたとき", "続き", "表が閉じていない、最後の「▶ 次は…」がない、ときに。"),
        ("④ 教材の番号がずれたとき", "規約を読み直してください。教材 k から再開してください。", "k を正しい番号に書き換えて送る。"),
        ("⑤ 引用が崩れてきたとき", "規約の「引用は一字一句そのまま」を守ってください。直前の教材をやり直してください。", ""),
        ("⑥ ジョブが1つ抜けているとき", "ジョブ○が抜けています。教材 k のジョブ○だけを出してください。", "○と k を書き換えて送る。"),
    ]
    alt = [("分割版：1回目（規約＋教材1）",
            rule + "\n\n" + listing + "\n\n本文は1本ずつ渡します。まず教材1です。\n\n" + texts[0],
            "この場合、教材1の返信が終わったら「次」の代わりに下の教材2を貼る。以降も同じ。")]
    for i, t in enumerate(texts[1:], 2):
        alt.append((f"分割版：{names[i - 1]}", f"次の教材です。同じ規約で続けてください。\n\n{t}", ""))
    alt.append(("分割版：最後（ジョブZ）", "全教材が終わりました。ジョブZを行ってください。", ""))

    rows = "".join(f"<tr><td>{i}</td><td>{html.escape(re.sub(r'^教材\d+_', '', s))}</td></tr>"
                   for i, s in enumerate(names, 1))
    page = TEMPLATE.format(
        title=html.escape(title), n=n, n1=n + 1, rows=rows,
        cards="".join(card(i, *x) for i, x in enumerate(items)),
        cards2="".join(card(100 + i, *x) for i, x in enumerate(alt)))
    out = os.path.join(folder, f"査読キット_{title}.html")
    open(out, "w", encoding="utf-8").write(page)
    print(out, len(full))


TEMPLATE = """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>査読キット {title}</title><style>
:root{{--bg:#f6f5f2;--card:#fff;--ink:#222;--sub:#666;--ac:#2f5d7c;--line:#ddd}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1b1c1e;--card:#26282b;--ink:#eee;--sub:#aaa;--ac:#7fb3d5;--line:#3a3c40}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:"Yu Gothic UI","Meiryo",sans-serif;line-height:1.7}}
main{{max-width:900px;margin:0 auto;padding:24px 16px 60px}}h1{{font-size:1.35rem;margin:.2em 0}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:14px 0}}
.hd{{display:flex;justify-content:space-between;align-items:center;gap:12px}}h2{{font-size:1.02rem;margin:0}}
button{{background:var(--ac);color:#fff;border:0;border-radius:6px;padding:8px 18px;font-size:.95rem;cursor:pointer;white-space:nowrap}}
button.ok{{background:#3c8c5a}}textarea{{width:100%;box-sizing:border-box;font:13px/1.5 Consolas,"MS Gothic",monospace;
background:transparent;color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:8px}}
.note{{color:var(--sub);font-size:.88rem;margin:.3em 0}}details{{margin-top:24px}}summary{{cursor:pointer;font-weight:bold}}
table{{border-collapse:collapse;font-size:.9rem}}td,th{{border:1px solid var(--line);padding:4px 10px}}</style></head>
<body><main><h1>Genspark 査読キット　{title}</h1>
<p class="note">プロンプト集 24番（第2版：1回の返信で教材1本ぶん）から自動生成</p>
<section class="card"><h2>手順</h2><ol>
<li>Genspark を <b>AI Chat モード</b>で開く。開始時刻とクレジット残高をメモ。</li>
<li>①をコピーして貼り、送信。教材1の全ジョブがまとめて返ってくる。</li>
<li>返信の最後に「▶ 次は…」が出たら ②「次」を送る（全 {n} 回。最後の返信はジョブZ）。合計 {n1} 回の返信で終わる。</li>
<li>困ったら ③〜⑥。</li>
<li>終わったら会話の<b>共有リンク</b>をくろたんへ。「次」「続き」を何回送ったかも一緒に。</li></ol>
<table><tr><th>返信</th><th>教材</th></tr>{rows}<tr><td>最後</td><td>ジョブZ（全体を通した食い違い）</td></tr></table></section>
{cards}
<details><summary>①が入力欄に入りきらないとき（分割版）</summary>{cards2}</details>
</main><script>
function cp(i,b){{var t=document.getElementById('t'+i);var done=function(){{b.textContent='コピーしました';b.className='ok';
setTimeout(function(){{b.textContent='コピー';b.className=''}},1800)}};
if(navigator.clipboard){{navigator.clipboard.writeText(t.value).then(done,function(){{t.select();document.execCommand('copy');done()}})}}
else{{t.select();document.execCommand('copy');done()}}}}
</script></body></html>"""

if __name__ == "__main__":
    main()
