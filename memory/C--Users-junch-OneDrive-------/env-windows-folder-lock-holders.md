---
name: env-windows-folder-lock-holders
description: フォルダが「別のプロセスで使用中」でリネームできない時の犯人特定法。犯人はClaude Codeのpowershellシェル自身とexplorer
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 87098a73-49d2-4d04-af78-6f212448910d
  modified: 2026-09-10T04:39:18.959Z
---

Windowsで「The process cannot access the file because it is being used by another process」が出てフォルダをリネーム／移動できない時、**推測で同期アプリを止めて回らず、ハンドルを直接列挙して犯人を特定する**。

2026-09-10 に `OneDrive\デスクトップ` をリネームしようとして実際に起きたこと：OneDrive終了 → Google Drive終了 → explorer再起動、を順に試して全部空振り。ハンドル列挙したら犯人は **①Claude Codeのpowershellツールシェル自身 ②explorer.exe** の2つだった。

**犯人特定のコード**：`NtQuerySystemInformation(SystemExtendedHandleInformation=64)` で全ハンドルを列挙 → `DuplicateHandle` → `GetFileType`==1 のものだけ `GetFinalPathNameByHandle` でパス解決。GrantedAccess が `0x0012019f` / `0x00120189` / `0x00100000` のものは同期パイプでハングするので必ずスキップ。

**Why:**
- `Set-Location` はPowerShellの論理位置しか変えず、**Win32のカレントディレクトリハンドルは解放されない**。`[System.IO.Directory]::SetCurrentDirectory()` を呼んでも、このセッションのシェルが起動時に掴んだハンドルは残った
- Claude Codeのシェルは「Shell cwd was reset to ...」と表示されても、プロセス起動時のCWDのハンドルを持ち続ける
- explorer.exe はナビゲーションウィンドウでOneDriveツリーを監視するため、**再起動しても1秒以内に握り直す**
- プロセスのCWDを読むだけ（PEB経由）では不十分。ファイル監視ハンドルは見つからない

**How to apply:** セッション開始時の作業フォルダを操作対象にしてはいけない。どうしても必要なら、
1. `mcp__ccd_directory__change_directory` でセッションを別フォルダへ移す（反映はターン終了時）
2. **Bashツール側から** `taskkill //F //PID <powershellのPID>` でシェルを落とす（次回呼び出し時に自動で作り直される）
3. 同時に `taskkill //F //IM explorer.exe`
4. その隙に bash の `mv` でリネーム（PowerShellを新規起動すると余計なハンドルが増える）
5. `explorer.exe` を復帰

関連: [[env-desktop-localized]] [[env-onedrive-desktop-file-ops]]
