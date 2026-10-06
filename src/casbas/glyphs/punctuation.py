"""Puntuación y símbolos ASCII + ¿ ¡."""
from ..pen import (arc, chevron, dot, ellipse, ellipse_point, mirror_x, mirror_y, rect,
                   reverse, ring, rotate180, slant, stroke, translate)
from ..registry import glyph
from .lowercase import s_shape

MATH_Y = 330  # eje de + − = < > ~


@glyph(".notdef")
def notdef(g):
    t = max(g.s * 0.6, 30)
    return [rect(80, 0, 520, g.C), reverse(rect(80 + t, t, 520 - t, g.C - t))]


@glyph("space", " ")
def space(g):
    return []


# --------------------------------------------------------------------------- puntos

def period_shape(g, cx=300, y=0):
    r = g.dot_r
    return [dot(cx, y + r, r)]


def comma_shape(g, cx=300, y=0):
    r = g.dot_r
    # gota: punto + cola inclinada hacia abajo-izquierda tangente al punto
    return [
        dot(cx, y + r, r),
        stroke(cx + r * 0.38, y + r * 0.9, cx - r * 0.55 - 30, y - 150, r * 1.05),
    ]


@glyph("period", ".")
def period(g):
    return period_shape(g)


@glyph("comma", ",")
def comma(g):
    return comma_shape(g)


@glyph("colon", ":")
def colon(g):
    r = g.dot_r
    return period_shape(g) + period_shape(g, y=g.X - 2 * r)


@glyph("semicolon", ";")
def semicolon(g):
    r = g.dot_r
    return comma_shape(g) + period_shape(g, y=g.X - 2 * r)


@glyph("exclam", "!")
def exclam(g):
    r = g.dot_r
    return [rect(300 - g.s * 0.55, 2 * r + 120, 300 + g.s * 0.55, g.C)] + period_shape(g)


@glyph("exclamdown", 0x00A1)
def exclamdown(g):
    return rotate180(exclam(g), 300, (g.X + g.D) / 2 + 85)


@glyph("question", "?")
def question(g):
    r = g.dot_r
    rx, ry = 200, 185 + 0.15 * (g.s - 80)
    cy = g.C + g.O - ry
    bottom = cy - ry  # borde exterior inferior de la panza
    return [
        arc(300, cy, rx, ry, g.s, g.h, -1, 2.08),
        rect(300 - g.s / 2, 2 * r + 120, 300 + g.s / 2, bottom + g.h),
    ] + period_shape(g)


@glyph("questiondown", 0x00BF)
def questiondown(g):
    return rotate180(question(g), 300, (g.X + g.D) / 2 + 85)


# --------------------------------------------------------------------------- comillas

def tick(g, cx, top, length=215, w=None):
    w = w or g.s * 1.05
    return rect(cx - w / 2, top - length, cx + w / 2, top)


@glyph("quotesingle", "'")
def quotesingle(g):
    return [tick(g, 300, g.C + 30)]


@glyph("quotedbl", '"')
def quotedbl(g):
    return [tick(g, 195, g.C + 30), tick(g, 405, g.C + 30)]


@glyph("grave", "`")
def grave(g):
    return translate(gravecomb_shape(g), 600, 0)


def gravecomb_shape(g):
    from .marks import grave_mark
    return grave_mark(g)


# --------------------------------------------------------------------------- matemáticas

@glyph("plus", "+")
def plus(g):
    t = g.s * 0.92
    a = 205
    return [rect(300 - a, MATH_Y - t / 2, 300 + a, MATH_Y + t / 2),
            rect(300 - t / 2, MATH_Y - a, 300 + t / 2, MATH_Y + a)]


@glyph("hyphen", "-")
def hyphen(g):
    t = g.h * 1.02
    return [rect(128, MATH_Y - t / 2, 472, MATH_Y + t / 2)]


def equal_bars(g, x0=95, x1=505, gap=None):
    t = g.h
    gap = gap or 92 + 0.35 * g.s
    return [rect(x0, MATH_Y + gap / 2, x1, MATH_Y + gap / 2 + t),
            rect(x0, MATH_Y - gap / 2 - t, x1, MATH_Y - gap / 2)]


@glyph("equal", "=")
def equal(g):
    return equal_bars(g)


@glyph("less", "<")
def less(g):
    return [chevron(108, MATH_Y, (490, MATH_Y + 225), (490, MATH_Y - 225), g.s * 0.95)]


@glyph("greater", ">")
def greater(g):
    return mirror_x(less(g))


@glyph("asciitilde", "~")
def asciitilde(g):
    return tilde_shape(g, 300, MATH_Y, half=218, amp=36 + 0.45 * g.s, w=g.s * 0.8 + 4)


def tilde_shape(g, cx, cy, half, amp, w, ty=0.85, a0=0.25, a1=1.78):
    """Tilde en onda: arco ∩ de a0 a a1 + su copia girada 180° alrededor de (cx, cy).
    El punto medio del corte en a0 se coloca en (cx, cy), así ambas mitades comparten
    corte y tangente en la inflexión. half = semiancho exterior, amp = radio vertical."""
    from ..pen import arc_end
    tx, tyy = w, w * ty
    ry = amp / 0.64 + tyy / 2      # cresta ≈ 0.64·ry_medio sobre la inflexión
    rx = (half - w / 2) / 1.88 + w / 2
    (ox, oy), (ix, iy) = arc_end(0, 0, rx, ry, tx, tyy, a0)
    ccx, ccy = cx - (ox + ix) / 2, cy - (oy + iy) / 2
    # cada mitad se prolonga un poco más allá de la inflexión para solaparse (sin costura)
    top = arc(ccx, ccy, rx, ry, tx, tyy, a0 - 0.035, a1)
    return [top] + rotate180([top], cx, cy)


@glyph("asciicircum", "^")
def asciicircum(g):
    return [chevron(300, g.C, (95, 370), (505, 370), g.s * 0.92)]


@glyph("underscore", "_")
def underscore(g):
    return [rect(50, -110 - g.h, 550, -110)]


@glyph("asterisk", "*")
def asterisk(g):
    import math
    cx, cy, r = 300, 470, 195
    w = g.s * 0.88
    out = []
    for ang in (90, 30, 150):
        dx, dy = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        out.append(stroke(cx - dx, cy - dy, cx + dx, cy + dy, w))
    return out


# --------------------------------------------------------------------------- barras y paréntesis

PAR_TOP, PAR_BOT = 835, -145


@glyph("slash", "/")
def slash(g):
    return [slant(95, PAR_BOT + 40, 505, PAR_TOP - 40, g.s * 0.95, "l", "r")]


@glyph("backslash", "\\")
def backslash(g):
    return mirror_x(slash(g))


@glyph("bar", "|")
def bar(g):
    return [rect(300 - g.s / 2, PAR_BOT - 30, 300 + g.s / 2, PAR_TOP + 30)]


@glyph("parenleft", "(")
def parenleft(g):
    cy = (PAR_TOP + PAR_BOT) / 2
    ry = (PAR_TOP - PAR_BOT) / 2 + 160
    rx = 330
    cx = 175 + rx
    import math
    from ..pen import param_at
    a0 = param_at(cx, cy, rx, ry, 1.0, 1.999, y=PAR_TOP)
    a1 = param_at(cx, cy, rx, ry, 2.001, 3.0, y=PAR_BOT)
    return [arc(cx, cy, rx, ry, g.s * 0.98, g.h, a0, a1)]


@glyph("parenright", ")")
def parenright(g):
    return mirror_x(parenleft(g))


@glyph("bracketleft", "[")
def bracketleft(g):
    x0 = 190
    return [rect(x0, PAR_BOT, x0 + g.s, PAR_TOP),
            rect(x0, PAR_TOP - g.h, 455, PAR_TOP),
            rect(x0, PAR_BOT, 455, PAR_BOT + g.h)]


@glyph("bracketright", "]")
def bracketright(g):
    return mirror_x(bracketleft(g))


@glyph("braceleft", "{")
def braceleft(g):
    mid = (PAR_TOP + PAR_BOT) / 2
    sx = 300 - g.s / 2           # borde izquierdo del asta
    r1 = 118 + 0.4 * g.s         # gancho superior
    r2 = 70 + 0.5 * g.s          # codo hacia la punta
    h = g.h
    upper = [
        arc(sx + r1, PAR_TOP - r1, r1, r1, g.s, h, 1, 2),
        rect(sx + r1, PAR_TOP - h, 462, PAR_TOP),
        rect(sx, mid + h / 2 + r2 - h, sx + g.s, PAR_TOP - r1),
        arc(sx + g.s - r2, mid + h / 2 + r2 - h, r2, r2, g.s, h, 3, 4),
    ]
    tip = rect(138, mid - h / 2, sx + g.s - r2, mid + h / 2)
    return upper + mirror_y(upper, mid) + [tip]


@glyph("braceright", "}")
def braceright(g):
    return mirror_x(braceleft(g))


# --------------------------------------------------------------------------- símbolos

@glyph("numbersign", "#")
def numbersign(g):
    w = g.s * 0.86
    t = g.h * 0.95
    y0, y1 = 20, 680
    return [
        slant(175, y0, 225, y1, w, "c", "c"),
        slant(375, y0, 425, y1, w, "c", "c"),
        rect(70, 225 - t / 2, 530, 225 + t / 2),
        rect(70, 475 - t / 2, 530, 475 + t / 2),
    ]


@glyph("dollar", "$")
def dollar(g):
    w = g.s * 0.86
    return s_shape(g, g.C, top_rx=200, bot_rx=220, sw=g.s, spine=0.535) + [
        rect(300 - w / 2, g.C - 20, 300 + w / 2, g.C + 105),
        rect(300 - w / 2, -105, 300 + w / 2, 20),
    ]


@glyph("percent", "%")
def percent(g):
    t = g.s * 0.82
    rx, ry = 98, 132
    return (
        ring(165, g.C - ry, rx, ry, t, t * 0.9)
        + ring(435, ry, rx, ry, t, t * 0.9)
        + [slant(60, 0, 540, g.C, t, "l", "r")]
    )


@glyph("ampersand", "&")
def ampersand(g):
    w = g.s * 0.9
    h = g.h * 0.92
    trx, try_ = 112 + 0.5 * g.s, 135 + 0.4 * g.s
    tcx, tcy = 250, g.C + g.O - try_
    brx, bry = 208, 228
    bcx, bcy = 262, bry - g.O
    return [
        arc(tcx, tcy, trx, try_, w, h, -0.6, 3.25),
        arc(bcx, bcy, brx, bry, w, h, 1.2, 4.2),
        slant(g.CR + 18, 0, tcx - 25, tcy - try_ + h * 0.5, w * 1.02, "r", "c"),
    ]


@glyph("at", "@")
def at(g):
    w = g.s * 0.64
    h = g.h * 0.72
    cy = 300
    orx, ory = 245, 350
    irx, iry = 108, 136
    icx = 285
    stem_r = icx + irx
    hook_cx = (stem_r - w + 300 + orx) / 2
    hook_rx = (300 + orx - (stem_r - w)) / 2
    return (
        ring(icx, cy, irx, iry, w, h)
        + [
            rect(stem_r - w, cy, stem_r, cy + iry - 4),
            arc(hook_cx, cy, hook_rx, 110, w, h, 2, 4),
            arc(300, cy, orx, ory, w, h, 0, 3.55),
        ]
    )
