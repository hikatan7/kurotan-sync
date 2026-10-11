"""python build.py <id> [<id> ...] | all   -> docx 生成 + Word で PDF 化 + 頁数表示"""
import glob
import importlib.util
import os
import subprocess
import sys

import fitz

import notekit

HERE = os.path.dirname(os.path.abspath(__file__))


def load(nid):
    path = os.path.join(HERE, "notes", nid + ".py")
    spec = importlib.util.spec_from_file_location(nid, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.NOTE


def to_pdf(docxs):
    lst = os.path.join(HERE, "_pdf_list.txt")
    with open(lst, "w", encoding="utf-8-sig") as f:
        f.write("\n".join(docxs))
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                    os.path.join(HERE, "to_pdf.ps1"), lst], check=True)


if __name__ == "__main__":
    ids = sys.argv[1:]
    if ids == ["all"]:
        ids = sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(HERE, "notes", "*.py")))
    out = []
    for nid in ids:
        path, n = notekit.build(load(nid))
        out.append(path)
        print("docx", nid, n, "語")
    to_pdf(out)
    for p in out:
        pdf = p[:-5] + ".pdf"
        print(fitz.open(pdf).page_count, "頁", os.path.relpath(pdf, notekit.ROOT))
