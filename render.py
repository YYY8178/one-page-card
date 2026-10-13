#!/usr/bin/env python3
"""一页卡渲染：python3 render.py card.txt [-o out.html]
把卡片纯文本塞进同目录的 template.html，生成可打印的 HTML。只用标准库。"""
import argparse
import html
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description="渲染一页卡")
ap.add_argument("card", help="卡片文本文件（.txt）")
ap.add_argument("-o", "--out", help="输出 HTML 路径，默认与输入同名")
a = ap.parse_args()

src = pathlib.Path(a.card)
if not src.exists():
    sys.exit(f"找不到文件：{src}")
text = src.read_text(encoding="utf-8").strip()
tpl = (here / "template.html").read_text(encoding="utf-8")
if "{{CARD_TEXT}}" not in tpl:
    sys.exit("template.html 缺少 {{CARD_TEXT}} 占位符")

# 文本放进 <textarea>，HTML 转义即可安全嵌入
out_html = tpl.replace("{{CARD_TEXT}}", html.escape(text), 1)
out = pathlib.Path(a.out) if a.out else src.with_suffix(".html")
out.write_text(out_html, encoding="utf-8")
print(f"已生成：{out.resolve()}")
