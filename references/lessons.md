# Lessons learned

Corrections from real runs. Read before a build; add to it after a correction.
A lesson seen three times should be promoted into SKILL.md or a script.

| Lesson | Why it matters | Seen |
|---|---|---|
| Diagram text must be at least 12 pt at print size; SVG `font-size="9"` is ~7 pt on paper | A judge called it unreadable | 3 (promoted to taste-system.md) |
| Strip direction must match the inner differential: vertical for `dy`, horizontal for `dx`, radial for `dr` | Four of seven figures were wrong | 3 (promoted to page-recipes.md) |
| Never violet or lavender; one teal accent, 90% neutral | The taste system's first rule | 2 |
| Labels are sentence case, never tracked capitals | Tracked ribbons read as template styling | 2 |
| Do not hand-type Bezier control points for a curve labelled with a formula; sample the function | Curve and markers disagreed | 2 |
| An example without a visible Check interpolation leaks literal `+ '` text into the PDF | A real bug in the f-string structure | 1 |
| Keep a machine-readable `TOCMAP` anchor; regex over reflowed flex Contents text is unreliable | The old cross-check produced notes, not verification | 2 |
| Two-pass Contents must skip every Contents page, not only the first | A two-page Contents created six false FAILs | 1 |
| Preflight PASS is structural, not mathematical; run `verify_math.py` and look at the page | Compilation is not fidelity | 3 (promoted to ACCURACY RULES) |
| A full chapter on this source needs seven chapters; the topic list lives in `topic-map.md` | Earlier builds omitted Jacobians and centre of mass | 1 |
| The opener label can be reordered by text extraction; match `INTHISCHAPTERYOUWILL`, not the full phrase | A false "no chapter opener" FAIL | 1 |
| Equal edges: 22 mm on all four sides | Unequal margins read as a template default | 2 |
| Every worked example carries Given, its own diagram, Method, ladder, boxed answer and Check | The user's explicit requirement | 3 (promoted to SKILL.md) |

## How to add

Append a row with the correction, the reason and `seen = 1`. If the same
correction appears again, increment rather than duplicating. At three, move the
rule into `SKILL.md`, a reference or a check in `preflight.py`.
