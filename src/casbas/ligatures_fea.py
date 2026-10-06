"""Genera la feature `calt` de ligaduras al estilo Fira Code.

Cada secuencia g1…gn se convierte en LIG…LIG + liga: todos los glifos menos el último
pasan a ser un espaciador vacío (LIG) y el último un glifo `.liga` de avance 600 cuyo
dibujo se extiende hacia la izquierda. Así se conserva la rejilla monospace y el cursor.
"""

LANGSYS = "languagesystem DFLT dflt;\nlanguagesystem latn dflt;\n"


def ligature_specs():
    from .glyphs.ligatures import LIGATURES
    return LIGATURES


def _lookup(seq, liga):
    name = liga.replace(".liga", "").replace(".", "_")
    n = len(seq)
    rules = [
        f"    ignore sub {seq[0]} {seq[0]}' {' '.join(seq[1:])};",
        f"    ignore sub {seq[0]}' {' '.join(seq[1:])} {seq[-1]};",
        f"    sub {'LIG ' * (n - 1)}{seq[-1]}' by {liga};",
    ]
    for i in range(n - 2, 0, -1):
        rest = " ".join(seq[i + 1:])
        rules.append(f"    sub {'LIG ' * i}{seq[i]}' {rest} by LIG;")
    rules.append(f"    sub {seq[0]}' {' '.join(seq[1:])} by LIG;")
    return f"  lookup {name} {{\n" + "\n".join(rules) + f"\n  }} {name};\n"


def calt_feature(glyphs):
    if "LIG" not in glyphs:
        return LANGSYS
    specs = [(seq, liga) for seq, liga in ligature_specs() if liga in glyphs]
    specs.sort(key=lambda s: -len(s[0]))  # las más largas primero (=== antes que ==)
    body = "".join(_lookup(seq, liga) for seq, liga in specs)
    return LANGSYS + "\nfeature calt {\n" + body + "} calt;\n"
