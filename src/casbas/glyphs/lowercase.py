"""Minúsculas a–z (+ ı sin punto)."""
import math

from ..pen import (arc, dot, ellipse_point, mirror_x, param_at, rect, ring, rotate180,
                   slant, slant_centers, x_at)
from ..registry import glyph


def top_x(g):
    return [("top", 300, g.X)]


def top_asc(g):
    return [("top", 300, g.A)]


# --------------------------------------------------------------------------- helpers

def bowl(g, left, right):
    """Panza ovalada de altura x entre left y right (borde exterior)."""
    return ring((left + right) / 2, g.X / 2, (right - left) / 2, g.X / 2 + g.O, g.s, g.h)


def arch(g, left, right, s=None, h=None, ry=230):
    """Hombro de n/h/m: medio anillo superior. Devuelve (contorno, y del arranque)."""
    s = s or g.s
    h = h or g.h
    top = g.X + g.O
    cy = top - ry
    return arc((left + right) / 2, cy, (right - left) / 2, ry, s, h, 0, 2), cy


def ellipse_x(cx, rx, cy, ry, y):
    """x del borde derecho de una elipse a la altura y (aprox. elipse verdadera)."""
    t = max(0.0, 1 - ((y - cy) / ry) ** 2)
    return cx + rx * math.sqrt(t)


def i_dot(g, cx=300):
    r = g.dot_r
    return dot(cx, g.X + 70 + r, r)


def tail(g, stem_left, rx=175, ry=165, end=3.5):
    """Cola inferior hacia la derecha (l, t). Devuelve (contorno, y del arranque)."""
    rx, ry = rx + 0.45 * (g.s - 80), ry + 0.35 * (g.s - 80)  # más abierta en pesos gruesos
    cy = ry - g.O
    return arc(stem_left + rx, cy, rx, ry, g.s, g.h, 2, end), cy


# --------------------------------------------------------------------------- redondas

@glyph("a", "a", anchors=top_x)
def a(g):
    return bowl(g, g.OL, g.LR) + [rect(g.LR - g.s, 0, g.LR, g.X)]


@glyph("b", "b", anchors=top_asc)
def b(g):
    return mirror_x(d(g))


@glyph("c", "c", anchors=top_x)
def c(g):
    rx = (g.OR - g.OL) / 2
    return [arc(300, g.X / 2, rx, g.X / 2 + g.O, g.s, g.h, 0.46, 3.54)]


@glyph("d", "d", anchors=top_asc)
def d(g):
    return bowl(g, g.OL, g.LR) + [rect(g.LR - g.s, 0, g.LR, g.A)]


@glyph("e", "e", anchors=top_x)
def e(g):
    rx = (g.OR - g.OL) / 2
    ry = g.X / 2 + g.O
    cy = g.X / 2
    bar_bot = cy - g.h * 0.35
    bar_top = bar_bot + g.h
    a0 = param_at(300, cy, rx, ry, -0.5, 0, y=bar_bot)
    return [
        arc(300, cy, rx, ry, g.s, g.h, a0, 3.58, cut0="h"),
        rect(g.OL + g.s * 0.5, bar_bot, g.OR - g.s * 0.5, bar_top),
    ]


@glyph("g", "g", anchors=top_x)
def g_(g):
    ry = 185
    cy = g.D - g.O + ry
    cx = (g.OL + g.LR) / 2
    rx = (g.LR - g.OL) / 2
    return bowl(g, g.OL, g.LR) + [
        rect(g.LR - g.s, cy, g.LR, g.X),
        arc(cx, cy, rx, ry, g.s, g.h, 2.45, 4),
    ]


@glyph("o", "o", anchors=top_x)
def o(g):
    return bowl(g, g.OL, g.OR)


@glyph("p", "p", anchors=top_x)
def p(g):
    return mirror_x(q(g))


@glyph("q", "q", anchors=top_x)
def q(g):
    return bowl(g, g.OL, g.LR) + [rect(g.LR - g.s, g.D, g.LR, g.X)]


@glyph("s", "s", anchors=top_x)
def s(g):
    return s_shape(g, g.X, top_rx=198, bot_rx=214, sw=g.s * 0.94)


def s_shape(g, height, top_rx, bot_rx, sw, spine=0.53):
    h = g.h * 0.96
    ym = height * spine
    ry1 = (height + g.O - ym + h / 2) / 2
    cy1 = height + g.O - ry1
    ry2 = (ym + h / 2 + g.O) / 2
    cy2 = ry2 - g.O
    return [
        arc(300, cy1, top_rx, ry1, sw, h, 0.42, 3),
        arc(300, cy2, bot_rx, ry2, sw, h, 2.42, 5),
    ]


# --------------------------------------------------------------------------- astas + hombros

@glyph("h", "h", anchors=top_asc)
def h(g):
    sh, cy = arch(g, g.LL, g.LR)
    return [rect(g.LL, 0, g.LL + g.s, g.A), sh, rect(g.LR - g.s, 0, g.LR, cy)]


@glyph("n", "n", anchors=top_x)
def n(g):
    sh, cy = arch(g, g.LL, g.LR)
    return [rect(g.LL, 0, g.LL + g.s, g.X), sh, rect(g.LR - g.s, 0, g.LR, cy)]


@glyph("m", "m", anchors=top_x)
def m(g):
    sm = g.s * 0.74
    hm = g.h * 0.82
    left, right = 62, 538
    mid0 = 300 - sm / 2
    a1, cy = arch(g, left, mid0 + sm, sm, hm, ry=200)
    a2, _ = arch(g, mid0, right, sm, hm, ry=200)
    return [
        rect(left, 0, left + sm, g.X),
        rect(mid0, 0, mid0 + sm, cy),
        rect(right - sm, 0, right, cy),
        a1, a2,
    ]


@glyph("r", "r", anchors=top_x)
def r(g):
    left = 132
    rx = (522 - left) / 2
    ry = 235
    cy = g.X + g.O - ry
    return [
        rect(left, 0, left + g.s, g.X),
        arc(left + rx, cy, rx, ry, g.s, g.h * 0.95, 0.5, 2),
    ]


@glyph("u", "u", anchors=top_x)
def u(g):
    return rotate180(n(g), 300, g.X / 2)


# --------------------------------------------------------------------------- astas con remates

@glyph("dotlessi", 0x0131, anchors=top_x)
def dotlessi(g):
    sx = 300 - g.s / 2
    return [
        rect(sx, 0, sx + g.s, g.X),
        rect(132, g.X - g.h, sx + g.s, g.X),
        rect(105, 0, 495, g.h),
    ]


@glyph("i", "i", anchors=top_x)
def i(g):
    return dotlessi(g) + [i_dot(g)]


@glyph("j", "j", anchors=top_x)
def j(g):
    jc = 362
    right = jc + g.s / 2
    rx, ry = 195, 175
    cy = g.D - g.O + ry
    return [
        rect(right - g.s, cy, right, g.X),
        rect(120, g.X - g.h, right, g.X),
        arc(right - rx, cy, rx, ry, g.s, g.h, 2.5, 4),
        i_dot(g, jc),
    ]


@glyph("l", "l", anchors=top_asc)
def l(g):
    lc = 268
    left = lc - g.s / 2
    t, cy = tail(g, left, rx=180, ry=170)
    return [
        rect(left, cy, left + g.s, g.A),
        rect(118, g.A - g.h, left + g.s, g.A),
        t,
    ]


@glyph("f", "f", anchors=top_asc)
def f(g):
    fc = 262
    left = fc - g.s / 2
    rx, ry = 175 + 0.45 * (g.s - 80), 165 + 0.35 * (g.s - 80)
    cy = g.A + g.O - ry
    return [
        rect(left, 0, left + g.s, cy),
        arc(left + rx, cy, rx, ry, g.s, g.h, 0.5, 2),
        rect(100, g.X - g.h, 492, g.X),
    ]


@glyph("t", "t", anchors=top_x)
def t(g):
    tc = 252
    left = tc - g.s / 2
    tl, cy = tail(g, left, rx=180, ry=170)
    return [
        rect(left, cy, left + g.s, 665),
        rect(92, g.X - g.h, 500, g.X),
        tl,
    ]


# --------------------------------------------------------------------------- diagonales

@glyph("k", "k", anchors=top_asc)
def k(g):
    w = g.s * 0.94
    jy = g.X * 0.16
    a0, a1, _ = slant_centers(g.LL + g.s * 0.72, jy, g.LR + 4, g.X, w, "c", "r")
    ly = g.X * 0.5
    return [
        rect(g.LL, 0, g.LL + g.s, g.A),
        slant(g.LL + g.s * 0.72, jy, g.LR + 4, g.X, w, "c", "r"),
        slant(g.LR + 12, 0, x_at(a0, jy, a1, g.X, ly), ly, w, "r", "c"),
    ]


def v_shape(g, height, left, right, w, bottom=0):
    return [
        slant(300, bottom, left, height, w, "c", "l"),
        slant(300, bottom, right, height, w, "c", "r"),
    ]


@glyph("v", "v", anchors=top_x)
def v(g):
    return v_shape(g, g.X, 70, 530, g.s * 0.98)


@glyph("w", "w", anchors=top_x)
def w(g):
    return w_shape(g, g.X, peak=g.X * 0.78)


def w_shape(g, height, peak):
    sw = g.s * 0.76
    lb, rb = 178, 422
    return [
        slant(lb, 0, 46, height, sw, "c", "l"),
        slant(lb, 0, 300, peak, sw, "c", "c"),
        slant(rb, 0, 300, peak, sw, "c", "c"),
        slant(rb, 0, 554, height, sw, "c", "r"),
    ]


@glyph("x", "x", anchors=top_x)
def x(g):
    sw = g.s * 0.95
    return [
        slant(76, 0, 524, g.X, sw, "l", "r"),
        slant(524, 0, 76, g.X, sw, "r", "l"),
    ]


@glyph("y", "y", anchors=top_x)
def y(g):
    sw = g.s * 0.98
    c0, c1, _ = slant_centers(150, g.D, 530, g.X, sw, "c", "r")
    xb = x_at(c0, g.D, c1, g.X, 0)
    return [
        slant(150, g.D, 530, g.X, sw, "c", "r"),
        slant(xb, 0, 70, g.X, sw, "c", "l"),
    ]


@glyph("z", "z", anchors=top_x)
def z(g):
    return [
        rect(g.LL + 12, g.X - g.h, g.LR - 6, g.X),
        rect(g.LL, 0, g.LR + 4, g.h),
        slant(g.LL, g.h, g.LR - 6, g.X - g.h, g.s * 1.02, "l", "r"),
    ]
