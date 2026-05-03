# PROYECTO FINAL: Sistema de Gestión de Incidencias UNIE

¡Hola! Este es el código de mi proyecto para la universidad. Es un sistema para que los alumnos y profes puedan reportar cosas que se rompen en el campus (como una bombilla fundida o que no funciona el WiFi) y que los del equipo técnico lo puedan arreglar.

He intentado que sea limpio y fácil de usar, usando **Django** para toda la parte de atrás (servidor/base de datos) y **Tailwind CSS** para que la web se vea moderna.

---

## 📂 ¿Cómo está organizado el código? (Estructura)

He repartido los archivos de forma que cada cosa tenga su sitio, como nos enseñaron en clase:

*   **/proyecto/**: Aquí están los "ajustes maestros" de la web.
    *   `settings.py`: Donde configuro la base de datos (SQLite), las apps que uso y los permisos.
    *   `urls.py`: El mapa principal de rutas de la web.
*   **/gestion/**: Esta es la carpeta más importante. Es donde está toda la "chicha" de la aplicación.
    *   `models.py`: Aquí diseño las tablas de la base de datos (Usuario, Incidencia, Comentario).
    *   `views.py`: Aquí está la lógica. Lo que pasa cuando clicas un botón o envías un formulario.
    *   `urls.py`: Las rutas específicas de las páginas de gestión.
    *   **/templates/**: Todos los archivos HTML de la web.
    *   **/migrations/**: Archivos que Django crea automáticamente para montar la base de datos.
*   **/static/**: Para guardar fotos o logos (aunque la mayoría de iconos los cargo por enlace).
*   `manage.py`: El mando a distancia para arrancar el servidor o crear tablas.
*   `requirements.txt`: La lista de librerías de Python necesarias para que esto arranque.

---

## 🛠️ ¿Cómo se usa esto? (Instalación)

Si te has bajado el código y quieres probarlo en tu ordenador:

1.  **Instala las librerías:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Crea la base de datos:**
    ```bash
    python manage.py migrate
    ```

3.  **Lanza el servidor:**
    ```bash
    python manage.py runserver
    ```
    Y luego entras en `http://127.0.0.1:8000`

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
