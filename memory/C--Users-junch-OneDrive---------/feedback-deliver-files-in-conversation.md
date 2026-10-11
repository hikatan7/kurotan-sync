---
name: feedback-deliver-files-in-conversation
description: 作ったファイルは相対パスのリンクで済ませず、SendUserFileでこの会話の中に開ける形で渡す。貼り付け用の文面はコピーボタン付きHTMLにまとめる
metadata:
  node_type: memory
  type: feedback
  originSessionId: 640bf3ea-4647-4c86-a982-c553c0768712
  modified: 2026-09-25T00:49:12.602Z
---

成果物は **SendUserFile（display: render）で会話内に直接出す**。本文中のmarkdownリンクだけで済ませない。
何回かに分けて他のAIに貼る文面は、**貼る順に並べてコピーボタンを付けたHTML1枚**にまとめて渡す（例：`23_急性腎障害AKI\_Genspark査読用\㉓AKI_査読_貼り付け用.html`）。

**Why:** 2026-09-25、プロンプトと本文txtを相対リンクで案内したら、作業中にカレントフォルダが変わったせいで「ファイルが見つかりません」になった。フォルダ名をコード表記で書いただけのものは、そもそもクリックできない。Junkoはメモ帳で開く運用もしていない（→ [[feedback-links-must-be-excel]]）。

**How to apply:** 何かを作ったら、最後に SendUserFile で渡す。どうしてもリンクを書くなら絶対パスで書く。

**コピーボタン付きHTMLは、会話内プレビューではボタンが効かない（2026-09-25）。** プレビュー枠は静的表示でスクリプトが動かない。Junkoから「コピーボタンが押せない」。→ コピー用キットは SendUserFile に加えて `Start-Process <html>` で既定ブラウザでも開く。本文は `<textarea>` に入れておく（枠内で Ctrl+A→Ctrl+C でも取れる）。ボタンは clipboard API＋execCommand の二段構え（_ツール_査読キット.py と同じ）。
