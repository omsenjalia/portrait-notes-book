# portrait-notes-book

Turn one lecture source — PDF, notes, slides or an OCR transcript — into one
A4 portrait PDF that reads like a short textbook. The output has numbered
sections, worked examples with diagrams, review questions, a practice set with
an answer key, a mind map, a quick reference and a glossary. A preflight script
checks the result before delivery.

This is an agent skill. Give `SKILL.md` and your course material to any coding
agent that reads skill files.

## What it produces

- One PDF per source. Real selectable text, vector diagrams, embedded fonts.
- A quiet, neutral design with one teal accent, equal margins and one card
  style. No violet, no decorative grids, no coloured chip legends. See
  `references/taste-system.md`.
- Five subject packs: `dsa`, `programming`, `maths`, `theory`, `spreadsheet`
  and `mixed`. The pack chooses the cover and page frame; the layout rules
  are the same for every subject.
- Worked sums are written one algebraic step per line with a margin note and a
  boxed answer. Each example carries its own diagram, drawn from the actual
  mathematics rather than a decorative sketch.
- `preflight.py` checks page size, fonts, type size, page budget, stranded
  headings, opener integrity, Contents page numbers and required pages.
  `verify_math.py` recomputes every printed result.

## Examples

| File | What it shows |
|---|---|
| `examples/Binary_Search_Notes.pdf` | Finished full-mode book, `dsa` pack |
| `examples/Infinite_Series_Slice_Test.pdf` | One-chapter maths-pack slice |

The first PDF is a style reference from an earlier build; it does not pass the
current `full` preflight. The second passes `slice`.

## Install

Clone into your harness's skills directory. The repository root is the skill
directory.

```sh
git clone https://github.com/omsenjalia/portrait-notes-book ~/.config/opencode/skills/portrait-notes-book
git clone https://github.com/omsenjalia/portrait-notes-book ~/.claude/skills/portrait-notes-book
```

## Use

Ask for a book and name the source:

> Make study notes on multiple integrals from `lecture-1.md`, maths pack, mini mode.

The agent follows the staged plan in `SKILL.md`:
`content.md → build → preflight → deliver`.

## Dependencies

Installed once per project, on first use.

```sh
pip install weasyprint brotli pdfminer.six --break-system-packages
npm install @fontsource/google-sans @fontsource/google-sans-code katex
pip install pymupdf pillow --break-system-packages   # optional: contact sheets
```

PyMuPDF is used only to render contact-sheet thumbnails. Text extraction and
QA stay on pdfminer, which is fast on WeasyPrint output.

## Repository layout

```
SKILL.md                     rules, run plan, build method
references/taste-system.md   the one palette, type scale and card recipe
references/style-packs.md    the subject packs
references/page-recipes.md   page recipes, shape library, figure grammar
assets/book.css              the stylesheet
assets/build_slice.py        worked one-chapter build
assets/shapes.py             sampled SVG primitives
assets/math_values.py        canonical results
assets/verify_math.py        recomputes every result
assets/preflight.py          QA script: full | mini | slice
assets/contact_sheet.py      visual QA grid
assets/mathrender.js         batch KaTeX renderer
examples/                    two finished PDFs
SOURCES.md                   exact citation strings
```

## License

MIT. See `LICENSE`.
