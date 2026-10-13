# 一页卡 · One Page Card

把冗长的 AI 回复和项目资料，提炼成能贴在桌上、也能在手机上看的卡片。这个开源项目包含 Agent 技能说明、浏览器模板和只依赖 Python 标准库的生成脚本。

[在线体验](https://yyy8178.github.io/one-page-card/) · [技能说明](SKILL.md) · [English README](README.md)

它支持两种卡：

- **原则卡**：保存一个判断、一套做法或一个习惯；标题先给结论，要点写能执行的动作或能核对的事实。
- **项目卡**：记录目标、最新进展、唯一下一步、卡点、已定事项和待决定事项；隔一段时间回来也能接着做。

## 交给 Agent 使用

Codex 可以把本仓库安装到技能目录：

```bash
git clone https://github.com/YYY8178/one-page-card.git ~/.codex/skills/one-page-card
```

然后说“用 $one-page-card 把这段内容出成一张原则卡”或“根据新进展和旧卡，更新项目卡”。其他能读文件的 Agent 直接读取 [SKILL.md](SKILL.md)；只能聊天的 Agent 可以按其中“第 1 步”的字段格式输出卡片文本，再粘贴到[在线体验页](https://yyy8178.github.io/one-page-card/)。

## 自己生成网页

在仓库目录运行：

```bash
python3 render.py example.txt -o card.html
```

用浏览器打开 `card.html`。手机上直接阅读；打印时选 A4、边距“无”、启用“背景图形”，先看预览，确认文字没有被裁切。多张卡用单独一行 `----` 分隔，一张卡打印一页。

也可以直接打开 `template.html`，把卡片文本粘贴到输入框，点“生成卡片”。网页可离线使用，不需要账号、API 密钥或安装依赖。

## 示例与授权

[example.txt](example.txt) 提供一张原则卡和一张项目卡。项目采用 [MIT 许可证](LICENSE)。如果它帮你省下了反复翻聊天记录的时间，欢迎在 GitHub 点一个 Star。
