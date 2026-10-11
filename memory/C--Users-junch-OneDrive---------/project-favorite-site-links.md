---
name: project-favorite-site-links
description: デスクトップ「Favorite site」にリンク台帳.xlsx＋.urlショートカットの2層でお気に入りサイトを保存
metadata:
  type: project
---

お気に入りサイトをクラウドに置かずローカル保存する仕組み。デスクトップ「Favorite site」フォルダに構築（2026-09-16開始）。

- `リンク台帳.xlsx` が「正」の名簿。列＝No/分類/サイト名/URL(ハイパーリンク)/概要メモ/タグ/登録日/最終確認日。B列は12分類のプルダウン、オートフィルタ＋ウィンドウ枠固定つき。「使い方」シート同梱
- `ショートカット\` に `[分類] サイト名.url` 形式のInternetShortcutファイル。エクスプローラー検索用
- 初回登録：MST（Medical Simulation Technologies）Release notes = TEEシミュレーターの更新履歴＋心疾患病理症例DB約30件

**Why:** .mdではリンクが飛べないという既存の方針（[[feedback-links-must-be-excel]]）に沿い、台帳はxlsxで作った。
**How to apply:** 追加依頼が来たら台帳に1行追記＋.url生成の両方を行う。将来は台帳からHTMLポータルを自動生成する構想（[[project-anesthesia-material-portal]]と同形式）。
