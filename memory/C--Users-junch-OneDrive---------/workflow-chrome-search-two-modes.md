---
name: workflow-chrome-search-two-modes
description: Chrome検索依頼時の2モード運用 — ①簡易検索(A4 1枚) ②AIサイト横断検索(Gemini→Perplexity→Copilot→ChatGPT、詳細ノート回収)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fdbdc720-d3c4-4943-a77c-c858d93ee9b0
  modified: 2026-10-09T10:53:04.825Z
---

ユーザーがChromeでの検索・調査を依頼した際は、以下の2モードを使い分ける(2026-07-05指定)。

## モード1: 簡易検索
- 対象: 商品情報・価格比較、地図、グルメ、病院情報など、複数サイトからまとまった情報を知りたい場合
- 出力: **毎回必ずWordファイルまで作成**してデスクトップに保存する(チャット回答だけで終わらせない)
  - ページ数はユーザーが毎回指定(A4 1枚、2枚、3枚…)。指定ページ数ちょうどに収める(Word COMのComputeStatisticsでページ数確認)
  - 文書末尾に「■ 出典リンク」セクションを設け、出典を**クリック可能なハイパーリンク**で全件埋め込む
  - 体裁の実績(2026-07-05にユーザーが「完璧」と承認): メイリオ9pt基調、タイトル+背景+項目別2列テーブル(ヘッダー色付き)+提案・箇条書き+出典リンク7.5pt、余白0.5インチ

## モード2: AIサイト横断検索
- 対象: 一つのテーマ・文献の横断的な深掘り調査
- 手順: Chrome上でAIサイトを **Gemini → Perplexity → Copilot → ChatGPT** の順に同一テーマで検索し、前のAIの回答で不足している情報を次のAIで補完的に拾い集める
- 目的: 情報の偏りとハルシネーションの回避(複数AIのクロスチェック)
- 収集基準: ノートが作成可能なレベルまで完全に回収する。分量はA4数十枚になっても構わない
- 出力: WordまたはメモにRAW寄りの詳細情報としてまとめる
- スコープ: 最終的なファイル整形・体裁は内容の複雑さに応じてユーザーが複数のAIに振り分けるため、**情報回収と詳細まとめまで**がこちらの担当

**Why:** 単一AI・単一検索では情報の偏りやハルシネーションが混入するため、複数AIの回答を突き合わせて網羅性と正確性を担保したい。

**How to apply:** 検索依頼を受けたら、比較・生活情報系なら簡易検索、テーマ深掘り・文献系なら横断検索と判断(迷ったら確認)。横断検索ではClaude in Chromeで各AIサイトに順にアクセスし(要ログイン済みセッション)、各回答を保存→差分・不足を次のAIへの質問に反映→全回答を統合した詳細ドキュメントを作成する。関連: [[user-medical-ai-workflows]]

**マスタープロンプト(2026-07-05作成):** 横断検索を1回の質問で済ませる「学習資料作成用マスタープロンプト」を作成。呼び出しキーは「マスタープロンプトで:【テーマ】」。出力要件10項目(全体像/トピック完全網羅=定義→仕組み→具体例→問われるポイント/用語集英語併記/実在事例/数値・数式/比較表/直近1〜2年動向/書誌正確な推薦書/誤解と注意点/学習ロードマップ)+厳守事項(不確実情報に※要確認/挨拶なし本文のみ/階層見出し)。Geminiには登録済み(「登録完了」確認)。ChatGPT/Copilot/Perplexity用の貼り付けテキストはデスクトップ「AI横断検索用マスタープロンプト.txt」に保存済み(ユーザーが手動登録する)。

**2026-10-09 実測（4サイト自動投入）：** Gemini・ChatGPT・Copilot・Perplexity の入力欄は、いずれも javascript_tool で `el.focus(); document.execCommand('insertText', false, text)` すれば全文（英数字・改行込み）が入る（Copilot は textarea）。送信はボタンを find→クリック（Enter は効かないことがある）。**用量を含む医学の質問は Gemini が1回目に「お手伝いできません」で止まる**→新しいチャットで「教科書的知識として解説」と短く言い換えると答えた（ただしFlashに落ちた）。Copilot は「Think Deeper」がオンだと「応答できません」が続き、通っても数値のない枠だけの表になった。回答の回収は get_page_text、長いものは最後の回答要素の innerText を2,000字ずつ切る。

**2026-10-16 更新：Claude in Chrome で Perplexity・Copilot・Gemini・Genspark の4つとも操作できた**（ログイン済みのChrome。内蔵ブラウザは4サイトとも未ログイン）。投入は javascript_tool の insertText、送信はボタンを aria-label（Copilot「メッセージの送信」、Gemini「プロンプトを送信」）か座標でクリック。Gemini の Deep Research は「その他のツール」→「Deep Research」で切替、計画は自動で開始し完了まで約20分、レポートは deep-research-immersive-panel 要素。Genspark はホームの入力欄（スタンダード＝無料枠）でスーパーエージェントになる。回収は表を DOM から行ごとに取り出す（innerText は '=' '&' を含むと[BLOCKED]になるので置換、出力は約2,000字で切れるので分割）。

**制約(2026-07-05判明・当時):** Claude in Chrome拡張ではperplexity.ai / copilot.microsoft.com / chatgpt.com / bing.comが操作不可。navigateは「not allowed」、ユーザーがタブをClaudeタブグループに入れて可視化できても操作は「Permission denied for this action on this domain」でポップアップすら出ない完全拒否(拡張の安全設計上の制限とみられ回避不能)。Geminiのみ許可ポップアップ経由で操作可能。→ 横断検索の実運用: ①Gemini=Claudeが代行(マスタープロンプト登録済み) ②他3サイト=ユーザーがデスクトップ「AI横断検索用マスタープロンプト.txt」からコピペで質問し、回答をClaudeに渡してもらう ③Claude側はWebSearch/WebFetchで実在Web情報源によるクロスチェック(書誌ハルシネーション検出実績あり)。この分担を最初から提案すること(タブ移動やchrome://extensions変更の試行錯誤は2026-07-05に全て失敗済み)。Geminiの送信はEnterキーでは発火しないことがあり、送信ボタン(↑)クリックが確実。回答回収はget_page_textで全文取得できる(サイドバー履歴も混ざるので本文のみ抽出)。
