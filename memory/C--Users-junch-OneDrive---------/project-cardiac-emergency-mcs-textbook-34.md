---
name: project-cardiac-emergency-mcs-textbook-34
description: ミニ教科書㉞『心臓麻酔の緊急と補助循環』49頁・全24章＋専攻医版ちょうど10頁。心臓麻酔補完リストの1番目
metadata: 
  node_type: memory
  type: project
  originSessionId: b1b32ccc-9630-41e9-b3f7-0c43af361005
  modified: 2026-09-22T05:22:35.412Z
---

`教育ファイル集\麻酔科ミニ教科書シリーズ\34_心臓麻酔の緊急と補助循環\`（2026-09-22）。
ユーザーの「おススメの順で心臓麻酔に必要な項目を補完していって」への1番目。

**構成**：本編49頁・全24章・図版12点（全て自作）・コラム9本・番号引用37件
＋専攻医版**ちょうど10頁**（図4点・引用32件、本編とは別採番）。
- 第I部 急性大動脈解離（1-5）／第II部 術中・術後の急変（6-9）
- 第III部 補助循環（10-18：何のために入れるのか／SCAI／IABP／VA-ECMO／
  微小軸流ポンプ／麻酔管理／LVAD／右心不全／ECPR）
- 第IV部 離脱できないとき（19-21）／第V部 支える（22-24）／付録A〜E

**貫く軸**：「効くのは知識より、あらかじめ決めておいた順番」。
装置の章では「強力な装置ほど、それ自体が問題を作る」（VA-ECMO は流量を足すが
左室後負荷を上げる）。装置を選ぶ前に **流量・心筋仕事・ガス交換のどれを足したいか**
を言葉にする、で統一した。

**歴史コラムに使った一次文献（PubMed で実在確認済み）**
Moulopoulos 1962（14476645、拡張期バルーンの発想）／Kantrowitz 1968（5694059、IABP 初の臨床）／
Hill 1972（5060491、体外循環が手術室を出た日）／Bartlett 1976（951895、新生児 ECMO）。
ECPR 三試験は ARREST 33197396／PRAGUE 35191923／INCEPTION 36720132（結果が揃っていない）。

**書かなかったこと**（付録C-5・C-6に明記）：血圧・心拍数の目標値、流量・回転数、
抗凝固の目標値、薬剤量。両心補助の詳細・小児・国内の診療報酬上の扱いも対象外。

**残りの補完リスト（ユーザーに提示済み、この順）**
2 低侵襲・ロボット心臓手術（MICS、分離肺換気、末梢送脱血）／3 術後鎮痛・ERAS・CSA-AKI
（※3は本巻第V部で一部を先取りした）／4 成人先天性心疾患／5 心臓移植・肺移植。

**作業メモ**：章を途中に挿入すると下流の章番号・図番号・本文の相互参照（第○章）が
一斉にずれる。unique な文字列で ordered replace し、`（㉝第22章）` のような
他巻参照を巻き込まないこと。総目次は 22 巻の `_生成スクリプト\build_toc.py` の
`VOLS` に追記（**保存先は cwd なので、実行後にシリーズ直下へ移動する**）。

関連: [[project-cardiac-anesthesia-consolidation]] [[project-cardiac-hemostasis-textbook-31]]
[[project-aortic-neuroprotection-textbook-32]] [[project-anesthesia-minitextbook-series]]
[[project-anesthesia-material-portal]] [[feedback-vancouver-citation-style]]
