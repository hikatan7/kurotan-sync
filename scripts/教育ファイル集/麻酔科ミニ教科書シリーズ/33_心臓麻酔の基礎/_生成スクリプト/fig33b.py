# -*- coding: utf-8 -*-
"""㉝ 図版（第III部の TEE 追加分：図11-1 〜 図17-1）"""
from fig33common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE,
                         C_NOTE)


def f11():
    cv = Canvas(W, 1220)
    y = head(cv, "図11-1　プローブの四つの操作と、画像を変える四つのつまみ",
             "「見えない」ときは、まずこの八つのどれかを動かす。")
    bw = (W - 112 - 3 * 24) / 4
    ops = (
        ("前後", "blue", ["進める・引く", "断面の高さが変わる",
                          "上部食道 → 中部食道 → 経胃"]),
        ("回旋", "green", ["右・左へ回す", "見る方向が変わる",
                           "左右の心腔・肺静脈・大動脈"]),
        ("屈曲", "amber", ["前屈・後屈", "傾きが変わる",
                           "経胃像で心尖を入れる"]),
        ("角度", "purple", ["0〜180°", "同じ位置で断面が変わる",
                            "長軸と短軸を切り替える"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(ops):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5, style=st,
                          title=ttl, title_size=15.5, min_h=220))
    y2 = y + max(hs) + 46
    hs2 = []
    knobs = (
        ("深度", "grey", ["浅くするほど", "分解能と表示が上がる"]),
        ("ゲイン", "grey", ["上げすぎると", "ノイズを構造と見誤る"]),
        ("フォーカス", "grey", ["見たい構造の", "深さに合わせる"]),
        ("周波数", "grey", ["分解能と深達度の", "トレードオフ"]),
    )
    for i, (ttl, st, lines) in enumerate(knobs):
        hs2.append(textbox(cv, 56 + i * (bw + 24), y2, bw, lines, 12.5,
                           style=st, title=ttl, title_size=15, min_h=170))
    y3 = y2 + max(hs2) + 46
    textbox(cv, 56, y3, W - 112, [
        "音響陰影 ── 人工弁やカルシウムの背後は見えない",
        "偽像（サイドローブ・残響）── 構造と見誤らない",
        "その断面に写っていないものは、判断できない",
        "見えなかったことは「見えなかった」と記録する。推測で埋めない",
    ], 13.5, style="red", title="仕組みから生じる落とし穴", title_size=15)
    cv.save(path("f11_probe.png"))


def f12():
    cv = Canvas(W, 1280)
    y = head(cv, "図12-1　中部食道の断面は、角度を回すと連続して変わる",
             "断面の名前を暗記しなくても、角度を辿れば出せる。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "角度", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.06, "0〜10°", "四腔像", BLUE),
             (0.32, "約60°", "交連像", GREEN),
             (0.57, "約90°", "二腔像", PURPLE),
             (0.84, "120〜140°", "長軸像", RED))
    for t, ang, name, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.72, ang, color=col, size=12.5)
        p.note(t, 0.42, name, color=col, size=13.5)
    p.note(0.5, 0.12, "角度を上げていく", color=GREY, size=12.5)

    y2 = y + 250 + 60
    h2 = textbox(cv, 56, y2, W - 112, [
        "四腔像（0〜10°）── 左右の心室と心房、僧帽弁と三尖弁、中隔、心嚢液",
        "交連像（約60°）── 僧帽弁の交連部、逆流の位置",
        "二腔像（約90°）── 左房・左室・左心耳、前壁と下壁",
        "長軸像（120〜140°）── 左室流出路、大動脈弁、僧帽弁前尖、SAM",
    ], 13.5, style="navy", title="中部食道の四つの基本断面", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "大動脈弁は短軸（30〜45°）と長軸（120〜140°）の二つで見る",
        "卵円孔開存は二腔静脈像（90〜110°）で確認する",
        "上行大動脈には TEE で見えない部分が残る ── 心表面エコーが補う",
    ], 13.5, style="amber", title="併せて出す断面", title_size=15)
    cv.save(path("f12_views_me.png"))


def f13():
    cv = Canvas(W, 1180)
    y = head(cv, "図13-1　経胃の断面 ── 壁運動とドプラのために",
             "深部経胃像は、流出路の血流にビームを平行に当てられる数少ない断面。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("経胃 中部短軸像", "blue",
         ["乳頭筋レベル", "三本の冠動脈支配が一枚に入る",
          "壁運動・容量・中隔の形"]),
        ("経胃 二腔像・長軸像", "green",
         ["約90°／約120°", "前壁と下壁、腱索と乳頭筋",
          "流出路と大動脈弁"]),
        ("深部経胃 長軸像", "amber",
         ["進めて前屈", "ビームを血流に平行に",
          "流出路・大動脈弁のドプラ計測"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13, style=st,
                          title=ttl, title_size=15.5, min_h=250))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "心停止の前後で必ず見る ── 新たな壁運動異常に気づきやすい",
        "心室中隔が左へ押されていれば、右室の圧・容量負荷を示す",
    ], 14, style="navy", title="経胃短軸像がいちばん働く場面", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "胃内へ進めるので、食道・胃の病変がある患者では慎重に",
        "前屈を強くかけすぎない ── 粘膜を傷つける",
        "ドプラは角度に依存する ── 平行に当てられているかを確かめる",
    ], 13.5, style="red", title="操作の注意", title_size=15)
    cv.save(path("f13_views_tg.png"))


def f14():
    cv = Canvas(W, 1280)
    y = head(cv, "図14-1　ドプラの三つの道具と、計算できるもの",
             "速さが分かれば圧較差が、流速と断面積が分かれば流量が出る。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("カラードプラ", "blue", ["流れの分布と方向", "逆流ジェットの位置",
                                  "設定で見え方が変わる"]),
        ("パルスドプラ", "green", ["指定した一点の流速", "流出路の VTI",
                                   "高速では折り返す"]),
        ("連続波ドプラ", "amber", ["ビーム上の最大流速", "狭窄・逆流の評価",
                                   "どこの流速かは特定できない"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13, style=st,
                          title=ttl, title_size=16, min_h=240))
    y2 = y + max(hs) + 50
    bw2 = (W - 112 - 40) / 2
    h1 = textbox(cv, 56, y2, bw2, [
        "圧較差 ≒ 4 ×（流速）の二乗",
        "流速が 2 倍になれば、圧較差は 4 倍",
    ], 15, style="navy", title="簡易ベルヌーイ式", title_size=16, min_h=190)
    h2 = textbox(cv, 56 + bw2 + 40, y2, bw2, [
        "一回拍出量 ＝ 断面積 × VTI",
        "流出路径の誤差は二乗で効く",
    ], 15, style="purple", title="連続の式", title_size=16, min_h=190)
    y3 = y2 + max(h1, h2) + 44
    textbox(cv, 56, y3, W - 112, [
        "ビームと血流の角度がずれている ── 流速は過小評価される",
        "エイリアシングを最大流速と読んでしまう",
        "カラーのゲインを上げすぎて、逆流を大きく見せてしまう",
        "術前と条件（心拍数・血圧）が違う値を、そのまま比べてしまう",
    ], 13.5, style="red", title="よくある失敗", title_size=15)
    cv.save(path("f14_doppler.png"))


def f15():
    cv = Canvas(W, 1200)
    y = head(cv, "図16-1　大動脈弁の評価 ── 形・動き・重症度",
             "短軸で形、長軸で動きと周囲、ドプラで重症度。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("短軸像（30〜45°）", "blue", ["弁尖の数（三尖・二尖）", "開放の程度",
                                       "逆流ジェットの位置"]),
        ("長軸像（120〜140°）", "green", ["弁輪径", "上行大動脈近位部",
                                          "逆流ジェットの幅と流出路径"]),
        ("深部経胃像", "amber", ["最大流速", "平均圧較差",
                                 "VTI と弁口面積"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13, style=st,
                          title=ttl, title_size=15.5, min_h=240))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "狭窄の評価は、最大流速・平均圧較差・弁口面積の三つを揃える",
        "心拍出量が低いと圧較差が小さく出る（低流量低圧較差 AS）",
        "麻酔下では後負荷が低く、逆流は軽く見えやすい",
    ], 14, style="navy", title="条件で数字が変わる", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "人工弁置換後は、圧較差・弁周囲逆流・可動性を確認する",
        "評価の基準は人工弁用の推奨に従う",
    ], 13.5, style="grey", min_h=120)
    cv.save(path("f15_av.png"))


def f16():
    cv = Canvas(W, 1280)
    y = head(cv, "図17-1　僧帽弁を部位の言葉で語る",
             "「どこが、どう壊れているか」を言えることが、形成術の会話になる。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "前尖と後尖を、それぞれ三つの区画に分ける",
        "交連像・二腔像・長軸像を組み合わせて",
        "どの区画が問題かを特定する",
        "",
        "逆流ジェットが後方へ → 前尖の逸脱",
        "逆流ジェットが前方へ → 後尖の逸脱",
    ], 13.5, style="blue", title="部位で語る", title_size=16.5, min_h=300)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "I 型：弁尖の動きは正常",
        "　（弁輪拡大・穿孔）",
        "II 型：動きが過剰（逸脱・腱索断裂）",
        "III 型：動きが制限される",
        "　（リウマチ性・虚血性）",
        "",
        "分類が形成術の方針につながる",
    ], 13.5, style="green", title="Carpentier の分類", title_size=16.5,
        min_h=300)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "逆流は減ったか ── 残存の程度と方向",
        "狭窄を作っていないか ── 圧較差",
        "流出路は開いているか ── SAM（第8章）",
        "弁周囲逆流はないか ／ 冠動脈に影響していないか（壁運動）",
    ], 13.5, style="navy", title="修復後に必ず見るもの", title_size=15)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "三尖弁は右心の評価と一組で見る ── 逆流の程度、弁輪径、右室の大きさ",
    ], 14, style="amber", min_h=110)
    cv.save(path("f16_mv.png"))


if __name__ == "__main__":
    for fn in (f11, f12, f13, f14, f15, f16):
        fn()
        print("ok:", fn.__name__)
