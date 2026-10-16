# -*- coding: utf-8 -*-
"""詳細版・専攻医用テキストの docx を組む。

  python build.py detail     → 心臓手術後の心停止_詳細版.docx
  python build.py resident   → 心臓手術後の心停止_専攻医用.docx
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH
import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para, page_break,
                     heading, toc_field, figure, table, bullets, summary, note, reflist,
                     NAVY, GREY, TEAL)
import refs

OUTDIR = os.path.join(HERE, "..")
FIGDIR = os.path.join(HERE, "..", "図版")
DATE = "2026 年 9 月 27 日（9 月 28 日改訂）"

ABBR = (["略語", "英語", "日本語"],
        [["ACLS", "advanced cardiovascular life support", "AHA の二次救命処置（コース）"],
         ["ALS", "advanced life support", "二次救命処置"],
         ["CALS", "Cardiac Surgery Advanced Life Support", "心臓手術後二次救命処置"],
         ["COR／LOE", "class of recommendation／level of evidence", "推奨クラス／エビデンスレベル（読み方は第2章）"],
         ["CSU-ALS", "Cardiac Surgical Unit-Advanced Life Support", "米国での CALS の呼び名"],
         ["DC", "direct current (defibrillation)", "直流通電（電気的除細動）"],
         ["DDD／VVI", "pacing modes", "心房と心室を感知・刺激する設定／心室だけを感知・刺激する設定"],
         ["ECLS", "extracorporeal life support", "体外式生命維持"],
         ["ECPR", "extracorporeal cardiopulmonary resuscitation", "体外循環式心肺蘇生"],
         ["HCU", "high care unit", "高度治療室"],
         ["ICLS", "Immediate Cardiac Life Support", "日本救急医学会の院内心停止対応コース"],
         ["EtCO2", "end-tidal carbon dioxide", "呼気終末二酸化炭素分圧"],
         ["IABP", "intra-aortic balloon pumping", "大動脈内バルーンパンピング"],
         ["LVAD", "left ventricular assist device", "左室補助人工心臓"],
         ["MICS", "minimally invasive cardiac surgery", "低侵襲心臓手術"],
         ["PEA", "pulseless electrical activity", "無脈性電気活動"],
         ["PEEP", "positive end-expiratory pressure", "呼気終末陽圧"],
         ["TAVI", "transcatheter aortic valve implantation", "経カテーテル大動脈弁植込み術"],
         ["TEE", "transesophageal echocardiography", "経食道心エコー"],
         ["VA-ECMO", "veno-arterial extracorporeal membrane oxygenation", "静脈脱血・動脈送血の体外式膜型人工肺"],
         ["VF／VT", "ventricular fibrillation／ventricular tachycardia", "心室細動／心室頻拍"]])

ABBR_RES = (["略語", "読み・英語", "日本語での意味"],
            [["CALS", "キャルス／Cardiac Surgery Advanced Life Support", "心臓手術後の二次救命処置（この資料の主題）"],
             ["ICLS", "アイシーエルエス／Immediate Cardiac Life Support", "日本救急医学会の院内二次救命処置コース"],
             ["ALS・ACLS", "advanced (cardiovascular) life support", "二次救命処置（標準の手順）"],
             ["ICU", "intensive care unit", "集中治療室"],
             ["VF／VT", "ventricular fibrillation／tachycardia", "心室細動／心室頻拍"],
             ["PEA", "pulseless electrical activity", "無脈性電気活動（波形はあるのに脈がない）"],
             ["ROSC", "return of spontaneous circulation", "自己心拍再開"],
             ["DDD", "—", "心房と心室の両方をペーシング・感知するモード"],
             ["SpO2", "—", "経皮的動脈血酸素飽和度"],
             ["EtCO2", "end-tidal CO2", "呼気終末二酸化炭素分圧"],
             ["FiO2", "fraction of inspired oxygen", "吸入酸素濃度"],
             ["PEEP", "positive end-expiratory pressure", "呼気終末陽圧"],
             ["ECLS", "extracorporeal life support", "体外式生命維持（VA-ECMO・人工心肺など）"],
             ["ECPR", "extracorporeal CPR", "体外循環式心肺蘇生"],
             ["VA-ECMO", "veno-arterial ECMO", "静脈脱血・動脈送血の体外式膜型人工肺"],
             ["MICS", "minimally invasive cardiac surgery", "低侵襲心臓手術（小開胸など）"],
             ["TAVI", "transcatheter aortic valve implantation", "経カテーテル大動脈弁植込み術"],
             ["AHA", "American Heart Association", "米国心臓協会（蘇生ガイドラインの発行元）"],
             ["ERC", "European Resuscitation Council", "欧州蘇生協議会"],
             ["STS", "Society of Thoracic Surgeons", "米国胸部外科学会"],
             ["EACTS", "European Association for Cardio-Thoracic Surgery", "欧州心臓胸部外科学会"],
             ["推奨クラス", "Class 1／2a／III", "1＝強く推奨、2a＝妥当、III＝行わない（harm は有害）"],
             ["LOE", "B-NR／C-EO", "エビデンスレベル。B-NR＝非ランダム化研究、C-EO＝専門家の意見"]])

KINDS = {
    "detail": dict(
        module="text_detail",
        out="心臓手術後の心停止_詳細版.docx",
        kicker="ICLS インストラクター用資料　詳細版",
        title="心臓手術後の心停止",
        sub="── ICLS と何が違うか（CALS の要点と教え方）──",
        lines=["AHA 2025・ERC 2025・STS 2017・EACTS 2009 と国内の報告にもとづく",
               "根拠・ガイドライン・教え方・追加シナリオ・当院チャートとの照合"],
        footer="心臓手術後の心停止（詳細版）　　",
        toc=True, abbr=True),
    "resident": dict(
        module="text_resident",
        out="心臓手術後の心停止_専攻医用.docx",
        kicker="専攻医用テキスト",
        title="心臓手術後の心停止",
        sub="── 最初の 1 分と 5 分 ──",
        lines=["麻酔科専攻医のための要点と確認問題"],
        footer="心臓手術後の心停止（専攻医用）　　",
        toc=False, abbr=True, abbr_table=ABBR_RES),
}


def build(kind):
    k = KINDS[kind]
    mod = __import__(k["module"])
    res = refs.Resolver()
    bookkit.set_cite_resolver(res)
    doc = new_document()
    set_footer(doc, k["footer"])

    # ---- 表紙（院内文書：表題の下・右寄せに作成者）
    for _ in range(3):
        para(doc)
    para(doc, k["kicker"], size=12, bold=True, color=TEAL, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, k["title"], size=26, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4)
    para(doc, k["sub"], size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "作成：麻酔科　玉里順子", size=11, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=10)
    para(doc)
    for ln in k["lines"]:
        para(doc, ln, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
    for _ in range(5):
        para(doc)
    para(doc, "作成日　%s" % DATE, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "静岡市立静岡病院　麻酔科", size=11.5, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)

    if k["toc"]:
        para(doc, "目　次", size=16, bold=True, color=NAVY,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
        toc_field(doc)
    if k["abbr"]:
        h = heading(doc, "この資料で使う略語", 2)
        if k["toc"]:
            h.paragraph_format.page_break_before = True
        else:
            para(doc, "本文では、初めて出てくる略語に日本語を添えている。図の中の略語はこの表で確かめてほしい。",
                 size=9.5, color=GREY)
        ab = k.get("abbr_table", ABBR)
        table(doc, None, ab[0], ab[1])

    first_h2 = True
    for b in mod.BLOCKS:
        t = b[0]
        if t == "h2":
            hh = heading(doc, b[1], 2)
            if kind == "detail" and b[1].startswith(("第1章", "付録A")):
                hh.paragraph_format.page_break_before = True
            first_h2 = False
        elif t == "h3":
            heading(doc, b[1], 3)
        elif t == "p":
            assert isinstance(b[1], str)
            para(doc, b[1])
        elif t == "ul":
            assert isinstance(b[1], list)
            bullets(doc, b[1])
        elif t == "fig":
            figure(doc, os.path.join(FIGDIR, b[1]), b[2], width_cm=16.0)
        elif t == "tbl":
            table(doc, None, b[1], b[2])
        elif t == "sum":
            assert isinstance(b[2], list)
            summary(doc, b[1], b[2])
        elif t == "note":
            assert isinstance(b[2], list)
            note(doc, b[1], b[2])
        else:
            raise ValueError(t)

    h = heading(doc, "参考文献", 2)
    if kind == "detail":
        h.paragraph_format.page_break_before = True
    para(doc, "本文の肩付き番号はこの一覧の番号に対応する。PubMed 収載のものは PMID を、"
              "それ以外は DOI または発行元を記した。2026 年 9 月 27 日に照合した。", size=9.5, color=GREY)
    reflist(doc, res.rows())
    if res.missing:
        print("!! 台帳にない ID:", sorted(res.missing))
    drop_orphan_blanks(doc)
    # 末尾の空段落を落とす（白紙の最終頁を防ぐ）
    body = doc.element.body
    while True:
        ps = [e for e in body if e.tag.endswith("}p")]
        last = ps[-1] if ps else None
        if last is None or "".join(last.itertext()).strip() or last.getnext() is None:
            break
        if last.getnext().tag.endswith("}sectPr"):
            body.remove(last)
        else:
            break
    out = os.path.join(OUTDIR, k["out"])
    doc.save(out)
    print(kind, "refs=%d paras=%d" % (len(res.order), len(doc.paragraphs)), out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for kind in (sys.argv[1:] or ["detail", "resident"]):
        build(kind)
