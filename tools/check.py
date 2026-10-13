#!/usr/bin/env python3
"""自检：把 examples/ 里每种卡在四种尺寸下渲染一遍，检查
1) 没有脚本错误；2) A4/A5 没有超出一页；3) 打印页数 = 卡片数；4) 390px 手机宽度无横向滚动。
需要 Playwright。用法：python3 tools/check.py [--shots DIR]"""
import argparse
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import render  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("需要 Playwright：pip install playwright && playwright install chromium")


def pdf_pages(data):
    return data.count(b"/Type /Page") - data.count(b"/Type /Pages")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", help="把截图存到这个目录")
    a = ap.parse_args()
    shots = pathlib.Path(a.shots) if a.shots else None
    if shots:
        shots.mkdir(parents=True, exist_ok=True)
    problems = []
    tmp = pathlib.Path(tempfile.mkdtemp())
    files = sorted((ROOT / "examples").glob("*.txt")) + [ROOT / "example.txt"]
    with sync_playwright() as p:
        b = p.chromium.launch()
        for f in files:
            text = f.read_text(encoding="utf-8")
            n_cards = len(render.split_cards(text))
            for size in render.SIZES:
                html_path = tmp / f"{f.stem}-{size}.html"
                html_path.write_text(render.build_html(text, size), encoding="utf-8")
                errors = []
                pg = b.new_page(viewport={"width": 1000, "height": 1300})
                pg.on("pageerror", lambda e: errors.append(str(e)))
                pg.goto(html_path.as_uri())
                pg.wait_for_timeout(250)
                tag = f"{f.stem}/{size}"
                if errors:
                    problems.append(f"{tag}: 脚本错误 {errors[0]}")
                cards = pg.query_selector_all(".card")
                if len(cards) != n_cards:
                    problems.append(f"{tag}: 渲染出 {len(cards)} 张卡，应为 {n_cards}")
                over = pg.eval_on_selector_all(".card", "cs => cs.filter(c => c.scrollHeight > c.clientHeight + 2).length")
                if over:
                    problems.append(f"{tag}: {over} 张卡超出版面")
                if size in ("a4", "a5"):
                    pages = pdf_pages(pg.pdf(prefer_css_page_size=True, print_background=True))
                    if pages != n_cards:
                        problems.append(f"{tag}: 打印 {pages} 页，应为 {n_cards} 页")
                if shots:
                    for i, c in enumerate(cards, 1):
                        c.screenshot(path=str(shots / f"{f.stem}-{size}-{i}.png"))
                pg.close()
            m = b.new_page(viewport={"width": 390, "height": 844})
            m.goto((tmp / f"{f.stem}-a4.html").as_uri())
            m.wait_for_timeout(200)
            if m.evaluate("document.documentElement.scrollWidth > 391"):
                problems.append(f"{f.stem}: 390px 手机宽度出现横向滚动")
            m.close()
        m = b.new_page(viewport={"width": 390, "height": 844})
        m.goto((ROOT / "docs" / "index.html").as_uri())
        m.wait_for_timeout(200)
        if m.evaluate("document.documentElement.scrollWidth > 391"):
            problems.append("docs/index.html: 390px 手机宽度出现横向滚动")
        m.close()
        b.close()
    if problems:
        print("发现问题：")
        for x in problems:
            print("  - " + x)
        sys.exit(1)
    print(f"全部通过：{len(files)} 个示例 × {len(render.SIZES)} 种尺寸")


if __name__ == "__main__":
    main()
