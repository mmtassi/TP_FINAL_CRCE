from datetime import datetime
import pytest

from dominio.aviso import Aviso
from dominio.reportante import Reportante
from dominio.enumeraciones import EstadoAviso, TipoSituacion, Gravedad
from dominio.excepciones import OperacionAvisoInvalida


@pytest.fixture
def aviso():
    reportante = Reportante("R001")
    return Aviso(
        "Av. San Martín 150",
        TipoSituacion.INCENDIO,
        Gravedad.ALTA,
        "Incendio en una vivienda",
        reportante,
        datetime(2026, 11, 17, 10, 0),
    )


# 1. Un aviso recién registrado está pendiente, no tiene notas y no tiene descarte.
def test_aviso_nuevo_comienza_pendiente(aviso):
    assert aviso.estado == EstadoAviso.PENDIENTE
    assert aviso.ubicacion == "Av. San Martín 150"
    assert aviso.tipo_situacion == TipoSituacion.INCENDIO
    assert aviso.gravedad_estimada == Gravedad.ALTA
    assert aviso.descripcion == "Incendio en una vivienda"
    assert aviso.reportante.identificador == "R001"
    assert aviso.fecha_registro == datetime(2026, 11, 17, 10, 0)
    assert aviso.notas == ()
    assert aviso.descarte is None


# 2. Se agrega una nota a un aviso pendiente y la nota conserva autor, fecha y hora.
def test_nota_conserva_autor_y_fecha(aviso):
    fecha = datetime(2026, 11, 17, 10, 30)
    aviso.agregar_nota("Hay personas atrapadas", aviso.reportante, fecha)

    assert len(aviso.notas) == 1
    nota = aviso.notas[0]
    assert nota.texto == "Hay personas atrapadas"
    assert nota.autor == aviso.reportante
    assert nota.fecha_hora == fecha
    assert aviso.estado == EstadoAviso.PENDIENTE


# 3. Se agregan dos notas y se conservan las dos, en el orden en que llegaron.
def test_r2_dos_notas_conservan_el_orden(aviso):
    aviso.agregar_nota("Primera nota", aviso.reportante, datetime(2026, 11, 17, 10, 30))
    aviso.agregar_nota("Segunda nota", aviso.reportante, datetime(2026, 11, 17, 10, 45))

    assert len(aviso.notas) == 2
    assert aviso.notas[0].texto == "Primera nota"
    assert aviso.notas[1].texto == "Segunda nota"


# 4. Después de agregar una nota, la ubicación, el tipo, la gravedad estimada y la descripción siguen iguales.
def test_r3_agregar_nota_no_modifica_datos_originales(aviso):
    ubicacion_original = aviso.ubicacion
    tipo_original = aviso.tipo_situacion
    gravedad_original = aviso.gravedad_estimada
    descripcion_original = aviso.descripcion
    reportante_original = aviso.reportante
    fecha_original = aviso.fecha_registro

    aviso.agregar_nota("Información adicional", aviso.reportante, datetime(2026, 11, 17, 11, 0))

    assert aviso.ubicacion == ubicacion_original
    assert aviso.tipo_situacion == tipo_original
    assert aviso.gravedad_estimada == gravedad_original
    assert aviso.descripcion == descripcion_original
    assert aviso.reportante == reportante_original
    assert aviso.fecha_registro == fecha_original


# 5. Se descarta un aviso pendiente con justificación: queda descartado y conserva lajustificación y la fecha.
def test_r4_descartar_aviso_con_justificacion(aviso):
    fecha = datetime(2026, 11, 17, 12, 0)
    aviso.descartar("El incidente ya fue resuelto", fecha)

    assert aviso.estado == EstadoAviso.DESCARTADO
    assert aviso.descarte is not None
    assert aviso.descarte.justificacion == "El incidente ya fue resuelto"
    assert aviso.descarte.fecha_hora == fecha


# 6. Se intenta descartar con una justificación vacía o con solo espacios. La operación serechaza y el aviso sigue pendiente.
def test_r4_r6_descartar_sin_justificacion_no_modifica_aviso(aviso):
    fecha = datetime(2026, 11, 17, 12, 0)

    for justificacion in ("", "   "):
        with pytest.raises(OperacionAvisoInvalida):
            aviso.descartar(justificacion, fecha)

        assert aviso.estado == EstadoAviso.PENDIENTE
        assert aviso.descarte is None
        assert aviso.notas == ()


# 7. Se intenta agregar una nota a un aviso descartado. La operación se rechaza y las notasno cambian.
def test_r5_r6_aviso_descartado_rechaza_nuevas_notas(aviso):
    aviso.agregar_nota("Nota anterior", aviso.reportante, datetime(2026, 11, 17, 10, 30))
    aviso.descartar("Aviso duplicado", datetime(2026, 11, 17, 11, 0))
    notas_anteriores = aviso.notas
    descarte_original = aviso.descarte

    with pytest.raises(OperacionAvisoInvalida):
        aviso.agregar_nota("Nueva nota", aviso.reportante, datetime(2026, 11, 17, 12, 0))

    assert aviso.estado == EstadoAviso.DESCARTADO
    assert aviso.notas == notas_anteriores
    assert aviso.descarte is descarte_original


# 8. Se intenta descartar por segunda vez. La operación se rechaza y se conserva lajustificación original.
def test_r5_r6_segundo_descarte_conserva_el_original(aviso):
    fecha_original = datetime(2026, 11, 17, 11, 0)
    aviso.descartar("Aviso duplicado", fecha_original)
    descarte_original = aviso.descarte

    with pytest.raises(OperacionAvisoInvalida):
        aviso.descartar("Otra justificación", datetime(2026, 11, 17, 12, 0))

    assert aviso.estado == EstadoAviso.DESCARTADO
    assert aviso.descarte is descarte_original
    assert aviso.descarte.justificacion == "Aviso duplicado"
    assert aviso.descarte.fecha_hora == fecha_original


# 9. Se intenta agregar una nota a un aviso aceptado. La operación se rechaza. Para armarese aviso no hace falta implementar aceptar: piensen cómo construir un objeto en ese estado.
def test_r5_r6_aviso_aceptado_rechaza_nuevas_notas(aviso):
    # Preparación exclusiva del test: aceptar() no pertenece al Avance 1.
    aviso.estado = EstadoAviso.ACEPTADO

    with pytest.raises(OperacionAvisoInvalida):
        aviso.agregar_nota(
            "Nota posterior", aviso.reportante, datetime(2026, 11, 17, 12, 0)
        )

    assert aviso.estado == EstadoAviso.ACEPTADO
    assert aviso.notas == ()
    assert aviso.descarte is None

