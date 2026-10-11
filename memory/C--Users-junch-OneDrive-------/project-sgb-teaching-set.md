---
name: project-sgb-teaching-set
description: 星状神経節ブロック(SGB)教材3点の保存先と、元PDFの文献誤りの修正内容
metadata: 
  node_type: memory
  type: project
  originSessionId: eb3ac05b-aa9c-42a1-bd0b-efa1c6d9735c
  modified: 2026-07-30T03:33:18.838Z
---

星状神経節ブロック（SGB／難治性VT・VF・電気的ストーム）の教材3点を作成（2026-07-30）:
専門医向け教科書45頁docx／専攻医向け要点ガイド8頁docx／専攻医向けスライド6枚pptx。
**現在はユーザー希望でデスクトップ直下に置いてある**（元PDFも直下）。
本来の収納先は `学習ファイル\医学\08_麻酔・気道管理`。確認後にそこへ戻す。

土台にした元資料「星状神経節ブロック（SGB）解説.pdf」には**文献の帰属誤り**があり、
教科書の付録Dに検証メモとして残した。主な誤り: ①「Bourke 2017 JACC Clin EP」の数値
（12.4→1.04回）は実際は Meng L, et al. JACC Clin Electrophysiol. 2017;3(9):942-949、
②「Nunez-Rodriguez 2026 BJA メタ解析」は実際は Tsai/Nunez-Rodriguez/Cata の
ナラティブレビュー（Br J Anaesth. 2026;136(1):179-196）で、65%(64.6%)の出典は
Motazedian P, et al. Sci Rep. 2024;14:24719、③「JCS 2022でClass IIa」は裏付けなし
（正しくは **ESC 2022 で Class IIb**）、④「ACC 2024 expert consensus」は存在を確認できず。

**Why:** 同じPDFを別の資料に再利用すると誤引用が伝播する。推奨度の誤記は臨床判断に影響する。

**How to apply:** SGB関連で再度資料を作るときは教科書の付録Dを先に見る。
医療資料では数値だけでなく「どの集団・どの時間窓・どの定義か」を必ず併記する
（92%=12時間で50%減、64.6%=完全消失、47%=24時間ゼロ）。作成手順は
[[env-word-com-doc-generation]]（python-docx/python-pptx＋Word/PowerPoint COMでTOC更新・PNG QA）。
