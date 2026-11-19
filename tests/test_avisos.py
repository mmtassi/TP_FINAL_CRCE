from datetime import datetime
import pytest

from dominio.aviso import Aviso
from dominio.reportante import Reportante
from dominio.enumeraciones import EstadoAviso, TipoSituacion, Gravedad
from dominio.excepciones import OperacionAvisoInvalida
from dominio.nota import Nota
from dominio.descarte import Descarte


@pytest.fixture
def aviso():
    reportante = Reportante("R001")
    return Aviso(
        "Av. San Martín 150",
        TipoSituacion.INCENDIO,
        Gravedad.ALTA,
        "Incendio en una vivienda",
        reportante,
        datetime(2026, 11, 17, 10, 0))


# 1. Un aviso recién registrado está pendiente, no tiene notas y no tiene descarte.
def test_aviso_nuevo_comienza_pendiente_sin_notas_ni_descarte(aviso):
    assert aviso.estado == EstadoAviso.PENDIENTE
    assert aviso.ubicacion == "Av. San Martín 150"
    assert aviso.tipo_situacion == TipoSituacion.INCENDIO
    assert aviso.gravedad_estimada == Gravedad.ALTA
    assert aviso.descripcion == "Incendio en una vivienda"
    assert aviso.reportante.identificador == "R001"
    assert aviso.fecha_registro == datetime(2026, 11, 17, 10, 0)
    assert aviso.notas == ()
    assert aviso.descarte is None


def test_aviso_rechaza_tipo_situacion_fuera_del_catalogo():
    with pytest.raises(OperacionAvisoInvalida):
        Aviso("Av. San Martín 150", "Tormenta", Gravedad.ALTA,
            "Incidente", Reportante("R001"), datetime(2026, 11, 17, 10, 0))


def test_aviso_rechaza_gravedad_fuera_del_catalogo():
    with pytest.raises(OperacionAvisoInvalida):
        Aviso("Av. San Martín 150", TipoSituacion.INCENDIO, "Urgente",
            "Incidente", Reportante("R001"), datetime(2026, 11, 17, 10, 0))


# 2. Se agrega una nota a un aviso pendiente y la nota conserva autor, fecha y hora.
def test_nota_agregada_conserva_texto_autor_y_fecha(aviso):
    fecha = datetime(2026, 11, 17, 10, 30)
    aviso.agregar_nota("Hay personas atrapadas", aviso.reportante, fecha)

    assert len(aviso.notas) == 1
    nota = aviso.notas[0]
    assert nota.texto == "Hay personas atrapadas"
    assert nota.autor is aviso.reportante
    assert nota.fecha_hora == fecha
    assert aviso.estado == EstadoAviso.PENDIENTE


# 3. Se agregan dos notas y se conservan las dos, en el orden en que llegaron.
def test_dos_notas_conservan_el_orden_de_llegada(aviso):
    aviso.agregar_nota("Primera nota", aviso.reportante, datetime(2026, 11, 17, 10, 30))
    aviso.agregar_nota("Segunda nota", aviso.reportante, datetime(2026, 11, 17, 10, 45))

    assert len(aviso.notas) == 2
    assert aviso.notas[0].texto == "Primera nota"
    assert aviso.notas[1].texto == "Segunda nota"


# 4. Después de agregar una nota, la ubicación, el tipo, la gravedad estimada y la descripción siguen iguales.
def test_agregar_nota_no_modifica_datos_originales(aviso):
    reportante_original = aviso.reportante
    fecha_original = aviso.fecha_registro

    aviso.agregar_nota("Información adicional", aviso.reportante, datetime(2026, 11, 17, 11, 0))

    assert aviso.ubicacion == "Av. San Martín 150"
    assert aviso.tipo_situacion == TipoSituacion.INCENDIO
    assert aviso.gravedad_estimada == Gravedad.ALTA
    assert aviso.descripcion == "Incendio en una vivienda"
    assert aviso.reportante is reportante_original
    assert aviso.fecha_registro == fecha_original



def test_aviso_rechaza_modificacion_directa_de_datos_originales(aviso):
    with pytest.raises(AttributeError):
        aviso.ubicacion = "Otra dirección"

    with pytest.raises(AttributeError):
        aviso.tipo_situacion = TipoSituacion.INUNDACION

    with pytest.raises(AttributeError):
        aviso.gravedad_estimada = Gravedad.BAJA

    with pytest.raises(AttributeError):
        aviso.descripcion = "Otra descripción"

    with pytest.raises(AttributeError):
        aviso.reportante = Reportante("R002")

    with pytest.raises(AttributeError):
        aviso.fecha_registro = datetime(2026, 11, 18, 10, 0)

    assert aviso.ubicacion == "Av. San Martín 150"
    assert aviso.tipo_situacion == TipoSituacion.INCENDIO
    assert aviso.gravedad_estimada == Gravedad.ALTA
    assert aviso.descripcion == "Incendio en una vivienda"
    assert aviso.reportante.identificador == "R001"
    assert aviso.fecha_registro == datetime(2026, 11, 17, 10, 0)



# 5. Se descarta un aviso pendiente con justificación: queda descartado y conserva la justificación y la fecha.
def test_descartar_aviso_conserva_justificacion_y_fecha(aviso):
    fecha = datetime(2026, 11, 17, 12, 0)
    aviso.descartar("El incidente ya fue resuelto", fecha)

    assert aviso.estado == EstadoAviso.DESCARTADO
    assert aviso.descarte is not None
    assert aviso.descarte.justificacion == "El incidente ya fue resuelto"
    assert aviso.descarte.fecha_hora == fecha


# 6. Se intenta descartar con una justificación vacía o con solo espacios. La operación se rechaza y el aviso sigue pendiente.
def test_descarte_sin_justificacion_se_rechaza_sin_modificar_aviso(aviso):
    fecha = datetime(2026, 11, 17, 12, 0)

    for justificacion in ("", "   "):
        with pytest.raises(OperacionAvisoInvalida):
            aviso.descartar(justificacion, fecha)

        assert aviso.estado == EstadoAviso.PENDIENTE
        assert aviso.descarte is None
        assert aviso.notas == ()


# 7. Se intenta agregar una nota a un aviso descartado. La operación se rechaza y las notas no cambian.
def test_aviso_descartado_rechaza_nuevas_notas_sin_modificar_datos(aviso):
    aviso.agregar_nota("Nota anterior", aviso.reportante, datetime(2026, 11, 17, 10, 30))
    aviso.descartar("Aviso duplicado", datetime(2026, 11, 17, 11, 0))
    notas_anteriores = aviso.notas
    descarte_original = aviso.descarte

    with pytest.raises(OperacionAvisoInvalida):
        aviso.agregar_nota("Nueva nota", aviso.reportante, datetime(2026, 11, 17, 12, 0))

    assert aviso.estado == EstadoAviso.DESCARTADO
    assert aviso.notas == notas_anteriores
    assert aviso.descarte is descarte_original


# 8. Se intenta descartar por segunda vez. La operación se rechaza y se conserva la justificación original.
def test_segundo_descarte_se_rechaza_y_conserva_el_original(aviso):
    fecha_original = datetime(2026, 11, 17, 11, 0)
    aviso.descartar("Aviso duplicado", fecha_original)
    descarte_original = aviso.descarte

    with pytest.raises(OperacionAvisoInvalida):
        aviso.descartar("Otra justificación", datetime(2026, 11, 17, 12, 0))

    assert aviso.estado == EstadoAviso.DESCARTADO
    assert aviso.descarte is descarte_original
    assert aviso.descarte.justificacion == "Aviso duplicado"
    assert aviso.descarte.fecha_hora == fecha_original


# 9. Se intenta agregar una nota a un aviso aceptado. La operación se rechaza. Para armar ese aviso no hace falta implementar aceptar: piensen cómo construir un objeto en ese estado.
def test_aviso_aceptado_rechaza_nuevas_notas_sin_modificar_datos(aviso):
    aviso._estado = EstadoAviso.ACEPTADO

    with pytest.raises(OperacionAvisoInvalida):
        aviso.agregar_nota("Nota posterior", aviso.reportante, datetime(2026, 11, 17, 12, 0))

    assert aviso.estado == EstadoAviso.ACEPTADO
    assert aviso.notas == ()
    assert aviso.descarte is None

def test_nota_rechaza_autor_que_no_es_reportante():
    fecha = datetime(2026, 11, 18, 10, 0)

    with pytest.raises(OperacionAvisoInvalida):
        Nota("Hay un incendio", "Juan", fecha)


def test_nota_rechaza_texto_vacio():
    fecha = datetime(2026, 11, 18, 10, 0)
    reportante = Reportante("R001")

    with pytest.raises(OperacionAvisoInvalida):
        Nota("   ", reportante, fecha)


def test_descarte_conserva_justificacion_y_fecha():
    fecha = datetime(2026, 11, 18, 11, 0)

    descarte = Descarte("Aviso duplicado", fecha)

    assert descarte.justificacion == "Aviso duplicado"
    assert descarte.fecha_hora == fecha


def test_descarte_rechaza_justificacion_vacia():
    fecha = datetime(2026, 11, 18, 11, 0)

    for justificacion in ("", "   "):
        with pytest.raises(OperacionAvisoInvalida):
            Descarte(justificacion, fecha)