# kurotan-sync

Junko のパソコン2台で、くろたん（Claude Code）の記憶・設定・自作スクリプトをそろえる非公開の保管場所。

| フォルダ | 中身 | 同期の向き |
|---|---|---|
| `memory/<プロジェクト名>/` | くろたんの記憶（`~/.claude/projects/*/memory`） | 双方向・新しいほうが勝つ |
| `claude/settings.json` | Claude Code の設定 | 双方向・新しいほうが勝つ |
| `scripts/` | 作業フォルダ（`OneDrive\_旧デスクトップ`）内の .py/.ps1/.bas など | 作業フォルダ → ここ（控え） |

- 作業の始めと終わりに `sync.bat` を実行する。
- 新しいパソコンでは、OneDrive の `自作ファイル集\PC移行キット\新PCセットアップ.bat` を1回実行する。
- 資料本体（docx/pdf/xlsx など）は OneDrive が同期する。ここには入れない。
- 患者データ・グロービス配布資料・院内文書は入れない。
