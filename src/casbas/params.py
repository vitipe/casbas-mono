"""Métricas globales y parámetros por máster de Casbas Mono."""
from dataclasses import dataclass
import math

FAMILY = "Casbas Mono"
PS_FAMILY = "CasbasMono"
VERSION = (1, 1)

UPM = 1000
ADV = 600          # avance fijo (monospace)
MID = ADV / 2      # eje central del glifo

SLANT_ORIGIN_Y = 270  # altura sobre la que pivota la oblicua


@dataclass(frozen=True)
class Master:
    style: str
    wght: int
    slnt: float      # grados; negativo = inclinada a la derecha (convención OpenType)
    s: float         # grosor de asta vertical
    contrast: float  # grosor horizontal / vertical

    # --- métricas verticales ---
    X = 530    # altura x
    C = 700    # altura de mayúsculas
    A = 750    # ascendentes (b d h k l)
    D = -200   # descendentes
    O = 12     # overshoot de curvas

    # --- límites horizontales ---
    LL, LR = 88, 512     # astas de minúsculas (n, h, u…)
    OL, OR = 80, 520     # curvas de minúsculas (o, c, e…)
    CL, CR = 78, 522     # astas de mayúsculas
    COL, COR = 70, 530   # curvas de mayúsculas

    @property
    def h(self) -> float:
        """Grosor de trazos horizontales y de la parte alta/baja de las curvas."""
        return self.s * self.contrast

    @property
    def trap(self) -> float:
        """Adelgazamiento de las uniones curva–asta (fracción del asta que se recorta).
        Crece con el peso: en Thin no hace falta, en ExtraBold evita manchas."""
        return 0.12 + 0.43 * (self.s - 22) / 118

    @property
    def dot_r(self) -> float:
        return 0.58 * self.s + 6

    @property
    def italic_angle(self) -> float:
        return self.slnt

    @property
    def skew(self) -> float:
        return math.tan(math.radians(-self.slnt))


WEIGHTS = {
    # wght: (nombre, grosor de asta, contraste)
    100: ("Thin", 22, 0.96),
    400: ("Regular", 80, 0.88),
    800: ("ExtraBold", 140, 0.82),
}
SLANTS = (0, -10)


def masters():
    out = []
    for slnt in SLANTS:
        for wght, (name, s, contrast) in WEIGHTS.items():
            style = name if slnt == 0 else f"{name} Oblique"
            out.append(Master(style=style, wght=wght, slnt=slnt, s=s, contrast=contrast))
    return out
