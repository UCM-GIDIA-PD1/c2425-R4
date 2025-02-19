import os
import subprocess

def ejecutar_script(script):
    """Ejecuta un script específico en la ruta indicada."""

    if os.path.isfile(script):  # Verifica si el archivo existe antes de ejecutarlo
        print(f"Ejecutando {script}...")
        subprocess.run(["python", script])
    else:
        print(f"Error: No se encontró el archivo '{script}'")

def ejecutar():
    """Ejecuta todos los archivos .py en la ruta especificada."""
    
    print('..')  
    # Obtiene la ruta absoluta del directorio donde está este script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construye la ruta del script dinámicamente
    script = os.path.join(base_dir, "extraccion", "scraper_peleadores_ufc.py")
    
    ejecutar_script(script)

if __name__ == "__main__":
    print('.')
    ejecutar()

