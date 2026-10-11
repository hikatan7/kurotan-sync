# -*- coding: utf-8 -*-
"""
ファイル保護ツール
  ① 削除保護 : 選んだフォルダ／ファイルを「間違って消せない」状態にする
       ・標準保護 … 対象そのものを削除・改名・移動できなくする（中身は普通に使える）
       ・強力保護 … 中身のファイルまで含めて一切削除できなくする
  ② アイコン変更 : フォルダのアイコンを色分け・記号化して一目で分かるようにする

  ・管理者権限は不要（自分が所有しているファイルの権限を書き換えるだけ）
  ・保護＝Windows のアクセス権(ACL)に「削除の拒否」を追加する方式。
    このアプリを消しても保護は残る。解除もこのアプリから行う。
  ・アイコン＝フォルダ内の desktop.ini を書き換える方式（Windows 標準の仕組み）
"""

import os
import re
import sys
import json
import ctypes
import subprocess
import traceback
from ctypes import wintypes
from datetime import datetime

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from PIL import Image, ImageDraw, ImageTk
    PIL_OK = True
except Exception:
    PIL_OK = False

APP_NAME = "ファイル保護ツール"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(APP_DIR, "設定.json")
ICON_DIR = os.path.join(APP_DIR, "アイコン")

CHECK_ON = "■"
CHECK_OFF = "□"

CREATE_NO_WINDOW = 0x08000000

LEVEL_LABEL = {"standard": "標準", "strong": "強力"}


# ==========================================================================
# Windows API（アイコンの取得用）
# ==========================================================================
user32 = ctypes.WinDLL("user32", use_last_error=True)
gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
shell32 = ctypes.WinDLL("shell32", use_last_error=True)


class ICONINFO(ctypes.Structure):
    _fields_ = [("fIcon", wintypes.BOOL), ("xHotspot", wintypes.DWORD),
                ("yHotspot", wintypes.DWORD), ("hbmMask", wintypes.HBITMAP),
                ("hbmColor", wintypes.HBITMAP)]


class BITMAP(ctypes.Structure):
    _fields_ = [("bmType", wintypes.LONG), ("bmWidth", wintypes.LONG),
                ("bmHeight", wintypes.LONG), ("bmWidthBytes", wintypes.LONG),
                ("bmPlanes", wintypes.WORD), ("bmBitsPixel", wintypes.WORD),
                ("bmBits", ctypes.c_void_p)]


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wintypes.DWORD), ("biWidth", wintypes.LONG),
                ("biHeight", wintypes.LONG), ("biPlanes", wintypes.WORD),
                ("biBitCount", wintypes.WORD), ("biCompression", wintypes.DWORD),
                ("biSizeImage", wintypes.DWORD), ("biXPelsPerMeter", wintypes.LONG),
                ("biYPelsPerMeter", wintypes.LONG), ("biClrUsed", wintypes.DWORD),
                ("biClrImportant", wintypes.DWORD)]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", wintypes.DWORD * 3)]


class SHFILEINFOW(ctypes.Structure):
    _fields_ = [("hIcon", wintypes.HICON), ("iIcon", ctypes.c_int),
                ("dwAttributes", wintypes.DWORD),
                ("szDisplayName", wintypes.WCHAR * 260),
                ("szTypeName", wintypes.WCHAR * 80)]


user32.PrivateExtractIconsW.argtypes = [wintypes.LPCWSTR, ctypes.c_int, ctypes.c_int,
                                        ctypes.c_int, ctypes.POINTER(wintypes.HICON),
                                        ctypes.POINTER(wintypes.UINT), wintypes.UINT,
                                        wintypes.UINT]
user32.PrivateExtractIconsW.restype = wintypes.UINT
user32.GetIconInfo.argtypes = [wintypes.HICON, ctypes.POINTER(ICONINFO)]
user32.DestroyIcon.argtypes = [wintypes.HICON]
gdi32.GetObjectW.argtypes = [wintypes.HGDIOBJ, ctypes.c_int, ctypes.c_void_p]
gdi32.DeleteObject.argtypes = [wintypes.HGDIOBJ]
gdi32.CreateCompatibleDC.argtypes = [wintypes.HDC]
gdi32.CreateCompatibleDC.restype = wintypes.HDC
gdi32.DeleteDC.argtypes = [wintypes.HDC]
gdi32.GetDIBits.argtypes = [wintypes.HDC, wintypes.HBITMAP, wintypes.UINT, wintypes.UINT,
                            ctypes.c_void_p, ctypes.POINTER(BITMAPINFO), wintypes.UINT]
shell32.ExtractIconExW.argtypes = [wintypes.LPCWSTR, ctypes.c_int,
                                   ctypes.POINTER(wintypes.HICON),
                                   ctypes.POINTER(wintypes.HICON), wintypes.UINT]
shell32.ExtractIconExW.restype = wintypes.UINT
shell32.SHGetFileInfoW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD,
                                   ctypes.POINTER(SHFILEINFOW), wintypes.UINT,
                                   wintypes.UINT]
shell32.SHChangeNotify.argtypes = [wintypes.LONG, wintypes.UINT,
                                   ctypes.c_void_p, ctypes.c_void_p]

SHGFI_ICON = 0x000000100
SHGFI_SMALLICON = 0x000000001
SHGFI_LARGEICON = 0x000000000
SHCNE_ASSOCCHANGED = 0x08000000
SHCNE_UPDATEDIR = 0x00001000
SHCNE_UPDATEITEM = 0x00002000
SHCNF_PATHW = 0x0005
SHCNF_IDLIST = 0x0000


def _bitmap_to_rgba(hbm):
    bm = BITMAP()
    if not gdi32.GetObjectW(hbm, ctypes.sizeof(BITMAP), ctypes.byref(bm)):
        return None
    w, h = bm.bmWidth, bm.bmHeight
    if w <= 0 or h <= 0:
        return None
    hdc = gdi32.CreateCompatibleDC(0)
    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = w
    bmi.bmiHeader.biHeight = -h
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = 0
    buf = ctypes.create_string_buffer(w * h * 4)
    ok = gdi32.GetDIBits(hdc, hbm, 0, h, buf, ctypes.byref(bmi), 0)
    gdi32.DeleteDC(hdc)
    if not ok:
        return None
    return Image.frombuffer("RGBA", (w, h), buf.raw, "raw", "BGRA", 0, 1)


def hicon_to_image(hicon):
    """HICON を PIL イメージへ。取れなければ None"""
    if not PIL_OK or not hicon:
        return None
    info = ICONINFO()
    if not user32.GetIconInfo(hicon, ctypes.byref(info)):
        return None
    img = None
    try:
        if info.hbmColor:
            img = _bitmap_to_rgba(info.hbmColor)
            if img is not None and img.getextrema()[3][1] == 0 and info.hbmMask:
                mask = _bitmap_to_rgba(info.hbmMask)
                if mask is not None:
                    img.putalpha(mask.convert("L").point(lambda v: 0 if v > 127 else 255))
        elif info.hbmMask:
            m = _bitmap_to_rgba(info.hbmMask)
            if m is not None:
                w, h = m.size
                img = m.crop((0, h // 2, w, h))
    except Exception:
        img = None
    finally:
        if info.hbmColor:
            gdi32.DeleteObject(info.hbmColor)
        if info.hbmMask:
            gdi32.DeleteObject(info.hbmMask)
    return img


def dll_icon_count(path):
    try:
        return int(shell32.ExtractIconExW(path, -1, None, None, 0))
    except Exception:
        return 0


def extract_dll_icon(path, index, size=48):
    """DLL/EXE/ICO の index 番目のアイコンを PIL イメージで返す"""
    if not PIL_OK:
        return None
    h = wintypes.HICON()
    ids = wintypes.UINT()
    try:
        n = user32.PrivateExtractIconsW(path, index, size, size,
                                        ctypes.byref(h), ctypes.byref(ids), 1, 0)
    except Exception:
        return None
    if n < 1 or not h.value:
        return None
    try:
        img = hicon_to_image(h)
    finally:
        user32.DestroyIcon(h)
    if img is None:
        return None
    if img.getextrema()[3][1] == 0:      # 完全に透明＝中身なし
        return None
    if img.size != (size, size):
        img = img.resize((size, size), Image.LANCZOS)
    return img


def shell_icon(path, size=16):
    """エクスプローラーが今実際に表示しているアイコンを取得"""
    if not PIL_OK:
        return None
    sfi = SHFILEINFOW()
    flags = SHGFI_ICON | (SHGFI_SMALLICON if size <= 16 else SHGFI_LARGEICON)
    try:
        r = shell32.SHGetFileInfoW(path, 0, ctypes.byref(sfi), ctypes.sizeof(sfi), flags)
    except Exception:
        return None
    if not r or not sfi.hIcon:
        return None
    try:
        img = hicon_to_image(sfi.hIcon)
    finally:
        user32.DestroyIcon(sfi.hIcon)
    if img is not None and img.size != (size, size):
        img = img.resize((size, size), Image.LANCZOS)
    return img


def refresh_explorer(path=None, item=None):
    """アイコンの変更をエクスプローラーに知らせる"""
    try:
        if item:
            shell32.SHChangeNotify(SHCNE_UPDATEITEM, SHCNF_PATHW,
                                   ctypes.c_wchar_p(item), None)
        if path:
            shell32.SHChangeNotify(SHCNE_UPDATEDIR, SHCNF_PATHW,
                                   ctypes.c_wchar_p(path), None)
        shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)
    except Exception:
        pass


def rebuild_icon_cache():
    """アイコンキャッシュを作り直す（エクスプローラーを一度落として再起動する）。

    フォルダのアイコンは iconcache だけでなく thumbcache（中身のサムネイル）にも
    保持されていて、サムネイルが残っているとカスタムアイコンが出てこない。
    両方消す必要がある。
    戻り値：(消したキャッシュ数, エラー文字列)"""
    err = ""
    removed = 0
    try:
        run_hidden(["taskkill", "/f", "/im", "explorer.exe"])
        d = os.path.join(os.environ.get("LOCALAPPDATA", ""),
                         "Microsoft", "Windows", "Explorer")
        try:
            for f in os.listdir(d):
                low = f.lower()
                if low.startswith("iconcache") or low.startswith("thumbcache"):
                    try:
                        os.remove(os.path.join(d, f))
                        removed += 1
                    except Exception:
                        pass
        except Exception as e:
            err = str(e)
    finally:
        try:
            subprocess.Popen(["explorer.exe"], creationflags=CREATE_NO_WINDOW)
        except Exception as e:
            err = (err + " / " if err else "") + "エクスプローラーの再起動に失敗: %s" % e
    return removed, err


# ==========================================================================
# 汎用
# ==========================================================================
def norm(p):
    return os.path.normcase(os.path.normpath(os.path.abspath(p)))


def human_size(n):
    if n is None:
        return ""
    f = float(n)
    for u in ["B", "KB", "MB", "GB", "TB"]:
        if f < 1024 or u == "TB":
            return ("%.0f %s" % (f, u)) if u == "B" else ("%.1f %s" % (f, u))
        f /= 1024
    return ""


def fmt_time(ts):
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ""


def run_hidden(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, creationflags=CREATE_NO_WINDOW)
        out = (p.stdout or b"") + (p.stderr or b"")
        try:
            text = out.decode("oem", errors="replace")
        except Exception:
            text = out.decode("utf-8", errors="replace")
        return p.returncode, text.strip()
    except Exception as e:
        return -1, str(e)


# ==========================================================================
# 削除保護（アクセス権 / icacls）
# ==========================================================================
#  Windows の削除判定は
#     「対象そのものの Delete 権」 か 「親フォルダの 子の削除(DC) 権」
#  のどちらかが通れば削除できてしまう。
#  そのため対象に「削除の拒否(DE)」を付けるだけでは効かないことがあり、
#  親フォルダ側の DC も塞いでおく必要がある（他のファイルの削除には影響しない）。

_dom = os.environ.get("USERDOMAIN", "")
_usr = os.environ.get("USERNAME", "")
USER_ACCOUNT = ("%s\\%s" % (_dom, _usr)) if _dom else _usr

ACE_RE = re.compile(r'^(?P<sid>[^:]+):(?P<flags>(?:\([^)]*\))+)\s*$')
BROAD_SIDS = {"everyone", "builtin\\users", "nt authority\\authenticated users",
              "authenticated users", "users"}


def read_aces(path):
    """icacls の出力を読んで ACE 一覧を返す"""
    rc, out = run_hidden(["icacls", path])
    aces = []
    for line in out.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.lower().startswith(path.lower()):
            s = s[len(path):].strip()
        m = ACE_RE.match(s)
        if not m:
            continue
        flags = re.findall(r'\(([^)]*)\)', m.group("flags"))
        aces.append({
            "sid": m.group("sid").strip(),
            "flags": flags,
            "inherited": "I" in flags,
            "deny": "DENY" in flags,
            "rights": flags[-1] if flags else "",
        })
    return aces


def _rights_set(rights):
    return set(x.strip().upper() for x in rights.split(",") if x.strip())


def parent_blocks_delete_child(parent):
    """親フォルダ側で『子の削除』が塞がれているか（＝保護が確実に効くか）"""
    for a in read_aces(parent):
        if not a["deny"]:
            continue
        if a["sid"].lower() not in BROAD_SIDS and a["sid"].lower() != USER_ACCOUNT.lower():
            continue
        if _rights_set(a["rights"]) & {"DC", "F", "M"}:
            return True
    return False


def set_deny(path, spec):
    """path に対する自分あての拒否 ACE を spec 一つだけにする（None なら全解除）"""
    run_hidden(["icacls", path, "/remove:d", USER_ACCOUNT, "/C", "/Q"])
    if not spec:
        return True, ""
    rc, out = run_hidden(["icacls", path, "/deny", USER_ACCOUNT + ":" + spec, "/C", "/Q"])
    return rc == 0, out


def _level_from_flags(flags):
    r = _rights_set(flags[-1] if flags else "")
    if not (r & {"DE", "D", "F", "M"}):
        return None
    if "DC" in r and ("OI" in flags or "CI" in flags):
        return "strong"
    return "standard"


def detect_protection(path):
    """実際の ACL から保護状態を判定 → None / 'standard' / 'strong'"""
    me = USER_ACCOUNT.lower()
    for a in read_aces(path):
        if not a["deny"] or a["inherited"] or a["sid"].lower() != me:
            continue
        lv = _level_from_flags(a["flags"])
        if lv:
            return lv
    return None


def scan_protection(dirpath, children):
    """フォルダ直下の全項目の保護状態を icacls 一回で調べる → {正規化パス: level}"""
    res = {}
    if not children:
        return res
    rc, out = run_hidden(["icacls", os.path.join(dirpath, "*")])
    lookup = {c.lower(): c for c in children}
    me = USER_ACCOUNT.lower()
    cur = None
    for raw in out.splitlines():
        if not raw.strip():
            cur = None
            continue
        line = raw
        if raw[:1] not in (" ", "\t"):
            cur = None
            low = raw.lower()
            for cl, c in lookup.items():
                if low.startswith(cl + " "):
                    cur = c
                    line = raw[len(cl):]
                    break
            if cur is None:
                continue
        if cur is None:
            continue
        m = ACE_RE.match(line.strip())
        if not m:
            continue
        flags = re.findall(r'\(([^)]*)\)', m.group("flags"))
        if "DENY" not in flags or "I" in flags:
            continue
        if m.group("sid").strip().lower() != me:
            continue
        lv = _level_from_flags(flags)
        if lv:
            res[norm(cur)] = lv
    return res


# ==========================================================================
# フォルダアイコン（desktop.ini）
# ==========================================================================
def _read_text(path):
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except Exception:
        return ""
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        try:
            return raw.decode("utf-16")
        except Exception:
            pass
    for enc in ("mbcs", "utf-8"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode("utf-8", errors="replace")


def _write_text(path, text):
    try:
        with open(path, "w", encoding="mbcs", newline="") as f:
            f.write(text)
        return
    except Exception:
        pass
    with open(path, "w", encoding="utf-16", newline="") as f:
        f.write(text)


def _attrib(args, target):
    run_hidden(["attrib"] + args + [target])


def set_folder_icon(folder, icon_ref):
    """icon_ref = 'C:\\path\\to\\file.ico,0' 形式"""
    ini = os.path.join(folder, "desktop.ini")
    if os.path.exists(ini):
        _attrib(["-h", "-s", "-r"], ini)
    body = _read_text(ini) if os.path.exists(ini) else ""
    lines = [l for l in body.splitlines()
             if not re.match(r'\s*(IconResource|IconFile|IconIndex)\s*=', l, re.I)]
    if not any(l.strip().lower() == "[.shellclassinfo]" for l in lines):
        lines.insert(0, "[.ShellClassInfo]")
    out = []
    inserted = False
    for l in lines:
        out.append(l)
        if not inserted and l.strip().lower() == "[.shellclassinfo]":
            out.append("IconResource=" + icon_ref)
            inserted = True
    _write_text(ini, "\r\n".join(out) + "\r\n")
    _attrib(["+h", "+s"], ini)
    _attrib(["+r"], folder)
    refresh_explorer(os.path.dirname(folder), item=folder)


def clear_folder_icon(folder):
    ini = os.path.join(folder, "desktop.ini")
    if os.path.exists(ini):
        _attrib(["-h", "-s", "-r"], ini)
        body = _read_text(ini)
        lines = [l for l in body.splitlines()
                 if not re.match(r'\s*(IconResource|IconFile|IconIndex)\s*=', l, re.I)]
        meaningful = [l for l in lines
                      if l.strip() and not l.strip().startswith("[")]
        if meaningful:
            _write_text(ini, "\r\n".join(lines) + "\r\n")
            _attrib(["+h", "+s"], ini)
        else:
            try:
                os.remove(ini)
            except Exception:
                _write_text(ini, "")
                _attrib(["+h", "+s"], ini)
    _attrib(["-r"], folder)
    refresh_explorer(os.path.dirname(folder), item=folder)


def set_shortcut_icon(lnk_path, icon_ref):
    """ショートカット(.lnk)のアイコンを変更"""
    ps = ("$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%s');"
          "$s.IconLocation='%s';$s.Save()"
          % (lnk_path.replace("'", "''"), icon_ref.replace("'", "''")))
    rc, out = run_hidden(["powershell", "-NoProfile", "-NonInteractive",
                          "-ExecutionPolicy", "Bypass", "-Command", ps])
    refresh_explorer(os.path.dirname(lnk_path))
    return rc == 0, out


# ==========================================================================
# カラーフォルダアイコンの生成
# ==========================================================================
PALETTE = [
    ("red",    "赤",     (0xC6, 0x28, 0x28), (0xEF, 0x53, 0x50)),
    ("orange", "オレンジ", (0xE6, 0x5A, 0x00), (0xFB, 0x8C, 0x00)),
    ("amber",  "山吹",   (0xE0, 0xA0, 0x00), (0xFF, 0xC7, 0x2C)),
    ("lime",   "黄緑",   (0x63, 0x8E, 0x1F), (0x9C, 0xCC, 0x65)),
    ("green",  "緑",     (0x24, 0x7A, 0x46), (0x4C, 0xAF, 0x50)),
    ("teal",   "青緑",   (0x00, 0x69, 0x5C), (0x26, 0xA6, 0x9A)),
    ("cyan",   "水色",   (0x00, 0x7A, 0xB5), (0x4F, 0xC3, 0xF7)),
    ("blue",   "青",     (0x15, 0x65, 0xC0), (0x42, 0x8B, 0xEC)),
    ("indigo", "紺",     (0x28, 0x35, 0x93), (0x5C, 0x6B, 0xC0)),
    ("purple", "紫",     (0x6A, 0x1B, 0x9A), (0xAB, 0x47, 0xBC)),
    ("pink",   "桃",     (0xAD, 0x14, 0x57), (0xEC, 0x5A, 0x8D)),
    ("brown",  "茶",     (0x4E, 0x34, 0x2E), (0x8D, 0x6E, 0x63)),
    ("slate",  "灰青",   (0x37, 0x47, 0x4F), (0x78, 0x90, 0x9C)),
    ("gray",   "灰",     (0x54, 0x54, 0x54), (0x9E, 0x9E, 0x9E)),
]

VARIANTS = [("plain", ""), ("lock", "＋鍵")]


def _folder_image(dark, light, lock=False):
    S = 256
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([20, 44, 116, 100], radius=12, fill=dark + (255,))
    d.rounded_rectangle([20, 62, 236, 216], radius=18, fill=dark + (255,))
    d.rounded_rectangle([20, 88, 236, 216], radius=18, fill=light + (255,))
    d.rounded_rectangle([20, 88, 236, 102], radius=7,
                        fill=tuple(min(255, c + 26) for c in light) + (255,))
    if lock:
        d.ellipse([144, 122, 236, 214], fill=(255, 255, 255, 255))
        d.ellipse([150, 128, 230, 208], fill=dark + (255,))
        d.arc([172, 144, 208, 182], start=180, end=360, fill=(255, 255, 255, 255), width=9)
        d.rounded_rectangle([168, 166, 212, 196], radius=6, fill=(255, 255, 255, 255))
    return img


def ensure_icons():
    """カラーフォルダアイコン(.ico)を生成（無いものだけ作る）"""
    if not PIL_OK:
        return []
    os.makedirs(ICON_DIR, exist_ok=True)
    made = []
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    for key, label, dark, light in PALETTE:
        for vkey, vlabel in VARIANTS:
            name = "folder_%s%s.ico" % (key, "" if vkey == "plain" else "_lock")
            path = os.path.join(ICON_DIR, name)
            if not os.path.exists(path):
                try:
                    _folder_image(dark, light, lock=(vkey == "lock")).save(
                        path, format="ICO", sizes=sizes)
                except Exception:
                    continue
            made.append((path, "%sフォルダ%s" % (label, vlabel)))
    return made


# ==========================================================================
# 設定（保護台帳）
# ==========================================================================
class Store:
    def __init__(self):
        self.data = {"protected": {}, "icons": {}, "applied": {}, "last_dir": ""}
        self.load()

    def load(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, encoding="utf-8") as f:
                    d = json.load(f)
                for k in self.data:
                    if k in d:
                        self.data[k] = d[k]
            except Exception:
                pass

    def save(self):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ---- 保護 -----------------------------------------------------------
    @property
    def protected(self):
        return self.data["protected"]

    def level_of(self, path):
        e = self.protected.get(norm(path))
        return e.get("level") if e else None

    def desired_spec(self, key):
        """key(正規化パス) に付けるべき拒否 ACE の指定文字列"""
        e = self.protected.get(key)
        real = e["path"] if e else key
        isdir = os.path.isdir(real)
        rights = []
        inherit = False
        if e:
            rights.append("DE")
            if isdir and e.get("level") == "strong":
                rights.append("DC")
                inherit = True
        if isdir and not inherit:
            if any(os.path.dirname(k) == key for k in self.protected):
                rights.append("DC")
        if not rights:
            return None
        return ("(OI)(CI)" if inherit else "") + "(" + ",".join(rights) + ")"

    def reconcile(self, extra=()):
        """台帳の内容どおりに実際のアクセス権を書き直す"""
        targets = set(self.data["applied"].keys())
        targets |= set(self.protected.keys())
        targets |= set(os.path.dirname(k) for k in self.protected.keys())
        targets |= set(norm(p) for p in extra)

        applied = {}
        errors = []
        real_of = {}
        for k, e in self.protected.items():
            real_of[k] = e["path"]
        for key in sorted(targets):
            real = real_of.get(key, key)
            if not os.path.exists(real):
                continue
            spec = self.desired_spec(key)
            ok, msg = set_deny(real, spec)
            if spec and not ok:
                errors.append((real, msg))
            elif spec:
                applied[key] = spec
        self.data["applied"] = applied
        self.save()
        return errors

    def prune(self):
        """消えてしまった場所の記録を整理する。
        （USB など切り離されたドライブの記録は消さない）"""
        removed = 0
        for section in ("protected", "icons"):
            for k, e in list(self.data[section].items()):
                p = e.get("path", k)
                drive = os.path.splitdrive(p)[0] + os.sep
                if os.path.exists(drive) and not os.path.exists(p):
                    del self.data[section][k]
                    removed += 1
        for k in list(self.data["applied"].keys()):
            drive = os.path.splitdrive(k)[0] + os.sep
            if os.path.exists(drive) and not os.path.exists(k):
                del self.data["applied"][k]
        if removed:
            self.save()
        return removed

    def protect(self, path, level):
        self.protected[norm(path)] = {
            "path": os.path.abspath(path),
            "level": level,
            "at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def unprotect(self, path):
        self.protected.pop(norm(path), None)

    # ---- アイコン -------------------------------------------------------
    @property
    def icons(self):
        return self.data["icons"]

    def set_icon(self, path, ref, label):
        self.icons[norm(path)] = {"path": os.path.abspath(path),
                                  "ref": ref, "label": label}

    def clear_icon(self, path):
        self.icons.pop(norm(path), None)

    def icon_label(self, path):
        e = self.icons.get(norm(path))
        return e.get("label", "") if e else ""


# ==========================================================================
# アイコン選択ダイアログ
# ==========================================================================
DLL_CHOICES = [
    ("Windows 標準（imageres.dll）", r"%SystemRoot%\System32\imageres.dll"),
    ("シェル（shell32.dll）",        r"%SystemRoot%\System32\shell32.dll"),
    ("機器（ddores.dll）",           r"%SystemRoot%\System32\ddores.dll"),
    ("ネットワーク（netshell.dll）", r"%SystemRoot%\System32\netshell.dll"),
    ("クラシック（pifmgr.dll）",     r"%SystemRoot%\System32\pifmgr.dll"),
    ("旧アイコン（moricons.dll）",   r"%SystemRoot%\System32\moricons.dll"),
]


class IconPicker(tk.Toplevel):
    """アイコンを選ぶダイアログ。result = (icon_ref, label) / None"""

    def __init__(self, master, font):
        super().__init__(master)
        self.title("アイコンを選ぶ")
        self.geometry("880x620")
        self.transient(master)
        self.grab_set()
        self.font = font
        self.result = None
        self._refs = []          # PhotoImage 保持用
        self._selected = None    # (ref, label, PIL image)
        self._tiles = {}

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=(8, 4))

        self.tab_color = ttk.Frame(nb)
        self.tab_win = ttk.Frame(nb)
        self.tab_file = ttk.Frame(nb)
        nb.add(self.tab_color, text="  カラーフォルダ  ")
        nb.add(self.tab_win, text="  Windows のアイコン  ")
        nb.add(self.tab_file, text="  ファイルから選ぶ  ")

        self._build_color()
        self._build_win()
        self._build_file()

        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=8, pady=(0, 8))
        self.prev_canvas = tk.Canvas(bar, width=52, height=52, highlightthickness=1,
                                     highlightbackground="#c8c8c8", bg="#ffffff")
        self.prev_canvas.pack(side="left")
        self.prev_label = ttk.Label(bar, text="アイコンを選んでください", font=font)
        self.prev_label.pack(side="left", padx=10)
        ttk.Button(bar, text="キャンセル", command=self.destroy).pack(side="right")
        self.ok_btn = ttk.Button(bar, text="このアイコンにする", command=self._ok,
                                 state="disabled")
        self.ok_btn.pack(side="right", padx=6)

    # -- 共通 ------------------------------------------------------------
    def _scroll_area(self, parent):
        wrap = ttk.Frame(parent)
        wrap.pack(fill="both", expand=True)
        canvas = tk.Canvas(wrap, highlightthickness=0, bg="#fafafa")
        sb = ttk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind("<Enter>", lambda e: setattr(self, "_wheel", canvas))
        if not getattr(self, "_wheel_bound", False):
            self._wheel_bound = True
            self.bind_all("<MouseWheel>", self._on_wheel)
        return inner

    def _on_wheel(self, ev):
        c = getattr(self, "_wheel", None)
        if c is not None:
            try:
                c.yview_scroll(int(-ev.delta / 120), "units")
            except Exception:
                pass

    def _add_tile(self, parent, img, ref, label, row, col, caption=None):
        photo = ImageTk.PhotoImage(img)
        self._refs.append(photo)
        f = tk.Frame(parent, bd=2, relief="flat", bg="#fafafa")
        lbl = tk.Label(f, image=photo, bg="#fafafa")
        lbl.pack(padx=6, pady=(5, 0))
        cap = tk.Label(f, text=caption if caption is not None else label,
                       font=(self.font[0], 8), bg="#fafafa",
                       wraplength=96, justify="center")
        cap.pack(pady=(0, 5))
        f.grid(row=row, column=col, padx=4, pady=4, sticky="n")
        for w in (f, lbl, cap):
            w.bind("<Button-1>", lambda e, r=ref, l=label, i=img, fr=f: self._select(r, l, i, fr))
            w.bind("<Double-Button-1>", lambda e, r=ref, l=label, i=img, fr=f:
                   (self._select(r, l, i, fr), self._ok()))
        self._tiles[id(f)] = f
        return f

    def _select(self, ref, label, img, frame=None):
        for f in self._tiles.values():
            try:
                f.configure(relief="flat", bg="#fafafa")
            except Exception:
                pass
        if frame is not None:
            frame.configure(relief="solid", bg="#cfe4ff")
        self._selected = (ref, label, img)
        self.prev_canvas.delete("all")
        big = img.resize((48, 48), Image.LANCZOS)
        self._prev_photo = ImageTk.PhotoImage(big)
        self.prev_canvas.create_image(26, 26, image=self._prev_photo)
        self.prev_label.configure(text=label)
        self.ok_btn.configure(state="normal")

    def _ok(self):
        if self._selected:
            self.result = (self._selected[0], self._selected[1])
            self.destroy()

    # -- タブ1 カラーフォルダ ---------------------------------------------
    def _build_color(self):
        ttk.Label(self.tab_color, font=self.font,
                  text="用途ごとに色分けすると一覧で見分けやすくなります"
                       "（鍵つきは保護中の目印に）").pack(anchor="w", padx=10, pady=6)
        inner = self._scroll_area(self.tab_color)
        items = ensure_icons()
        for i, (path, label) in enumerate(items):
            try:
                img = Image.open(path).convert("RGBA").resize((48, 48), Image.LANCZOS)
            except Exception:
                continue
            self._add_tile(inner, img, path + ",0", label, i // 8, i % 8,
                           caption=label.replace("フォルダ", ""))

    # -- タブ2 Windows のアイコン -----------------------------------------
    def _build_win(self):
        top = ttk.Frame(self.tab_win)
        top.pack(fill="x", padx=10, pady=6)
        ttk.Label(top, text="種類：", font=self.font).pack(side="left")
        self.dll_var = tk.StringVar(value=DLL_CHOICES[0][0])
        cb = ttk.Combobox(top, textvariable=self.dll_var, state="readonly", width=34,
                          values=[c[0] for c in DLL_CHOICES], font=self.font)
        cb.pack(side="left")
        cb.bind("<<ComboboxSelected>>", lambda e: self._load_dll())
        self.win_status = ttk.Label(top, text="", font=self.font)
        self.win_status.pack(side="left", padx=10)
        self.win_inner = self._scroll_area(self.tab_win)
        self.after(200, self._load_dll)

    def _load_dll(self):
        for w in self.win_inner.winfo_children():
            w.destroy()
        name = self.dll_var.get()
        path = dict((a, b) for a, b in DLL_CHOICES).get(name)
        path = os.path.expandvars(path)
        if not os.path.exists(path):
            self.win_status.configure(text="見つかりません")
            return
        total = min(dll_icon_count(path), 400)
        self.win_status.configure(text="読み込み中…")
        state = {"i": 0, "n": 0}

        def chunk():
            if not self.winfo_exists():
                return
            end = min(state["i"] + 24, total)
            for idx in range(state["i"], end):
                img = extract_dll_icon(path, idx, 48)
                if img is None:
                    continue
                self._add_tile(self.win_inner, img, "%s,%d" % (path, idx),
                               "%s の %d 番" % (os.path.basename(path), idx),
                               state["n"] // 8, state["n"] % 8, caption=str(idx))
                state["n"] += 1
            state["i"] = end
            if end < total:
                self.win_status.configure(text="読み込み中… %d / %d" % (end, total))
                self.after(1, chunk)
            else:
                self.win_status.configure(text="%d 個" % state["n"])

        chunk()

    # -- タブ3 ファイルから選ぶ -------------------------------------------
    def _build_file(self):
        f = ttk.Frame(self.tab_file)
        f.pack(fill="x", padx=12, pady=14)
        ttk.Label(f, font=self.font,
                  text="手持ちの .ico ファイル、または .exe / .dll の中のアイコンを使えます"
                  ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))
        self.file_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.file_var, width=58, font=self.font
                  ).grid(row=1, column=0, sticky="we")
        ttk.Button(f, text="参照…", command=self._browse).grid(row=1, column=1, padx=6)
        ttk.Label(f, text="番号：", font=self.font).grid(row=2, column=0, sticky="e", pady=8)
        self.idx_var = tk.IntVar(value=0)
        ttk.Spinbox(f, from_=0, to=999, textvariable=self.idx_var, width=6,
                    command=self._load_file, font=self.font
                    ).grid(row=2, column=1, sticky="w", pady=8)
        ttk.Button(f, text="表示", command=self._load_file).grid(row=2, column=2, sticky="w")
        self.file_inner = ttk.Frame(self.tab_file)
        self.file_inner.pack(fill="both", expand=True, padx=12)

    def _browse(self):
        p = filedialog.askopenfilename(
            parent=self, title="アイコンを含むファイルを選ぶ",
            filetypes=[("アイコン / プログラム", "*.ico;*.exe;*.dll"),
                       ("すべてのファイル", "*.*")])
        if p:
            self.file_var.set(p)
            self._load_file()

    def _load_file(self):
        for w in self.file_inner.winfo_children():
            w.destroy()
        p = self.file_var.get().strip('"')
        if not p or not os.path.exists(p):
            return
        idx = int(self.idx_var.get() or 0)
        img = extract_dll_icon(p, idx, 48)
        if img is None:
            ttk.Label(self.file_inner, text="このファイルの %d 番にアイコンがありません" % idx,
                      font=self.font).pack(anchor="w")
            return
        ref = "%s,%d" % (os.path.abspath(p), idx)
        label = "%s (%d)" % (os.path.basename(p), idx)
        fr = self._add_tile(self.file_inner, img, ref, label, 0, 0)
        self._select(ref, label, img, fr)


# ==========================================================================
# メインウィンドウ
# ==========================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1180x800")
        self.minsize(900, 620)
        self.font = ("Meiryo UI", 10)
        self.store = Store()
        self.store.prune()
        self.checked = set()
        self.rows = {}          # iid -> dict
        self.img_cache = {}
        self.sort_key = None
        self.sort_desc = False

        self._style()
        self._build()

        start = self.store.data.get("last_dir") or self._desktop()
        if not os.path.isdir(start):
            start = self._desktop()
        self.path_var.set(start)
        self.after(80, self.reload)

    # -- 見た目 -----------------------------------------------------------
    def _style(self):
        st = ttk.Style(self)
        try:
            st.theme_use("vista")
        except Exception:
            pass
        st.configure(".", font=self.font)
        st.configure("Treeview", rowheight=26, font=self.font)
        st.configure("Treeview.Heading", font=(self.font[0], 10, "bold"))
        st.configure("Head.TLabel", font=(self.font[0], 10, "bold"))
        st.configure("Hint.TLabel", foreground="#555555")

    def _desktop(self):
        for p in (os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "デスクトップ"),
                  os.path.join(os.environ.get("USERPROFILE", ""), "Desktop"),
                  os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Desktop")):
            if os.path.isdir(p):
                return p
        return os.path.expanduser("~")

    def _build(self):
        # 上部：場所
        top = ttk.Frame(self, padding=(10, 8, 10, 4))
        top.pack(fill="x")
        ttk.Label(top, text="場所：", style="Head.TLabel").pack(side="left")
        self.path_var = tk.StringVar()
        e = ttk.Entry(top, textvariable=self.path_var, font=self.font)
        e.pack(side="left", fill="x", expand=True, padx=(0, 6))
        e.bind("<Return>", lambda ev: self.reload())
        ttk.Button(top, text="参照…", command=self.browse, width=7).pack(side="left")
        ttk.Button(top, text="上へ", command=self.go_up, width=6).pack(side="left", padx=4)
        ttk.Button(top, text="デスクトップ", command=self.go_desktop,
                   width=12).pack(side="left")
        ttk.Button(top, text="再読み込み", command=self.reload,
                   width=11).pack(side="left", padx=4)

        # 一覧
        mid = ttk.Frame(self, padding=(10, 4, 10, 4))
        mid.pack(fill="both", expand=True)
        cols = ("sel", "name", "kind", "prot", "icon", "mtime", "size")
        self.tree = ttk.Treeview(mid, columns=cols, show="tree headings",
                                 selectmode="extended")
        heads = {"sel": "選択", "name": "名前", "kind": "種類", "prot": "削除保護",
                 "icon": "アイコン", "mtime": "更新日時", "size": "サイズ"}
        widths = {"sel": 46, "name": 400, "kind": 90, "prot": 90,
                  "icon": 150, "mtime": 130, "size": 90}
        anchors = {"sel": "center", "prot": "center", "size": "e"}
        self.tree.column("#0", width=34, minwidth=34, stretch=False, anchor="center")
        self.tree.heading("#0", text="")
        for c in cols:
            self.tree.heading(c, text=heads[c],
                              command=lambda cc=c: self.sort_by(cc))
            self.tree.column(c, width=widths[c], anchor=anchors.get(c, "w"),
                             stretch=(c == "name"))
        vsb = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.tree.tag_configure("prot", background="#eef6ff")
        self.tree.tag_configure("strong", background="#e2f0e2")
        self.tree.bind("<Button-1>", self.on_click)
        self.tree.bind("<Double-1>", self.on_double)
        self.tree.bind("<space>", self.on_space)

        # 操作
        ops = ttk.Frame(self, padding=(10, 2, 10, 2))
        ops.pack(fill="x")
        row1 = ttk.Frame(ops)
        row1.pack(fill="x")
        row2 = ttk.Frame(ops)
        row2.pack(fill="x", pady=(6, 0))

        g0 = ttk.LabelFrame(row1, text=" 選択 ", padding=6)
        g0.pack(side="left", fill="y")
        ttk.Button(g0, text="すべて選択", command=lambda: self.check_all(True),
                   width=11).grid(row=0, column=0, padx=2)
        ttk.Button(g0, text="選択を解除", command=lambda: self.check_all(False),
                   width=11).grid(row=0, column=1, padx=2)
        ttk.Button(g0, text="保護中だけ選択", command=self.check_protected,
                   width=14).grid(row=0, column=2, padx=2)

        g1 = ttk.LabelFrame(row1, text=" 削除保護 ", padding=6)
        g1.pack(side="left", fill="y", padx=8)
        ttk.Button(g1, text="標準で保護", width=12,
                   command=lambda: self.do_protect("standard")).grid(row=0, column=0, padx=2)
        ttk.Button(g1, text="強力に保護", width=12,
                   command=lambda: self.do_protect("strong")).grid(row=0, column=1, padx=2)
        ttk.Button(g1, text="保護を解除", width=12,
                   command=self.do_unprotect).grid(row=0, column=2, padx=2)

        g2 = ttk.LabelFrame(row2, text=" アイコン ", padding=6)
        g2.pack(side="left", fill="y")
        ttk.Button(g2, text="アイコンを変更…", width=16,
                   command=self.do_icon).grid(row=0, column=0, padx=2)
        ttk.Button(g2, text="既定に戻す", width=12,
                   command=self.do_icon_clear).grid(row=0, column=1, padx=2)
        ttk.Button(g2, text="表示を更新", width=12,
                   command=self.do_icon_refresh).grid(row=0, column=2, padx=2)

        g3 = ttk.LabelFrame(row2, text=" その他 ", padding=6)
        g3.pack(side="left", fill="y", padx=8)
        ttk.Button(g3, text="保護中の一覧…", width=14,
                   command=self.show_list).grid(row=0, column=0, padx=2)
        ttk.Button(g3, text="使い方", width=8,
                   command=self.show_help).grid(row=0, column=1, padx=2)

        hint = ttk.Frame(self, padding=(12, 4, 12, 2))
        hint.pack(fill="x")
        self.hint_label = ttk.Label(
            hint, style="Hint.TLabel", font=(self.font[0], 9), justify="left",
            wraplength=1100,
            text=("標準保護 … 対象そのものを「ごみ箱へ削除」「名前の変更」「ドラッグで移動」"
                  "できなくします。中身は今までどおり編集・追加・削除できます（ふだん使う"
                  "フォルダはこちら）。\n"
                  "強力保護 … 中身のファイルまで削除できなくします。ただしその中の "
                  "Word / Excel は上書き保存ができなくなるので、完成済みの保管用フォルダ向けです。"))
        self.hint_label.pack(anchor="w", fill="x")
        hint.bind("<Configure>",
                  lambda e: self.hint_label.configure(wraplength=max(400, e.width - 20)))

        # ログ
        low = ttk.Frame(self, padding=(10, 0, 10, 8))
        low.pack(fill="x")
        self.log = tk.Text(low, height=4, font=("Consolas", 9), bg="#f7f7f7",
                           relief="solid", bd=1, wrap="none")
        self.log.pack(fill="x")
        self.log.configure(state="disabled")

        self.status = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.status, anchor="w", relief="sunken",
                  padding=(8, 3)).pack(fill="x", side="bottom")

    # -- ログ -------------------------------------------------------------
    def say(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", "[%s] %s\n" % (datetime.now().strftime("%H:%M:%S"), msg))
        self.log.see("end")
        self.log.configure(state="disabled")
        self.status.set(msg)
        self.update_idletasks()

    # -- 一覧 -------------------------------------------------------------
    def cur_dir(self):
        return self.path_var.get().strip('"').rstrip("\\/") or self._desktop()

    def browse(self):
        p = filedialog.askdirectory(title="場所を選ぶ", initialdir=self.cur_dir())
        if p:
            self.path_var.set(os.path.normpath(p))
            self.reload()

    def go_up(self):
        p = os.path.dirname(self.cur_dir())
        if p and os.path.isdir(p):
            self.path_var.set(p)
            self.reload()

    def go_desktop(self):
        self.path_var.set(self._desktop())
        self.reload()

    def _photo(self, path, isdir):
        # このアプリで設定したアイコンは台帳から直接読む
        # （SHGetFileInfo はフォルダのカスタムアイコンを返さないため）
        ent = self.store.icons.get(norm(path))
        key = ("ref:" + ent["ref"]) if ent else (
            norm(path) if isdir else os.path.splitext(path)[1].lower() or "?file")
        if key in self.img_cache:
            return self.img_cache[key]
        photo = None
        if PIL_OK:
            img = None
            if ent:
                src, _, idx = ent["ref"].rpartition(",")
                try:
                    img = extract_dll_icon(os.path.expandvars(src), int(idx or 0), 16)
                except Exception:
                    img = None
            if img is None:
                img = shell_icon(path, 16)
            if img is not None:
                try:
                    photo = ImageTk.PhotoImage(img)
                except Exception:
                    photo = None
        self.img_cache[key] = photo
        return photo

    def reload(self):
        d = self.cur_dir()
        if not os.path.isdir(d):
            messagebox.showwarning(APP_NAME, "フォルダが見つかりません：\n%s" % d)
            return
        self.store.data["last_dir"] = d
        self.store.save()
        self.tree.delete(*self.tree.get_children())
        self.rows.clear()
        self.checked.clear()
        if PIL_OK:
            self.img_cache.clear()

        try:
            entries = list(os.scandir(d))
        except Exception as e:
            messagebox.showerror(APP_NAME, "読み取れません：\n%s" % e)
            return

        items = []
        for en in entries:
            name = en.name
            if name.lower() in ("desktop.ini", "thumbs.db"):
                continue
            try:
                isdir = en.is_dir()
                st = en.stat()
            except Exception:
                continue
            items.append({
                "path": en.path, "name": name, "isdir": isdir,
                "mtime": st.st_mtime,
                "size": None if isdir else st.st_size,
            })
        items.sort(key=lambda x: (not x["isdir"], x["name"].lower()))

        # 実際のアクセス権を一度に読み取り、台帳と食い違っていれば台帳を直す
        actual = scan_protection(d, [it["path"] for it in items])
        for it in items:
            key = norm(it["path"])
            lvl = actual.get(key)
            if lvl and self.store.protected.get(key, {}).get("level") != lvl:
                self.store.protect(it["path"], lvl)
            elif not lvl and key in self.store.protected:
                self.store.unprotect(it["path"])
            it["level"] = lvl

        n_prot = 0
        for it in items:
            lvl = it["level"]
            if lvl:
                n_prot += 1
            iid = self.tree.insert(
                "", "end",
                image=self._photo(it["path"], it["isdir"]) or "",
                values=(CHECK_OFF, it["name"],
                        "フォルダ" if it["isdir"] else (os.path.splitext(it["name"])[1] or "ファイル"),
                        LEVEL_LABEL.get(lvl, ""),
                        self.store.icon_label(it["path"]),
                        fmt_time(it["mtime"]), human_size(it["size"])),
                tags=(("strong",) if lvl == "strong" else ("prot",)) if lvl else ())
            self.rows[iid] = it
        self.store.save()
        self.say("%s ： %d 件（保護中 %d 件）" % (d, len(items), n_prot))

    def sort_by(self, col):
        if self.sort_key == col:
            self.sort_desc = not self.sort_desc
        else:
            self.sort_key, self.sort_desc = col, False
        data = []
        for iid in self.tree.get_children():
            it = self.rows[iid]
            if col == "size":
                k = (-1 if it["isdir"] else it["size"] or 0)
            elif col == "mtime":
                k = it["mtime"]
            else:
                k = str(self.tree.set(iid, col)).lower()
            data.append((k, iid))
        try:
            data.sort(key=lambda x: x[0], reverse=self.sort_desc)
        except TypeError:
            data.sort(key=lambda x: str(x[0]), reverse=self.sort_desc)
        for pos, (_, iid) in enumerate(data):
            self.tree.move(iid, "", pos)

    # -- チェック ---------------------------------------------------------
    def set_check(self, iid, on):
        self.tree.set(iid, "sel", CHECK_ON if on else CHECK_OFF)
        if on:
            self.checked.add(iid)
        else:
            self.checked.discard(iid)

    def toggle(self, iid):
        self.set_check(iid, iid not in self.checked)

    def check_all(self, on):
        for iid in self.tree.get_children():
            self.set_check(iid, on)
        self.status.set("%d 件を選択中" % len(self.checked))

    def check_protected(self):
        for iid in self.tree.get_children():
            self.set_check(iid, bool(self.rows[iid].get("level")))
        self.status.set("%d 件を選択中" % len(self.checked))

    def on_click(self, ev):
        iid = self.tree.identify_row(ev.y)
        col = self.tree.identify_column(ev.x)
        if iid and col in ("#0", "#1"):
            self.toggle(iid)
            return "break"

    def on_space(self, ev):
        for iid in self.tree.selection():
            self.toggle(iid)
        return "break"

    def on_double(self, ev):
        iid = self.tree.identify_row(ev.y)
        col = self.tree.identify_column(ev.x)
        if not iid or col in ("#0", "#1"):
            return
        it = self.rows[iid]
        if it["isdir"]:
            self.path_var.set(it["path"])
            self.reload()

    def targets(self):
        if self.checked:
            return [self.rows[i] for i in self.checked if i in self.rows]
        return [self.rows[i] for i in self.tree.selection() if i in self.rows]

    # -- 保護 -------------------------------------------------------------
    def do_protect(self, level):
        tg = self.targets()
        if not tg:
            messagebox.showinfo(APP_NAME, "先に対象を選んでください（□をクリック）。")
            return
        names = "\n".join("・" + t["name"] for t in tg[:12])
        if len(tg) > 12:
            names += "\n…ほか %d 件" % (len(tg) - 12)
        extra = ("\n\n※強力保護は中身のファイルも削除できなくなります。"
                 "そのフォルダ内の Word / Excel を編集して上書き保存しようとすると"
                 "エラーになります（動作確認済み）。編集し続けるファイルが入っている場合は"
                 "「標準で保護」を選んでください。") if level == "strong" else ""
        if not messagebox.askyesno(
                APP_NAME,
                "次の %d 件を【%s保護】します。よろしいですか？\n\n%s%s"
                % (len(tg), LEVEL_LABEL[level], names, extra)):
            return

        self.say("保護を開始します（%s）…" % LEVEL_LABEL[level])
        for t in tg:
            self.store.protect(t["path"], level)
        errors = self.store.reconcile(extra=[t["path"] for t in tg])

        weak = []
        for t in tg:
            if not parent_blocks_delete_child(os.path.dirname(t["path"])):
                weak.append(t["name"])
        for path, msg in errors:
            self.say("！権限を変更できませんでした： %s  %s" % (path, msg))
        self.say("%d 件を%s保護しました。" % (len(tg), LEVEL_LABEL[level]))
        if weak:
            messagebox.showwarning(
                APP_NAME,
                "次の項目は親フォルダ側の設定を変更できなかったため、\n"
                "保護が効かない可能性があります：\n\n" + "\n".join("・" + w for w in weak[:10]))
        self.reload()

    def do_unprotect(self):
        tg = [t for t in self.targets() if t.get("level")]
        if not tg:
            messagebox.showinfo(APP_NAME, "保護中の項目が選ばれていません。")
            return
        if not messagebox.askyesno(
                APP_NAME, "次の %d 件の保護を解除します。\n解除後は普通に削除できるようになります。\n\n%s"
                % (len(tg), "\n".join("・" + t["name"] for t in tg[:12]))):
            return
        for t in tg:
            self.store.unprotect(t["path"])
            set_deny(t["path"], None)
        self.store.reconcile(extra=[t["path"] for t in tg])
        self.say("%d 件の保護を解除しました。" % len(tg))
        self.reload()

    # -- アイコン ---------------------------------------------------------
    def do_icon(self):
        if not PIL_OK:
            messagebox.showerror(APP_NAME, "画像ライブラリ(Pillow)が見つからないため"
                                           "アイコン機能は使えません。")
            return
        tg = self.targets()
        if not tg:
            messagebox.showinfo(APP_NAME, "先に対象を選んでください（□をクリック）。")
            return
        ok = [t for t in tg if t["isdir"] or t["name"].lower().endswith(".lnk")]
        if not ok:
            messagebox.showinfo(
                APP_NAME,
                "アイコンを変えられるのはフォルダとショートカット(.lnk)だけです。\n"
                "通常のファイルのアイコンは拡張子ごとに Windows が決めているため、\n"
                "1 つだけ変えることはできません。")
            return
        dlg = IconPicker(self, self.font)
        self.wait_window(dlg)
        if not dlg.result:
            return
        ref, label = dlg.result
        done = 0
        for t in ok:
            try:
                if t["isdir"]:
                    set_folder_icon(t["path"], ref)
                else:
                    set_shortcut_icon(t["path"], ref)
                self.store.set_icon(t["path"], ref, label)
                done += 1
            except Exception as e:
                self.say("！アイコン変更に失敗： %s  %s" % (t["name"], e))
        self.store.save()
        skipped = len(tg) - len(ok)
        self.say("%d 件のアイコンを「%s」に変更しました。%s"
                 % (done, label, ("（%d 件はファイルのため対象外）" % skipped) if skipped else ""))
        self.reload()

    def do_icon_clear(self):
        tg = [t for t in self.targets() if t["isdir"] or t["name"].lower().endswith(".lnk")]
        if not tg:
            messagebox.showinfo(APP_NAME, "フォルダまたはショートカットを選んでください。")
            return
        for t in tg:
            try:
                if t["isdir"]:
                    clear_folder_icon(t["path"])
                else:
                    set_shortcut_icon(t["path"], "")
                self.store.clear_icon(t["path"])
            except Exception as e:
                self.say("！戻せませんでした： %s  %s" % (t["name"], e))
        self.store.save()
        self.say("%d 件のアイコンを既定に戻しました。" % len(tg))
        self.reload()

    def do_icon_refresh(self):
        """アイコンがすぐ切り替わらないときにエクスプローラーの表示を更新する"""
        self.say("アイコン表示を更新しています…")
        run_hidden(["ie4uinit.exe", "-show"])
        n = 0
        for e in list(self.store.icons.values()):
            p = e.get("path")
            if p and os.path.exists(p):
                refresh_explorer(os.path.dirname(p), item=p)
                n += 1
        refresh_explorer(self.cur_dir())
        self.say("%d 件に更新を通知しました。" % n)
        self.reload()
        if not messagebox.askyesno(
                APP_NAME,
                "デスクトップやフォルダ窓で F5 を押して確認してください。\n\n"
                "それでも古いアイコンのままの場合は、Windows の"
                "アイコンキャッシュを作り直す必要があります。\n"
                "実行するとエクスプローラー（デスクトップと開いているフォルダ窓）が"
                "いったん閉じて自動的に開き直ります。\n"
                "作業中の Word / Excel などのアプリには影響しません。\n\n"
                "アイコンキャッシュを作り直しますか？"):
            return
        self.say("アイコンキャッシュを作り直しています…")
        self.update_idletasks()
        removed, err = rebuild_icon_cache()
        if err:
            self.say("！ %s" % err)
            messagebox.showwarning(APP_NAME, "うまくいきませんでした：\n%s" % err)
        else:
            self.say("キャッシュ %d 個を削除し、エクスプローラーを開き直しました。" % removed)
            messagebox.showinfo(
                APP_NAME,
                "アイコンキャッシュを作り直しました（%d 個）。\n"
                "デスクトップのアイコンが並び直るまで数秒かかることがあります。" % removed)

    # -- 保護一覧 ---------------------------------------------------------
    def show_list(self):
        win = tk.Toplevel(self)
        win.title("保護中の一覧")
        win.geometry("820x460")
        win.transient(self)
        wrap = ttk.Frame(win, padding=8)
        wrap.pack(side="top", fill="both", expand=True)
        cols = ("level", "path", "at")
        tv = ttk.Treeview(wrap, columns=cols, show="headings")
        for c, h, w in (("level", "保護", 70), ("path", "場所", 600), ("at", "設定日時", 140)):
            tv.heading(c, text=h)
            tv.column(c, width=w, anchor="center" if c == "level" else "w")
        sb = ttk.Scrollbar(wrap, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        tv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def fill():
            tv.delete(*tv.get_children())
            for k, e in sorted(self.store.protected.items(), key=lambda x: x[1]["path"]):
                mark = "" if os.path.exists(e["path"]) else "（見つかりません）"
                tv.insert("", "end", values=(LEVEL_LABEL.get(e["level"], e["level"]),
                                             e["path"] + mark, e.get("at", "")))
        fill()

        bar = ttk.Frame(win, padding=8)
        bar.pack(fill="x")

        def jump():
            sel = tv.selection()
            if not sel:
                return
            p = tv.set(sel[0], "path").replace("（見つかりません）", "")
            d = p if os.path.isdir(p) else os.path.dirname(p)
            if os.path.isdir(d):
                self.path_var.set(os.path.dirname(p) if os.path.isdir(p) else d)
                self.reload()
                win.destroy()

        def release_sel():
            sel = tv.selection()
            if not sel:
                return
            paths = [tv.set(s, "path").replace("（見つかりません）", "") for s in sel]
            if not messagebox.askyesno(APP_NAME, "選んだ %d 件の保護を解除します。" % len(paths),
                                       parent=win):
                return
            for p in paths:
                self.store.unprotect(p)
                if os.path.exists(p):
                    set_deny(p, None)
            self.store.reconcile()
            fill()
            self.reload()

        def release_all():
            if not self.store.protected:
                return
            if not messagebox.askyesno(
                    APP_NAME, "すべての保護（%d 件）を解除します。よろしいですか？"
                    % len(self.store.protected), parent=win):
                return
            for k, e in list(self.store.protected.items()):
                if os.path.exists(e["path"]):
                    set_deny(e["path"], None)
            self.store.data["protected"] = {}
            self.store.reconcile()
            fill()
            self.reload()
            self.say("すべての保護を解除しました。")

        ttk.Button(bar, text="この場所を開く", command=jump).pack(side="left")
        ttk.Button(bar, text="選んだものを解除", command=release_sel).pack(side="left", padx=6)
        ttk.Button(bar, text="すべて解除", command=release_all).pack(side="left")
        ttk.Button(bar, text="閉じる", command=win.destroy).pack(side="right")

    def show_help(self):
        p = os.path.join(APP_DIR, "使い方.md")
        if os.path.exists(p):
            try:
                os.startfile(p)
                return
            except Exception:
                pass
        messagebox.showinfo(APP_NAME, "使い方.md が見つかりません。")


def main():
    try:
        app = App()
        app.mainloop()
    except Exception:
        try:
            with open(os.path.join(APP_DIR, "エラー.log"), "a", encoding="utf-8") as f:
                f.write(datetime.now().isoformat() + "\n")
                f.write(traceback.format_exc() + "\n")
        except Exception:
            pass
        raise


if __name__ == "__main__":
    main()
