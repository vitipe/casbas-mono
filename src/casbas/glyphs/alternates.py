"""Alternativas activables con features OpenType (ss01, ss02, zero).

En VS Code:  "editor.fontLigatures": "'calt', 'ss01', 'zero'"
"""
from ..pen import mirror_x, rect, ring, ring_oi, slant, arc_oi
from ..registry import GLYPHS, GlyphDef, composite, glyph
from .digits import zero
from .ligatures import equal_greater
from .lowercase import top_x

FEATURES = [
    ("ss01", "a y g de dos pisos", [("a", "a.ss01"), ("g", "g.ss01"), ("aacute", "aacute.ss01")]),
    ("ss02", "<= como flecha", [("less_equal.liga", "less_equal.arrow")]),
    ("zero", None, [("zero", "zero.zero")]),
]


@glyph("a.ss01", anchors=top_x)
def a_ss01(g):
    """a de dos pisos: panza baja + asta + gancho superior."""
    right = g.LR
    # gancho: medio arco superior que baja por la derecha hasta el asta
    hry = 160 + 0.15 * (g.s - 80)
    hcy = g.X + g.O - hry
    hl = 112
    hook = arc_oi(((hl + right) / 2, hcy, (right - hl) / 2, hry),
                  ((hl + right) / 2, hcy, (right - hl) / 2 - g.s, hry - g.h),
                  0, 1.62)
    # panza: más baja que la x, unida al asta con la unión adelgazada
    top = g.X * 0.6 + 0.2 * g.h
    cy, ry = (top - g.O) / 2, (top + g.O) / 2
    ol, orr = g.OL + 6, right - g.trap * g.s
    il, ir = ol + g.s, right - g.s
    bowl = ring_oi(((ol + orr) / 2, cy, (orr - ol) / 2, ry),
                   ((il + ir) / 2, cy, (ir - il) / 2, ry - g.h))
    return [hook, rect(right - g.s, 0, right, hcy)] + bowl


@glyph("g.ss01", anchors=top_x)
def g_ss01(g):
    """g de dos pisos (binocular): ojo superior, oreja, cuello y lazo inferior."""
    s, h = g.s * 0.92, g.h * 0.92
    ucx, urx, ury = 282, 150 + 0.15 * (g.s - 80), 158
    ucy = g.X - 25 - ury
    lcx, lrx, lry = 300, 214, 118 + 0.2 * (g.s - 80)
    lcy = g.D - g.O + lry
    neck_x = ucx - urx * 0.55
    return (
        ring(ucx, ucy, urx, ury, s, h)
        + ring(lcx, lcy, lrx, lry, s, h)
        + [
            rect(ucx + urx * 0.2, g.X - h, g.LR + 8, g.X),           # oreja
            slant(neck_x, lcy + lry - h * 0.5, neck_x + 10, ucy - ury + h * 0.5, s * 0.95),
        ]
    )


composite("aacute.ss01", None, ("a.ss01", 0, 0), ("acutecomb", 600, 0))


@glyph("zero.zero")
def zero_slashed(g):
    """Cero con barra diagonal (feature zero)."""
    out = zero(g)[:2]  # el anillo, sin el punto
    rx, ry = 212, g.C / 2 + g.O
    return out + [slant(300 - rx * 0.62, g.C / 2 - ry * 0.62, 300 + rx * 0.62, g.C / 2 + ry * 0.62,
                        g.s * 0.86)]


GLYPHS["less_equal.arrow"] = GlyphDef(
    "less_equal.arrow", None, draw=lambda g: mirror_x(equal_greater(g), about=0))


def alternates_fea(glyphs):
    out = []
    for tag, label, subs in FEATURES:
        subs = [(a, b) for a, b in subs if a in glyphs and b in glyphs]
        if not subs:
            continue
        names = f'  featureNames {{ name "{label}"; }};\n' if label else ""
        rules = "".join(f"  sub {a} by {b};\n" for a, b in subs)
        out.append(f"feature {tag} {{\n{names}{rules}}} {tag};\n")
    return "\n".join(out)
