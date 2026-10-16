import fitz, glob, os, re, json, collections

KW = {
    '麻酔・鎮静': r'麻酔|鎮静',
    'TEE': r'経食道心エコー|TEE',
    '周術期': r'周術期|術前|術中|術後|非心臓手術',
    '補助循環': r'IABP|大動脈内バルーン|Impella|インペラ|補助循環用ポンプ|ECMO|ECPELLA|PCPS|補助人工心臓|LVAD',
    'Structural': r'TAVI|TAVR|経カテーテル的大動脈弁|MitraClip|マイトラクリップ|経皮的僧帽弁|TEER|左心耳閉鎖|WATCHMAN|TriClip|PFO閉鎖|経皮的心房中隔',
    '抗血栓の休薬': r'ヘパリンブリッジ|ブリッジング|休薬|中断',
}
HEAD_RE = re.compile(r'^(第\s*\d+\s*章|Part\s*\d+|\d+(\.\d+)*\.?\s*\S|[０-９]+\.|付表|表\s*\d+|図\s*\d+)')


def is_heading(spans):
    t = ''.join(s['text'] for s in spans).strip()
    if not t or len(t) > 70:
        return None
    big = max(s['size'] for s in spans)
    bold = any(('DeBold' in s['font'] or 'Bold' in s['font'] or 'W6' in s['font'] or 'W7' in s['font']) for s in spans)
    if bold and big >= 9.0 and not t.startswith(('表', '図')):
        return (round(big, 1), t)
    return None


def run(f):
    d = fitz.open(f)
    stack = []  # list of (size, text)
    secs = collections.OrderedDict()
    for pn, page in enumerate(d, 1):
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                sp = [s for s in l['spans'] if s['text'].strip()]
                if not sp:
                    continue
                h = is_heading(sp)
                if h:
                    size, t = h
                    # merge numeric-only heading with next text later: keep simple
                    while stack and stack[-1][0] <= size:
                        stack.pop()
                    stack.append((size, t))
                    continue
                key = ' > '.join(x[1] for x in stack[-3:]) or '(前付)'
                txt = ''.join(s['text'] for s in sp)
                e = secs.setdefault(key, {'pages': set(), 'text': []})
                e['pages'].add(pn)
                e['text'].append(txt)
    out = []
    for k, e in secs.items():
        t = ''.join(e['text'])
        c = {n: len(re.findall(r, t)) for n, r in KW.items()}
        out.append({'section': k, 'pages': sorted(e['pages']), 'counts': c, 'len': len(t), 'text': t})
    return out


res = {}
for f in sorted(glob.glob('pdf/*.pdf')):
    res[os.path.basename(f)[:-4]] = run(f)
json.dump(res, open('sections.json', 'w', encoding='utf-8'), ensure_ascii=False)
for g, secs in res.items():
    hit = [s for s in secs if sum(s['counts'].values()) >= 3]
    print(g, len(secs), 'sections,', len(hit), 'with hits')
