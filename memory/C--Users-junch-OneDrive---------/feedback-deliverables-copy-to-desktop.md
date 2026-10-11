---
name: feedback-deliverables-copy-to-desktop
description: 作ったファイルは元のフォルダとデスクトップ直下の両方に置く。デスクトップ側はJunkoが確認後にごみ箱へ入れる
metadata:
  node_type: memory
  type: feedback
  originSessionId: 674be580-03fd-47ae-86ca-76b55254a4b2
  modified: 2026-10-11T07:54:06.896Z
---

作った成果物（docx・PDF・xlsx・pptx など）は、**本来の保存先フォルダに置いたうえで、デスクトップ直下にも同じものをコピーする**（2026-10-11 Junko 指示）。重複は承知のうえ。デスクトップ側は Junko が確認してからごみ箱に入れる。

**Why:** フォルダの奥に置かれると、どれが今回できたものかすぐに見つけられない。デスクトップに並べて確認し、済んだら自分で片づけたい。

**How to apply:**
- デスクトップの実体は `[Environment]::GetFolderPath('Desktop')`（2026-10-11時点で `C:\Users\junch\OneDrive\_旧デスクトップ`）。決め打ちせず毎回これで取る。
- コピー後はハッシュを比べて一致を確認する。作り直したら両方を上書きする。
- デスクトップ側のコピーをくろたんが消すことはしない（[[feedback-never-empty-recycle-bin]]）。
- [[project-desktop-folder-layout]] の「直下ファイル0を維持」より、この指示が優先する。SendUserFile での受け渡し（[[feedback-deliver-files-in-conversation]]）も続ける。
