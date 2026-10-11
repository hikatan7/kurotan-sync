---
name: project-thoracic-anesthesia-textbook-52
description: 〔52〕『呼吸器外科の麻酔』本編55頁＋専攻医版20頁。他AI原案を原典照合し誤り9点を付録Bに記録。PROTHOR・ERS/ESTS2025・PROSPECT2026反映
metadata:
  type: project
---

2026-09-24 作成。`教育ファイル集\麻酔科ミニ教科書シリーズ\52_呼吸器外科の麻酔`。
本編55頁（全6部25章・図版15点〔13自作＋⑱から2点再掲〕・コラム7本・文献55件）、
専攻医版20頁（コラム7本・症例4例・文献37件）、台帳xlsx、_生成スクリプト（build52.py／build_short52.py）。
副題「切る前に、残る肺を見積もる」。ユーザーが他AI（Perplexity/ChatGPT系）の原案を貼って依頼。

**この巻は例外的に数値を書いた**（ユーザーが数値・ガイドラインを明示的に要求）。ただし「線ではなく分かれ道」と前書きに明記。

## 原案を照合して直した点（本編 付録B）
- ACCP 2013 の筆頭は Colice ではなく Brunelli（PMID 23649437）。
- 駆動圧RCTは「Brunelli JAMA Surg 2019」ではなく Park, Anesthesiology 2019（30664548）。
- 2025 ERS/ESTS（41232938）のCPET参考値は **VO2peak <12 または VE/VCO2 slope >40**（<10は2009/2013の値）。
  低技術テストは歩行>400m・**階段>10m**。強い推奨は **DLCO測定のみ**。「リスクスコアは役割なし」は本文推奨に見当たらず。
- 全摘後肺水腫「輸液2L・ppo-FEV1<45%・血流≤55%」は出典不明 → Zeldin 1984（右全摘・大量輸液・多尿）に差替。
- 駆動圧SR「2026年4研究654例」は確認できず → Li 2022（7研究640例）。
- 「晶質液1–2 mL/kg/h」は根拠なし。確認できたのは Arslantas 2015 の **>6 mL/kg/h で PPC 増**。
- 原案の参考文献に付いていた PMC の URL は内容と対応していなかった。
正しかった：PROTHOR数値、禁煙RR 0.73/0.71/0.63（Tang 2025）、Thoracoscore、PROSPECT、POAF 25.1→13.4%（Riber 2014）。

## 新しく拾った一次資料
PROSPECT開胸2026（Lemoine、41521792：TEA または PVB が第一選択）、ASA 2026 区域鎮痛GL（41363869）、
EACTAIC 2025 気道コンセンサス（Granell、41353026）、Khor 2026 線維性ILD急性増悪IWG（42447235）、
Sato 2015 AE-IPスコア（25352311）、Cui 2024 CTでDLTサイズ（39080380）。
ERS/ESTS 2025 は PMC に無く、本文は academic.oup.com/ejcts/article/67/11/ezaf329 で読めた（ERJ は403）。

ポータル：book_toc.py の部名を「胸部外科麻酔」→「呼吸器外科の麻酔」、章39も「呼吸器外科の緊急事態」に改名し、
「呼吸器外科の麻酔」を部直下に振る規則を追加（資料220件）。総目次にも〔52〕を追記。

関連: [[project-minitextbook-18to21]] [[feedback-verify-ai-supplied-urls]] [[project-anesthesia-material-portal]] [[feedback-vancouver-citation-style]]
