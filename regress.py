"""Regresión visual: renderiza cada carácter por estilo y lo compara con snapshots/.

    .venv/bin/python regress.py            # informa qué glifos cambiaron
    .venv/bin/python regress.py --update   # acepta el estado actual como referencia
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONT = ROOT / "dist" / "CasbasMono[slnt,wght].ttf"
SNAP = ROOT / "snapshots"
SETTINGS = [(100, 0), (400, 0), (800, 0), (400, -10)]
SIZE, CELL_W, CELL_H, COLS = 64, 48, 96, 20
THRESHOLD = 12  # píxeles distintos tolerados por celda (ruido de antialiasing)


def chars_in_font():
    from fontTools.ttLib import TTFont
    cmap = TTFont(FONT).getBestCmap()
    return [chr(c) for c in sorted(cmap) if c > 0x20 and not 0x300 <= c < 0x370]


def render(chars, wght, slnt):
    f = ImageFont.truetype(str(FONT), SIZE)
    f.set_variation_by_axes([wght, slnt])
    rows = (len(chars) + COLS - 1) // COLS
    img = Image.new("L", (COLS * CELL_W, rows * CELL_H), 255)
    d = ImageDraw.Draw(img)
    for i, ch in enumerate(chars):
        x, y = (i % COLS) * CELL_W, (i // COLS) * CELL_H
        d.text((x + 4, y + 70), ch, fill=0, font=f, anchor="ls")
    return img


def cell(img, i):
    x, y = (i % COLS) * CELL_W, (i // COLS) * CELL_H
    return img.crop((x, y, x + CELL_W, y + CELL_H))


def main():
    update = "--update" in sys.argv
    chars = chars_in_font()
    SNAP.mkdir(exist_ok=True)
    changed, added = {}, set()
    for wght, slnt in SETTINGS:
        key = f"w{wght}_s{abs(slnt)}"
        img = render(chars, wght, slnt)
        png, idx = SNAP / f"{key}.png", SNAP / f"{key}.json"
        if not update and png.exists():
            old_img = Image.open(png).convert("L")
            old_chars = json.loads(idx.read_text())
            for i, ch in enumerate(chars):
                if ch not in old_chars:
                    added.add(ch)
                    continue
                diff = ImageChops.difference(cell(img, i), cell(old_img, old_chars.index(ch)))
                n = diff.point(lambda p: 255 if p > 40 else 0).histogram()[255]
                if n > THRESHOLD:
                    changed.setdefault(ch, []).append(key)
        if update or not png.exists():
            img.save(png)
            idx.write_text(json.dumps(chars, ensure_ascii=False))
    if update:
        print(f"snapshots actualizados ({len(chars)} caracteres × {len(SETTINGS)} estilos)")
        return
    if added:
        print("nuevos:", " ".join(sorted(added)))
    if changed:
        print("cambiaron:")
        for ch, keys in changed.items():
            print(f"  {ch!r:6} U+{ord(ch):04X}  {', '.join(keys)}")
    if not changed and not added:
        print("sin cambios visuales")


if __name__ == "__main__":
    main()
