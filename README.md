# PROYECTO FINAL: Sistema de Gestión de Incidencias UNIE

¡Hola! Este es el código de mi proyecto para la universidad. Es un sistema para que los alumnos y profes puedan reportar cosas que se rompen en el campus (como una bombilla fundida o que no funciona el WiFi) y que los del equipo técnico lo puedan arreglar.

He intentado que sea limpio y fácil de usar, usando **Django** para toda la parte de atrás (servidor/base de datos) y **Tailwind CSS** para que la web se vea moderna. He borrado todos los archivos temporales y configuraciones raras que crea la IA por defecto (como los de JavaScript) para que el proyecto sea 100% Python puro, como si lo hubiera hecho yo en mi portátil.

---

## 📂 ¿Cómo está organizado el código? (Estructura detallada)

Para que no te pierdas, aquí te explico para qué sirve cada carpeta:

1.  **/proyecto/**: Es el "corazón" de la aplicación.
    *   `settings.py`: Aquí es donde le digo a Django que use la base de datos `db.sqlite3`. También he configurado los `MESSAGES` para que salgan los avisos de "Incidencia guardada" y he puesto los nombres de los usuarios de prueba.
    *   `urls.py`: Este archivo reparte el tráfico. Si entras en la web vacía, te manda a las URLs de la carpeta `gestion`.
    *   `wsgi.py` / `asgi.py`: Son archivos estándar de Django para que el servidor pueda arrancar. No hay que tocarlos casi nunca.

2.  **/gestion/**: Es la "app" donde ocurre todo el negocio.
    *   `models.py`: Aquí definí la clase `Incidencia`. Tiene campos para el título, la descripción, la prioridad (que se calcula sola) y la categoría (TI, Limpieza, etc.). También hay una relación `ForeignKey` con el usuario para saber quién subió cada cosa.
    *   `views.py`: ¡El cerebro! Aquí he programado funciones como `dashboard` (que saca las estadísticas de las gráficas) o `incidents_list` (que filtra quién puede ver qué). Por ejemplo, un profe no ve lo mismo que un alumno.
    *   `urls.py`: Aquí están las direcciones de "nueva incidencia", "lista", etc.
    *   **/templates/**: Son los archivos HTML. He usado una "base.html" para no repetir el código del menú lateral en todas las páginas. Uso etiquetas de Django como `{% if %}` y `{% for %}` para pintar los datos de la base de datos.
    *   **/migrations/**: Aquí Django guarda los cambios que hago en las tablas. He dejado las migraciones limpias para que al hacer `migrate` se cree todo perfecto.

3.  **/static/**: Aquí irían los logos de la uni, pero de momento los iconos los saco de una librería que se llama Lucide mediante un script en el HTML para que carguen rápido.

---

## 🛠️ ¿Cómo funciona por dentro? (Flujo de datos)

Cuando un usuario entra a reportar algo:
1.  Rellena el formulario en `create_incident.html`.
2.  Al darle a enviar, el servidor recibe los datos en `views.py`.
3.  **Análisis automático:** Antes de guardar, paso el texto por una función que busca palabras clave (si pones "fuego" le pone prioridad Crítica del tirón).
4.  Se guarda en el archivo `db.sqlite3`.
5.  El usuario es redirigido a la lista, donde sale un mensaje verde confirmando que todo está OK.

---

## 👥 Usuarios que he creado para probar:

He metido unos usuarios por defecto para que no tengas que registrarte:

*   **Administrador (Jefe):** user `admin` / pass `admin123`
*   **Técnico (Mantenimiento):** user `tecnico` / pass `tecnico123`
*   **Profesor (Docente):** user `docente` / pass `docente123`
*   **Estudiante (Alumno):** user `alumno` / pass `alumno123`

---

## 🧪 Cosas chulas que hace el código:

1.  **Filtro inteligente de prioridad:** Cuando escribes una incidencia, el sistema busca palabras como "peligro" o "roto" y le pone prioridad alta automáticamente. Está en `views.py` bajo la función `analizar_urgencia`.
2.  **Panel de Control (Dashboard):** He metido gráficas con **D3.js** que se dibujan según los datos reales de la base de datos (nada de datos falsos).
3.  **Roles de usuario:** Un alumno no puede ver las gráficas de gestión ni cambiar el estado de incidencias ajenas, solo puede reportar sus propios problemas.
4.  **Diseño Adaptable:** Funciona bien en el móvil por si el técnico tiene que ir por los pasillos con el teléfono revisando los fallos.

Espero que te guste el código, ¡ha llevado su tiempo! :)
