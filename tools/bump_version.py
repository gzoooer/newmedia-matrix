#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发布新版本：提升指定专家的版本号，同步写入 plugin.json 与 marketplace.json。

用法：
    python tools/bump_version.py <专家名> [patch|minor|major]
    python tools/bump_version.py --list          # 查看当前所有版本

示例：
    python tools/bump_version.py legal-compliance-auditor patch
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = os.path.join(ROOT, ".codebuddy-plugin", "marketplace.json")


def bump(v: str, part: str) -> str:
    try:
        major, minor, patch = (int(x) for x in v.split("."))
    except Exception:
        major, minor, patch = 1, 0, 0
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def main():
    mp = json.load(open(META, encoding="utf-8"))

    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print(f"{'专家':34s}{'plugin.json':>14s}{'marketplace':>14s}")
        for e in mp["plugins"]:
            pj_path = os.path.join(ROOT, e["source"].lstrip("./"), ".codebuddy-plugin", "plugin.json")
            pv = json.load(open(pj_path, encoding="utf-8")).get("version", "-")
            flag = "" if pv == e.get("version") else "  ⚠️ 不一致"
            print(f"{e['name']:34s}{pv:>14s}{e.get('version', '-'):>14s}{flag}")
        return

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    name = sys.argv[1]
    part = sys.argv[2] if len(sys.argv) > 2 else "patch"
    if part not in ("patch", "minor", "major"):
        print(f"❌ 未知的版本类型：{part}（可选 patch / minor / major）")
        sys.exit(1)

    entry = next((e for e in mp["plugins"] if e["name"] == name), None)
    if entry is None:
        print(f"❌ 市场中没有专家：{name}")
        print("   现有专家：" + ", ".join(e["name"] for e in mp["plugins"]))
        sys.exit(1)

    pj_path = os.path.join(ROOT, entry["source"].lstrip("./"), ".codebuddy-plugin", "plugin.json")
    pj = json.load(open(pj_path, encoding="utf-8"))

    old = pj.get("version", "1.0.0")
    new = bump(old, part)

    pj["version"] = new
    with open(pj_path, "w", encoding="utf-8") as f:
        json.dump(pj, f, ensure_ascii=False, indent=2)
        f.write("\n")

    entry["version"] = new
    with open(META, "w", encoding="utf-8") as f:
        json.dump(mp, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"✅ {name}: {old} → {new}（plugin.json 与 marketplace.json 已同步）")
    print("   下一步：git add -A && git commit -m \"update: %s v%s\" && git push" % (name, new))


if __name__ == "__main__":
    main()
