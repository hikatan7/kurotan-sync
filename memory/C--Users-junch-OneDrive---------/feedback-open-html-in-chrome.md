---
name: feedback-open-html-in-chrome
description: HTMLを開くときは既定ブラウザ任せにせずChromeを明示して起動する。Edgeで開かれるのをJunkoは嫌う
metadata:
  node_type: memory
  type: feedback
  originSessionId: 53d63e6a-c308-40f2-8810-68287f0f7370
  modified: 2026-10-01T14:43:58.623Z
---

HTML（コピーボタン付きキット等）をブラウザで開くときは `Start-Process <html>` ではなく
`Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "<html>"` でChromeを明示する。

**Why:** 2026-10-01、既定ブラウザが Edge（http と .html の関連付けが MSEdgeHTM）になっており、キットが Edge で開いた。Junko「Edgeで開きたくない」。既定の変更はシステム設定なのでくろたんは触らず、設定画面を開いて本人に切り替えてもらった。

**How to apply:** [[feedback-deliver-files-in-conversation]] の「既定ブラウザでも開く」は Chrome 指定で行う。
