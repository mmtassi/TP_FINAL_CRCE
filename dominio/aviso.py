
from .enumeraciones import EstadoAviso
from .nota import Nota
from .descarte import Descarte
from .excepciones import OperacionAvisoInvalida


class Aviso:
    def __init__(
        self,
        ubicacion,
        tipo_situacion,
        gravedad_estimada,
        descripcion,
        reportante,
        fecha_registro
    ):
        self.ubicacion = ubicacion
        self.tipo_situacion = tipo_situacion
        self.gravedad_estimada = gravedad_estimada
        self.descripcion = descripcion
        self.reportante = reportante
        self.fecha_registro = fecha_registro

        self.estado = EstadoAviso.PENDIENTE
        self._notas = []
        self._descarte = None

    @property
    def notas(self):
        return tuple(self._notas)

    @property
    def descarte(self):
        return self._descarte

    def _exigir_pendiente(self):
        if self.estado != EstadoAviso.PENDIENTE:
            raise OperacionAvisoInvalida(
                "El aviso no está pendiente"
            )

    def agregar_nota(self, texto, autor, fecha_hora):
        self._exigir_pendiente()

        nota = Nota(texto, autor, fecha_hora)
        self._notas.append(nota)

    def descartar(self, justificacion, fecha_hora):
        self._exigir_pendiente()

        if not justificacion or not justificacion.strip():
            raise OperacionAvisoInvalida(
                "La justificación no puede estar vacía"
            )

        self._descarte = Descarte(justificacion, fecha_hora)
        self.estado = EstadoAviso.DESCARTADO
