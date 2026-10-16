# -*- coding: utf-8 -*-
"""参考文献台帳。本文には {{ID}} で書く。ID は PMID、PubMed にないものは 90000xx。

すべて 2026-09-27 に PubMed・Crossref・J-STAGE・学会/出版社の公式ページで照合した。
照合の経過は ../開心術後ALS_照合結果と検証プロンプト.html にある。
"""

REFS = {
    # ---- ガイドライン・合意文書
    "41122889": ("Cao D, Arens AM, Chow SL, et al. Part 10: Adult and Pediatric Special "
                 "Circumstances of Resuscitation: 2025 American Heart Association Guidelines "
                 "for Cardiopulmonary Resuscitation and Emergency Cardiovascular Care. "
                 "Circulation. 2025;152(16 Suppl 2):S578-S672.",
                 "41122889", "10.1161/CIR.0000000000001380"),
    "41117569": ("Lott C, Karageorgos V, Abelairas-Gomez C, et al. European Resuscitation "
                 "Council Guidelines 2025 Special Circumstances in Resuscitation. "
                 "Resuscitation. 2025;215 Suppl 1:110753.",
                 "41117569", "10.1016/j.resuscitation.2025.110753"),
    "28122680": ("Society of Thoracic Surgeons Task Force on Resuscitation After Cardiac "
                 "Surgery. The Society of Thoracic Surgeons Expert Consensus for the "
                 "Resuscitation of Patients Who Arrest After Cardiac Surgery. "
                 "Ann Thorac Surg. 2017;103(3):1005-1020.",
                 "28122680", "10.1016/j.athoracsur.2016.10.033"),
    "19297185": ("Dunning J, Fabbri A, Kolh PH, et al. Guideline for resuscitation in cardiac "
                 "arrest after cardiac surgery. Eur J Cardiothorac Surg. 2009;36(1):3-28.",
                 "19297185", "10.1016/j.ejcts.2009.01.033"),
    "38046213": ("Karcher C, Jurisevic C, Southwood T, et al. The Australasian ANZSCTS/ANZICS "
                 "guidelines on cardiothoracic advanced life support (CALS-ANZ). "
                 "Crit Care Resusc. 2022;24(3):218-223.",
                 "38046213", ""),
    # ---- 頻度・転帰
    "9440561": ("Anthi A, Tzelepis GE, Alivizatos P, et al. Unexpected cardiac arrest after "
                "cardiac surgery: incidence, predisposing causes, and outcome of open chest "
                "cardiopulmonary resuscitation. Chest. 1998;113(1):15-19.",
                "9440561", "10.1378/chest.113.1.15"),
    "19559193": ("Ngaage DL, Cowen ME. Survival of cardiorespiratory arrest after coronary "
                 "artery bypass grafting or aortic valve surgery. Ann Thorac Surg. "
                 "2009;88(1):64-68.", "19559193", "10.1016/j.athoracsur.2009.03.042"),
    "24820394": ("LaPar DJ, Ghanta RK, Kern JA, et al. Hospital variation in mortality from "
                 "cardiac arrest after cardiac surgery: an opportunity for improvement? "
                 "Ann Thorac Surg. 2014;98(2):534-539.",
                 "24820394", "10.1016/j.athoracsur.2014.03.030"),
    "33621835": ("Mir Mohammad Sadeghi P, Mir Mohammad Sadeghi M. Cardiopulmonary arrest after "
                 "cardiac surgery: a retrospective cohort of 142 patients with nine year "
                 "follow up. Heart Lung. 2021;50(3):382-385.",
                 "33621835", "10.1016/j.hrtlng.2021.01.018"),
    "34219876": ("Moh'd AF, Khasawneh MA, Al-Odwan HT, et al. Postoperative cardiac arrest in "
                 "cardiac surgery-how to improve the outcome? Med Arch. 2021;75(2):149-153.",
                 "34219876", "10.5455/medarh.2021.75.149-153"),
    "19369089": ("Adam Z, Adam S, Everngam RL, et al. Resuscitation after cardiac surgery: "
                 "results of an international survey. Eur J Cardiothorac Surg. "
                 "2009;36(1):29-34.", "19369089", "10.1016/j.ejcts.2009.02.050"),
    "12204734": ("Mackay JH, Powell SJ, Osgathorp J, et al. Six-year prospective audit of "
                 "chest reopening after cardiac arrest. Eur J Cardiothorac Surg. "
                 "2002;22(3):421-425.", "12204734", "10.1016/s1010-7940(02)00294-4"),
    # ---- 手技・治療
    "17693437": ("Richardson L, Dissanayake A, Dunning J. What cardioversion protocol for "
                 "ventricular fibrillation should be followed for patients who arrest shortly "
                 "post-cardiac surgery? Interact Cardiovasc Thorac Surg. 2007;6(6):799-805.",
                 "17693437", "10.1510/icvts.2007.163899"),
    "18000024": ("Twomey D, Das M, Subramanian H, et al. Is internal massage superior to "
                 "external massage for patients suffering a cardiac arrest after cardiac "
                 "surgery? Interact Cardiovasc Thorac Surg. 2008;7(1):151-156.",
                 "18000024", "10.1510/icvts.2007.170399"),
    "41583928": ("Takemoto S, Shimoda TM, Inoue Y, et al. Extracorporeal cardiopulmonary "
                 "resuscitation following cardiac surgery: a scoping review. Resusc Plus. "
                 "2026;27:101210.", "41583928", "10.1016/j.resplu.2025.101210"),
    "40914351": ("Ley SJ, Dunning J. Expert opinion: intensive care unit resternotomy should "
                 "be practiced in all facilities that perform cardiac surgery. Semin Thorac "
                 "Cardiovasc Surg. 2026;38(2):126-132.",
                 "40914351", "10.1053/j.semtcvs.2025.08.003"),
    # ---- 教育
    "16631670": ("Dunning J, Nandi J, Ariffin S, et al. The Cardiac Surgery Advanced Life "
                 "Support Course (CALS): delivering significant improvements in emergency "
                 "cardiothoracic care. Ann Thorac Surg. 2006;81(5):1767-1772.",
                 "16631670", "10.1016/j.athoracsur.2005.12.012"),
    "36826563": ("Peek JJ, Max SA, Bakhuis W, et al. Virtual reality simulator versus "
                 "conventional advanced life support training for cardiopulmonary "
                 "resuscitation post-cardiac surgery: a randomized controlled trial. "
                 "J Cardiovasc Dev Dis. 2023;10(2):67.",
                 "36826563", "10.3390/jcdd10020067"),
    "36413642": ("Whitlock JP. Cardiac Surgery Unit Advanced Life Support training: a 10-year "
                 "retrospective study examining patient mortality outcomes after "
                 "implementation. Dimens Crit Care Nurs. 2023;42(1):22-32.",
                 "36413642", "10.1097/DCC.0000000000000557"),
    "9000011": ("Gali B, Arteaga GM, Au G, Herasevich V. Impact of in situ education on "
                "management of cardiac arrest after cardiac surgery. Southwest J Pulm Crit "
                "Care. 2021;23(2):54-61.", "", "10.13175/swjpcc028-21"),
    "27922571": ("Gali B, Au G, Rosenbush KA. Simulation incorporating cardiac surgery life "
                 "support algorithm into cardiac intensive care unit practice. Simul Healthc. "
                 "2016;11(6):419-424.", "27922571", "10.1097/SIH.0000000000000193"),
    # ---- 国内
    "9000003": ("神尾直, 松永渉, 大塚祐史. 胸骨正中切開術後の心肺蘇生―その特殊性と再開胸を"
                "含めた対応. INTENSIVIST. 2016;8(1):49-59.", "", ""),
    "9000002": ("高木大地, 角浜孝行, 桐生健太郎, ほか. 開心術後心肺蘇生プロトコルCALSの導入と"
                "経験. 日本心臓血管外科学会雑誌. 2023;52(4):239-243.",
                "", "10.4326/jjcvs.52.239"),
    "9000001": ("髙橋伸二. 心臓手術後の心停止. 日本集中治療医学会雑誌. 2024;31(6):559-565.",
                "", "10.3918/jsicm.31_559"),
    "9000004": ("高木大地. CALSのすゝめ―チームで救う心臓血管外科術後心停止. LiSA. "
                "2025;32(6):631-639.", "", "10.11477/mf.134088360320060631"),
    "9000005": ("植野剛. CALS（心大血管術後心停止に対する蘇生プロトコール）の導入と多科・"
                "多職種連携・蘇生学への展開. 蘇生. 2025;44(3):73.", "", ""),
    "9000006": ("植野剛, 野上英次郎, 高木大地, 小渡亮介 訳・執筆. CALSハンドブック 原書第5版 "
                "心臓血管外科術後の急変・心停止に対する対応・心肺蘇生. 東京: 南江堂; 2025.",
                "", ""),
    "9000007": ("特定非営利活動法人 CALS Japan. 活動実績. https://www.calsjapan.org/"
                "（2026年9月27日閲覧）.", "", ""),
    "9000008": ("日本蘇生協議会 監修. JRC蘇生ガイドライン2025. 東京: 医学書院; 2026.", "", ""),
    "9000009": ("日本救急医学会ICLSコース企画運営委員会 編. 改訂第6版 日本救急医学会ICLS"
                "コースガイドブック. 東京: 羊土社; 2026.", "", ""),
    "9000010": ("日本麻酔科学会. 術中心停止に対するプラクティカルガイド. 2021年2月26日制定"
                "（2022年1月6日訂正）.", "", ""),
    "39173710": ("Weber MP, Strobel RJ, Norman AV, et al. Cardiac Surgical Unit-Advanced Life "
                 "Support-certified centers are associated with improved failure to rescue after "
                 "cardiac arrest: a propensity score-matched analysis. J Thorac Cardiovasc Surg. "
                 "2025;169(4):1271-1281.", "39173710", "10.1016/j.jtcvs.2024.08.014"),
    "33456790": ("Brand J, McDonald A, Dunning J. Management of cardiac arrest following cardiac surgery. "
                 "BJA Educ. 2018;18(1):16-22.", "33456790", "10.1016/j.bjae.2017.11.002"),
    "9000013": ("特定非営利活動法人 CALS Japan. CALS とは／CALS Japan とは. https://www.calsjapan.org/cals ・ "
                "https://www.calsjapan.org/about（2026年9月28日閲覧）.", "", ""),
    "9000014": ("湊谷謙司. 書評 CALSハンドブック 原書第5版. 胸部外科. 2026;79(2). "
                "南江堂ウェブサイトに転載（2026年9月28日閲覧）.", "", ""),
    "9000012": ("日本集中治療医学会 第10回関東甲信越支部学術集会 プログラム. パネルディスカッション"
                "「その胸骨、本当に押しますか？―CALSで振り返る開心術後心停止―」. "
                "2026年7月11日, 松本.", "", ""),
}


class Resolver(object):
    """出現順に番号を振る"""

    def __init__(self):
        self.order = []
        self.missing = set()

    def __call__(self, ids):
        nums = []
        for i in ids:
            if i not in REFS:
                self.missing.add(i)
                continue
            if i not in self.order:
                self.order.append(i)
            nums.append(self.order.index(i) + 1)
        return _fmt(nums)

    def rows(self):
        out = []
        for n, i in enumerate(self.order, 1):
            d, pmid, doi = REFS[i]
            out.append([str(n), d, pmid, doi])
        return out


def _fmt(nums):
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append("%d-%d" % (nums[i], nums[j]) if j - i >= 2
                   else ",".join(str(x) for x in nums[i:j + 1]))
        i = j + 1
    return ",".join(out)
