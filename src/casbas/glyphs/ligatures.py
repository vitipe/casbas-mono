"""Ligaduras de programación (feature calt, ver ligatures_fea.py).

Un glifo `.liga` de n caracteres tiene avance 600 y se dibuja en x ∈ [-600·(n-1), 600]:
ocupa visualmente las n celdas, colocado en la última.
"""
from ..pen import chevron, mirror_x, rect, slant
from ..registry import GLYPHS, GlyphDef, glyph
from .punctuation import MATH_Y, equal_bars

LIGATURES = [
    (["hyphen", "greater"], "hyphen_greater.liga"),
    (["less", "hyphen"], "less_hyphen.liga"),
    (["equal", "greater"], "equal_greater.liga"),
    (["equal", "equal"], "equal_equal.liga"),
    (["equal", "equal", "equal"], "equal_equal_equal.liga"),
    (["exclam", "equal"], "exclam_equal.liga"),
    (["exclam", "equal", "equal"], "exclam_equal_equal.liga"),
    (["greater", "equal"], "greater_equal.liga"),
    (["less", "equal"], "less_equal.liga"),
    (["colon", "colon"], "colon_colon.liga"),
    (["slash", "slash"], "slash_slash.liga"),
    (["bar", "bar"], "bar_bar.liga"),
    (["bar", "greater"], "bar_greater.liga"),
]

GLYPHS["LIG"] = GlyphDef("LIG", None, draw=lambda g: [])


def triple_bars(g, x0, x1):
    t = g.h
    gap = 70 + 0.3 * g.s
    step = t + gap
    return [rect(x0, MATH_Y + d - t / 2, x1, MATH_Y + d + t / 2) for d in (-step, 0, step)]


def arrow_head(g, tip_x, back_x, spread):
    return chevron(tip_x, MATH_Y, (back_x, MATH_Y + spread), (back_x, MATH_Y - spread), g.s * 0.95)


@glyph("hyphen_greater.liga")
def hyphen_greater(g):
    t = g.h * 1.02
    return [rect(-490, MATH_Y - t / 2, 470, MATH_Y + t / 2), arrow_head(g, 520, 270, 215)]


@glyph("less_hyphen.liga")
def less_hyphen(g):
    return mirror_x(hyphen_greater(g), about=0)


@glyph("equal_greater.liga")
def equal_greater(g):
    tip, back, spread = 520, 205, 245
    bars = equal_bars(g, -490, 0)
    out = []
    for c in bars:
        ys = [y for _, y, _ in c]
        yc = (min(ys) + max(ys)) / 2
        x_arm = tip - (tip - back) * abs(yc - MATH_Y) / spread
        out.append(rect(-490, min(ys), x_arm, max(ys)))
    return out + [arrow_head(g, tip, back, spread)]


@glyph("equal_equal.liga")
def equal_equal(g):
    return equal_bars(g, -495, 495)


@glyph("equal_equal_equal.liga")
def equal_equal_equal(g):
    return triple_bars(g, -1095, 495)


def neq_slash(g, cx):
    return slant(cx - 125, MATH_Y - 270, cx + 125, MATH_Y + 270, g.s * 0.92)


@glyph("exclam_equal.liga")
def exclam_equal(g):
    return equal_bars(g, -495, 495) + [neq_slash(g, 0)]


@glyph("exclam_equal_equal.liga")
def exclam_equal_equal(g):
    return triple_bars(g, -1095, 495) + [neq_slash(g, -300)]


@glyph("greater_equal.liga")
def greater_equal(g):
    vy = MATH_Y + 75
    return [
        chevron(275, vy, (-265, vy + 200), (-265, vy - 200), g.s * 0.95),
        rect(-275, MATH_Y - 235 - g.h, 275, MATH_Y - 235),
    ]


@glyph("less_equal.liga")
def less_equal(g):
    return mirror_x(greater_equal(g), about=0)


@glyph("bar_greater.liga")
def bar_greater(g):
    bx, spread = -330, 255
    return [
        rect(bx - g.s / 2, MATH_Y - spread - g.s * 0.35, bx + g.s / 2, MATH_Y + spread + g.s * 0.35),
        chevron(440, MATH_Y, (bx, MATH_Y + spread), (bx, MATH_Y - spread), g.s * 0.95),
    ]


def tight_pair(name, base, offset):
    """Ligadura por componentes: dos copias del glifo base acercadas al centro."""
    GLYPHS[name] = GlyphDef(name, None, components=[(base, -600 + offset, 0), (base, -offset, 0)])


tight_pair("colon_colon.liga", "colon", 175)
tight_pair("slash_slash.liga", "slash", 165)
tight_pair("bar_bar.liga", "bar", 160)
