# Proyecto Final UNIE - Gestion de Incidencias

Hola! Este es mi proyecto para la UNI. Es una web para gestionar las quejas y cosas que se rompen en el campus.

## Como hacerlo funcionar (IMPORTANTE)

Para que funcione bien en tu ordenador, sigue estos pasos (ayer me dio guerra la base de datos):

1. **Librerias:**
   Instala lo que he puesto en el `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

2. **La base de datos (Si te da error de 'no such table' o 'InconsistentMigrationHistory'):**
   Si has cambiado carpetas de sitio como yo, a veces Django se ralla. Lo mejor es:
   - Borrar el archivo `db.sqlite3` si ya existe.
   - Ejecutar esto para crear las carpetas de migraciones si no estan: `python manage.py makemigrations principal`
   - Y luego lanzar las tablas: `python manage.py migrate`
   
   *Si te sale error de que no encuentra la tabla `principal_user`, es que te has saltado el migrate.*

3. **Crear tu usuario:**
   Como no hay registro publico (por seguridad), create un admin a mano:
   ```bash
   python manage.py createsuperuser
   ```
   *Luego entra en /admin y cambiate el rol a ADMIN en tu perfil, si no verás las gráficas vacías.*

4. **Ejecutar:**
   Para ver la web en local:
   ```bash
   python manage.py runserver
   ```
   **IMPORTANTE:** Si te sale un error de **'WinError 1450: Recursos insuficientes'**, es porque Windows se agobia vigilando tantos archivos. Ejecútalo así para que funcione:
   ```bash
   python manage.py runserver --noreload
   ```
   Y entras en `http://127.0.0.1:8000/`.

Luego entras en `http://127.0.0.1:8000/` y ya está.

## Cosas que tiene la web:
- Dashboard con graficos de D3 (me costó un poco pillarlo).
- Roles: Alumno, Profe, Tecnico y Admin.
- Registro de quejas/incidencias segun donde pase.
- Color azul de la UNIE.
