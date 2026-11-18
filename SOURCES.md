# Source strings for References pages

Copy these verbatim into a book's References list. Do not retype citations in
the build script — a citation that lives in two places will drift.

## Historical claims (verify before first use; checked for the maths test book)

- Fubini, G. (1907), "Sugli integrali multipli," *Rendiconti della Reale
  Accademia dei Lincei*. Also summarised as "Fubini's theorem," Wikipedia.
  Used for: interchanging the order of integration for a continuous function
  on the region.

## Lecture sources (cite neutrally; no instructor branding)

- Source lecture notes: *Multiple Integral, Lectures 1–2 (OCR transcript)*,
  used for worked examples and problem statements.

## Assessment of the OCR source

- Superscripts, fractions and Greek letters in the transcript were restored
  before typesetting. Every printed numeric result was recomputed independently
  with `assets/verify_math.py`; uncertain reconstructions are reported in the
  chat reply, never inside the PDF.

## Rules

- Historical or real-world claims need a source actually read in the run. If
  it cannot be verified, leave the claim out.
- Add new verified citations here in the same format: exact title, venue, year,
  and the claim they support.
