import io, pickle, re, sys
import fitz, pdfplumber
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen

ref = pickle.load(open("ref.pkl","rb"))

def glyph_sig(gs, name):
    pen = DecomposingRecordingPen(gs)
    try: gs[name].draw(pen)
    except Exception: return None
    if not pen.value: return None
    out=[]
    for op,args in pen.value:
        out.append(op)
        for a in args:
            if isinstance(a,tuple): out.append((round(a[0]),round(a[1])))
    return repr(out)

def build_maps(pdfpath):
    doc = fitz.open(pdfpath)
    xrefs=set()
    for p in doc:
        for f in p.get_fonts(full=True):
            xrefs.add(f[0])
    maps={}
    for x in sorted(xrefs):
        try: name, ext, ftype, buf = doc.extract_font(x)
        except Exception: continue
        if not buf: continue
        try: tt = TTFont(io.BytesIO(buf), fontNumber=0)
        except Exception: continue
        gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
        sigs = {}; blanks=set()
        for gid,gname in enumerate(order):
            s = glyph_sig(gs,gname)
            if s: sigs[gid]=s
            else: blanks.add(gid)
        best=None;bestn=-1
        for rname,rd in ref.items():
            n=sum(1 for s in sigs.values() if s in rd)
            if n>bestn: bestn=n; best=rname
        rd=ref[best]
        m={gid: rd[s] for gid,s in sigs.items() if s in rd}
        for g in blanks: m[g]=' '
        maps[name]=m
        print(f"{name}: gids={len(order)} matched={len(m)} via {best}", file=sys.stderr)
    return maps

def decode_pdf(pdfpath, outpath):
    maps = build_maps(pdfpath)
    base = {k.split('+')[-1]:v for k,v in maps.items()}
    out=[]
    with pdfplumber.open(pdfpath) as pdf:
        for pi,page in enumerate(pdf.pages):
            chars=[]
            for c in page.chars:
                t=c['text']
                m=re.fullmatch(r'\(cid:(\d+)\)', t)
                if m:
                    gid=int(m.group(1))
                    fn=c['fontname']
                    mp = maps.get(fn) or base.get(fn.split('+')[-1]) or {}
                    t = mp.get(gid, f'?{gid}?')
                chars.append((round(c['top']/3.0), c['x0'], t))
            lines={}
            for row,x,t in chars:
                lines.setdefault(row,[]).append((x,t))
            out.append(f"\n===PAGE {pi+1}===")
            for row in sorted(lines):
                items=sorted(lines[row])
                s=''; prev=None
                for x,t in items:
                    if prev is not None and x-prev>8: s+='\t'
                    s+=t; prev=x
                out.append(s)
    open(outpath,"w",encoding="utf-8").write("\n".join(out))
    print("wrote",outpath, file=sys.stderr)

if __name__=="__main__":
    decode_pdf(sys.argv[1], sys.argv[2])
