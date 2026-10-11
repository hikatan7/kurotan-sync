# -*- coding: utf-8 -*-
"""初出の略語がすべて、初出ページ以前に正式名称つきで説明されているかを検証する。"""
import fitz, re, sys
sys.stdout.reconfigure(encoding="utf-8")

d = fitz.open("book.pdf")
raw = [p.get_text() for p in d]
flat = [re.sub(r"\s+", "", t) for t in raw]

CHECK = {
 "MAC":"最小肺胞濃度","GABA_A":"γ-アミノ酪酸","NMDA":"N-メチル-D-アスパラギン酸",
 "BIS":"バイスペクトラル指数","TOF":"四連刺激","EtCO₂":"呼気終末二酸化炭素",
 "EEG":"脳波","NRS":"数値評価スケール","SpO₂":"経皮的動脈血酸素飽和度","MAP":"平均動脈圧",
 "MAC-awake":"覚醒MAC","MAC-BAR":"交感神経反応抑制MAC","N₂O":"nitrousoxide",
 "FRC":"機能的残気量","EtO₂":"end-tidaloxygen","CPAP":"持続気道陽圧","PEEP":"呼気終末陽圧",
 "CO":"心拍出量","HR":"心拍数","SV":"一回拍出量","SVR":"体血管抵抗","CVP":"中心静脈圧",
 "SVV":"一回拍出量変動","PPV":"脈圧変動","IVC":"下大静脈","POCUS":"ポイントオブケア超音波",
 "ACE":"アンジオテンシン変換酵素","ARB":"アンジオテンシンII受容体拮抗薬",
 "Pplat":"plateaupressure","ΔP":"drivingpressure",
 "AChE":"アセチルコリンエステラーゼ","PACU":"麻酔後回復室",
 "SAD":"声門上器具","SGA":"supraglotticairway","CICO":"換気も挿管も不能",
 "RSI":"迅速導入","GLP-1":"グルカゴン様ペプチド","STOP-Bang":"スクリーニング質問票",
 "ASA":"米国麻酔科学会","MAC-sparing":"MACの節約",
 "TCI":"目標制御注入","TIVA":"全静脈麻酔","TRPA1":"侵害刺激受容チャネル",
 "Vd":"volumeofdistribution","CL":"clearance","CSHT":"文脈依存性半減期",
 "CYP3A4":"チトクロームP450","COX":"シクロオキシゲナーゼ","NSAIDs":"非ステロイド性抗炎症薬",
 "PONV":"術後悪心・嘔吐","ACh":"acetylcholine","PTC":"テタヌス後カウント",
 "TBW":"総体液量","ICF":"intracellularfluid","ECF":"extracellularfluid",
 "SIADH":"抗利尿ホルモン不適合分泌症候群","EGL":"endothelialglycocalyx",
 "ANP":"心房性ナトリウム利尿ペプチド","SID":"強イオン差","RCT":"ランダム化比較試験",
 "RAAS":"レニン-アンジオテンシン-アルドステロン系","AVP":"アルギニンバソプレシン",
 "VExUS":"静脈うっ血超音波スコア","mini-FC":"少量輸液負荷試験","EEO":"呼気終末閉塞試験",
 "PLR":"下肢挙上試験","GDFT":"goal-directedfluidtherapy","EBV":"estimatedbloodvolume",
 "ROSE":"Resuscitation・Optimization","%FO":"体液過剰率","KDIGO":"国際腎臓病予後改善機構",
 "AKI":"急性腎障害","CaO₂":"動脈血酸素含量","SaO₂":"動脈血酸素飽和度",
 "PaO₂":"動脈血酸素分圧","DO₂":"酸素運搬量","2,3-DPG":"ジホスホグリセリン酸",
 "INR":"プロトロンビン時間国際標準比","RBC-LR":"赤血球液-白血球除去",
 "Hb":"ヘモグロビン","Ht":"ヘマトクリット","EF":"左室駆出率",
 "ATPase":"アデノシン三リン酸分解酵素","LR":"白血球除去","GVHD":"移植片対宿主病",
 "FFP":"新鮮凍結血漿","CCI":"補正血小板増加数","PBM":"患者血液管理","ICU":"集中治療室",
 "TACO":"輸血関連循環過負荷","TRALI":"輸血関連急性肺障害","BNP":"脳性ナトリウム利尿ペプチド",
 "LDH":"乳酸脱水素酵素","DHTR":"delayedhemolytictransfusionreaction",
 "IVR":"画像下治療","iCa":"イオン化カルシウム",
 "COP":"膠質浸透圧","GFR":"糸球体濾過量","TAL":"thickascendinglimb","PO₂":"酸素分圧",
 "IAP":"腹腔内圧","ScvO₂":"中心静脈血酸素飽和度","ATN":"急性尿細管壊死","BUN":"血中尿素窒素",
 "PT":"近位尿細管","DCT":"遠位尿細管","CD":"集合管",
 "SGLT2":"ナトリウム・グルコース共輸送体","MRA":"ミネラルコルチコイド受容体拮抗薬",
 "AKD":"急性腎臓病","CKD":"慢性腎臓病","eGFR":"推算糸球体濾過量","sCr":"血清クレアチニン",
 "PK":"薬物動態","PD":"薬力学","KRT":"kidneyreplacementtherapy",
 "NaV":"電位依存性ナトリウムチャネル","CNS":"中枢神経系","LAST":"localanestheticsystemictoxicity",
 "ACLS":"二次心肺蘇生法","ASRA":"米国区域麻酔疼痛医学会","TAP":"腹横筋膜面",
 "CSF":"cerebrospinalfluid","METs":"代謝当量","DLCO":"肺一酸化炭素拡散能",
 "DASI":"デューク活動状態指数","RCRI":"改訂心臓リスク指数","CFS":"臨床虚弱スケール",
 "MELD-Na":"終末期肝疾患モデル","CGA":"Cause・GFR・Albuminuria",
 "WHO":"世界保健機関","CRM":"危機資源管理",
}

# 見出しの字送り（"CO R E  CO M P..."）や CO₂ 等の誤検出を除くため、
# 英数字に挟まれていないこと＋直後が下付き数字でないことを条件にする
def first_use(ab):
    pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(ab) + r"(?![A-Za-z0-9₀-₉])")
    for i, t in enumerate(raw):
        # 字送りされた英語見出し行（大文字と空白だけの行）は除外
        body = "\n".join(l for l in t.split("\n")
                         if not re.fullmatch(r"[A-Z0-9｜／\-–\s]{6,}", l))
        if pat.search(body):
            return i + 1
    return None

def first_def(mark):
    for i, t in enumerate(flat):
        if mark in t:
            return i + 1
    return None

bad = []
for ab, mark in sorted(CHECK.items()):
    fu, fd = first_use(ab), first_def(mark)
    if fd is None:
        bad.append((ab, "説明が見つからない", fu, None))
    elif fu is not None and fd > fu:
        bad.append((ab, "説明が初出より後", fu, fd))

print(f"検証した略語：{len(CHECK)}　／　問題：{len(bad)}")
for ab, why, fu, fd in bad:
    print(f"  {ab:<12}{why}  初出 p{fu}  説明 p{fd}")
