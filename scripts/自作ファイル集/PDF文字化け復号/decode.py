import io, json, sys, glob
import fitz
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.recordingPen import DecomposingRecordingPen

def sig_font(tt):
    gs = tt.getGlyphSet()
    return gs

def glyph_sig(gs, name):
    pen = DecomposingRecordingPen(gs)
    try:
        gs[name].draw(pen)
    except Exception:
        return None
    if not pen.value:
        return None
    out=[]
    for op,args in pen.value:
        out.append(op)
        for a in args:
            if isinstance(a,tuple):
                out.append((round(a[0]),round(a[1])))
    return repr(out)

# Build reference: unicode -> signature from MS Mincho & MS PMincho & Gothic
ref = {}
for path in ("C:/Windows/Fonts/msmincho.ttc","C:/Windows/Fonts/msgothic.ttc"):
    coll = TTCollection(path)
    for tt in coll.fonts:
        name = tt['name'].getDebugName(6)
        gs = tt.getGlyphSet()
        cmap = tt.getBestCmap()
        rev = {}
        for uni, gname in cmap.items():
            rev.setdefault(gname, uni)
        d={}
        for gname, uni in rev.items():
            s = glyph_sig(gs, gname)
            if s and s not in d:
                d[s]=chr(uni)
        ref[name]=d
        print("ref", name, len(d), file=sys.stderr)
json.dump({k:{} for k in ref}, open("refkeys.json","w"))

import pickle
pickle.dump(ref, open("ref.pkl","wb"))
