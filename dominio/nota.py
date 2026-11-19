from dataclasses import dataclass
from datetime import datetime

from .reportante import Reportante
from .excepciones import OperacionAvisoInvalida


@dataclass(frozen=True)
class Nota:
    texto: str
    autor: Reportante
    fecha_hora: datetime

    def __post_init__(self):
        if type(self.autor) is not Reportante:
            raise OperacionAvisoInvalida("El autor tiene que ser un Reportante")

        if not self.texto or not self.texto.strip():
            raise OperacionAvisoInvalida("La nota tiene que tener texto")
