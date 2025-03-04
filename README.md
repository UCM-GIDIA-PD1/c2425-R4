# c2425-P4


# Funcionamiento mains:
  - Main src ejecuta tanto el código de extracción como de transformación, no neceista parámetros
  - Main extracción, ejecución por defecto todas las páginas de las webs, se puede escribir por teclado "peleas", "peleador" y "fechas" para ejecutar solo uno, también se puede poner como argumento las páginas que extrae cada   uno.
  - Main transformación, ejecución por defecto obteniendo los datos de data/raw pero se puede pasar como argumento una dirección en caso de que se quiera obtener los dataframes de otro lugar.
# Problema con parquet:
  - No nos deja leer de parquet sin instalar pyarrow, la cual no funciona bien descargandose en requirements.txt, por lo que hay que instalarlo manualmente.
# Carpeta data en drive: 
- https://drive.google.com/drive/folders/1jX3HSEBXGX7HC6WhPOpthBHoO4UmwI8O?usp=drive_link
