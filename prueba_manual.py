
from datetime import datetime

from dominio.enumeraciones import TipoSituacion, Gravedad
from dominio.reportante import Reportante
from dominio.nota import Nota
from dominio.descarte import Descarte


reportante = Reportante("R001")
fecha = datetime(2026, 6, 4, 10, 30)

nota = Nota("Hay personas atrapadas", reportante, fecha)
descarte = Descarte("Aviso duplicado", fecha)

print("Reportante:", reportante.identificador)
print("Nota:", nota.texto)
print("Autor:", nota.autor.identificador)
print("Descarte:", descarte.justificacion)
print("Tipo:", TipoSituacion.INCENDIO.value)
print("Gravedad:", Gravedad.ALTA.value)
print("Fecha: ", descarte.fecha_hora)