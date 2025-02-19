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

    # Obtiene la ruta absoluta del directorio donde está este script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    #Extraccion

    script = os.path.join(base_dir, "extraccion", "scraper_peleadores_ufc.py")
    ejecutar_script(script)

    script = os.path.join(base_dir, "extraccion", "WebScrapCombates.py")
    ejecutar_script(script)

    script = os.path.join(base_dir, "extraccion", "scraper_tapology_bf.py")
    ejecutar_script(script)

    #Transformacion
    script = os.path.join(base_dir, "transformacion", "tratamiento_peleas.py")

    ejecutar_script(script)
    script = os.path.join(base_dir, "transformacion", "tratamiento_peleadores.py")
    
    #Analisis
    ejecutar_script(script)
    script = os.path.join(base_dir, "analisis", "ranking_v2.py")
    
    #Prediccion...


if __name__ == "__main__":
    ejecutar()

