# Reconstructing mathematics from a lecture source

Adapted from `pdf2tex` (Calix-L/awesome-latex-skills) for this book's OCR and
lecture-transcript workflow. The goal is a correct book, not a confident guess.

## Separate four things

1. **Extraction** — text and glyphs actually present in the source file.
2. **OCR** — machine reading of an image or scan; plausible but fallible.
3. **Reconstruction** — the LaTeX/KaTeX we write from that evidence.
4. **Verification** — the checks we run on the finished PDF.

Never present (3) as if it were (1). A clean KaTeX render proves syntax, not
mathematical fidelity. Preflight PASS is not proof that a restored symbol is
right — that needs the recomputation in `verify_math.py` and a visual look.

## Keep an evidence ledger

For every symbol, limit or result that was uncertain, record:

| Source page | Item | What was read | Candidate readings | Resolution | Checked how |
|---|---|---|---|---|---|
| `one_part1.md` p.22 | inner limit | `√(a²−y²)` | `√(a²−y²)`, `a²−y²` | `√(a²−y²)` | recomputed to `πa³/6` |

Keep this beside the book (`content.md` is a good home). Report unresolved
items in the chat reply, never inside the PDF. A hidden comment alone is not
enough: the reader must be told what remains uncertain.

## Glyph candidates, not a dictionary

A glyph or font name does not identify the author's original command. Verify
against the surrounding mathematics:

| Visible | Common reading | Watch for |
|---|---|---|
| ε / ϵ | `\epsilon` / `\varepsilon` | variant conventions; match the glyph |
| φ / ϕ | `\phi` / `\varphi` | same |
| ≤ ≥ ≠ ≈ | `\leq`, `\geq`, `\neq`, `\approx` | do not substitute ≈ for = |
| ∈ ⊂ ⊆ | `\in`, `\subset`, `\subseteq` | strict vs non-strict |
| ∥ | `\parallel` only as a relation | paired norm bars need `\lVert … \rVert` |
| ∫ ∑ | `\int`, `\sum` | limits, scope, display style |
| named operators | `\sin`, `\log`, `\lim` | upright operator, not italic product |

## Recover grouping before typesetting

- `a_ij` subscripts only `i`; `a_{ij}` subscripts both. Brace multi-character
  scripts explicitly.
- `\frac{a+b}{c}` has both terms above the bar; `a+\frac{b}{c}` does not.
- A horizontal stroke may be a minus, a fraction bar, an overline or a table
  rule. Check its extent before generating `\frac`.
- Preserve matrix dimensions, empty entries, delimiters and case conditions.
  Do not replace an ambiguous symbol with a more familiar formula.

## Common OCR damage and its repair

Adapted from `claude-latex/references/ocr-reconstruction.md`:

| OCR gave | Usually means |
|---|---|
| `x2`, `e x`, `a n` | x², eˣ, aⁿ — lost elevation |
| `xn`, `a1` in a sequence | xₙ, a₁ — flattened subscript |
| `ab` where a ratio is expected | a/b — lost fraction bar |
| `J`, `f` before `dx` | ∫ |
| `E`, `Z` before an index range | Σ |
| `TT` in a trig context | π |
| `oo`, `00` as a limit | ∞ |
| `->`, `<=`, `>=`, `!=` | →, ≤, ≥, ≠ |
| `lim x→0 f(x)` on one line | lim with subscript x→0 |

Repair only when the surrounding derivation makes the reading clear. If both
readings are plausible, choose the standard one and report the alternative in
chat. Never "fix" an unusual but valid expression. Never drop a figure or a
formula silently: redraw what the surviving labels establish, or report the gap.

## Nothing about the process goes in the PDF

The following must never appear as visible text: "reconstructed", "typeset by",
"clarity improved", "AI-generated", "as the source", "in the source", "LLM",
"ChatGPT", "Claude", "presumably", "unverified claim". `preflight.py` checks
these phrases. Audit or method notes belong in the chat reply, not the book.

Colour is styling only: it never adds words. Use at most three or four
emphasised elements per page, and keep one meaning per colour everywhere.

## Verification sequence

1. Recompute every printed result with `verify_math.py` — numerically here,
   and by hand where a numeric check cannot resolve a symbolic claim.
2. Compare the rendered page with the source for glyphs, scripts, grouping,
   limits and line breaks. A matching page count proves nothing.
3. Run preflight for size, fonts, pages and structure. Treat it as a structural
   gate only.
4. State what could not be recovered and what remains unverified.

## What we do differently from pdf2tex

That skill reconstructs editable LaTeX source from a PDF and uses a real TeX
compiler. This skill builds a final PDF from OCR/lecture notes with WeasyPrint
and KaTeX. The shared principle is the same: **evidence first, uncertainty
visible, compilation is not verification.**
