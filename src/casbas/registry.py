"""Registro de glifos: nombre → unicode, función de dibujo, anclas, componentes."""
from dataclasses import dataclass, field
from typing import Callable, Optional

from .params import ADV


@dataclass
class GlyphDef:
    name: str
    unicode: Optional[int]
    draw: Optional[Callable] = None              # draw(g) -> lista de contornos
    components: list = field(default_factory=list)  # [(base, dx, dy)]
    anchors: Optional[Callable] = None           # anchors(g) -> [(nombre, x, y)]
    advance: int = ADV


GLYPHS: dict[str, GlyphDef] = {}


def glyph(name, char=None, advance=ADV, anchors=None):
    """Decorador: registra una función de dibujo como glifo."""
    def deco(fn):
        code = ord(char) if isinstance(char, str) else char
        GLYPHS[name] = GlyphDef(name, code, draw=fn, anchors=anchors, advance=advance)
        return fn
    return deco


def composite(name, char, *components, anchors=None):
    code = ord(char) if isinstance(char, str) else char
    GLYPHS[name] = GlyphDef(name, code, components=list(components), anchors=anchors)


def load_all():
    # importar los módulos registra los glifos (el orden define el glyph order)
    from .glyphs import (lowercase, uppercase, digits, punctuation, marks,  # noqa: F401
                         typography, ligatures)
    return GLYPHS
