# UNIE Universidad - Portal de Gestión (Django Version)

Esta es la versión completa en Django y Python del portal de gestión de incidencias, diseñada para ser idéntica en funcionalidad y estética a la versión de React.

## Requisitos Previos

- Python 3.8 o superior instalado.
- Pip (gestor de paquetes de Python).

## Pasos para la Instalación Local

1. **Instalar Dependencias:**
   Abre una terminal en la carpeta raíz del proyecto y ejecuta:
   ```bash
   pip install -r requirements.txt
   ```

2. **Preparar la Base de Datos:**
   Ejecuta las migraciones para crear las tablas necesarias:
   ```bash
   python manage.py makemigrations gestion
   python manage.py migrate
   ```

3. **Crear Usuario Administrador:**
   Para poder acceder al portal, necesitas una cuenta. Crea un superusuario ejecutando:
   ```bash
   python manage.py createsuperuser
   ```
   *Nota: Sigue las instrucciones en pantalla. Una vez creado, entra en el panel de administración (`/admin`) para asignarte el rol de 'ADMIN' en tu perfil de usuario, ya que por defecto Django no asigna el rol personalizado.*

4. **Iniciar el Servidor:**
   Lanza el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

5. **Acceder a la Aplicación:**
   Abre tu navegador en: `http://127.0.0.1:8000/`

## Características Implementadas

- **Interfaz Corporativa:** Diseño basado en Tailwind CSS con los colores y tipografía de UNIE.
- **Sistema de Roles:** Lógica diferenciada para Alumnos, Docentes, Técnicos y Administradores.
- **Dashboard con KPIs:** Visualización de estadísticas en tiempo real.
- **Gestión de Incidencias:** Listado maestro y formulario de creación con análisis de prioridad.
- **Pestaña de Configuración:** Panel exclusivo para administradores (Gestión de usuarios y campus).
- **Imágenes Reales:** Integración con Unsplash para una estética profesional.
