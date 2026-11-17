from dataclasses import dataclass
from datetime import datetime

from .reportante import Reportante

@dataclass(frozen=True)

class Nota:
    texto: str
    autor: Reportante
    fecha_hora: datetime

