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
    'flow': '#0e8f80', 'data': '#0d6d78', 'rule': '#0d6d78',
    'wrong': '#b3392e', 'analogy': '#66717a', 'result': '#1f7a4d',
    'axis': '#667085', 'grid': '#e9ecea', 'accent': '#0d6d78',
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
            out.append(f'<text x="{ax}" y="{ay+15}" text-anchor="middle" font-size="16" fill="{c}">{esc(t)}</text>')
        for t in yticks:
            ax, ay = self.pt(0, t)
            out.append(f'<line x1="{ax}" y1="{ay}" x2="{ax-4}" y2="{ay}" stroke="{c}" stroke-width="1"/>')
            out.append(f'<text x="{ax-7}" y="{ay+3}" text-anchor="end" font-size="16" fill="{c}">{esc(t)}</text>')
        ox, oy = self.pt(0, 0)
        if xlabel:
            out.append(f'<text x="{self.px1+2}" y="{oy+16}" text-anchor="end" font-size="16" fill="{c}">{esc(xlabel)}</text>')
        if ylabel:
            out.append(f'<text x="{ox-8}" y="{self.py1-4}" text-anchor="middle" font-size="16" fill="{c}">{esc(ylabel)}</text>')
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

    def point(self, x, y, label, color=None, r=2.8, dx=7, dy=-6, size=16):
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
                f'<text x="{bx+4}" y="{by+12}" font-size="16" fill="{c}">{esc(label)}</text>')

    def angle(self, t0, t1, radius=0.16, label=None, color=None):
        """Small arc between two directions, e.g. a 45-degree annotation."""
        c = color or ROLE['analogy']
        pts = [(radius * __import__('math').cos(t0 + (t1-t0)*i/24),
                radius * __import__('math').sin(t0 + (t1-t0)*i/24)) for i in range(25)]
        s = '<polyline points="' + ' '.join(f'{self.pt(x,y)[0]},{self.pt(x,y)[1]}' for x,y in pts) + f'" fill="none" stroke="{c}" stroke-width="1"/>'
        if label:
            mx = radius * 1.35 * __import__('math').cos((t0+t1)/2)
            my = radius * 1.35 * __import__('math').sin((t0+t1)/2)
            s += self.label(mx, my, label, color=c, size=16)
        return s

    def label(self, x, y, text, anchor='start', color=None, size=16, dy=0):
        px, py = self.pt(x, y)
        c = color or ROLE['axis']
        return (f'<text x="{px}" y="{py+dy}" text-anchor="{anchor}" font-size="{size}" '
                f'fill="{c}">{esc(text)}</text>')

    def rule_label(self, x, y, text, color=None, size=16):
        """Label at a pixel position (for placing text beside a curve)."""
        c = color or ROLE['axis']
        return f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}">{esc(text)}</text>'


def region_figure():
    """Ex 1.3: region y=x to sqrt(x); dy inner => vertical strips."""
    c = Canvas(520, 280, (0, 1), (0, 1), pad=(60, 42, 20, 38))
    inner = c.region(lambda x: x, lambda x: math.sqrt(x), 0, 1, opacity=0.07)
    inner += c.axes(xticks=(0, 1), yticks=(0, 1))
    inner += c.strips_vertical(lambda x: x, lambda x: math.sqrt(x), 0, 1, n=10)
    inner += c.plot(lambda x: math.sqrt(x), 0, 1, color=ROLE['rule'], width=2.2)
    inner += c.plot(lambda x: x, 0, 1, color=ROLE['data'], width=2.2)
    inner += c.point(1, 1, '(1, 1)', color=ROLE['accent'], dx=10, dy=-12)
    inner += c.label(0.34, math.sqrt(0.34), 'y = sqrt(x)', color=ROLE['rule'], size=16, dy=-12)
    inner += c.label(0.58, 0.58, 'y = x', color=ROLE['data'], size=16, dy=18)
    return c.svg(inner, cls='fig')


def rectangle_figure(x0, x1, y0, y1, label='R', strips='vertical'):
    """Constant-limit rectangle with boundary labels and integration strips."""
    c = Canvas(500, 250, (x0 - 0.5, x1 + 0.9), (y0 - 0.5, y1 + 0.7),
               pad=(62, 34, 20, 38))
    inner = c.region(lambda x: y0, lambda x: y1, x0, x1, opacity=0.06)
    inner += c.axes(xticks=(x0, x1), yticks=(y0, y1))
    if strips == 'vertical':
        inner += c.strips_vertical(lambda x: y0, lambda x: y1, x0, x1, n=9)
    else:
        inner += c.strips_horizontal(lambda y: x0, lambda y: x1, y0, y1, n=8)
    inner += c.label(x0, y1 + 0.35, f'{label}: {x0} <= x <= {x1}, {y0} <= y <= {y1}',
                     color=ROLE['accent'], size=16, dy=-14)
    return c.svg(inner, cls='fig')


def unit_square_figure():
    """Ex 1.2: unit square, dx inner => horizontal strips."""
    return rectangle_figure(0, 1, 0, 1, label='R', strips='horizontal')


def strip_between_figure():
    """Ex 1.4: x from y to 2, y from 1 to 2; dx inner => horizontal strips."""
    c = Canvas(500, 265, (0, 2.8), (0, 2.6), pad=(62, 34, 18, 38))
    inner = c.region(lambda x: 1, lambda x: min(x, 2), 1, 2, opacity=0.06)
    inner += c.axes(xticks=(1, 2), yticks=(1, 2))
    inner += c.strips_horizontal(lambda y: y, lambda y: 2, 1, 2, n=8)
    inner += c.plot(lambda x: x, 0.6, 2, color=ROLE['rule'], width=2)
    inner += c.plot(lambda x: 2, 0.6, 2, color=ROLE['data'], width=2)
    inner += c.point(2, 2, '(2, 2)', color=ROLE['accent'], dx=10, dy=-12)
    inner += c.label(1.42, 1.5, 'x = y', color=ROLE['rule'], size=16, dy=16)
    inner += c.label(2.03, 1.45, 'x = 2', color=ROLE['data'], size=16, dy=0)
    inner += c.label(1.45, 1.02, 'y = 1', color=ROLE['axis'], size=16, dy=18)
    inner += c.label(1.45, 2.02, 'y = 2', color=ROLE['axis'], size=16, dy=-12)
    return c.svg(inner, cls='fig')


def octant_figure():
    """Ex 1.5: quarter disk, dx inner => horizontal strips x=0..sqrt(1-y^2)."""
    c = Canvas(500, 255, (0, 1.3), (0, 1.3), pad=(62, 34, 18, 38))
    f = lambda x: math.sqrt(max(0.0, 1 - x * x))
    inner = c.region(lambda x: 0, f, 0, 1, opacity=0.07)
    inner += c.axes(xticks=(0, 1), yticks=(0, 1))
    inner += c.strips_horizontal(lambda y: 0, lambda y: f(y), 0, 1, n=9)
    inner += c.plot(f, 0, 1, color=ROLE['rule'], width=2.2)
    inner += c.point(1, 0, '(a, 0)', color=ROLE['accent'], dx=8, dy=22)
    inner += c.point(0, 1, '(0, a)', color=ROLE['accent'], dx=12, dy=-12)
    inner += c.label(0.5, 0.87, 'sqrt(a^2 - x^2)', color=ROLE['rule'], size=16, dy=-18)
    return c.svg(inner, cls='fig')


def cardioid_figure(a=1.0):
    """Ex 1.6: only theta in [0, pi] (upper half) is shaded and striped."""
    c = Canvas(520, 305, (-0.4 * a, 2.35 * a), (-1.5 * a, 1.5 * a), pad=(52, 34, 20, 38))
    rfn = lambda t: a * (1 + math.cos(t))
    inner = c.polar_region(rfn, 0, math.pi, n=90, opacity=0.07)
    inner += c.axes(xticks=(0,), yticks=(), xlabel='x', ylabel='y')
    inner += c.radial_strips(rfn, 0.1, math.pi - 0.1, n=8)
    inner += c.polar_curve(rfn, 0, math.pi, n=150, color=ROLE['rule'], width=2.2)
    t = math.pi / 3
    r = rfn(t)
    inner += c.arrow(0, 0, r * math.cos(t), r * math.sin(t), color=ROLE['wrong'], width=1.8, head=7)
    inner += c.label(r * math.cos(t), r * math.sin(t), 'r = a(1 + cos theta)',
                     color=ROLE['rule'], size=16, dy=-14)
    inner += c.point(2 * a, 0, '(2a, 0)', color=ROLE['accent'], dx=-46, dy=-14)
    inner += c.point(a, 0, 'a', color=ROLE['axis'], dx=-4, dy=22)
    return c.svg(inner, cls='fig')


def circle_figure(a=1.0):
    """Ex 1.7: circle r=2a cos(theta), theta in [0, pi/2], radial strips."""
    c = Canvas(440, 255, (0, 2.35 * a), (-0.15 * a, 1.25 * a), pad=(54, 30, 18, 38))
    rfn = lambda t: 2 * a * math.cos(t)
    inner = c.polar_region(rfn, 0, math.pi / 2, n=70, opacity=0.07)
    inner += c.axes(xticks=(), yticks=(), xlabel='x', ylabel='y')
    inner += c.radial_strips(rfn, 0.1, math.pi / 2 - 0.1, n=7)
    inner += c.polar_curve(rfn, 0, math.pi / 2, n=120, color=ROLE['data'], width=2.2)
    t = math.pi / 4
    r = rfn(t)
    inner += c.arrow(0, 0, r * math.cos(t), r * math.sin(t), color=ROLE['wrong'], width=1.8, head=7)
    inner += c.label(r * math.cos(t), r * math.sin(t), 'r = 2a cos theta',
                     color=ROLE['data'], size=16, dy=-14)
    inner += c.label(a, 0, 'a', color=ROLE['axis'], size=16, dy=22)
    inner += c.label(2 * a, 0, '2a', color=ROLE['axis'], size=16, dy=22)
    return c.svg(inner, cls='fig')


def order_swap_figure():
    """Two panels of the same triangle: dy dx and dx dy strips."""
    c = Canvas(900, 320, (0, 2.45), (0, 1.15), pad=(64, 36, 22, 40))
    o = 1.35
    inner = ''
    inner += c.arrow(0, 0, 1.08, 0) + c.arrow(0, 0, 0, 1.1)
    inner += c.strips_vertical(lambda x: 0, lambda x: x, 0.06, 0.94, n=9)
    inner += c.plot(lambda x: x, 0, 1, color=ROLE['rule'], width=2)
    inner += c.point(1, 1, '(1, 1)', dx=8, dy=-12)
    inner += c.label(0.5, 1.1, 'dy dx: vertical strips', color=ROLE['wrong'], size=16)
    inner += c.label(1.02, 0, 'x = 1', color=ROLE['axis'], size=16, dy=18)
    inner += c.arrow(o, 0, o + 1.08, 0) + c.arrow(o, 0, o, 1.1)
    inner += c.strips_horizontal(lambda y: y + o, lambda y: 1 + o, 0.06, 0.94, n=9)
    inner += c.plot(lambda x: x - o, o, o + 1, color=ROLE['rule'], width=2)
    inner += c.point(o + 1, 1, '(1, 1)', dx=8, dy=-12)
    inner += c.label(o + 0.42, 1.1, 'dx dy: rewrite the limits', color=ROLE['analogy'], size=16)
    inner += c.label(o + 1.02, 0, 'x = 1', color=ROLE['axis'], size=16, dy=18)
    return c.svg(inner, cls='fig')
