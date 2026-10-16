---
name: project-thoracic-photos-20261016
description: 呼吸器外科・分離肺換気の5資料に実画像13種を追加（2026-10-16）。画像台帳は _素材、Word PDF化は「読み取り専用で開くと固まる」
metadata:
  node_type: memory
  type: project
  originSessionId: f257e9dc-2e8e-44d0-b211-3b2cb56757a6
  modified: 2026-10-16T06:28:33.811Z
---

Junko「フリーの症例集から画像を集めて分かりやすく、画像集めは他AIに投げて」で、4AIに画像収集を依頼し、PMC の CC 論文と Wikimedia Commons から13種を採用。
- 研修医版『呼吸器外科の麻酔と呼吸生理』HTML/PDF：20→26頁、写真1〜13（既存の図1〜9と別番号）。
- ⑱呼吸管理と分離肺換気（56頁）・専攻医版（34頁）、〔52〕呼吸器外科の麻酔（58頁）・専攻医版（28頁）：docx の該当図の直後に「写真N」＋説明＋出典（8〜12点）。控えは各 `_旧版\…_写真追加前`。
- 画像と台帳：`教育ファイル集\_素材\呼吸器外科・分離肺換気の画像_20261016\`（画像台帳_ライセンス.xlsx に AI 提示 38 本の照合も）。
- ライセンス方針：非営利の院内教育・改変なしなので CC BY／BY-SA／BY-NC／NC-SA／NC-ND を使用、ライセンス表記のないもの（BJA Educ 2023 の DLT 総説など）は不採用。今回は AI の PMC 番号の捏造なし。Copilot は短い依頼文なら答えた。

**Word の PDF 化の落とし穴（2026-10-16）**：Documents.Open を ReadOnly=$true で開くと SaveAs2/ExportAsFixedFormat が無限に固まる。Convert() 失敗後の保存も固まる。→ docx を %TEMP% にコピーし、読み書きで開いて SaveAs2(…,17) だけ、1ファイル1プロセス、timeout 付きで回す（各5秒）。固まった WINWORD は taskkill。

関連 [[env-word-export-saveas2]] [[project-thoracic-resident-physiology-text]] [[feedback-verify-ai-supplied-urls]]
