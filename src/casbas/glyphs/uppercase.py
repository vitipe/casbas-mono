"""Mayúsculas A–Z."""
from ..pen import arc, param_at, rect, ring, slant, slant_centers, x_at
from ..registry import glyph
from .lowercase import s_shape


def top_c(g):
    return [("top", 300, g.C)]


def caps(name):
    return glyph(name, name, anchors=top_c)


def stem(g, x0, y0=0, y1=None, s=None):
    return rect(x0, y0, x0 + (s or g.s), g.C if y1 is None else y1)


def right_bowl(g, left, right, bottom, top):
    """Panza derecha (B, D, P, R): barras horizontales + medio anillo a la derecha."""
    ry = (top - bottom) / 2
    rx = min(ry * 1.02, right - left - g.s)
    cx = right - rx
    return [
        rect(left, top - g.h, cx, top),
        rect(left, bottom, cx, bottom + g.h),
        arc(cx, bottom + ry, rx, ry, g.s, g.h, -1, 1),
    ]


# --------------------------------------------------------------------------- rectas

@caps("E")
def E(g):
    ym = g.C * 0.52
    return [stem(g, g.CL), rect(g.CL, g.C - g.h, g.CR - 8, g.C),
            rect(g.CL, ym - g.h / 2, g.CR - 40, ym + g.h / 2), rect(g.CL, 0, g.CR + 2, g.h)]


@caps("F")
def F(g):
    ym = g.C * 0.50
    return [stem(g, g.CL), rect(g.CL, g.C - g.h, g.CR - 4, g.C),
            rect(g.CL, ym - g.h / 2, g.CR - 40, ym + g.h / 2)]


@caps("H")
def H(g):
    ym = g.C * 0.52
    return [stem(g, g.CL), stem(g, g.CR - g.s), rect(g.CL, ym - g.h / 2, g.CR, ym + g.h / 2)]


@caps("I")
def I(g):
    return [stem(g, 300 - g.s / 2), rect(118, g.C - g.h, 482, g.C), rect(118, 0, 482, g.h)]


@caps("L")
def L(g):
    return [stem(g, g.CL + 12), rect(g.CL + 12, 0, g.CR + 4, g.h)]


@caps("T")
def T(g):
    return [stem(g, 300 - g.s / 2), rect(g.CL - 10, g.C - g.h, g.CR + 10, g.C)]


# --------------------------------------------------------------------------- panzas

@caps("B")
def B(g):
    ym = g.C * 0.54
    top = right_bowl(g, g.CL, g.CR - 26, ym - g.h / 2, g.C)
    bot = right_bowl(g, g.CL, g.CR, 0, ym + g.h / 2)
    return [stem(g, g.CL)] + top + bot


@caps("D")
def D(g):
    rx = 250
    cx = g.CR - rx
    return [
        stem(g, g.CL),
        rect(g.CL, g.C - g.h, cx, g.C),
        rect(g.CL, 0, cx, g.h),
        arc(cx, g.C / 2, rx, g.C / 2, g.s, g.h, -1, 1),
    ]


@caps("P")
def P(g):
    ym = g.C * 0.42
    return [stem(g, g.CL)] + right_bowl(g, g.CL, g.CR, ym - g.h / 2, g.C)


@caps("R")
def R(g):
    ym = g.C * 0.44
    bowl = right_bowl(g, g.CL, g.CR - 8, ym - g.h / 2, g.C)
    leg_x = (g.CR - 8) - (g.C - ym + g.h / 2) / 2 * 1.02  # centro de la panza
    return [stem(g, g.CL)] + bowl + [slant(g.CR + 8, 0, leg_x + g.s * 0.2, ym, g.s * 1.0, "r", "c")]


# --------------------------------------------------------------------------- redondas

def round_box(g):
    return 300, g.C / 2, (g.COR - g.COL) / 2, g.C / 2 + g.O


@caps("O")
def O(g):
    cx, cy, rx, ry = round_box(g)
    return ring(cx, cy, rx, ry, g.s, g.h)


@caps("Q")
def Q(g):
    return O(g) + [slant(g.COR + 10, -150, 360, 150, g.s * 1.0, "r", "c")]


@caps("C")
def C(g):
    cx, cy, rx, ry = round_box(g)
    return [arc(cx, cy, rx, ry, g.s, g.h, 0.44, 3.56)]


@caps("G")
def G(g):
    cx, cy, rx, ry = round_box(g)
    bar_top = cy + g.h * 0.3
    a1 = param_at(cx, cy, rx, ry, 4, 4.4, y=bar_top)
    return [
        arc(cx, cy, rx, ry, g.s, g.h, 0.44, a1, cut1="h"),
        rect(310, bar_top - g.h, g.COR - g.s * 0.5, bar_top),
    ]


@caps("S")
def S(g):
    return s_shape(g, g.C, top_rx=205, bot_rx=226, sw=g.s, spine=0.535)


@caps("U")
def U(g):
    ry = 245
    cy = ry - g.O
    return [stem(g, g.CL, cy), stem(g, g.CR - g.s, cy),
            arc(300, cy, (g.CR - g.CL) / 2, ry, g.s, g.h, 2, 4)]


@caps("J")
def J(g):
    right = g.CR - 14
    rx = 200 + 0.3 * (g.s - 80)
    ry = 210
    cy = ry - g.O
    return [
        stem(g, right - g.s, cy),
        rect(150, g.C - g.h, right, g.C),
        arc(right - rx, cy, rx, ry, g.s, g.h, 2.42, 4),
    ]


# --------------------------------------------------------------------------- diagonales

@caps("A")
def A(g):
    w = g.s * 1.0
    l0, l1, _ = slant_centers(g.CL - 12, 0, 300, g.C, w, "l", "c")
    r0, r1, _ = slant_centers(g.CR + 12, 0, 300, g.C, w, "r", "c")
    by = g.C * 0.25
    return [
        slant(g.CL - 12, 0, 300, g.C, w, "l", "c"),
        slant(g.CR + 12, 0, 300, g.C, w, "r", "c"),
        rect(x_at(l0, 0, l1, g.C, by + g.h), by, x_at(r0, 0, r1, g.C, by + g.h), by + g.h),
    ]


@caps("V")
def V(g):
    w = g.s * 1.0
    return [slant(300, 0, g.CL - 12, g.C, w, "c", "l"), slant(300, 0, g.CR + 12, g.C, w, "c", "r")]


@caps("W")
def W(g):
    sw = g.s * 0.78
    lb, rb = 172, 428
    peak = g.C * 0.66
    return [
        slant(lb, 0, 40, g.C, sw, "c", "l"),
        slant(lb, 0, 300, peak, sw, "c", "c"),
        slant(rb, 0, 300, peak, sw, "c", "c"),
        slant(rb, 0, 560, g.C, sw, "c", "r"),
    ]


@caps("X")
def X(g):
    w = g.s * 1.0
    return [slant(g.CL - 6, 0, g.CR + 6, g.C, w, "l", "r"),
            slant(g.CR + 6, 0, g.CL - 6, g.C, w, "r", "l")]


@caps("Y")
def Y(g):
    w = g.s * 1.0
    jy = g.C * 0.40
    return [
        rect(300 - g.s / 2, 0, 300 + g.s / 2, jy),
        slant(300, jy, g.CL - 12, g.C, w, "c", "l"),
        slant(300, jy, g.CR + 12, g.C, w, "c", "r"),
    ]


@caps("Z")
def Z(g):
    return [
        rect(g.CL + 8, g.C - g.h, g.CR - 4, g.C),
        rect(g.CL, 0, g.CR + 4, g.h),
        slant(g.CL, g.h, g.CR - 4, g.C - g.h, g.s * 1.04, "l", "r"),
    ]


@caps("K")
def K(g):
    w = g.s * 0.98
    jy = g.C * 0.22
    a0, a1, _ = slant_centers(g.CL + g.s * 0.72, jy, g.CR + 6, g.C, w, "c", "r")
    ly = g.C * 0.52
    return [
        stem(g, g.CL),
        slant(g.CL + g.s * 0.72, jy, g.CR + 6, g.C, w, "c", "r"),
        slant(g.CR + 14, 0, x_at(a0, jy, a1, g.C, ly), ly, w, "r", "c"),
    ]


@caps("M")
def M(g):
    sm = g.s * 0.86
    vy = g.C * 0.28
    w = g.s * 0.84
    return [
        stem(g, g.CL - 10, s=sm),
        stem(g, g.CR + 10 - sm, s=sm),
        slant(300, vy, g.CL - 10, g.C, w, "c", "l"),
        slant(300, vy, g.CR + 10, g.C, w, "c", "r"),
    ]


@caps("N")
def N(g):
    sn = g.s * 0.9
    return [
        stem(g, g.CL, s=sn),
        stem(g, g.CR - sn, s=sn),
        slant(g.CR, 0, g.CL, g.C, g.s * 0.98, "r", "l"),
    ]
