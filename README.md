# c2425-P4


# Funcionamiento mains:
  - Main src ejecuta tanto el código de extracción como de transformación, no neceista parámetros
  - Main extracción, ejecución por defecto todas las páginas de las webs, se puede escribir por teclado "peleas", "peleador" y "fechas" para ejecutar solo uno, también se puede poner como argumento las páginas que extrae cada   uno.
  - Main transformación, ejecución por defecto obteniendo los datos de data/raw pero se puede pasar como argumento una dirección en caso de que se quiera obtener los dataframes de otro lugar.
# requirements.txt:
  - PyArrow da un error desconocido al descargarlo por lo tanto lo hemos comentado para que se puedan descargar las bibliotecas correctamente. (Quizás por la versión de Python)
