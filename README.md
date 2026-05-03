# 🎓 PROYECTO: Sistema de Gestión de Campus - UNIE

¡Hola! Este es el código de mi proyecto de fin de curso. Es una aplicación web completa para gestionar las incidencias y averías dentro del campus de la Universidad UNIE. 

La idea es que cualquier persona (alumnos, profes, técnicos) pueda avisar si algo va mal y que se gestione de forma ordenada.

---

## 🏗️ Estructura del Proyecto (Qué es cada cosa)

He organizado el código siguiendo el patrón **MTV (Modelo-Template-Vista)** de Django para que sea fácil seguir el rastro de la información:

### 1. 📂 `proyecto/` (Configuración Maestra)
Esta carpeta es el cerebro administrativo. Aquí no hay lógica del programa, sino los ajustes de Django.
*   `settings.py`: Aquí configuro el idioma (Español), la zona horaria (Madrid), y le digo a la web que use la base de datos `db.sqlite3`. También defino que el usuario de la web tiene "roles" (Admin, Alumno, etc.).
*   `urls.py`: Es el portero de la web. Cuando alguien entra en una dirección, este archivo decide a qué parte de la aplicación enviarlo.

### 2. 📂 `gestion/` (La Aplicación en sí)
Aquí es donde he programado toda la funcionalidad.
*   `models.py`: Aquí diseño "las tablas". Definí tres modelos: `User` (con roles), `Incidencia` (donde guardamos los reportes) y `Comentario` (por si queremos añadir chats más adelante).
*   `views.py`: ¡Aquí está la magia! He creado funciones que:
    *   `dashboard`: Calcula las estadísticas para que los gráficos funcionen (usa lógica de tiempos de resolución).
    *   `analizar_urgencia`: Un pequeño algoritmo que lee el título del reporte y decide si es "Urgente" basándose en palabras clave.
    *   `incidents_list`: Decide qué incidencias puedes ver. Por ejemplo, un alumno solo ve reportes que le competen (limpieza, cafetería), mientras que un técnico lo ve todo.
*   `urls.py`: Aquí están las direcciones de la app (`/incidencias/`, `/nueva/`, `/configuracion/`).
*   `templates/`: Son los archivos HTML. He usado **Django Templates** para meter lógica dentro del HTML (bucles, condiciones).

### 3. 📂 `static/`
Aquí se guardan los archivos que no cambian, como el logo de la universidad o archivos CSS personalizados.

---

## ⚡ Funcionalidades Principales

1.  **Panel de Control Inteligente:** El dashboard muestra gráficas en tiempo real de cuántas incidencias están abiertas o resueltas. Las gráficas se dibujan usando la librería **D3.js**.
2.  **Sistema de Roles:**
    *   **Administrador:** Puede gestionar usuarios y ver todos los datos.
    *   **Técnico:** Solo ve la lista de tareas pendientes para ir a arreglarlas.
    *   **Docente/Alumno:** Pueden crear reportes nuevos.
3.  **Filtrado por Categoría:** Si reportas algo de "Informática", le llega al equipo de TI. Si es una "Bombilla", va a Mantenimiento.
4.  **Cálculo de SLA:** El sistema calcula automáticamente el "tiempo medio de arreglo" para que el jefe sepa si el equipo está trabajando rápido.

---

## 🚀 Cómo ponerlo en marcha

Para que el proyecto funcione al 100%, solo necesitas Python instalado:

1.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Lanzar la base de datos:**
    ```bash
    python manage.py migrate
    ```

3.  **Ejecutar el servidor de pruebas:**
    ```bash
    python manage.py runserver
    ```

¡Espero que esto te sirva como documentación para el proyecto!

