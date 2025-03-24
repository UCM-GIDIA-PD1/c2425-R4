 # c2425-P4



# Funcionamiento mains:
  - Main src ejecuta tanto el código de extracción como de transformación, no necesita parámetros
  - Main extracción, ejecución por defecto todas las páginas de las webs, se puede escribir por teclado "peleas", "peleador" y "fechas" para ejecutar solo uno, también se puede poner como argumento las páginas que extrae cada   uno.
  - Main transformación, ejecución por defecto obteniendo los datos de data/raw pero se puede pasar como argumento una dirección en caso de que se quiera obtener los dataframes de otro lugar.
# Carpeta data en drive: 
- https://drive.google.com/drive/folders/1jX3HSEBXGX7HC6WhPOpthBHoO4UmwI8O?usp=drive_link

# El miércoles empezamos a usar uv para gestionar los entornos virtuales, es bastante fácil.
- Este video me he visto yo y se entiende todo bien: https://www.youtube.com/watch?v=zgSQr0d5EVg&ab_channel=MattPalmer
- Guia para usarlo en notebooks que igual no queda claro en el vídeo.
- Creas el entorno virtual, pones ese comando y ya debería funcionar los notebooks.
![image](https://github.com/user-attachments/assets/113b576e-d139-4682-9f43-ccf04eacf940)
- Guía oficial sobre uso de notebooks con uv: https://docs.astral.sh/uv/guides/integration/jupyter/


# **Objetivo**
Hay dos propuestas:
## **P1:** Ganador combate:
Este modelo consiste en predecir el ganador de una pelea a partir de los datos de ese combate. Su función es similar a la que tendría un juez de la UFC.
Dataframe: carpeta drive: P1
Se debe predecir la variable winner.  
Modelos propuestos:
- Regresión logística
- Random Forest
- XGBoost

## **P2:** Predice ganador entre dos peleadores:
Este modelo predice el ganador de un combate que no se ha dado entre dos peleadores. 
Dataframe: carpeta drive: P2
Se predice la variable winner, y la probabilidad de victoria para cada peleador.  
Modelos propuestos:
- Regresión logística
- Random Forest
- XGBoost

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
Cada tarea añadida al backlog debe estar rellanada con todas las característica: tamaño, iteracion, etc.  
Cada integrante del grupo debe asignarse la tarea en la que está trabajando, y posicionarla en el lugar adecuado: todo, in progress, review.
Las tareas pasarán a "done" si son revisadas unicamente por el encargado de ello.

### **2.2 Revisar todo el codigo subido**
Asignar a un integrante del grupo encargado de revisar todo el código que se sube funcione correctamente.
### **2.3 Mayor documentación del código**
## Guía de Documentación del Código

Todo el código debe estar correctamente documentado siguiendo estas instrucciones:

### Documentación por archivo  
Cada archivo debe incluir al inicio los siguientes elementos:

- **Tarea del backlog:** Enlace a la tarea que este código resuelve.
- **Propósito del código:** Breve descripción de la función principal del archivo.  
- **Autor(es):** Nombre(s) de quienes han trabajado en el código.  
- **Descripción y uso:** Explicar de manera concisa cómo funciona el código y cómo debe utilizarse.
- **Estado actual:** Explicar como esta el código en este momento(finalizado, en proceso, etc) indicando que estás haciendo y que falta para terminarlo.

En caso de modificar el código, se debe añadir:
- **Autor:** Modificación realizada.  

⏳ **Tiempo aproximado:** 5 minutos.

Ejemplo:  
![image](https://github.com/user-attachments/assets/ec452b8e-aada-49be-b3e3-661acb170ce1)

### Comentarios dentro del código  
- Agregar comentarios en aquellas partes que puedan generar dudas sobre el funcionamiento o la lógica aplicada.  
- Explicar claramente fragmentos de código complejos o poco intuitivos.  

⏳ **Tiempo aproximado:** 10 minutos.

## Revisión antes de hacer push  
Antes de hacer un `push` de uno o varios archivos, se debe revisar que el archivo cumpla con las reglas anteriores.

### **2.4 Memoria y presentación**
La memoria y la presentación deben estar terminadas para la clase anterior a la entrega. Para este sprint el 31/3/2025.  

## **3️⃣ Comentarios y sugerencias**  
Cualquier mejora adicional que se considere necesaria para el próximo Sprint podéis escribirla. Si alguien no está de acuerdo con algún punto de este documento o tiene problemas con alguna de las instrucciones, es importante comunicarlo para buscar una solución en conjunto.  

# UFC PREDICTOR

### Proyecto Datos I

### 1. Descripción del proyecto

El objetivo de este proyecto es desarrollar dos sistemas de aprendizaje automático. Uno predice el ganador de un combate de la UFC basándose en datos de la pelea. El segundo predice el ganador usando información previa al combate. Para ello utilizamos información sobre peleas previas y peleadores. Esta información se obtiene de la página oficial de la UFC y UFC Stats que tiene todos los combates históricos.

### 2. Integrantes 
 -  Andrés Fernández Ortega
 -  Francisco José Pastor Ruiz
 -  Mario Granados Guerruero
 -  Telmo Aracama Docampo
 -  Carlos Vallejo Ros

### 3. Instrucciones de instalación


### 4. Fuentes de datos

- (UFC Stats) [http://ufcstats.com/statistics/events/completed]

Para extraer todas las peleas con su información respectiva, golpes por peleador, porcentajes de knockdowns etc.

- (UFC) [https://www.ufc.com/athletes/all]

Para extraer información de los luchadores y sus fotos, las cuales usaremos para crear la web.

- [Tapology](https://www.tapology.com/)

La usamos como fuente secundaria para obtener la edad del luchador, entre otras características.

### 5. Estructura del código


### 6. Resultados y evaluación


### 7. Trabajo futuro


