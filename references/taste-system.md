# The taste system

This template follows one visual system for every subject pack. It is adapted
from `design-taste-frontend` (`system.md`, `cards.md`, `copy.md`): 90–95 % of a
page is neutral, one accent does all the structural work, and colour carries
meaning rather than decoration. A page should look like a well-made book, not
a slide deck or a chatbot reply.

## Tokens

| Role | Value | Where it appears |
|---|---|---|
| Page | `#ffffff` | every page |
| Surface | `#f5f6f4` | cards, tables, practice tiles |
| Ink | `#14181b` | body text, headings, dark panels |
| Muted | `#66717a` | captions, labels, running heads |
| Hairline | `#dfe3e0` | borders, rules, leaders, strip lines |
| Accent | `#0d6d78` | section numbers, rules, links, small marks |
| Error | `#b3392e` | wrong steps, common slips, find-the-error |
| Result | `#1f7a4d` | boxed answers, chapter summary, checks |
| Radius | 6 pt | every card and panel |
| Margins | 22 mm | all four sides — equal edges |

**Never violet or lavender.** No `#6b46d6`, `#3b3fa8` or similar. Do not
introduce a second accent, a second radius, or a second card style.

## Typography

- Google Sans only (plus Google Sans Code for listings and KaTeX for maths).
- Weights 400 and 700. Display tracking −0.03 em; headings −0.02 em.
- Body 16 pt / 1.65. Captions and labels 12–13 pt. Diagram text ≥ 12 pt.
- Sentence case everywhere. No tracked capitals, no small caps, no marker
  highlights behind words. A number never breaks from its unit.
- One size per kind of element: every section heading is 23 pt, every figure
  caption 13 pt, every card label 12 pt.

## One card recipe

Every box — definition, slip, note, Given, Method, Check, practice card, fact
card — uses the same surface fill, hairline, radius and padding. The only
difference is a 3 pt left rule and a small label in the matching role colour.
Never nest a card inside a card. Never use a notched corner, a ribbon tab or a
stack of coloured chips as a legend.

## Structure and rhythm

- Equal left and right edges: content sits on the same column on every page.
- One idea per page. Leave air rather than cram; more pages is acceptable.
- A heading stays with its lead paragraph and first block.
- A worked example starts a fresh page after the first one in a section and
  carries its own diagram, Given, Method, step ladder, boxed answer and Check.
- Figures are sampled from their definitions; the strip direction matches the
  inner differential; labels are legible and never overlap.

## Prohibited

Grid-paper backgrounds, decorative hexagons, six-colour legends, uppercase
tracked ribbons, faux bold, a coloured bar behind a word, a caption that
explains an image, a card that fades in, and any colour that is not a token
above. A real third-party logo keeps its own colours — this template has none.

## Why

A disciplined neutral system makes the mathematics the only colour. The
effect is a book that reads like a university text rather than a template:
quiet, exact, and easy to revise from.
