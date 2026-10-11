# -*- coding: utf-8 -*-
"""BISモニター②専攻医向け を、区画ごとのスライドに組み直す（文字 16〜19pt）。
元のスライドの部品（帯・見出し・表の行・カード）を雛形として複製するので配色は変わらない。"""
import copy, re, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.oxml.ns import qn
from pptx.opc.packuri import PackURI

SRC = sys.argv[1]
DST = sys.argv[2]
pr = Presentation(SRC)
E = 914400
RNS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
S = list(pr.slides)


def find(slide, x, y, w=None, kind=None):
    for sh in slide.shapes:
        if abs(sh.left / E - x) < 0.02 and abs(sh.top / E - y) < 0.02 and (w is None or abs(sh.width / E - w) < 0.02):
            if kind is None or sh.shape_type == kind:
                return sh
    raise KeyError((x, y, w))


s2, s3, s4, s5, s6 = S[1], S[2], S[3], S[4], S[5]
T = {
    'hbg': find(s2, 0.70, 1.32, 6.15), 'htx': find(s2, 0.84, 1.32),
    'body': find(s2, 0.82, 1.86),
    'thbg': find(s2, 6.90, 1.32, 6.00), 'thtx': find(s2, 6.98, 1.32),
    'rbg': find(s2, 6.90, 1.76, 6.00, 1), 'rtx': find(s2, 6.98, 1.76),
    'rline': find(s2, 6.90, 1.76, 6.00, 9),
    'nbg': find(s2, 6.90, 4.70, 6.00), 'ntx': find(s2, 7.08, 4.70),
    'cbg': find(s4, 0.70, 1.30, 3.82), 'cacc': find(s4, 0.70, 1.30, 0.07),
    'ctt': find(s4, 0.94, 1.42), 'ctx': find(s4, 0.94, 1.92),
    'pic': find(s3, 0.35, 1.25),
}
HEADER_Y = 1.0      # 帯の下端（インチ）


def clone_header(src_slide):
    """帯・タイトル・ラベル・ページ番号・最下段の帯だけを持つ新しいスライド"""
    ns = pr.slides.add_slide(src_slide.slide_layout)
    import uuid
    ns.part.partname = PackURI('/ppt/slides/n_%s.xml' % uuid.uuid4().hex[:8])
    for ph in list(ns.placeholders):
        ph._element.getparent().remove(ph._element)
    for sh in src_slide.shapes:
        t = sh.top / E
        if t < HEADER_Y + 0.05 or t >= 6.55:
            ns.shapes._spTree.append(copy.deepcopy(sh._element))
    return ns


def relink(ns, el, src_slide):
    for node in el.iter():
        rid = node.get('{%s}embed' % RNS)
        if rid and rid in src_slide.part.rels:
            rel = src_slide.part.rels[rid]
            node.set('{%s}embed' % RNS, ns.part.relate_to(rel.target_part, rel.reltype))


def put(ns, key, x, y, w, h, lines=None, size=None, bold=None, src=None):
    tpl = T[key]
    el = copy.deepcopy(tpl._element)
    ns.shapes._spTree.append(el)
    if key == 'pic':
        relink(ns, el, s3)
    sh = ns.shapes[-1]
    sh.left, sh.top, sh.width, sh.height = int(x * E), int(y * E), int(w * E), int(h * E)
    if lines is not None and sh.has_text_frame:
        tf = sh.text_frame
        p0 = tf.paragraphs[0]
        tmpl = copy.deepcopy(p0._p)
        txBody = p0._p.getparent()
        for p in list(tf.paragraphs):
            txBody.remove(p._p)
        for ln in lines:
            np_ = copy.deepcopy(tmpl)
            rs = np_.findall(qn('a:r'))
            for r in rs[1:]:
                np_.remove(r)
            for br in np_.findall(qn('a:br')):
                np_.remove(br)
            if rs:
                rs[0].find(qn('a:t')).text = ln
                rpr = rs[0].find(qn('a:rPr'))
                if rpr is not None:
                    if size:
                        rpr.set('sz', str(int(size * 100)))
                    if bold is not None:
                        rpr.set('b', '1' if bold else '0')
            txBody.append(np_)
        tf.word_wrap = True
        for p in tf.paragraphs:
            for r in p.runs:
                if size:
                    r.font.size = Pt(size)
                if bold is not None:
                    r.font.bold = bold
    return sh


def set_title(ns, title, label, key):
    if key == '':
        for sh in list(ns.shapes):
            if sh.top / E > 6.5 and sh.width / E > 10:
                sh._element.getparent().remove(sh._element)
    for sh in ns.shapes:
        if not sh.has_text_frame:
            continue
        t = sh.text_frame.text
        if not t.strip() or not sh.text_frame.paragraphs[0].runs:
            continue
        if sh.top / E < 0.3 and sh.left / E < 1 and sh.width / E > 5:
            sh.text_frame.paragraphs[0].runs[0].text = title
            for r in sh.text_frame.paragraphs[0].runs[1:]:
                r.text = ''
        elif sh.top / E < 0.3 and sh.left / E > 9:
            sh.text_frame.paragraphs[0].runs[0].text = label
            for r in sh.text_frame.paragraphs[0].runs[1:]:
                r.text = ''
        elif sh.top / E > 6.5 and sh.width / E > 10 and key == '':
            pass
        elif sh.top / E > 6.5 and sh.width / E > 10 and key is not None:
            r0 = sh.text_frame.paragraphs[0].runs[0]
            r0.text = key
            for r in sh.text_frame.paragraphs[0].runs[1:]:
                r.text = ''
            r0.font.size = Pt(16)


def heading(ns, x, y, w, text, size=18):
    put(ns, 'hbg', x, y, w, 0.52)
    put(ns, 'htx', x + 0.14, y, w - 0.28, 0.52, [text], size)


def table(ns, x, y, widths, head, rows, size=17, hsize=17, rh=0.62):
    W = sum(widths)
    put(ns, 'thbg', x, y, W, 0.56)
    cx = x
    for wd, h in zip(widths, head):
        put(ns, 'thtx', cx + 0.08, y, wd - 0.12, 0.56, [h], hsize)
        cx += wd
    yy = y + 0.56
    for k, r in enumerate(rows):
        if k % 2 == 0:
            put(ns, 'rbg', x, yy, W, rh)
        cx = x
        for wd, c in zip(widths, r):
            put(ns, 'rtx', cx + 0.08, yy, wd - 0.12, rh, [c], size)
            cx += wd
        put(ns, 'rline', x, yy, W, 0)
        yy += rh
    put(ns, 'rline', x, yy, W, 0)
    return yy


def cards(ns, x, y, w, h, items, cols, tsize=18, bsize=16, gap=0.25):
    cw = (w - gap * (cols - 1)) / cols
    for i, (t, body) in enumerate(items):
        c, r = i % cols, i // cols
        cx = x + c * (cw + gap)
        cy = y + r * (h + gap)
        put(ns, 'cbg', cx, cy, cw, h)
        put(ns, 'cacc', cx, cy, 0.07, h)
        put(ns, 'ctt', cx + 0.24, cy + 0.12, cw - 0.4, 0.5, [t], tsize)
        put(ns, 'ctx', cx + 0.24, cy + 0.65, cw - 0.4, h - 0.75, body, bsize)


X0, WF = 0.7, 11.93
new = []

# 1. 読む順番
ns = clone_header(s2); set_title(ns, '① 読み方の型 ― 読む順番と、BISが測っていないもの', 'まずここ', '①②を飛ばすと、アーチファクトを「所見」として読んでしまう。')
heading(ns, X0, 1.35, WF, 'BISを読む順番（視線を固定する）')
put(ns, 'body', X0 + 0.15, 1.98, WF - 0.3, 2.6, [
    '① SQI ― この数字を信じてよいか。低ければ解釈を保留',
    '② EMG ― 高ければ BIS は高めに出ている（偽高値）',
    '③ SR ― 0%でなければ深すぎる。時間を読む',
    '④ raw EEG ― 最終判断はここでする'], 20)
heading(ns, X0, 4.65, WF, 'BISが測っていないもの')
put(ns, 'body', X0 + 0.15, 5.25, WF - 0.3, 1.2, [
    '・鎮痛　・不動　・麻酔薬濃度　・脳灌流　・皮質下の状態',
    '「BIS 50 だから鎮痛は足りている」は成り立たない。'], 18)
new.append(ns)

# 2. 数字の意味
ns = clone_header(s2); set_title(ns, '① 読み方の型 ― 数字の意味と、次に見るもの', 'まずここ',
                                 '数字は境界であってスイッチではない。BIS 41 と 39 の間に生理学的な断崖はない。')
yy = table(ns, X0, 1.35, [2.2, 4.6, 5.13], ['BIS', '解釈', '次に見るもの'], [
    ['60以上', '浅い／偽高値', 'EMG・薬剤・投与経路'],
    ['40–60', '一般的な全身麻酔域', 'raw EEGの形'],
    ['30–40', '深めの催眠', 'SR・raw EEG'],
    ['20–30', 'かなり深い', 'SR・raw EEG（必須）'],
    ['20未満', 'burst suppression〜無活動', '循環・体温・電極']], size=18, hsize=18, rh=0.6)
put(ns, 'nbg', X0, yy + 0.25, WF, 1.15)
put(ns, 'ntx', X0 + 0.2, yy + 0.25, WF - 0.4, 1.15, [
    '「40〜60」は指針に書かれた数字ではない。日本麻酔科学会の指針（2019年 第4回改訂）は',
    '「脳波モニターは必要に応じて装着すること」とのみ記載している。'], 16)
new.append(ns)

# 3. 図：BIS が下がったときの順番
ns = clone_header(s3); set_title(ns, '② BIS が下がったときに踏む順番', '現場で最も使う', 'BIS 40以下＝burst suppression ではない。区別できるのは SR と raw EEG だけ。')
pw = 5.6 / 4.48 * 6.0          # 縦 5.3in に合わせた幅
ph = 5.35
put(ns, 'pic', (13.33 - ph * 6.0 / 4.48) / 2, 1.12, ph * 6.0 / 4.48, ph)
new.append(ns)

# 4. 40以下の原因 ＋ 60以上
ns = clone_header(s3); set_title(ns, '② 深すぎ・浅すぎの見分けと対処', '現場で最も使う', '偽高値にプロポフォールを足すと、不要な深麻酔を作る。')
heading(ns, X0, 1.25, WF, 'BIS 40以下 ― 原因は1つではない', 17)
yy = table(ns, X0, 1.85, [2.7, 5.0, 4.23], ['原因', '見分け方', '対処'], [
    ['麻酔薬が多い', '薬剤量・呼気濃度と一致', '減量'],
    ['高齢・脆弱脳', '80歳超、術前の認知機能低下', '減量。目標を45–55へ'],
    ['低体温', '体温低下と一致（1℃で約1）', '加温。薬効と誤らない'],
    ['低灌流・低血圧', 'MAP低下・出血・乳酸上昇', '循環を治す'],
    ['電極不良', 'SQI低下・値の突然の跳び', '装着確認。判断保留']], size=16.5, hsize=16.5, rh=0.47)
heading(ns, X0, yy + 0.15, WF, 'BIS 60以上 ― 薬を足す前に', 17)
put(ns, 'body', X0 + 0.15, yy + 0.72, WF - 0.3, 1.2, [
    '・本物：投与の中断／強い侵害刺激／自律神経徴候／α紡錘の消失',
    '・偽物：EMG上昇／筋弛緩の回復／ケタミン等／電気的干渉'], 17)
new.append(ns)

# 5. 落とし穴：薬剤・患者
ns = clone_header(s4); set_title(ns, '③ 落とし穴 ― 薬剤と患者背景', '事故に近い順', '')
cards(ns, X0, 1.3, WF, 2.45, [
    ('レミマゾラム', ['同じ深さでもBISは高値。EMGの影響も受けやすい。', '目標値は未確立。60台を理由に増量しない']),
    ('ケタミン', ['β・γが増え、意識がなくてもBISは下がらない／上がる。', '投与後の上昇に催眠薬で反応しない']),
    ('筋弛緩薬', ['EMGが消えて見かけ上BISが低下。', '拮抗後の上昇は覚醒とは限らない']),
    ('デクスメデトミジン', ['BISは低いのに呼びかけで覚醒する。', '数字と反応が乖離する']),
    ('高齢者', ['α振幅が低下し、同じ薬量で深くなる。', 'BIS 45 と SR 8% が同居しうる（80歳超 OR 10.59）']),
    ('小児', ['1歳未満での妥当性は確立していない。', '高濃度セボフルランではてんかん様波が出る'])], 3, tsize=20, bsize=18)
new.append(ns)

# 6. 高く出る・低く出る要因
ns = clone_header(s4); set_title(ns, '③ 落とし穴 ― BISを高く・低く見せる要因', '事故に近い順',
                                 '説明のつかない値の跳びで、他のバイタルが静かなら、まず機械（SQI → 装着 → ノイズ源）。')
hw = (WF - 0.3) / 2
heading(ns, X0, 1.35, hw, 'BISが高く出る要因')
put(ns, 'body', X0 + 0.15, 1.98, hw - 0.3, 4.4, ['・EMG（前頭筋・シバリング・体動）', '・スキサメトニウム', '・電気メス', '・温風式加温装置',
                                                   '・顔面神経モニタリング', '・ケタミン／N₂O／レミマゾラム'], 18)
heading(ns, X0 + hw + 0.3, 1.35, hw, 'BISが低く出る要因')
put(ns, 'body', X0 + hw + 0.45, 1.98, hw - 0.3, 4.4, ['・低体温（1℃あたり約1）', '・低灌流・低血圧・心停止', '・筋弛緩薬（EMGが消える）',
                                                        '・電極不良／剥離', '・低血糖・低酸素・重症脳症', '・高齢／脆弱脳'], 18)
new.append(ns)

# 7. エビデンス表
ns = clone_header(s5); set_title(ns, '④ エビデンス早見 ― 試験と主要結果', '第6章', '')
table(ns, X0, 1.25, [2.75, 1.0, 3.3, 4.88], ['試験', '年', '比較', '主要結果'], [
    ['B-Aware', '2004', 'BIS vs 通常管理', '術中覚醒 0.17% vs 0.91%（約82%減）'],
    ['B-Unaware / BAG-RECALL', '2008/11', 'BIS vs 呼気麻酔薬濃度', '差なし'],
    ['NAP5（監査）', '2014', '—', '覚醒 約1/19,600、筋弛緩下 約1/8,200'],
    ['Cochrane', '2019', 'BIS vs 臨床徴候／呼気濃度', '臨床徴候比では減らす可能性（確実性は低い）'],
    ['ENGAGES', '2019', 'EEGガイド vs 通常管理', 'せん妄 26.0% vs 23.0%（差なし）'],
    ['ENGAGES-Canada', '2024', 'EEGガイド（心臓外科）', 'せん妄 18.15% vs 18.10%（差なし）'],
    ['BALANCED 本体', '2019', 'BIS 35 vs 50（n=6,644）', '1年死亡 7.2% vs 6.5%（差なし）'],
    ['BALANCED せん妄解析', '2021', 'BIS 35 vs 50（n=655）', 'せん妄 28% vs 19%（OR 0.58）']], size=15, hsize=16, rh=0.62)
new.append(ns)

# 8. 読み分け
ns = clone_header(s5); set_title(ns, '④ エビデンス早見 ― 何が言えて、何が言えないか', '第6章',
                                 '代替指標のない TIVA＋筋弛緩 が、BISの意義が最も大きい状況。吸入麻酔なら呼気濃度という優れた代替がある。')
cards(ns, X0, 1.4, WF, 2.35, [
    ('読み分け①', ['「モニターを見せる」介入ではせん妄は減らなかった', '（ENGAGES／ENGAGES-Canada）']),
    ('読み分け②', ['「深さそのもの」を割り付けた試験では減った（BALANCEDせん妄解析）', 'ただし死亡には差なし']),
    ('読み分け③', ['burst suppressionとせん妄はメタ解析でOR 1.49〜1.68', '関連であって因果ではない']),
    ('Cochrane 2019 の結論', ['臨床徴候と比べると術中覚醒を減らす可能性（確実性は低い）', '呼気濃度と比べると差の証拠なし'])], 2, tsize=19, bsize=17)
new.append(ns)

# 9. 5か条と維持中の実務
ns = clone_header(s6); set_title(ns, '⑤ 明日からの実践 ― 5か条と維持中の実務', 'まとめ', '')
heading(ns, X0, 1.25, WF, '専攻医が覚える5つ', 17)
put(ns, 'body', X0 + 0.15, 1.8, WF - 0.3, 2.7, ['① BIS 40〜60は目安。安全域の保証ではない', '② BIS <40 は深麻酔を疑う。数字だけで判断しない',
                                                 '③ BIS ≒20 は burst suppression を疑い、SRとraw EEGを見る', '④ 最低値より「時間」。SR>0 が何分あったか',
                                                 '⑤ BISは raw EEG の代用品ではない'], 18)
heading(ns, X0, 4.6, WF, '維持中の実務', 17)
put(ns, 'body', X0 + 0.15, 5.15, WF - 0.3, 1.8, ['・目標は「SRを0%に保つ」。高齢者は45〜55　・30分ごとに raw EEG と SR を確認（1回10秒）',
                                                 '・導入時はBISの低下を待たない（表示は20〜30秒遅れる）　・急速投与を避ける。高齢者では特に緩徐に',
                                                 '・BISが動いたら SQI → EMG → 薬剤 → 循環 → 体温'], 17)
new.append(ns)

# 10. 記録
ns = clone_header(s6); set_title(ns, '⑤ 明日からの実践 ― 麻酔記録に残すこと', 'まとめ', None)
heading(ns, X0, 1.35, WF, '術後せん妄を振り返るとき、役に立つのはこの4つ')
put(ns, 'body', X0 + 0.15, 1.98, WF - 0.3, 3.0, ['① SR>0（またはBIS<40）だった時間の合計', '② その時間帯の血圧・体温・薬剤量',
                                                   '③ アーチファクトがあった場合、その原因と対処', '④ ケタミン・レミマゾラムなど解釈に影響する薬剤'], 20)
put(ns, 'nbg', X0, 4.75, WF, 1.4)
put(ns, 'ntx', X0 + 0.25, 4.75, WF - 0.5, 1.4, ['「BISが70になった時点でEMGを確認し、鎮痛を追加した」と一行あれば、',
                                                  'それが臨床判断の記録になる。'], 19)
new.append(ns)

for sh in S[0].shapes:
    if sh.has_text_frame:
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                r.text = r.text.replace('専攻医のための6枚', '専攻医のための要点')
# 並べ替え：表紙のあとに新スライド、元の 2〜6 は削除
lst = pr.slides._sldIdLst
ids = list(lst)
old = ids[1:6]
newids = ids[6:]
for el in newids:
    lst.remove(el)
for el in old:
    pr.part.drop_rel(el.get('{%s}id' % RNS))
    lst.remove(el)
for el in newids:
    lst.append(el)
# ページ番号
for i, s in enumerate(pr.slides, 1):
    for sh in s.shapes:
        if sh.has_text_frame and sh.top / E > 6.9 and re.fullmatch(r'\d+', sh.text_frame.text.strip()):
            sh.text_frame.paragraphs[0].runs[0].text = str(i)
for i, s in enumerate(pr.slides, 1):
    s.part.partname = PackURI('/ppt/slides/t%d.xml' % i)
for i, s in enumerate(pr.slides, 1):
    s.part.partname = PackURI('/ppt/slides/slide%d.xml' % i)
pr.save(DST)
print('slides', len(pr.slides))
