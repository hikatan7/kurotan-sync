---
name: project-file-protect-tool
description: デスクトップ「ファイル保護ツール」= 削除保護(ACL)＋フォルダアイコン変更のGUIアプリ。Windows ACL の落とし穴と検証結果つき
metadata: 
  node_type: memory
  type: project
  originSessionId: 75282f94-cb1d-4e07-a102-f31b0731866e
  modified: 2026-07-25T19:42:31.841Z
---

デスクトップ「ファイル保護ツール」（2026-07-26 作成）。Python+tkinter の GUI で
①選んだフォルダ／ファイルの削除保護（標準／強力の2段階）②フォルダアイコンの色分け変更。
[[project-file-organizer-tool]]（ファイル整理ツール）と対になる位置づけ。

**Windows ACL の重要な落とし穴（実機検証済み）**：削除は「対象自身の DELETE 権」
または「親フォルダの DELETE_CHILD(DC) 権」の**どちらかが通れば成立**する。
そのため対象に deny DE を付けるだけでは効かず、**親フォルダにも非継承の deny (DC) が必要**。
これは同フォルダ内の他ファイルの削除には影響しない。
（OneDrive 配下は既定で `Everyone:(I)(CI)(DENY)(DC)` が継承されているため元から効く）

- 標準保護 = 対象に `(DE)` … ごみ箱削除・改名・移動を阻止。中身は自由。
  ただし Shift+Delete の再帰削除では中身が先に消える（既知の限界）。
- 強力保護 = 対象に `(OI)(CI)(DE,DC)` … 中身も削除不可。**Word/Excel の上書き保存が失敗する**
  （一時ファイル→差し替え方式のため。os.replace が PermissionError になることを実測）。

**フォルダアイコン**：desktop.ini に `IconResource=path,0`＋ini を +h +s、フォルダを +r。
Windows 自身の Downloads/Music と全く同じ構成。
注意：`SHGetFileInfo` はパス指定でも PIDL 指定でもカスタムフォルダアイコンを返さない
（Windows 標準の Downloads で試しても既定の黄色フォルダが返る）。
設定内容の確認は `SHGetSetFolderCustomSettings(FCS_READ)`、
実際の描画確認は `IShellItemImageFactory::GetImage`（COM, vtable[3]）を使う。

**「アイコンが一部だけ反映されない」の真因（2026-07-26 実機で解明）**：
`iconcache_*.db` ではなく **`thumbcache_*.db`**。フォルダの中身から作られたサムネイルが
残っているとカスタムアイコンより優先され、サムネイルを持つフォルダだけ古いままになる。
`ie4uinit.exe -show` も explorer 再起動＋iconcache 削除だけでも直らない。
**両方消して explorer 再起動**で全部直った。desktop.ini がバイト単位で同一の2フォルダで
片方だけ効かない、という切り分けで確定。

**Why:** 同じ検証を二度やらないため。ACL の deny だけ付けて「効かない」と誤診しやすい。
**How to apply:** 削除保護や誤削除防止の相談が来たらこのツールを案内。
ACL を扱うコードを書くときは親フォルダの DC を必ずセットで考える。
