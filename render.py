#!/usr/bin/env python3
"""一页卡渲染器（只用 Python 标准库；导出 PNG 时才需要 Playwright）。

用法：
  python3 render.py card.txt                 # 生成 card.html（A4）
  python3 render.py card.txt --size phone    # a4 | a5 | phone | widget
  python3 render.py card.txt --png           # 另存每张卡的 PNG（需 Playwright）
  python3 render.py card.txt --save cards/   # 存档：cards/<卡名>/<日期>.txt + index.html
  python3 render.py --list                   # 列出全部卡片类型
  python3 render.py --skeleton project       # 打印某个类型的填写骨架
  cat card.txt | python3 render.py - -o out.html
"""
import argparse
import datetime as dt
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
SIZES = ("a4", "a5", "phone", "widget")
LIST_KINDS = {"numbered", "steps", "list", "checks", "options", "layers", "history"}
EXAMPLE_LINE = {
    "numbered": "1. {hint}",
    "steps": "1. {hint}",
    "list": "- {hint}",
    "checks": "- {hint}",
    "options": "- 选项名——{hint}",
    "layers": "- 层名：{hint}",
    "history": "- YYYY-MM-DD {hint}",
}


def load_types():
    return json.loads((HERE / "types.json").read_text(encoding="utf-8"))["types"]


def skeleton(t):
    """某个类型的填写骨架（纯文本），给 agent 照着填。"""
    out = [f"# {t['name']}：字数上限 {t['maxChars']}；不需要的可选行整行删掉", f"类型：{t['name']}"]
    for f in t["fields"]:
        if f["kind"] in LIST_KINDS:
            out.append(f"{f['key']}：")
            out.append(EXAMPLE_LINE[f["kind"]].format(hint=f["hint"]))
        elif f["kind"] == "days":
            out.append(f"{f['key']}：")
        else:
            out.append(f"{f['key']}：（{f['hint']}）")
    return "\n".join(out)


def split_cards(text):
    return [b.strip() for b in re.split(r"^\s*-{4,}\s*$", text, flags=re.M) if b.strip()]


def detect(block, types):
    keys = {m.group(1) for m in re.finditer(r"^\s*([^\s：:]{1,8})\s*[：:]", block, flags=re.M)}
    m = re.search(r"^\s*类型\s*[：:]\s*(\S+)", block, flags=re.M)
    if m:
        v = m.group(1)
        for t in types:
            if v in (t["id"], t["name"], *t["aliases"]) or t["name"] in v:
                return t
    best, score = types[0], 0
    for t in types:
        s = sum(2 for k in t["detect"] if k in keys) + sum(1 for f in t["fields"] if f["key"] in keys)
        if s > score:
            best, score = t, s
    return best


def card_name(block, t):
    for f in t["fields"]:
        if f["kind"] in ("title", "eyebrow"):
            m = re.search(rf"^\s*{re.escape(f['key'])}\s*[：:]\s*(.+)$", block, flags=re.M)
            if m:
                name = re.sub(r"[\\/:*?\"<>|\s／]+", "-", m.group(1)).strip("-")
                return name[:40] or t["id"]
    return t["id"]


def build_html(text, size="a4"):
    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    for ph in ("{{CARD_TEXT}}", "{{SIZE}}"):
        if ph not in tpl:
            sys.exit(f"template.html 缺少 {ph} 占位符，请运行 python3 tools/build.py")
    tpl = tpl.replace("{{SIZE}}", size, 1)
    return tpl.replace("{{CARD_TEXT}}", html.escape(text), 1)


def export_png(html_path, size, stem):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("导出 PNG 需要 Playwright：pip install playwright && playwright install chromium")
    scale = 3 if size in ("phone", "widget") else 2
    paths = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1000, "height": 1300}, device_scale_factor=scale)
        pg.goto(html_path.resolve().as_uri() + f"#size={size}")
        pg.wait_for_timeout(300)
        for i, card in enumerate(pg.query_selector_all(".card"), 1):
            out = stem.parent / f"{stem.name}-{i}.png"
            card.screenshot(path=str(out))
            paths.append(out)
        b.close()
    return paths


def main():
    ap = argparse.ArgumentParser(description="渲染一页卡")
    ap.add_argument("card", nargs="?", help="卡片文本文件；- 表示从标准输入读")
    ap.add_argument("-o", "--out", help="输出 HTML 路径，默认与输入同名")
    ap.add_argument("--size", choices=SIZES, default="a4", help="a4 / a5 / phone（手机壁纸）/ widget（小组件）")
    ap.add_argument("--png", action="store_true", help="同时导出每张卡的 PNG（需 Playwright）")
    ap.add_argument("--save", metavar="DIR", help="存档：DIR/<卡名>/<日期>.txt，并生成 DIR/<卡名>/index.html")
    ap.add_argument("--list", action="store_true", help="列出全部卡片类型")
    ap.add_argument("--skeleton", metavar="TYPE", help="打印某个类型的填写骨架（id 或中文名）")
    a = ap.parse_args()
    types = load_types()

    if a.list:
        for t in types:
            print(f"{t['id']:<10} {t['name']:<5} {t['when']}")
        return
    if a.skeleton:
        t = next((t for t in types if a.skeleton in (t["id"], t["name"], *t["aliases"])), None)
        if not t:
            sys.exit(f"没有这个类型：{a.skeleton}。用 --list 查看全部类型")
        print(skeleton(t))
        return
    if not a.card:
        ap.error("请给出卡片文本文件，或使用 --list / --skeleton")

    if a.card == "-":
        text, src = sys.stdin.read().strip(), pathlib.Path("card.txt")
    else:
        src = pathlib.Path(a.card)
        if not src.exists():
            sys.exit(f"找不到文件：{src}")
        text = src.read_text(encoding="utf-8").strip()
    if not text:
        sys.exit("卡片文本是空的")

    outputs = []
    if a.save:
        today = dt.date.today().isoformat()
        for block in split_cards(text):
            t = detect(block, types)
            folder = pathlib.Path(a.save) / card_name(block, t)
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"{today}.txt").write_text(block + "\n", encoding="utf-8")
            (folder / "latest.txt").write_text(block + "\n", encoding="utf-8")
            out = folder / "index.html"
            out.write_text(build_html(block, a.size), encoding="utf-8")
            outputs.append(out)
            versions = sorted(p.stem for p in folder.glob("????-??-??.txt"))
            print(f"已存档：{folder.resolve()}（{t['name']}，共 {len(versions)} 个版本）")
    else:
        out = pathlib.Path(a.out) if a.out else src.with_suffix(".html")
        out.write_text(build_html(text, a.size), encoding="utf-8")
        outputs.append(out)
        names = "、".join(detect(b, types)["name"] for b in split_cards(text))
        print(f"已生成：{out.resolve()}（{names}）")

    if a.png:
        for out in outputs:
            for p in export_png(out, a.size, out.with_suffix("")):
                print(f"已导出：{p.resolve()}")


if __name__ == "__main__":
    main()
