---
name: project-pc-migration-kit
description: 2台目PCへの移行と2台運用。GitHub非公開リポジトリkurotan-syncに記憶・設定・自作スクリプト、資料はOneDrive。キットは自作ファイル集\PC移行キット
metadata:
  node_type: memory
  type: project
  originSessionId: 6809e539-378e-4efe-a9a9-53a5bf82478c
  modified: 2026-10-16T17:02:49.795Z
---

2026-10-11、Junko が2台目のパソコンを買って同じ作業をする準備を作った。

- ローカルのリポジトリは `C:\Users\junch\kurotan-sync`（OneDrive の外）。GitHub の非公開リポジトリ名は kurotan-sync。
- `sync.ps1` / `sync.bat`：記憶（~/.claude/projects/*/memory。3プロジェクト分、計256件）と settings.json は双方向で、新しいほうが勝つ（robocopy /XO を使うので削除は伝わらない）。作業フォルダ内の .py/.ps1/.bas/.vbs/.bat/.cmd/.cls/.psm1（1,162件）は一方向の控え。
- 新しいPCでは `OneDrive\_旧デスクトップ\自作ファイル集\PC移行キット\新PCセットアップ.bat` を実行する。winget で Git・Python3.12・Chrome・Claude を入れ、pip で13個のライブラリ、Noto Sans/Serif JP（キットの fonts\）、git の設定を入れ、clone したあと sync を走らせる。
- 手順書はキット内の `新PC移行手順書.docx`（5頁）。生成スクリプトは scratchpad の build_manual.py だった（保存していない）。
- 大前提はユーザー名 `junch`。記憶フォルダのキーとスクリプトの絶対パスがこの名前に依存している。
- GitHub のユーザー名は **hikatan7**（setup.ps1 に書き込み済み）。リモートは https://github.com/hikatan7/kurotan-sync 。2026-10-11 に初回の push と sync の往復を確認した。ログインには Git Credential Manager を使う（ブラウザで Authorize）。
- Claude Code のシェルは対話できないので、ログインが必要な push はターミナルパネル（run_in_terminal）で実行する。

- 2026-10-17 方針変更：届いた新PCは shige さんのもの（既に shige アカウントあり）。junch アカウントを別に作って一時的に作業し、終わったら**古いPCをメインに戻す**。新PCからは「新PCで sync → 古いPCで sync → OneDrive同期完了を確認してリンク解除 → junch アカウントごと削除（Junko本人が操作）」で片づける。GitHub の認証取り消しと Microsoft アカウントのデバイス削除も勧めた。
- 同日最終決定：shige さんのPCは初回起動の段階だったので、Windows 初期設定に junchink@gmail.com で入って使う（フォルダは C:\Users\junch になる想定）。返すときは Windows を「すべて削除」で初期化し、Microsoft アカウントのデバイス一覧から外して渡す。↓の「junch ローカルアカウントを別に作る」案は不要になった。
- 同日さらに具体化：古いPCを**点検に出す間**、shige さんのPCに junch ローカルアカウントを作って作業し、点検から戻ったら古いPCへ戻して上記の片づけをする。Chrome は Google アカウントの同期で移す。点検前の時点で OneDrive の外にあるのは ダウンロード（403件・1.3GB）とデスクトップ直下の xlsx 1件だけ。

**Why:** Junko は2台のパソコンを完全に同じ環境で使いたい。
**How to apply:** 記憶を書き換えたあとや作業の区切りには、sync.bat を実行するよう勧める。ユーザー名やパスが変わったら sync.ps1 と setup.ps1 を直す。関連：[[env-desktop-localized]] [[desktop-path-change-2026-09-12]]
