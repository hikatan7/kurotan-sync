---
name: workflow-figure-text-fit
description: matplotlib 図版の「枠から文字がはみ出す」を構造的に防ぐ figlib と、既存図の一括点検・差し替え手順
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 80bf980a-acfc-472a-94b0-61f197aea489
  modified: 2026-09-03T02:47:49.523Z
---

ミニ教科書シリーズの図版129点を点検し、44点が枠外はみ出し・重なりで作り直しになった（2026-09-03）。
**原因は共通で「テキスト幅を測らずに固定座標で枠を描いていた」こと。**

**Why**：matplotlib はテキストをクリップしないので、枠より長い文字列は黙って外へ流れる。
サイズを目で決めていると、文字数が増えた図だけが静かに壊れる。

**How to apply**：`figlib.py`（scratchpad と `13_気道管理\_生成スクリプト`）を使う。
- 座標は**ピクセル**（`ax.set_xlim(0,W); ax.set_ylim(H,0)`、figsize=W/200×H/200, dpi=200）
- `cv.measure()` が `get_window_extent` で実測 → `fit_size()` で枠に収まる最大の pt を返す
- **行送りは `LH(size, k)=size*dpi/72*k`**。pt をそのまま px として掛けると行が重なる（実際にやらかした）
- `wrap()` は英数字・単位を1トークン扱いにして「5 万/µL 維／持」のような語中改行を防ぐ
- 枠の高さは行数から逆算（`textbox()`）。先に枠を決めない

**フォント**：既刊①②③⑪⑫は `["DejaVu Sans","Yu Gothic"]`、⑦は `["Noto Sans JP","Yu Gothic","DejaVu Sans"]`。
Noto Sans JP は ₂ や ≧ を持たないので**必ずフォールバックを足す**（CO₂ が豆腐になる）。

**点検の自動化は2段構え**。マージン検査だけでは足りない（2026-09-04に判明）。
1. **キャンバス端**：全PNGで「非白画素の上下左右マージン」を測り、12px 未満なら要確認。
2. **枠の内側**：`boxaudit.py`（`14_血管確保\_生成スクリプト`）で `Canvas.box/rect/text` を
   差し替えて描画座標を記録し、**「文字の中心がある枠の中にあるのに、文字がその枠から出ている」**
   ものを列挙する。①は canvas の縁しか見ないので、枠から溢れて隣の枠にかぶるものを取り逃す。
   ⑭で28件、既刊でも⑬に2種・①に1種の残りが見つかった。
   使い方 `python boxaudit.py <出力先> <図版スクリプト...>` → `qa14/overflow.txt` に
   ファイル名・はみ出し量・方向・該当文字列が出る。**0件になるまで直す。**
   ※ 図版スクリプトの末尾の `for fn in (...)` に描画しない関数が残っていると、
   作り直した図の**旧版が同じ PNG 名に上書き**されて検出が混乱する。旧関数は必ずループから外す。

**差し替え手順**：①元と**同一ピクセル寸法**で作り直す（docx の extent を触らずに済む）
②`図版\_修正前` へ退避 ③docx/pptx は `word/media`・`ppt/media` を md5 で突き合わせて入れ替え
④Word/PowerPoint COM で PDF を再出力 ⑤最後に「旧版が残っていないか」を md5 で全数照合。
OneDrive 配下なので操作は [[env-onedrive-desktop-file-ops]] に従う。

関連：[[project-anesthesia-minitextbook-series]] [[project-pptxlib-slide-engine]]
