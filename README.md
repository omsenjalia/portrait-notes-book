# portrait-notes-book

Turn ONE lecture source (PDF, notes, slides, OCR'd transcript) into ONE
finished **A4 portrait PDF** that reads like a short, well-made **textbook** —
numbered chapters and sections, full-page chapter openers, worked examples,
teaching figures, review questions, practice set with answer key, mind map,
quick reference and glossary — with a **preflight QA script** that gates
delivery.

This is an agent skill: give the SKILL.md to any coding agent (Claude Code,
OpenCode, Codex-style CLIs, …) together with your course material, and it
builds the book for you.

## What you get

- **One template, every subject** — subject style packs: `dsa`/`programming`
  (code-editor look), `maths` (graph-paper look), `theory`, `spreadsheet`,
  `mixed`. The pack sets the cover, chapter openers, accent colour and box
  styles; the layout rules are subject-neutral.
- **Real build tooling, battle-tested** — WeasyPrint + KaTeX pipeline with the
  hard-won fixes baked in (`file://` font URLs, named cover/opener pages,
  ribbon-inside-box, `break-after:avoid`, two-pass Contents page numbers,
  `font-family` on every SVG).
- **Honest QA** — `preflight.py` hard-checks page size, fonts, body size, page
  budget, stranded headings, opener integrity, Contents page numbers and
  required pages. A FAIL means rebuild, not "mention it".
- **Accuracy rules** — every worked example is recomputed, historical claims
  need a source you actually read, and GATE (exam-syllabus) tagging is
  verify-first, `off` by default for anything else.

## Example output

| | |
|---|---|
| [`examples/Binary_Search_Notes.pdf`](examples/Binary_Search_Notes.pdf) | Finished full-mode book, `dsa` pack (code-editor look) |
| [`examples/Infinite_Series_Slice_Test.pdf`](examples/Infinite_Series_Slice_Test.pdf) | One-chapter maths-pack slice from the worked harness |

## Install

Clone the repo into your harness's skills directory:

```sh
# Claude Code
git clone https://github.com/omsenjalia/portrait-notes-book ~/.claude/skills/portrait-notes-book

# OpenCode
git clone https://github.com/omsenjalia/portrait-notes-book ~/.config/opencode/skills/portrait-notes-book
```

(Any harness that reads `SKILL.md` files works the same way: the repo root is
the skill directory.)

## Use

Ask the agent for a book, e.g.:

> Make study notes on multiple integrals from `lecture-1.md`, maths pack, mini mode.

Or with overrides in chat: *"dark theme"*, *"no GATE tags"*, *"compact"*,
*"mini"*.

The agent follows the staged RUN PLAN inside `SKILL.md`:
**content.md → build (reusing `assets/`) → preflight → deliver**, and reports
what was verified and what was not.

## Dependencies (installed once per project, on first run)

| Tool | Used for |
|---|---|
| `pip install weasyprint brotli pdfminer.six --break-system-packages` | HTML/CSS → PDF rendering and preflight |
| `npm install @fontsource/google-sans @fontsource/google-sans-code katex` | Real Google Sans fonts + server-side KaTeX |

## Repo layout

```
SKILL.md                  the skill: config, rules, run plan, build method
references/style-packs.md the 5 subject style packs in full
references/page-recipes.md page recipes, shape library, pill inventory
assets/preflight.py       QA script (full | mini | slice modes)
assets/build_slice.py     worked one-chapter maths build (reference harness)
assets/book.css           maths-pack stylesheet used by build_slice.py
assets/mathrender.js      batch KaTeX renderer (node)
examples/                 two finished PDFs, showcase + style reference
```

## License

MIT — see [LICENSE](LICENSE).
