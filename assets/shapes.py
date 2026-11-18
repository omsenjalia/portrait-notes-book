"""shapes.py — reusable, mathematically-sampled SVG primitives for the books.

Every figure is built through ONE data-to-pixel transform, so the curve, the
shaded region, the axis ticks and the markers cannot disagree. Functions are
sampled from their definitions (no hand-typed Bezier control points).

Rules enforced here (see references/page-recipes.md):
  - every SVG tag carries font-family="Google Sans"
  - every arrow ends in a head exactly on its target
  - labels are plain ASCII/short words; write symbols as words ("sqrt(x)",
    "theta") so no font falls back to DejaVu/Liberation
  - colour by role: teal main flow, blue data, purple rule, red wrong,
    amber analogy, green result

No third-party dependencies.
"""
import html, math

ROLE = {
    'flow': '#0e8f80', 'data': '#1a64d8', 'rule': '#6b46d6',
    'wrong': '#d1342a', 'analogy': '#b06f00', 'result': '#17803d',
    'axis': '#667085', 'grid': '#e9ecf7', 'accent': '#3b3fa8',
}


def esc(t):
    return html.escape(str(t), quote=True)


class Canvas:
    """Map data coordinates to SVG pixels with one shared transform."""

    def __init__(self, width, height, xlim, ylim, pad=(46, 26, 16, 26)):
        self.w, self.h = width, height
        self.x0, self.x1 = xlim
        self.y0, self.y1 = ylim
        left, right, top, bottom = pad
        self.px0, self.px1 = left, width - right
        self.py0, self.py1 = height - bottom, top

    def pt(self, x, y):
        px = self.px0 + (x - self.x0) / (self.x1 - self.x0) * (self.px1 - self.px0)
        py = self.py0 - (y - self.y0) / (self.y1 - self.y0) * (self.py0 - self.py1)
        return round(px, 2), round(py, 2)

    def svg(self, inner, cls=''):
        c = f' class="{esc(cls)}"' if cls else ''
        return (f'<svg{c} width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" font-family="Google Sans">'
                f'{inner}</svg>')

    # ---- axes, ticks, arrows -------------------------------------------------
    def axes(self, xticks=(), yticks=(), xlabel='x', ylabel='y', color=None):
        c = color or ROLE['axis']
        out = [self.arrow(self.x0, 0, self.x1, 0, color=c, head=6),
               self.arrow(0, self.y0, 0, self.y1, color=c, head=6)]
        for t in xticks:
            ax, ay = self.pt(t, 0)
            out.append(f'<line x1="{ax}" y1="{ay}" x2="{ax}" y2="{ay+4}" stroke="{c}" stroke-width="1"/>')
            out.append(f'<text x="{ax}" y="{ay+15}" text-anchor="middle" font-size="9" fill="{c}">{esc(t)}</text>')
        for t in yticks:
            ax, ay = self.pt(0, t)
            out.append(f'<line x1="{ax}" y1="{ay}" x2="{ax-4}" y2="{ay}" stroke="{c}" stroke-width="1"/>')
            out.append(f'<text x="{ax-7}" y="{ay+3}" text-anchor="end" font-size="9" fill="{c}">{esc(t)}</text>')
        ox, oy = self.pt(0, 0)
        if xlabel:
            out.append(f'<text x="{self.px1+2}" y="{oy+16}" text-anchor="end" font-size="10" fill="{c}">{esc(xlabel)}</text>')
        if ylabel:
            out.append(f'<text x="{ox-8}" y="{self.py1-4}" text-anchor="middle" font-size="10" fill="{c}">{esc(ylabel)}</text>')
        return ''.join(out)

    def arrow(self, x1, y1, x2, y2, color=None, width=1.4, head=6):
        """Line ending in a triangular head whose tip is exactly at (x2, y2)."""
        c = color or ROLE['axis']
        ax, ay = self.pt(x1, y1)
        bx, by = self.pt(x2, y2)
        ang = math.atan2(by - ay, bx - ax)
        p1 = (bx - head * math.cos(ang - 0.45), by - head * math.sin(ang - 0.45))
        p2 = (bx - head * math.cos(ang + 0.45), by - head * math.sin(ang + 0.45))
        return (f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{c}" stroke-width="{width}"/>'
                f'<polygon points="{bx},{by} {p1[0]:.2f},{p1[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}" fill="{c}"/>')

    # ---- sampled curves and regions -----------------------------------------
    def plot(self, fn, x0, x1, n=120, color=None, width=1.8, dash=None):
        """Sample fn(x) at n+1 points and emit a polyline in data space."""
        c = color or ROLE['data']
        step = (x1 - x0) / n
        pts = [self.pt(x0 + i * step, fn(x0 + i * step)) for i in range(n + 1)]
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return (f'<polyline points="{" ".join(f"{px},{py}" for px, py in pts)}" '
                f'fill="none" stroke="{c}" stroke-width="{width}"{d}/>')

    def region(self, lower, upper, x0, x1, n=120, fill=None, opacity=0.12):
        """Shade the vertical strip between two sampled functions."""
        step = (x1 - x0) / n
        xs = [x0 + i * step for i in range(n + 1)]
        top = [self.pt(x, upper(x)) for x in xs]
        bot = [self.pt(x, lower(x)) for x in reversed(xs)]
        pts = top + bot
        return (f'<polygon points="{" ".join(f"{px},{py}" for px, py in pts)}" '
                f'fill="{fill or ROLE["accent"]}" opacity="{opacity}"/>')

    def polar_curve(self, rfn, t0, t1, n=180, color=None, width=1.8, dash=None):
        """Sample a polar curve r=f(theta); used for cardioid / circle figures."""
        c = color or ROLE['data']
        step = (t1 - t0) / n
        pts = []
        for i in range(n + 1):
            t = t0 + i * step
            r = rfn(t)
            pts.append(self.pt(r * math.cos(t), r * math.sin(t)))
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return (f'<polyline points="{" ".join(f"{px},{py}" for px, py in pts)}" '
                f'fill="none" stroke="{c}" stroke-width="{width}"{d}/>')

    def polar_region(self, rfn, t0, t1, n=90, fill=None, opacity=0.12):
        """Shade the area inside a polar curve from the origin."""
        step = (t1 - t0) / n
        outer = []
        for i in range(n + 1):
            t = t0 + i * step
            r = rfn(t)
            outer.append(self.pt(r * math.cos(t), r * math.sin(t)))
        ox, oy = self.pt(0, 0)
        pts = [(ox, oy)] + outer + [(ox, oy)]
        return (f'<polygon points="{" ".join(f"{px},{py}" for px, py in pts)}" '
                f'fill="{fill or ROLE["accent"]}" opacity="{opacity}"/>')

    # ---- markers and text ----------------------------------------------------
    def points(self, coords, r=3, color=None):
        c = color or ROLE['data']
        return ''.join(
            f'<circle cx="{self.pt(x, y)[0]}" cy="{self.pt(x, y)[1]}" r="{r}" fill="{c}"/>'
            for x, y in coords)

    # ---- integration strips (the source deck's signature visual language) ----
    def strips_vertical(self, lower, upper, x0, x1, n=12, color=None, width=0.85,
                        head=3.2, arrow=True):
        """Thin upward strips between two curves: shows a dy inner integral."""
        c = color or ROLE['wrong']
        out = []
        for i in range(1, n + 1):
            x = x0 + (x1 - x0) * i / (n + 1)
            lo, hi = lower(x), upper(x)
            if hi <= lo: continue
            if arrow:
                out.append(self.arrow(x, lo, x, hi, color=c, width=width, head=head))
            else:
                (ax, ay), (bx, by) = self.pt(x, lo), self.pt(x, hi)
                out.append(f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{c}" stroke-width="{width}"/>')
        return ''.join(out)

    def strips_horizontal(self, left, right, y0, y1, n=12, color=None, width=0.85,
                          head=3.2, arrow=True):
        """Thin rightward strips between two curves: shows a dx inner integral."""
        c = color or ROLE['analogy']
        out = []
        for i in range(1, n + 1):
            y = y0 + (y1 - y0) * i / (n + 1)
            xa, xb = left(y), right(y)
            if xb <= xa: continue
            if arrow:
                out.append(self.arrow(xa, y, xb, y, color=c, width=width, head=head))
            else:
                (ax, ay), (bx, by) = self.pt(xa, y), self.pt(xb, y)
                out.append(f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{c}" stroke-width="{width}"/>')
        return ''.join(out)

    def radial_strips(self, rfn, t0, t1, n=9, color=None, width=0.9, head=3.2):
        """Rays from the origin to a polar curve: shows a dr inner integral."""
        c = color or ROLE['analogy']
        return ''.join(self.arrow(0, 0, rfn(t) * __import__('math').cos(t),
                                  rfn(t) * __import__('math').sin(t),
                                  color=c, width=width, head=head)
                       for t in [t0 + (t1 - t0) * i / (n + 1) for i in range(1, n + 1)])

    def point(self, x, y, label, color=None, r=2.8, dx=7, dy=-6, size=9):
        """A marked point with its coordinate label, as in the source slides."""
        c = color or ROLE['accent']
        px, py = self.pt(x, y)
        return (f'<circle cx="{px}" cy="{py}" r="{r}" fill="{c}"/>'
                f'<text x="{px+dx}" y="{py+dy}" font-size="{size}" fill="{c}">{esc(label)}</text>')

    def split_line(self, x, y0, y1, label, color=None, dash='4 3'):
        """Dashed line where a region must be split, with an inline label."""
        c = color or ROLE['wrong']
        ax, ay = self.pt(x, y0); bx, by = self.pt(x, y1)
        return (f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{c}" '
                f'stroke-width="1.2" stroke-dasharray="{dash}"/>'
                f'<text x="{bx+4}" y="{by+12}" font-size="9" fill="{c}">{esc(label)}</text>')

    def angle(self, t0, t1, radius=0.16, label=None, color=None):
        """Small arc between two directions, e.g. a 45-degree annotation."""
        c = color or ROLE['analogy']
        pts = [(radius * __import__('math').cos(t0 + (t1-t0)*i/24),
                radius * __import__('math').sin(t0 + (t1-t0)*i/24)) for i in range(25)]
        s = '<polyline points="' + ' '.join(f'{self.pt(x,y)[0]},{self.pt(x,y)[1]}' for x,y in pts) + f'" fill="none" stroke="{c}" stroke-width="1"/>'
        if label:
            mx = radius * 1.35 * __import__('math').cos((t0+t1)/2)
            my = radius * 1.35 * __import__('math').sin((t0+t1)/2)
            s += self.label(mx, my, label, color=c, size=9)
        return s

    def label(self, x, y, text, anchor='start', color=None, size=10, dy=0):
        px, py = self.pt(x, y)
        c = color or ROLE['axis']
        return (f'<text x="{px}" y="{py+dy}" text-anchor="{anchor}" font-size="{size}" '
                f'fill="{c}">{esc(text)}</text>')

    def rule_label(self, x, y, text, color=None, size=10):
        """Label at a pixel position (for placing text beside a curve)."""
        c = color or ROLE['axis']
        return f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}">{esc(text)}</text>'


def region_figure():
    """Figure: region between y=x and y=sqrt(x), with dy integration strips."""
    c = Canvas(400, 215, (0, 1), (0, 1), pad=(46, 30, 16, 26))
    inner = c.region(lambda x: x, lambda x: math.sqrt(x), 0, 1, opacity=0.08)
    inner += c.axes(xticks=(0, 1), yticks=(0, 1))
    inner += c.strips_vertical(lambda x: x, lambda x: math.sqrt(x), 0, 1, n=10)
    inner += c.plot(lambda x: math.sqrt(x), 0, 1, color=ROLE['rule'], width=2)
    inner += c.plot(lambda x: x, 0, 1, color=ROLE['data'], width=2)
    inner += c.point(1, 1, '(1, 1)', color=ROLE['accent'], dx=6, dy=-7)
    inner += c.point(0, 0, '(0, 0)', color=ROLE['accent'], dx=6, dy=12)
    inner += c.label(0.42, math.sqrt(0.42), 'y = sqrt(x)', color=ROLE['rule'], size=10, dy=-8)
    inner += c.label(0.62, 0.62, 'y = x', color=ROLE['data'], size=10, dy=12)
    return c.svg(inner, cls='fig')


def cardioid_figure(a=1.0):
    """Figure: cardioid r = a(1 + cos theta) with radial (dr) strips."""
    c = Canvas(360, 210, (-0.35 * a, 2.15 * a), (-1.45 * a, 1.45 * a), pad=(30, 20, 14, 26))
    rfn = lambda t: a * (1 + math.cos(t))
    inner = c.polar_region(rfn, 0, 2 * math.pi, n=120, opacity=0.09)
    inner += c.axes(xticks=(0, a), yticks=(), xlabel='x', ylabel='y')
    inner += c.radial_strips(rfn, 0.15, 2 * math.pi - 0.15, n=9)
    inner += c.polar_curve(rfn, 0, 2 * math.pi, n=200, color=ROLE['rule'], width=2)
    t = math.pi / 3
    r = rfn(t)
    inner += c.arrow(0, 0, r * math.cos(t), r * math.sin(t), color=ROLE['wrong'], width=1.6, head=6)
    inner += c.label(r * math.cos(t), r * math.sin(t), 'r = a(1 + cos theta)', color=ROLE['rule'], size=9, dy=-6)
    inner += c.point(2 * a, 0, '(2a, 0)', color=ROLE['accent'], dx=-40, dy=-7)
    return c.svg(inner, cls='fig')


def circle_figure(a=1.0):
    """Figure: circle r = 2a cos(theta), upper half, with radial dr strips."""
    c = Canvas(300, 170, (0, 2.15 * a), (-0.1 * a, 1.1 * a), pad=(34, 18, 14, 24))
    rfn = lambda t: 2 * a * math.cos(t)
    inner = c.polar_region(rfn, 0, math.pi / 2, n=90, opacity=0.09)
    inner += c.axes(xticks=(0, a, 2 * a), yticks=(), xlabel='x', ylabel='y')
    inner += c.radial_strips(rfn, 0.08, math.pi / 2 - 0.08, n=7)
    inner += c.polar_curve(rfn, 0, math.pi / 2, n=120, color=ROLE['data'], width=2)
    t = math.pi / 4
    r = rfn(t)
    inner += c.arrow(0, 0, r * math.cos(t), r * math.sin(t), color=ROLE['wrong'], width=1.6, head=6)
    inner += c.label(r * math.cos(t), r * math.sin(t), 'r = 2a cos theta', color=ROLE['data'], size=9, dy=-6)
    inner += c.point(a, 0, '(a, 0)', color=ROLE['accent'], dx=-18, dy=13)
    return c.svg(inner, cls='fig')


def order_swap_figure():
    """Two side-by-side panels: the same triangle with dy and dx strips.

    This is the source deck's classic 'change the order' figure: vertical
    strips for the dy inner integral, horizontal strips after rewriting the
    limits for the dx inner integral.
    """
    c = Canvas(700, 235, (0, 2.45), (0, 1.15), pad=(40, 28, 16, 28))
    o = 1.35  # offset of the right-hand panel
    inner = ''
    # left panel: 0 <= y <= x, 0 <= x <= 1 -> vertical dy strips
    inner += c.arrow(0, 0, 1.08, 0) + c.arrow(0, 0, 0, 1.1)
    inner += c.strips_vertical(lambda x: 0, lambda x: x, 0.06, 0.94, n=9)
    inner += c.plot(lambda x: x, 0, 1, color=ROLE['rule'], width=1.8)
    inner += c.point(1, 1, '(1, 1)', dx=5, dy=-7)
    inner += c.rule_label(150, 16, 'dy dx: vertical strips', ROLE['wrong'], 9)
    inner += c.label(1.02, 0, 'x = 1', color=ROLE['axis'], size=9, dy=13)
    inner += c.label(0, 1.04, 'y = x', color=ROLE['rule'], size=9)
    # right panel: 0 <= y <= 1, y <= x <= 1 -> horizontal dx strips
    inner += c.arrow(o, 0, o + 1.08, 0) + c.arrow(o, 0, o, 1.1)
    inner += c.strips_horizontal(lambda y: y + o, lambda y: 1 + o, 0.06, 0.94, n=9)
    inner += c.plot(lambda x: x - o, o, o + 1, color=ROLE['rule'], width=1.8)
    inner += c.point(o + 1, 1, '(1, 1)', dx=5, dy=-7)
    inner += c.rule_label(505, 16, 'dx dy: rewrite the limits', ROLE['analogy'], 9)
    inner += c.label(o + 1.02, 0, 'x = 1', color=ROLE['axis'], size=9, dy=13)
    inner += c.label(o, 1.04, 'y = x', color=ROLE['rule'], size=9)
    return c.svg(inner, cls='fig')

def rectangle_figure(x0, x1, y0, y1, label='R', strips='vertical'):
    """Constant-limit rectangle with boundary labels and integration strips."""
    c = Canvas(360, 180, (x0 - 0.3, x1 + 0.7), (y0 - 0.35, y1 + 0.45),
               pad=(44, 24, 14, 26))
    inner = c.region(lambda x: y0, lambda x: y1, x0, x1, opacity=0.07)
    inner += c.axes(xticks=(x0, x1), yticks=(y0, y1))
    if strips == 'vertical':
        inner += c.strips_vertical(lambda x: y0, lambda x: y1, x0, x1, n=9)
    else:
        inner += c.strips_horizontal(lambda y: x0, lambda y: x1, y0, y1, n=8)
    inner += c.label(x0, y0, f'{label}: {x0} <= x <= {x1}, {y0} <= y <= {y1}',
                     color=ROLE['accent'], size=9, dy=-10)
    return c.svg(inner, cls='fig')


def unit_square_figure():
    """Unit square for the separable integrand, with vertical dy strips."""
    return rectangle_figure(0, 1, 0, 1, label='R', strips='vertical')


def strip_between_figure():
    """Region x from y to 2, y from 1 to 2 (Example 1.4)."""
    c = Canvas(360, 195, (0.5, 2.6), (0.5, 2.5), pad=(46, 26, 14, 28))
    inner = c.region(lambda x: 1, lambda x: min(x, 2), 1, 2, opacity=0.07)
    inner += c.axes(xticks=(1, 2), yticks=(1, 2))
    inner += c.strips_vertical(lambda x: 1, lambda x: min(x, 2), 1, 2, n=8)
    inner += c.plot(lambda x: x, 0.5, 2, color=ROLE['rule'], width=1.8)
    inner += c.plot(lambda x: 2, 0.5, 2.5, color=ROLE['data'], width=1.8)
    inner += c.point(2, 2, '(2, 2)', dx=5, dy=-7)
    inner += c.label(1.7, 1.1, 'x = y', color=ROLE['rule'], size=9)
    inner += c.label(1.7, 2.15, 'x = 2', color=ROLE['data'], size=9)
    return c.svg(inner, cls='fig')


def octant_figure():
    """Quarter disk x^2+y^2 <= a^2 in the first quadrant, vertical strips."""
    c = Canvas(360, 185, (0, 1.2), (0, 1.2), pad=(44, 26, 14, 26))
    f = lambda x: math.sqrt(max(0.0, 1 - x*x))
    inner = c.region(lambda x: 0, f, 0, 1, opacity=0.08)
    inner += c.axes(xticks=(0, 1), yticks=(0, 1))
    inner += c.strips_vertical(lambda x: 0, f, 0, 1, n=9)
    inner += c.plot(f, 0, 1, color=ROLE['rule'], width=2)
    inner += c.point(1, 0, '(a, 0)', dx=-4, dy=14)
    inner += c.label(0.55, 0.72, 'sqrt(a^2 - x^2)', color=ROLE['rule'], size=9)
    return c.svg(inner, cls='fig')
