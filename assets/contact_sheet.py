"""contact_sheet.py <book.pdf> [out.png] [cols] — visual QA thumbnail grid.

Renders every page to a small pixmap and tiles them with page numbers, so a
human can spot clipping, overflow, stranded headings and wrong-looking figures
in one image. Run this after preflight; it checks what a text-only script
cannot see.

Rendering uses PyMuPDF pixmaps ONLY. Do not use PyMuPDF for text extraction in
this toolkit: mupdf 1.28+ takes 4-10 s per page on WeasyPrint 70 output.

Needs: pip install pymupdf pillow
"""
import sys, math
import pymupdf
from PIL import Image, ImageDraw, ImageFont

pdf = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else 'contact_sheet.png'
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
scale = 0.34

doc = pymupdf.open(pdf)
thumbs = []
for pg in doc:
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
    thumbs.append(Image.frombytes('RGB', (pix.width, pix.height), pix.samples))

tw, th = thumbs[0].size
label_h = 22
rows = math.ceil(len(thumbs) / cols)
sheet = Image.new('RGB', (cols * (tw + 8) + 8, rows * (th + label_h + 8) + 8), '#e9ecf7')
draw = ImageDraw.Draw(sheet)
try:
    font = ImageFont.load_default()
except Exception:
    font = None

for i, img in enumerate(thumbs):
    r, c = divmod(i, cols)
    x = 8 + c * (tw + 8)
    y = 8 + r * (th + label_h + 8)
    sheet.paste(img, (x, y))
    draw.rectangle((x, y + th, x + tw, y + th + label_h), fill='#1b1f4b')
    draw.text((x + 6, y + th + 5), f'page {i+1}', fill='white', font=font)
    draw.rectangle((x, y, x + tw, y + th), outline='#b8bfd4')

sheet.save(out)
print(f'wrote {out} | {len(thumbs)} pages | {cols} cols | {sheet.width}x{sheet.height}px')
