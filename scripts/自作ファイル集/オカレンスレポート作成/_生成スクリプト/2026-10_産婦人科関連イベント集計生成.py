# -*- coding: utf-8 -*-
import sys
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
out=sys.argv[1]
FONT="メイリオ"
d=Document()
s=d.sections[0]; s.page_height=Mm(297); s.page_width=Mm(210)
s.top_margin=s.bottom_margin=Mm(11); s.left_margin=s.right_margin=Mm(13)
st=d.styles["Normal"]; st.font.name=FONT; st.font.size=Pt(9)
st.element.rPr.rFonts.set(qn("w:eastAsia"),FONT)
st.paragraph_format.space_after=Pt(0); st.paragraph_format.space_before=Pt(0); st.paragraph_format.line_spacing=1.0
NAVY=RGBColor(0x1F,0x3A,0x5F); RED=RGBColor(0xB0,0x1E,0x1E)
def shade(c,hexc):
    tcPr=c._tc.get_or_add_tcPr(); sh=OxmlElement("w:shd"); sh.set(qn("w:val"),"clear"); sh.set(qn("w:color"),"auto"); sh.set(qn("w:fill"),hexc); tcPr.append(sh)
def para(text="",size=9,bold=False,color=None,align=None,after=0,before=0):
    p=d.add_paragraph(); p.paragraph_format.space_after=Pt(after); p.paragraph_format.space_before=Pt(before)
    if align: p.alignment=align
    p.paragraph_format.line_spacing=Pt(max(size,9)*1.35)
    if text:
        r=p.add_run(text); r.font.size=Pt(size); r.bold=bold
        if color: r.font.color.rgb=color
    return p
def head(t):
    p=para(t,10.5,True,NAVY,before=4,after=1)
    pPr=p._p.get_or_add_pPr(); b=OxmlElement("w:pBdr"); bt=OxmlElement("w:bottom")
    for k,v in (("val","single"),("sz","6"),("space","1"),("color","1F3A5F")): bt.set(qn("w:"+k),v)
    b.append(bt); pPr.append(b)
def cellw(c,text,size=8.5,bold=False,color=None,align=None):
    c.text=""; p=c.paragraphs[0]
    if align: p.alignment=align
    r=p.add_run(text); r.font.size=Pt(size); r.bold=bold
    p.paragraph_format.line_spacing=Pt(size*1.3)
    if color: r.font.color.rgb=color
def table(rows,widths,header_fill="1F3A5F",size=9.3,center_cols=(),hl_rows=()):
    t=d.add_table(rows=len(rows),cols=len(rows[0])); t.style="Table Grid"; t.alignment=WD_TABLE_ALIGNMENT.CENTER
    t.autofit=False
    lay=OxmlElement("w:tblLayout"); lay.set(qn("w:type"),"fixed"); t._tbl.tblPr.append(lay)
    for j,w in enumerate(widths): t.columns[j].width=Mm(w)
    for i,row in enumerate(rows):
        for j,v in enumerate(row):
            c=t.cell(i,j); c.width=Mm(widths[j])
            al=WD_ALIGN_PARAGRAPH.CENTER if (j in center_cols or i==0) else None
            if i==0: cellw(c,v,size,True,RGBColor(255,255,255),al); shade(c,header_fill)
            else:
                cellw(c,v,size,i in hl_rows and j==0,None,al)
                if i in hl_rows: shade(c,"FBE9E7")
    return t

para("手術室オカレンスレポート　産婦人科関連イベント集計",15,True,NAVY,WD_ALIGN_PARAGRAPH.CENTER)
para("対象期間：2025年4月〜2026年9月（麻酔科・看護師・臨床工学技士の3職種レポート）",9,False,None,WD_ALIGN_PARAGRAPH.CENTER)
para("作成：麻酔科　玉里順子　2026年10月16日",9,False,None,WD_ALIGN_PARAGRAPH.RIGHT,after=3)

# KPI
t=d.add_table(rows=2,cols=4); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.style="Table Grid"
kp=[("総件数","36件","3職種の合計"),("臓器損傷","3件","膀胱2・尿管1"),("他科の術中介入","2件","泌尿器科1・外科1"),("腸管損傷","0件","明記された報告なし")]
for j,(a,b,c) in enumerate(kp):
    c0=t.cell(0,j); c1=t.cell(1,j); c0.width=c1.width=Mm(46)
    cellw(c0,a,9,True,RGBColor(255,255,255),WD_ALIGN_PARAGRAPH.CENTER); shade(c0,"1F3A5F" if j!=1 else "B01E1E")
    cellw(c1,b,18,True,RED if j==1 else NAVY,WD_ALIGN_PARAGRAPH.CENTER)
    p=c1.add_paragraph(); p.paragraph_format.line_spacing=Pt(10); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; r=p.add_run(c); r.font.size=Pt(8)

head("1．職種別・内容別の件数")
rows=[["内容","麻酔科","看護師","CE","計"],
["術中の臓器損傷・他科の術中介入","4","—","—","4"],
["物品・器材の準備（サイズ違い・不足）","—","4","—","4"],
["検体・標本・リンパ節の左右／取り扱い","—","4","—","4"],
["麻酔体制・連絡・手術順の調整","—","4","—","4"],
["薬剤・麻薬管理","—","2","—","2"],
["カウント（綿球の一時不明）","—","1","—","1"],
["術後の重大事象（声帯麻痺→気管切開）","—","1","—","1"],
["手術時間の延長","1","—","—","1"],
["機器：映像・記録系（内視鏡トロリー等）","—","—","4","4"],
["機器：麻酔器・モニタ・麻酔チャート","—","—","4","4"],
["機器：エネルギーデバイス・ロボット鉗子","—","1","3","4"],
["機器：気腹装置・手台","—","—","3","3"],
["合計","5","17","14","36"],
]
table(rows,[104,20,20,20,20],center_cols=(1,2,3,4),hl_rows=(1,))
t=d.tables[-1]
for j in range(5):
    c=t.cell(len(rows)-1,j); shade(c,"E8EEF5"); 
    for r in c.paragraphs[0].runs: r.bold=True
para("内訳：産科（帝王切開）5件・婦人科31件。看護師は2026年9月のエネルギーデバイス不具合1件を含む。",8.8,after=0)

head("2．術中の臓器損傷・他科の術中介入（4件）")
rows2=[["報告月","術式","事象","対応"],
["2026年3月","婦人科手術","尿管損傷","泌尿器科医をコール"],
["2026年4月","帝王切開","膀胱損傷","—"],
["2026年7月","産婦人科手術","外科の術中介入","—"],
["2026年9月","腹式子宮全摘＋両側付属器切除（ATH＋BSO）","膀胱損傷","—"],
]
table(rows2,[26,70,34,54],header_fill="B01E1E",center_cols=(0,))
para("いずれも麻酔科レポート「その他・重要なもの」欄の記載。腸管損傷と明記された報告はなし。",8.8)
para("参考（診療科の記載なし）：2025年5月「ポート挿入時に腸管に接触し外科介入」、2025年10月「膀胱が術野の妨げとなりドレープ下から尿道カテーテル挿入」。",8.8,after=0)

head("3．看護師・CE報告の主な事例")
items=[
("術後の重大事象","子宮全摘後、病棟帰室後に声帯麻痺で呼吸状態が悪化し緊急気管切開（2025年10月）"),
("検体・左右","リンパ節の左右取り違え・ボックス入れ間違い（同日3件、2025年11月）、標本をガーゼに包んだまま下ろしかけた（2026年1月）"),
("薬剤・麻薬","20万倍ボスミン指示に外用ボスミン5mgを準備（2026年1月）、帝王切開後のフェンタニル伝票を白紙で申し送り（2025年8月）"),
("体制・連絡","超緊急帝王切開で麻酔科医への連絡が届かず入室時に不在（2025年8月）、子宮筋腫合併帝王切開で末梢ルート1本のまま出血（2025年7月）"),
("物品準備","ポート・ルミⅡなどのサイズ違い2件、キット不足、バルーン重複（2025年7〜12月）"),
("機器","5番室の内視鏡トロリー映像系とバイクランプ・電気メスの不具合が反復、ロボット鉗子ワイヤー離断（2026年1月）、ソニックビート3本不具合（2026年9月）"),
]
rows3=[["区分","事例"]]+[[a,b] for a,b in items]
table(rows3,[32,152],size=9)

head("4．まとめと今後の対応")
for tx in [
"・臓器損傷3件（膀胱2・尿管1）はすべて2026年に入ってからの報告で、医療安全で事例検討を行う。報告が増えたのは術中事象を拾い上げる文化が根づいてきた表れであり、安全性は件数ではなく個々の重大性で評価する。",
"・婦人科手術で尿路損傷が疑われたときの泌尿器科コールの手順と、術前の尿管ステント留置の適応を産婦人科と共有する。",
"・検体の左右・ラベル確認は、リンパ節採取時に術者と器械出しが声に出して確認する運用を徹底する。",
"・5番室の映像系・エネルギーデバイスはCEの定期点検の重点項目とし、予備機の配置を確認する。",
]:
    para(tx,9.3,after=1)
para("集計対象：麻酔科 2025年4月〜2026年9月（2026年6月・8月を除く）、看護師 2025年6月〜2026年9月、CE 2025年4月〜2026年3月および2026年9月。麻酔科は診療科・術式が記載された事象を計上。",7.5,color=RGBColor(0x55,0x55,0x55),before=3)
d.save(out)
