"""Dígitos 0–9 (cero con punto)."""
from ..pen import (arc, arc_end, ellipse, param_at, poly, rect, ring, rotate180, slant)
from ..registry import glyph

NAMES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def digit(n):
    return glyph(NAMES[n], str(n))


@digit(0)
def zero(g):
    rx, ry = 212, g.C / 2 + g.O
    inner = rx - g.s
    drx = min(0.36 * g.s + 16, 0.42 * inner)
    return ring(300, g.C / 2, rx, ry, g.s, g.h) + [ellipse(300, g.C / 2, drx, drx * 1.35)]


@digit(1)
def one(g):
    cx = 318
    left = cx - g.s / 2
    return [
        rect(left, 0, left + g.s, g.C),
        slant(118, g.C - 175, left + g.s * 0.6, g.C, g.s * 0.92, "l", "c"),
        rect(110, 0, 500, g.h),
    ]


@digit(2)
def two(g):
    rx, ry = 205, 190 + 0.2 * (g.s - 80)
    cy = g.C + g.O - ry
    a0 = -0.42
    # la diagonal nace exactamente del corte del arco: unión sin costura
    (ox, oy), (ix, iy) = arc_end(300, cy, rx, ry, g.s, g.h, a0)
    w = g.s * 1.02
    yb = g.h * 0.5
    dx, dy = (ox + ix) / 2 - g.CL, (oy + iy) / 2 - yb
    hw = w * (dx * dx + dy * dy) ** 0.5 / abs(dy)  # ancho horizontal del trazo
    return [
        arc(300, cy, rx, ry, g.s, g.h, a0, 2.06),
        poly((ox, oy), (ix, iy), (g.CL, yb), (g.CL + hw, yb)),
        rect(g.CL, 0, g.CR + 4, g.h),
    ]


@digit(3)
def three(g):
    ym = g.C * 0.56
    h = g.h
    ry1 = (g.C + g.O - (ym - h / 2)) / 2
    cy1 = g.C + g.O - ry1
    ry2 = (ym + h / 2 + g.O) / 2
    cy2 = ry2 - g.O
    return [
        arc(292, cy1, 196, ry1, g.s, h, -1, 1.62),
        arc(300, cy2, 218, ry2, g.s, h, 2.4, 5),
        rect(210, ym - h / 2, 300, ym + h / 2),
    ]


@digit(4)
def four(g):
    sx = 372
    by = g.C * 0.26
    return [
        rect(sx, 0, sx + g.s, g.C),
        rect(g.CL - 6, by, g.CR + 8, by + g.h),
        slant(g.CL - 6, by + g.h * 0.5, sx + g.s * 0.35, g.C, g.s * 0.94, "l", "c"),
    ]


@digit(5)
def five(g):
    rx, ry = 216, 238
    cy = ry - g.O
    left = 118
    a1 = param_at(300, cy, rx, ry, 5.0, 5.999, x=left + g.s * 0.5)
    top_y = cy + ry * 0.62
    return [
        arc(300, cy, rx, ry, g.s, g.h, 2.42, a1, cut1="v"),
        rect(left, top_y, left + g.s, g.C),
        rect(left, g.C - g.h, g.CR - 6, g.C),
    ]


@digit(6)
def six(g):
    rx, ry = 214, 232
    cy = ry - g.O
    big_ry = g.C + g.O - cy
    return ring(300, cy, rx, ry, g.s, g.h) + [
        arc(300, cy, rx, big_ry, g.s, g.h, 0.52, 2),
    ]


@digit(7)
def seven(g):
    return [
        rect(g.CL - 4, g.C - g.h, g.CR + 6, g.C),
        slant(205, 0, g.CR + 6, g.C - g.h, g.s * 1.0, "c", "r"),
    ]


@digit(8)
def eight(g):
    ym = g.C * 0.55
    h = g.h
    ry1 = (g.C + g.O - (ym - h / 2)) / 2
    ry2 = (ym + h / 2 + g.O) / 2
    return (ring(300, g.C + g.O - ry1, 192, ry1, g.s * 0.95, h)
            + ring(300, ry2 - g.O, 216, ry2, g.s, h))


@digit(9)
def nine(g):
    return rotate180(six(g), 300, g.C / 2)
