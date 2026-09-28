# Constitución del proyecto
CLI educativa de hábitos de estudio, mantenible por un desarrollador junior.

1. **Stack simple:** Python 3 y biblioteca estándar; `argparse` para la CLI y cero dependencias externas.
2. **Spec primero:** todo cambio de comportamiento requiere una especificación aprobada con criterios de aceptación antes de escribir código.
3. **Separación:** la lógica de hábitos y rachas usa funciones sin entrada/salida; la CLI y la persistencia viven en módulos separados.
4. **Tests:** usar `unittest` para reglas, errores y límites de fechas; cada bug corregido añade una prueba de regresión; todas deben pasar.
5. **Persistencia:** guardar en JSON local UTF-8, validar al cargar y escribir mediante reemplazo atómico; nunca sobrescribir datos corruptos.
6. **Idioma:** identificadores, comandos, comentarios y docstrings en inglés; documentación, ayuda y mensajes al usuario en español.
