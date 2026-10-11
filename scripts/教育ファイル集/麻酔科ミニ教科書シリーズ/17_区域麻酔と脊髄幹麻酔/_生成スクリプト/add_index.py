# -*- coding: utf-8 -*-
"""総目次に ⑬〜⑰ の巻ブロックを追加する。

既刊⑫のブロック（巻タイトル／サブタイトル／表／空段落／章立て／収録ファイル…）を
deepcopy して、テキストだけ差し替える。
"""
import copy
import io
import os
from docx import Document
from docx.oxml.ns import qn

BASE = (r"C:\Users\junch\OneDrive\デスクトップ\教育ファイル集"
        r"\麻酔科ミニ教科書シリーズ")
PATH = os.path.join(BASE, "00_麻酔科ミニ教科書シリーズ_総目次.docx")

# (巻記号, タイトル, サブタイトル, 作成日, 分量, 図版・付属, 章立て, 収録ファイル)
NEW = [
    ("⑬", "気道管理", "見えるかどうかではなく、酸素化を続けられるか",
     "2026年9月3日", "78 頁 / 78 頁", "図版 20 点・表 9 点",
     "第I部 原則と生理（気道管理が守るもの／上気道が閉じる仕組み／無呼吸で何分もつか）"
     "／第II部 術前の気道評価（病歴と身体所見／スコア・画像・超音波／評価を計画に変える）"
     "／第III部 手技（体位・用手気道確保・マスク換気／声門上器具／喉頭鏡と気管挿管／覚醒下気管挿管）"
     "／第IV部 危機（予期せぬ挿管困難／CICO と緊急前頸部気道確保／特殊な状況）"
     "／第V部 挿管後・抜管・体制（挿管後の管理／抜管と抜管後の気道／組織としての備え）"
     "／付録A〜E（気道評価チェックリスト・困難気道カート・数値の早見・用語集・"
     "確認できなかった記載）",
     ["・気道管理.docx／.pdf", "・図版／（20点）", "・_生成スクリプト／"]),

    ("⑭", "血管確保", "末梢静脈路・橈骨動脈穿刺・観血的動脈圧ライン",
     "2026年9月4日", "65 頁 / 65 頁", "図版 20 点・表 5 点",
     "第I部 総論（3つの手技が守るもの／上肢の血管と神経／超音波の基礎／針先を見失わない）"
     "／第II部 末梢静脈路（サイズと部位／逆血のあとの3手／難しい末梢静脈路／"
     "小児・高齢者・特殊な状況／骨髄路）"
     "／第III部 観血的動脈圧ライン（適応と禁忌／穿刺前の準備／穿刺手技／"
     "留置後の管理 ── その波形を信じてよいか／採血と血液の節約）"
     "／第IV部 合併症と撤退（末梢静脈路／動脈ライン／抜去とやめどきの設計）"
     "／第V部 体制（感染対策／記録・教育・チェックリスト）"
     "／付録A〜F（ゲージ別流量・スクエア波テスト・トランスデューサ高さの誤差・"
     "困ったときの早見表・参考資料・用語小辞典）",
     ["・血管確保.docx／.pdf", "・図版／（20点）", "・_生成スクリプト／"]),

    ("⑮", "手術体位と末梢神経障害",
     "体位は設置作業ではなく、術中ずっと続く生理学的介入である",
     "2026年9月4日", "64 頁 / 64 頁", "図版 21 点・表 3 点",
     "第I部 なぜ神経は傷むのか（重なりで生じる／圧迫・牽引・虚血は別の言葉ではない／"
     "障害の深さと回復の時間軸／頻度の読み方）"
     "／第II部 誰が危ないか（高リスク患者／糖尿病／体格の両極と栄養／30秒プロファイル）"
     "／第III部 体位ごとに何を守るか（対応表／仰臥位と尺骨神経／急峻頭低位と腕神経叢／"
     "腹臥位と側臥位／砕石位と下肢神経／well-leg compartment syndrome／"
     "ロボット骨盤手術／心臓手術の上肢障害）"
     "／第IV部 守り方（パッドは荷重を分散する／長時間症例の再評価）"
     "／第V部 起きたあと（初期対応／術後診察の最小セット／チーム手順）"
     "／付録A〜F（体位と神経の早見表・症状から圧迫点を逆算・チェックリスト・"
     "症例演習・参考資料・用語小辞典）",
     ["・手術体位と末梢神経障害.docx／.pdf", "・図版／（21点）", "・_生成スクリプト／"]),

    ("⑯", "周術期のアナフィラキシーと局所麻酔薬中毒",
     "見た目が似ていて、機序も治療も違う二つを分ける",
     "2026年9月4日", "61 頁 / 61 頁", "図版 19 点・表 7 点",
     "第I部 二つを分ける（似ているのは見た目だけ／治療の分岐点／麻酔下で何が最初の徴候か）"
     "／第II部 局所麻酔薬中毒（効果の延長線上にある／どこにどれだけ入れるか／"
     "誰に起こりやすいか／起きたときの順序／脂肪乳剤／予防の7か条／始める前の準備）"
     "／第III部 アナフィラキシー（麻酔下の見え方／何を疑うか／初期対応／"
     "難治例と二相性反応／起きたあとの仕事）"
     "／第IV部「使えない」と言われたら（既往を分解する／代替薬／効かないとき）"
     "／第V部 体制（裁判事例が教えること／シナリオで練習する／チェックリスト）"
     "／付録A〜G（二つを分ける早見表・対応の順序2種・「使えない」の分解・"
     "参考資料・現場カード・用語小辞典）",
     ["・アナフィラキシーと局所麻酔薬中毒.docx／.pdf", "・図版／（19点）",
      "・_生成スクリプト／"]),

    ("⑰", "区域麻酔と脊髄幹麻酔",
     "手技ではなく、リスクを調整する処方として選ぶ",
     "2026年9月4日", "60 頁 / 60 頁", "図版 19 点・表 5 点",
     "第I部 区域麻酔の設計（手技ではなく処方である／組み立ての順序／"
     "薬物予算 ── 濃度×mL＝mg／抗血栓薬と部位の格付け）"
     "／第II部 脊髄幹麻酔の解剖（背面から脊髄まで／脊髄円錐と穿刺高位／脊髄の血管支配）"
     "／第III部 脊髄くも膜下麻酔（何をしているのか／広がりを決めるもの／"
     "どの高さまで効かせるか／合併症）"
     "／第IV部 硬膜外麻酔（抵抗消失法／カテーテルとテストドーズ／投与量と広がり／硬膜外血腫）"
     "／第V部 超音波と末梢神経ブロック（ランドマークの限界／プレスキャン／"
     "腰椎の超音波／末梢神経ブロックの原則）"
     "／付録A〜H（解剖早見表・くも膜下と硬膜外の比較・プレスキャンの数字・"
     "チェックリスト・参考資料・用語小辞典・症例演習・思ったとおりにならなかったときの早見表）",
     ["・区域麻酔と脊髄幹麻酔.docx／.pdf", "・図版／（19点）", "・_生成スクリプト／"]),
]


def set_para_text(el, text):
    """段落の最初の run に text を入れ、残りの run のテキストを空にする"""
    runs = el.findall(qn("w:r"))
    done = False
    for r in runs:
        ts = r.findall(qn("w:t"))
        for t in ts:
            if not done:
                t.text = text
                t.set(qn("xml:space"), "preserve")
                done = True
            else:
                t.text = ""
    return done


def set_cell_text(tc, text):
    for p in tc.findall(qn("w:p")):
        if set_para_text(p, text):
            return True
    return False


def main():
    doc = Document(PATH)
    body = doc.element.body
    kids = [e for e in body if e.tag in (qn("w:p"), qn("w:tbl"))]

    # ⑫ のブロック範囲を探す（巻タイトル 〜 収録ファイルの最終行）
    start = None
    for i, el in enumerate(kids):
        if el.tag != qn("w:p"):
            continue
        t = "".join(x.text or "" for x in el.iter(qn("w:t")))
        if "⑫" in t and "BIS" in t:
            start = i
            break
    if start is None:
        raise SystemExit("⑫のブロックが見つかりません")
    end = start
    for j in range(start + 1, len(kids)):
        el = kids[j]
        if el.tag == qn("w:p"):
            t = "".join(x.text or "" for x in el.iter(qn("w:t")))
            if any(b.get(qn("w:type")) == "page" for b in el.iter(qn("w:br"))):
                break
            if t.strip():
                end = j
        else:
            end = j
    tmpl = kids[start:end + 1]
    print("template block:", start, "-", end, "(%d elements)" % len(tmpl))

    anchor = kids[end]
    log = []
    for (mark, title, sub, date, pages, figs, outline, files) in NEW:
        new = [copy.deepcopy(e) for e in tmpl]
        paras = [e for e in new if e.tag == qn("w:p")]
        tbls = [e for e in new if e.tag == qn("w:tbl")]
        # paras の並び：[0]巻タイトル [1]サブ [2]空 [3]章立て [4]"収録ファイル" [5..]ファイル行
        set_para_text(paras[0], "　%s　%s" % (mark, title))
        set_para_text(paras[1], sub)
        set_para_text(paras[3], outline)
        # 収録ファイル行を必要数に合わせる
        filelines = paras[5:]
        for k, p in enumerate(filelines):
            if k < len(files):
                set_para_text(p, files[k])
            else:
                new.remove(p)
        if len(files) > len(filelines):
            base = filelines[-1]
            for extra in files[len(filelines):]:
                cp = copy.deepcopy(base)
                set_para_text(cp, extra)
                new.insert(new.index(filelines[-1]) + 1, cp)
        # 表の2行目を書き換える
        rows = tbls[0].findall(qn("w:tr"))
        cells = rows[1].findall(qn("w:tc"))
        for c, v in zip(cells, (date, pages, figs)):
            set_cell_text(c, v)
        for e in new:
            anchor.addnext(e)
            anchor = e
        log.append("追加 %s %s（%s／%s）" % (mark, title, pages, figs))

    # 冒頭の巻数と日付
    for el in body.iter(qn("w:t")):
        if el.text and "既刊 12 巻" in el.text:
            el.text = el.text.replace("既刊 12 巻（本編 12 冊",
                                      "既刊 17 巻（本編 17 冊")
            log.append("冒頭の巻数を更新")
        if el.text and "2026年8月28日 現在" in el.text:
            el.text = el.text.replace("2026年8月28日 現在", "2026年9月4日 現在")
            log.append("日付を更新")
        if el.text and "既刊 12 巻は、" in el.text:
            el.text = el.text.replace("既刊 12 巻は、", "既刊 17 巻は、")
            log.append("末尾の組版基盤の記述を更新（巻数）")

    doc.save(PATH)
    io.open("qa_index_add.txt", "w", encoding="utf-8").write("\n".join(log))
    print("\n".join(log))


if __name__ == "__main__":
    main()
