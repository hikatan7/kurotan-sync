# -*- coding: utf-8 -*-
"""㊲ 図版（図1-1 〜 図18-1）"""
from fig37common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)


def f01():
    cv = Canvas(W, 1260)
    y = head(cv, "図1-1　移植の麻酔が持つ三つの特徴",
             "この三つが、準備・段取り・チームの形を決めている。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 患者が二人いる", "blue",
         ["ドナーとレシピエント", "ドナーの管理が",
          "移植片の質を左右する"]),
        ("② 時間が外から決まる", "green",
         ["阻血時間・搬送・到着", "待機のあいだに",
          "準備を完了させておく"]),
        ("③ 臓器が働き始める", "amber",
         ["再灌流の瞬間が山場", "そこまでが麻酔の仕事",
          "免疫抑制も術中に始まる"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13,
                          style=st, title=ttl, title_size=15, min_h=250))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "心臓と肺で臓器は違うが、"
        "「重症の患者に、他人の臓器を入れて、働かせる」構造は同じ",
        "だから麻酔科が引き受ける仕事の形もよく似ている",
    ], 14, style="navy", title="一冊にまとめた理由", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "実際に移植を行う施設は限られている。"
        "多くの読者が関わるのは「移植を受けた患者が別の手術を受ける」場面（第18章）。",
    ], 14, style="red", min_h=130)
    cv.save(path("f01_what_differs.png"))


def f02():
    cv = Canvas(W, 1280)
    y = head(cv, "図5-1　移植手術の時間軸 ── 導入の時刻は逆算で決まる",
             "阻血時間を短くするために、"
             "「届いたときに吻合を始められる状態」を作る。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "時間", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.10, "ドナー手術", "摘出", BLUE),
             (0.34, "搬送", "阻血時間が\n進んでいる", RED),
             (0.58, "到着", "吻合開始", GREEN),
             (0.84, "再灌流", "働き始める", PURPLE))
    for t, when, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.78, when, color=col, size=13)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.42 - j * 0.16, ln, color=col, size=12.5)
    p.note(0.46, 0.10, "この間、レシピエントの準備が並行して進む",
           color=GREY, size=12.5)
    y2 = y + 250 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "早すぎる導入 ── 患者を長く不安定な状態に置くことになる",
        "遅すぎる導入 ── 阻血時間が延びる",
        "だから「移植片の到着時刻」から逆算して決める",
    ], 14, style="navy", title="導入の時刻をどう決めるか", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "この時間軸は麻酔科だけでは決められない。"
        "外科・臨床工学技士・看護・移植の調整に関わる人が"
        "同じ時間軸を共有していること（第19章）。",
    ], 14, style="amber", min_h=130)
    cv.save(path("f02_timeline.png"))


def f03():
    cv = Canvas(W, 1300)
    y = head(cv, "図6-1　除神経された心臓で起きること",
             "移植された心臓は、神経とつながっていない。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("① 安静時心拍数が高い", "blue", ["迷走神経の抑制がない",
                                          "それが普通の状態"]),
        ("② 心拍数の上昇が遅い", "red", ["交感神経の直接支配がない",
                                         "循環血液中の",
                                         "カテコラミンに頼る"]),
        ("③ 前負荷に依存する", "green", ["容量の低下に弱い",
                                         "出血・脱水を避ける"]),
        ("④ 間接的に働く薬が効かない", "purple", ["アトロピンは効かない",
                                                  "直接作用する薬か",
                                                  "ペーシングを使う"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=13.5, min_h=240))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "血圧が下がっても、身体が自力で心拍数を上げて補えない",
        "だから容量を保ち、必要なら直接作用する薬とペーシングで補う",
        "狭心症の痛みも出ない ── 心筋虚血が無症候で進む",
    ], 14, style="navy", title="麻酔でいちばん効いてくること", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "この性質は、移植後何年経っても続く。"
        "移植後の患者が別の手術を受けるとき（第18章）、"
        "いちばん覚えておくべき点である。",
    ], 14, style="red", min_h=130)
    cv.save(path("f03_denervated.png"))


def f04():
    cv = Canvas(W, 1280)
    y = head(cv, "図7-1　移植心の右室が直面する不一致",
             "離脱の山場はここにある。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "レシピエントの肺血管抵抗",
        "　長い心不全のあいだに上がっている",
        "　移植しても、すぐには下がらない",
        "",
        "→ 高いまま",
    ], 14, style="red", title="受ける側", title_size=16.5, min_h=280)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "ドナーの右室",
        "　正常な肺血管抵抗のもとで働いてきた",
        "　高い後負荷に慣れていない",
        "",
        "→ 圧に弱い",
    ], 14, style="blue", title="与えられる側", title_size=16.5, min_h=280)
    y2 = y + max(h1, h2) + 52
    h3 = textbox(cv, 56, y2, W - 112, [
        "肺血管抵抗を下げる ── 酸素化・換気・酸塩基・体温・疼痛、"
        "吸入の肺血管拡張薬",
        "右室を助ける ── 体血圧を保って右冠動脈の灌流を守る、"
        "前負荷は足りなくても多すぎても悪い",
        "それでも駄目なら補助循環（㉞）── 体制を先に確認しておく",
    ], 14, style="navy", title="対策は二方向", title_size=16)
    y3 = y2 + h3 + 46
    textbox(cv, 56, y3, W - 112, [
        "プロタミン投与が肺血管抵抗の急上昇を招くことがある（㉛）。"
        "移植直後の右室にとって、この反応は致命的になりうる。",
    ], 14, style="amber", min_h=130)
    cv.save(path("f04_rv_mismatch.png"))


def f05():
    cv = Canvas(W, 1280)
    y = head(cv, "図10-1　肺移植の進行と、麻酔が引き受けるもの",
             "片肺換気の負債を、最も条件の悪い肺で背負うことになる。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "進行", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.10, "①", "片肺換気\n片側を摘出", BLUE),
             (0.36, "②", "吻合", GREEN),
             (0.60, "③", "再灌流", RED),
             (0.86, "④", "反対側へ\nもう一度", PURPLE))
    for t, no, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, no, color=col, size=17)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12.5)
    y2 = y + 250 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "片肺換気 ── 酸素化と換気が悪化する。もともと予備能がない",
        "肺動脈の遮断 ── 残った肺へ血流が集中し、右室の後負荷が上がる",
        "再灌流 ── 血行動態の変動、肺水腫、移植片機能不全（第13章）",
    ], 14, style="navy", title="同時に見続ける三つ", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "「両肺換気に戻す」という逃げ道が使えない場面が多い。",
        "だから体外循環が、早い段階で選択肢に入ってくる（第12章）。",
    ], 14.5, style="red", min_h=140)
    cv.save(path("f05_lung_tx_flow.png"))


def f06():
    cv = Canvas(W, 1300)
    y = head(cv, "図13-1　再灌流のときに起きること",
             "遮断解除の合図を共有し、準備してから解除する。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 流れ出すもの", "red",
         ["保存液と代謝産物が全身へ", "血圧低下・不整脈",
          "高カリウム"]),
        ("② 入っていくもの", "blue",
         ["移植片へ血流が入る", "肺水腫",
          "ガス交換の悪化"]),
        ("③ 配分が変わる", "purple",
         ["血行動態の再配分", "右室の後負荷が変わる",
          "TEE で確かめる"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14.5, min_h=250))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "昇圧薬・抗不整脈薬を手元に用意する",
        "血液ガスと電解質（とくにカリウム）を確認しておく",
        "換気の設定を、移植片に合わせて決めておく",
        "術者と合図を決める ── ゆっくり解除してもらう",
    ], 14, style="navy", title="解除の前にやっておくこと", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "移植片機能不全の定義と分類は、現在も精密化が議論されている。",
        "分類に当てはめるより、酸素化と画像を経時的に追うほうが役に立つ。",
    ], 14, style="grey", min_h=140)
    cv.save(path("f06_reperfusion.png"))


def f07():
    cv = Canvas(W, 1260)
    y = head(cv, "図18-1　移植後の患者が別の手術に来たとき、確認する四つ",
             "本書の読者の多くが実際に出会うのは、この場面である。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("① 移植片の機能", "blue", ["最近の検査", "拒絶の既往",
                                    "運動能力"]),
        ("② 免疫抑制", "green", ["何を、どのくらい", "止められるか",
                                 "内服できないときの経路"]),
        ("③ 臓器障害", "amber", ["腎機能・血算", "血糖",
                                 "創傷治癒"]),
        ("④ 生理の変化", "purple", ["心：除神経（第6章）",
                                    "肺：咳嗽反射の低下",
                                    "感染の徴候が乏しい"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14, min_h=230))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "アトロピンは効かない ── 徐脈には直接作用する薬かペーシング",
        "前負荷に依存する ── 脱水・出血に弱い",
        "心拍数の応答が遅い ── 血圧低下を自力で補えない",
        "狭心症の痛みが出ない ── 虚血が無症候で進む",
        "脊髄幹麻酔の交感神経遮断に対する代償が働かない",
    ], 13.5, style="navy", title="心臓移植後で特に覚えておくこと",
        title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "免疫抑制薬を止めない ── 中断は拒絶につながる。"
        "絶食・嘔吐で内服できないときの代替経路を決めておく。",
    ], 14, style="red", min_h=130)
    cv.save(path("f07_after_tx.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07):
        fn()
        print("ok:", fn.__name__)
