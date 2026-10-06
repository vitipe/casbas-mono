# Casbas Mono

Monoespaciada geométrica de curvas circulares, para código y titulares. Está generada
por código: cada glifo es una función de Python que recibe el grosor del máster y
devuelve contornos.

- **Ejes:** `wght` 100–800 y `slnt` 0 a −10° (oblicua). 16 instancias con nombre.
- **Cobertura (212 glifos):** ASCII, español (á é í ó ú ü ñ ¿ ¡ « » — … “ ” ª º €…),
  cajas, bloques y separadores Powerline.
- **Ligaduras (`calt`):** `-> <- => == === != !== >= <= |> :: // ||`
- **Alternativas:** `ss01` a y g de dos pisos · `ss02` `<=` como flecha · `zero` cero con barra

## Archivos

| | |
|---|---|
| `dist/CasbasMono[slnt,wght].ttf` / `.woff2` | Fuente variable (macOS, Windows, web) |
| `dist/static/*.ttf` | 16 estáticas **sin solapes**: para Linux y terminales con FreeType |
| `specimen/index.html` | Muestrario: `python3 -m http.server` y abrir `/specimen/` |

En VS Code:

```jsonc
"editor.fontFamily": "Casbas Mono",
"editor.fontLigatures": "'calt', 'ss01', 'zero'",
"editor.fontVariations": "'wght' 420"
```

## Compilar

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python build.py            # UFOs → variable + estáticas → checks → pruebas PNG
.venv/bin/python regress.py          # qué glifos cambiaron respecto a snapshots/
.venv/bin/python regress.py --update # aceptar los cambios
```

`build.py` falla si los checks no pasan: cobertura, avance fijo de 600, ligaduras y
features (con HarfBuzz) y ausencia de solapes en las estáticas.

## Cómo está hecha

- `src/casbas/params.py`: métricas y los 6 másteres (Thin/Regular/ExtraBold × recta/oblicua).
- `src/casbas/pen.py`: primitivas (rectángulos, anillos, arcos, trazos). Generan los mismos
  puntos a cualquier grosor, así que los másteres son compatibles sin booleanas: las piezas
  se superponen y se rellenan con nonzero (flag `OVERLAP_SIMPLE`).
- `src/casbas/glyphs/`: un módulo por grupo de glifos. `ligatures_fea.py` genera la `calt`.

Licencia: SIL Open Font License 1.1.
