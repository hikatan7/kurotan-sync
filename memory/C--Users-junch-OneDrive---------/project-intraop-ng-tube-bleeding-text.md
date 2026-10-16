---
name: project-intraop-ng-tube-bleeding-text
description: 術中の胃管と術後の上部消化管出血 専攻医向け8頁・番号引用26件（2026-10-14）。他AI原案の書誌の誤りと、確かめた数値
metadata:
  node_type: memory
  type: project
  originSessionId: aa737672-0a0c-48a1-8522-b83397941efa
  modified: 2026-10-14T04:47:42.119Z
---

教育ファイル集\1_総論\10_周術期医学・安全・チーム\術中の胃管と上部消化管出血\ に
`術中の胃管と術後の上部消化管出血_専攻医のためのテキスト.html/.pdf`（8頁・26件）。デスクトップにもコピー済み。
作り方は VPC と同じ（HTML→Chrome headless→PyMuPDFでノンブル）。src.html に {{key}} と書き、make.py が出現順に番号を振る。スクリプトは scratchpad限り。改訂は HTML を直接直す。ポータル未登録・SourceLedger 未作成。

構成：出血源の鑑別表 → 対応（制限的輸血・PPI・24h内視鏡・TXAは使わない・抗凝固/低体温）→ 予防表（挿入前/挿入時/留置中/抜去時）→ 是非 → 入れなかった場合 → 報告例コラム3本。

確かめた要点：
- 他AI原案の「Ilias K 2017」は誤り。筆頭は **Sdralis EIK**（Dis Esophagus 2017, PMID 28575240）。死亡13.3%、医原性46.5%
- 食道壁内血腫の症例は Yamada T, Am J Case Rep 2019（PMID 30783075）、剝離性食道炎は Sudo G, BMJ Case Rep 2020（PMID 33229484）。どちらも日本の報告
- Lowham 1996：前腸手術1,620件で損傷13件（胃管2・ブジー11）
- ERAS大腸2018：術後胃管は常用しない、術中に入れたら覚醒前に抜く（高・強）。腹腔鏡では胃損傷予防に経口胃管
- Kerger 2009：術中胃管でPONV減らず 44.4% vs 41.5%。Cochrane（Nelson 2007）33試験5,240例
- 挿入法：Ou 2021メタ解析、Kirtania 2012 ガイドワイヤー初回99.2%、Yamaguchi 2026 J Anesth ビデオ喉頭鏡連続挿入で合併症2/30 vs 12/30
- ESGE 2026改訂（Endoscopy 58:899）：循環不安定でなければ6h/12h以内の緊急内視鏡を勧めない
関連 [[project-intraop-vpc-lidocaine-atropine]] [[feedback-verify-ai-supplied-urls]] [[feedback-vancouver-citation-style]]
