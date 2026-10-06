#!/usr/bin/env python3
"""Construye Casbas Mono: params → UFOs → designspace → fontmake → woff2 → checks/pruebas.

Uso:  .venv/bin/python build.py [--no-proofs]
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import ufoLib2  # noqa: E402
from fontTools.designspaceLib import (AxisDescriptor, DesignSpaceDocument,  # noqa: E402
                                      InstanceDescriptor, SourceDescriptor)
from fontTools.ttLib import TTFont  # noqa: E402

from casbas import params  # noqa: E402
from casbas.glyphs.alternates import alternates_fea  # noqa: E402
from casbas.ligatures_fea import calt_feature  # noqa: E402
from casbas.registry import load_all  # noqa: E402

MASTER_DIR = ROOT / "master"
DIST = ROOT / "dist"
VF_NAME = f"{params.PS_FAMILY}[slnt,wght]"


# --------------------------------------------------------------------------- UFO

def draw_contours(glyph, contours, skew):
    pen = glyph.getPointPen()
    for contour in contours:
        pen.beginPath()
        n = len(contour)
        for i, (x, y, on) in enumerate(contour):
            x = x + skew * (y - params.SLANT_ORIGIN_Y)
            if on:
                prev_on = contour[(i - 1) % n][2]
                seg = "line" if prev_on else "curve"
                pen.addPoint((round(x), round(y)), segmentType=seg)
            else:
                pen.addPoint((round(x), round(y)))
        pen.endPath()


def build_ufo(m, glyphs):
    ufo = ufoLib2.Font()
    info = ufo.info
    info.familyName = params.FAMILY
    info.styleName = m.style
    info.versionMajor, info.versionMinor = params.VERSION
    info.unitsPerEm = params.UPM
    info.xHeight = m.X
    info.capHeight = m.C
    info.ascender = m.A
    info.descender = m.D
    info.italicAngle = m.italic_angle
    info.postscriptIsFixedPitch = True
    info.postscriptUnderlinePosition = -120
    info.postscriptUnderlineThickness = round(m.h)
    info.openTypeOS2WeightClass = m.wght
    info.openTypeOS2WidthClass = 5
    # Panose: latin text, sans normal, …, proportion 9 = monospaced
    info.openTypeOS2Panose = [2, 11, min(10, max(2, round(m.wght / 100) + 1)), 9, 2, 2, 3, 2, 2, 4]
    info.openTypeOS2Selection = [7]  # USE_TYPO_METRICS
    info.openTypeOS2TypoAscender = 800
    info.openTypeOS2TypoDescender = -200
    info.openTypeOS2TypoLineGap = 250
    info.openTypeHheaAscender = 1000
    info.openTypeHheaDescender = -250
    info.openTypeHheaLineGap = 0
    info.openTypeOS2WinAscent = 1000
    info.openTypeOS2WinDescent = 250
    info.openTypeNameDesigner = "Victor Casbas"
    info.copyright = "Copyright 2026 Victor Casbas"
    info.openTypeNameLicense = "This Font Software is licensed under the SIL Open Font License, Version 1.1."
    info.openTypeNameLicenseURL = "https://openfontlicense.org"

    order = [".notdef", "space"] + [n for n in glyphs if n not in (".notdef", "space")]
    ufo.lib["public.glyphOrder"] = order
    ufo.lib["public.postscriptNames"] = {}

    for name in order:
        gd = glyphs[name]
        glyph = ufo.newGlyph(name)
        glyph.width = gd.advance
        if gd.unicode is not None:
            glyph.unicodes = [gd.unicode]
        skew = 0 if gd.upright else m.skew
        if gd.draw:
            draw_contours(glyph, gd.draw(m), skew)
        for base, dx, dy in gd.components:
            glyph.components.append(
                ufoLib2.objects.Component(base, transformation=(1, 0, 0, 1, round(dx + m.skew * dy), dy)))
        if gd.anchors:
            for aname, x, y in gd.anchors(m):
                x = x + skew * (y - params.SLANT_ORIGIN_Y)
                glyph.appendAnchor({"name": aname, "x": round(x), "y": round(y)})

    ufo.features.text = calt_feature(glyphs) + "\n" + alternates_fea(glyphs)
    return ufo


# --------------------------------------------------------------------------- designspace

def build_designspace(paths):
    doc = DesignSpaceDocument()
    wght = AxisDescriptor()
    wght.tag, wght.name, wght.minimum, wght.default, wght.maximum = "wght", "Weight", 100, 400, 800
    slnt = AxisDescriptor()
    slnt.tag, slnt.name, slnt.minimum, slnt.default, slnt.maximum = "slnt", "Slant", -10, 0, 0
    doc.addAxis(wght)
    doc.addAxis(slnt)

    for m, path in paths:
        src = SourceDescriptor()
        src.path = str(path)
        src.familyName = params.FAMILY
        src.styleName = m.style
        src.location = {"Weight": m.wght, "Slant": m.slnt}
        doc.addSource(src)

    names = {100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium",
             600: "SemiBold", 700: "Bold", 800: "ExtraBold"}
    for slant in (0, -10):
        for w, n in names.items():
            inst = InstanceDescriptor()
            inst.familyName = params.FAMILY
            style = n if slant == 0 else ("Oblique" if n == "Regular" else f"{n} Oblique")
            inst.styleName = style
            inst.location = {"Weight": w, "Slant": slant}
            doc.addInstance(inst)
    return doc


# --------------------------------------------------------------------------- post-proceso

def set_overlap_flags(font):
    """Marca OVERLAP_SIMPLE/OVERLAP_COMPOUND para que los rasterizadores rellenen con nonzero."""
    from fontTools.ttLib.tables._g_l_y_f import OVERLAP_COMPOUND, flagOverlapSimple
    glyf = font["glyf"]
    for name in font.getGlyphOrder():
        g = glyf[name]
        if g.isComposite():
            g.components[0].flags |= OVERLAP_COMPOUND
        elif g.numberOfContours > 0:
            g.flags[0] |= flagOverlapSimple


def postprocess(path):
    font = TTFont(path)
    set_overlap_flags(font)
    font["post"].isFixedPitch = 1
    font["OS/2"].panose.bProportion = 9
    font.save(path)
    woff2 = path.with_suffix(".woff2")
    font.flavor = "woff2"
    font.save(woff2)
    return woff2


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-proofs", action="store_true")
    args = ap.parse_args()

    glyphs = load_all()
    print(f"{len(glyphs)} glifos registrados")

    if MASTER_DIR.exists():
        shutil.rmtree(MASTER_DIR)
    MASTER_DIR.mkdir()
    paths = []
    for m in params.masters():
        ufo = build_ufo(m, glyphs)
        p = MASTER_DIR / f"{params.PS_FAMILY}-{m.style.replace(' ', '')}.ufo"
        ufo.save(p, overwrite=True)
        paths.append((m, p))
    ds_path = MASTER_DIR / f"{params.PS_FAMILY}.designspace"
    build_designspace(paths).write(ds_path)

    DIST.mkdir(exist_ok=True)
    vf = DIST / f"{VF_NAME}.ttf"
    subprocess.run(
        [str(ROOT / ".venv/bin/fontmake"), "-m", str(ds_path), "-o", "variable",
         "--output-path", str(vf), "--no-production-names", "--verbose", "WARNING"],
        check=True,
    )
    woff2 = postprocess(vf)
    print(f"→ {vf.relative_to(ROOT)}\n→ {woff2.relative_to(ROOT)}")

    from checks import run_checks
    ok = run_checks(vf, glyphs)

    if not args.no_proofs:
        from proofs import render_proofs
        render_proofs(vf, ROOT / "proofs")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
