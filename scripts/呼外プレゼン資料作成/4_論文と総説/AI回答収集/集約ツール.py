# -*- coding: utf-8 -*-
r"""
AI横断検索の回答を1つのExcelへ集約するツール

使い方:
    python 集約ツール.py

やること:
 1. 01_原文\ の中の .md / .txt をすべて読む
 2. ファイル名からAI名とフェーズ（①文献 / ②アイデア）を判定
 3. #TSV-xxx 〜 #END の構造化ブロックを抽出して表にする
 4. 似たタイトル・似た文献をまとめ、「何個のAIが挙げたか」を数える
 5. AIごとの傾向（案の本数・領域の偏り・独自案の数・要確認文献の割合）を集計
 6. 集約結果_YYYYMMDD.xlsx を出力する
 7. 構造化ブロックが無い回答も、本文をそのまま保管シートへ残す（取りこぼし防止）

ファイル名の規則（01_原文\ の中）:
    <AI名>_<フェーズ>_<任意メモ>.md
      例) Gemini_文献.md / Perplexity_文献.md / ChatGPT_アイデア.md / Claude_アイデア_2巡目.md
    AI名は Gemini / Perplexity / Copilot / ChatGPT / Claude / Genspark / その他 を自動認識
"""
import io, os, re, sys, glob, datetime
from collections import Counter, defaultdict
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '01_原文')
OUT = os.path.join(HERE, '集約結果_%s.xlsx' % datetime.date.today().strftime('%Y%m%d'))

AI_NAMES = ['Gemini', 'Perplexity', 'Copilot', 'ChatGPT', 'Claude',
            'Consensus', 'Elicit', 'NotebookLM', 'Genspark']

def detect_ai(fn):
    base = os.path.basename(fn)
    for a in AI_NAMES:
        if a.lower() in base.lower():
            return a
    return base.split('_')[0] or 'その他'

def detect_phase(fn):
    b = os.path.basename(fn)
    if '文献' in b or '検索' in b or '①' in b or 'bib' in b.lower():
        return '①文献'
    if 'アイデア' in b or '②' in b or 'idea' in b.lower():
        return '②アイデア'
    if '追撃' in b or '2巡' in b or '③' in b or '絞' in b:
        return '③追撃'
    return '未分類'

# ---------- 構造化ブロックの抽出 ----------
def blocks(text, tag):
    out = []
    for m in re.finditer(r'#TSV-%s\s*\n(.*?)\n\s*#END' % tag, text, flags=re.S):
        body = m.group(1)
        rows = []
        for ln in body.splitlines():
            ln = ln.rstrip()
            if not ln.strip():
                continue
            if '\t' in ln:
                cells = [c.strip() for c in ln.split('\t')]
            else:
                cells = [c.strip() for c in re.split(r'\s*\|\s*', ln.strip('| '))]
            if len(cells) >= 2:
                rows.append(cells)
        if rows:
            out.append(rows)
    return out

# ---------- プロンプト本文の除去 ----------
# 回答と一緒にプロンプトも貼られている場合、プロンプト内の表を拾ってしまうため除外する
PROMPT_FILES = [
    os.path.join(os.path.dirname(HERE), 'プロンプト_呼吸器外科論文_横断検索とアイデア抽出_20260823.md'),
    os.path.join(os.path.dirname(HERE), 'プロンプト_論文デザイン10本依頼_20260823.md'),
    os.path.join(HERE, '追加指示ブロック_これを各プロンプトの末尾に足す.md'),
]
PROMPT_LINES = set()
for _p in PROMPT_FILES:
    if os.path.exists(_p):
        try:
            for _ln in io.open(_p, encoding='utf-8').read().splitlines():
                _s = _ln.strip()
                if len(_s) >= 8:
                    PROMPT_LINES.add(re.sub(r'\s+', '', _s))
        except Exception:
            pass

def from_prompt(line):
    return re.sub(r'\s+', '', str(line).strip()) in PROMPT_LINES

# ---------- タブ区切り表からの回収（Web画面の表をコピペするとこの形になる） ----------
def tab_tables(text):
    """連続する「タブ2個以上の行」を1つの表とみなす"""
    out, cur = [], []
    for ln in text.splitlines():
        if ln.count('\t') >= 2 and ln.strip():
            cur.append([c.strip() for c in ln.split('\t')])
        else:
            if len(cur) >= 2:
                out.append((cur[0], cur[1:]))
            cur = []
    if len(cur) >= 2:
        out.append((cur[0], cur[1:]))
    return out

# ---------- 本文中のMarkdown表からの回収（TSVブロックが無いとき用） ----------
def md_tables(text):
    """本文中の | a | b | c | 形式の表を (ヘッダ, 行リスト) で返す"""
    out, cur = [], []
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith('|') and s.count('|') >= 3:
            cells = [c.strip() for c in s.strip('|').split('|')]
            if all(re.fullmatch(r'[-:\s]*', c) for c in cells):
                continue                      # 罫線行は捨てる
            cur.append(cells)
        else:
            if len(cur) >= 2:
                out.append((cur[0], cur[1:]))
            cur = []
    if len(cur) >= 2:
        out.append((cur[0], cur[1:]))
    return out

# 正規形の各列に対応するヘッダ語（部分一致・優先順）
FIELDS = {
    'BIB': [['テーマ', '#'], ['著者', 'author', '文献名', '報告'], ['年', 'year'],
            ['雑誌', 'journal', '出典'], ['デザイン', '症例', 'design', '対象'],
            ['結果', '数値', '所見', 'result'], ['確度', '確実', '信頼']],
    'IDEA': [['案番号', 'no', '#', '番号'], ['タイトル', '題', 'title'],
             ['領域', '分野', 'カテゴリ'], ['アウトカム', '主要評価', 'outcome'],
             ['例数', '対象', 'n数', 'サンプル'], ['要否', '追加収集の', '追加収集'],
             ['追加収集項目', '必要な項目', '追加項目', '必要データ'],
             ['実現', '実行可能', 'feasib'], ['投稿', '雑誌', 'journal']],
    'VAR': [['優先'], ['変数', '項目名'], ['定義', '入力規則', '規則'],
            ['取得元', '出所', 'ソース'], ['関係', '該当案', '案番号'],
            ['工数', '時間', 'コスト']],
}

def map_row(kind, header, row):
    """ヘッダ名を手がかりに、列順が違っても正規形に並べ替える"""
    spec = FIELDS[kind]
    hl = [str(h).lower() for h in header]
    out = []
    for keys in spec:
        idx = None
        for i, h in enumerate(hl):
            if any(k.lower() in h for k in keys):
                idx = i; break
        out.append(row[idx].strip() if idx is not None and idx < len(row) else '-')
    return out

def classify(header):
    h = ' '.join(str(x) for x in header).lower()
    if any(k in h for k in ['著者', 'author', '雑誌', 'journal']):
        return 'BIB'
    if any(k in h for k in ['タイトル', 'title', '題']) and any(
            k in h for k in ['領域', '分野', 'アウトカム', '実現', '投稿']):
        return 'IDEA'
    if any(k in h for k in ['変数', '項目名']) and any(
            k in h for k in ['取得元', '定義', '工数', '優先']):
        return 'VAR'
    return None

def fallback(text):
    """本文の表（タブ区切り／Markdown）から BIB / IDEA / VAR を回収する。
       プロンプトを一緒に貼っている場合、プロンプト由来の行は除外する。"""
    got = {'BIB': [], 'IDEA': [], 'VAR': []}
    seen = set()
    # タブ区切り表を優先（Web画面の表をコピペするとこの形になる＝AIの回答）
    for tables in (tab_tables(text), md_tables(text)):
        for header, rows in tables:
            if from_prompt('\t'.join(header)) or from_prompt(' | '.join(header)):
                continue                      # プロンプト内の出力形式例
            kind = classify(header)
            if not kind:
                continue
            for r in rows:
                if len([c for c in r if c and c != '-']) < 2:
                    continue
                if from_prompt('\t'.join(r)) or from_prompt(' | '.join(r)):
                    continue                  # プロンプト内のデータ仕様の表
                cells = map_row(kind, header, r)
                sig = (kind, re.sub(r'\s+', '', ''.join(cells))[:80])
                if sig in seen:
                    continue
                seen.add(sig)
                got[kind].append(cells)
    # 表になっていないアイデア（「No.12 タイトル」形式の見出し）も拾う
    if not got['IDEA']:
        for m in re.finditer(r'^\s*(?:No\.?|案|アイデア)\s*(\d{1,2})[\.．　:：\s]\s*(.{6,90})$',
                             text, flags=re.M):
            t = m.group(2).strip()
            if from_prompt(t) or t.startswith(('タイトル', 'PECO', '対象')):
                continue
            got['IDEA'].append([m.group(1), t, '-', '-', '-', '-', '-', '-', '-'])
    return got

def outline(text):
    """見出しの一覧（本文の骨格を残す）"""
    out = []
    for ln in text.splitlines():
        m = re.match(r'^(#{1,4})\s+(.{1,120})$', ln.strip())
        if m:
            out.append((len(m.group(1)), m.group(2).strip()))
        else:
            m2 = re.match(r'^\s*(?:###\s*)?(?:案|アイデア)?\s*(\d{1,2})[\.．、）\)]\s*(.{4,110})$', ln)
            if m2 and len(ln.strip()) < 130:
                out.append((3, '%s. %s' % (m2.group(1), m2.group(2).strip())))
    return out

def norm(s):
    s = str(s or '').lower()
    s = re.sub(r'[\s　・,，.。、\-–—_/（）\(\)「」『』"\'’:：;；!！?？]', '', s)
    return s

def bigrams(s):
    s = norm(s)
    return set(s[i:i+2] for i in range(len(s) - 1)) or {s}

def similar(a, b, th=0.45):
    A, B = bigrams(a), bigrams(b)
    if not A or not B:
        return False
    return len(A & B) / len(A | B) >= th

def group_items(items, keyfunc):
    """似たものをまとめる。items=[(key, payload...)] -> [[idx,...], ...]"""
    groups = []
    for i, it in enumerate(items):
        k = keyfunc(it)
        placed = False
        for g in groups:
            if similar(k, keyfunc(items[g[0]])):
                g.append(i); placed = True; break
        if not placed:
            groups.append([i])
    return groups

# ---------- 読み込み ----------
if not os.path.isdir(SRC):
    os.makedirs(SRC, exist_ok=True)
files = sorted(glob.glob(os.path.join(SRC, '*.md')) + glob.glob(os.path.join(SRC, '*.txt')))
if not files:
    print('01_原文 フォルダに回答ファイルがありません。')
    print('  ' + SRC)
    print('  <AI名>_文献.md / <AI名>_アイデア.md の形式で保存してください。')
    sys.exit(0)

docs = []
for f in files:
    try:
        t = io.open(f, encoding='utf-8').read()
    except UnicodeDecodeError:
        t = io.open(f, encoding='cp932', errors='replace').read()
    docs.append({'file': os.path.basename(f), 'path': f, 'ai': detect_ai(f),
                 'phase': detect_phase(f), 'text': t, 'chars': len(t)})

BIB, IDEA, VAR, VERD, QUERY, OUTL = [], [], [], [], [], []
# 同じ回答を2回貼っても二重計上しないための記録（AI名込みで判定するので、
# 別のAIが同じ文献を挙げた場合は残る＝「何個のAIが挙げたか」は正しく数えられる）
SEEN_ROWS = set()
DUP_SKIPPED = Counter()

def add_row(store, d, cells, src, tag):
    sig = (d['ai'], tag, re.sub(r'\s+', '', ''.join(str(c) for c in cells))[:90])
    if sig in SEEN_ROWS:
        DUP_SKIPPED[d['ai']] += 1
        return False
    SEEN_ROWS.add(sig)
    store.append({'ai': d['ai'], 'file': d['file'], 'cells': cells, 'src': src})
    return True

# 内容がまったく同じファイルの検出
_seen_files = {}
for d in docs:
    key = re.sub(r'\s+', '', d['text'])[:4000]
    d['dup_of'] = _seen_files.get(key)
    if d['dup_of'] is None:
        _seen_files[key] = d['file']

for d in docs:
    hit = {'BIB': 0, 'IDEA': 0, 'VAR': 0}
    for tag, store, headkey in [('BIB', BIB, '著者'), ('IDEA', IDEA, 'タイトル'),
                                ('VAR', VAR, '変数名')]:
        for rows in blocks(d['text'], tag):
            for r in (rows[1:] if rows and (headkey in ''.join(rows[0])) else rows):
                add_row(store, d, r, 'TSVブロック', tag)
                hit[tag] += 1
    for rows in blocks(d['text'], 'VERDICT'):
        for r in rows[1:] if rows and ('項目' in ''.join(rows[0])) else rows:
            add_row(VERD, d, r, 'TSVブロック', 'VERDICT')
    for rows in blocks(d['text'], 'QUERY'):
        for r in rows[1:] if rows and ('検索語' in ''.join(rows[0])) else rows:
            add_row(QUERY, d, r, 'TSVブロック', 'QUERY')
    # TSVブロックが無かった種別は、本文中の表（タブ区切り／Markdown）から回収する
    fb = fallback(d['text'])
    for tag, store in [('BIB', BIB), ('IDEA', IDEA), ('VAR', VAR)]:
        if hit[tag] == 0:
            for r in fb[tag]:
                add_row(store, d, r, '本文の表', tag)
    d['fallback'] = {k: len(v) for k, v in fb.items()}
    for lv, tt in outline(d['text']):
        OUTL.append([d['ai'], d['phase'], d['file'], lv, ('　' * (lv - 1)) + tt])

def cell(rec, i, default='-'):
    c = rec['cells']
    return c[i] if i < len(c) and c[i] else default

# ---------- Excel ----------
wb = openpyxl.Workbook()
thin = Side(style='thin', color='BFBFBF')
HDR = PatternFill('solid', fgColor='DDE5F0')
HDR2 = PatternFill('solid', fgColor='E2EFDA')
WARN = PatternFill('solid', fgColor='FFF2CC')
HIT = PatternFill('solid', fgColor='D9EAD3')

def sheet(name, header, rows, widths=None, fill=HDR):
    ws = wb.create_sheet(name)
    ws.append(header)
    for r in rows:
        ws.append(r)
    for c in range(1, len(header) + 1):
        x = ws.cell(1, c)
        x.font = Font(bold=True, size=9)
        x.fill = fill
        x.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        x.border = Border(thin, thin, thin, thin)
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(header)):
        for x in row:
            x.font = Font(size=9)
            x.alignment = Alignment(vertical='top', wrap_text=True)
            x.border = Border(thin, thin, thin, thin)
    ws.freeze_panes = 'A2'
    if ws.max_row > 1:
        ws.auto_filter.ref = 'A1:%s%d' % (get_column_letter(len(header)), ws.max_row)
    for i, wd in enumerate(widths or [], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    return ws

# --- 10 論文アイデア ---
idea_rows = []
gi = group_items(IDEA, lambda r: cell(r, 1))
gid = {}
for n, g in enumerate(gi, 1):
    for i in g:
        gid[i] = n
for i, rec in enumerate(IDEA):
    ais = sorted(set(IDEA[j]['ai'] for j in gi[gid[i] - 1]))
    idea_rows.append([gid[i], rec['ai'], cell(rec, 0), cell(rec, 1), cell(rec, 2), cell(rec, 3),
                      cell(rec, 4), cell(rec, 5), cell(rec, 6), cell(rec, 7), cell(rec, 8),
                      len(ais), '／'.join(ais), rec['src'], rec['file']])
idea_rows.sort(key=lambda r: (-r[11], r[0]))
ws = sheet('10_論文アイデア',
           ['統合#', '提案AI', '案番号', '仮タイトル(和文)', '領域', '主要アウトカム', '解析対象例数',
            '追加収集', '追加収集項目', '実現可能性', '投稿先第一候補', '提案AI数', '提案したAI',
            '取得方法', '出典ファイル'],
           idea_rows,
           [7, 11, 7, 42, 13, 22, 11, 9, 24, 10, 22, 9, 20, 12, 24])
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    n = row[11].value
    if isinstance(n, int) and n >= 2:
        row[11].fill = HIT
        row[3].fill = HIT

# --- 11 アイデア重複マップ ---
dup_rows = []
for n, g in enumerate(gi, 1):
    ais = sorted(set(IDEA[j]['ai'] for j in g))
    titles = list(dict.fromkeys(cell(IDEA[j], 1) for j in g))
    dup_rows.append([n, len(ais), '／'.join(ais), len(g), ' ／ '.join(titles[:4]),
                     '複数AIが独立に提案' if len(ais) >= 2 else '単独提案（独自視点 or 的外れ）'])
dup_rows.sort(key=lambda r: -r[1])
sheet('11_アイデア重複マップ', ['統合#', '提案AI数', 'AI', '行数', 'タイトルのバリエーション', '判定'],
      dup_rows, [7, 10, 22, 7, 70, 26], HDR2)

# --- 12 テーマ別マップ（言い回しが違っても同じ論点をまとめる） ---
TOPICS = [
    ('occult N・リンパ節郭清', ['occult', 'リンパ節', '郭清', 'pn+', 'pn2', 'station', 'ln数', 'nodal']),
    ('病期移動（c-p不一致）', ['upstag', 'up-stag', '病期', 'stage', 'ステージ', 'ct–pt', 'ct-pt', 'c-p']),
    ('RFIDマーキング', ['rfid', 'マーカー', 'マーキング', 'ステント', '二段階']),
    ('切除断端（margin）', ['margin', '断端']),
    ('学習曲線', ['学習', 'learning', 'plateau', 'cusum', '習熟']),
    ('術式選択の変化', ['術式選択', 'シフト', '区域切除の急増', '増加', 'トレンド', '推移']),
    ('手術室運営・時間', ['手術室', 'or運営', '在室', '非手術時間', 'turnover', '予定手術時間',
                  '定時外', '枠', 'resource', '運営']),
    ('麻酔・周術期管理', ['麻酔', '周術期', '導入', '覚醒']),
    ('術後回復・ドレーン', ['ドレーン', 'chest tube', '在院', '回復', 'eras', '退院']),
    ('医療経済・原価', ['費用', '人件費', 'コスト', '原価', '経済', 'burden']),
    ('画像・GGO・腫瘍径', ['ggo', '充実成分', 'c/t', '腫瘍径', 'ct所見', '画像']),
    ('出血・合併症', ['出血', '合併症', 'conversion']),
    ('データ品質・方法論', ['データ品質', '突合', '精度', '方法論', 'linkage', 'レジストリの']),
]

def topics_of(text):
    t = str(text).lower()
    hit = [name for name, keys in TOPICS if any(k in t for k in keys)]
    return hit or ['その他']

topic_rows = []
tmap = defaultdict(lambda: defaultdict(list))
for rec in IDEA:
    label = cell(rec, 1) + ' ' + cell(rec, 2) + ' ' + cell(rec, 3)
    for tp in topics_of(label):
        tmap[tp][rec['ai']].append('%s-%s' % (rec['ai'][:2], cell(rec, 0)))
ais_sorted = sorted(set(r['ai'] for r in IDEA))
for tp, _ in TOPICS + [('その他', None)]:
    if tp not in tmap:
        continue
    row = [tp, len(tmap[tp]), sum(len(v) for v in tmap[tp].values())]
    for a in ais_sorted:
        row.append('／'.join(tmap[tp].get(a, [])) or '-')
    row.append('複数AIが着目' if len(tmap[tp]) >= 2 else '単独')
    topic_rows.append(row)
topic_rows.sort(key=lambda r: (-r[1], -r[2]))
ws = sheet('12_テーマ別マップ',
           ['論点', '着目したAI数', '案の延べ数'] + ais_sorted + ['判定'],
           topic_rows, [26, 12, 11] + [16] * len(ais_sorted) + [16], HDR2)
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    if isinstance(row[1].value, int) and row[1].value >= 2:
        row[0].fill = HIT
        row[1].fill = HIT

# --- 20 文献 ---
bib_rows = []
gb = group_items(BIB, lambda r: cell(r, 1) + cell(r, 2) + cell(r, 3))
gbid = {}
for n, g in enumerate(gb, 1):
    for i in g:
        gbid[i] = n
for i, rec in enumerate(BIB):
    ais = sorted(set(BIB[j]['ai'] for j in gb[gbid[i] - 1]))
    bib_rows.append([gbid[i], cell(rec, 0), cell(rec, 1), cell(rec, 2), cell(rec, 3),
                     cell(rec, 4), cell(rec, 5), cell(rec, 6), rec['ai'], len(ais),
                     '／'.join(ais), rec['src']])
bib_rows.sort(key=lambda r: (-r[9], str(r[1])))
ws = sheet('20_文献',
           ['統合#', 'テーマ', '筆頭著者', '年', '雑誌', 'デザイン・症例数', '主要な数値結果',
            '確度(AI申告)', '挙げたAI', '挙げたAI数', 'AI一覧', '取得方法'],
           bib_rows, [7, 8, 16, 6, 22, 22, 34, 12, 11, 10, 22, 12])
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    n = row[9].value
    if isinstance(n, int) and n >= 2:
        row[9].fill = HIT
        row[2].fill = HIT
    if str(row[7].value).startswith('要確認') or n == 1:
        row[7].fill = WARN

# --- 21 検索語 ---
sheet('21_検索語', ['AI', 'テーマ', '検索語', '出典ファイル'],
      [[r['ai'], cell(r, 0), cell(r, 1), r['file']] for r in QUERY],
      [12, 8, 70, 24], HDR2)

# --- 30 追加収集変数 ---
var_rows = []
gv = group_items(VAR, lambda r: cell(r, 1))
gvid = {}
for n, g in enumerate(gv, 1):
    for i in g:
        gvid[i] = n
for i, rec in enumerate(VAR):
    ais = sorted(set(VAR[j]['ai'] for j in gv[gvid[i] - 1]))
    var_rows.append([gvid[i], rec['ai'], cell(rec, 0), cell(rec, 1), cell(rec, 2), cell(rec, 3),
                     cell(rec, 4), cell(rec, 5), len(ais), '／'.join(ais), rec['src']])
var_rows.sort(key=lambda r: (-r[8], str(r[2])))
ws = sheet('30_追加収集変数',
           ['統合#', '提案AI', '優先順位', '変数名', '定義・入力規則', '取得元', '関係案番号',
            '総工数', '提案AI数', 'AI一覧', '取得方法'],
           var_rows, [7, 11, 9, 20, 46, 18, 12, 11, 9, 22, 12])
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    if isinstance(row[8].value, int) and row[8].value >= 2:
        row[8].fill = HIT
        row[3].fill = HIT

# --- 31 結論ブロック ---
sheet('31_各AIの結論', ['AI', '項目', '回答', '出典ファイル'],
      [[r['ai'], cell(r, 0), cell(r, 1), r['file']] for r in VERD],
      [12, 34, 46, 24], HDR2)

# --- 40 AI別の傾向 ---
tr = []
ais_all = sorted(set(d['ai'] for d in docs))
for a in ais_all:
    dd = [d for d in docs if d['ai'] == a]
    ideas = [r for r in IDEA if r['ai'] == a]
    bibs = [r for r in BIB if r['ai'] == a]
    vars_ = [r for r in VAR if r['ai'] == a]
    dom = Counter(cell(r, 2) for r in ideas)
    feas = [int(re.sub(r'\D', '', cell(r, 7, '0')) or 0) for r in ideas]
    feas = [x for x in feas if 1 <= x <= 5]
    need = sum(1 for r in ideas if '要' in cell(r, 5))
    uniq = sum(1 for i, r in enumerate(IDEA)
               if r['ai'] == a and len(set(IDEA[j]['ai'] for j in gi[gid[i] - 1])) == 1)
    uncertain = sum(1 for r in bibs if '要確認' in cell(r, 6))
    tr.append([a, len(dd), sum(d['chars'] for d in dd), len(ideas), len(bibs), len(vars_),
               '／'.join('%s%d' % (k, v) for k, v in dom.most_common()),
               round(sum(feas) / len(feas), 1) if feas else '-',
               '%d/%d' % (need, len(ideas)) if ideas else '-',
               uniq,
               '%d/%d' % (uncertain, len(bibs)) if bibs else '-'])
sheet('40_AI別の傾向',
      ['AI', 'ファイル数', '総文字数', 'アイデア数', '文献数', '変数提案数', '領域の内訳',
       '実現可能性の平均', '追加収集が要の案', '単独提案の案数', '要確認と自己申告した文献'],
      tr, [12, 9, 10, 10, 8, 11, 34, 12, 13, 12, 15], HDR2)

# --- 90 原文の保管 ---
raw = []
for d in docs:
    has = []
    for tag, name in [('BIB', '文献'), ('IDEA', 'アイデア'), ('VAR', '変数'),
                      ('VERDICT', '結論'), ('QUERY', '検索語')]:
        if blocks(d['text'], tag):
            has.append(name)
    fb = d.get('fallback', {})
    fbtxt = '／'.join('%s%d件' % (k, v) for k, v in fb.items() if v) or '-'
    raw.append([d['ai'], d['phase'], d['file'], d['chars'],
                '／'.join(has) if has else '★構造化ブロックなし（本文の表から回収）',
                fbtxt,
                ('★%s と内容が同一' % d['dup_of']) if d.get('dup_of') else '-',
                d['text'][:32000]])
ws = sheet('90_原文保管',
           ['AI', 'フェーズ', 'ファイル名', '文字数', '検出した構造化ブロック',
            '本文の表から拾えた件数', '重複', '本文（先頭32,000字）'],
           raw, [12, 11, 28, 9, 32, 20, 26, 120])
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    if '★' in str(row[4].value):
        row[4].fill = WARN
    if '★' in str(row[6].value):
        row[6].fill = WARN

# --- 91 見出し一覧 ---
sheet('91_見出し一覧', ['AI', 'フェーズ', 'ファイル名', '階層', '見出し'],
      OUTL, [12, 11, 26, 6, 96], HDR2)

# --- 00 サマリ（先頭へ） ---
s = wb.create_sheet('00_サマリ', 0)
info = [
    ['AI横断検索 集約結果', ''],
    ['集約日', datetime.date.today().strftime('%Y-%m-%d')],
    ['読み込んだファイル', len(docs)],
    ['参加AI', '／'.join(ais_all)],
    ['', ''],
    ['論文アイデア（延べ）', len(IDEA)],
    ['　うち統合後のユニーク案', len(gi)],
    ['　2つ以上のAIが独立提案した案', sum(1 for g in gi if len(set(IDEA[j]['ai'] for j in g)) >= 2)],
    ['　単独提案の案', sum(1 for g in gi if len(set(IDEA[j]['ai'] for j in g)) == 1)],
    ['', ''],
    ['文献（延べ）', len(BIB)],
    ['　うち統合後のユニーク文献', len(gb)],
    ['　2つ以上のAIが挙げた文献（実在確度：高）',
     sum(1 for g in gb if len(set(BIB[j]['ai'] for j in g)) >= 2)],
    ['　1つのAIだけが挙げた文献（要検証）',
     sum(1 for g in gb if len(set(BIB[j]['ai'] for j in g)) == 1)],
    ['　AI自身が「要確認」と申告した文献', sum(1 for r in BIB if '要確認' in cell(r, 6))],
    ['', ''],
    ['追加収集変数の提案（延べ）', len(VAR)],
    ['　うち統合後のユニーク変数', len(gv)],
    ['　2つ以上のAIが挙げた変数（優先度：高）',
     sum(1 for g in gv if len(set(VAR[j]['ai'] for j in g)) >= 2)],
    ['', ''],
    ['重複として除外した行', sum(DUP_SKIPPED.values())],
    ['　内訳', '／'.join('%s %d行' % (k, v) for k, v in DUP_SKIPPED.items()) or 'なし'],
    ['内容が同一のファイル', sum(1 for d in docs if d.get('dup_of')) or 'なし'],
    ['', ''],
    ['【読み方】', ''],
    ['', '「20_文献」で挙げたAI数が2以上の行から先に当たる。1のものは捏造を疑ってPubMedで確認。'],
    ['', '「10_論文アイデア」で提案AI数が2以上＝どのモデルも思いつく案＝新規性は低い可能性。'],
    ['', '単独提案の案は、独自の視点か的外れかの二択。中身を読んで判断する。'],
    ['', '「30_追加収集変数」で複数AIが挙げた変数＝投資対効果が高い。ここから着手する。'],
    ['', '「90_原文保管」は取りこぼし防止。構造化ブロックが無い回答もここに全文が残る。'],
    ['', '「取得方法」列＝TSVブロック（確実）か、本文の表から自動回収したもの（要目視確認）かの別。'],
    ['', '「91_見出し一覧」で、各AIの回答の骨格を並べて比較できる。'],
    ['', '同じ回答を2回貼っても、同一AIの同一行は自動で1つにまとめられる。'],
    ['', '別のAIが同じ文献を挙げた場合は残る（それが「挙げたAI数」の根拠になるため）。'],
]
for r in info:
    s.append(r)
s.column_dimensions['A'].width = 42
s.column_dimensions['B'].width = 96
for row in s.iter_rows():
    for c in row:
        c.font = Font(size=10, bold=(c.row == 1 or str(c.value or '').startswith('【')))
        c.alignment = Alignment(vertical='top', wrap_text=True)
s['A1'].font = Font(size=13, bold=True)
s['A1'].fill = HDR

if 'Sheet' in wb.sheetnames:
    del wb['Sheet']
try:
    wb.save(OUT)
except PermissionError:
    base, ext = os.path.splitext(OUT)
    n = 2
    while os.path.exists('%s_%d%s' % (base, n, ext)):
        n += 1
    OUT = '%s_%d%s' % (base, n, ext)
    wb.save(OUT)
    print('※ 前回の集約結果がExcelで開かれていたため、別名で保存しました。')
    print('   開いているExcelを閉じてから実行すると、同じ名前に上書きされます。')
print('出力:', OUT)
print('ファイル %d件 / アイデア %d件(ユニーク%d) / 文献 %d件(ユニーク%d) / 変数 %d件'
      % (len(docs), len(IDEA), len(gi), len(BIB), len(gb), len(VAR)))
for d in docs:
    print('   %-12s %-8s %-30s %6d字' % (d['ai'], d['phase'], d['file'], d['chars']))
