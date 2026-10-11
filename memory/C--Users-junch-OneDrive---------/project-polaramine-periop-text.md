---
name: project-polaramine-periop-text
description: 周術期のポララミン 専攻医向け10頁版（文献42件）＋4頁簡易版（28件）。2026-10-06。ポータルはアレルギー・アナフィラキシー対応
metadata:
  node_type: memory
  type: project
  originSessionId: 157964ef-cf49-4ebf-b366-e469afd8160d
  modified: 2026-10-06T06:24:48.719Z
---

教育ファイル集\研修医・専攻医向けテキスト\周術期のポララミン_専攻医のための10頁テキスト.html/.pdf と 4頁テキスト.html/.pdf（2026-10-06）。
ノルアドレナリン6頁版と同じ HTML→Chrome headless 印刷方式。ソースは scratchpad にあったので、改訂するときは HTML を直接直す（肩付き番号は振り済み）。

原本で確かめた要点（他AIの原案と違った点を含む）:
- ASCIA 2026 は6月版（v2あり）。「Do not use **oral** sedating antihistamines…mimic some signs of anaphylaxis」。プロメタジン注も使わない
- RCUK周術期アルゴリズム2024（ポスター）には抗ヒスタミン薬が一切出てこない。「Skin signs are often absent in severe reactions」。初回アドレナリン 50μg は確認済み
- 「約1/3で皮膚所見なし」の出典は Mertes 2011 の IgE介在性反応。NAP6 は初発症状で皮疹6.6%・経過中56%、日本の全国調査（Sugiyama 2023）は81.4%
- 日本アレルギー学会2022 表15：H1は推奨度C、急速静注で血圧低下、第二世代は同等の効果だが十分なデータなし（PDFは画像なので頁を画像化して読む）
- 日本麻酔科学会2021は「H1遮断薬は血管拡張と気管支収縮を軽減」「安全性は高い」とまだ書いている（海外改訂とずれる）
- 日本には静注できる第二世代H1薬がない。ポララミン注の効能にアナフィラキシーは含まれず、静注速度の規定もない（英国SmPCは1分以上かけて）

Genspark には [[workflow-genspark-kurotan-style]] 形式で抽出・検索を流したが、5時間制限で①は返信1、②は返信2で止まった。残りはくろたんが PubMed/原本で埋めた。プロンプトは プロンプト集\28_ポララミン周術期_Genspark抽出と検索.html。
関連: [[project-periop-anaphylaxis-guide]] [[project-anaphylaxis-last-textbook]] [[project-noradrenaline-5p-text]]
