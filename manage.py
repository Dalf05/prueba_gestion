#!/usr/bin/env python
import os
import sys

def main():
    """Para arrancar el servidor y las migraciones."""
    # Aqui le digo donde estan los ajustes de mi proyecto
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No he podido importar Django. Asegurate de tenerlo instalado "
            "en tu entorno virtual o mira el requirements.txt."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
