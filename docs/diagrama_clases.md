```mermaid
classDiagram
    direction TB

    class Aviso {
        -str ubicacion
        -str descripcion
        +agregar_nota(texto, autor, fecha_hora)
        +descartar(justificacion, fecha_hora)
    }
```