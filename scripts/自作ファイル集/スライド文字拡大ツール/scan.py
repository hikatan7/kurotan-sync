import json,os,re,fitz,statistics,sys
BASE=r"C:\Users\junch\OneDrive\_旧デスクトップ"
ED=os.path.join(BASE,"教育ファイル集")
paths=set()
def walk(o):
    if isinstance(o,dict):
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
    elif isinstance(o,str) and o.lower().split('#')[0].endswith('.pdf'):
        paths.add(o.split('#')[0])
walk(json.load(open(os.path.join(ED,'_portal_data.json'),encoding='utf-8')))
walk(json.load(open(os.path.join(ED,'_ポータル生成','theme_resus.json'),encoding='utf-8')))
rows=[];miss=[]
for p in sorted(paths):
    f=os.path.join(BASE,os.path.normpath(p))
    if not os.path.exists(f): miss.append(p);continue
    try: doc=fitz.open(f)
    except Exception as e: rows.append((p,'ERR',str(e)));continue
    sizes=[];npg=len(doc);img_only=0
    for i,pg in enumerate(doc):
        if i>=40 and i%5: continue
        w=min(pg.rect.width,pg.rect.height) if False else pg.rect.width
        scale=595.0/w  # A4-portrait-width equivalent
        d=pg.get_text('dict')
        chars=0
        for b in d['blocks']:
            for l in b.get('lines',[]):
                for s in l['spans']:
                    t=s['text'].strip()
                    if not t: continue
                    n=len(t);chars+=n
                    sizes.append((s['size']*scale,n))
        if chars<20: img_only+=1
    tot=sum(n for _,n in sizes)
    if tot==0:
        rows.append((p,npg,'NOTEXT',img_only));continue
    sizes.sort()
    def pct(q):
        acc=0
        for s,n in sizes:
            acc+=n
            if acc>=tot*q: return s
    small=sum(n for s,n in sizes if s<7.5)/tot
    rows.append((p,npg,round(pct(0.5),1),round(pct(0.1),1),round(small*100),img_only,round(doc[0].rect.width),round(doc[0].rect.height)))
json.dump({'rows':rows,'miss':miss},open(sys.argv[1],'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(paths),len(rows),len(miss))
