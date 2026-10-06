"""Signos tipográficos del español y símbolos frecuentes (Latin-1 / puntuación general)."""
import dataclasses

from ..pen import arc, chevron, dot, rect, ring, rotate180, scale, stroke, translate
from ..registry import glyph
from .lowercase import a as a_glyph, o as o_glyph
from .punctuation import MATH_Y, comma_shape, plus


def top_of(shape):
    return max(y for c in shape for _, y, _ in c)


def bottom_of(shape):
    return min(y for c in shape for _, y, _ in c)


# --------------------------------------------------------------------------- comillas

def guillemet(g, x0, x1, half=135):
    """Ángulo de comilla angular apuntando a la izquierda, entre x0 (vértice) y x1."""
    return chevron(x0, g.X / 2, (x1, g.X / 2 + half), (x1, g.X / 2 - half), g.s * 0.8)


@glyph("guillemotleft", 0x00AB)
def guillemotleft(g):
    return [guillemet(g, 78, 248), guillemet(g, 318, 488)]


@glyph("guillemotright", 0x00BB)
def guillemotright(g):
    return rotate180(guillemotleft(g), 300, g.X / 2)


@glyph("guilsinglleft", 0x2039)
def guilsinglleft(g):
    return [guillemet(g, 205, 385)]


@glyph("guilsinglright", 0x203A)
def guilsinglright(g):
    return rotate180(guilsinglleft(g), 300, g.X / 2)


def quote_r(g):
    return 0.8 * g.dot_r


def curly(g, cx, top, opening):
    """Comilla curva: la coma (’) o la coma girada (‘), con la parte alta en `top`."""
    shape = comma_shape(g, cx=cx, r=quote_r(g), tail=125)
    if opening:
        mid = (top_of(shape) + bottom_of(shape)) / 2
        shape = rotate180(shape, cx, mid)
    return translate(shape, 0, top - top_of(shape))


QUOTE_TOP = 730
DOUBLE = 112  # separación de las comillas dobles respecto al centro


@glyph("quoteleft", 0x2018)
def quoteleft(g):
    return curly(g, 300, QUOTE_TOP, True)


@glyph("quoteright", 0x2019)
def quoteright(g):
    return curly(g, 300, QUOTE_TOP, False)


@glyph("quotedblleft", 0x201C)
def quotedblleft(g):
    return curly(g, 300 - DOUBLE, QUOTE_TOP, True) + curly(g, 300 + DOUBLE, QUOTE_TOP, True)


@glyph("quotedblright", 0x201D)
def quotedblright(g):
    return curly(g, 300 - DOUBLE, QUOTE_TOP, False) + curly(g, 300 + DOUBLE, QUOTE_TOP, False)


@glyph("quotesinglbase", 0x201A)
def quotesinglbase(g):
    return comma_shape(g, r=quote_r(g), tail=125)


@glyph("quotedblbase", 0x201E)
def quotedblbase(g):
    r = quote_r(g)
    return comma_shape(g, cx=300 - DOUBLE, r=r, tail=125) + comma_shape(g, cx=300 + DOUBLE, r=r, tail=125)


# --------------------------------------------------------------------------- rayas y puntos

@glyph("endash", 0x2013)
def endash(g):
    t = g.h * 1.02
    return [rect(48, MATH_Y - t / 2, 552, MATH_Y + t / 2)]


@glyph("emdash", 0x2014)
def emdash(g):
    # de borde a borde: varias rayas seguidas forman una línea continua
    t = g.h * 1.02
    return [rect(0, MATH_Y - t / 2, 600, MATH_Y + t / 2)]


@glyph("ellipsis", 0x2026)
def ellipsis(g):
    r = min(g.dot_r * 0.85, 64)
    return [dot(x, r, r) for x in (100, 300, 500)]


@glyph("periodcentered", 0x00B7)
def periodcentered(g):
    return [dot(300, MATH_Y, g.dot_r)]


@glyph("bullet", 0x2022)
def bullet(g):
    return [dot(300, MATH_Y, 62 + 0.42 * g.s)]


@glyph("nbspace", 0x00A0)
def nbspace(g):
    return []


# --------------------------------------------------------------------------- símbolos

@glyph("Euro", 0x20AC)
def Euro(g):
    cx, rx, ry = 330, 205, g.C / 2 + g.O
    t = g.h * 0.92
    gap = 62 + 0.3 * g.s
    return [
        arc(cx, g.C / 2, rx, ry, g.s, g.h, 0.42, 3.58),
        rect(42, g.C / 2 + gap / 2, 372, g.C / 2 + gap / 2 + t),
        rect(42, g.C / 2 - gap / 2 - t, 372, g.C / 2 - gap / 2),
    ]


@glyph("degree", 0x00B0)
def degree(g):
    r = 112 + 0.15 * g.s
    t = g.s * 0.78
    return ring(300, g.C + 20 - r, r, r, t, t)


@glyph("plusminus", 0x00B1)
def plusminus(g):
    t = g.s * 0.92
    return translate(plus(g), 0, 70) + [rect(95, MATH_Y - 255 - t / 2, 505, MATH_Y - 255 + t / 2)]


@glyph("multiply", 0x00D7)
def multiply(g):
    d = 150
    w = g.s * 0.92
    return [stroke(300 - d, MATH_Y - d, 300 + d, MATH_Y + d, w),
            stroke(300 - d, MATH_Y + d, 300 + d, MATH_Y - d, w)]


@glyph("divide", 0x00F7)
def divide(g):
    t = g.h
    r = g.dot_r
    off = 120 + 0.25 * g.s
    return [rect(95, MATH_Y - t / 2, 505, MATH_Y + t / 2),
            dot(300, MATH_Y + off, r), dot(300, MATH_Y - off, r)]


def ordinal(g, letter_fn):
    """ª º: letra a ~60 % con trazo compensado, elevada, con subrayado."""
    k = 0.6
    # compensar el trazo al escalar: ~0.8·s en pesos finos, menos en gruesos (si no, empasta)
    heavy = dataclasses.replace(g, s=g.s * (1.32 - 0.3 * (g.s - 22) / 118))
    small = scale(letter_fn(heavy), k, k, ox=300, oy=0)
    lift = 360
    return translate(small, 0, lift) + [rect(150, lift - 75 - g.h * 0.8, 450, lift - 75)]


@glyph("ordfeminine", 0x00AA)
def ordfeminine(g):
    return ordinal(g, a_glyph)


@glyph("ordmasculine", 0x00BA)
def ordmasculine(g):
    return ordinal(g, o_glyph)
