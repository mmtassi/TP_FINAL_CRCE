from .enumeraciones import EstadoAviso, TipoSituacion, Gravedad
from .nota import Nota
from .descarte import Descarte
from .excepciones import OperacionAvisoInvalida


class Aviso:
    def __init__(self, ubicacion, tipo_situacion, gravedad_estimada, descripcion, reportante, fecha_registro):
        if tipo_situacion not in list(TipoSituacion):
            raise OperacionAvisoInvalida("Tipo de situación inválido")

        if gravedad_estimada not in list(Gravedad):
            raise OperacionAvisoInvalida("Gravedad estimada inválida")
        self._ubicacion = ubicacion
        self._tipo_situacion = tipo_situacion
        self._gravedad_estimada = gravedad_estimada
        self._descripcion = descripcion
        self._reportante = reportante
        self._fecha_registro = fecha_registro

        self._estado = EstadoAviso.PENDIENTE
        self._notas = []
        self._descarte = None

    @property
    def ubicacion(self):
        return self._ubicacion

    @property
    def tipo_situacion(self):
        return self._tipo_situacion

    @property
    def gravedad_estimada(self):
        return self._gravedad_estimada

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def reportante(self):
        return self._reportante

    @property
    def fecha_registro(self):
        return self._fecha_registro

    @property
    def notas(self):
        return tuple(self._notas)

    @property
    def descarte(self):
        return self._descarte

    @property
    def estado(self):
        return self._estado

    def _exigir_pendiente(self):
        if self._estado != EstadoAviso.PENDIENTE:
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
        self._estado = EstadoAviso.DESCARTADO
