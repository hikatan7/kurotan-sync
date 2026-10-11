"""復習ノートから、講義の進め方・評価・課題・振り返り手順などの記載を削除する（2026-09-24）。
概念・語句・フレームワークのまとめだけを残す。python strip_logistics.py"""
import io, os, re, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.join(HERE, "notes")
BK = os.path.join(HERE, "_更新前_20260924_講義運営削除")


def load(n):
    return io.open(os.path.join(NOTES, n + ".py"), encoding="utf-8").read()


def save(n, s):
    io.open(os.path.join(NOTES, n + ".py"), "w", encoding="utf-8").write(s)


def del_section(s, start, end):
    """start を含む行から、end の直前までを削除（end は次の見出し行など）"""
    i = s.index(start); i = s.rindex("\n", 0, i) + 1
    j = s.index(end, i); j = s.rindex("\n", 0, j) + 1
    return s[:i] + s[j:]


def del_line(s, key):
    """key を含む1行（1項目）を削除"""
    i = s.index(key); i = s.rindex("\n", 0, i) + 1
    j = s.index("\n", i) + 1
    return s[:i] + s[j:]


def del_closing(s, head):
    """closing の中の、head で始まる連結文字列1つを削除（末尾が '",' の行まで）"""
    i = s.index('        "' + head); j = i
    while True:
        k = s.index("\n", j)
        line = s[j:k]
        if line.strip().startswith("]"):
            raise ValueError("closing end not found: " + head)
        if line.rstrip().endswith('",') or line.rstrip().endswith("',"):
            break
        j = k + 1
    return s[:i] + s[k + 1:]


def renumber(s):
    n = [0]
    def rep(m):
        n[0] += 1
        return f'{m.group(1)}{n[0]}. '
    return re.sub(r'^(        \(")\d+\. ', rep, s, flags=re.M)


EDITS = {
    "acc1": [("sec", "1. このクラスのゴール（p3–5）", '        ("2. '), ("clo", "振り返りのやり方（p63）")],
    "crt1": [("sec", "0. 受講の心構えと全体像（p2–8）", '        ("1. 演習'),
             ("line", '("振り返りの3ステップ：'), ("line", '("評価：'), ("line", '("「わかる」と「できる」は違う：'),
             ("clo", "振り返りの問い（p66）")],
    "crt2": [("clo", "次回に向けて（p152）")],
    "crt3": [("sec", "6. レポートに向けて（p117–120）", "    ],\n    closing=")],
    "crt4": [("clo", "振り返りの進め方（p112–113）")],
    "crt5": [("clo", "事後課題と振り返り（p89・p93）"), ("line", '("枠組み生活", ')],
    "crt6": [("line", '("問い：", "Day1〜6を振り返り'), ("line", '("グロービスで学ぶ価値：'),
             ("clo", "3か月・90日の『クリシン生活』を終えて（p38）"), ("line", '("デルタ（Before→After）"')],
    "ems1": [("clo", "事後課題と実務への適用（p61–63）")],
    "ems2": [("clo", "事後課題（p67–68）")],
    "ems3": [("clo", "事後課題と振り返り（p50–51）")],
    "ems4": [("clo", "振り返りの観点（p60–61）")],
    "ems5": [("clo", "振り返りの観点（p64–65）")],
    "ems6": [("clo", "振り返りの観点（p53）")],
    "fin1": [("line", '("クラスの狙い（p2–3）：'), ("clo", "Day2に向けて（p37）")],
    "hrm1": [("clo", "振り返りの問い（p71）")],
    "hrm3": [("sec", "5. レポートに向けて（p58–62）", "    ],\n    closing=")],
    "mkt1": [("line", '"全6回：Day1〜4が'), ("line", '("ケース・メソッドの目的：'), ("line", '("ケース・メソッド", ')],
    "obh1": [("line", '("クラス構成：')],
    "obh3": [("sec", "5. Day4レポートに向けて（p53–56）", "    ],\n    closing=")],
    "obh4": [("line", '("期待されたレポートの構成：')],
}
RENAME = {
    "fin1": [("1. コースの全体像と身近なファイナンス（p2–13）", "1. 身近なファイナンスと価値評価の3つのアプローチ（p6–13）")],
    "mkt1": [("0. ケース・メソッドの心得とコースの全体像（p3–4, p8）", "0. マーケティング・プロセスの全体像（p8）")],
    "obh4": [("0. レポートの構成と「志事」（p4–10）", "0. 「志事」と価値観（p4–10）")],
}


def main():
    os.makedirs(BK, exist_ok=True)
    for n, eds in EDITS.items():
        shutil.copy2(os.path.join(NOTES, n + ".py"), os.path.join(BK, n + ".py"))
        s = load(n)
        for e in eds:
            if e[0] == "sec":
                s = del_section(s, e[1], e[2])
            elif e[0] == "line":
                s = del_line(s, e[1])
            else:
                s = del_closing(s, e[1])
        for a, b in RENAME.get(n, []):
            assert a in s, (n, a); s = s.replace(a, b)
        if n == "fin1":   # コース全体像の表を削除
            i = s.index('            ("t", ["Day", "テーマ", "内容", "ケース・演習"]')
            j = s.index("], [10, 44, 64, 56]),\n", i) + len("], [10, 44, 64, 56]),\n")
            s = s[:i] + s[j:]
        if n == "hrm4":   # closing の最終行「レポートの添削観点」を削除
            s2 = re.sub(r'\\n"\n        "レポートの添削観点：[^\n]*",\n', '",\n', s)
            assert s2 != s; s = s2
        s = renumber(s)
        compile(s, n, "exec")
        save(n, s)
        print("ok", n)


if __name__ == "__main__":
    main()
