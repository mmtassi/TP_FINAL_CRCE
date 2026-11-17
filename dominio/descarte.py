from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Descarte:
    justificacion: str
    fecha_hora: datetime
