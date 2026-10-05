# Tareas — MVP de habits-cli

**Destino:** `specs/001-habits-mvp/tasks.md`  
**Estado:** T01 y T02 completadas; T03–T34 pendientes.

Desglose de la especificación y el plan aprobados. Las tareas están ordenadas por dependencia y tienen estimaciones de **15–30 minutos**, incluyendo su comprobación.

**Reglas de ejecución:** usar únicamente la biblioteca estándar y `unittest`; mantener identificadores, comentarios y docstrings en inglés y mensajes al usuario en español. Ejecutar `python -m unittest discover -s tests -v` al cerrar cada tarea y registrar el resultado real. Cada corrección de un bug requiere una prueba de regresión. Los datos de pruebas serán temporales.

## 1. Estructura y lógica de dominio

- [x] **T01 — Preparar el paquete y la estructura de pruebas.**  
  **Estimación:** 20 min · **RF:** RF-1 a RF-8, soporte transversal · **Depende de:** ninguna.  
  **Hecho cuando:** existen los módulos previstos y el directorio de pruebas; los módulos se importan sin acceder a archivos ni consultar el reloj, y el descubrimiento de pruebas funciona sin dependencias externas.
  **Validación T01 (2026-10-05):** tests escritos antes del paquete; ejecución inicial de `pytest -q`: `3 failed in 7.35s` por ausencia de `habits`. Tras crear la estructura, `pytest -q`: `3 passed in 2.67s` (código 0). `python -B -S -m unittest discover -s tests -v`: `Ran 3 tests in 2.183s`, `OK` (código 0), con paquetes externos deshabilitados. Python 3.12.14; `pytest` se utilizó únicamente como ejecutor en un entorno temporal externo al proyecto. Las pruebas de `tests/test_scaffolding.py` verifican los módulos previstos, las importaciones sin acceso a archivos de datos ni al reloj y la ausencia de dependencias externas. Cobertura: RF-1 a RF-8 como soporte transversal; todavía no se implementa su comportamiento funcional.

- [x] **T02 — Definir el modelo de hábito y los errores de dominio.**  
  **Estimación:** 20 min · **RF:** RF-1, RF-2, RF-3, RF-5, RF-6 · **Depende de:** T01.  
  **Hecho cuando:** un hábito contiene nombre y fechas inmutables, las interfaces públicas tienen anotaciones de tipos y los errores distinguen nombre inválido, duplicado y hábito inexistente.
  **Validación T02 (2026-10-05):** seis tests escritos antes del código: `pytest -q` detectó inicialmente 6 fallos por ausencia del modelo y los errores, mientras las 3 pruebas de T01 pasaban. Tras implementar `Habit` inmutable y los errores con motivos en inglés, `pytest -q`: `9 passed, 5 subtests passed in 2.42s` (código 0). Se desactivó únicamente la caché del ejecutor mediante `PYTEST_ADDOPTS=-p no:cacheprovider` por falta de permisos sobre la caché anterior. `python -m unittest discover -s tests -v`: `Ran 9 tests in 2.172s`, `OK` (código 0). `tests/test_core_model.py` comprueba conservación del nombre y las fechas, inmutabilidad, independencia de listas externas y distinción de errores. Las interfaces públicas tienen anotaciones de tipos. Cobertura de soporte: RF-1, RF-2, RF-3, RF-5 y RF-6; T03 y las operaciones de usuario siguen pendientes.

- [ ] **T03 — Implementar la validación y presentación de nombres.**  
  **Estimación:** 25 min · **RF:** RF-1, RF-2 · **Depende de:** T02.  
  **Hecho cuando:** pasan pruebas de recorte de extremos, normalización NFC, conservación de mayúsculas, nombres mayores de 80 caracteres y rechazo de vacíos, controles, tabulaciones y saltos de línea incluso en los extremos.

- [ ] **T04 — Implementar la comparación y búsqueda de nombres.**  
  **Estimación:** 20 min · **RF:** RF-2 · **Depende de:** T03.  
  **Hecho cuando:** las pruebas consideran equivalentes mayúsculas y representaciones Unicode canónicas, pero distinguen tildes y espacios interiores; creación y búsqueda utilizan la misma clave de comparación.

- [ ] **T05 — Implementar la creación de hábitos como operación pura.**  
  **Estimación:** 25 min · **RF:** RF-1, RF-2, RF-6 · **Depende de:** T04.  
  **Hecho cuando:** crear devuelve una colección nueva con el hábito al final y sin cumplimientos; un duplicado produce el error previsto y la colección original permanece intacta.

- [ ] **T06 — Implementar el marcado diario como operación pura.**  
  **Estimación:** 25 min · **RF:** RF-2, RF-3, RF-4 · **Depende de:** T05.  
  **Hecho cuando:** marcar añade únicamente la fecha recibida, repetir devuelve «sin cambios», un hábito inexistente produce error y las pruebas confirman que los otros hábitos y la entrada original se conservan.

- [ ] **T07 — Implementar el cálculo de racha del plan.**  
  **Estimación:** 25 min · **RF:** RF-4, RF-5 · **Depende de:** T02.  
  **Hecho cuando:** pasan los casos sin fechas, solo hoy, secuencia hasta ayer, último cumplimiento anteayer, hueco interno y hoy cumplido sin ayer; el cálculo no consulta el reloj.

- [ ] **T08 — Cubrir los límites de calendario de las rachas.**  
  **Estimación:** 20 min · **RF:** RF-4, RF-5 · **Depende de:** T07.  
  **Hecho cuando:** pasan pruebas de cambio de mes y año, febrero bisiesto, fines de semana, días de 23/25 horas y fecha mínima admitida, sin esperas reales ni desbordamientos.

- [ ] **T09 — Construir los resúmenes de hábitos.**  
  **Estimación:** 20 min · **RF:** RF-4, RF-5, RF-6 · **Depende de:** T06, T08.  
  **Hecho cuando:** cada resumen contiene nombre, racha y estado de hoy; las pruebas conservan el orden de creación y comprueban resultados independientes para varios hábitos sin modificar la colección.

## 2. Modelo JSON y persistencia

- [ ] **T10 — Implementar la serialización del modelo aprobado.**  
  **Estimación:** 20 min · **RF:** RF-1, RF-3, RF-6, RF-7 · **Depende de:** T09.  
  **Hecho cuando:** la salida contiene exclusivamente los campos previstos, versión 1, fechas ISO y orden de creación; utiliza Unicode legible, sangría de dos espacios y salto final, sin guardar rachas ni estados derivados.

- [ ] **T11 — Validar la estructura del documento JSON.**  
  **Estimación:** 25 min · **RF:** RF-7 · **Depende de:** T10.  
  **Hecho cuando:** las pruebas aceptan documentos válidos y rechazan JSON mal formado, versiones distintas de 1, tipos incorrectos, campos ausentes o desconocidos y claves repetidas.

- [ ] **T12 — Validar los nombres almacenados.**  
  **Estimación:** 20 min · **RF:** RF-2, RF-7 · **Depende de:** T04, T11.  
  **Hecho cuando:** nombres inválidos, presentaciones no canónicas y hábitos equivalentes provocan rechazo completo; las pruebas confirman que no se normalizan ni eliminan registros silenciosamente.

- [ ] **T13 — Validar las fechas almacenadas.**  
  **Estimación:** 25 min · **RF:** RF-3, RF-4, RF-7 · **Depende de:** T11.  
  **Hecho cuando:** se rechazan formatos distintos de `YYYY-MM-DD`, fechas imposibles, futuras, repetidas o desordenadas, utilizando la fecha de referencia recibida.

- [ ] **T14 — Implementar la ubicación personal y la lectura.**  
  **Estimación:** 25 min · **RF:** RF-7 · **Depende de:** T12, T13.  
  **Hecho cuando:** se resuelve la ubicación aprobada dentro de la carpeta personal, se admite una ruta interna para pruebas, un archivo ausente devuelve una colección vacía sin crear nada y los documentos válidos se cargan completamente.

- [ ] **T15 — Cubrir los errores de lectura y la preservación de datos.**  
  **Estimación:** 20 min · **RF:** RF-7 · **Depende de:** T14.  
  **Hecho cuando:** archivo vacío, UTF-8 inválido, datos corruptos y permisos insuficientes simulados producen errores identificables; los bytes originales permanecen intactos y nunca se devuelve una colección vacía como recuperación.

- [ ] **T16 — Implementar el guardado atómico.**  
  **Estimación:** 30 min · **RF:** RF-7 · **Depende de:** T10, T15.  
  **Hecho cuando:** se valida antes de guardar, se crea el directorio solo cuando corresponde y se escribe, sincroniza y cierra un temporal en la misma carpeta antes de reemplazar el destino; una lectura posterior recupera la colección completa.

- [ ] **T17 — Cubrir fallos del guardado y limpieza de temporales.**  
  **Estimación:** 30 min · **RF:** RF-7 · **Depende de:** T16.  
  **Hecho cuando:** fallos simulados al crear o escribir el temporal, sincronizar o reemplazar conservan el archivo anterior o su ausencia inicial; se comunica el fallo y se intenta limpiar únicamente el temporal de esa operación.

## 3. Contrato e integración de la CLI

- [ ] **T18 — Configurar el análisis de comandos con `argparse`.**  
  **Estimación:** 25 min · **RF:** RF-2, RF-4, RF-8 · **Depende de:** T04.  
  **Hecho cuando:** se reconocen `add`, `done` y `list`; los dos primeros requieren exactamente un nombre; se admiten nombres con espacios y guion inicial mediante `--`, y se rechazan argumentos adicionales, abreviaturas y opciones de fecha.

- [ ] **T19 — Presentar ayuda y errores sintácticos en español.**  
  **Estimación:** 25 min · **RF:** RF-8 · **Depende de:** T18.  
  **Hecho cuando:** la ayuda general y por comando incluye uso y ejemplos y termina con código 0; los errores sintácticos muestran el mensaje y uso acordados en `stderr`, con código 2.

- [ ] **T20 — Preparar la coordinación con fecha y ruta controlables.**  
  **Estimación:** 25 min · **RF:** RF-2, RF-4, RF-7, RF-8 · **Depende de:** T14, T19.  
  **Hecho cuando:** el coordinador admite proveedor de fecha y ruta internos para pruebas, captura una sola fecha antes de cargar datos y valida el nombre antes de acceder a la persistencia.

- [ ] **T21 — Conectar el comando de creación.**  
  **Estimación:** 20 min · **RF:** RF-1, RF-2, RF-7, RF-8 · **Depende de:** T05, T09, T17, T20.  
  **Hecho cuando:** `add` crea y guarda un hábito y, únicamente después del guardado exitoso, muestra en `stdout` el mensaje contratado, racha 0 y estado pendiente, terminando con código 0.

- [ ] **T22 — Conectar el comando de marcado.**  
  **Estimación:** 25 min · **RF:** RF-2, RF-3, RF-4, RF-5, RF-7, RF-8 · **Depende de:** T06, T09, T17, T20.  
  **Hecho cuando:** `done` muestra nombre, racha y estado con los mensajes acordados; el marcado repetido termina con código 0 sin llamar al guardado, y las pruebas comprueban `1 día` frente a otros valores.

- [ ] **T23 — Conectar el comando de listado.**  
  **Estimación:** 20 min · **RF:** RF-4, RF-5, RF-6, RF-7, RF-8 · **Depende de:** T09, T20.  
  **Hecho cuando:** `list` presenta cabecera y columnas tabuladas en orden de creación, o el mensaje de colección vacía; devuelve código 0 y nunca guarda ni crea almacenamiento.

- [ ] **T24 — Traducir los errores de dominio y persistencia.**  
  **Estimación:** 30 min · **RF:** RF-2, RF-3, RF-7, RF-8 · **Depende de:** T21, T22, T23.  
  **Hecho cuando:** nombres inválidos, duplicados, hábitos inexistentes y fallos de datos o acceso generan código 1 y mensajes españoles iniciados con `Error:`; los errores de acceso incluyen ruta y orientación, sin trazas ni confirmación de éxito.

- [ ] **T25 — Verificar la precedencia de errores y los canales.**  
  **Estimación:** 20 min · **RF:** RF-2, RF-7, RF-8 · **Depende de:** T24.  
  **Hecho cuando:** pruebas con errores simultáneos confirman el orden sintaxis → nombre → datos → existencia o duplicidad → guardado; ayuda y sintaxis inválida no acceden a datos, y las salidas respetan `stdout`/`stderr`.

- [ ] **T26 — Conectar el punto de entrada del paquete.**  
  **Estimación:** 15 min · **RF:** RF-8 · **Depende de:** T25.  
  **Hecho cuando:** `python -m habits` delega en la CLI y propaga sus códigos de salida; la ayuda y los errores de sintaxis se comprueban desde un proceso real.

- [ ] **T27 — Verificar el cambio de día durante una operación.**  
  **Estimación:** 20 min · **RF:** RF-4, RF-5, RF-7 · **Depende de:** T22, T23.  
  **Hecho cuando:** un reloj simulado confirma una única consulta por operación, fecha constante al atravesar medianoche y nueva fecha en la operación siguiente, con resultados correctos de marcado y racha.

## 4. Integración, documentación y cierre

- [ ] **T28 — Preparar el entorno aislado de integración.**  
  **Estimación:** 20 min · **RF:** RF-4, RF-7, RF-8 · **Depende de:** T26, T27.  
  **Hecho cuando:** el soporte de pruebas ejecuta procesos separados con carpeta personal temporal y fecha controlada desde las pruebas, captura salidas y códigos y no requiere opciones públicas nuevas ni datos personales reales.

- [ ] **T29 — Comprobar el recorrido completo de usuario.**  
  **Estimación:** 25 min · **RF:** RF-1, RF-2, RF-3, RF-5, RF-6, RF-7, RF-8 · **Depende de:** T28.  
  **Hecho cuando:** crear dos hábitos, rechazar un duplicado, marcar uno, repetir el marcado y listar en procesos posteriores conserva nombres, orden, cumplimientos y rachas; repetir no altera los bytes guardados.

- [ ] **T30 — Verificar independencia del directorio de trabajo.**  
  **Estimación:** 20 min · **RF:** RF-6, RF-7 · **Depende de:** T29.  
  **Hecho cuando:** procesos ejecutados desde dos directorios distintos, con el paquete disponible y la misma carpeta personal temporal, consultan la misma colección sin crear archivos de datos en esos directorios.

- [ ] **T31 — Comprobar interrupciones alrededor de la confirmación.**  
  **Estimación:** 30 min · **RF:** RF-7, RF-8 · **Depende de:** T17, T21, T22, T24.  
  **Hecho cuando:** interrupciones simuladas antes del reemplazo conservan los datos anteriores y, después del reemplazo pero antes del mensaje de éxito, dejan la nueva colección completa; no hay restauración automática ni documento parcial.

- [ ] **T32 — Documentar el uso y la verificación del MVP.**  
  **Estimación:** 20 min · **RF:** RF-1 a RF-8 · **Depende de:** T30, T31.  
  **Hecho cuando:** el README explica en español requisitos, ejecución, los tres comandos, nombres y comillas, rachas, ubicación de datos, códigos de salida, errores y ejecución de pruebas; los ejemplos coinciden con el contrato aprobado.

- [ ] **T33 — Revisar el cumplimiento de la constitución.**  
  **Estimación:** 20 min · **RF:** RF-1 a RF-8, revisión transversal · **Depende de:** T32.  
  **Hecho cuando:** la revisión confirma cero dependencias externas, pruebas con `unittest`, lógica sin entrada/salida ni reloj, persistencia separada y atómica, anotaciones públicas, idiomas correctos y ausencia de funcionalidades fuera del MVP.

- [ ] **T34 — Cerrar la trazabilidad y registrar la validación final.**  
  **Estimación:** 20 min · **RF:** RF-1 a RF-8 · **Depende de:** T33.  
  **Hecho cuando:** cada criterio de aceptación y caso límite está vinculado a una prueba identificable, la suite completa ejecuta pruebas reales y termina sin fallos, y se registran en este documento el comando, el número de pruebas y el resultado.

**Condición de cierre:** todas las casillas están respaldadas por sus comprobaciones. Un resultado de cero pruebas ejecutadas no acredita la finalización del MVP.
