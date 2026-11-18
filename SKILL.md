---
name: portrait-notes-book
license: MIT
description: >
  Turn ONE lecture source (PDF, notes, slides, transcript) into ONE finished
  A4 portrait PDF that reads like a short, well-made textbook: numbered
  chapters and sections, full-page chapter openers, worked examples, figures,
  review questions, practice set, answer key, mind map, quick reference,
  glossary — with a WeasyPrint + KaTeX build pipeline and a preflight QA
  script that gates delivery. Subject style packs for dsa/programming, maths,
  theory, spreadsheet and mixed notes. Use when the user asks for study
  notes, a notes book, textbook-style notes, lecture notes as a PDF book,
  revision notes, or a "study notes" deliverable from their course material.
---

# Portrait Notes Book

Turn ONE lecture source into ONE finished A4 portrait PDF that reads like a
short, well-made TEXTBOOK. Works for ANY subject: maths, programming, DSA,
theory subjects, or a mix.

This is the "digital / sellable e-book" template. It is separate from
handwritten-notes styles and does not follow their rules (no handwriting, no
ink colours, no highlighter marks).

**How to use this skill**

1. Read this SKILL.md fully.
2. Read `references/style-packs.md` (pick the pack FIRST, before any layout
   work) and `references/page-recipes.md` (page recipes, shape library, pill
   inventory) before drawing anything.
3. Copy build tooling from `assets/` and crib layout code from the worked
   example `assets/build_slice.py` + `assets/book.css` (a complete one-chapter
   maths build). Open `examples/Binary_Search_Notes.pdf` (dsa pack, finished
   book) and `examples/Infinite_Series_Slice_Test.pdf` (maths pack slice) to
   see the target look before you build.

---

## CONFIG — edit these; everything below reads from them

```
OUTPUT_FORMAT: PDF
PAGE_SIZE:     A4 portrait (210 × 297 mm)
THEME:         light
FONT:          Google Sans (text), Google Sans Code (code)
AUDIENCE:      student / exam aspirant / self-learner
SUBJECT_TYPE:  auto
TEMPLATE_MODE: full
GATE_TAGGING:  on
COVER_IMAGE:   none
STYLE_PACK:    auto      # dsa | programming | maths | theory | mixed | spreadsheet — see references/style-packs.md
                         # auto = chosen from the SUBJECT of the notes. The look of any previous book or
                         # reference file NEVER decides the pack. Only `spreadsheet` may use spreadsheet chrome.
SIZE:          large     # body 12 pt, roomy spacing
PAGE_BUDGET:   full 36–54 pages at SIZE large, mini 12–16 pages
                         # the required pages alone are about 22, so a 20–30 budget was impossible.
                         # Outside the budget: fix once, then deliver and say so. Never loop.
RUN_MODE:      staged    # content -> build -> check, see RUN PLAN. Never build the whole book in one go.
```

- `THEME`: `light` (white paper, restrained colour; the textbook default) or
  `dark` (screen reading only). "Print" always means `light`.
- `FONT`: Google Sans, regular for body text and bold for bold. Use real
  font files, not a lookalike (see BUILD METHOD). Math keeps its own math
  font.
- `SUBJECT_TYPE`: `auto` or one of `maths`, `programming`, `dsa`, `theory`,
  `mixed`.
- `TEMPLATE_MODE`: `full` (complete book) or `mini` (condensed).
- `GATE_TAGGING`: `on`, `off`, or `auto`.
- `COVER_IMAGE`: `none` (designed vector cover) or a path to an image the
  user supplied.
- `STYLE_PACK`: `auto` picks the pack from the subject. The pack sets the
  page frame, cover, chapter openers, accent colour and box styles. NEVER
  carry one pack's look into another subject. Full pack specs:
  `references/style-packs.md`.
- `SIZE`: `large` (default) or `compact`.
- One-off overrides in chat: "dark theme", "no cover", "mini", "no GATE tags".

---

## WHAT THE OUTPUT IS

- Exactly ONE file per run, covering ONE source / topic.
- Real selectable text. Vector shapes and diagrams. Embedded fonts.
- Reads like a textbook: numbered chapters and sections, numbered figures,
  tables and listings, definitions, worked examples, chapter summaries,
  review questions, glossary.
- Information is **simple, accurate and checkable**. Every fact, formula,
  bound and code listing must be correct. Do not guess. If the source and
  your knowledge disagree, say so in the chat reply and follow the source
  unless it is clearly wrong.
- Page count stays inside `PAGE_BUDGET`. If the source is bigger, say so
  and suggest splitting.

---

## TEXTBOOK STRUCTURE (full mode)

```
1.  Cover
2.  About this book (who it is for, what to know first, how chapters are
    built, how to read the figures, what GATE tags mean)
3.  Contents (chapters + numbered sections + page numbers)
4+. Chapters (1, 2, 3 …), each with an opener, content, summary, review
    questions, then Learning in Action + Practice + Answer key once at the end
    of the last chapter (or one per chapter in a long book)
    Mind map
    Quick reference
    You learned how to
    Glossary and references
    So, what is next? (closing page)
```

### Every chapter has, in this order

1. **Chapter opener**: the full-page layout from UNIVERSAL LAYOUT, drawn in
   the STYLE PACK. The learning objectives live ON the opener ("In this chapter you
   will learn to", 4 icon rows on the right). There is no separate objectives block.
2. **Numbered sections** (1.1, 1.2, …). Short headings, plain words.
3. Blocks from the BLOCK MENU below.
4. **Review questions**: 2 per chapter, each with the answer printed directly under it.
5. **GATE corner(s)**: only when verified. Put it inside the section it belongs to,
   or right after the review questions when it covers the whole chapter.
6. **Chapter summary**: 3–5 bullets, green box, the LAST thing in the chapter.
   Order is fixed: review questions -> GATE corner -> chapter summary.

A chapter may span several pages. A section never starts at the very bottom
of a page. Leave a little empty space rather than cram.

### Numbering rules

- Sections: `1.1`, `1.2`. Chapters: `Chapter 1`.
- Figures, tables, listings and examples are numbered per chapter:
  `Figure 2.1`, `Table 3.2`, `Listing 2.1`, `Example 1.1`.
- Captions: table and listing captions go ABOVE; figure captions go BELOW.
  The label is bold, the text is muted.
- Cross-refer by number ("see Section 4.1"), never "above" or "below".
- The Contents page lists chapters and sections with real page numbers.
  Compute them from the final page order; never type them by hand.

---

## SUBJECT TYPES (one template, every subject)

Pick blocks by what the SOURCE contains, not by the subject label.

| Subject type | Core teaching sequence inside a section |
|---|---|
| maths | Definition → Intuition picture → Formula box → Worked example (numbered steps) → Slip (wrong step → right step) |
| programming | Plain statement → Simple picture → Diagram (memory / flow) → Listing → Trap (buggy snippet → fix) |
| dsa | Idea → Simple picture → Trace (figure with state after each step) → Listing → Complexity → Trap |
| theory (OS, DBMS, networks, TOC …) | Definition → Analogy → Diagram (layers, state machine, ER, timeline) → Comparison table → Small example → Trap |
| mixed | Combine; never force a block the source cannot support |

### Block menu

1. **Plain statement**: one or two sentences. Bold the key term the first
   time it appears.
2. **Definition box**: notched card with a "Definition" ribbon. Exact,
   learn-by-heart wording.
3. **Worked example box**: header band "Example 2.1 · title", then every step.
4. **Figure**: from the SHAPE LIBRARY (see `references/page-recipes.md`),
   numbered, with a caption.
5. **Listing**: highlighted code, line numbers, numbered caption, and a short
   "line by line" table when the code is more than 8 lines.
6. **Formula / recurrence box**: notched card with a ribbon, real typeset math,
   one plain sentence about what it means.
7. **Table**: numbered, captioned.
8. **Simple picture** (amber): an everyday comparison. One per topic.
9. **Note / Tip** (teal / blue): something to remember.
10. **Trap (Wrong → Right)**: the mistake people really make, shown as wrong
    and right versions with a one-line reason. The "version" can be a line of
    code, a line of algebra or a claim.
11. **Historical note** (amber): only if verified (see ACCURACY).
12. **GATE corner**: see GATE TAGGING.

---

## ACCURACY RULES (a textbook must be right)

- Prefer standard definitions and standard notation.
- Check every number you print: recompute worked examples, bounds and
  traces step by step before you write them.
- State assumptions ("assume increasing order", "assume 32-bit int").
- Say "at most", "about" or "up to" when that is what is true.
- Historical or real-world claims (dates, names, incidents) need a source
  you actually looked up. Put it under References. If you cannot verify it,
  leave it out.
- Do not invent theorems, APIs, results, or past exam questions.
- If the source came from OCR, restore superscripts, fractions, Greek letters
  and arrows. Flag uncertain reconstructions in the chat reply, never inside
  the PDF.

---

## WRITING RULES

Write like a clear human teacher. Simple words, short sentences, one idea at
a time. Explain *why*, not just *what*.

**Do**
- Start with the thing itself.
- Keep one metaphor per topic and stay with it.
- Say what each symbol means the first time it appears.
- Use the same name for the same thing everywhere (lo, hi, mid; not "left",
  "start", "low" in other places).

**Do not**
- "In this section we will explore…", "It is important to note that…"
- "Delve", "leverage", "robust", "comprehensive", "seamless", "empower"
- "Moreover", "Furthermore", "In conclusion"
- Exclamation marks, hype, or marketing language.

---

## DESIGN SYSTEM

### Theme tokens (light — default)

```
Page:           #ffffff
Card:           #f4f6fb
Card-2:         #e9edf6
Border:         #d3d9e6
Text primary:   #10131a
Text body:      #2a2f3b
Text muted:     #667085
Pack accent:    from the STYLE PACK (dsa: #1a64d8)  (headings, section numbers, pills)
Pack dark:      from the STYLE PACK (dsa: #0f1b33)  (opener panel, status bar)
Highlight:      #fff176   (title highlight bar on the cover only)
Blue:           #1a64d8
Teal:           #0e8f80
Purple:         #6b46d6
Red:            #d1342a
Amber:          #b06f00
Green:          #17803d
Code bg:        #f3f5fa
```

Dark theme: near-black page (#0b0b0d), same hues lifted for contrast.

### Typography (Google Sans) — LARGE and ROOMY

- Body **12 pt**, line-height **1.65**. Bold = Google Sans Bold. No faux bold.
- Chapter title 32 pt bold. Section heading 17 pt bold, number in the PACK ACCENT colour (never a fixed green).
  Sub-heading 13.5 pt.
- Captions 10 pt muted. Ribbons / labels 8.5–9 pt, uppercase, tracked.
- Code: Google Sans Code 10.5 pt, line-height 1.6, ligatures OFF.
- Text inside diagrams: minimum 9 pt at print size.
- Spacing scale: paragraph gap 10 pt; gap before a section heading 26 pt,
  after it 10 pt; box padding 16–18 pt; gap between a box and the next block
  18 pt. Page margins 20 mm sides, 22 mm top and bottom.
- **Fewer things per page.** If a page holds more than one big figure plus one
  box plus text, move the last item to the next page. White space is part of
  the design. The page count is set by PAGE_BUDGET only.
- Running header and footer: from the STYLE PACK.

### Boxes and callouts

- Left accent bar (3 pt) plus a very light tint of the accent colour.
- Note → teal. Tip → blue. Simple picture / Historical note → amber.
  Trap → red. Summary → green. Objectives → blue outline card.
- Definition and formula boxes use the notched-corner card with a ribbon.

### Code highlighting (light)

```
Keyword #7b3fe4 bold   Type #0b7f73   Function #1a62d6   String #137333
Number  #b45f06        Comment #7a8294 italic   Operator #b0136a
```

### Maths

- Typeset with KaTeX / MathJax / LaTeX. Vector output.
- Never leave a formula without one plain sentence on what it does (except on
  pure reference pages).

---

## UNIVERSAL LAYOUT (every subject, every pack)

These are subject-neutral. Keep them in all packs:

- **Large and airy**: 12 pt body, generous spacing, fewer items per page.
- **Chapter opener = full page, in EVERY pack** (never a banner across the top of a content page): dark panel on the left (about 55 %) with a
  "Chapter n" tab, big title, rule and lead; objectives as icon rows on the
  right; big chapter number at the bottom of the panel.
- **Step pills** ("Step 1", "A", "B", "C") for procedures and proofs.
- **Learning in Action** spread near the end: Fun Facts + Did You Know (verified
  facts only), Find Errors cards with "Find the error / What's wrong / Fix it"
  lines, an Assessment Question.
- **Practice set**: one card per problem, numbered badge, tag pill (TRACE,
  GATE-STYLE, FIND THE BUG, SOLVE …), ruled "Your working" lines, NO answers on
  these pages. Separate **Answer key** pages, same numbering. Each question page
  says "Answers are on page N" (computed).
- **Closing pages**: "You learned how to" (six icon rows) and "So, what is
  next?" (full-colour page, three icon rows, one closing paragraph). Content
  must be true for the topic.
- **Cover recipe** (layout only): big three-line title with the key word
  highlighted, a small series tag above it, a solid subtitle bar below it,
  two or three small "preview" cards at the bottom edge that show REAL content
  from the book (a figure, a formula, a code snippet), a thin spine strip on
  the left. The decoration around it comes from the STYLE PACK.

**Never copy spreadsheet chrome** (search-bar strip, column letters, cell
grid, row numbers, sticky notes, hatched footer) unless `STYLE_PACK:
spreadsheet`, i.e. the notes are about Excel or Sheets themselves.

---

## RUN PLAN (mandatory: this is what keeps a run inside the limits)

Build the book in stages. Do not write layout code from scratch each run, and do not wait for a perfect page.

1. **CONTENT.** Read the source once. Write `content.md`: chapters, sections and blocks (plain text with block tags), no CSS, no layout.
2. **BUILD.** Copy `assets/build_slice.py`, `assets/book.css` and
   `assets/mathrender.js` into the project and extend, or write `build_book.py`
   once from them (they read `content.md`-shaped data and are the proven
   working harness). Install fonts once into `./fonts` / `./node_modules` and
   reuse them. More than 4 chapters: build in batches, one batch per message,
   and say which batch is done.
3. **CHECK.** Run `assets/preflight.py` on the PDF (add `mini` or `slice` as
   the second argument for mini books / partial slices). View only the pages it
   flags, plus ONE contact sheet (8 pages per image) that covers the cover,
   one opener, one listing page and one flowchart. Never view every page one by one.

Limits:
- At most 2 rebuild loops. After that deliver the file and list what is still wrong.
- GATE tags: one batch of at most 3 web searches for the whole book, or `GATE_TAGGING: off`. Never tag from memory.
- Do not ask for a reference PDF. Everything the reference showed is written in this skill.
- If a run is about to hit its limit, save content.md, the build files and the PDF so far, and say which stage is done.

---

## REQUIRED PAGES (nothing may be merged, shrunk into a banner, or dropped)

A full-mode book contains ALL of these, each on its own page(s), in this order:

```
Cover → About this book → Contents →
for each chapter: Opener (full page) → content → Chapter summary → Review questions
last chapter ends with, numbered and listed in Contents:
   x.1 Five common mistakes   x.2 Learning in action   x.3 Practice set   x.4 Answer key
   (Find errors and the Assessment question sit on the second page of x.2, under its heading)
Mind map → Quick reference → You learned how to → Glossary and references →
So, what is next? (closing page)
```

- If the topic is too small for this list, use `TEMPLATE_MODE: mini`. Do not silently drop pages.
- "You learned how to" and "Next steps" are separate pages. Quick reference and Glossary are separate pages.
- Every numbered heading appears in Contents with its real page. x.2 Learning in action carries its number on its FIRST page.

---

## LAYOUT FLOW RULES (what a human typesetter would never allow)

1. **Keep with next.** A heading, its lead sentence and the first block under it (figure, table, listing or at least 3 lines of text) stay on the same page. A heading is never the last thing on a page.
2. **Caption stays with its figure, table or listing.**
3. **Define before you use.** A Definition box comes immediately after the sentence that first needs it, never after the table, figure or picture that uses the term.
4. **A box stays next to the paragraph it belongs to.** A Note about section 2.2 may not appear under the heading of 2.3.
5. **Page fill.** Aim for 70–90 % of each page used. If a page ends under 60 % full and the next block is a large figure, shrink the figure (max 55 % of the page height) or move text from the next page up. At most 15 % of pages may be under 60 % full (openers and the closing page excluded). This is a warning, never a reason to rebuild.
6. **No tiny tail pages.** A table or list that splits must leave at least 4 rows on each page, or move whole.
7. **No repeated content.** Practice problems, Find-errors items and Quick-check questions must be NEW. They may not repeat a Common-mistakes card or each other.
8. **Contents and cross-references are read back from the finished PDF** (heading text → page number), then written in. Never typed by hand.

---

## FIGURE AND FLOWCHART RULES

- Every arrow ends in a small arrowhead (at most 2 mm) exactly on a node. Branch labels (YES / NO) sit beside the arrow, never on the arrowhead.
- **Flowcharts must be logically correct.** Check each path against the code or the algorithm. Every branch that returns to a loop must join the loop-back line; it must NOT run into another step box (for example, `lo = mid + 1` and `hi = mid - 1` are alternatives, not a sequence).
- Text inside diagrams is at least 9 pt at print size. Index numbers under array cells too.
- A figure may be at most 55 % of the page height. A trace of more than 4 steps goes on its own page.
- Show the rule you used. A Master-theorem box states the case ("f(n) = Θ(n^(log_b a)) ⇒ T(n) = Θ(n^(log_b a) log n)") before it shows the result.

---

## FONT AND SYMBOL RULES

- Only three font families may appear in the PDF: Google Sans, Google Sans Code, and KaTeX (maths). No Inter, no Liberation, no DejaVu, no Type 3 text fonts.
- Google Sans has no glyphs for many symbols (→ ≤ ≥ ≠ ₂ ⁹ Θ ⌊ ⌋ ∞ ∑ and similar). Never let the browser fall back to another font. Instead:
  - in running text and tables, write the symbol with inline KaTeX (`$\le$`, `$\log_2 n$`, `$2^9$`);
  - in code listings and inline code, use ASCII (`<=`, `>=`, `->`);
  - in SVG labels, use ASCII or words.
- Listings are 10.5 pt (line numbers 9 pt or more). Body text is 12 pt. The only text under 9 pt is decoration on the cover.

---

## PRACTICE AND FIND-ERRORS RULES

- Learning in Action: Fun Facts and Did You Know. Every fact is verified and keeps its source name inline (for example "(Bentley, Programming Pearls)"). The fact list may not copy the Historical note.
- Find errors: 2 items, each a new snippet or claim. Each card has the lines "Find the error", "What's wrong", "Fix it". Answers go only in the Answer key.
- Assessment question: one longer task with a "Task" label.
- Practice set: one card per problem, numbered badge, tag pill, "Your working" lines, no answers on these pages. Exactly 8 problems, ordered warm-up -> core -> exam-style, each with a tag pill (TRACE, GATE-STYLE, FIND THE BUG, SOLVE, COMPARE). Answer key uses the same numbers, and each question page says "Answers are on page N".

---

## GATE TAGGING

Controlled by `GATE_TAGGING`. Tags appear in the PDF, small and honest. This
is designed for GATE (India) syllabi; set `GATE_TAGGING: off` for any other
exam system or none.

**Verification (mandatory)**
- Before tagging a chapter, run 2–3 web searches to check (a) which syllabus
  section it belongs to, and (b) real past-year appearances.
- Never invent a year, paper, set or marks value. If it cannot be verified,
  tag the syllabus section only and leave out years.
- Name the paper correctly. GATE CS/IT is not GATE DA.

**Where tags go**
- One pill in the chapter opener that NAMES THE PAPER, in the form `GATE CS · <SYLLABUS SECTION> · <TOPIC>` (for example `GATE CS · ALGORITHMS · SEARCHING`; other papers: `GATE XE-A · ENGINEERING MATHEMATICS`). A bare "GATE" is not allowed, because the syllabus differs by paper. Verify the topic against that paper's own syllabus. Chapters with no GATE link get no pill.
- A "GATE corner" box near the end of a chapter, only when real appearances
  were verified: year, paper, marks, and what the question tested. Describe
  the pattern; do not copy the question.
- Practice problems: `GATE-style` if you wrote them; `GATE <year> · <marks>`
  only if it truly is a past question.
- No tags on chapters with no GATE link. No badge on every page.

**In the chat reply**
- List what was searched, what was verified, and anything you could not confirm.

---

## REFERENCES

The last page carries a short numbered References list of the sources you
actually used (books, papers, official syllabus, past-question archives).
Nothing you did not read.

---

## BUILD METHOD

```
PDF:
- HTML/CSS -> PDF with WeasyPrint: `pip install weasyprint brotli --break-system-packages`.
  Use Playwright only where `playwright install chromium` already works.
  Tested WeasyPrint rules (each one fixed a real failure):
  - Font and KaTeX CSS must use `url(file:///abs/path/...)`. A plain absolute path silently falls back to Inter / Latin Modern.
  - Inline SVG ignores the page font: put `font-family="Google Sans"` on every `<svg>` tag.
  - Cover and chapter opener use named pages: `@page cover{margin:0}` `@page opener{margin:0}`, with the page div 296 mm tall (297 mm adds a blank page).
  - Opener and cover text is letter-spaced, so look up its page by the TITLE text, never by the tracked label, when filling Contents.
  - Ribbons sit INSIDE the box corner (`top:0;left:0`). A ribbon above the box is clipped at the top of a page.
  - `break-after:avoid` on headings AND on the lead paragraph under them, or the heading is stranded.
  - KaTeX: render with node (output:'html', one batch for all formulas), then substitute into the HTML. Use `assets/mathrender.js`.
  - Fonts show as `Google-Sans`, `Google-Sans-Bold`, `KaTeX_*` in the PDF. That is correct.
- Fonts: install Google Sans and Google Sans Code from the open-source
  Fontsource packages (@fontsource/google-sans, @fontsource/google-sans-code),
  load them with @font-face, confirm they are embedded in the PDF.
- Shapes and diagrams as inline SVG, scaled to the column (max-width 100%).
- Math with KaTeX (server-side render). Code with a small tokenizer mapped to
  the colour table above, ligatures off.
- Build each page as a fixed A4 block. Measure free space at the bottom of
  every page and rebalance content until nothing overflows.
- Table of contents page numbers are computed from the page list.

PREFLIGHT (run before delivery; a FAIL means rebuild, not "mention it"):
- python3 assets/preflight.py <Topic>_Notes.pdf    (add `mini` or `slice` as a second argument for mini books / partial slices)
- It checks: required pages present, chapter openers are full pages, GATE pill names the paper, A4 size, only Google Sans / Google Sans Code / KaTeX fonts, body 12 pt,
  listing size, page budget, pages under 60 % full, headings stranded at the bottom of a page, and Contents page numbers against the real heading pages.
- Then do the checks a script cannot do, by looking at the flagged rasterised pages:
  flowcharts are logically correct, Definition comes before first use, no heading
  is separated from its figure, no repeated questions, cover and openers match
  the chosen STYLE PACK (use the pack checklist), no overflow or cut-off text.
- Recompute every number in worked examples and answers.
- Check every GATE tag (paper named, syllabus checked) and every historical claim against its source.
- Paste the preflight result into the chat reply.
- Fix before delivery.
```

The worked example `assets/build_slice.py` shows every hard-won detail in
code: the two-pass build that fills Contents page numbers from the rendered
PDF (`find_pages` + rebuild), the `@@i@@` placeholder round-trip through
`mathrender.js`, named cover/opener pages, hexagon badges, step pills,
notched definition cards with ribbons, and the `font-family` fix on every
`<svg>` tag. Start from it instead of writing a harness from scratch.

---

## DELIVER

- Files: `<Topic>_Notes.pdf` (or .pptx), plus `content.md`, `build_book.py`, `book.css` so the next run can reuse them.
- Chat reply, kept short: what was covered, page count, the preflight result, GATE sources checked
  and anything unverified, historical claims and where they came from, any
  OCR / math reconstructions that need a human look. None of that goes
  inside the PDF except the References page.

---

## STYLE TARGET (read this when unsure)

The finished PDF should feel like a page from a good university course book:

- Calm, white, well-spaced, easy to scan.
- Clear numbering, clear boxes, one idea at a time.
- Figures that teach, with shapes that mean something.
- Language a first-year can follow without a dictionary.
- Enough structure to revise from (summaries, mind map, quick reference,
  glossary) without re-reading every chapter.

If a page looks like a slide, a poster or a chatbot essay, rebuild that page.
If a page feels crowded, split it. Bigger type and more air beats more content.
