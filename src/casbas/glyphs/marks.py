"""Acentos combinantes (avance 0, dibujados sobre la celda anterior) y compuestos."""
from ..pen import dot, mirror_x, stroke
from ..registry import composite, glyph
from .punctuation import tilde_shape

MC = -300  # eje de las marcas: centro de la celda anterior


def mark_anchor(g):
    return [("_top", MC, g.X)]


def acute_mark(g):
    w = g.s * 0.8
    return [stroke(MC - 62, g.X + 100, MC + 70, g.X + 252, w)]


def grave_mark(g):
    return mirror_x(acute_mark(g), about=MC)


@glyph("acutecomb", 0x0301, advance=0, anchors=mark_anchor)
def acutecomb(g):
    return acute_mark(g)


@glyph("gravecomb", 0x0300, advance=0, anchors=mark_anchor)
def gravecomb(g):
    return grave_mark(g)


@glyph("dieresiscomb", 0x0308, advance=0, anchors=mark_anchor)
def dieresiscomb(g):
    r = g.dot_r
    y = g.X + 80 + r
    return [dot(MC - 108, y, r), dot(MC + 108, y, r)]


@glyph("tildecomb", 0x0303, advance=0, anchors=mark_anchor)
def tildecomb(g):
    w = g.s * 0.5 + 8
    return tilde_shape(g, MC, g.X + 165, half=180, amp=22 + 0.26 * g.s, w=w, ty=0.8)


# --------------------------------------------------------------------------- compuestos

CAP_DY = 700 - 530 + 10  # de altura x a altura de mayúsculas (+ un poco de aire)

SPANISH = [
    ("aacute", 0xE1, "a", "acutecomb"), ("eacute", 0xE9, "e", "acutecomb"),
    ("iacute", 0xED, "dotlessi", "acutecomb"), ("oacute", 0xF3, "o", "acutecomb"),
    ("uacute", 0xFA, "u", "acutecomb"), ("udieresis", 0xFC, "u", "dieresiscomb"),
    ("ntilde", 0xF1, "n", "tildecomb"),
    ("Aacute", 0xC1, "A", "acutecomb"), ("Eacute", 0xC9, "E", "acutecomb"),
    ("Iacute", 0xCD, "I", "acutecomb"), ("Oacute", 0xD3, "O", "acutecomb"),
    ("Uacute", 0xDA, "U", "acutecomb"), ("Udieresis", 0xDC, "U", "dieresiscomb"),
    ("Ntilde", 0xD1, "N", "tildecomb"),
]

for name, code, base, mark in SPANISH:
    dy = CAP_DY if base[0].isupper() else 0
    composite(name, code, (base, 0, 0), (mark, 600, dy))
