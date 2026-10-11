---
name: project-teaching-file-folder
description: Teaching file と 学習ファイル\医学 を2026-09-09に教育ファイル集へ全統合。一次資料225件＋重複退避67件
metadata: 
  node_type: memory
  type: project
  originSessionId: 7096358a-ec55-4d61-a20d-d9aa10d39cc8
  modified: 2026-09-09
---

デスクトップの医学系一次資料は **2026-09-09 に教育ファイル集へ全統合**した。
Teaching file は空（フォルダのみ残置）、`学習ファイル\医学` はフォルダごと削除済み。

**移動先**：`教育ファイル集\一次資料（講義スライド・文献）\` に10分類で **225件**
（01_蘇生26／02_血管アクセス15／03_PAC 5／04_循環24／05_集中治療・呼吸30／
06_輸液・薬剤9／07_輸血・凝固20／08_麻酔・気道78／09_周術期・外科9／10_教育・安全9）

- Teaching file 236件 → 174件を移動、62件は既存と完全同一で退避
- 学習ファイル\医学 57件 → 51件を移動、移植6件は麻酔教材でないため `学習ファイル\移植` へ
- 退避先は `_重複レビュー\Teaching file重複_20260909\`（Office一時ファイル3件を含め計67件）。削除はユーザー判断
- 一覧：`一次資料（講義スライド・文献）\_一次資料一覧.xlsx`
  （シート2に退避67件それぞれの「同じものが残っている場所」あり。64件は教育ファイル集内を指す）

**Why:** 10分類は2026-07-24に決めた体系をそのまま流用した。
**既存の教育ファイル集のファイルは一切動かしていない** —— 麻酔資料ポータルがパスを参照しており、
移動すると壊れるため。統合は「既存に足す」方式に限定してある。

**How to apply:** 統合のたびに `教育ファイル集\_ポータル生成\更新する.bat` を実行
（[[project-anesthesia-material-portal]]、2026-09-09時点で438資料）。
移動は必ず SHA-256 で全件照合してから空フォルダを消す（[[env-onedrive-desktop-file-ops]]）。
OneDrive下では python の os.rmdir が PermissionError になることがあり、
PowerShell の `Remove-Item -Recurse -Force` なら通る。
関連: [[project-education-file-collection]] [[project-desktop-folder-layout]] [[feedback-links-must-be-excel]]
