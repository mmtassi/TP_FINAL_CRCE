# Avance 1 - Avisos y notas

## 1. Diagrama de clases

```mermaid
classDiagram
    direction TB

    class Reportante {
        -str _identificador
        +str identificador
        +__init__(identificador)
    }

    class Aviso {
        -str _ubicacion
        -TipoSituacion _tipo_situacion
        -Gravedad _gravedad_estimada
        -str _descripcion
        -Reportante _reportante
        -datetime _fecha_registro
        -EstadoAviso _estado
        -list~Nota~ _notas
        -Descarte _descarte
        +str ubicacion
        +TipoSituacion tipo_situacion
        +Gravedad gravedad_estimada
        +str descripcion
        +Reportante reportante
        +datetime fecha_registro
        +EstadoAviso estado
        +tuple notas
        +Descarte descarte
        +__init__(ubicacion, tipo_situacion, gravedad_estimada, descripcion, reportante, fecha_registro)
        +agregar_nota(texto, autor, fecha_hora)
        +descartar(justificacion, fecha_hora)
        -_exigir_pendiente()
    }

    class Nota {
        <<valor_inmutable>>
        +str texto
        +Reportante autor
        +datetime fecha_hora
        +__init__(texto, autor, fecha_hora)
        +__post_init__()
    }

    class Descarte {
        <<valor_inmutable>>
        +str justificacion
        +datetime fecha_hora
        +__init__(justificacion, fecha_hora)
        +__post_init__()
    }

    class EstadoAviso {
        <<enumeration>>
        PENDIENTE
        ACEPTADO
        DESCARTADO
    }

    class TipoSituacion {
        <<enumeration>>
        INUNDACION
        INCENDIO
        ACCIDENTE_VIAL
    }

    class Gravedad {
        <<enumeration>>
        BAJA
        MEDIA
        ALTA
    }

    class OperacionAvisoInvalida {
        <<exception>>
    }

    Reportante "1" -- "0..*" Aviso : registra
    Reportante "1" -- "0..*" Nota : autor de

    Aviso "1" *-- "0..*" Nota : contiene
    Aviso "1" *-- "0..1" Descarte : conserva

    Aviso ..> EstadoAviso : utiliza
    Aviso ..> TipoSituacion : utiliza
    Aviso ..> Gravedad : utiliza

    Aviso ..> OperacionAvisoInvalida : lanza
    Nota ..> OperacionAvisoInvalida : lanza
    Descarte ..> OperacionAvisoInvalida : lanza
```

## 2. Diagrama de estados

```mermaid

stateDiagram-v2
    direction TB

    [*] --> PENDIENTE : Registrar aviso

    PENDIENTE --> PENDIENTE : agregar_nota()
    PENDIENTE --> DESCARTADO : descartar() con justificación válida
    PENDIENTE --> ACEPTADO : aceptar() - futuro, no implementado

    note right of PENDIENTE
        Permite agregar notas.
        Rechaza notas sin texto.
        Rechaza descartes sin justificación.
    end note

    note right of DESCARTADO
        Rechaza agregar_nota().
        Rechaza descartar() nuevamente.
        No permite nuevas evaluaciones.
    end note

    note right of ACEPTADO
        Rechaza agregar_nota().
        Rechaza descartar().
        No permite nuevas evaluaciones.
    end note

```

## 3. Tarjetas CRC

### Aviso

**Qué sabe:** ubicación, tipo de situación, gravedad, descripción, reportante, fecha de registro, estado, notas y descarte.

**Responsabilidades:**
- Registrar un aviso en estado pendiente.
- Permitir agregar notas mientras esté pendiente.
- Descartar un aviso con una justificación.
- Rechazar operaciones que no correspondan a su estado.

**Colaboradores:** Reportante, Nota y Descarte.

### Reportante

**Qué sabe:** su identificador.

**Responsabilidad:** representar al reportante de un aviso y permitir consultar su identificador.

**Colaboradores:** Aviso y Nota.

### Nota

**Qué sabe:** texto, autor y fecha y hora.

**Responsabilidades:**
- Conservar los datos de una nota.
- Validar que tenga un autor válido y texto no vacío.

**Colaboradores:** Reportante y Aviso.

### Descarte

**Qué sabe:** justificación y fecha y hora.

**Responsabilidades:**
- Conservar los datos del descarte.
- Validar que la justificación no esté vacía.

**Colaborador:** Aviso.

## 4. Decisiones de diseño

La verificación del autor de las notas será responsabilidad de la clase `Aviso`, porque conoce al reportante que lo registró. Entonces, cuando se agregue una nota, va a poder comprobar que el autor sea ese mismo reportante y, además, que el aviso esté pendiente.

Elegí esta opción para mantener las reglas adentro de la clase y evitar que se puedan agregar notas sin realizar las verificaciones correspondientes. Por ejemplo, si esta comprobación se hiciera únicamente en la capa de aplicación, se podría llamar directamente al método `agregar_nota()` y saltarse esa verificación.