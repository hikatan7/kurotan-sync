---
name: env-desktop-localized
description: デスクトップは2026-09-10にOneDriveから切り離してローカル化。パスは C:\Users\junch\Desktop
metadata: 
  node_type: memory
  type: project
  originSessionId: 87098a73-49d2-4d04-af78-6f212448910d
  modified: 2026-09-10T10:19:15.830Z
---

## 【2026-09-14 現在】デスクトップの実体は `C:\Users\junch\OneDrive\_旧デスクトップ`

**2026-09-12〜14の間に、デスクトップの参照先がここへ戻された。`C:\Users\junch\Desktop` は空（0件）。今後ずっとこのパスで固定する方針でユーザー合意済み。** フォルダ名が「_旧」で実態と食い違うが、**改名しない**（2026-09-10の改名が終日のトラブルの発端だった。動いているものは触らない）。以下の2026-09-10時点の記述は歴史的経緯として残す。

**デスクトップアイコンが1個（ごみ箱）しか出ない障害の直し方**（2026-09-10に発生・解決）。ファイルもレジストリも正常なのに explorer のデスクトップビューだけがファイルを列挙しない。参照先を新規フォルダに向けても再現し、SFC/DISMもクリーン、BagMRU・Bags（2箇所）・アイコン配置・アイコンキャッシュ・名前空間拡張・`HKCU\...\Explorer` 丸ごと削除、すべて空振り。**真因は `%LOCALAPPDATA%\Microsoft\Windows\UsrClass.dat` の破損**。サインイン中はロックされて触れないので、管理者権限で `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\PendingFileRenameOperations` に `UsrClass.dat` と `.LOG1/.LOG2` の改名を予約し、再起動で作り直させて解決した（testアカウントでは正常＝プロファイル固有、と切り分けてから到達）。

移行内容（2026-09-10時点の記録）:
- 4,229ファイル / 16.47GB を robocopy /MOVE で移動。棚卸しCSVで照合し欠落0・サイズ不一致0
- **2026-09-10（同日夕）に旧 `OneDrive\デスクトップ` を `OneDrive\_旧デスクトップ` にリネームした**。ファイル選択ダイアログのサイドバーに「デスクトップ」が2つ並び、古い方が開かれてしまう事故を防ぐため。中身はOneDrive内に残るのでクラウドバックアップは維持
- **病院経営学 / 経営学 / 経営学テキスト**（計約1.08GB・585ファイル）は `C:\Users\junch\OneDrive\_旧デスクトップ\` が実体で、デスクトップに「〇〇（OneDrive）.lnk」を置いてある。※このlnkは `OneDrive\` 直下を指してリンク切れになっていたので2026-09-10に貼り直し済み
- **教育ファイル集 と 自作ファイル集 は2026-09-10にデスクトップへ戻した**（実体は `Desktop\教育ファイル集` 994件3.5GB / `Desktop\自作ファイル集` 109件104MB）。OneDrive 側にも同名フォルダが残るが、全ファイルが**クラウドのみのプレースホルダー**でローカル実体を持たない＝ディスクを食わないバックアップ。ただし**両者は同期しておらず独立**で、OneDrive 側は2026-09-10時点のスナップショット。デスクトップ側を編集しても反映されない
- ドキュメントとピクチャは今も OneDrive 側（`OneDrive\ドキュメント`・`OneDrive\画像`）のまま。KfmFoldersProtectedNow=3072
- ローカルDesktop配下のファイルはクラウド再解析ポイント0件＝完全な実ファイル
- `Desktop\病院経営学` は **ジャンクション**（→ `OneDrive\_旧デスクトップ\病院経営学`）。麻酔資料ポータルのランチャーがデスクトップ配下しか解決できないため。⚠️ デスクトップを再帰削除するツールを使うとOneDrive側まで消える
- **OneDriveを強制終了した状態でOneDrive内のフォルダを改名すると、復帰時にクラウド側から空フォルダが降ってきて復活する**（2026-09-10、`デスクトップ` が18:59に再生成された）。desktop.iniに `shell32.dll,-21769` が入るのでKFM再開と紛らわしいが、OneDriveの「デスクトップのバックアップ」設定はオフのままだった。中身が `desktop.ini` だけなら削除してよい
- 旧パスを指す残骸は**レジストリの文字列検索では見つからない**。Explorerのフォルダキャッシュ `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU` にPIDLとして残り、保存ダイアログのサイドバーで「場所が利用できません」を出す。該当の値と子ノードを消し、MRUListEx から番号を抜いてexplorer再起動で直る

**Why:** 保存のたびにフリーズしていた原因は、OneDrive.exe が起動していないのにクラウドファイル フィルタドライバ cldflt がデスクトップの4,234ファイル（全部プレースホルダー）を抱えていたため。応答しない同期プロバイダを待ってタイムアウトしていた。イベントログにクラッシュ記録は14日間0件で、OneDriveは異常終了ではなく単に終了させられたまま起動していなかった。デスクトップをOneDriveから外せば、以後OneDriveが落ちてもデスクトップは巻き込まれない。

**How to apply:** デスクトップのパスを書くときは `C:\Users\junch\Desktop`。旧デスクトップ由来の資料を触るときだけ `C:\Users\junch\OneDrive\_旧デスクトップ\<名前>`。このフォルダをリネーム／移動しようとするとロックで弾かれるので [[env-windows-folder-lock-holders]] の手順を使う。整理体系は [[project-desktop-folder-layout]]、移動手順の注意は [[env-onedrive-desktop-file-ops]]。
