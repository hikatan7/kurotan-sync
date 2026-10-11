---
name: project-icu-ventilation-textbook-30
description: ミニ教科書㉚ ICUの人工呼吸管理。本編82頁・全35章・コラム21本・図版28点・番号引用89件＋専攻医版ちょうど20頁
metadata: 
  node_type: memory
  type: project
  originSessionId: b1b32ccc-9630-41e9-b3f7-0c43af361005
  modified: 2026-09-22T01:17:44.744Z
---

麻酔科ミニ教科書シリーズ **㉚「ICU の人工呼吸管理 ── 一回の呼吸を四つの局面に分けて読む」**（2026-09-22 作成）。
`教育ファイル集\麻酔科ミニ教科書シリーズ\30_ICUの人工呼吸管理\` に docx＋PDF＋図版＋_生成スクリプト＋台帳。

- 本編 **82頁**・全6部35章・**コラム21本**・図版28点（全て自作）・表14点・**番号引用89件**
- 別冊 `ICUの人工呼吸管理_専攻医版20頁`（**ちょうど20頁**）。本編と別採番で62件を引用
- 台帳 `ICUの人工呼吸管理_SourceLedger.xlsx`（89件・全件 PubMed）

**主題**：設定は患者の状態の記述である。だから設定を変えるのは「患者が変わったから記述を改める」順番で起きるはず。
逆（記述を変えて患者を動かそうとする）になっているときは何かを見落としている。

**構成の背骨は「一回の呼吸を四つの局面で読む」**（トリガ・リミット・サイクル・PEEP）。
モード名は商品名なので覚えない。申し送りも四つの局面の言葉で行う、という形に統一した。
ユーザー要望どおり第II部（第5〜12章）をモード解説に厚く割いた（VCV/PCV/二重制御/PSV/SIMV/APRV/NAVA・PAV＋/各社名称対応表）。

**⑱『呼吸管理と分離肺換気』との棲み分け**：⑱は周術期・分離肺換気、㉚は ICU で数日〜数週間続ける場面
（モード・波形・鎮静とバンドル・離脱）。本編の前書きに明記した。

**コラム（歴史もの）が本巻の色**：1952年コペンハーゲン（Ibsen と学生の手）／Vesalius の葦の茎／
SIMV 漸減が消えるまで／Sinderby の Edi／Pepe & Marini の隠れた PEEP／Webb & Tierney 1974／
baby lung／HFOV 2013 の二本／Hickling の permissive hypercapnia／RSBI 100／Ayre の T ピース／
青柳卓雄のパルスオキシメータ／pendelluft ほか全21本。

**How to apply（次巻でも使う）**
- **文献はタイトル検索で引き当ててから使う**。`_生成スクリプト\resolve.py`（PubMed esearch、**`sort=relevance` 必須** ──
  既定は新しい順なので、古典的な原著が絶対に出てこない）→ 実物タイトルを目で突き合わせ → `mkledger.py` で
  esummary から書誌を取り台帳 xlsx と `refs30.py` を生成。PMID を記憶から書かない。
- **番号引用は bookkit 側に入れた**。本文に `{{PMID}}` / `{{PMID,PMID}}` と書くと `_run` が肩付き番号を描き、
  `references(doc)` が出現順の一覧を出す。台帳にない PMID は KeyError で落ちる（strict）。
  別冊は `bookkit.CITES = bookkit._Cites()` で採番をリセットしてから組む。
- **図版の注記はパネルの外（上）に置く**。枠の中に置くと必ず枠線をまたぐか注記どうしが重なる。
  `fig30common.Panel` に `caption()`（見出し行の右端）と `toplabel()`（任意の t の頭）を用意した。
  パネルを縦に並べるときの間隔は **210px の枠なら 60px 以上**（ラベル1行ぶん）。
- **textbox の高さは戻り値で受けて次の y を決める**。固定値で積むと下の枠に重なる（f20 で実際に重なった）。
- `qa30.py`（figqa を全図に当てる）を **0件になるまで** 回してから docx を組む。43件→0件まで直した。
- 頁数合わせは本編では不要だが、別冊は「20頁ちょうど」を要求されたので、
  節を足して 15→17→19→20 と寄せた（減らすより足すほうが速い）。

関連: [[project-anesthesia-minitextbook-series]] [[project-minitextbook-18to21]]
[[feedback-vancouver-citation-style]] [[workflow-figure-text-fit]] [[env-word-com-doc-generation]]
[[project-anesthesia-material-portal]] [[project-teaching-material-backlog]]
