"""Primitivas geométricas compatibles entre másteres.

Un contorno es una lista cíclica de nodos ``(x, y, on)``; los nodos ``on=False`` van
de dos en dos (manejadores cúbicos). Una forma es una lista de contornos.

Regla de oro: la *estructura* (número y tipo de nodos) de cada primitiva depende solo
de sus argumentos discretos (p. ej. los ángulos ``a0``/``a1`` de un arco), nunca del
grosor. Así cualquier glifo genera los mismos puntos en todos los másteres y la fuente
variable interpola sin booleanas: las piezas se solapan y se rellenan con nonzero.
Contornos exteriores en sentido antihorario (convención PostScript/UFO).
"""
import math

K = 0.58  # tensión de las curvas: 0.552 = círculo perfecto, algo más = ligeramente llena


# --------------------------------------------------------------------------- utilidades

def _area(contour):
    a = 0.0
    n = len(contour)
    for i in range(n):
        x0, y0, _ = contour[i]
        x1, y1, _ = contour[(i + 1) % n]
        a += x0 * y1 - x1 * y0
    return a / 2


def reverse(contour):
    rev = contour[::-1]
    # rotar para empezar en un nodo on-curve
    i = next(i for i, n in enumerate(rev) if n[2])
    return rev[i:] + rev[:i]


def ccw(contour):
    return contour if _area(contour) > 0 else reverse(contour)


def cw(contour):
    return contour if _area(contour) < 0 else reverse(contour)


def transform(shape, a, b, c, d, e=0.0, f=0.0):
    """Aplica x' = a·x + c·y + e, y' = b·x + d·y + f a todos los contornos."""
    out = []
    for contour in shape:
        t = [(a * x + c * y + e, b * x + d * y + f, on) for x, y, on in contour]
        if a * d - b * c < 0:
            t = reverse(t)
        out.append(t)
    return out


def translate(shape, dx, dy=0.0):
    return transform(shape, 1, 0, 0, 1, dx, dy)


def mirror_x(shape, about=300.0):
    return transform(shape, -1, 0, 0, 1, 2 * about, 0)


def mirror_y(shape, about):
    return transform(shape, 1, 0, 0, -1, 0, 2 * about)


def rotate180(shape, cx, cy):
    return transform(shape, -1, 0, 0, -1, 2 * cx, 2 * cy)


def scale(shape, sx, sy, ox=300.0, oy=0.0):
    return transform(shape, sx, 0, 0, sy, ox - sx * ox, oy - sy * oy)


# --------------------------------------------------------------------------- cúbicas

def _lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _split(c, t):
    p0, p1, p2, p3 = c
    a, b, cc = _lerp(p0, p1, t), _lerp(p1, p2, t), _lerp(p2, p3, t)
    d, e = _lerp(a, b, t), _lerp(b, cc, t)
    f = _lerp(d, e, t)
    return (p0, a, d, f), (f, e, cc, p3)


def _sub(c, u0, u1):
    if u1 < 1:
        c = _split(c, u1)[0]
    if u0 > 0:
        c = _split(c, u0 / u1)[1]
    return c


def _quarter(cx, cy, rx, ry, q, k):
    """Cuarto de elipse q (0: der→arriba, 1: arriba→izq, 2: izq→abajo, 3: abajo→der)."""
    base = [(1, 0), (1, k), (k, 1), (0, 1)]
    q %= 4
    pts = []
    for x, y in base:
        for _ in range(q):
            x, y = -y, x
        pts.append((cx + rx * x, cy + ry * y))
    return tuple(pts)


def arc_segments(cx, cy, rx, ry, a0, a1, k=K):
    """Cúbicas desde a0 hasta a1 (a1 > a0), en unidades de cuarto de vuelta, antihorario.
    0 = derecha, 1 = arriba, 2 = izquierda, 3 = abajo."""
    assert a1 > a0
    segs = []
    q = math.floor(a0)
    while q < a1:
        u0 = max(a0 - q, 0.0)
        u1 = min(a1 - q, 1.0)
        if u1 - u0 > 1e-9:
            segs.append(_sub(_quarter(cx, cy, rx, ry, q, k), u0, u1))
        q += 1
    return segs


def ellipse_point(cx, cy, rx, ry, a, k=K):
    q = math.floor(a)
    u = a - q
    c = _quarter(cx, cy, rx, ry, q, k)
    if u == 0:
        return c[0]
    return _split(c, u)[0][3]


def _segs_to_nodes(segs):
    nodes = [(*segs[0][0], True)]
    for _, p1, p2, p3 in segs:
        nodes += [(*p1, False), (*p2, False), (*p3, True)]
    return nodes


# --------------------------------------------------------------------------- primitivas

def rect(x0, y0, x1, y1):
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    return [(x0, y0, True), (x1, y0, True), (x1, y1, True), (x0, y1, True)]


def poly(*pts):
    return ccw([(x, y, True) for x, y in pts])


def ellipse(cx, cy, rx, ry, k=K):
    nodes = _segs_to_nodes(arc_segments(cx, cy, rx, ry, 0, 4, k))
    return nodes[:-1]  # el último on-curve coincide con el primero


def dot(cx, cy, r):
    return ellipse(cx, cy, r, r, k=0.5523)


def ring(cx, cy, rx, ry, tx, ty, k=K):
    """Anillo: elipse exterior + contraforma invertida. tx/ty = grosor horizontal/vertical."""
    return [ellipse(cx, cy, rx, ry, k), reverse(ellipse(cx, cy, rx - tx, ry - ty, k))]


def ring_oi(o, i, k=K):
    """Anillo con elipses exterior/interior independientes: o, i = (cx, cy, rx, ry)."""
    return [ellipse(*o, k), reverse(ellipse(*i, k))]


def box(left, right, bottom, top):
    """Elipse (cx, cy, rx, ry) inscrita en una caja."""
    return ((left + right) / 2, (bottom + top) / 2, (right - left) / 2, (top - bottom) / 2)


def _cut_param(cx, cy, rx, ry, icx, icy, irx, iry, a, cut, k, start):
    """Parámetro del punto interior para un remate en a.

    cut: None = perpendicular al trazo, 'h' = horizontal, 'v' = vertical, o un ángulo
    en grados. La búsqueda se limita al cuarto de a, así la estructura de nodos no
    cambia entre másteres."""
    if a == math.floor(a) and cut is None:
        # en un cuarto exacto la normal es horizontal (a par) o vertical (a impar):
        # si las elipses comparten ese eje, el remate recto cae en el mismo parámetro
        if (int(a) % 2 == 0 and icy == cy) or (int(a) % 2 == 1 and icx == cx):
            return a
    px, py = ellipse_point(cx, cy, rx, ry, a, k)
    if cut is None:
        e = 1e-4
        x0, y0 = ellipse_point(cx, cy, rx, ry, a - e, k)
        x1, y1 = ellipse_point(cx, cy, rx, ry, a + e, k)
        dx, dy = -(y1 - y0), x1 - x0
    elif cut == "h":
        dx, dy = 1.0, 0.0
    elif cut == "v":
        dx, dy = 0.0, 1.0
    else:
        dx, dy = math.cos(math.radians(cut)), math.sin(math.radians(cut))

    def f(b):
        ix, iy = ellipse_point(icx, icy, irx, iry, b, k)
        return dx * (iy - py) - dy * (ix - px)

    q = math.floor(a) if (start or a != math.floor(a)) else a - 1
    lo, hi = q + 1e-6, q + 1 - 1e-6
    # el corte suele estar cerca de a: buscar el cambio de signo más próximo
    n = 64
    xs = [lo + (hi - lo) * i / n for i in range(n + 1)]
    best = None
    for u, v in zip(xs, xs[1:]):
        if f(u) * f(v) <= 0:
            mid = (u + v) / 2
            if best is None or abs(mid - a) < abs(best[0] - a):
                best = (mid, u, v)
    if best is None:
        return min(max(a, lo), hi)
    _, u, v = best
    for _ in range(50):
        m = (u + v) / 2
        if f(u) * f(m) <= 0:
            v = m
        else:
            u = m
    return (u + v) / 2


def arc_oi(o, i, a0, a1, k=K, cut0=None, cut1=None):
    """Banda de arco entre la elipse exterior o y la interior i, ambas (cx, cy, rx, ry).
    Con centros distintos el grosor varía a lo largo del arco (p. ej. más fino donde el
    hombro de la n se une al asta). Si un extremo es un cuarto exacto y las elipses
    comparten esa coordenada, el remate es recto (horizontal o vertical)."""
    b0 = _cut_param(*o, *i, a0, cut0, k, start=True)
    b1 = _cut_param(*o, *i, a1, cut1, k, start=False)
    outer = _segs_to_nodes(arc_segments(*o, a0, a1, k))
    inner = _segs_to_nodes(arc_segments(*i, b0, b1, k))
    assert len(outer) == len(inner), "arco incompatible: el corte cruzó un cuarto"
    return ccw(outer + inner[::-1])


def arc(cx, cy, rx, ry, tx, ty, a0, a1, k=K, cut0=None, cut1=None):
    """Banda de arco de a0 a a1 con grosor tx (horizontal) / ty (vertical).
    cut0/cut1: dirección del remate en cada extremo (ver _cut_param)."""
    return arc_oi((cx, cy, rx, ry), (cx, cy, rx - tx, ry - ty), a0, a1, k, cut0, cut1)


def arc_end(cx, cy, rx, ry, tx, ty, a, k=K, cut=None, start=True):
    """Puntos (exterior, interior) del remate de un arco en a."""
    b = _cut_param(cx, cy, rx, ry, cx, cy, rx - tx, ry - ty, a, cut, k, start)
    return ellipse_point(cx, cy, rx, ry, a, k), ellipse_point(cx, cy, rx - tx, ry - ty, b, k)


def param_at(cx, cy, rx, ry, a_lo, a_hi, y=None, x=None, k=K):
    """Parámetro en [a_lo, a_hi] donde la elipse pasa por la altura y (o la x dada)."""
    def f(a):
        px, py = ellipse_point(cx, cy, rx, ry, a, k)
        return (py - y) if y is not None else (px - x)
    u, v = a_lo, a_hi
    for _ in range(60):
        m = (u + v) / 2
        if f(u) * f(m) <= 0:
            v = m
        else:
            u = m
    return (u + v) / 2


def stroke(x0, y0, x1, y1, w):
    """Trazo recto con remates perpendiculares."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    return poly((x0 + nx, y0 + ny), (x0 - nx, y0 - ny), (x1 - nx, y1 - ny), (x1 + nx, y1 + ny))


def slant_centers(x0, y0, x1, y1, w, a0="c", a1="c"):
    """Centros (c0, c1) y semiancho horizontal de un trazo diagonal con remates horizontales.
    a0/a1: 'l' = x es el borde izquierdo, 'r' = el derecho, 'c' = el centro."""
    hw = w / 2
    off = {"l": 1, "r": -1, "c": 0}
    for _ in range(6):
        c0 = x0 + off[a0] * hw
        c1 = x1 + off[a1] * hw
        L = math.hypot(c1 - c0, y1 - y0)
        hw = (w / 2) * L / abs(y1 - y0)
    return c0, c1, hw


def slant(x0, y0, x1, y1, w, a0="c", a1="c"):
    c0, c1, hw = slant_centers(x0, y0, x1, y1, w, a0, a1)
    return poly((c0 - hw, y0), (c0 + hw, y0), (c1 + hw, y1), (c1 - hw, y1))


def x_at(c0, y0, c1, y1, y):
    """x del eje de un trazo (c0,y0)-(c1,y1) a la altura y."""
    return c0 + (c1 - c0) * (y - y0) / (y1 - y0)


def chevron(vx, vy, e1, e2, w):
    """Ángulo con vértice en inglete (para < > ^ y flechas). e1/e2 = extremos del eje."""
    def unit(x, y):
        L = math.hypot(x, y)
        return x / L, y / L

    u1 = unit(e1[0] - vx, e1[1] - vy)
    u2 = unit(e2[0] - vx, e2[1] - vy)
    b = unit(u1[0] + u2[0], u1[1] + u2[1])
    sin_half = abs(u1[0] * b[1] - u1[1] * b[0])
    m = (w / 2) / sin_half
    tip = (vx - b[0] * m, vy - b[1] * m)
    inner = (vx + b[0] * m, vy + b[1] * m)

    def normal_away(u, other):
        n = (-u[1], u[0])
        if n[0] * other[0] + n[1] * other[1] > 0:
            n = (-n[0], -n[1])
        return n

    n1 = normal_away(u1, u2)
    n2 = normal_away(u2, u1)
    hw = w / 2
    return poly(
        tip,
        (e1[0] + n1[0] * hw, e1[1] + n1[1] * hw),
        (e1[0] - n1[0] * hw, e1[1] - n1[1] * hw),
        inner,
        (e2[0] - n2[0] * hw, e2[1] - n2[1] * hw),
        (e2[0] + n2[0] * hw, e2[1] + n2[1] * hw),
    )
