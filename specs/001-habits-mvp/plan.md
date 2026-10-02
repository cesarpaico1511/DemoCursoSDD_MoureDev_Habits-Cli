# Plan técnico — MVP de habits-cli

**Destino:** `specs/001-habits-mvp/plan.md`  
**Estado:** aprobado; especificación y guía de trabajo sincronizadas.

Implementar las tres operaciones aprobadas con Python 3.12+, biblioteca estándar, `argparse`, `unittest` y persistencia JSON local. El desarrollo será secuencial y para una sola persona. Este documento contiene diseño, datos de ejemplo y pseudocódigo, sin implementación.

## 1. Estructura de módulos y responsabilidades

| Componente | Responsabilidad | RF cubiertos |
|---|---|---|
| `habits/core.py` | Modelo de hábito; validación y comparación de nombres; creación; marcado; cálculo de rachas y resúmenes. Funciones puras, sin archivos, terminal ni consultas al reloj. | RF-1 a RF-6 |
| `habits/storage.py` | Leer, validar y convertir el JSON; guardar mediante reemplazo atómico; comunicar errores de persistencia. | RF-7; invariantes de RF-2 y RF-3 |
| `habits/cli.py` | Interpretar argumentos, capturar la fecha local, coordinar operaciones, presentar mensajes y establecer códigos de salida. | RF-1 a RF-8 |
| Entrada del paquete | Permitir `python -m habits` y delegar en la CLI, sin lógica de negocio. | RF-8 |
| Directorio de pruebas | Pruebas de dominio, persistencia y contrato de CLI. | RF-1 a RF-8 |

El paquete tendrá los archivos convencionales de inicialización y entrada. La ejecución inicial se documentará desde la raíz del repositorio; la ubicación de los datos será independiente del directorio de trabajo.

**Interfaces internas:**

- El dominio utiliza un modelo `Habit` con `name` y una colección inmutable de fechas `completed_dates`.
- Crear y marcar devuelven una nueva colección; no modifican la recibida.
- El marcado devuelve además si produjo un cambio, para evitar guardar un marcado repetido.
- El resumen de cada hábito contiene nombre, racha y estado de hoy.
- Los errores de dominio y persistencia contienen motivos identificables en inglés; la CLI los convierte en mensajes españoles.
- Las funciones públicas llevan anotaciones de tipos. Los identificadores, comentarios y docstrings estarán en inglés.

**Flujo de una operación:**

Interpretar argumentos → capturar una sola fecha local → validar el nombre, si corresponde → cargar y validar datos → ejecutar la operación de dominio → guardar únicamente si hubo cambios → presentar el resultado.

La ayuda y los errores de sintaxis terminan antes de acceder a los datos. El dominio recibe `today` explícitamente; nunca consulta la fecha real.

## 2. Modelo JSON, nombres y persistencia

**Cobertura: RF-1, RF-2, RF-3, RF-6 y RF-7.**

### Ubicación y ejemplo

La colección se guardará en `~/.habits-cli/habits.json`, resolviendo `~` como la carpeta personal del usuario. No habrá una opción pública para cambiar la ubicación en este MVP; las pruebas usarán rutas temporales inyectadas internamente.

```json
{
  "version": 1,
  "habits": [
    {
      "name": "Leer Python",
      "completed_dates": [
        "2026-09-29",
        "2026-09-30",
        "2026-10-01"
      ]
    },
    {
      "name": "Repasar inglés",
      "completed_dates": []
    }
  ]
}
```

Con fecha de referencia **2026-10-02**, el primer hábito tiene racha **3** y está pendiente hoy; el segundo tiene racha **0** y también está pendiente.

### Reglas del modelo

- `version` es el entero `1`; otras versiones se rechazan sin modificar el archivo.
- `habits` es una lista cuyo orden representa el orden de creación. Los nuevos hábitos se añaden al final.
- Cada hábito contiene exclusivamente `name` y `completed_dates`.
- Las fechas son cadenas de calendario válidas en formato estricto `YYYY-MM-DD`, únicas, ordenadas de menor a mayor y no posteriores a `today`.
- No se guardan identificadores adicionales, rachas ni estados diarios: se derivan del nombre y las fechas.
- Una colección vacía válida conserva la estructura del documento y contiene `habits` vacío.
- Se rechazan tipos incorrectos, campos ausentes o desconocidos, claves JSON repetidas y nombres equivalentes entre hábitos.
- No habrá migraciones ni reparaciones automáticas.

### Política de nombres acordada

- Se admiten nombres Unicode legibles **sin límite fijo de longitud**.
- Se rechazan tabulaciones, saltos de línea y caracteres de control, incluso en los extremos.
- Se eliminan los espacios en los extremos, se aplica normalización Unicode NFC y se rechaza el resultado vacío o con caracteres no imprimibles.
- Se conservan las mayúsculas, tildes y espacios interiores del nombre presentado.
- La clave de comparación se obtiene aplicando `casefold` al nombre normalizado y normalizando nuevamente a NFC. Se usa la misma operación al crear y buscar.
- No se eliminan tildes ni se comprimen espacios interiores: `café` y `cafe` son distintos; `Leer Python` y `Leer  Python` también.

NFC permite unificar representaciones canónicamente equivalentes sin aplicar las equivalencias adicionales de compatibilidad de NFKC. [Referencia de normalización Unicode](https://docs.python.org/3.12/library/unicodedata.html#unicodedata.normalize).

### Lectura y guardado

- Un archivo inexistente representa una colección vacía. Listar en esa situación no crea archivos ni directorios.
- Un archivo existente vacío, ilegible, con codificación incorrecta o que incumpla el modelo produce un error. Su contenido se conserva.
- La carga valida la colección completa antes de permitir operaciones. No corrige silenciosamente nombres, fechas ni duplicados.
- El guardado valida la nueva colección y escribe JSON UTF-8 legible, con sangría de dos espacios, caracteres Unicode sin escapes innecesarios y salto final.
- La carpeta de datos se crea únicamente cuando una operación necesita guardar.
- Se escribe un archivo temporal en la misma carpeta del destino; se vacían los búferes, se sincroniza el archivo, se cierra y se sustituye el destino mediante `os.replace`.
- Nunca se abre el archivo definitivo para truncarlo. La confirmación de éxito ocurre después del reemplazo.
- Ante un fallo previo al reemplazo, se conservan los datos anteriores y se intenta eliminar el temporal creado por esa operación.
- Listar y repetir un marcado ya realizado hoy no ejecutan el guardado.

El temporal comparte sistema de archivos con el destino para permitir el reemplazo atómico. [Referencias de `os.replace` y sincronización](https://docs.python.org/3.12/library/os.html#os.replace).

**Interrupciones:** antes del reemplazo permanece la versión anterior; después permanece la nueva versión completa, aunque el proceso no alcance a confirmar el éxito. No se recuperan automáticamente temporales abandonados. Este diseño protege contra escrituras parciales durante la operación; no promete durabilidad absoluta frente a fallos físicos del dispositivo.

## 3. Fecha y algoritmo de racha

**Cobertura: RF-3, RF-4 y RF-5.**

La CLI captura la fecha local al comenzar la ejecución del subcomando, antes de leer los datos. Esa fecha permanece fija durante toda la operación, aunque se atraviese medianoche. La siguiente operación obtiene una fecha nueva.

El dominio trabaja con fechas de calendario, sin medir intervalos de 24 horas. Un cambio estacional de hora no añade ni elimina días de racha.

**Pseudocódigo no ejecutable:**

```text
FUNCTION current_streak(completed_dates, today)
    days ← SET(completed_dates)

    IF today IN days THEN
        cursor ← today
    ELSE IF today > MIN_DATE AND PREVIOUS_DAY(today) IN days THEN
        cursor ← PREVIOUS_DAY(today)
    ELSE
        RETURN 0
    END IF

    length ← 0

    WHILE cursor IN days DO
        length ← length + 1

        IF cursor = MIN_DATE THEN
            BREAK
        END IF

        cursor ← PREVIOUS_DAY(cursor)
    END WHILE

    RETURN length
END FUNCTION
```

- Si hoy está cumplido, la secuencia termina hoy.
- Si hoy está pendiente y ayer está cumplido, la secuencia termina ayer.
- En otro caso, la racha es cero.
- Un hueco termina el recorrido; las secuencias anteriores al hueco no se suman.
- Marcar hoy añade exclusivamente la fecha capturada, si todavía no existe.
- El coste por hábito es lineal respecto a sus fechas registradas; no recorre años sin actividad.

## 4. Contrato de la CLI

**Cobertura: RF-1 a RF-8.**

### Comandos

| Comando | Comportamiento | RF |
|---|---|---|
| `python -m habits add "Leer Python"` | Crea el hábito; confirma nombre, racha 0 y estado pendiente. | RF-1, RF-2, RF-7 |
| `python -m habits done "Leer Python"` | Marca hoy o informa de que ya estaba marcado; muestra la racha resultante. | RF-2 a RF-5, RF-7 |
| `python -m habits list` | Lista todos los hábitos en orden de creación. | RF-4 a RF-6 |
| `python -m habits --help` | Muestra ayuda general en español, sin acceder a los datos. | RF-8 |
| Ayuda de cada subcomando | Explica su uso, argumentos y ejemplos en español. | RF-8 |

`add` y `done` reciben exactamente un nombre. Los nombres con espacios se pasan entre comillas. Un nombre que comienza con guion se puede pasar después de `--`.

No existen alias, preguntas interactivas, abreviaturas de opciones ni opción de fecha. Un argumento como `--date`, incluso acompañado de la fecha actual, se rechaza como opción no admitida.

### Salidas normales

Los resultados y la ayuda se escriben en `stdout`; los errores gestionados, en `stderr`. Cada salida termina en un salto de línea.

| Situación | Salida |
|---|---|
| Creación | `Hábito creado: {name}. Racha: 0 días. Pendiente hoy.` |
| Primer marcado de hoy | `Hábito marcado como hecho hoy: {name}. Racha: {n} días. Hecho hoy.` |
| Marcado repetido | `El hábito ya estaba hecho hoy: {name}. Racha: {n} días. Hecho hoy.` |
| Colección vacía | `Todavía no hay hábitos.` |

Para las rachas, se usa `1 día` y `{n} días` en los demás casos.

El listado no vacío contiene una cabecera **Nombre**, **Racha (días)** y **Estado**, seguida de una línea por hábito, con columnas separadas por tabulaciones. La racha se presenta como número y el estado es exactamente `Hecho hoy` o `Pendiente hoy`. No se añaden colores, bordes ni ordenaciones adicionales.

### Errores y códigos de salida

| Código | Significado |
|---|---|
| `0` | Operación exitosa, ayuda, listado vacío o marcado repetido. |
| `1` | Nombre inválido, nombre duplicado, hábito inexistente, datos inválidos o fallo de lectura/guardado. |
| `2` | Sintaxis incorrecta: falta un comando o argumento, comando desconocido, argumento adicional u opción no admitida. |

Los mensajes gestionados comienzan con `Error:` y explican el motivo en español. Los errores de acceso indican también la ruta afectada y una orientación breve para revisarla. No muestran trazas ni mensajes del sistema operativo sin traducir.

Los errores de sintaxis muestran `Error: comando o argumentos no válidos.` y el uso válido. La presentación de ayuda, uso y errores de `argparse` se adapta al español sin sustituir su análisis de argumentos. [Referencia de `argparse`](https://docs.python.org/3.12/library/argparse.html).

**Precedencia:** sintaxis → validez del nombre → lectura y validación de datos → existencia o duplicidad del hábito → guardado. Un fallo interrumpe las etapas posteriores.

## 5. Decisiones técnicas y alternativas descartadas

| Decisión | Justificación | Alternativa descartada | RF |
|---|---|---|---|
| Python 3.12+ y biblioteca estándar | Cumple la constitución y el mínimo indicado por el repositorio. | Dependencias de ejecución externas. | Todos |
| `argparse` | Suficiente para tres subcomandos; viene con Python. | Click o Typer: añaden dependencias innecesarias. | RF-8 |
| Tres módulos principales | Separa responsabilidades sin introducir capas adicionales. | Framework de servicios, repositorios abstractos o contenedor de dependencias. | Todos |
| Modelo `Habit` con fechas e interfaces puras | Hace explícitos los datos y permite comprobar reglas sin terminal ni archivos. | Diccionarios modificados directamente desde los comandos. | RF-1 a RF-6 |
| JSON versionado y validación explícita | Formato requerido y fácil de inspeccionar para aprender. | SQLite o un validador externo. | RF-7 |
| Lista de hábitos y lista de fechas | Conserva orden de creación y suficiente información para calcular rachas. | Guardar únicamente un contador y la última fecha. | RF-3, RF-5, RF-6 |
| NFC y comparación sin distinguir mayúsculas | Evita nombres visualmente equivalentes duplicados, conservando tildes. | Comparación literal o eliminación de acentos. | RF-2 |
| Archivo en la carpeta personal | Mantiene una colección estable entre directorios de trabajo. | Una colección distinta en cada carpeta. | RF-7 |
| Fecha capturada una vez | Evita resultados inconsistentes dentro de una operación que cruza medianoche. | Consultar el reloj durante cada cálculo. | RF-4, RF-5 |
| Temporal y reemplazo atómico | Evita dejar el documento definitivo parcialmente escrito. | Sobrescritura directa. | RF-7 |
| `unittest`, temporales y simulación de fallos | Cumple la política de pruebas sin dependencias externas. | `pytest`: dependencia externa incompatible con la constitución. | Todos |

Se conserva el supuesto de uso secuencial: no se añaden bloqueos entre procesos, sincronización, recuperación automática ni nuevas operaciones de usuario.

## 6. Estrategia de tests y condiciones previas

### Organización

- **Dominio:** pruebas unitarias con fechas explícitas y colecciones en memoria. Comprobar resultados y que las entradas permanezcan intactas.
- **Persistencia:** pruebas con directorios temporales y documentos válidos e inválidos. Simular fallos de lectura, escritura, sincronización y reemplazo.
- **CLI:** ejecutar su coordinador con argumentos, ruta temporal y proveedor de fecha controlados; capturar ambos canales de salida y comprobar códigos.
- **Integración:** ejecutar el punto de entrada en procesos separados con una carpeta personal temporal para comprobar conservación de datos entre ejecuciones.
- Usar exclusivamente `unittest`, `unittest.mock` y utilidades de la biblioteca estándar. No esperar al reloj real ni utilizar los datos personales del desarrollador.

### Matriz de cobertura

| RF | Escenarios mínimos |
|---|---|
| **RF-1** | Creación inicial y posterior; nombre presentado correctamente; racha 0; pendiente hoy; incorporación al final de la colección. |
| **RF-2** | Vacío, solo espacios, controles y saltos de línea; nombres de más de 80 caracteres; diferencias de mayúsculas; equivalencia Unicode; tildes y espacios interiores; nombres con guion inicial; mismas reglas al crear y buscar. |
| **RF-3** | Primer marcado; repetición exitosa sin guardar; hábito inexistente; un cumplimiento por fecha; independencia entre varios hábitos. |
| **RF-4** | Captura única de fecha; operación que cruza medianoche; siguiente operación en el día nuevo; fines de semana; días de 23/25 horas; rechazo de argumentos de fecha. |
| **RF-5** | Sin fechas: 0; solo hoy: 1; tres días hasta ayer: 3; añadir hoy: 4; último cumplimiento anteayer: 0; hueco interno; hoy sin ayer: 1; reinicio tras interrupción; cambio de mes/año y febrero bisiesto. |
| **RF-6** | Colección vacía; orden estable; columnas y estados; varios hábitos con rachas diferentes; ninguna llamada al guardado. |
| **RF-7** | Archivo ausente frente a existente vacío; UTF-8 y JSON inválidos; tipos y versiones incorrectos; duplicados; fechas imposibles o futuras; lectura sin permisos; fallos antes del reemplazo; conservación exacta de los bytes anteriores; reapertura tras guardado exitoso. |
| **RF-8** | Ayuda general y por comando; argumentos ausentes o adicionales; comando y opción desconocidos; códigos 0/1/2; separación de canales; mensajes españoles; ningún acceso a datos ante errores sintácticos. |

Añadir una comprobación del límite inferior de fechas para evitar desbordamientos al buscar el día anterior. Los fallos de permisos se simulan para que las pruebas sean reproducibles tanto en Windows como en otros entornos.

**Ejecución prevista:** `python -m unittest discover -s tests -v`. Cada bug corregido incorporará una prueba de regresión; todas las pruebas deberán pasar.

### Preparación documental antes de implementar

Para respetar «spec primero», las precisiones observables aprobadas de este plan se han reflejado en la especificación: política Unicode y caracteres permitidos, ausencia de límite fijo, fecha congelada durante la operación, información mostrada al marcar, definición de datos inválidos y resultado de una interrupción alrededor del guardado. También quedan recogidos los códigos de salida y la precedencia de errores.

`AGENTS.md` está alineado con `unittest` y ya no contiene una excepción para `pytest`. La constitución permanece como autoridad para esa decisión.

La preparación documental está completada. La implementación de la aplicación no ha comenzado. Este plan no representa código implementado ni pruebas ejecutadas.
