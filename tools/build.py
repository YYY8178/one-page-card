#!/usr/bin/env python3
"""从 src/template.src.html + types.json + examples/ 生成：
template.html、docs/index.html、TYPES.md。改了类型或模板后运行一次。"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import render  # noqa: E402


def js(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def main():
    types_doc = json.loads((ROOT / "types.json").read_text(encoding="utf-8"))
    examples = {}
    for t in types_doc["types"]:
        p = ROOT / "examples" / f"{t['id']}.txt"
        if p.exists():
            examples[t["id"]] = p.read_text(encoding="utf-8").strip()
    src = (ROOT / "src" / "template.src.html").read_text(encoding="utf-8")
    out = src.replace("{{TYPES_JSON}}", js(types_doc)).replace("{{EXAMPLES_JSON}}", js(examples))
    (ROOT / "template.html").write_text(out, encoding="utf-8")
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "index.html").write_text(out, encoding="utf-8")

    lines = [
        "# 卡片类型与填写骨架",
        "",
        "> 本文件由 `tools/build.py` 根据 `types.json` 生成，不要手改。",
        "> Agent：先按 SKILL.md 的选型表选定类型，只读对应的那一节。",
        "",
    ]
    for t in types_doc["types"]:
        lines += [
            f"## {t['name']} `{t['id']}`",
            "",
            f"用途：{t['when']}。字数上限 {t['maxChars']}。",
            "",
            "```",
            render.skeleton(t),
            "```",
            "",
        ]
    (ROOT / "TYPES.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成 template.html、docs/index.html、TYPES.md（{len(types_doc['types'])} 种类型，{len(examples)} 个示例）")


if __name__ == "__main__":
    main()
