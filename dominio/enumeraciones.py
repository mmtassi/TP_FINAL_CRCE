from enum import Enum


class EstadoAviso(Enum):
    PENDIENTE = "Pendiente"
    ACEPTADO = "Aceptado"
    DESCARTADO = "Descartado"


class TipoSituacion(Enum):
    INUNDACION = "Inundación"
    INCENDIO = "Incendio"
    ACCIDENTE_VIAL = "Accidente vial"


class Gravedad(Enum):
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
