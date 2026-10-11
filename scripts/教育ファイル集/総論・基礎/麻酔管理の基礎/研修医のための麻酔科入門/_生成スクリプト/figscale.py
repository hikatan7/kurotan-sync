# -*- coding: utf-8 -*-
"""図（SVG）ごとに、文字を大きくしても崩れない最大の倍率を Chrome で実測して figscale.json に書く。
崩れ＝①文字が viewBox の外へ出る ②文字どうしが重なる ③文字が自分を囲む枠からはみ出す。
倍率 1.0 のときの件数を基準に、それより増えない最大の倍率を選ぶ。"""
import os, sys, re, json, subprocess, importlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import front, svglib
from engine import Book

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
MODS = ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8"]
JS = r"""
<script>
window.addEventListener('load', function(){
  var out = {};
  document.querySelectorAll('svg[data-fig]').forEach(function(sv){
    var vb = sv.viewBox.baseVal, n = 0;
    var ts = Array.from(sv.querySelectorAll('text')).filter(function(t){return t.textContent.trim();});
    var bx = ts.map(function(t){ var b=t.getBBox(); return [b.x,b.y,b.x+b.width,b.y+b.height]; });
    var rs = Array.from(sv.querySelectorAll('rect')).map(function(r){ var b=r.getBBox(); return [b.x,b.y,b.x+b.width,b.y+b.height]; })
             .filter(function(r){ return (r[2]-r[0]) < vb.width*0.98 || (r[3]-r[1]) < vb.height*0.98; });
    bx.forEach(function(a){
      if (a[0] < vb.x-1 || a[2] > vb.x+vb.width+1 || a[1] < vb.y-1 || a[3] > vb.y+vb.height+1) n++;
      var cx=(a[0]+a[2])/2, cy=(a[1]+a[3])/2, best=null, area=1e18;
      rs.forEach(function(r){ if (cx>r[0]&&cx<r[2]&&cy>r[1]&&cy<r[3]) { var ar=(r[2]-r[0])*(r[3]-r[1]); if (ar<area){area=ar;best=r;} } });
      if (best && (a[0] < best[0]-1 || a[2] > best[2]+1)) n++;
    });
    for (var i=0;i<bx.length;i++) for (var j=i+1;j<bx.length;j++){
      var a=bx[i], b=bx[j];
      var vo=Math.min(a[3],b[3])-Math.max(a[1],b[1]), ho=Math.min(a[2],b[2])-Math.max(a[0],b[0]);
      var hm=Math.min(a[3]-a[1], b[3]-b[1]);
      if (vo > 0.3*hm && ho > 2) n++;
    }
    out[sv.getAttribute('data-fig')] = n;
  });
  var p=document.createElement('pre'); p.id='figres'; p.textContent=JSON.stringify(out); document.body.appendChild(p);
});
</script>
"""


def measure(k):
    os.environ["FIGSCALE_ALL"] = str(k)
    svglib._FS["n"] = 0
    importlib.reload(front)
    b = Book()
    b.add(front.cover(), "cover")
    b.add(front.toc())
    for m in MODS:
        mod = importlib.import_module(m)
        importlib.reload(mod)
        mod.build(b)
    html = b.render("check").replace("</body>", JS + "</body>")
    p = os.path.join(HERE, "_check.html")
    open(p, "w", encoding="utf-8").write(html)
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=8000", "--dump-dom",
                        "file:///" + p.replace("\\", "/")], capture_output=True, timeout=240)
    dom = r.stdout.decode("utf-8", "replace")
    m = re.search(r'<pre id="figres">(.*?)</pre>', dom, re.S)
    return json.loads(m.group(1).replace("&quot;", '"'))


KS = [1.0, 1.1, 1.2, 1.3]
res = {k: measure(k) for k in KS}
base = res[1.0]
choice = {}
for f in base:
    best = 1.0
    for k in KS[1:]:
        if res[k].get(f, 99) <= base[f]:
            best = k
        else:
            break
    choice[f] = best
del os.environ["FIGSCALE_ALL"]
json.dump(choice, open(os.path.join(HERE, "figscale.json"), "w", encoding="utf-8"), indent=0)
from collections import Counter
print("figs", len(base), Counter(choice.values()))
print("base issues", {f: n for f, n in base.items() if n})
