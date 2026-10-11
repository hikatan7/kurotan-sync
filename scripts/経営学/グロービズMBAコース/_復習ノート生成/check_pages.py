"""語句解説の頁が、元スライドPDFのその頁に実際に載っているかを確かめる。
python check_pages.py <id> ...   （index/<id>.json と src_map の元PDFテキストを照合）"""
import json, os, re, sys, glob
import fitz
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = {
 "mkt1":"マーケティング/Day1/jpimkt2607dl_day1_20260627195108157_1.pdf",
 "mkt2":"マーケティング/Day2/jpimkt2607dl_day2_20260627195159197_1.pdf",
 "mkt3":"マーケティング/Day3/MKT_Day3_jpimkt2607dl_day3_20260627195401080_1.pdf",
 "mkt4":"マーケティング/Day4/MKT_Day4_jpimkt2607dl_day4_20260627195446733_1.pdf",
 "mkt5":"マーケティング/Day5/jpimkt2607dl_day5_20260910132234513_1.pdf",
 "ems1":"マーケティング経営戦略基礎/Day1/EMS_Day1_jpiems2601bl_day1_20260108172855527_1.pdf",
 "ems2":"マーケティング経営戦略基礎/Day2/jpiems2601bl_day2_20260120165442033_1.pdf",
 "ems3":"マーケティング経営戦略基礎/Day3/jpiems2601bl_day3_20260204164743213_1.pdf",
 "ems4":"マーケティング経営戦略基礎/Day4/jpiems2601bl_day4_20260220103556300_1.pdf",
 "ems5":"マーケティング経営戦略基礎/Day5/jpiems2601bl_day5_20260306092425540_1.pdf",
 "ems6":"マーケティング経営戦略基礎/Day6/jpiems2601bl_day6_20260320120411817_1.pdf",
 "crt1":"クリティカルシンキング/Day1教材/CRT_Day1_jpicrt2601cl_day1_20260110212722227_1.pdf",
 "crt2":"クリティカルシンキング/Day2教材/CRT_Day2_jpicrt2601cl_day2_20260129180911433_1.pdf",
 "crt3":"クリティカルシンキング/Day3教材/jpicrt2601cl_day3_20260212021811590_1.pdf",
 "crt4":"クリティカルシンキング/Day4教材/jpicrt2601cl_day4_20260226080708120_1.pdf",
 "crt5":"クリティカルシンキング/Day5教材/jpicrt2601cl_day5_20260312034411417_1.pdf",
 "crt6":"クリティカルシンキング/Day6教材/jpicrt2601cl_day6_20260326184103203_1.pdf",
 "obh1":"組織行動とリーダーシップ/Day1/jpiobh2604bl_day1_20260403144815560_1.pdf",
 "obh2":"組織行動とリーダーシップ/Day2/OBH_Day2_jpiobh2604bl_day2_20260417122049510_1.pdf",
 "obh3":"組織行動とリーダーシップ/Day3/OBH_Day3_jpiobh2604bl_day3_20260508153845083_1.pdf",
 "obh4":"組織行動とリーダーシップ/Day4/jpiobh2604bl_day4_20260523083753807_1.pdf",
 "obh5":"組織行動とリーダーシップ/Day5/jpiobh2604bl_day5_20260605191108280_1.pdf",
 "obh6":"組織行動とリーダーシップ/Day6/OBH_Day6_jpiobh2604bl_day6_20260620004425830_1.pdf",
 "hrm1":"人材マネジメント/Day1/jpihrm2607el_day1_20260716141046303_1.pdf",
 "hrm2":"人材マネジメント/Day2/jpihrm2607el_day2_20260731060050417_1.pdf",
 "hrm3":"人材マネジメント/Day3/jpihrm2607el_day3_20260811042844533_.pdf",
 "hrm4":"人材マネジメント/Day4/jpihrm2607al_day4_20260817085109963_.pdf",
 "hrm5":"人材マネジメント/Day5/jpihrm2604al_day5_20260419131102340_.pdf",
 "hrm6":"人材マネジメント/Day6/jpihrm2604al_day6_20260419131118147_.pdf",
 "acc1":"アカウンティング基礎/Day1/IEA_Day1_jpiea2607al_day1_20260624213215387_1.pdf",
 "acc2":"アカウンティング基礎/Day2/IEA_Day2_jpiea2607al_day2_20260711092750623_1.pdf",
 "acc3":"アカウンティング基礎/Day3/jpiea2607al_day3_20260724000253910_1.pdf",
 "acc4":"アカウンティング基礎/Day4/jpiea2607al_day4_20260809195116413_1.pdf",
 "acc5":"アカウンティング基礎/Day5/IEA_Day5_jpiea2607al_day5_20260822091908220_1.pdf",
 "fin1":"ファイナンス基礎/Day1/IEF_Day1_jpief2607fl_day1_20260701112455437_1.pdf",
 "fin2":"ファイナンス基礎/Day2/IEF_Day2_jpief2607fl_day2_20260723210317023_1.pdf",
 "fin3":"ファイナンス基礎/Day3/IEF_Day3_jpief2607fl_day3_20260615100425747_.pdf",
 "fin4":"ファイナンス基礎/Day4/jpief2607fl_day4_20260615100540080_.pdf",
 "fin5":"ファイナンス基礎/Day5/IEF_Day5_jpief2607fl_day5_20260615100842337_.pdf",
}
def norm(s): return re.sub(r'[\s　・･\-－ー―]', '', s).lower()
def keys(term):
    t = re.split(r'[（(]', term)[0]
    parts = [p for p in re.split(r'[／/＋×]', t) if p.strip()]
    ks = [norm(p) for p in parts if len(norm(p)) >= 2]
    return ks or [norm(term)]
def pages(pg):
    out=set()
    for tok in re.split(r'[,、]\s*', pg):
        m=re.match(r'(\d+)\s*[–\-~〜]\s*(\d+)', tok.strip())
        if m: out.update(range(int(m[1]), int(m[2])+1))
        elif tok.strip().isdigit(): out.add(int(tok))
    return out
def check(nid, extra=()):
    meta=json.load(open(os.path.join(HERE,'index',nid+'.json'),encoding='utf-8'))
    srcs=[SRC[nid]]+list(extra)
    txt={}
    for s in srcs[:1]:
        d=fitz.open(os.path.join(ROOT,s))
        for i,p in enumerate(d): txt[i+1]=norm(p.get_text())
    bad=[]
    for t in meta['terms']:
        ks=keys(t['term']); cited=pages(t['pages'])
        hit={n for n,x in txt.items() if any(k in x for k in ks)}
        if not cited: bad.append((t['term'],t['pages'],'頁なし',sorted(hit)[:8])); continue
        if cited & hit: continue
        bad.append((t['term'],t['pages'],'不一致',sorted(hit)[:10]))
    return meta,bad
if __name__=='__main__':
    for nid in sys.argv[1:]:
        meta,bad=check(nid)
        print(f'== {nid} {len(meta["terms"])}語 / 要確認 {len(bad)}')
        for b in bad: print('  ',b)
