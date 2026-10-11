---
name: project-file-organizer-tool
description: デスクトップ「ファイル整理ツール」— 重複検出＋条件抽出のPython/tkinter GUIアプリ(2026-07-26作成)
metadata: 
  node_type: memory
  type: project
  originSessionId: 9d623f75-5a2c-45d9-8a47-75e9ecb94cb0
  modified: 2026-07-25T17:51:59.604Z
---

デスクトップ `ファイル整理ツール\ファイル整理ツール.py`（Python3.12+tkinter、追加ライブラリ不要）。
デスクトップ直下に起動用ショートカット `ファイル整理ツール.lnk` あり。

- ①重複検出：サイズ→先頭64KB→全体SHA-256の3段階。グループ表示し「★残す推奨」を自動選定
  （コピー/(1)/旧/統合済_ を減点 → 浅い階層 → 短いパス → 古い更新日 の順で残す）
- ②条件抽出：ファイル名・拡張子・更新日・サイズ。プリセット「統合済_の一次ファイル」等
- 処理は「移動」（操作ログ.json に記録し1クリックで元に戻せる）と「ごみ箱送り」のみ。**完全削除機能は意図的に非実装**
- OneDriveのクラウドのみファイルは st_file_attributes で検出し、既定でハッシュ照合しない（勝手にDLさせない）。
  該当グループは「サイズ一致(クラウド未照合)」として自動チェック対象外
- ごみ箱送りは PowerShell の Microsoft.VisualBasic.FileIO.FileSystem::DeleteFile 経由
  （ctypes の SHFileOperation は構造体を誤ると完全削除になるため避けた）

既定の移動先はデスクトップ `_重複レビュー`（[[env-onedrive-desktop-file-ops]] の運用に合わせた）。
[[workflow-file-consolidation]] の「統合済_」退避作業をこのツールで代行できる。
