from dataclasses import dataclass
from datetime import datetime

from .excepciones import OperacionAvisoInvalida


@dataclass(frozen=True)
class Descarte:
    justificacion: str
    fecha_hora: datetime

    def __post_init__(self):
        if not self.justificacion or not self.justificacion.strip():
            raise OperacionAvisoInvalida("La justificación no puede estar vacía")