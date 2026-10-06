"""Comprobaciones automáticas sobre la fuente compilada."""
from fontTools.ttLib import TTFont

SPANISH = "áéíóúüñÁÉÍÓÚÜÑ¿¡"
TYPOGRAPHY = "«»‹›–—…‘’“”‚„€°·•±×÷ªº\u00a0"
BOXES = "─│┌┐└┘├┤┬┴┼╴╵╶╷━┃┏┓┗┛┣┫┳┻╋═║╔╗╚╝╠╣╦╩╬╭╮╯╰█▀▄▌▐░▒▓\ue0b0\ue0b1\ue0b2\ue0b3"
REQUIRED = [chr(c) for c in range(0x20, 0x7F)] + list(SPANISH) + list(TYPOGRAPHY) + list(BOXES)

LIGA_TESTS = {
    "->": ["LIG", "hyphen_greater.liga"],
    "=>": ["LIG", "equal_greater.liga"],
    "===": ["LIG", "LIG", "equal_equal_equal.liga"],
    "!=": ["LIG", "exclam_equal.liga"],
    "====": ["equal", "equal", "equal", "equal"],  # no debe ligar
}


def shape(path, text, features=None):
    import uharfbuzz as hb
    blob = hb.Blob.from_file_path(str(path))
    font = hb.Font(hb.Face(blob))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {})
    names = [font.glyph_to_string(i.codepoint) for i in buf.glyph_infos]
    advances = [p.x_advance for p in buf.glyph_positions]
    return names, advances


def run_checks(path, glyphs):
    font = TTFont(path)
    problems = []

    cmap = font.getBestCmap()
    missing = [c for c in REQUIRED if ord(c) not in cmap]
    if missing:
        problems.append(f"faltan {len(missing)} caracteres: {''.join(missing)!r}")

    hmtx = font["hmtx"]
    for name, gd in glyphs.items():
        adv = hmtx[name][0]
        if adv != gd.advance:
            problems.append(f"{name}: avance {adv} ≠ {gd.advance}")
    spacing = {hmtx[n][0] for n, gd in glyphs.items() if gd.advance}
    if spacing != {600}:
        problems.append(f"avances no cero distintos de 600: {spacing}")

    if font["post"].isFixedPitch != 1:
        problems.append("post.isFixedPitch != 1")
    if font["OS/2"].panose.bProportion != 9:
        problems.append("panose proportion != 9")

    if "LIG" in glyphs:
        for text, expected in LIGA_TESTS.items():
            if expected[-1].endswith(".liga") and expected[-1] not in glyphs:
                continue
            names, advances = shape(path, text)
            if names != expected:
                problems.append(f"ligadura {text!r}: {names} (esperado {expected})")
            if set(advances) != {600}:
                problems.append(f"ligadura {text!r}: avances {advances}")
        names, _ = shape(path, "->", {"calt": False})
        if names != ["hyphen", "greater"]:
            problems.append(f"calt desactivado sigue ligando: {names}")

    feature_tests = [
        ("aá g", {"ss01": True}, ["a.ss01", "aacute.ss01", "space", "g.ss01"]),
        ("0", {"zero": True}, ["zero.zero"]),
        ("<=", {"ss02": True}, ["LIG", "less_equal.arrow"]),
        ("<=", {}, ["LIG", "less_equal.liga"]),
    ]
    for text, feats, expected in feature_tests:
        if not all(n in glyphs for n in expected):
            continue
        names, _ = shape(path, text, feats)
        if names != expected:
            problems.append(f"feature {feats} en {text!r}: {names} (esperado {expected})")

    found = len([c for c in REQUIRED if ord(c) in cmap])
    print(f"checks: {len(font.getGlyphOrder())} glifos, {found}/{len(REQUIRED)} caracteres requeridos")
    for p in problems:
        print("  ✗", p)
    if not problems:
        print("  ✓ todo correcto")
    return not problems
