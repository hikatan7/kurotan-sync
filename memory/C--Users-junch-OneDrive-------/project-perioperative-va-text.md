---
name: project-perioperative-va-text
description: 周術期VPC/VTの4頁テキスト（教育ファイル集）と、そこで採用した記載方針の修正点
metadata: 
  node_type: memory
  type: project
  originSessionId: 413e5bd9-be7b-47e4-9f22-24780b16b9d3
  modified: 2026-08-21T09:40:26.694Z
---

デスクトップ「教育ファイル集」直下に
`周術期の心室性不整脈_VPC・VTが散発したとき_4頁テキスト.docx / .pdf`（2026-08-21、専門医向け全9節・A4×4頁）。

ユーザー指示で、旧来よく書かれる記載を次のように改めた。**周術期不整脈の資料を今後作るときはこの方針を踏襲する。**

- **GIK（虚血関連VPC/VTへのブドウ糖・インスリン・K）は削除**。CREATE-ECLA（20,201例）で改善せず、標準治療ではない。
- **リドカインは格下げ**。「VPCが多いからリドカイン」は不可。AMIへのルーチン予防投与は非推奨（Cochrane、asystole増加）。虚血性VAでは今も可。
- **ランジオロールを前面に**（エスモロールより日本臨床向き）。難治性VT/VFで1→1〜10 µg/kg/min、状況により最大40。
- **TdPは多形性VTと分けて独立の章**。QT正常の多形性VTはまず急性虚血。
- **VTとVFを分ける**。脈ありの不安定VT＝同期カルディオバージョン／VF・無脈性VT＝非同期除細動＋CPR。
- **PVC burdenは ≥10% を精査閾値、>20% でリスク上昇**（「≥10〜15%」とは書かない）。
- **「PVC ≥6/分ならリドカイン」はLown由来の歴史的基準**として扱う。
- **「K>4.0、Mg>2.0」を普遍的目標値として書かない**。TdPでは「低Kを正常高値側へ、Mg投与、QT延長薬中止」と記す。
- アミオダロンはACLSレジメンと日本の添付文書用法が異なる旨を必ず注記。安定持続性単形性VTはPROCAMIO（MACE 9% vs 41%）を踏まえプロカインアミドも併記。

**Why:** 原稿にあった旧記載をそのまま流用すると、現行ガイドラインから外れた資料になる。
**How to apply:** 作成環境は [[env-word-com-doc-generation]]、頁数合わせは [[workflow-docx-exact-page-count]]。配置先は [[project-education-file-collection]]。
