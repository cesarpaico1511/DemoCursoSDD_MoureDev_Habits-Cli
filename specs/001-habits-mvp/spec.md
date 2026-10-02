# Especificación 001 — MVP de hábitos de estudio

**Estado:** aprobada.

## Contexto y objetivo

Las personas que estudian necesitan registrar su constancia de forma sencilla. La funcionalidad permitirá crear hábitos diarios, marcarlos como hechos hoy y consultar su racha actual desde una terminal.

El objetivo es identificar qué hábitos están pendientes hoy y cuántos días consecutivos se han cumplido, sin penalizar al usuario mientras el día actual siga en curso.

## Usuarios

Una persona que registra sus propios hábitos de estudio y conoce el uso básico de una terminal. El MVP es de uso personal, sin cuentas ni colaboración.

## Historias de usuario

- **HU-1:** Como estudiante, quiero crear un hábito con un nombre reconocible para empezar a registrar su cumplimiento.
- **HU-2:** Como estudiante, quiero marcar un hábito como hecho hoy para dejar constancia de mi actividad.
- **HU-3:** Como estudiante, quiero consultar mis hábitos, sus rachas y su estado de hoy para saber qué he cumplido y qué tengo pendiente.

## Requisitos funcionales y criterios de aceptación

### RF-1 — Crear un hábito

- **Cuando** el usuario solicite crear un hábito con un nombre válido y disponible, **el sistema deberá** registrarlo y confirmar su creación.
- **Cuando** se cree un hábito, **el sistema deberá** mostrarlo inicialmente con racha de 0 días y pendiente hoy.
- **Cuando** se reciba un nombre, **el sistema deberá** eliminar los espacios de sus extremos y conservar las mayúsculas y minúsculas elegidas para su presentación.

### RF-2 — Validar e identificar los nombres

- **El sistema deberá** identificar los hábitos por nombres únicos, sin distinguir mayúsculas y minúsculas ni espacios en sus extremos.
- **Si** el nombre está vacío o contiene únicamente espacios, **el sistema deberá** rechazar la creación, explicar el motivo y conservar los datos existentes.
- **Si** ya existe un hábito con un nombre equivalente, **el sistema deberá** rechazar la creación y comunicar que el hábito ya existe.
- **Cuando** se busque un hábito para marcarlo, **el sistema deberá** aplicar las mismas reglas de comparación utilizadas al crearlo.
- **El sistema deberá** admitir nombres Unicode legibles sin un límite fijo de longitud.
- **Si** un nombre contiene tabulaciones, saltos de línea o caracteres de control, incluso en sus extremos, **el sistema deberá** rechazarlo sin modificar los datos.
- **Cuando** se hayan eliminado los espacios de los extremos, **el sistema deberá** rechazar un nombre vacío o con caracteres no imprimibles.
- **El sistema deberá** considerar equivalentes las representaciones Unicode canónicamente equivalentes y presentar los nombres con una representación canónica común.
- **El sistema deberá** conservar las tildes y los espacios interiores: «café» y «cafe» identifican hábitos distintos, al igual que «Leer Python» y «Leer  Python».

### RF-3 — Marcar un hábito como hecho

- **Cuando** el usuario marque un hábito existente que está pendiente hoy, **el sistema deberá** registrar su cumplimiento para hoy y confirmar la operación.
- **Si** el hábito ya está hecho hoy, **el sistema deberá** informar de ello y terminar con éxito, sin añadir otro cumplimiento ni modificar la racha.
- **Si** el hábito indicado no existe, **el sistema deberá** comunicar el error sin crearlo ni modificar otros hábitos.
- **El sistema deberá** admitir como máximo un cumplimiento por hábito y fecha.
- **Cuando** un marcado termine con éxito, incluido un marcado repetido, **el sistema deberá** mostrar el nombre del hábito, su racha actual y el estado «Hecho hoy».
- **Cuando** se marque un hábito, **el sistema deberá** conservar los cumplimientos y el orden de creación de los demás hábitos.

### RF-4 — Determinar el día de cumplimiento

- **Cuando** comience una operación, antes de acceder a los datos, **el sistema deberá** obtener una sola fecha local de referencia y utilizarla como «hoy» durante toda esa operación.
- **El sistema deberá** considerar días de calendario consecutivos, incluidos fines de semana y festivos.
- **Si** una operación atraviesa medianoche, **el sistema deberá** conservar su fecha de referencia inicial; la siguiente operación utilizará la nueva fecha local.
- **El sistema deberá** contar días de calendario aunque un cambio estacional de hora produzca días de 23 o 25 horas.
- **Si** el usuario intenta registrar una fecha diferente de hoy, **el sistema deberá** rechazar la solicitud sin modificar los datos.

### RF-5 — Calcular la racha actual

- **Si** el hábito está hecho hoy, **el sistema deberá** mostrar la cantidad de fechas consecutivas con cumplimiento que terminan hoy.
- **Si** el hábito está pendiente hoy pero fue cumplido ayer, **el sistema deberá** conservar la cantidad de fechas consecutivas con cumplimiento que terminan ayer.
- **Si** el hábito no tiene cumplimientos o su último cumplimiento es anterior a ayer, **el sistema deberá** mostrar una racha de 0 días.
- **Cuando** se marque hoy un hábito cuya racha estaba rota, **el sistema deberá** mostrar una nueva racha de 1 día.

### RF-6 — Listar los hábitos

- **Cuando** el usuario solicite el listado, **el sistema deberá** mostrar todos los hábitos, cada uno con su nombre, racha actual en días y estado «Hecho hoy» o «Pendiente hoy».
- **El sistema deberá** presentar los hábitos en orden de creación.
- **Si** no existen hábitos, **el sistema deberá** informar de que todavía no hay hábitos y terminar con éxito.
- **Cuando** se consulte el listado, **el sistema deberá** conservar los datos sin modificaciones.

### RF-7 — Conservar los datos

- **Cuando** una creación o un marcado se confirme como exitoso, **el sistema deberá** conservar el resultado para ejecuciones posteriores.
- **Si** todavía no existen datos guardados, **el sistema deberá** permitir comenzar con una colección vacía.
- **Si** los datos existentes están dañados o no pueden leerse, **el sistema deberá** informar del problema y detener la operación sin sustituirlos ni tratarlos como una colección vacía.
- **Si** no puede guardarse una modificación, **el sistema deberá** informar del fallo, conservar los datos previamente guardados y evitar confirmar un éxito.
- **El sistema deberá** mantener la misma colección personal aunque cambie la carpeta desde la que se ejecuta una operación.
- **Si** existe un almacenamiento vacío sin una colección válida, **el sistema deberá** considerarlo dañado; únicamente la ausencia de almacenamiento o una colección vacía válida permiten empezar sin hábitos.
- **Si** los datos contienen nombres inválidos o equivalentes entre sí, fechas imposibles o futuras, cumplimientos repetidos o desordenados, información obligatoria ausente, datos de tipo incorrecto, elementos no admitidos o una versión no compatible, **el sistema deberá** rechazarlos íntegramente, sin corregirlos ni sobrescribirlos.
- **Cuando** el usuario liste sin datos previos o repita un marcado ya realizado hoy, **el sistema deberá** evitar crear o volver a guardar datos.
- **Si** la operación se interrumpe antes de que la nueva colección sustituya a la anterior, **el sistema deberá** conservar la colección anterior o su ausencia inicial.
- **Si** la operación se interrumpe después de esa sustitución y antes de confirmar el éxito, **el sistema deberá** conservar la nueva colección completa, sin revertirla ni recuperarla automáticamente.

### RF-8 — Comunicar errores de uso

- **Si** falta información obligatoria o se solicita una operación no admitida, **el sistema deberá** explicar el problema y orientar al usuario sobre el uso válido, sin modificar los datos.
- **Cuando** termine una operación, **el sistema deberá** permitir distinguir entre éxito y error mediante su estado de salida.
- **Cuando** se produzca un resultado exitoso, una consulta de ayuda, un listado vacío o un marcado repetido, **el sistema deberá** terminar con código 0 y presentar el resultado en la salida normal.
- **Si** se produce un error de nombre, de existencia o duplicidad de hábito, de validez de datos o de acceso a ellos, **el sistema deberá** terminar con código 1 y explicar el error en la salida de errores.
- **Si** la sintaxis contiene un comando ausente o desconocido, argumentos ausentes o adicionales u opciones no admitidas, **el sistema deberá** terminar con código 2, explicar que el comando o los argumentos no son válidos y mostrar el uso válido, sin acceder a los datos.
- **Cuando** el usuario solicite ayuda, **el sistema deberá** explicar en español el uso, los argumentos y ejemplos, sin acceder a los datos.
- **Si** concurren errores de distintas etapas, **el sistema deberá** comunicar el primero según este orden: sintaxis, validez del nombre, acceso y validez de datos, existencia o duplicidad del hábito y guardado.
- **Cuando** se comunique un error gestionado, **el sistema deberá** utilizar un mensaje en español iniciado con «Error:», sin trazas; los errores de acceso identificarán la ubicación afectada y orientarán sobre su revisión.

## Requisitos no funcionales

- **RNF-1 — Claridad:** la documentación, la ayuda y los mensajes al usuario estarán en español y explicarán las acciones y errores con lenguaje sencillo.
- **RNF-2 — Uso personal sin conexión:** las tres operaciones estarán disponibles sin acceso a Internet ni autenticación.
- **RNF-3 — Integridad:** un error no provocará pérdida, reinicio silencioso ni modificación parcial de los datos existentes.
- **RNF-4 — Verificabilidad:** cada requisito tendrá comprobaciones reproducibles; los escenarios de fechas podrán verificarse sin esperar al cambio real de día.
- **RNF-5 — Comprensión:** las reglas utilizarán términos consistentes y ejemplos comprensibles para un desarrollador junior.

## Casos límite

| Caso | Resultado esperado |
|---|---|
| Primera ejecución, sin hábitos | Listado vacío informado como éxito. |
| Hábito recién creado | Racha 0; pendiente hoy. |
| Crear `Leer` cuando existe ` leer ` | Error de nombre duplicado. |
| Marcar dos veces el mismo día | Segundo marcado exitoso con aviso; sin cambios. |
| Tres días consecutivos hasta ayer; hoy pendiente | Racha 3; pendiente hoy. |
| Marcar hoy después de esos tres días | Racha 4; hecho hoy. |
| Último cumplimiento anteayer | Racha 0; al marcar hoy pasa a 1. |
| Cumplimientos a ambos lados de medianoche | Cuentan como dos días si sus fechas son consecutivas. |
| Cambio de mes, año o febrero bisiesto | Se mantiene la continuidad entre fechas consecutivas. |
| Datos guardados dañados o inaccesibles | Error; los datos se conservan. |
| Nombre legible de más de 80 caracteres | Se admite si cumple las demás reglas. |
| Dos representaciones Unicode canónicamente equivalentes del mismo nombre | Se consideran el mismo hábito al crear y marcar. |
| Nombre con tabulación o salto de línea en un extremo | Error; no se crea ni marca ningún hábito. |
| Operación iniciada antes de medianoche y terminada después | Usa su fecha inicial; la siguiente operación usa la fecha nueva. |
| Dos fechas consecutivas separadas por un día de 23 o 25 horas | Cuentan como dos días de calendario consecutivos. |
| Con hoy como 2026-10-02, cumplimientos el 28, 29 de septiembre, 1 y 2 de octubre | Racha 2; el hueco del 30 de septiembre interrumpe la secuencia. |
| Hoy cumplido, ayer omitido y una racha antigua larga | Racha 1. |
| Marcar uno de varios hábitos | Los otros conservan sus cumplimientos y su orden. |
| Almacenamiento ausente frente a existente vacío e inválido | El primero permite empezar vacío; el segundo produce error. |
| Interrupción antes de sustituir los datos | Permanece la colección anterior o su ausencia inicial. |
| Interrupción después de sustituir los datos, antes de confirmar | Permanece la nueva colección completa, aunque no se haya recibido confirmación. |

## Fuera de alcance

- Renombrar, editar, eliminar o archivar hábitos.
- Deshacer cumplimientos o registrar días pasados o futuros.
- Consultar historial, racha máxima, estadísticas o clasificaciones.
- Configurar frecuencias semanales, descansos o días excluidos.
- Registrar duración, cantidad de sesiones o metas de estudio.
- Recordatorios, cuentas, colaboración, sincronización, importación y exportación.
- Recuperación automática de datos dañados.
- Tratamiento especial de cambios manuales del reloj o desplazamientos entre zonas horarias.
- Garantías de durabilidad absoluta frente a fallos físicos del dispositivo.

## Criterios de finalización

- La especificación está aprobada.
- Las tres operaciones cumplen todos los criterios de aceptación RF-1 a RF-8.
- Los casos límite tienen comprobaciones reproducibles y todas pasan.
- Se verifica la conservación de hábitos y cumplimientos entre ejecuciones.
- Los errores de uso y de acceso a datos preservan la información existente.
- La ayuda y los mensajes cumplen los requisitos de idioma y claridad.
- No se incorporan funcionalidades declaradas fuera de alcance.

## Dudas abiertas y supuestos

No quedan dudas funcionales bloqueantes identificadas tras las respuestas y las precisiones aprobadas del plan técnico. Toda nueva duda se registrará con la marca **[NECESITA ACLARACIÓN]**.

Decisiones aprobadas: listado en orden de creación, rechazo de nombres vacíos, conservación de la presentación del nombre y ausencia de creación automática al marcar un hábito inexistente. Se supone que la fecha y la zona horaria del equipo son correctas y que el uso es secuencial por una sola persona.
