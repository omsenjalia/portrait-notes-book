# Subject Style Packs

The pack decides how the book LOOKS. Pick by subject; do not mix packs unless
`mixed`. Pack choice (do this first, before any layout work): read the topic.
Code, algorithms, data structures, complexity -> `dsa`/`programming`
(code-editor look). Calculus, algebra, probability, proofs -> `maths`
(graph-paper look). OS, DBMS, networks, TOC -> `theory`. Excel/Sheets itself
-> `spreadsheet`. Table header bands, section numbers, pills, ribbons, page
numbers and the closing page all use the PACK ACCENT, so a dsa book is blue
and a maths book is deep teal; nothing is green by default.

---

## Pack: dsa / programming (code-editor look)

- **Accent**: blue `#1a64d8`; dark panels navy `#0f1b33`; light tints of blue.
  Role colours come from `references/taste-system.md`: accent teal, error red, result green.
- **Page header**: editor tab bar. Three small window dots, an active file tab
  (e.g. `binary_search.c`, blue underline), then a muted breadcrumb in
  Google Sans Code: `binary_search › Chapter 2`. No grid, no ruler.
- **Footer**: slim navy status bar with the book title (left or right) and
  `pg N` in Google Sans Code, thin blue line above it. No hatching.
- **Chapter opener**: navy panel with a line-number gutter down its left
  edge, tab styled like an editor tab, title in white with the key word in
  light blue.
- **Cover**: an editor window. White page, three-dot title bar with file
  tabs, a line-number gutter down the left, one highlighted code line near the
  top, 2 grey `// comment` lines in place of sticky notes (one is a question
  the reader has, one is a tag), series tag box, big title, navy subtitle bar
  that starts with `$`, bottom preview cards: a trace of the algorithm, a
  growth curve, a code snippet.
- **Blocks**: Listing (line numbers, tinted code card), Trace figures,
  Complexity pills, Trap (Wrong → Right) cards, Definition (notched blue).
- **Practice flavour**: trace, find the bug, complexity, write-the-function.

See `examples/Binary_Search_Notes.pdf` in this skill for a finished book in
this pack.

---

## Pack: maths (graph-paper look)

- **Accent**: deep teal `#0d6d78`; dark panels `#14181b`; light accent text on dark `#9fb7ba`. Error red only for wrong steps, result green only for answers and checks.
- **Page header**: thin ruled strip, chapter name left, section number and title right, one hairline under the header; no grid.
- **Footer**: thin rule, `<Book title>` left in muted text, page number centred in a small circle.
- **Chapter opener** (FULL PAGE, its own page): the dark panel fills the LEFT 55 % of the page from top to bottom, with a single quiet curve
  a single quiet curve. On the panel, top to bottom: a "Chapter n" tab chip, the title at 32 pt white with the key word in light
  light accent, a short rule, a two-line lead in white, the GATE pill, then one large KaTeX formula (white, 40–48 pt) and a ring badge with the chapter number at the
  bottom. The RIGHT 45 % is white: the label `IN THIS CHAPTER YOU WILL LEARN TO`, then 4 rows, each a ring icon badge plus one objective line. Same
  geometry as the dsa opener, only the decoration differs.
- **Cover**: graph-paper background, x/y axes with one real curve from the topic, the main formula set large, series tag `ENGINEERING MATHEMATICS · STUDY NOTES`,
  three-line title with the key word highlighted, subtitle bar, one plain sentence, three preview cards: a worked example, a graph, a formula or test card.
  (A plain white cover with a formula card is NOT the maths cover.)
- **Blocks**: Theorem / Definition / Formula (notched cards with ribbon), Proof (Step pills A, B, C, ending with a QED square), Worked example with numbered
  steps and the Example chip, "Common slip" (red card: wrong line -> right line), Intuition picture (surface card).
- **Practice flavour**: cards with a tag pill (SOLVE, PROVE, FIND THE SLIP, GATE-STYLE, COMPUTE), a number badge and a big YOUR WORKING area (at least 5 ruled lines or a small grid box).

See `assets/build_slice.py` + `assets/book.css` and
`examples/Infinite_Series_Slice_Test.pdf` for a working build and output in
this pack.

---

## Pack: theory (OS, DBMS, networks, TOC …)

- **Accent**: teal `#0e8f80`; dark panels `#0f2a2e`.
- **Page header**: a layer-tab strip (small stacked-rectangle icon + chapter
  name). Footer: thin teal rule, page number in a rounded square.
- **Cover**: layered-stack drawing (real layers of the topic), title, bar.
- **Blocks**: diagram-first (layers, state machines, ER, timelines),
  comparison tables, analogy boxes, "Exam trap" cards.

---

## Pack: spreadsheet (ONLY for Excel / Sheets notes)

- The spreadsheet-window look: spreadsheet-window cover with yellow sticky
  notes, search-bar strip, column ruler, hatched footer, green accent.
- This chrome is FORBIDDEN in every other pack.

---

## Pack: mixed

- Use the pack of the dominant subject for the frame and cover; borrow single
  blocks (for example a Proof from maths) without changing the frame.
