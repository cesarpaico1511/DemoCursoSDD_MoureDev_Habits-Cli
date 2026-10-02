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

### RF-3 — Marcar un hábito como hecho

- **Cuando** el usuario marque un hábito existente que está pendiente hoy, **el sistema deberá** registrar su cumplimiento para hoy y confirmar la operación.
- **Si** el hábito ya está hecho hoy, **el sistema deberá** informar de ello y terminar con éxito, sin añadir otro cumplimiento ni modificar la racha.
- **Si** el hábito indicado no existe, **el sistema deberá** comunicar el error sin crearlo ni modificar otros hábitos.
- **El sistema deberá** admitir como máximo un cumplimiento por hábito y fecha.

### RF-4 — Determinar el día de cumplimiento

- **Cuando** se ejecute una operación, **el sistema deberá** tomar como «hoy» la fecha local del equipo al inicio de esa operación.
- **El sistema deberá** considerar días de calendario consecutivos, incluidos fines de semana y festivos.
- **Cuando** cambie la fecha a medianoche local, **el sistema deberá** considerar iniciado un nuevo día, aunque no hayan transcurrido 24 horas desde el último cumplimiento.
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

### RF-8 — Comunicar errores de uso

- **Si** falta información obligatoria o se solicita una operación no admitida, **el sistema deberá** explicar el problema y orientar al usuario sobre el uso válido, sin modificar los datos.
- **Cuando** termine una operación, **el sistema deberá** permitir distinguir entre éxito y error mediante su estado de salida.

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

## Fuera de alcance

- Renombrar, editar, eliminar o archivar hábitos.
- Deshacer cumplimientos o registrar días pasados o futuros.
- Consultar historial, racha máxima, estadísticas o clasificaciones.
- Configurar frecuencias semanales, descansos o días excluidos.
- Registrar duración, cantidad de sesiones o metas de estudio.
- Recordatorios, cuentas, colaboración, sincronización, importación y exportación.
- Recuperación automática de datos dañados.
- Tratamiento especial de cambios manuales del reloj o desplazamientos entre zonas horarias.

## Criterios de finalización

- La especificación está aprobada.
- Las tres operaciones cumplen todos los criterios de aceptación RF-1 a RF-8.
- Los casos límite tienen comprobaciones reproducibles y todas pasan.
- Se verifica la conservación de hábitos y cumplimientos entre ejecuciones.
- Los errores de uso y de acceso a datos preservan la información existente.
- La ayuda y los mensajes cumplen los requisitos de idioma y claridad.
- No se incorporan funcionalidades declaradas fuera de alcance.

## Dudas abiertas y supuestos

No quedan dudas funcionales bloqueantes identificadas tras las seis respuestas. Toda nueva duda se registrará con la marca **[NECESITA ACLARACIÓN]**.

Valores propuestos para aspectos no consultados expresamente: listado en orden de creación, rechazo de nombres vacíos, conservación de la presentación del nombre y ausencia de creación automática al marcar un hábito inexistente. Se supone que la fecha y la zona horaria del equipo son correctas y que el uso es secuencial por una sola persona.
