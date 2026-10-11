---
name: feedback-never-empty-recycle-bin
description: ごみ箱は絶対に空にしない。中身の確認と空にする判断は Junko が自分で行う
metadata:
  node_type: memory
  type: feedback
  originSessionId: 179b0caa-363e-4fde-94d0-182bbf00d8ca
  modified: 2026-09-30T17:36:23.497Z
---

ごみ箱を空にすること、ごみ箱内の項目を個別に完全削除することは絶対にしない（2026-10-01 Junko「ゴミ箱は自分で確認するので、絶対に空にしないで」）。

**Why:** 退避フォルダ等をごみ箱へ送った後、中身の確認と最終削除は Junko が自分で判断する。
**How to apply:** 削除を頼まれたら常にごみ箱へ送る（VB FileSystem.DeleteDirectory/DeleteFile + SendToRecycleBin）。送る前にごみ箱の上限と現在量を確かめ、押し出しで古い項目が完全削除されないようにする。報告でも「空にしますか」とは聞かない。関連: [[env-onedrive-desktop-file-ops]]
