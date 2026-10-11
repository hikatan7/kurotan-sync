---
name: project-mba-required-four-books
description: MBA必修4冊（人材マネジメント17頁／マーケ・戦略基礎15頁／経営戦略12頁／リーダーシップと倫理12頁）2026-10-07。演習・点検表なし、グロービス資料不使用
metadata:
  type: project
---

経営学\経営学テキスト に `急性期病院で学ぶ_MBA人材マネジメント`／`…マーケティング・経営戦略基礎`／`…経営戦略`／`…リーダーシップ開発と倫理・価値観`（docx+pdf、2026-10-07）。各9章・図版5〜6点・文献14〜19件（全件 PubMed/Crossref/NDL で書誌確認、著者名は PubMed から写す）。

- **Junko 指示：演習は不要、点検表（付録）も不要**（2026-10-07、作成途中で）。今後の経営学テキストも同様にする
- グロービス受講資料は一切開いていない（[[feedback-globis-materials-no-ai-input]]）。例の病院・数字は架空
- 生成：`経営学テキスト\_生成スクリプト_必修4冊`（engine.py＝共通組版、book_hrm/mkt/strat/lead.py＝META・REFS・FIGS・BLOCKS、figkit.py＝cards/flow/matrix/bars、to_pdf.ps1＝Wordを落とさない）。`python engine.py hrm` → `to_pdf.ps1 -Name <ファイル名>`
- bookkit の CITE_RE を英字キー対応に変更（`{{huselid95}}` 形式）
- flow 図は5枠以上だと見出しが縮む。見出しは6字以内、6項目以上は cards にする
- 照合で直した点：Kim&Mauborgne 2004 HBR に ERRC は無い（2005年の書籍）、Judge&Piccolo 2004 は「87資料・626相関」
- Genspark 査読キット：`経営学テキスト\_Genspark査読キュー\必修4冊_2026-10-07\査読キット_MBA必修4冊.html`（経営学ジョブA〜D＋Z）
- **2026-10-07 査読を反映（18＋17＋16＋16か所）→ 18/15/13/14頁**。反映スクリプトは `_rev_hrm/mkt/strat/lead.py`、反映前は `_査読前_20261007\`。採ったのは用語の説明不足・関連を因果と書いた箇所・架空例からの断定・名称の揺れ（6機能、5要因＋制度、心理的安全性の定義）。採らなかったのは Excel 手順などの大きな加筆と確認問題（演習不要の方針）
- Genspark は自分の文に露語を混ぜた（「добавえる」）。査読結果を写すときも異文字を走査する

関連: [[project-mba-critical-thinking-textbook]] [[project-ba-quant-intro-textbook]] [[feedback-genspark-max-work-per-reply]]
