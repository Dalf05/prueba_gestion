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
    
    # Si estamos arrancando el servidor, lanzamos las migraciones primero (solo una vez)
    if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
        print(">>> Sincronizando modelos y base de datos (una sola vez)...")
        try:
            execute_from_command_line([sys.argv[0], 'makemigrations', 'principal', '--noinput'])
            execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])
        except Exception as e:
            print(f">>> Error al migrar: {e}")
        
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
