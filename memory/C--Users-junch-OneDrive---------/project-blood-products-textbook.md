---
name: project-blood-products-textbook
description: 「血液製剤とアルブミン」教科書（docx/PDF 102頁・図版28点）の所在と構成
metadata: 
  node_type: memory
  type: project
  originSessionId: dfa56fed-97fb-49e2-913d-191807cdb3d5
  modified: 2026-08-14T00:02:48.182Z
---

デスクトップ「学習ファイル\医学\07_輸血・凝固・血栓塞栓\血液製剤とアルブミン」に
血液製剤とアルブミン.docx／.pdf（94頁）＋「図版」24点を作成（2026-08-13）。

全6部15章。第I部 製剤を分解する（全体像／赤血球＋保存病変／FFP・血小板＋輸注後動態／アルブミン5%vs25%）、
第II部 圧・分布・酸素（4つの圧／Alb分布40-60・TER・半減期19日／CaO2・ボーア効果）、
第III部 合併症（ヘモビジランスの読み方／急性／遅発性・鉄過剰）、
第IV部 臨床判断（Hb閾値／アルブミン適応／大量出血／小児・新生児・胎児／血液腫瘍・HSCT）、
第V部 病態生理コラム20本（ユーザー指定のテーマ）、第VI部 歴史・社会コラム12本（Denis〜PBM・Titmuss）、
付録A〜E（製剤早見表・公式集・初期対応カード4枚・文献・自己評価40問）。

デスクトップ直下にあった調査資料6PDF＋2MDが原典（日赤添付文書・安定性試験、
輸血療法実践ガイド2026、アルブミンGL改訂第3版、大量出血GL第2版、小児輸血GL2017、
ICTMG/AABB/CHEST/J-SSCG、SAFE/ALBIOS/ATTIRE/TRICS III/MINT/HEMOTION/TOP/ETTNO/PlaNeT-2/PROPPR）。
**教科書全体の主題**＝「袋の中身」と「体内で起きること」を混同しない
（上清K濃度≠血清K、回収率40%≠残存率、浸透圧比≠膠質浸透圧、1時間CCI≠24時間CCI）。

**2026-08-14 改訂**（102頁・図版28点）：図版の文字重なり／枠外はみ出しを修正
（figs3.py の box() に `_autofit`＝折り返し→縮小の自動調整を実装。幅だけ超過時のみ折り返し、
高さが溢れたら縮小に切替）。第2章に 2-5〜2-10 を増補 ── 製剤の Hb 17.6 g/dL・Ht 50〜52%、
Ht と粘度の指数関数関係、4℃は37℃の約2.2倍粘い、Hagen-Poiseuille（内径の4乗）、
加圧は300 mmHg まで、輸血は前負荷と後負荷を同時に上げ左室一回仕事量が約+21%、
**2026年時点で非LR製剤は存在しない（日赤2007年全面導入）／非照射の赤血球液-LRは存在する**。
コラム33（vCJDと universal leukoreduction の国際比較）を追加。自己評価問題は46問。

ビルドは [[project-fluid-management-textbook]] と同じ基盤（doclib.py/htmldoc.py）。
figs3.py＋figs3b.py で図生成 → b_content1/1b/2〜5.py → build_blood.py。
PDF は Chrome の --print-to-pdf。

**2026-08-31 派生（12頁版）**：`教育ファイル集\アルブミン製剤と輸血_大量出血の凝固管理まで_専攻医のための12頁ミニテキスト.docx / .pdf`（A4×12頁ちょうど）。
①総論＋大量出血の評価3軸 ②赤血球製剤 ③輸血閾値 ④凝固の cell-based model（図） ⑤大量出血の7軸を個別補正
⑥フィブリノゲン（濃縮製剤50 mg/kg、FFPでは非効率と計算） ⑦FFPの量15〜20 mL/kgと速度10〜15 mL/kg/時
⑧血小板とVET（EXTEM/FIBTEM） ⑨MTPアルゴリズム（図） ⑩⑪アルブミン ⑫副反応と数値早見。
図版2点は `03_血液製剤とアルブミン\図版` に PNG で保存（matplotlib＋Meiryo、figs.py）。
**先に作った10頁版は `デスクトップ\_重複レビュー\旧版_…10頁ミニテキスト` へ退避済み。**

**組版の教訓**：表・囲みの直後に入れる空段落は、行高を `w:spacing lineRule="exact"` で 1pt に固定すること。
既定の9pt段落記号のままだと、ページ末で13pt前後の「幽霊の高さ」になり、内容が入っているのに次頁へ溢れる。
これを直しただけで17頁→12頁になった。ページ数合わせでは、まず PyMuPDF で溢れ頁の `get_text()` を見て
「何が溢れたか」を特定する（maxY だけでは原因が分からない）。

**2026-08-31 派生（10頁版・旧）**：専攻医向けの要約版
`教育ファイル集\アルブミン製剤と輸血_専攻医のための10頁ミニテキスト.docx / .pdf`（A4×10頁ちょうど）。
①総論と5つの区別＋10頁の地図 ②赤血球製剤の物性・保存病変 ③輸血閾値と主要RCT ④FFP・血小板・CCI
⑤アルブミンの物性と動態 ⑥アルブミンの適応（SAFE/ALBIOS/ATTIRE） ⑦大量出血7軸＋PROPPR
⑧急性合併症・ヘモビジランス ⑨遅発性合併症・鉄過剰 ⑩数値早見＋自己点検10問と解答。
本編102頁からの抜き書きで、新規の医学的主張は足していない。体裁は
[[project-perioperative-va-text]] の4頁テキストと同じ（メイリオ9pt・行間245・余白14/13/15、
見出し navy 1F3A5F、小見出し B03030）。ビルドは python-docx（scratchpad の dlib.py/build.py）→
Word COM で PDF 化し、[[workflow-docx-exact-page-count]] の maxY 法で10頁ちょうどに詰めた。

**2026-08-31 増補 → 13頁版**（旧10頁版もデスクトップ\教育ファイル集に残置）。
`アルブミン製剤と輸血_大量出血の凝固管理まで_専攻医のための13頁ミニテキスト.docx / .pdf`。
ユーザー指示で凝固の章を厚くした：①4頁＝従来カスケード図（PT/APTTの守備範囲・薬剤の作用点・
「この図で見えないもの」）②5頁＝cell-based model（Initiation/Amplification/Propagation）
③6頁＝大量出血の7軸を個別補正 ④7頁＝フィブリノゲン（50 mg/kg＝3〜4 g、FFPで同量を補うと約1,400 mL
必要という計算）⑤8頁＝FFPの量と速度（RBC:FFP 1:1、15〜20 mL/kg、10〜15 mL/kg/時以上、PROPPR）
⑥9頁＝血小板とVET（FIBTEM A5<10、EXTEM A5<35、EXTEM CT延長、ML>15%）⑦10頁＝アルゴリズム図。
体温は「国内ガイド ≧35℃を下限、目標は36℃」と両論併記した。

**図版3点**は `教育ファイル集\アルブミンと輸血_図版\` に fig_cascade / fig_cellbased / fig_algo。
**作図は matplotlib＋Meiryo で自作**（scratchpad の figs.py / fig_cascade.py）。
→ **画像生成AIに日本語ラベルの機序図を描かせない**。Geminiに凝固カスケードを描かせたところ
「stableized フィブリン網」「蕁蔽粗制織に鋭裏され」等、全ラベルが幻の文字列になった。
どうしてもAIに任せるなら「画像ではなく matplotlib のコードを書かせる」プロンプトにする。

## 番号引用化（2026-09-22）

**122頁・番号引用45件**（PubMed 27件＋未収載18件）。台帳は同フォルダの
**血液製剤とアルブミン_SourceLedger.xlsx**（シート「③_血液製剤とアルブミン」）。
付録D の見出しを残して中身を出現順の番号一覧に差し替えた（`_引用ツール\applycites_inplace.py`）。

未収載18件＝日赤の資料表と添付文書6件、PMDA のアルブミン添付文書2件、
日本輸血・細胞治療学会の各ガイドライン5件、SSC 2026、丹羽ほか（日本血栓止血学会誌）、
Titmuss『The Gift Relationship』、Bohr/Hasselbalch/Krogh 1904、厚労省・日赤の血液事業資料。

**付録Dで直したもの:**
- 「Fleck A, Raines G. Albumin distribution in health and disease. Lancet 1989;1:781-784」
  → 巻号頁の一致する実在論文は **Fleck A ほか, Lancet 1985;1:781-784
  『Increased vascular permeability: a major cause of hypoalbuminaemia in disease and injury』
  （PMID 2858667）**。題名も年も違っていた。
- 「Rifkind JM, et al. Red Blood Cell Storage Lesion. Transfus Med Hemother 2017」は
  PubMed に該当なし。同主題の総説 **Yoshida T ほか, Blood Transfus 2019（PMID 30653459）** に差し替え。
- StatPearls の4項目は二次情報のため除外。

**How to apply:** 肩付き番号を節見出し（「11-1 患者群別の目安」など）に置かない。
一度そこに載ってしまい、直前の本文「その「あたり」は患者集団ごとに違う。」へ移した。
