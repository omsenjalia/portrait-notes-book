"""build_slice.py [output.pdf] — worked example: a complete ONE-CHAPTER maths-pack build.

This is the reference harness for the portrait-notes-book skill. It builds a
cover, About page, Contents, a full-page chapter opener, chapter content
(definition card, note, common-slip card, three worked examples, a figure,
review questions, chapter summary) with real KaTeX math, then does a SECOND
PASS to read the real page numbers back from the rendered PDF and fill the
Contents rows.

Run:
    pip install weasyprint brotli pdfminer.six
    npm install @fontsource/google-sans @fontsource/google-sans-code katex
    python3 build_slice.py            # writes Infinite_Series_Slice.pdf

Paths:
    node_modules      is auto-detected from cwd, or set PNB_NODE_MODULES.
    mathrender.js and book.css are loaded from this file's directory.
"""
import json, re, subprocess, sys, os
import weasyprint
from pdfminer.high_level import extract_text
from shapes import Canvas
from math_values import MX


def svgfont(s):
    """Put the allowed font on every SVG without duplicating the attribute."""
    return re.sub(r'<svg(?![^>]*font-family)', '<svg font-family="Google Sans"', s)

ASSETS = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else 'Infinite_Series_Slice.pdf'

def resolve_nm():
    env = os.environ.get('PNB_NODE_MODULES')
    if env: return os.path.abspath(env)
    cand = os.path.join(os.getcwd(), 'node_modules')
    if os.path.isdir(cand): return cand
    return os.path.join(ASSETS, 'node_modules')

NM = resolve_nm()
FS = NM + '/@fontsource'
tex = []
def m(t, disp=False):
    tex.append((t, disp)); return f'@@{len(tex)-1}@@'
def M(t): return m(t, True)
IND = '#3b3fa8'; DARK = '#1b1f4b'
def hexa(txt, size=34, fill=None, stroke=IND, col=IND):
    f = fill or 'none'
    return f'<svg width="{size}" height="{size}" viewBox="0 0 40 40"><polygon points="20,2 37,11 37,29 20,38 3,29 3,11" fill="{f}" stroke="{stroke}" stroke-width="2"/><text x="20" y="25.5" text-anchor="middle" font-size="15" font-weight="700" fill="{col}">{txt}</text></svg>'

def build(pages_map):
    tex.clear()
    pg = lambda k: pages_map.get(k, '0')
    # ---------- COVER ----------
    curve = ' '.join(f'{40+i*22},{250-(1-1/(i+2))*170:.1f}' for i in range(0, 12))
    cover = f'''<section class="cover"><div class="grid"></div>
    <svg class="axes" width="360" height="270" viewBox="0 0 360 270"><line x1="30" y1="250" x2="350" y2="250" stroke="{IND}" stroke-width="1.6"/><line x1="30" y1="250" x2="30" y2="20" stroke="{IND}" stroke-width="1.6"/>
    <line x1="30" y1="80" x2="350" y2="80" stroke="#6b46d6" stroke-width="1.2" stroke-dasharray="5 4"/><polyline points="{curve}" fill="none" stroke="{IND}" stroke-width="2.4"/>
    {''.join(f'<circle cx="{40+i*22}" cy="{250-(1-1/(i+2))*170:.1f}" r="3.4" fill="{IND}"/>' for i in range(0, 12))}
    <text x="338" y="72" font-size="11" fill="#6b46d6" text-anchor="end">S = 1</text><text x="344" y="266" font-size="11" fill="#667085" text-anchor="end">n</text></svg>
    <div class="ctag">ENGINEERING MATHEMATICS &middot; STUDY NOTES</div>
    <div class="ctitle"><span class="hl">Infinite</span><br>Series<br>Notes</div>
    <div class="cformula">{M(r'\sum_{n=1}^{\infty}\frac{1}{2^{n}}=\frac12+\frac14+\frac18+\cdots=1')}</div>
    <div class="csub">Definitions, convergence and tests of convergence</div>
    <p class="cdesc">An infinite sum can be finite. These notes build that idea from partial sums, one worked example at a time.</p>
    <div class="cards"><div class="cc"><b>Example 1.3</b><span>{m(r'S_n=1-\frac{1}{n+1}')}</span></div><div class="cc"><b>Graph</b><span>partial sums rise to 1</span></div><div class="cc"><b>Definition</b><span>{m(r'S=\lim_{n\to\infty}S_n')}</span></div></div></section>'''
    # ---------- ABOUT ----------
    about = f'''<section class="flow"><h1 class="pt">About this book</h1>
    <p>These notes turn a standard lecture on infinite series into a short textbook. They are written for a first- or second-year engineering student who already knows limits of sequences.</p>
    <h3>What you should know first</h3><ul><li>Limits of sequences, including {m(r'\lim_{n\to\infty}\frac1n=0')}.</li><li>Continuity and the idea of an improper integral.</li><li>Elementary algebra of inequalities.</li></ul>
    <h3>How each chapter is built</h3>
    <table class="t"><tr><th>BOX</th><th>WHAT IT GIVES YOU</th></tr><tr><td>Learning objectives</td><td>What you will be able to do after the chapter. They sit on the chapter opener.</td></tr><tr><td>Definition</td><td>The exact statement of a term. Learn these word for word.</td></tr><tr><td>Example</td><td>A worked problem with every step shown.</td></tr><tr><td>Note, Common slip, Intuition</td><td>Something to remember, a mistake to avoid, or an everyday picture.</td></tr><tr><td>Review questions</td><td>Check yourself. The answer is printed directly underneath.</td></tr><tr><td>Chapter summary</td><td>The chapter in a few lines, for revision.</td></tr></table>
    <h3>How to read the colours</h3>
    <p class="chips"><span class="chip c1">teal = main flow</span> <span class="chip c2">blue = data</span> <span class="chip c3">purple = rule or formula</span> <span class="chip c4">red = wrong or a slip</span> <span class="chip c5">amber = picture or analogy</span> <span class="chip c6">green = right or result</span></p>
    <h3>GATE tags</h3><p>A GATE pill marks a topic in the official GATE syllabus. A GATE corner lists past questions only when they were verified. Where a past appearance could not be confirmed, only the syllabus topic is tagged.</p></section>'''
    # ---------- CONTENTS ----------
    rows = [('1', 'What is an Infinite Series?', 'ch1'), ('1.1', 'Definition and partial sums', 's11'), ('1.2', 'Convergence, divergence and oscillation', 's12'), ('1.3', 'Worked examples', 's13')]
    crow = ''.join(f'<div class="cr {"ch" if "." not in n_ else "sc"}"><span class="n">{n_}</span><span class="tt">{t}</span><span class="dots"></span><span class="pn">{pg(k)}</span></div>' for n_, t, k in rows)
    tocmap = ' '.join(f'{n_}:{pg(k)}' for n_, _, k in rows)
    contents = (f'<section class="flow"><h1 class="pt">Contents</h1>{crow}'
                f'<div class="qa-anchor">TOCMAP {tocmap}</div></section>')
    # ---------- OPENER ----------
    obj = ['Write the general term and the n-th partial sum of a series', 'Decide convergence, divergence to infinity, or oscillation from the partial sums', 'Recognise a telescoping series and evaluate its sum', 'Spot the three classical oscillating examples']
    orows = ''.join(f'<div class="orow">{hexa(i+1, 34)}<div>{t}</div></div>' for i, t in enumerate(obj))
    opener = f'''<section class="opener"><div class="panel"><div class="pgrid"></div>
    <svg class="pcurve" width="300" height="180" viewBox="0 0 300 180"><line x1="10" y1="170" x2="290" y2="170" stroke="#aab0ff" stroke-width="1.4"/><line x1="10" y1="170" x2="10" y2="10" stroke="#aab0ff" stroke-width="1.4"/><path d="M10,160 C60,60 120,40 290,30" fill="none" stroke="#aab0ff" stroke-width="2.2"/></svg>
    <div class="otab">Chapter 1</div><h1 class="otitle">What is an <span>Infinite</span> Series?</h1><div class="orule"></div>
    <p class="olead">An infinite sum is not a finite sum written with dots. Its meaning is defined through the sequence of partial sums.</p>
    <div class="opill">GATE CS &middot; ENGINEERING MATHEMATICS &middot; SEQUENCES AND SERIES</div>
    <div class="oformula">{M(r'S_n=a_1+a_2+\cdots+a_n')}</div><div class="obadge">{hexa(1, 64, fill=DARK, stroke='#aab0ff', col='#ffffff')}</div></div>
    <div class="oright"><div class="olabel">IN THIS CHAPTER YOU WILL LEARN TO</div>{orows}</div></section>'''
    # ---------- CONTENT ----------
    def ex(n, title, body): return f'<div class="ex"><div class="exh"><span class="exc">Example {n}</span> {title}</div><div class="exb">{body}</div></div>'
    def step(l, t): return f'<div class="stp"><span class="pill">{l}</span><span>{t}</span></div>'
    xs = []
    xs.append(ex('1.1', 'Sum of the odd positive integers',
      f'<p>Show that {m(r"1+3+5+7+\cdots")} is divergent.</p>' + step('A', f'The {m("n")}th term is {m("a_n=2n-1")}.') + step('B', 'The partial sum is an arithmetic progression:') + f'<div class="disp">{M(r"S_n=\frac n2\,[\,2\cdot 1+(n-1)\cdot 2\,]=n^2")}</div>' + step('C', f'So {m(r"\lim_{n\to\infty}S_n=+\infty")}.') + f'<p class="res"><b>Conclusion.</b> The series is divergent (to {m(r"+\infty")}).</p>'))
    xs.append(ex('1.2', 'An oscillating series',
      f'<p>Test {m(r"8-5-3+8-5-3+8-5-3+\cdots")}.</p>' + step('A', 'Group the terms in threes and add: the partial sums repeat in a cycle.') + f'<div class="disp">{M(r"S_{3n}=0,\quad S_{3n+1}=8,\quad S_{3n+2}=3")}</div>' + step('B', 'Three subsequences tend to three different finite limits.') + '<p class="res"><b>Conclusion.</b> The series oscillates (finitely).</p>'))
    xs.append(ex('1.3', 'A telescoping series',
      f'<p>Examine {m(r"\frac{1}{1\cdot 2}+\frac{1}{2\cdot 3}+\frac{1}{3\cdot 4}+\cdots")}.</p>' + step('A', f'Partial fractions: {m(r"a_n=\frac{1}{n(n+1)}=\frac1n-\frac1{n+1}")}.') + step('B', 'Add the first n terms. Every middle term cancels:') + f'<div class="disp">{M(r"S_n=\left(1-\tfrac12\right)+\left(\tfrac12-\tfrac13\right)+\cdots+\left(\tfrac1n-\tfrac1{n+1}\right)=1-\tfrac{1}{n+1}")}</div>' + step('C', f'Therefore {m(r"\lim_{n\to\infty}S_n=1")}.') + f'<p class="res"><b>Conclusion.</b> The series converges and its sum is {m("1")}. It is called a telescoping series.</p>'))
    # figure — sampled from the actual partial sums S_n = 1 - 1/(n+1)
    _c = Canvas(400, 215, (0, 9), (0, 1.05), pad=(46, 46, 16, 28))
    _inner = _c.axes(xticks=(0, 2, 4, 6, 8), yticks=(0, 0.5, 1), xlabel='n', ylabel='S(n)')
    _inner += _c.plot(lambda n: 1.0, 0, 8, color='#6b46d6', width=1.4, dash='6 4')
    _inner += _c.plot(lambda n: 1 - 1/(n+1) if n >= 0 else 0, 0, 8, n=160,
                     color='#1a64d8', width=1.8)
    _inner += _c.points([(n, 1 - 1/(n+1)) for n in range(1, 9)], r=3.4)
    _inner += _c.rule_label(352, _c.pt(0, 1)[1] - 7, 'S = 1', '#6b46d6')
    fig = ('<div class="fig">' + _c.svg(_inner) +
           f'<p class="cap"><b>Figure 1.1</b> Partial sums of Example 1.3 rise towards 1 but never pass it. The horizontal axis is {m("n")}.</p></div>')
    S = '<section class="flow">'
    S += f'<h2 id="s11"><span class="sn">1.1</span> Definition and partial sums</h2><p>An expression of the form {m(r"a_1+a_2+a_3+\cdots+a_n+\cdots")} is called an <b>infinite series</b>. In compact notation we write {m(r"\sum_{n=1}^{\infty}a_n")}. Here {m("a_n")} is the {m("n")}th term, or general term, of the series.</p>'
    S += f'<div class="def"><span class="rib">Definition</span><p>The <b>{m("n")}th partial sum</b> of the series is the sum of its first {m("n")} terms: {m(r"S_n=a_1+a_2+\cdots+a_n")}. The sequence {m("(S_n)")} completely determines the nature of the series.</p></div>'
    S += f'<h2 id="s12"><span class="sn">1.2</span> Convergence, divergence and oscillation</h2><p>The nature of a series is decided by the limit of its partial sums. There are three cases.</p>'
    S += f'<table class="t3"><tr><th>CONVERGENT</th><th>DIVERGENT TO {m(r"\pm\infty")}</th><th>OSCILLATING</th></tr><tr><td>{m(r"\lim_{n\to\infty}S_n=S")}, where {m("S")} is a finite number. {m("S")} is called the sum.</td><td>{m(r"S_n\to+\infty")} or {m(r"S_n\to-\infty")}. The partial sums tend to an infinite limit.</td><td>{m("S_n")} tends neither to a finite limit nor to {m(r"\pm\infty")}.</td></tr></table>'
    S += '<div class="note"><b>Note.</b> Oscillating series are divergent in the broad sense. The three-way naming is kept because it matches many Indian textbooks.</div>'
    S += f'<div class="slip"><span class="rib r">Common slip</span><p class="w"><b>Wrong</b> {m(r"1-1+1-1+\cdots=(1-1)+(1-1)+\cdots=0")}</p><p class="r2"><b>Right</b> {m("S_n")} alternates between {m("1")} and {m("0")}, so the series oscillates. Regrouping an infinite sum changes its partial sums.</p></div>'
    S += f'<h2 id="s13"><span class="sn">1.3</span> Worked examples</h2><p class="lead">Each example finds the partial sum first and then takes its limit.</p>' + xs[0] + xs[1] + xs[2] + fig
    S += '<div class="rq"><h3>Review questions</h3>'
    S += f'<div class="q"><p><b>1.</b> Find {m("S_n")} for {m(r"1-1+1-1+\cdots")} and state its nature.</p><p class="a"><b>Answer.</b> {m("S_n=1")} for odd {m("n")} and {m("S_n=0")} for even {m("n")}. The series oscillates (finitely).</p></div>'
    S += f'<div class="q"><p><b>2.</b> A series has {m(r"S_n=3-\frac1n")}. Find {m("a_1")}, {m("a_n")} for {m(r"n\ge 2")}, and the sum.</p><p class="a"><b>Answer.</b> {m(r"a_1=S_1=2")}. For {m(r"n\ge2")}, {m(r"a_n=S_n-S_{n-1}=\frac1{n-1}-\frac1n=\frac{1}{n(n-1)}")}. The series converges to {m("3")}.</p></div></div>'
    S += '<div class="sum"><span class="rib g">Chapter summary</span><ul><li>A series is defined by the sequence of its partial sums.</li><li>It converges when the partial sums have a finite limit, diverges to infinity when they tend to infinity, and otherwise oscillates.</li><li>Telescoping series cancel in pairs and often have an explicit sum.</li></ul></div></section>'
    body = svgfont(cover + about + contents + opener + S)
    # render math
    json.dump({str(i): [t, d] for i, (t, d) in enumerate(tex)}, open('tex.json', 'w'))
    subprocess.run(['node', os.path.join(ASSETS, 'mathrender.js'), 'tex.json', 'tex_out.json'], check=True)
    out = json.load(open('tex_out.json'))
    body = re.sub(r'@@(\d+)@@', lambda x: out[x.group(1)], body)
    css = open(os.path.join(ASSETS, 'book.css')).read().replace('@FS', FS).replace('@NM', NM)
    kcss = open(NM + '/katex/dist/katex.min.css').read().replace('url(fonts/', 'url(file://' + NM + '/katex/dist/fonts/')
    return f'<html><head><meta charset="utf-8"><style>{kcss}</style><style>{css}</style></head><body>{body}</body></html>'

def find_pages(pdf):
    # pdfminer.six replaces PyMuPDF here: mupdf 1.28+ takes 4-10 s per page on
    # WeasyPrint 70 output, while pdfminer reads the same PDF in milliseconds.
    pages = extract_text(pdf).split('\x0c')
    if pages and not pages[-1].strip(): pages.pop()
    res = {}
    for key, pat in [('ch1', r'What is an\s+Infinite Series\?'), ('s11', r'^1\.1\s+Definition'), ('s12', r'^1\.2\s+Convergence'), ('s13', r'^1\.3\s+Worked')]:
        for i, t in enumerate(pages, 1):
            if i > (3 if key == 'ch1' else 4) and re.search(pat, t, re.M): res[key] = str(i); break
    return res

pm = {}
for rnd in (1, 2):
    weasyprint.HTML(string=build(pm)).write_pdf(OUT)
    pm = find_pages(OUT); print('pass', rnd, pm)
print('wrote', OUT)
