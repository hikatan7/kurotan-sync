---
name: project-vascular-access-text
description: 「血管確保の実際」10頁テキスト（末梢静脈・橈骨動脈・動脈圧ライン）の所在と作り方
metadata: 
  node_type: memory
  type: project
  originSessionId: 279dc8db-9411-4950-96bf-1e0613e17051
  modified: 2026-08-21T05:57:28.345Z
---

**2026-09-04：この10頁テキストを土台に [[project-vascular-access-textbook]]（ミニ教科書⑭・65頁）を作った。以後はそちらが本体。**

2026-08-21 作成。`デスクトップ\動脈圧ライン\血管確保の実際_10頁.pdf`（A4・10頁）。

**素材**：同フォルダの `動脈穿刺・観血的動脈圧ライン確保.pdf`（Manus AI 作成・11頁）を土台に、
**末梢静脈ライン確保の章を新規に書き足して**3手技をそろえた。
同フォルダの提供図版4点（`01_upper_extremity_anatomy_and_ultrasound.jpg` ほか）を本文に配置。

**構成**：①総論と4原則 ②上肢の血管・神経の超音波解剖 ③静脈ライン（ゲージと流量・部位）
④静脈ライン（逆血後の3手・US ガイド）⑤動脈ライン（適応・準備・回路）⑥短軸法とDNTP
⑦長軸法と逆血後 ⑧波形とライン管理 ⑨合併症（Scheer 2002 の頻度表）⑩まとめ。

**図版の出典が未確定**：提供4点は Cho SA, et al. Anesth Pain Med (Seoul) 2021;16:119-132 の
図と内容が一致するが確証がないため、暫定で「出典：提供図版（院内教育用）」と入れてある。
**配布前に原典の出典表記へ差し替えること。**

**ビルド**：scratchpad の `aline/` に [[project-perioperative-reader-50p]] の engine.py／svglib.py を
コピーし、以下を足して使った（同じ HTML→Chrome print-to-pdf 方式、1ページ＝1ユニット）。
- `imgfig(src, cap, credit, width)` … 画像＋キャプション＋出典行。widthは % で指定して高さを調整する。
  A4本文幅176 mm なので、縦横比 h/w の画像は `width%×176×h/w` mm を占める。先に電卓で当てる。
- `phead(num, title, sub)` … ページ冒頭の番号つき見出し帯。`two(a, b, ratio)` … 2カラム。
- `Book.page()` の柱は「第N章」固定をやめ、任意ラベルにした。
- build.py の充填率チェックは `page.get_image_info()` の bbox も見て最下端を出す（画像で溢れるため）。
- 画像は base64 にせず、HTMLと同じフォルダに置いて相対パス参照でよい（Chrome が file:// で読む）。
