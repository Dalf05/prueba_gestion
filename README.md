# Proyecto UNIE - Gestión de Incidencias

Este es mi proyecto para la gestión de incidencias de la universidad. Lo he hecho con Django porque es bastante rápido para estas cosas.

## Como hacerlo funcionar

1. **Instalar las librerias:**
   Tienes que instalar lo que hay en el requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

2. **La base de datos:**
   Hay que crear las tablas de la base de datos (he usado sqlite):
   ```bash
   python manage.py makemigrations principal
   python manage.py migrate
   ```

3. **Crear el admin:**
   Para poder entrar la primera vez necesitas un superusuario:
   ```bash
   python manage.py createsuperuser
   ```
   *Nota: Acuérdate de entrar en /admin y ponerte el rol de ADMIN en tu usuario, si no no verás el panel.*

4. **Arrancar:**
   Para ver la web:
   ```bash
   python manage.py runserver
   ```

Luego entras en `http://127.0.0.1:8000/` y ya está.

## Cosas que tiene la web:
- Dashboard con graficos de D3 (me costó un poco pillarlo).
- Roles: Alumno, Profe, Tecnico y Admin.
- Registro de quejas/incidencias segun donde pase.
- Color azul de la UNIE.
