import fitz, glob, re, json, os
KW = {
 'anes': r'麻酔|鎮静|麻酔科',
 'tee': r'経食道心エコー|TEE',
 'periop': r'周術期|術前評価|術中|術後管理|非心臓手術',
 'mcs': r'IABP|大動脈内バルーン|Impella|インペラ|補助循環用ポンプ|ECMO|VA-ECMO|ECPELLA|PCPS',
 'shd': r'TAVI|TAVR|経カテーテル的大動脈弁|MitraClip|経皮的僧帽弁|TEER|左心耳閉鎖|WATCHMAN|TriClip',
 'bridge': r'ヘパリンブリッジ|休薬|抗凝固薬の中断|ブリッジング',
}
res = {}
for f in sorted(glob.glob('pdf/*.pdf')):
    d = fitz.open(f); name = os.path.basename(f)[:-4]
    title = re.sub(r'\s+', ' ', d[0].get_text())[:160]
    pages = []
    for i, p in enumerate(d):
        t = p.get_text()
        c = {k: len(re.findall(v, t)) for k, v in KW.items()}
        if c['anes'] + c['tee'] + c['periop'] + c['mcs'] + c['shd'] + c['bridge'] > 0:
            pages.append((i + 1, c))
    res[name] = dict(title=title, n=len(d), pages=pages)
    tot = {k: sum(c[k] for _, c in pages) for k in KW}
    print(name, len(d), 'p |', tot, '|', title[:70])
json.dump(res, open('scan.json', 'w', encoding='utf-8'), ensure_ascii=False)
