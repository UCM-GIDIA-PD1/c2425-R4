# c2425-P4


# Funcionamiento mains:
  - Main src ejecuta tanto el código de extracción como de transformación, no necesita parámetros
  - Main extracción, ejecución por defecto todas las páginas de las webs, se puede escribir por teclado "peleas", "peleador" y "fechas" para ejecutar solo uno, también se puede poner como argumento las páginas que extrae cada   uno.
  - Main transformación, ejecución por defecto obteniendo los datos de data/raw pero se puede pasar como argumento una dirección en caso de que se quiera obtener los dataframes de otro lugar.
# Problema con parquet(Corregido creo si os da problemas avisarme):
  - No nos deja leer de parquet sin instalar pyarrow, la cual no funciona bien descargándose con requirements.txt, por lo que hay que instalarlo manualmente. 
# Carpeta data en drive: 
- https://drive.google.com/drive/folders/1jX3HSEBXGX7HC6WhPOpthBHoO4UmwI8O?usp=drive_link


# **Mejoras para Sprint 3 / Entregable 3**  

## **1️⃣ Uso obligatorio**  

Para garantizar la correcta ejecución del proyecto y evitar errores relacionados con datos desactualizados o configuraciones inconsistentes, es imprescindible seguir estas normas:  

### **1.1 Uso de la carpeta "data" en Drive**  
Todos los datos deben almacenarse y utilizarse desde la carpeta **data** en Drive. Si cada persona usa archivos locales, puede generar inconsistencias y errores cuando el código se ejecute con versiones actualizadas del **dataframe**.  

### **1.2 Mantener los datos actualizados**  
Los archivos de la carpeta **data** se actualizarán periódicamente. No obstante, en caso de necesitar la última versión, puedes generarla ejecutando el script de transformación siguiendo estos pasos:  

#### **Guía para ejecutar el script de transformación**  

1. Asegúrate de que los datos extraídos mediante **web scraping** están almacenados en:  
   ```
   data/raw
   ```
2. Abre la terminal del sistema operativo o la integrada en **Visual Studio Code** y navega hasta la carpeta donde se encuentra el script `main.py`.  
   Si el script está en `src/transformacion`, usa el siguiente comando:  
   ```sh
   cd src/transformacion
   ```
3. Verifica que estás en el directorio correcto. La terminal debería mostrar algo como:  
   ```
   .../c2425-R4/src/transformacion >
   ```
4. Ejecuta el script con el siguiente comando:  
   ```sh
   python main.py
   ```
   Esto aplicará las transformaciones necesarias y generará los archivos actualizados en **formato Parquet**.  

### **1.3 Mantener actualizado el archivo "requirements.txt"**  
Es obligatorio el uso de entornos virtuales y del archivo **requirements.txt** para asegurar que cualquier persona pueda ejecutar el proyecto sin errores.  

- Cada vez que se instale una nueva biblioteca, es necesario registrarla en **requirements.txt** con su versión específica.  
- Si hay dudas sobre cómo utilizar entornos virtuales, se puede consultar la presentación disponible en el **Campus** o preguntar al equipo.  

## **2️⃣ Mejoras a implementar**  

### **2.1 Uso del tablero de tareas**  
Durante el último Sprint, el uso del **tablero de tareas** ha disminuido. Es fundamental mantenerlo actualizado y seguir un orden de trabajo estructurado para mejorar la organización del equipo. 
### **2.2 Revisar todo el codigo subido**
Asignar a un integrante del grupo encargado de revisar todo el código que se sube funcione correctamente.
### **2.3 Mayor documentación del código**
Todo el código debe estar correctamente documentado:  
Para cada archivo:  
- Tarea del backlog que resuelve
- Descripción breve del propósito del archivo
- Autor(es)


## **3️⃣ Comentarios y sugerencias**  
Cualquier mejora adicional que se considere necesaria para el próximo Sprint podéis escribirla. Si alguien no está de acuerdo con algún punto de este documento o tiene problemas con alguna de las instrucciones, es importante comunicarlo para buscar una solución en conjunto.  
