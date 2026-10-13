# 一页卡 · One Page Card

**把冗长的 AI 回复，变成一张你真的会看的纸。**一页卡是一个 Agent 技能，加一个不依赖任何第三方库的排版器。Agent 自己从 **11 种卡型**里选一种，写几百字纯文本；固定模板把它排成 **A4 / A5 打印版**、**手机壁纸**或**桌面小组件**。

[在线体验](https://yyy8178.github.io/one-page-card/) · [技能说明](SKILL.md) · [卡型骨架](TYPES.md) · [English README](README.md)

![11 种卡型的 A4 打印效果](assets/gallery.png)

## 11 种卡型

由 Agent 根据内容自己选，不用你指定。

| 卡型 | id | 用途 |
| --- | --- | --- |
| 原则卡 | `principle` | 一个方法、规则、判断标准，想天天看到 |
| 项目卡 | `project` | 隔一阵回来也能接上：目标、现状、唯一下一步、卡点、已定的事、历史 |
| 决策卡 | `decision` | 守住底线比较选项，记下选择、撤回条件和复盘日 |
| 复盘卡 | `review` | 一件事做完：目标对结果，做对做错，下次怎么做 |
| 流程卡 | `sop` | 照着步骤做、交给别人执行的事，每步带打勾框 |
| 知识卡 | `knowledge` | 课程或书里的一个概念，落到自己身上的动作 |
| 架构卡 | `map` | 一个系统的分层，以及数据或事情怎么流动 |
| 习惯卡 | `habit` | 靠环境不靠意志力的规则、最低版本、7–60 天打卡格 |
| 周计划卡 | `week` | 最多三件要事、不做清单、每天一行 |
| 清单卡 | `checklist` | 每次做某件事前都要过一遍的检查项 |
| 人物卡 | `person` | 客户、合作方或家人：对方要什么、约定过什么、下次联系 |

卡型定义都在 [`types.json`](types.json)。每种卡型是一组字段，每个字段使用 17 种版式之一（编号要点、步骤、选项、分层、打卡格、手写线……）。新增一种卡只要加一段配置和一个示例，不用改代码。

## 为什么省 token

- Agent 只写固定格式的纯文本，从不写 HTML。
- Agent 只读它选中那一种卡型的骨架（`render.py --skeleton <id>`，或 `TYPES.md` 里的一节），不用读全部格式。
- 每种卡型有字数上限；更新卡片时只改有变化的行。

## 交给 Agent 使用

Codex 可以把本仓库装进技能目录：

```bash
git clone https://github.com/YYY8178/one-page-card.git ~/.codex/skills/one-page-card
```

然后说"把这段内容出成一页卡"或"根据新进展更新项目卡"。其他能读文件的 Agent 直接读 [SKILL.md](SKILL.md)；只能聊天的 Agent 按其中的步骤输出卡片文本，再粘贴到[在线体验页](https://yyy8178.github.io/one-page-card/)。

## 命令行生成

```bash
python3 render.py examples/project.txt                 # A4，生成 examples/project.html
python3 render.py card.txt --size phone                # a4 / a5 / phone / widget
python3 render.py card.txt --png                       # 同时导出 PNG（需要 Playwright）
python3 render.py card.txt --save cards/               # 按日期存档每个版本
python3 render.py --list                               # 列出全部卡型
python3 render.py --skeleton decision                  # 打印某种卡型的骨架
```

用浏览器打开生成的网页。工具栏可以切换尺寸；每张卡上方显示字数，超出一页会提示。打印时选对应纸张、边距"无"、勾选"背景图形"。多张卡用单独一行 `----` 分隔，一张卡打印一页；A4/A5 上多出的空白会自动变成手写备注线。

`render.py` 只用 Python 标准库（导出 PNG 时才需要 Playwright）。网页使用系统字体，可离线使用，不需要服务器、账号、API 密钥或任何外部请求。

| A4 打印 | 手机壁纸 |
| --- | --- |
| ![原则卡 A4](assets/preview-a4.png) | ![手机壁纸](assets/preview-mobile.png) |

## 常见问题

**这是 AI 摘要工具吗？**不是。内容由你的 Agent 挑选和撰写；本仓库提供写卡规则、文本格式、模板和确定性的排版器，不调用任何 AI 接口。

**一定要指定卡型吗？**不用。Agent 自己选；如果缺了"类型："这一行，排版器也会按字段名自动识别，所以 v0.1 的旧卡照样能用。

**能加自己的卡型吗？**能。在 `types.json` 里加一段，再加 `examples/<id>.txt`，然后运行 `python3 tools/build.py` 和 `python3 tools/check.py`。

## 授权

[MIT 许可证](LICENSE)。如果它帮你省下了反复翻聊天记录的时间，欢迎在 GitHub 点一个 Star。
