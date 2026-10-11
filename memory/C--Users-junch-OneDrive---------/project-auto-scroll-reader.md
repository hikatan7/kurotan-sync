---
name: project-auto-scroll-reader
description: 食事中に読む用の自動スクロール読書HTML（PDF・画像・テキスト）。自作ファイル集\自動スクロール読書
metadata:
  node_type: memory
  type: project
  originSessionId: d20a207c-33fc-43f5-b90b-5bbd2b8ba35c
  modified: 2026-10-07T07:51:53.989Z
---

2026-10-07作成。`自作ファイル集\自動スクロール読書\自動スクロール読書.html`（Chromeで開く）。PDF.js 3.11.174 を jsdelivr から読むので PDF表示はネット接続が必要。
Space/画面クリックで再生停止、↑↓速さ(1〜60)、←→少し戻る/進む、+−大きさ、N色(白/セピア/夜)、F全画面。ファイルごとに位置・速さ・大きさを localStorage に保存、再生中は画面スリープ防止(Wake Lock)。

デスクトップ直下に「自動スクロール読書.lnk」（chrome.exe にHTMLを渡す形、アイコンは黄緑地(#7CB342)に白「読」＋下矢印の自作 自動スクロール読書_黄緑.ico。色を変えるときはファイル名ごと変えるとアイコンキャッシュに引っかからない）。直下に置いてよいのはポータル2つとこれ。

**Why:** ごはんを食べながら手を使わずにPDFを読みたい、という依頼。
**How to apply:** 改良依頼はこのファイルを直す。ブラウザペインは非表示だと innerWidth=0・rAF間引きでテストが狂う → resize_window で寸法指定し、ローカルCORSサーバ経由でPDFを渡して検証した。[[feedback-open-html-in-chrome]]
