# -*- coding: utf-8 -*-
"""
ファイル整理ツール
  ① 重複ファイル検出 : 内容(SHA-256)が完全一致するファイルをグループ表示
  ② 条件でファイル抽出 : 名前・拡張子・更新日・サイズで一次ファイル等を抽出
  → 一覧にチェックを付けて「退避フォルダへ移動」「ごみ箱へ」「CSV出力」

  ・削除は必ず「ごみ箱」経由（完全削除はしない）
  ・移動は操作ログに記録し、ワンクリックで元に戻せる
  ・OneDrive の「クラウドのみ」ファイルは既定で中身を読まない（勝手にDLしない）
"""

import os
import sys
import csv
import json
import stat
import shutil
import hashlib
import tempfile
import threading
import queue
import subprocess
import traceback
from datetime import datetime

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_NAME = "ファイル整理ツール"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(APP_DIR, "操作ログ.json")
CONFIG_PATH = os.path.join(APP_DIR, "設定.json")

QUARANTINE_NAME = "_重複レビュー"
CONSOLIDATED_NAME = "_統合済み元資料"

# 走査から除外するフォルダ名
SKIP_DIRS_ALWAYS = {
    ".git", "node_modules", "__pycache__", ".claude", ".vs", ".idea",
    "$RECYCLE.BIN", "System Volume Information", "AppData",
}
SKIP_DIRS_OPTIONAL = {QUARANTINE_NAME, CONSOLIDATED_NAME, "_統合済み元資料", "_旧版"}

# 走査から除外するファイル
SKIP_FILE_PREFIX = ("~$",)
SKIP_FILE_NAMES = {"thumbs.db", "desktop.ini", ".ds_store"}

# 「残さない側」と判定されやすいキーワード
COPY_HINTS = ("コピー", "- copy", "copy", "(1)", "(2)", "(3)", "_旧", "旧版",
              "backup", "バックアップ", "写し", "_old", " - コピー")

FILE_ATTRIBUTE_OFFLINE = 0x00001000
FILE_ATTRIBUTE_RECALL_ON_OPEN = 0x00040000
FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x00400000
CLOUD_MASK = (FILE_ATTRIBUTE_OFFLINE
              | FILE_ATTRIBUTE_RECALL_ON_OPEN
              | FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS)

CHECK_ON = "■"
CHECK_OFF = "□"


# --------------------------------------------------------------------------
# 汎用ユーティリティ
# --------------------------------------------------------------------------
def human_size(n):
    if n is None:
        return ""
    units = ["B", "KB", "MB", "GB", "TB"]
    f = float(n)
    for u in units:
        if f < 1024 or u == "TB":
            return ("%.0f %s" % (f, u)) if u == "B" else ("%.1f %s" % (f, u))
        f /= 1024
    return "%.1f TB" % f


def fmt_time(ts):
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ""


def is_cloud_only(st):
    """OneDrive の『オンラインのみ』ファイルか（中身を読むとDLが走る）"""
    attrs = getattr(st, "st_file_attributes", 0)
    return bool(attrs & CLOUD_MASK)


def unique_path(dest):
    """同名ファイルがあれば _1, _2 ... を付けて衝突を避ける"""
    if not os.path.exists(dest):
        return dest
    base, ext = os.path.splitext(dest)
    i = 1
    while True:
        cand = "%s_%d%s" % (base, i, ext)
        if not os.path.exists(cand):
            return cand
        i += 1


class FileRec(object):
    __slots__ = ("path", "size", "mtime", "cloud", "digest")

    def __init__(self, path, size, mtime, cloud):
        self.path = path
        self.size = size
        self.mtime = mtime
        self.cloud = cloud
        self.digest = None

    @property
    def name(self):
        return os.path.basename(self.path)

    @property
    def folder(self):
        return os.path.dirname(self.path)


# --------------------------------------------------------------------------
# 走査 / ハッシュ
# --------------------------------------------------------------------------
def iter_files(roots, recursive=True, skip_optional=True, report=None, cancel=None):
    seen = set()
    skip_dirs = set(SKIP_DIRS_ALWAYS)
    if skip_optional:
        skip_dirs |= SKIP_DIRS_OPTIONAL
    count = 0
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            if cancel is not None and cancel.is_set():
                return
            dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith("$")]
            if not recursive:
                dirnames[:] = []
            for fn in filenames:
                low = fn.lower()
                if low in SKIP_FILE_NAMES or fn.startswith(SKIP_FILE_PREFIX):
                    continue
                full = os.path.join(dirpath, fn)
                key = os.path.normcase(os.path.abspath(full))
                if key in seen:
                    continue
                seen.add(key)
                try:
                    st = os.stat(full, follow_symlinks=False)
                except OSError:
                    continue
                if stat.S_ISDIR(st.st_mode):
                    continue
                count += 1
                if report is not None and count % 200 == 0:
                    report("ファイルを列挙中… %d 件" % count)
                yield FileRec(full, st.st_size, st.st_mtime, is_cloud_only(st))


def hash_file(path, size, partial=False, chunk=1024 * 1024):
    h = hashlib.sha256()
    limit = 65536 if partial else None
    read = 0
    with open(path, "rb") as f:
        while True:
            n = chunk if limit is None else min(chunk, limit - read)
            if n <= 0:
                break
            b = f.read(n)
            if not b:
                break
            h.update(b)
            read += len(b)
    return h.hexdigest()


def find_duplicates(roots, opts, report, cancel):
    """戻り値: [ (代表サイズ, 状態, [FileRec, ...]), ... ]"""
    min_size = opts.get("min_size", 1)
    files = []
    for rec in iter_files(roots, opts.get("recursive", True),
                          opts.get("skip_optional", True), report, cancel):
        if rec.size < min_size:
            continue
        files.append(rec)
    if cancel.is_set():
        return []

    report("サイズで絞り込み中… 対象 %d 件" % len(files))
    by_size = {}
    for rec in files:
        by_size.setdefault(rec.size, []).append(rec)
    cand = [v for v in by_size.values() if len(v) > 1]

    groups = []
    # クラウドのみのファイルは中身を読まない（DL回避）→ サイズ一致のみで参考表示
    hydrate = opts.get("hydrate_cloud", False)
    total = sum(len(v) for v in cand)
    done = 0

    for bucket in cand:
        if cancel.is_set():
            return groups
        local = [r for r in bucket if hydrate or not r.cloud]
        cloud = [r for r in bucket if not (hydrate or not r.cloud)]

        # 段階1: 先頭64KBのハッシュ
        pre = {}
        for rec in local:
            if cancel.is_set():
                return groups
            done += 1
            if done % 25 == 0:
                report("内容を照合中… %d / %d" % (done, total), done / max(total, 1))
            try:
                key = hash_file(rec.path, rec.size, partial=True)
            except OSError:
                continue
            pre.setdefault(key, []).append(rec)

        # 段階2: 全体ハッシュ
        for sub in pre.values():
            if len(sub) < 2:
                continue
            full = {}
            for rec in sub:
                if cancel.is_set():
                    return groups
                try:
                    rec.digest = hash_file(rec.path, rec.size)
                except OSError:
                    continue
                full.setdefault(rec.digest, []).append(rec)
            for members in full.values():
                if len(members) > 1:
                    groups.append((members[0].size, "完全一致", members))

        if len(cloud) > 1:
            done += len(cloud)
            groups.append((cloud[0].size, "サイズ一致(クラウド未照合)", cloud))

    groups.sort(key=lambda g: g[0] * (len(g[2]) - 1), reverse=True)
    return groups


def filter_files(roots, opts, report, cancel):
    kws = [k.strip().lower() for k in opts.get("keywords", "").split(",") if k.strip()]
    exts = [e.strip().lower() for e in opts.get("exts", "").split(",") if e.strip()]
    exts = [e if e.startswith(".") else "." + e for e in exts]
    older_ts = opts.get("older_than_ts")
    newer_ts = opts.get("newer_than_ts")
    min_size = opts.get("min_size", 0)
    match_all = opts.get("match_all", False)

    out = []
    for rec in iter_files(roots, opts.get("recursive", True),
                          opts.get("skip_optional", False), report, cancel):
        if cancel.is_set():
            return out
        name = rec.name.lower()
        if kws:
            hit = [k in name for k in kws]
            if (all(hit) if match_all else any(hit)) is False:
                continue
        if exts and os.path.splitext(name)[1] not in exts:
            continue
        if older_ts is not None and rec.mtime > older_ts:
            continue
        if newer_ts is not None and rec.mtime < newer_ts:
            continue
        if rec.size < min_size:
            continue
        out.append(rec)
        if len(out) % 200 == 0:
            report("抽出中… %d 件" % len(out))
    out.sort(key=lambda r: (-r.size, r.path))
    return out


# --------------------------------------------------------------------------
# 実操作（移動 / ごみ箱 / 元に戻す）
# --------------------------------------------------------------------------
def append_log(entries):
    if not entries:
        return
    batch = {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "items": entries}
    data = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
    data.append(batch)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data[-50:], f, ensure_ascii=False, indent=1)


def move_files(recs, dest_root, keep_tree, base_hint):
    """移動を実行。戻り値 (成功件数, 失敗リスト, ログ項目)"""
    ok, ng, log = 0, [], []
    os.makedirs(dest_root, exist_ok=True)
    for rec in recs:
        try:
            if keep_tree:
                try:
                    rel = os.path.relpath(rec.folder, base_hint)
                except ValueError:
                    rel = ""
                if rel.startswith(".."):
                    rel = os.path.splitdrive(rec.folder)[1].lstrip("\\/")
                sub = os.path.join(dest_root, rel)
            else:
                sub = dest_root
            os.makedirs(sub, exist_ok=True)          # 直前にフォルダ存在を保証
            dest = unique_path(os.path.join(sub, rec.name))
            shutil.move(rec.path, dest)
            if not os.path.exists(dest):
                raise OSError("移動先にファイルが見つかりません")
            ok += 1
            log.append({"op": "move", "src": rec.path, "dst": dest})
        except Exception as e:
            ng.append((rec.path, str(e)))
    append_log(log)
    return ok, ng, log


def send_to_recycle(paths):
    """PowerShell 経由でごみ箱へ（完全削除はしない）"""
    if not paths:
        return 0, []
    fd, listfile = tempfile.mkstemp(suffix=".txt", prefix="fileorg_")
    os.close(fd)
    with open(listfile, "w", encoding="utf-8-sig") as f:
        f.write("\n".join(paths))
    ps = r'''
Add-Type -AssemblyName Microsoft.VisualBasic
$list = Get-Content -LiteralPath "%s" -Encoding UTF8
foreach ($p in $list) {
  if ([string]::IsNullOrWhiteSpace($p)) { continue }
  if (Test-Path -LiteralPath $p) {
    try {
      [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($p, 'OnlyErrorDialogs', 'SendToRecycleBin')
    } catch { }
  }
}
''' % listfile
    fd, psfile = tempfile.mkstemp(suffix=".ps1", prefix="fileorg_")
    os.close(fd)
    with open(psfile, "w", encoding="utf-8-sig") as f:
        f.write(ps)
    flags = 0x08000000 if os.name == "nt" else 0  # CREATE_NO_WINDOW
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                    "-File", psfile], creationflags=flags,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for p in (listfile, psfile):
        try:
            os.remove(p)
        except OSError:
            pass
    ng = [p for p in paths if os.path.exists(p)]
    ok = len(paths) - len(ng)
    append_log([{"op": "recycle", "src": p, "dst": "(ごみ箱)"} for p in paths if p not in ng])
    return ok, ng


def undo_last_move():
    if not os.path.exists(LOG_PATH):
        return 0, 0, "操作ログがありません。"
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    for i in range(len(data) - 1, -1, -1):
        items = [it for it in data[i]["items"] if it["op"] == "move"]
        if items:
            ok = ng = 0
            for it in items:
                try:
                    if os.path.exists(it["dst"]):
                        os.makedirs(os.path.dirname(it["src"]), exist_ok=True)
                        shutil.move(it["dst"], unique_path(it["src"]))
                        ok += 1
                    else:
                        ng += 1
                except Exception:
                    ng += 1
            data.pop(i)
            with open(LOG_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
            return ok, ng, data[i - 1]["time"] if i > 0 else ""
    return 0, 0, "元に戻せる移動操作がありません（ごみ箱への削除はごみ箱から復元してください）。"


# --------------------------------------------------------------------------
# GUI
# --------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1180x760")
        self.minsize(960, 620)

        self.q = queue.Queue()
        self.cancel = threading.Event()
        self.worker = None
        self.records = {}     # iid -> FileRec
        self.checked = set()  # iid
        self.groups = []
        self.mode = "dup"

        self._build_style()
        self._build_widgets()
        self._load_config()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(120, self._poll)

    # -------------------------------------------------- 見た目
    def _build_style(self):
        s = ttk.Style(self)
        try:
            s.theme_use("vista")
        except tk.TclError:
            pass
        base = ("Meiryo UI", 10)
        self.option_add("*Font", base)
        s.configure("Treeview", rowheight=24, font=base)
        s.configure("Treeview.Heading", font=("Meiryo UI", 10, "bold"))
        s.configure("Head.TLabel", font=("Meiryo UI", 12, "bold"))
        s.configure("Warn.TLabel", foreground="#b00020")
        s.configure("Act.TButton", font=("Meiryo UI", 10, "bold"))

    def _build_widgets(self):
        # ===== 対象フォルダ =====
        top = ttk.LabelFrame(self, text=" 1. 対象フォルダ ")
        top.pack(fill="x", padx=10, pady=(10, 4))

        self.folder_list = tk.Listbox(top, height=3, selectmode="extended")
        self.folder_list.pack(side="left", fill="both", expand=True, padx=(8, 4), pady=8)
        bb = ttk.Frame(top)
        bb.pack(side="left", padx=(0, 8), pady=8)
        ttk.Button(bb, text="フォルダを追加", command=self.add_folder).pack(fill="x")
        ttk.Button(bb, text="選択を削除", command=self.del_folder).pack(fill="x", pady=3)
        ttk.Button(bb, text="デスクトップ", command=self.add_desktop).pack(fill="x")

        opt = ttk.Frame(top)
        opt.pack(side="left", padx=(0, 10), pady=8)
        self.var_recursive = tk.BooleanVar(value=True)
        self.var_skipopt = tk.BooleanVar(value=True)
        self.var_hydrate = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt, text="サブフォルダも含める", variable=self.var_recursive).pack(anchor="w")
        ttk.Checkbutton(opt, text="_重複レビュー / _統合済み元資料 を除外",
                        variable=self.var_skipopt).pack(anchor="w")
        ttk.Checkbutton(opt, text="クラウドのみのファイルもDLして照合",
                        variable=self.var_hydrate).pack(anchor="w")

        # ===== 条件 =====
        nb = ttk.Notebook(self)
        nb.pack(fill="x", padx=10, pady=4)
        self.nb = nb
        nb.bind("<<NotebookTabChanged>>", self._on_tab)

        # --- 重複タブ
        t1 = ttk.Frame(nb)
        nb.add(t1, text="  ① 重複ファイルを探す  ")
        r = ttk.Frame(t1)
        r.pack(fill="x", padx=10, pady=10)
        ttk.Label(r, text="内容が完全に一致するファイルを検出します（ファイル名は違っていてもOK）。",
                  style="Head.TLabel").pack(anchor="w")
        r2 = ttk.Frame(t1)
        r2.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Label(r2, text="この容量未満は無視:").pack(side="left")
        self.var_minkb = tk.StringVar(value="1")
        ttk.Entry(r2, textvariable=self.var_minkb, width=8).pack(side="left", padx=4)
        ttk.Label(r2, text="KB").pack(side="left")
        ttk.Button(r2, text="重複を検索", style="Act.TButton",
                   command=self.run_dup).pack(side="left", padx=16)

        # --- 抽出タブ
        t2 = ttk.Frame(nb)
        nb.add(t2, text="  ② 条件でファイルを抽出  ")
        g = ttk.Frame(t2)
        g.pack(fill="x", padx=10, pady=8)
        ttk.Label(g, text="ファイル名に含む語（, 区切り）:").grid(row=0, column=0, sticky="w", pady=3)
        self.var_kw = tk.StringVar()
        ttk.Entry(g, textvariable=self.var_kw, width=42).grid(row=0, column=1, sticky="w", padx=6)
        self.var_matchall = tk.BooleanVar(value=False)
        ttk.Checkbutton(g, text="すべて含む（AND）", variable=self.var_matchall).grid(row=0, column=2, sticky="w")

        ttk.Label(g, text="拡張子（, 区切り / 空欄=全部）:").grid(row=1, column=0, sticky="w", pady=3)
        self.var_ext = tk.StringVar()
        ttk.Entry(g, textvariable=self.var_ext, width=42).grid(row=1, column=1, sticky="w", padx=6)

        ttk.Label(g, text="更新日がこの日より前:").grid(row=2, column=0, sticky="w", pady=3)
        self.var_older = tk.StringVar()
        ttk.Entry(g, textvariable=self.var_older, width=18).grid(row=2, column=1, sticky="w", padx=6)
        ttk.Label(g, text="例) 2026-01-31（空欄=条件なし）").grid(row=2, column=2, sticky="w")

        ttk.Label(g, text="この容量以上:").grid(row=3, column=0, sticky="w", pady=3)
        self.var_minmb = tk.StringVar(value="0")
        ttk.Entry(g, textvariable=self.var_minmb, width=18).grid(row=3, column=1, sticky="w", padx=6)
        ttk.Label(g, text="MB").grid(row=3, column=2, sticky="w")

        p = ttk.Frame(t2)
        p.pack(fill="x", padx=10, pady=(0, 8))
        ttk.Label(p, text="よく使う条件:").pack(side="left")
        ttk.Button(p, text="統合済_ の一次ファイル",
                   command=lambda: self._preset("統合済_", "")).pack(side="left", padx=4)
        ttk.Button(p, text="コピー / (1) 系",
                   command=lambda: self._preset("コピー,- copy,(1),(2)", "")).pack(side="left", padx=4)
        ttk.Button(p, text="一時ファイル",
                   command=lambda: self._preset("", ".tmp,.bak,.old")).pack(side="left", padx=4)
        ttk.Button(p, text="抽出する", style="Act.TButton",
                   command=self.run_filter).pack(side="left", padx=16)

        # ===== 一覧 =====
        mid = ttk.LabelFrame(self, text=" 2. 一覧（■＝整理する対象 / クリックで切替）")
        mid.pack(fill="both", expand=True, padx=10, pady=4)

        cols = ("chk", "folder", "size", "mtime", "note")
        self.tree = ttk.Treeview(mid, columns=cols, show="tree headings", selectmode="extended")
        self.tree.heading("#0", text="グループ / ファイル名")
        self.tree.heading("chk", text="対象")
        self.tree.heading("folder", text="フォルダ")
        self.tree.heading("size", text="サイズ")
        self.tree.heading("mtime", text="更新日時")
        self.tree.heading("note", text="備考")
        self.tree.column("#0", width=350, minwidth=180)
        self.tree.column("chk", width=48, anchor="center", stretch=False)
        self.tree.column("folder", width=430)
        self.tree.column("size", width=90, anchor="e", stretch=False)
        self.tree.column("mtime", width=130, anchor="center", stretch=False)
        self.tree.column("note", width=140)
        vs = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        hs = ttk.Scrollbar(mid, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vs.grid(row=0, column=1, sticky="ns")
        hs.grid(row=1, column=0, sticky="ew")
        mid.rowconfigure(0, weight=1)
        mid.columnconfigure(0, weight=1)

        self.tree.tag_configure("group", background="#eef3fb")
        self.tree.tag_configure("keep", foreground="#0a6b2a")
        self.tree.tag_configure("target", foreground="#b00020")
        self.tree.tag_configure("cloud", foreground="#7a5c00")
        self.tree.bind("<Button-1>", self._on_click)
        self.tree.bind("<space>", lambda e: self._toggle_selected())
        self.tree.bind("<Double-1>", self._open_file)
        self.tree.bind("<Button-3>", self._popup)

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="エクスプローラーで表示", command=self._reveal)
        self.menu.add_command(label="ファイルを開く", command=self._open_file)
        self.menu.add_separator()
        self.menu.add_command(label="チェックを反転", command=self._toggle_selected)

        # ===== 操作 =====
        bot = ttk.LabelFrame(self, text=" 3. 選択したファイルの処理 ")
        bot.pack(fill="x", padx=10, pady=(4, 8))

        row1 = ttk.Frame(bot)
        row1.pack(fill="x", padx=8, pady=(8, 2))
        ttk.Button(row1, text="各グループ 1件残して選択", command=self.auto_select).pack(side="left")
        ttk.Button(row1, text="全選択", command=lambda: self.select_all(True)).pack(side="left", padx=4)
        ttk.Button(row1, text="全解除", command=lambda: self.select_all(False)).pack(side="left")
        ttk.Separator(row1, orient="vertical").pack(side="left", fill="y", padx=10)
        ttk.Label(row1, text="移動先:").pack(side="left")
        self.var_dest = tk.StringVar(value="")
        ttk.Entry(row1, textvariable=self.var_dest, width=48).pack(side="left", padx=4)
        ttk.Button(row1, text="参照", command=self.pick_dest).pack(side="left")
        self.var_tree = tk.BooleanVar(value=True)
        ttk.Checkbutton(row1, text="元のフォルダ構成を保つ", variable=self.var_tree).pack(side="left", padx=8)

        row2 = ttk.Frame(bot)
        row2.pack(fill="x", padx=8, pady=(2, 8))
        ttk.Button(row2, text="■ 選択を移動する", style="Act.TButton",
                   command=self.do_move).pack(side="left")
        ttk.Button(row2, text="■ 選択をごみ箱へ", style="Act.TButton",
                   command=self.do_recycle).pack(side="left", padx=6)
        ttk.Button(row2, text="CSVに書き出す", command=self.do_csv).pack(side="left", padx=6)
        ttk.Separator(row2, orient="vertical").pack(side="left", fill="y", padx=10)
        ttk.Button(row2, text="直前の移動を元に戻す", command=self.do_undo).pack(side="left")
        ttk.Button(row2, text="中止", command=self.do_cancel).pack(side="right")

        # ===== ステータス =====
        st = ttk.Frame(self)
        st.pack(fill="x", padx=10, pady=(0, 8))
        self.pb = ttk.Progressbar(st, mode="determinate", maximum=1000)
        self.pb.pack(side="left", fill="x", expand=True)
        self.var_status = tk.StringVar(value="対象フォルダを追加して検索してください。")
        ttk.Label(st, textvariable=self.var_status).pack(side="left", padx=10)
        self.var_summary = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.var_summary, style="Head.TLabel").pack(
            anchor="w", padx=12, pady=(0, 8))

    # -------------------------------------------------- 設定
    def _load_config(self):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                c = json.load(f)
            for p in c.get("folders", []):
                if os.path.isdir(p):
                    self.folder_list.insert("end", p)
            self.var_dest.set(c.get("dest", ""))
        except Exception:
            pass
        if not self.folder_list.size():
            self.add_desktop()
        if not self.var_dest.get():
            self.var_dest.set(os.path.join(self._desktop(), QUARANTINE_NAME))

    def _save_config(self):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump({"folders": list(self.folder_list.get(0, "end")),
                           "dest": self.var_dest.get()}, f, ensure_ascii=False, indent=1)
        except Exception:
            pass

    def _on_close(self):
        self.cancel.set()
        self._save_config()
        self.destroy()

    def _desktop(self):
        for cand in (os.path.join(os.path.expanduser("~"), "OneDrive", "デスクトップ"),
                     os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop"),
                     os.path.join(os.path.expanduser("~"), "Desktop")):
            if os.path.isdir(cand):
                return cand
        return os.path.expanduser("~")

    # -------------------------------------------------- フォルダ操作
    def add_folder(self):
        d = filedialog.askdirectory(title="対象フォルダを選択", initialdir=self._desktop())
        if d:
            d = os.path.normpath(d)
            if d not in self.folder_list.get(0, "end"):
                self.folder_list.insert("end", d)

    def add_desktop(self):
        d = self._desktop()
        if d not in self.folder_list.get(0, "end"):
            self.folder_list.insert("end", d)

    def del_folder(self):
        for i in reversed(self.folder_list.curselection()):
            self.folder_list.delete(i)

    def pick_dest(self):
        d = filedialog.askdirectory(title="移動先フォルダ", initialdir=self._desktop())
        if d:
            self.var_dest.set(os.path.normpath(d))

    def _preset(self, kw, ext):
        self.var_kw.set(kw)
        self.var_ext.set(ext)

    def _on_tab(self, _e=None):
        self.mode = "dup" if self.nb.index("current") == 0 else "filter"

    # -------------------------------------------------- 検索実行
    def _roots(self):
        roots = [p for p in self.folder_list.get(0, "end") if os.path.isdir(p)]
        if not roots:
            messagebox.showwarning(APP_NAME, "対象フォルダを追加してください。")
        return roots

    def _busy(self):
        if self.worker and self.worker.is_alive():
            messagebox.showinfo(APP_NAME, "処理中です。完了までお待ちください。")
            return True
        return False

    def run_dup(self):
        if self._busy():
            return
        roots = self._roots()
        if not roots:
            return
        try:
            min_size = max(int(float(self.var_minkb.get() or 0) * 1024), 1)
        except ValueError:
            min_size = 1
        opts = {"recursive": self.var_recursive.get(),
                "skip_optional": self.var_skipopt.get(),
                "hydrate_cloud": self.var_hydrate.get(),
                "min_size": min_size}
        self.mode = "dup"
        self._start(lambda rep, cx: ("dup", find_duplicates(roots, opts, rep, cx)))

    def run_filter(self):
        if self._busy():
            return
        roots = self._roots()
        if not roots:
            return
        older = None
        s = self.var_older.get().strip()
        if s:
            for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"):
                try:
                    older = datetime.strptime(s, fmt).timestamp()
                    break
                except ValueError:
                    continue
            if older is None:
                messagebox.showwarning(APP_NAME, "日付は 2026-01-31 の形式で入力してください。")
                return
        try:
            min_size = int(float(self.var_minmb.get() or 0) * 1024 * 1024)
        except ValueError:
            min_size = 0
        opts = {"recursive": self.var_recursive.get(),
                "skip_optional": self.var_skipopt.get(),
                "keywords": self.var_kw.get(),
                "match_all": self.var_matchall.get(),
                "exts": self.var_ext.get(),
                "older_than_ts": older,
                "min_size": min_size}
        if not (opts["keywords"].strip() or opts["exts"].strip() or older or min_size):
            if not messagebox.askyesno(APP_NAME, "条件が空です。対象フォルダの全ファイルを一覧にしますか？"):
                return
        self.mode = "filter"
        self._start(lambda rep, cx: ("filter", filter_files(roots, opts, rep, cx)))

    def _start(self, fn):
        self.cancel.clear()
        self.tree.delete(*self.tree.get_children())
        self.records.clear()
        self.checked.clear()
        self.groups = []
        self.var_summary.set("")
        self.pb["value"] = 0

        def report(text, frac=None):
            self.q.put(("progress", text, frac))

        def run():
            try:
                kind, result = fn(report, self.cancel)
                self.q.put(("done", kind, result))
            except Exception:
                self.q.put(("error", traceback.format_exc()))

        self.worker = threading.Thread(target=run, daemon=True)
        self.worker.start()
        self.var_status.set("検索中…")

    def do_cancel(self):
        self.cancel.set()
        self.var_status.set("中止しました。")

    def _poll(self):
        try:
            while True:
                msg = self.q.get_nowait()
                if msg[0] == "progress":
                    self.var_status.set(msg[1])
                    if msg[2] is not None:
                        self.pb["value"] = int(msg[2] * 1000)
                elif msg[0] == "done":
                    self.pb["value"] = 1000
                    if msg[1] == "dup":
                        self._show_dups(msg[2])
                    else:
                        self._show_flat(msg[2])
                elif msg[0] == "error":
                    self.var_status.set("エラーが発生しました。")
                    messagebox.showerror(APP_NAME, msg[1])
        except queue.Empty:
            pass
        self.after(120, self._poll)

    # -------------------------------------------------- 一覧表示
    def _keep_rank(self, rec):
        name = rec.name
        low = name.lower()
        penalty = 0
        for kw in COPY_HINTS:
            if kw in name or kw in low:
                penalty += 10
                break
        if QUARANTINE_NAME in rec.path or CONSOLIDATED_NAME in rec.path:
            penalty += 50
        if name.startswith("統合済_"):
            penalty += 30
        return (penalty, rec.path.count(os.sep), len(rec.path), rec.mtime)

    def _show_dups(self, groups):
        self.groups = groups
        total_files = 0
        waste = 0
        for i, (size, state, members) in enumerate(groups, 1):
            members = sorted(members, key=self._keep_rank)
            total_files += len(members)
            waste += size * (len(members) - 1)
            gid = self.tree.insert(
                "", "end",
                text="グループ %d  （%d 件が同一 / 1件 %s）" % (i, len(members), human_size(size)),
                values=("", "", human_size(size * (len(members) - 1)), "", state),
                open=True, tags=("group",))
            for j, rec in enumerate(members):
                cloud = state.startswith("サイズ一致")
                note = "★残す（推奨）" if j == 0 else ""
                if cloud:
                    note = "クラウドのみ・未照合" if j else "★残す（要目視確認）"
                iid = self.tree.insert(gid, "end", text=rec.name,
                                       values=(CHECK_OFF, rec.folder, human_size(rec.size),
                                               fmt_time(rec.mtime), note),
                                       tags=("cloud",) if cloud else ("keep" if j == 0 else "target",))
                self.records[iid] = rec
        self.var_status.set("完了")
        self.var_summary.set("重複グループ %d 件 / 対象ファイル %d 件 / 整理できる容量 約 %s"
                             % (len(groups), total_files, human_size(waste)))
        if groups:
            self.auto_select()
        else:
            messagebox.showinfo(APP_NAME, "内容が完全一致する重複ファイルは見つかりませんでした。")

    def _show_flat(self, recs):
        total = 0
        for rec in recs:
            total += rec.size
            note = "クラウドのみ" if rec.cloud else ""
            iid = self.tree.insert("", "end", text=rec.name,
                                   values=(CHECK_OFF, rec.folder, human_size(rec.size),
                                           fmt_time(rec.mtime), note),
                                   tags=("cloud",) if rec.cloud else ())
            self.records[iid] = rec
        self.var_status.set("完了")
        self.var_summary.set("抽出 %d 件 / 合計 %s" % (len(recs), human_size(total)))
        if not recs:
            messagebox.showinfo(APP_NAME, "条件に一致するファイルはありませんでした。")

    # -------------------------------------------------- チェック操作
    def _set_check(self, iid, on):
        if iid not in self.records:
            return
        self.tree.set(iid, "chk", CHECK_ON if on else CHECK_OFF)
        if on:
            self.checked.add(iid)
        else:
            self.checked.discard(iid)

    def _on_click(self, event):
        if self.tree.identify_region(event.x, event.y) != "cell":
            return
        if self.tree.identify_column(event.x) != "#1":
            return
        iid = self.tree.identify_row(event.y)
        if iid in self.records:
            self._set_check(iid, iid not in self.checked)
            self._update_count()
            return "break"

    def _toggle_selected(self):
        for iid in self.tree.selection():
            if iid in self.records:
                self._set_check(iid, iid not in self.checked)
            else:
                for c in self.tree.get_children(iid):
                    self._set_check(c, c not in self.checked)
        self._update_count()

    def select_all(self, on):
        for iid in self.records:
            self._set_check(iid, on)
        self._update_count()

    def auto_select(self):
        """各グループの先頭（残す推奨）以外にチェック。クラウド未照合グループは対象外。"""
        if self.mode != "dup":
            self.select_all(True)
            return
        self.select_all(False)
        for gid in self.tree.get_children(""):
            state = self.tree.set(gid, "note")
            kids = self.tree.get_children(gid)
            if state.startswith("サイズ一致"):
                continue
            for iid in kids[1:]:
                self._set_check(iid, True)
        self._update_count()

    def _update_count(self):
        n = len(self.checked)
        size = sum(self.records[i].size for i in self.checked)
        self.var_status.set("チェック中: %d 件 / %s" % (n, human_size(size)))

    def _checked_recs(self):
        """一覧の並び順どおりにチェック済みレコードを返す"""
        out = []
        for gid in self.tree.get_children(""):
            kids = self.tree.get_children(gid)
            for iid in (kids if kids else (gid,)):
                if iid in self.checked and iid in self.records:
                    out.append(self.records[iid])
        return out

    # -------------------------------------------------- 右クリック等
    def _popup(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            self.menu.tk_popup(event.x_root, event.y_root)

    def _open_file(self, _e=None):
        sel = self.tree.selection()
        if sel and sel[0] in self.records:
            try:
                os.startfile(self.records[sel[0]].path)
            except Exception as e:
                messagebox.showerror(APP_NAME, str(e))

    def _reveal(self):
        sel = self.tree.selection()
        if sel and sel[0] in self.records:
            subprocess.Popen(["explorer", "/select,", os.path.normpath(self.records[sel[0]].path)])

    # -------------------------------------------------- 実行
    def do_move(self):
        recs = self._checked_recs()
        if not recs:
            messagebox.showinfo(APP_NAME, "チェックされたファイルがありません。")
            return
        dest = self.var_dest.get().strip()
        if not dest:
            messagebox.showwarning(APP_NAME, "移動先フォルダを指定してください。")
            return
        size = sum(r.size for r in recs)
        if not messagebox.askokcancel(
                APP_NAME,
                "%d 件（%s）を下記へ移動します。\n\n%s\n\n※あとで「直前の移動を元に戻す」で戻せます。"
                % (len(recs), human_size(size), dest)):
            return
        base = self.folder_list.get(0) if self.folder_list.size() else self._desktop()
        ok, ng, _ = move_files(recs, dest, self.var_tree.get(), base)
        self._after_action(ok, ng, "移動")

    def do_recycle(self):
        recs = self._checked_recs()
        if not recs:
            messagebox.showinfo(APP_NAME, "チェックされたファイルがありません。")
            return
        size = sum(r.size for r in recs)
        if not messagebox.askokcancel(
                APP_NAME,
                "%d 件（%s）を【ごみ箱】へ送ります。\n\n"
                "完全削除ではありません。誤りに気づいたらごみ箱から復元できます。\n実行しますか？"
                % (len(recs), human_size(size)), icon="warning"):
            return
        ok, ng = send_to_recycle([r.path for r in recs])
        self._after_action(ok, [(p, "失敗") for p in ng], "ごみ箱への移動")

    def _after_action(self, ok, ng, label):
        for iid in list(self.checked):
            rec = self.records.get(iid)
            if rec and not os.path.exists(rec.path):
                self.tree.delete(iid)
                self.records.pop(iid, None)
                self.checked.discard(iid)
        for gid in self.tree.get_children(""):
            if self.tree.item(gid, "text").startswith("グループ") and not self.tree.get_children(gid):
                self.tree.delete(gid)
        msg = "%s 完了: %d 件" % (label, ok)
        if ng:
            msg += "\n\n失敗 %d 件:\n" % len(ng) + "\n".join("・%s（%s）" % (p, e) for p, e in ng[:10])
        messagebox.showinfo(APP_NAME, msg)
        self.var_status.set(msg.splitlines()[0])

    def do_undo(self):
        ok, ng, info = undo_last_move()
        if ok == 0 and ng == 0:
            messagebox.showinfo(APP_NAME, info)
        else:
            messagebox.showinfo(APP_NAME, "元に戻しました: %d 件（失敗 %d 件）" % (ok, ng))

    def do_csv(self):
        if not self.records:
            messagebox.showinfo(APP_NAME, "一覧が空です。")
            return
        path = filedialog.asksaveasfilename(
            title="CSVの保存先", defaultextension=".csv",
            initialfile="ファイル整理リスト_%s.csv" % datetime.now().strftime("%Y%m%d_%H%M"),
            filetypes=[("CSV", "*.csv")], initialdir=self._desktop())
        if not path:
            return
        rows = []
        for gid in self.tree.get_children(""):
            kids = self.tree.get_children(gid)
            if kids:
                gname = self.tree.item(gid, "text")
                for iid in kids:
                    rows.append((gname, iid))
            else:
                rows.append(("", gid))
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["グループ", "処理", "ファイル名", "フォルダ", "サイズ(バイト)",
                        "サイズ", "更新日時", "備考", "フルパス"])
            for gname, iid in rows:
                rec = self.records.get(iid)
                if not rec:
                    continue
                w.writerow([gname, "整理する" if iid in self.checked else "残す",
                            rec.name, rec.folder, rec.size, human_size(rec.size),
                            fmt_time(rec.mtime), self.tree.set(iid, "note"), rec.path])
        if messagebox.askyesno(APP_NAME, "CSVを保存しました。開きますか？\n%s" % path):
            os.startfile(path)


def main():
    try:
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
        App().mainloop()
    except Exception:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(APP_NAME, traceback.format_exc())


if __name__ == "__main__":
    main()
