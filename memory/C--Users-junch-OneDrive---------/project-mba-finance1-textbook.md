---
name: project-mba-finance1-textbook
description: MBAファイナンスⅠ（中級）32頁・全12章・図9・引用30件（2026-10-15）。グロービス資料不使用、架空のA病院・C病院。数字は calc.py から本文へ自動で入る
metadata:
  node_type: memory
  type: project
  originSessionId: 94a65cb4-2d26-4789-8fed-1d2cf8eed7ac
  modified: 2026-10-15T07:55:46.315Z
---

`経営学\経営学テキスト\急性期病院で学ぶ_MBAファイナンスⅠ_投資判断・資本コスト・企業価値.docx / .pdf`（2026-10-15、32頁）。デスクトップにもコピー済み。ポータル登録済み（テーマ fin）。
受講中の10月期ファイナンスⅠ（Day1は投資評価）に合わせ、Junko指示「公刊書と架空データで」。

- 構成：Ⅰ投資判断（増分CF・NPV/IRR/回収期間・感度/シナリオ・リアルオプション）／Ⅱ資本コスト（CAPM・WACC）／Ⅲ企業価値（DCF・マルチプル）／Ⅳ財務政策（MM・トレードオフ・ペッキングオーダー・配当）＋第12章 病院での限界。演習・点検表なし
- 例：A病院のロボット2台目（NPV 50.5、損益分岐 新規116件/年）、B案との順位逆転（交点9.9%）、C病院の事業譲受DCF（EV 2,468、継続価値76%）。無リスク利子率は財務省 jgbcm.csv の 2026-10-14 10年債 3.015% → 3.0%、WACC 6.5%
- 実データの引用：Graham&Harvey 2001（NPV 74.9%・IRR 75.7%・回収期間56.7%・CAPM 73.5%・全社一律割引率58.8%、原論文PDFで確認）、国内ロボットの損益分岐（Teraishi 2026 年200〜250件、Kojo 2026 年233件）、医療法54条（配当禁止）・54条の2（社会医療法人債）は e-Gov API v2、持分なし医療法人は厚労省手引書p.3とQ&A Q1-1、公立病院経営強化GL
- 生成：`経営学テキスト\_生成スクリプト_ファイナンスⅠ`（calc.py＝全数字、fin_p1〜p3.py＝本文、book_fin1.py＝META/REFS/FIGS、figkit_fin.py＝lines/tornado/tree/stack を追加、engine.py）。`python engine.py fin1` → `自作ファイル集\表の列幅自動調整\readable_docx.py` の reprocess（目次更新とPDFまで）
- 落とし穴：%書式を通さない文字列に「%%」と書くとそのまま出る（58.8%% が2か所出た）。PDFの全文を `%%` と異文字で走査してから渡す
- 他AI用の下調べキット `プロンプト集\37_ファイナンスⅠ中級テキスト_多AI分担キット.html` を作ったが、Junkoが「くろたんが作業して」と言い直したため未使用。調べ物は全部自分でやった

関連: [[project-mba-required-four-books]] [[feedback-globis-materials-no-ai-input]] [[project-globis-review-notes]] [[project-finance-textbook]]
