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

**⑧を番号引用（バンクーバー方式）に改修（2026-09-21）:** 本文27文に肩付き番号、巻末に19件（45頁）。
台帳は同フォルダ `星状神経節ブロック_SourceLedger.xlsx`（PubMed 18 件＋ ASA 基本モニタリング基準）。
**第10章の末尾に1〜22の「引用文献」があったが、本文に番号がなく対応が追えなかった。**
その一覧を巻末の参考文献に置き換え、出現順に番号を振り直した。
主なもの ── ESC 2022（36017572）、Meng 2017（29270467）、Tian 2019（31514529）、
STAR study（Savastano 2024、38289867）、Chouairi 2024 多施設（38363278）と 2025 成功因子（39253899）、
Motazedian メタ解析（39433834）、Dusi 持続SGB（38531027）、
**STAR サブ解析（Currao 2026、41698390 ── 合併症率 単剤2%/2剤8%、重大0.5%の出どころ）**、
Sreekumar スコーピングレビュー（40961841 ── 74報中43報が症例報告）、
Goel 合併症レビュー（30992414）、ASRA LAST 2020（33148630）、ASRA 抗血栓 第4版（29561531）。
**3件は PubMed 上に特定できず外した** ── 11) BJA 2026 in press、21) Vlok の intra-arrest スコーピング
レビュー、22) StatPearls。その旨を参考文献の前書きに明記した。
付録D（原資料の出典帰属の誤り4点）はそのまま有効。
