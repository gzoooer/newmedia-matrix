#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""打包本市场为可直接订阅的市场 zip（备选市场源）。

用法：
    python tools/build_market_zip.py            # 版本号自动从 marketplace.json 读取
    python tools/build_market_zip.py --out X.zip

产物默认写到 dist/新媒体矩阵专家市场-v<版本>.zip，同时保留一份不带版本号的
固定名 dist/marketplace-latest.zip（便于给朋友一个永久直链）。

关键：打包时排除 dist/ 自身，否则会把上一版 zip 套进新 zip，体积无限膨胀。
"""

import argparse
import json
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", "__pycache__", "dist", ".idea", ".vscode"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db", ".created-by-session"}
EXCLUDE_EXT = {".pyc"}


def read_version():
    p = os.path.join(ROOT, ".codebuddy-plugin", "marketplace.json")
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    # 市场级版本优先；没有则取各插件版本最大值
    if data.get("version"):
        return data["version"]
    vers = [x.get("version", "0.0.0") for x in data.get("plugins", [])]
    return max(vers) if vers else "0.0.0"


def collect():
    files = []
    for root, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for n in names:
            if n in EXCLUDE_FILES or os.path.splitext(n)[1] in EXCLUDE_EXT:
                continue
            full = os.path.join(root, n)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            files.append((full, rel))
    return sorted(files, key=lambda x: x[1])


def build(out_path, files, version):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        for full, rel in files:
            z.write(full, rel)
    size = os.path.getsize(out_path)
    # 自检：必须含市场清单，且不得泄漏 .git
    with zipfile.ZipFile(out_path) as z:
        names = z.namelist()
        assert ".codebuddy-plugin/marketplace.json" in names, "缺少 marketplace.json"
        assert not any(x.startswith(".git/") for x in names), "泄漏 .git"
        assert not any(x.startswith("dist/") for x in names), "误把 dist 套进 zip"
        assert not any("/.created-by-session" in x for x in names), "泄漏会话标识"
        bad = z.testzip()
        assert bad is None, f"zip 损坏于 {bad}"
    print(f"✅ {os.path.basename(out_path)}  v{version}  "
          f"{size / 1024:.1f} KB  {len(files)} 个文件")
    return size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="输出路径，默认 dist/ 下")
    args = ap.parse_args()

    version = read_version()
    files = collect()
    dist = os.path.join(ROOT, "dist")

    if args.out:
        targets = [args.out]
    else:
        # 双产物：带版本号（归档）+ latest（永久直链）
        targets = [
            os.path.join(dist, f"新媒体矩阵专家市场-v{version}.zip"),
            os.path.join(dist, "marketplace-latest.zip"),
        ]

    for t in targets:
        build(t, files, version)

    print("\n市场源可直接填其中一个 zip 的直链（raw 地址）：")
    print(f"  https://github.com/gzoooer/newmedia-matrix/raw/main/dist/marketplace-latest.zip")


if __name__ == "__main__":
    main()
