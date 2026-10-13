# One Page Card · 一页卡

**Turn long AI answers into cards you can use.** One Page Card is an agent skill and a dependency-free renderer for two formats: a **principle card** with a clear rule and concrete actions, and a **project card** with the current state, one next step, blockers, and decisions. Each card is a mobile-friendly web page and a printable A4 page.

[中文说明](README.zh-CN.md) · [Live demo](https://yyy8178.github.io/one-page-card/) · [Skill instructions](SKILL.md)

| Printable A4 | Mobile view |
| --- | --- |
| ![Example principle card printed on A4](assets/preview-a4.png) | ![Example principle card on a phone](assets/preview-mobile.png) |

## When to use it

- **Principle card:** Keep a rule, habit, or decision criterion visible instead of burying it in a long chat.
- **Project card:** Resume a project after a break with its goal, latest progress, next action, blocker, and pending decisions in one place.
- **Long AI response:** Ask your agent to extract one important idea into a card you can review later.

The skill tells the agent to write one card about one subject, lead with a conclusion, use checkable facts or actions, and mark uncertainty. It does not invent missing project facts.

## Quick start

### With an agent

Install this repository as a skill. For Codex, clone it into your skills directory:

```bash
git clone https://github.com/YYY8178/one-page-card.git ~/.codex/skills/one-page-card
```

Then ask: **“Use $one-page-card to turn this into a printable principle card: …”** or **“Update my project card from these notes and the previous card: …”**. Agents that do not discover skills automatically can read [SKILL.md](SKILL.md) directly. A chat-only agent can follow its **Step 1** and return card text; paste that text into the [live demo](https://yyy8178.github.io/one-page-card/).

### Without an agent

Open the [live demo](https://yyy8178.github.io/one-page-card/) or `template.html` locally, paste card text, and select **Generate Card** (the page UI is in Chinese). To render a text file with Python 3:

```bash
python3 render.py example.txt -o card.html
```

Open `card.html` in a browser. Select **Print**, choose **A4**, set margins to **None**, and enable **Background graphics**. Preview before printing to check for clipping. Separate multiple cards with a line containing `----`; each prints on its own page.

`render.py` uses only the Python standard library. The generated HTML works locally without a server, account, API key, or external font request.

## Files

| File | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Instructions and field formats for agents |
| [template.html](template.html) | Responsive browser editor and print layout |
| [render.py](render.py) | Converts card text into a single HTML file |
| [example.txt](example.txt) | One principle card and one project card |
| [docs/index.html](docs/index.html) | Public paste-and-print demo |

## Questions

**Is this an AI summarizer?** The agent selects and writes the content. This repository provides the card-writing instructions, text format, browser template, and deterministic renderer. It does not call an AI API.

**Can I use another agent?** Yes. Any agent that can read `SKILL.md` can follow it. Chat-only agents can output the specified plain-text format for the browser editor.

**Can I update an existing project card?** Yes. Give the agent the old card and new facts; the skill tells it to preserve lines that have not changed.

## License

[MIT](LICENSE). If this saves you from rereading a long AI response, a GitHub star helps others find it.
