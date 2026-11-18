"""preflight.py <notes.pdf> [full|mini|slice] — hard checks; exit 1 if any FAIL. Needs: pip install pdfminer.six

full  (default) = complete book: required pages + 36-54 page budget.
mini            = condensed book: required pages + 18-26 page budget.
                  (16 cannot hold the required page list plus one worked chapter.)
slice           = partial build (one chapter): skips the full-book page list and
                  budget; checks the core pages a slice must have instead.

Extraction engine: pdfminer.six (pure Python). Earlier versions used PyMuPDF,
but mupdf 1.28+ takes 4-10 s per page on WeasyPrint 70 output (pathological
font path), while pdfminer reads the same PDF ~100x faster on both old and new
WeasyPrint output. All checks and the CLI are unchanged.

Coordinates: pdfminer reports bboxes with the origin at the BOTTOM-left; this
script converts to top-origin (y grows downward) to match the layout rules.
"""
import sys, re, collections, warnings
warnings.filterwarnings('ignore')
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTContainer, LTTextLine, LTChar

mode = sys.argv[2] if len(sys.argv) > 2 else 'full'
fails = []; notes = []

def children(o):
    try: return list(iter(o))
    except TypeError: return []

def text_lines(page):
    """Yield every LTTextLine on the page (walks text boxes, figures, nests)."""
    stack = children(page)
    while stack:
        o = stack.pop()
        if isinstance(o, LTTextLine):
            yield o
        else:
            stack.extend(c for c in children(o) if not isinstance(c, LTChar))

pages = []
for pg in extract_pages(sys.argv[1]):
    W = pg.bbox[2] - pg.bbox[0]; H = pg.bbox[3] - pg.bbox[1]
    lines = []; chars = collections.Counter()
    for line in text_lines(pg):
        t = line.get_text()
        if t.strip():
            lines.append((t, H - line.bbox[3], H - line.bbox[1]))  # (text, y_top, y_bot)
            for ch in children(line):
                if isinstance(ch, LTChar) and ch.get_text().strip():
                    f = ch.fontname.split('+')[-1]
                    chars[(f, round(ch.size, 1))] += len(ch.get_text().strip())
    pages.append({
        'W': W, 'H': H, 'lines': lines,
        'text': '\n'.join(t for t, _, _ in lines),
        'chars': chars,
    })

n = len(pages)
if not n:
    print('FAIL no pages extracted (is this a valid PDF?)'); sys.exit(1)

H = pages[0]['H']; w = pages[0]['W']
if abs(w - 595.28) > 1.5 or abs(H - 841.89) > 1.5: fails.append(f'page size {w:.1f}x{H:.1f} pt is not A4')

# ---- font / size census (same semantics as the fitz version) ----
fonts, sizes, codes = collections.Counter(), collections.Counter(), collections.Counter()
for pg in pages:
    for (f, size), cnt in pg['chars'].items():
        fonts[f] += cnt
        if 'Code' in f: codes[size] += cnt
        elif not f.startswith('KaTeX'): sizes[size] += cnt
bad = {f: c for f, c in fonts.items() if not (f.replace('-', '').startswith('GoogleSans') or f.startswith('KaTeX'))}
if bad: fails.append(f'fonts outside Google Sans / Google Sans Code / KaTeX: {bad}')
body = sizes.most_common(1)[0][0]
if abs(body - 12) > 0.3: fails.append(f'body text is {body} pt, must be 12 pt')
if codes and codes.most_common(1)[0][0] < 10.4: fails.append(f'listing text is {codes.most_common(1)[0][0]} pt, must be 10.5 pt')

# ---- page budget ----
if mode == 'slice':
    pass
elif mode == 'mini':
    if not 18 <= n <= 26: fails.append(f'{n} pages, PAGE_BUDGET is 18-26')
else:
    if not 36 <= n <= 54: fails.append(f'{n} pages, PAGE_BUDGET is 36-54')

# ---- sparse pages + stranded section headings ----
sparse, orphans = [], []
for i, pg in enumerate(pages, 1):
    txt = pg['text']
    if i <= 3 or 'IN THIS CHAPTER' in txt.upper().replace('\n', ' ') or i >= n - 1: continue
    blocks = [(t, yt, yb) for (t, yt, yb) in pg['lines'] if yb < 0.93 * H and yt > 0.06 * H]
    if blocks and max(yb for _, _, yb in blocks) / (0.93 * H) < 0.6: sparse.append(i)
    for t, yt, yb in blocks:
        if re.match(r'^\d+\.\d+\s+\S', t.strip()) and yt > 0.80 * H: orphans.append(i)
if len(sparse) > 0.15 * n: notes.append(f'warning: {len(sparse)} pages under 60% full: {sparse}')
_runs, _cur = [], []
for _i in sparse:
    if _cur and _i != _cur[-1] + 1: _runs.append(_cur); _cur = []
    _cur.append(_i)
if _cur: _runs.append(_cur)
_long = [r for r in _runs if len(r) >= 3]
if _long: notes.append('warning: consecutive sparse pages (likely a pagination problem): ' + ', '.join(f'{r[0]}-{r[-1]}' for r in _long))
if orphans: fails.append(f'section heading stranded at the bottom of page(s) {orphans}')

# ---- Contents page-number cross-check ----
alltext = '\n'.join(pg['text'] for pg in pages)
ti = next((i for i, pg in enumerate(pages) if re.search(r'^Contents', pg['text'], re.M)), None)
if ti is not None:
    rows = re.findall(r'^(\d+\.\d+)\s+(.+?)\s+(\d+)\s*$', pages[ti]['text'], re.M)
    for num, title, pgno in rows:
        hit = [i for i, pg in enumerate(pages, 1) if i - 1 != ti and
               any(re.match(r'^' + re.escape(num) + r'\s+' + re.escape(title[:25]), ln.strip())
                   for ln, _, _ in pg['lines'])]
        if hit and hit[0] != int(pgno): fails.append(f'Contents says {num} is on page {pgno}, it is on page {hit[0]}')
        if not hit: notes.append(f'Contents row {num} {title!r} not found as a heading')

# ---- machine-readable Contents map (builds may emit a hidden TOCMAP line) ----
# Flex/reflowed Contents rows confuse text extraction, so the harness writes a
# plain `TOCMAP 1:4 1.1:5 ...` anchor. When present it is checked for real;
# older builds without it fall back to the regex check above.
_map = re.search(r'TOCMAP\s+([^\n]+)', alltext)
if _map:
    _openers = {i for i, pg in enumerate(pages, 1)
                if 'INTHISCHAPTERYOUWILLLEARN' in re.sub(r'\s+', '', pg['text']).upper()}
    _special = {1} | _openers
    if ti is not None: _special.add(ti + 1)
    for pair in _map.group(1).split():
        if ':' not in pair: continue
        num, pno = pair.split(':', 1)
        if not pno.isdigit(): continue
        if '.' not in num:  # a chapter row must point at a full-page opener
            if int(pno) not in _openers:
                fails.append(f'TOCMAP says chapter {num} is on page {pno}, which is not a chapter opener')
            continue
        hit = [i for i, pg in enumerate(pages, 1) if i not in _special and
               any(re.match(r'^' + re.escape(num) + r'(?![\d.])', ln.strip())
                   for ln, _, _ in pg['lines'])]
        if hit and hit[0] != int(pno):
            fails.append(f'TOCMAP says {num} is on page {pno}, it is on page {hit[0]}')
        if not hit:
            notes.append(f'TOCMAP entry {num} has no matching heading on page {pno}')

# ---- required pages ----
if mode == 'slice':
    reqs = ['About this book', 'Contents', 'Review questions', 'Chapter summary']
    # the opener itself is verified below by the whitespace-stripped openers check
    # (tracked letter-spacing breaks literal text search)
else:
    reqs = ['About this book', 'Contents', 'Learning in action', 'Find ', 'Practice set', 'Answer key', 'Mind map', 'Quick reference', 'You learned how to', 'Glossary', 'So, what is next']
for req in reqs:
    if not re.search(re.escape(req), alltext, re.I): fails.append(f'required page missing: {req}')

# ---- chapter openers ----
openers = [i for i, pg in enumerate(pages, 1) if 'INTHISCHAPTERYOUWILLLEARN' in re.sub(r'\s+', '', pg['text']).upper()]
if not openers: fails.append('no chapter opener pages found')
for i in openers:
    if len(pages[i - 1]['text'].split()) > 170: fails.append(f'page {i}: chapter opener shares its page with content (must be a full page of its own)')

# ---- GATE pill names the paper ----
if re.search(r'GATE\s*·\s*(?!\s*(CS|XE|EC|EE|ME|CE|DA|IN|PH|CH|BT|CY|MA|ST|TF|AE|AG|ES|EY|GE|GG|MN|MT|NM|PE|XH|XL)\b)', alltext): fails.append('GATE pill does not name the paper (use GATE CS · SECTION · TOPIC)')

print('PDF:', sys.argv[1], '| pages', n, '| body', body, 'pt | fonts', dict(fonts.most_common(4)))
for f in fails: print('FAIL', f)
for x in notes[:6]: print('note', x)
print('RESULT', 'PASS' if not fails else f'{len(fails)} FAIL(S)'); sys.exit(1 if fails else 0)
