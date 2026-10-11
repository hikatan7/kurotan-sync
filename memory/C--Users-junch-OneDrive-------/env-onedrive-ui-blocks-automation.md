---
name: env-onedrive-ui-blocks-automation
description: OneDriveのUIは合成クリックを一切受け付けない。Tabキーのフォーカス移動だけは通る
metadata:
  node_type: memory
  type: reference
---

OneDrive のウィンドウ（Activity Center のフライアウト、削除確認ダイアログ）は **computer-use の合成クリックをまったく受け付けない**。座標を正確に合わせても、msedgewebview2.exe に許可を出しても、クリックは「Clicked」と返るだけで画面は無反応（2026-09-10 に確認）。`OneDrive.exe /settings` も現行版26.153では効かない。

一方 **キーボードは届く**。Tab でフォーカスが動き、フォーカス枠が画面に出る。Space でボタンを押せた。

**Why:** OneDriveの設定変更をGUIで代行しようとして詰まった。結局 SHSetKnownFolderPath を PowerShell から呼ぶ方が確実だった。

**How to apply:** OneDriveのダイアログを操作するなら、クリックではなく Tab を1回ずつ送ってフォーカス枠をズームで目視確認し、目的のボタンに乗ってから Space。**Enter は既定ボタン（多くの場合こちらが望まない側）に当たるので使わない**。設定変更そのものは可能な限り API／レジストリで行う。関連: [[env-desktop-localized]]
