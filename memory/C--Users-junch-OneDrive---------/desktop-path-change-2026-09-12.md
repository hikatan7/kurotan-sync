---
name: desktop-path-change-2026-09-12
description: デスクトップの正は OneDrive\デスクトップ。2026-09-12に_旧デスクトップへ改名され復旧作業をした
metadata:
  type: project
---

2026-09-12、OneDrive同期の混乱で `C:\Users\junch\OneDrive\デスクトップ` が `_旧デスクトップ` に改名され、`C:\Users\junch\Desktop` も存在しない状態になった。正しい名前は `デスクトップ`（記憶87件の表記も、Claudeの会話74件が期待する作業フォルダもこれ）。

この一件で分かった、再発時に効く事実：

- **デスクトップの登録先は SHSetKnownFolderPath（FOLDERID_Desktop = B4BFCC3A-DB2C-424C-B029-7FE99A87C641）で設定する。** レジストリ直書きより確実で、再起動しても保たれる
- **Claudeの会話は作業フォルダ単位で束ねられる。** フォルダ名が変わると過去の会話が全部リンク切れになり「作業フォルダーが存在しません」が出る。復旧は「フォルダを選択」か、フォルダ名を元に戻すか
- **Claudeのセッション自身が作業フォルダを握るので、そのフォルダはセッション内からリネームできない。** Claudeを完全終了した状態で外部スクリプトから実行する必要がある（`C:\Users\junch\Downloads\デスクトップ名前戻し.bat`）
- **フォルダの色分けアイコンは各フォルダの desktop.ini の `IconResource=` が絶対パスで `自作ファイル集\ファイル保護ツール\アイコン\*.ico` を指す方式。** デスクトップの場所が変わると6フォルダ分が一斉に白紙化する
- **desktop.ini は UTF-16LE(BOM付き)。** 書き換え時は `Encoding.GetString()` が BOM を U+FEFF として文字列に残すので `.TrimStart([char]0xFEFF)` が必須。怠るとBOMが二重になり Windows がファイルを読めずアイコンが無視される

**Why:** 同じ事故が起きたとき、白紙アイコン・会話のリンク切れ・リネーム不可がバラバラの問題に見えるが、全部「デスクトップの実パスが変わった」一因から出ている。
**How to apply:** デスクトップ配下を触る前に `[Environment]::GetFolderPath('Desktop')` で現在の実パスを確認する。[[env-onedrive-desktop-file-ops]] の移動時の注意点も併せて適用。