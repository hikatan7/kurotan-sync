---
name: workflow-genspark-kurotan-style
description: Gensparkにくろたんの作法を覚えさせる2層方式（カスタム指示＋チャット冒頭の仕様書）。プロンプト集25番
metadata:
  type: project
---

2026-09-25、Junkoの依頼で `自作ファイル集\プロンプト集\25_Gensparkにくろたん流を覚えさせる.md` と `25_くろたん流_Genspark設定キット.html`（コピーボタン付き）を作成。

- ① 短い版（約780字）＝Personalize → Custom Instructions に貼る。10か条＋合言葉「くろたん流で教科書／研修医テキスト／院内文書／スライド／点検」。入らなければ ①' 最短版（約320字）。
- ② 仕様書（約3,300字）＝毎回チャットの1通目に貼る。出典・略語・くろたん記法（# 部／## 章／〔Pearl〕…〔/Pearl〕／【図n.m】…【図ここまで】）・種類別仕様・Word実測スタイル・返信作法。
- 基本は AI Chat（無料）で「くろたん記法」の原稿を出させ、くろたんが PubMed 照合＋bookkit で組む。AI Docs/Slides での直接生成は有料の予備ルート。

**未実測（25番の「6. 実測」表に記録する）：** カスタム指示の字数上限、Plusで使えるか、AI Chat／Docs に効くか、試しの2頁でどこまで守るか。

**試しの2頁（PONV、2026-09-25）：** 出典は文献5本・数値13か所とも PubMed の書誌・抄録と完全一致。Genspark が自分で Web 検索（PubMed/Europe PMC）を十数回かけて裏を取っていた。過去の監査で著者名や巻号を作っていたのは、検索せずに答えた場合だったと考えられる。守れなかった点：分量が約2倍、くろたん記法の崩れ、研修医向けなのに統計用語の説明なし、表記ゆれ（スコポラミン／スコパミン）。→ 仕様書で分量の上限を「±10%」と明記し、記法の見本を1つ示すと改善しそう。**クレジット消費ゼロ（Junko確認）＝AI Chat は Web 検索込みで無料。** 同日、仕様書を第1.1版に（分量±10%、記法の見本、統計用語の説明必須、表記ゆれ禁止、実数の自己点検4項目）。

**How to apply:** 作法（出典・表紙・略語・Word書式など）を変えたら 25番の①②も直し、キットHTMLを作り直す。関連 [[project-genspark-capability-ledger]] [[feedback-genspark-max-work-per-reply]] [[feedback-vancouver-citation-style]]
