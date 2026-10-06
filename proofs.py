"""Pruebas PNG renderizadas con FreeType (Pillow) a varios pesos e inclinaciones."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LINES = [
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0123456789 0O 1lI| ;: '\"`",
    "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~",
    "áéíóúüñ ÁÉÍÓÚÜÑ ¿Qué? ¡Sí!",
    "fn main() { let x = a[i] + 0x1F; }",
]
SETTINGS = [(100, 0), (400, 0), (800, 0), (400, -10), (800, -10)]


def _font(path, size, wght, slnt):
    f = ImageFont.truetype(str(path), size)
    f.set_variation_by_axes([wght, slnt])
    return f


def render_proofs(path, out_dir: Path):
    out_dir.mkdir(exist_ok=True)
    size, lh = 34, 46
    w = 30 + 36 * size * 0.6 + 30
    h = 20 + len(SETTINGS) * (len(LINES) * lh + 30)
    img = Image.new("L", (int(w), int(h)), 255)
    d = ImageDraw.Draw(img)
    y = 20
    for wght, slnt in SETTINGS:
        d.text((8, y - 14), f"wght {wght} slnt {slnt}", fill=150,
               font=ImageFont.load_default())
        f = _font(path, size, wght, slnt)
        for line in LINES:
            d.text((30, y), line, fill=0, font=f)
            y += lh
        y += 30
    img.save(out_dir / "overview.png")

    # hoja de glifos grande con guías, una por peso extremo
    chars = [chr(c) for c in range(0x21, 0x7F)] + list("áéíóúüñÁÉÍÓÚÜÑ¿¡")
    big, cell_w, cell_h, cols = 110, 74, 150, 16
    for wght, slnt in [(100, 0), (400, 0), (800, 0)]:
        f = _font(path, big, wght, slnt)
        rows = (len(chars) + cols - 1) // cols
        img = Image.new("L", (cols * cell_w + 20, rows * cell_h + 20), 255)
        d = ImageDraw.Draw(img)
        for i, ch in enumerate(chars):
            cx = 10 + (i % cols) * cell_w
            cy = 10 + (i // cols) * cell_h
            base = cy + 110
            for frac, shade in [(0, 200), (0.53, 225), (0.70, 225)]:
                yy = base - frac * big
                d.line([(cx, yy), (cx + cell_w - 4, yy)], fill=shade)
            d.text((cx + 4, base), ch, fill=0, font=f, anchor="ls")
        img.save(out_dir / f"glyphs-{wght}.png")
    print(f"→ pruebas en {out_dir}")
