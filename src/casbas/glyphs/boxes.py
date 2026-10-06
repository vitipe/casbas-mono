"""Dibujo de cajas, bloques y separadores Powerline para la terminal.

Ocupan la celda entera de altura de línea (hhea: 1000 / −250) para empalmar entre
filas, y no se inclinan en la oblicua.
"""
from ..pen import arc, chevron, mirror_x, poly, rect, reverse
from ..registry import glyph

TOP, BOT = 1000, -250
YM = (TOP + BOT) / 2   # centro vertical de la celda
XM = 300


def light(g):
    return g.s * 0.8 + 10


def box(name, code):
    return glyph(name, code, upright=True)


def arms(t, dirs, cx=XM, cy=YM):
    """Líneas simples desde el centro hacia los bordes indicados (l r u d)."""
    out = []
    if "l" in dirs:
        out.append(rect(0, cy - t / 2, cx + t / 2, cy + t / 2))
    if "r" in dirs:
        out.append(rect(cx - t / 2, cy - t / 2, 600, cy + t / 2))
    if "u" in dirs:
        out.append(rect(cx - t / 2, cy - t / 2, cx + t / 2, TOP))
    if "d" in dirs:
        out.append(rect(cx - t / 2, BOT, cx + t / 2, cy + t / 2))
    return out


def double(g, dirs):
    """Líneas dobles. Cada brazo tiene dos líneas a ±gap; una línea llega hasta la
    esquina exterior si no hay brazo perpendicular de su lado, si no se detiene en
    la línea interior del brazo perpendicular."""
    t = g.s * 0.55 + 10
    gap = 55 + 0.5 * t
    out = []
    ext, stop = gap + t / 2, gap - t / 2   # distancias al centro donde acaba cada línea
    for d in dirs:
        for side in (+1, -1):
            if d in "lr":
                perp = "u" if side > 0 else "d"
                y = YM + side * gap
                if d == "l":
                    x0, x1 = 0, (XM - stop if perp in dirs else XM + ext)
                else:
                    x0, x1 = (XM + stop if perp in dirs else XM - ext), 600
                out.append(rect(x0, y - t / 2, x1, y + t / 2))
            else:
                perp = "r" if side > 0 else "l"
                x = XM + side * gap
                if d == "u":
                    y0 = YM + stop if perp in dirs else YM - ext
                    out.append(rect(x - t / 2, y0, x + t / 2, TOP))
                else:
                    y1 = YM - stop if perp in dirs else YM + ext
                    out.append(rect(x - t / 2, BOT, x + t / 2, y1))
    return out


LIGHT = {
    "boxlh": (0x2500, "lr"), "boxlv": (0x2502, "ud"),
    "boxdr": (0x250C, "rd"), "boxdl": (0x2510, "ld"), "boxur": (0x2514, "ru"), "boxul": (0x2518, "lu"),
    "boxvr": (0x251C, "udr"), "boxvl": (0x2524, "udl"), "boxdh": (0x252C, "lrd"), "boxuh": (0x2534, "lru"),
    "boxvh": (0x253C, "lrud"),
    "boxleft": (0x2574, "l"), "boxup": (0x2575, "u"), "boxright": (0x2576, "r"), "boxdown": (0x2577, "d"),
}
HEAVY = {
    "boxhh": (0x2501, "lr"), "boxhv": (0x2503, "ud"),
    "boxhdr": (0x250F, "rd"), "boxhdl": (0x2513, "ld"), "boxhur": (0x2517, "ru"), "boxhul": (0x251B, "lu"),
    "boxhvr": (0x2523, "udr"), "boxhvl": (0x252B, "udl"), "boxhdh": (0x2533, "lrd"), "boxhuh": (0x253B, "lru"),
    "boxhvh": (0x254B, "lrud"),
}
DOUBLE = {
    "boxdblh": (0x2550, "lr"), "boxdblv": (0x2551, "ud"),
    "boxdbldr": (0x2554, "rd"), "boxdbldl": (0x2557, "ld"), "boxdblur": (0x255A, "ru"), "boxdblul": (0x255D, "lu"),
    "boxdblvr": (0x2560, "udr"), "boxdblvl": (0x2563, "udl"), "boxdbldh": (0x2566, "lrd"), "boxdbluh": (0x2569, "lru"),
    "boxdblvh": (0x256C, "lrud"),
}

for _name, (_code, _dirs) in LIGHT.items():
    box(_name, _code)(lambda g, d=_dirs: arms(light(g), d))
for _name, (_code, _dirs) in HEAVY.items():
    box(_name, _code)(lambda g, d=_dirs: arms(light(g) * 2, d))
for _name, (_code, _dirs) in DOUBLE.items():
    box(_name, _code)(lambda g, d=_dirs: double(g, d))


# --------------------------------------------------------------------------- esquinas redondeadas

R = 160


@box("boxarcdr", 0x256D)
def boxarcdr(g):
    """╭: cuarto de círculo de la derecha hacia abajo."""
    t = light(g)
    cx, cy = XM + R, YM - R
    return [
        arc(cx, cy, R + t / 2, R + t / 2, t, t, 1, 2, k=0.5523),
        rect(cx - 1, YM - t / 2, 600, YM + t / 2),
        rect(XM - t / 2, BOT, XM + t / 2, cy + 1),
    ]


@box("boxarcdl", 0x256E)
def boxarcdl(g):
    return mirror_x(boxarcdr(g))


@box("boxarcul", 0x256F)
def boxarcul(g):
    from ..pen import mirror_y
    return mirror_x(mirror_y(boxarcdr(g), YM))


@box("boxarcur", 0x2570)
def boxarcur(g):
    from ..pen import mirror_y
    return mirror_y(boxarcdr(g), YM)


# --------------------------------------------------------------------------- bloques

@box("block", 0x2588)
def block(g):
    return [rect(0, BOT, 600, TOP)]


@box("upblock", 0x2580)
def upblock(g):
    return [rect(0, YM, 600, TOP)]


@box("dnblock", 0x2584)
def dnblock(g):
    return [rect(0, BOT, 600, YM)]


@box("lfblock", 0x258C)
def lfblock(g):
    return [rect(0, BOT, 300, TOP)]


@box("rtblock", 0x2590)
def rtblock(g):
    return [rect(300, BOT, 600, TOP)]


def pixels(pred):
    """Cuadrícula de 8×16 «píxeles» (75 × 78.125) para las tramas."""
    pw, ph = 600 / 8, (TOP - BOT) / 16
    return [(i * pw, BOT + j * ph, (i + 1) * pw, BOT + (j + 1) * ph)
            for j in range(16) for i in range(8) if pred(i, j)]


@box("shadelight", 0x2591)
def shadelight(g):
    return [rect(*p) for p in pixels(lambda i, j: i % 2 == 0 and j % 2 == 0)]


@box("shademedium", 0x2592)
def shademedium(g):
    return [rect(*p) for p in pixels(lambda i, j: (i + j) % 2 == 0)]


@box("shadedark", 0x2593)
def shadedark(g):
    holes = [reverse(rect(*p)) for p in pixels(lambda i, j: i % 2 == 1 and j % 2 == 1)]
    return [rect(0, BOT, 600, TOP)] + holes


# --------------------------------------------------------------------------- Powerline

@box("pl_right", 0xE0B0)
def pl_right(g):
    return [poly((0, BOT), (600, YM), (0, TOP))]


@box("pl_right_thin", 0xE0B1)
def pl_right_thin(g):
    return [chevron(600 - light(g), YM, (0, TOP), (0, BOT), light(g))]


@box("pl_left", 0xE0B2)
def pl_left(g):
    return mirror_x(pl_right(g))


@box("pl_left_thin", 0xE0B3)
def pl_left_thin(g):
    return mirror_x(pl_right_thin(g))
