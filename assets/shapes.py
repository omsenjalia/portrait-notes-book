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
    """Figure: region between y=x and y=sqrt(x) on [0,1], sampled from source."""
    c = Canvas(400, 215, (0, 1), (0, 1), pad=(46, 30, 16, 26))
    inner = c.region(lambda x: x, lambda x: math.sqrt(x), 0, 1)
    inner += c.axes(xticks=(0, 1), yticks=(0, 1))
    inner += c.plot(lambda x: math.sqrt(x), 0, 1, color=ROLE['rule'], width=2)
    inner += c.plot(lambda x: x, 0, 1, color=ROLE['data'], width=2)
    inner += c.points([(x, math.sqrt(x)) for x in (0.25, 0.5, 0.75)], r=2.6)
    inner += c.rule_label(392, c.pt(0, math.sqrt(0.97))[1] - 6, 'y = sqrt(x)', ROLE['rule'])
    inner += c.rule_label(392, c.pt(0, 0.97)[1] - 4, 'y = x', ROLE['data'])
    return c.svg(inner, cls='fig')


def cardioid_figure(a=1.0):
    """Figure: cardioid r = a(1 + cos(theta)) with a sample radius arrow."""
    c = Canvas(360, 210, (-0.35 * a, 2.15 * a), (-1.45 * a, 1.45 * a), pad=(30, 20, 14, 26))
    inner = c.polar_region(lambda t: a * (1 + math.cos(t)), 0, 2 * math.pi, n=120, opacity=0.10)
    inner += c.axes(xticks=(0, a), yticks=(), xlabel='x', ylabel='y')
    inner += c.polar_curve(lambda t: a * (1 + math.cos(t)), 0, 2 * math.pi, n=200, color=ROLE['rule'], width=2)
    t = math.pi / 3
    r = a * (1 + math.cos(t))
    inner += c.arrow(0, 0, r * math.cos(t), r * math.sin(t), color=ROLE['wrong'], width=1.6, head=6)
    inner += c.label(r * math.cos(t), r * math.sin(t), 'r = a(1 + cos theta)', color=ROLE['rule'], size=9, dy=-6)
    return c.svg(inner, cls='fig')


def circle_figure(a=1.0):
    """Figure: circle r = 2a cos(theta), upper half, with a sample radius."""
    c = Canvas(300, 170, (0, 2.15 * a), (-0.1 * a, 1.1 * a), pad=(34, 18, 14, 24))
    inner = c.polar_region(lambda t: 2 * a * math.cos(t), 0, math.pi / 2, n=90, opacity=0.10)
    inner += c.axes(xticks=(0, a, 2 * a), yticks=(), xlabel='x', ylabel='y')
    inner += c.polar_curve(lambda t: 2 * a * math.cos(t), 0, math.pi / 2, n=120, color=ROLE['data'], width=2)
    t = math.pi / 4
    r = 2 * a * math.cos(t)
    inner += c.arrow(0, 0, r * math.cos(t), r * math.sin(t), color=ROLE['wrong'], width=1.6, head=6)
    inner += c.label(r * math.cos(t), r * math.sin(t), 'r = 2a cos theta', color=ROLE['data'], size=9, dy=-6)
    return c.svg(inner, cls='fig')
