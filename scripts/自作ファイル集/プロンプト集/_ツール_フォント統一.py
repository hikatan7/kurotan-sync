# -*- coding: utf-8 -*-
"""
docx のフォントを1系統に強制統一するツール（AI製docxの font ばらつき対策）

使い方:
    python _ツール_フォント統一.py "対象.docx"
    python _ツール_フォント統一.py "対象.docx" "Yu Mincho"      # 游明朝にする
    python _ツール_フォント統一.py "対象.docx" "Yu Gothic" A4    # A4化も同時に行う

やること:
 1. theme1.xml の日本語フォント欄（a:ea）が空だと、指定のない文字は環境依存の
    フォントで表示される（Linux書き出しで中国語フォントに化ける原因）。ここを埋める。
 2. styles.xml の docDefaults がテーマ参照になっているのを、実フォント名の直接指定に変える。
 3. 本文・ヘッダー・フッター・脚注の全 rFonts を同じフォントに書き換える。
 4. 元ファイルは変更せず、_フォント統一.docx を新規作成する。
"""
import sys, os, re, zipfile, shutil

def canon(font):
    return ('<w:rFonts w:ascii="{f}" w:eastAsia="{f}" w:hAnsi="{f}" w:cs="{f}"/>').format(f=font)

def fix(path, font="Yu Gothic", a4=False):
    out = os.path.splitext(path)[0] + "_フォント統一.docx"
    zin = zipfile.ZipFile(path)
    parts = {n: zin.read(n) for n in zin.namelist()}
    zin.close()
    stats = {"rFonts書換": 0, "テーマ修正": 0, "docDefaults修正": 0}

    targets = [n for n in parts if re.match(
        r'word/(document|header\d*|footer\d*|footnotes|endnotes|styles)\.xml$', n)]
    for n in targets:
        x = parts[n].decode('utf-8')
        def rep(m):
            if 'Courier' in m.group(0):      # 等幅指定は残す
                return m.group(0)
            stats["rFonts書換"] += 1
            return canon(font)
        x = re.sub(r'<w:rFonts[^>]*/>', rep, x)
        x = re.sub(r'<w:rFonts[^>]*>.*?</w:rFonts>', rep, x, flags=re.S)
        if n.endswith('styles.xml'):
            before = x
            x = re.sub(r'<w:rFonts w:asciiTheme[^>]*/>', canon(font), x)
            if x != before:
                stats["docDefaults修正"] += 1
        parts[n] = x.encode('utf-8')

    for n in [k for k in parts if k.startswith('word/theme/')]:
        x = parts[n].decode('utf-8')
        x2 = re.sub(r'<a:latin typeface="[^"]*"', '<a:latin typeface="%s"' % font, x)
        x2 = re.sub(r'<a:ea typeface="[^"]*"',    '<a:ea typeface="%s"'    % font, x2)
        x2 = re.sub(r'<a:cs typeface="[^"]*"',    '<a:cs typeface="%s"'    % font, x2)
        if x2 != x:
            stats["テーマ修正"] += 1
        parts[n] = x2.encode('utf-8')

    if a4:
        x = parts['word/document.xml'].decode('utf-8')
        x = re.sub(r'<w:pgSz w:w="\d+" w:h="\d+"',
                   '<w:pgSz w:w="11906" w:h="16838"', x)   # A4 = 210 x 297mm
        parts['word/document.xml'] = x.encode('utf-8')

    zo = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
    for n, data in parts.items():
        zo.writestr(n, data)
    zo.close()
    return out, stats

def audit(path):
    """使われているフォント指定を数える（修正前後の確認用）"""
    z = zipfile.ZipFile(path); c = {}
    for n in z.namelist():
        if re.match(r'word/(document|styles|header\d*|footer\d*)\.xml$', n):
            x = z.read(n).decode('utf-8')
            for f in re.findall(r'w:eastAsia="([^"]+)"', x):
                c[f] = c.get(f, 0) + 1
    t = [n for n in z.namelist() if n.startswith('word/theme/')]
    ea = re.findall(r'<a:ea typeface="([^"]*)"', z.read(t[0]).decode('utf-8')) if t else []
    return c, ea

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    src = sys.argv[1]
    font = sys.argv[2] if len(sys.argv) > 2 else "Yu Gothic"
    a4 = (len(sys.argv) > 3 and sys.argv[3].upper() == "A4")
    print("修正前:", audit(src))
    out, st = fix(src, font, a4)
    print("修正後:", audit(out))
    print("統計:", st)
    print("出力:", out)
