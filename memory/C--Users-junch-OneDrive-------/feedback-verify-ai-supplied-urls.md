---
name: feedback-verify-ai-supplied-urls
description: 他AIが提示した画像URL・出典URL・数値は捏造前提で実在検証してから使う
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8e450de3-9567-4fcf-be37-752073f03196
  modified: 2026-08-26T06:04:26.584Z
---

他AI（Gemini/Genspark等）が提示したURLや数値は、そのまま使わず必ず実在検証する。2026-08-26のダッシュボード案件では、Geminiが提示したWikipedia病院画像URL **12本すべてが実在しないファイル名**で、これが「画像が貼れない」の真因だった（プロキシ経由やBase64化を試しても無駄）。同様に順天堂静岡の「242例/705例」も出典不明だった。

**Why:** 生成AIはURLをパターンから合成するため、それらしいが存在しないURLを作る。下流で何度プロンプトを書き直しても直らず、クレジットと時間を溶かす。

**How to apply:**
- 画像は Wikimedia Commons API（`action=query&list=search&srnamespace=6`）で実ファイル名を検索 → `imageinfo` で thumburl とライセンス取得 → ダウンロードして目視確認。
- URL生死は `curl -o /dev/null -w "%{http_code}"`。upload.wikimedia.org は連続アクセスで429になるのでAPI経由＋sleepを挟む。
- 数値は一次情報（病院公式ページ、学会名簿PDF）で裏取りし、取れないものは「未確認」と資料に明示する。断定しない。
- 座標も同様。AI提示の緯度経度はズレる。Nominatim で geocode する。

**病院サイトの年度別ページは必ず一覧ページから辿る（2026-08-29に実害）:** 藤枝市立総合病院の令和6年度病院指標を「未公表」と誤記した。原因は、検索結果から令和5年度の個別ページ(24049.html)に直行し、そのページに翌年度へのリンクが無いことを「令和6年度は未公表」と解釈したこと。実際には親ディレクトリ `/about/statistics/sihyou/` の一覧に令和6年度(26073.html)が先頭で載っていた。検索エンジンにも未収載だったため検索でも出ない。
**How to apply:** 年度もの（病院指標・年報・統計）は必ずセクションの一覧ページを開いて年度リンクを列挙する。個別ページの「リンクが無い」を根拠に非公表と断定しない。WebFetchが弾かれるドメインでもブラウザなら開けることがある。
**同時に判明した転記ミス:** 聖隷浜松の肺葉切除を99例と記載していたが正しくは61例。**取得した数値は必ず原典画面と1件ずつ突き合わせる**こと。7施設中2施設で誤りがあった。

関連: [[project-shizuoka-robot-dashboard]] [[workflow-cross-site-search]]
