# Changelog

## v0.2.0 · 2026-10-13 

- **11 card types**: principle, project, decision, review, SOP, knowledge, system map, habit, weekly plan, checklist, person.
- **Configurable types**: `types.json` is the single source of truth; each type is a list of fields using 17 layout kinds. New types need no code.
- **Automatic type choice**: the skill tells the agent to choose the type itself; the renderer detects the type from field names when the `类型：` line is missing, so v0.1 cards still render.
- **Four sizes**: A4, A5, phone wallpaper (space left for the clock) and desktop widget, switchable in the page toolbar or with `render.py --size`.
- **PNG export**: `render.py --png` (optional Playwright).
- **Project history**: a `历史` field on project cards, plus `render.py --save DIR` to keep a dated copy of every version.
- **Fit checks**: each card shows its character count against the type's limit and warns when it overflows one page; spare space on A4/A5 becomes ruled note lines.
- **Fewer tokens**: agents read only the skeleton of the chosen type (`render.py --skeleton <id>` or one section of `TYPES.md`).
- **Tooling**: `tools/build.py` regenerates `template.html`, `docs/index.html` and `TYPES.md`; `tools/check.py` renders every example in every size and checks fit, print page count and 390px mobile width.

## v0.1.0 · 2026-10-13

- First public release: principle and project cards, A4 print layout, mobile view, `render.py`, live demo.
