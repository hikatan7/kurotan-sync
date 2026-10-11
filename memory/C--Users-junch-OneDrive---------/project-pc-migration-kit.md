---
name: project-pc-migration-kit
description: 2台目PCへの移行と2台運用。GitHub非公開リポジトリkurotan-syncに記憶・設定・自作スクリプト、資料はOneDrive。キットは自作ファイル集\PC移行キット
metadata:
  node_type: memory
  type: project
  originSessionId: 6809e539-378e-4efe-a9a9-53a5bf82478c
  modified: 2026-10-11T08:05:43.823Z
---

2026-10-11、Junko が2台目のパソコンを買って同じ作業をする準備を作った。

- ローカルのリポジトリは `C:\Users\junch\kurotan-sync`（OneDrive の外）。GitHub の非公開リポジトリ名は kurotan-sync。
- `sync.ps1` / `sync.bat`：記憶（~/.claude/projects/*/memory。3プロジェクト分、計256件）と settings.json は双方向で、新しいほうが勝つ（robocopy /XO を使うので削除は伝わらない）。作業フォルダ内の .py/.ps1/.bas/.vbs/.bat/.cmd/.cls/.psm1（1,162件）は一方向の控え。
- 新しいPCでは `OneDrive\_旧デスクトップ\自作ファイル集\PC移行キット\新PCセットアップ.bat` を実行する。winget で Git・Python3.12・Chrome・Claude を入れ、pip で13個のライブラリ、Noto Sans/Serif JP（キットの fonts\）、git の設定を入れ、clone したあと sync を走らせる。
- 手順書はキット内の `新PC移行手順書.docx`（5頁）。生成スクリプトは scratchpad の build_manual.py だった（保存していない）。
- 大前提はユーザー名 `junch`。記憶フォルダのキーとスクリプトの絶対パスがこの名前に依存している。
- setup.ps1 の `__GITHUB_USER__` は GitHub のユーザー名に置き換える必要がある。

**Why:** Junko は2台のパソコンを完全に同じ環境で使いたい。
**How to apply:** 記憶を書き換えたあとや作業の区切りには、sync.bat を実行するよう勧める。ユーザー名やパスが変わったら sync.ps1 と setup.ps1 を直す。関連：[[env-desktop-localized]] [[desktop-path-change-2026-09-12]]
