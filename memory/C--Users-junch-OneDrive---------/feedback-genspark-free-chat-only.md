---
name: feedback-genspark-free-chat-only
description: 画像・文献検索は Genspark の無料 AI Chat だけを使う。Super Agent（有料クレジット）は使わない（2026-10-18〜）
metadata:
  node_type: memory
  type: feedback
  originSessionId: f257e9dc-2e8e-44d0-b211-3b2cb56757a6
  modified: 2026-10-18T04:09:06.413Z
---

画像・文献の横断検索を Genspark に出すときは、無料の AI Chat（`agents?type=ai_chat`）だけを使い、Super Agent（有料クレジット消費）は使わない。

**Why:** 2026-10-18、Super Agent でクレジットが残り86まで減り、購入画面が出るようになった。Junko から「Genspark無料分だけにして検索続けて」と指示。

**How to apply:** 5時間制限に達したら、リセット時刻まで待ってから**新しい** AI Chat で送り直す（元のチャットには送れない）。待つ間は Perplexity・Gemini・ChatGPT に回してよいが、画像リンクはほとんど出ない。Super Agent へ回すのは Junko が改めて許可したときだけ。関連：[[project-genspark-capability-ledger]]、[[project-volume-up-plan-20261017-c]]
