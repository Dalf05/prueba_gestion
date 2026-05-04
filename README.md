# Proyecto Final UNIE - Gestion de Incidencias

Hola! Este es mi proyecto para la UNI. Es una web para gestionar las quejas y cosas que se rompen en el campus.

## Como hacerlo funcionar (IMPORTANTE)

Para que funcione bien en tu ordenador:

1. **Librerias:**
   Instala lo que he puesto en el requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

2. **La base de datos (Si te da error de 'no such table' mira aqui):**
   Tienes que crear las tablas, yo he usado sqlite para no liarme con servidores:
   ```bash
   python manage.py makemigrations principal
   python manage.py migrate
   ```
   *Si te sale error de que no encuentra la tabla `principal_user`, es que te has saltado este paso.*

3. **Crear tu usuario:**
   Como no hay registro publico, create un admin:
   ```bash
   python manage.py createsuperuser
   ```
   *Luego entra en /admin y cambiate el rol a ADMIN en tu perfil, que si no no ves las graficas.*

4. **Ejecutar:**
   ```bash
   python manage.py runserver
   ```

Luego entras en `http://127.0.0.1:8000/` y ya está.

## Cosas que tiene la web:
- Dashboard con graficos de D3 (me costó un poco pillarlo).
- Roles: Alumno, Profe, Tecnico y Admin.
- Registro de quejas/incidencias segun donde pase.
- Color azul de la UNIE.
