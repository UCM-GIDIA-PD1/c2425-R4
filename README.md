 # UFC Predictor: Sistema de predicción para la UFC

### Proyecto Datos I

### 1. Descripción de los objetivos

El objetivo de este proyecto es desarrollar dos sistemas de aprendizaje automático. Uno predice el ganador de un combate de la UFC basándose en datos de la pelea para conocer cual es el ganador justo o como una herramienta que puedan usar jueces de la UFC. 

El segundo predice el ganador usando información previa al combate. Este modelo puede ser usado por fans del deporte para conocer cuales son las probabilidades de victoria de cada peleador o en el mundo de las apuestas deportivas. Para ello utilizamos información sobre peleas previas de cada peleador realizando medias ponderadas. Esta información se obtiene de la página oficial de la UFC y UFC Stats que tiene todos los combates históricos.

De forma interna referenciamos el primer modelo mencionado como P2 y el segundo como P1, no es necesario saberlo pero quizás facilita el entendimiento del repositorio y las carpetas.

### 2. Estructura del repositorio

- La carpeta data incluye un .txt con un link a Google Drive para descargarse la carpeta de data con los parquets procesados y los csv extraídos. Los archivos de esta carpeta se deben copiar dentro de la carpeta data ya creada.
- La carpeta mlruns incluye los diferentes experimentos realizados con diferentes modelos e hiperparámetros.
- La carpeta src contiene todo el código. En esta carpeta encontramos diferentes carpetas con los módulos y procesos utilizados para realizar el proyecto.
   * Extracción:
      - `scraper_peleas.py`: Extrae información de todos los combates por evento de la UFC de forma cronológica, registramos el ganador, diferentes métricas de cada pelea y los peleadores que pelean en ella. Para obtener la
        información realizamos web-scraping de [UFC Stats](http://ufcstats.com/statistics/events/completed)
      - `scraper_peleadores.py`: Realiza web-scraping de información de peleadores y sus imágenes las cuales usaremos en la página web. La información se extrae de [UFC](https://www.ufc.com/athletes/all)
      - `scraper_fecha_nacimiento.py`: Utilizado para extraer las fechas de naciemientos de los peleadores realizando web-scraping de una fuente de datos secundaria llamada [Tapology](https://www.tapology.com/).
   * Transformación:
      - `tratamiento_peleas.py`: Contiene una función que realiza una limpieza de las variables extraídas para que sean más fáciles de utilizar. Creamos algunas nuevas variables para que sean más útiles para los modelos.
      - `tratamiento_peleadores.py`: Realiza la limpieza del dataset de peleadores para que las variables sean más usables.
      - `recordPeleas.py`: Calcula los records de cada peleador en el momento de las peleas. Es decir basándose en el record actual de un peleador, el cual hemos guardado en el dataset de peleadores, vamos calculando el    record de cada peleador teniendo en cuenta si han perdido o ganado combates.
      - `nuevas_columnas_peleas_peleadores.py`: Este código contiene una función que crea nuevas variables algo más complejas basándose tanto en las peleas de cada luchador como en su perfil de peleador. En este código se crean variables como un sistema de Puntos o las victorias o derrotas por cada método.
      - `peleasMediasPond.py`: Para cada pelea en el DataFrame de peleas sustituimos los datos reales de la pelea por las medias ponderadas de los últimos tres combates de cada peleador. En este caso las peleas cuyos peleadores no tengan más de tres combates son eliminados. Con esta función creamos el DataFrame que usaremos en el modelo de predicción de peleas futuras.
      - `dfDif.py`: Crea un DataFrame con las variables como diferencias entre peleadores. Este DataFrame se crea a partir del DataFrame de medias ponderadas.
   * Análisis:

        Para realizar análisis lo separamos en cuatro notebooks diferentes. En `analisis_peleas.ipynb` y `analisis_peleadores.ipynb` realizamos una exploración inicial de el dataset de peleas y peleadores con visualizaciones. También realizamos el notebook `analisis_peleas_ponderadas.ipynb`, este notebook lo usamos para ver las distribuciones de las variables en el dataset creado en el script de transformaciones con medias ponderadas. También estudiamos la correlación de las variables con la variable respuesta. Por último, también realizamos `analisis_relaciones_variables_peleas.ipynb` en el cual estudiamos la relación de diferentes variables y sus correlaciones con las variables respuesta.
   * Models:

        Para realizar los diferentes modelos organizamos la carpeta model en tres carpetas. Una para los modelos de P1 otra para los modelos de P2 y otra para los modelos de P2 con las variables como diferencias entre los peleadores. En cada uno de estas carpetas encontramos los modelos de `XGBoost`, `LogisticRegression` y `TreeClassifier` para cada modelo. En el caso de los modelos usando diferencias no usamos árboles de decisión ya que estos los usamos para realizar un análisis exploratorio. En esta carpeta también encontramos los notebooks para realizar las particiones de datos, respetando la secuencia temporal en caso de que sea necesario.
   * Evaluación:

### 3. Como iniciar el entorno de desarrollo y sus dependencias

Para este proyecto hemos utilizado el gestor de entornos y dependencias [uv](https://github.com/astral-sh/uv), que simplifica considerablemente la configuración del entorno de desarrollo.

Pasos para comenzar:
Clona este repositorio:

```
git clone https://github.com/UCM-GIDIA-PD1/c2425-R4.git
cd c2425-R4
```
Instala las dependencias con el siguiente comando:

```
uv sync
```
Esto creará automáticamente un entorno virtual y descargará todas las dependencias especificadas.

Ejecuta scripts dentro del entorno con:

```
uv run script.py
```
Esto garantiza que el script se ejecute con la versión correcta de Python y todas las dependencias necesarias, sin necesidad de activarlo manualmente.

💡 Nota: Asegúrate de tener uv instalado antes de ejecutar estos comandos. Puedes encontrar instrucciones de instalación en el repositorio oficial de uv.



### . Resultados y evaluación


### . Integrantes 
 -  Andrés Fernández Ortega
 -  Francisco José Pastor Ruiz
 -  Mario Granados Guerrero
 -  Telmo Aracama Docampo
 -  Carlos Vallejo Ros
 -  Mateo Turati Domínguez

# Funcionamiento mains:
  - Main src ejecuta tanto el código de extracción como de transformación, no necesita parámetros
  - Main extracción, ejecución por defecto todas las páginas de las webs, se puede escribir por teclado "peleas", "peleador" y "fechas" para ejecutar solo uno, también se puede poner como argumento las páginas que extrae cada   uno.
  - Main transformación, ejecución por defecto obteniendo los datos de data/raw pero se puede pasar como argumento una dirección en caso de que se quiera obtener los dataframes de otro lugar.
# Carpeta data en drive: 
- https://drive.google.com/drive/folders/1jX3HSEBXGX7HC6WhPOpthBHoO4UmwI8O?usp=drive_link

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
