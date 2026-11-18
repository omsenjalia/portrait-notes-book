# Page Recipes, Shape Library and Pill Inventory

Load this file when drawing any page, figure or diagram. The decoration comes
from the STYLE PACK (`references/style-packs.md`); the layout recipes here are
subject-neutral.

---

## PAGE RECIPES

- **Header and footer** (every page except the cover): from the STYLE PACK. dsa: editor header (three dots, active tab `<file>.c`,
  breadcrumb `<book> › About | Contents | Chapter N | Mind map | Quick reference | Summary | Glossary`), footer `<Book title> — Study Notes`
  left and `pg N` right in Google Sans Code. maths: see its pack. The cover is page 1 and has no footer.
- **Cover skeleton** (all packs): series tag, small `STUDY NOTES ON`, three-line title with the key word highlighted, subtitle bar,
  one plain sentence, three preview cards that show REAL content from the book. dsa decoration: file-tab bar, line-number gutter,
  one highlighted code line, two grey `//` comments, subtitle bar starting with `$`, cards labelled `trace.sheet`, `growth.plot`, `search.c`.
  maths decoration: see its pack.
- **Chapter opener** (all packs): ALWAYS a full page of its own, with the next page starting the first section. Never a banner on top
  of a content page, never half a page. See the pack for the drawing.
- **About this book** (2 pages): intro paragraph; "What you should know first" (3 bullets); "How each chapter is built" table
  (BOX | WHAT IT GIVES YOU: Learning objectives, Definition, Example, Note/Trap/Simple picture, Chapter summary, Review questions);
  "How to read the figures" (the six shape chips) and the colour legend (teal main flow, blue data, purple rule or formula, red wrong
  or trap, amber picture or analogy, green right or result); "GATE tags" paragraph saying a tag marks an official-syllabus topic,
  a GATE corner lists verified past questions, and unconfirmed ones get the syllabus tag only.
- **Contents**: chapter rows in bold with page, section rows indented, then Mind map, Quick reference, You learned how to,
  Glossary and references, So, what is next?.
- **Tables**: header band with uppercase tracked column names. Table and listing captions above, figure captions below.
- **Common mistakes** (x.1; in maths called Common slips): one card per mistake: number + title, WRONG line, RIGHT line, one reason line. 3 cards then 2.
- **Learning in action** (x.2): page 1 `// LEARNING IN ACTION` (any pack: same heading text), FUN FACTS (2) and DID YOU KNOW (2). Page 2 `! Find errors`
  (maths: Find the slip) with 2 cards (Find the error / What's wrong / Fix it) and the TASK (Assessment question). "Answers are on page N".
- **Practice set** (x.3): intro sentence, one card per problem (number badge, tag pill, YOUR WORKING lines), closing Tip box. No plain numbered lists.
- **Answer key** (x.4): labels FIND ERROR 1, FIND ERROR 2, ASSESSMENT, PRACTICE 1 … 8 in the same order.
- **Mind map**: centre node plus five branches, 3–4 leaves each (dsa: Needs, Code, Speed, Traps, Variants; maths: Definitions, Tests or Methods, Formulas, Slips, Next).
- **Quick reference**: ITEM | MEANING table (maths: TEST | CONDITION | CONCLUSION) and one closing line in a pill. Its own page.
- **You learned how to**: six icon rows. Its own page. **Glossary**: TERM | MEANING, alphabetical, its own page(s), with the numbered References after it.
- **So, what is next?**: full-colour page in the pack accent, `// the end of the notes, the start of the practice` (maths: a one-line closing thought),
  one bold line, heading, three icon rows, one closing paragraph. Its own page.

### Pill and chip inventory (use all that apply; never plain text in their place)

- **GATE pill** on the opener, form `GATE <PAPER> · <SYLLABUS SECTION> · <TOPIC>` (never a bare `GATE ·`).
- **Tag pill** on every practice card (SOLVE, PROVE, FIND THE SLIP, COMPUTE, COMPARE, TRACE, FIND THE BUG, GATE-STYLE).
- **Step pills** (`Step 1`, `A`, `B`, `C`) on every procedure and proof.
- **Ribbon** on every Definition, Theorem and Formula card. **Example chip** `Example 2.1` in the worked-example header band.
- **Chapter-number hexagon** on the opener. **Value pill** for complexity (dsa) or a result value (maths).

### Things earlier builds got wrong. Do NOT copy these

- Heading 2.3 stranded at the bottom of a page with its flowchart on the next page, and a figure caption that repeats the lead sentence.
- Fun Facts and Did You Know repeating the Historical note word for word.
- Find errors and some Practice problems repeating Common mistakes cards.
- Learning in action missing its section number while Contents lists it.
- A few symbols falling back to Liberation fonts.
- A v7 maths build shrank every chapter opener into a half-page banner on top of a content page, dropped Common slips, Learning in action,
  Find the slip, the Assessment question, the Mind map and the closing page, merged Quick reference with Glossary, used a bare
  `GATE · Engg. Mathematics` pill, and printed the practice set as a plain list. All of these are required, see REQUIRED PAGES in SKILL.md. Use inline KaTeX or ASCII (see FONT AND SYMBOL RULES).

---

## SHAPE LIBRARY (the visual language)

Shapes carry meaning. The same shape means the same thing across the book.
Do not use a shape purely as decoration.

| Shape | Means |
|---|---|
| Rounded rectangle | A concept, component or step. The default node |
| Array cells (squares, index under each) | Arrays, memory, sequences, tape |
| Triangle under a cell | A pointer or index (lo, mid, hi, head, i, j) |
| Circle | Tree / graph node, or a numbered step badge |
| Diamond | A decision, with YES / NO branches |
| Parallelogram | Input / output |
| Pill (capsule) | A tag or chip: GATE, complexity value |
| Hexagon | The chapter-number badge on each chapter opener |
| Chevron | Stages in a process, left to right |
| Cylinder | Stored data: database, disk, file |
| Stack of rectangles | A stack, call stack, or layers |
| Curly brace | A group or range |
| Notched-corner card | Definitions, theorems, formula boxes |
| Ribbon | Small label on a card ("Definition", "Formula") |
| Axes + curve | Functions, growth rates, distributions |
| Number line | Intervals, ranges, inequalities |
| Overlapping circles (Venn) | Sets, relations |
| Tree | Recursion, hierarchy, parse |
| Table grid | Comparisons, truth tables, trace tables |
| Timeline bar | Ordered events, protocol steps |

Arrows: solid = flow, dashed = reference or optional, curved = jump or return,
double-headed = equivalence.

Colour by role: teal = main flow, blue = data, purple = rule / formula, red =
wrong or problem, amber = analogy, green = right / result.

Rules: every shape has a short label; diagrams stay readable at print size
(min 7 pt text in shapes); no textures, no fake handwriting, no heavy shadows,
no stock photos.
