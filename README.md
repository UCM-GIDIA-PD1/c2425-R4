# UFC Predictor: Sistema de predicción para la UFC
![imageheader](https://github.com/user-attachments/assets/fd3f4147-2067-4185-abf6-0875b595e960)

### Proyecto Datos I

## Índice

1. [Descripción de los objetivos](#1-descripción-de-los-objetivos)
2. [Estructura del repositorio](#2-estructura-del-repositorio)
3. [Cómo iniciar el entorno de desarrollo y sus dependencias](#3-como-iniciar-el-entorno-de-desarrollo-y-sus-dependencias)
4. [Instrucciones para ejecutar los scripts del proyecto](#4-instrucciones-para-ejecutar-los-scripts-del-proyecto)
5. [Resultados y evaluación](#5-resultados-y-evaluación)

### 1. Descripción de los objetivos

El objetivo de este proyecto es desarrollar dos sistemas de aprendizaje automático. Uno predice el ganador de un combate de la UFC basándose en datos de la pelea para conocer cuál es el ganador justo o cómo una herramienta que puedan usar jueces de la UFC. 

El segundo predice el ganador usando información previa al combate. Este modelo puede ser usado por fans del deporte para conocer cuáles son las probabilidades de victoria de cada peleador o en el mundo de las apuestas deportivas. Para ello utilizamos información sobre peleas previas de cada peleador realizando medias ponderadas. Esta información se obtiene de la página oficial de la UFC y UFC Stats que tiene todos los combates históricos.

De forma interna referenciamos el primer modelo mencionado como P2 y el segundo como P1, no es necesario saberlo pero quizás facilita el entendimiento del repositorio y las carpetas.

### 2. Estructura del repositorio

- La carpeta data incluye un .txt con un link a Google Drive para descargarse la carpeta de data con los parquets procesados y los csv extraídos. Los archivos de esta carpeta se deben copiar dentro de la carpeta data ya creada.
- La carpeta mlruns incluye los diferentes experimentos realizados con diferentes modelos e hiperparámetros.
- La carpeta src contiene todo el código. En esta carpeta encontramos diferentes carpetas con los módulos y procesos utilizados para realizar el proyecto.
   * Extracción:
      - `scraper_peleas.py`: Extrae información de todos los combates por evento de la UFC de forma cronológica, registramos el ganador, diferentes métricas de cada pelea y los peleadores que pelean en ella. Para obtener la
        información realizamos web-scraping de [UFC Stats](http://ufcstats.com/statistics/events/completed)
      - `scraper_peleadores.py`: Realiza web-scraping de información de peleadores y sus imágenes las cuales usaremos en la página web. La información se extrae de [UFC](https://www.ufc.com/athletes/all)
      - `scraper_fecha_nacimiento.py`: Utilizado para extraer las fechas de nacimientos de los peleadores realizando web-scraping de una fuente de datos secundaria llamada [Tapology](https://www.tapology.com/).
   * Transformación:
      - `tratamiento_peleas.py`: Contiene una función que realiza una limpieza de las variables extraídas para que sean más fáciles de utilizar. Creamos algunas nuevas variables para que sean más útiles para los modelos.
      - `tratamiento_peleadores.py`: Realiza la limpieza del dataset de peleadores para que las variables sean más usables.
      - `recordPeleas.py`: Calcula los records de cada peleador en el momento de las peleas. Es decir basándose en el record actual de un peleador, el cual hemos guardado en el dataset de peleadores, vamos calculando el record de cada peleador teniendo en cuenta si han perdido o ganado combates.
      - `nuevas_columnas_peleas_peleadores.py`: Este código contiene una función que crea nuevas variables algo más complejas basándose tanto en las peleas de cada luchador como en su perfil de peleador. En este código se crean variables como un sistema de puntos o las victorias o derrotas por cada método.
      - `peleasMediasPond.py`: Para cada pelea en el DataFrame de peleas sustituimos los datos reales de la pelea por las medias ponderadas de los últimos tres combates de cada peleador. En este caso las peleas cuyos peleadores no tengan más de tres combates son eliminados. Con esta función creamos el DataFrame que usaremos en el modelo de predicción de peleas futuras.
      - `dfDif.py`: Crea un DataFrame con las variables como diferencias entre peleadores. Este DataFrame se crea a partir del DataFrame de medias ponderadas.
   * Análisis:

        Para realizar el análisis lo separamos en cuatro notebooks diferentes. En `analisis_peleas.ipynb` y `analisis_peleadores.ipynb` realizamos una exploración inicial de el dataset de peleas y peleadores con visualizaciones. También realizamos el notebook `analisis_peleas_ponderadas.ipynb`, este notebook lo usamos para ver las distribuciones de las variables en el dataset creado en el script de transformaciones con medias ponderadas. También estudiamos la correlación de las variables con la variable respuesta. Por último, también realizamos `analisis_relaciones_variables_peleas.ipynb` en el cual estudiamos la relación de diferentes variables y sus correlaciones con las variables respuesta.
   * Modelos:

        Para realizar los diferentes modelos organizamos la carpeta model en tres carpetas. Una para los modelos con los datos de las peleas (P1), otra para los modelos de previos a las peleas (P2) y otra para los modelos de P2 con las variables como diferencias entre los peleadores. En cada uno de estas carpetas encontramos los modelos de `XGBoost`, `LogisticRegression` y `TreeClassifier` para cada modelo. En el caso de los modelos usando diferencias no usamos árboles de decisión ya que estos los usamos para realizar un análisis exploratorio. En esta carpeta también encontramos los notebooks para realizar las particiones de datos, respetando la secuencia temporal en caso de que sea necesario.
   * Evaluación:
 
        En cuanto a la carpeta de evaluación, encontramos dos subcarpetas que separan las evaluaciones por objetivo del modelo. Es decir, encontramos una carpeta para la evaluación de los modelos que predicen con datos de la pelea y otra carpeta para los modelos que predicen con datos previos a la pelea. En cada carpeta encontramos un notebook de evaluación, en el cual se comparan todos los modelos creados con ese objetivo en la fase de modelaje y se escoje el que obtiene mejores resultados. También encontramos otro notebook en el cual se pone a prueba a los modelos con nuevos datos más recientes para probar el funcionamiento de los modelos.

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

### 4. Instrucciones para ejecutar los scripts del proyecto

💡 Nota: Es necesario haber inicializado el entorno virtual con sus dependencias previamente.

* Extracción:

💡 Nota: La extracción puede tomar bastante tiempo. En caso de no querer realizarla existe un documento `data/data.txt` que contiene el link con una carpeta drive con los datos ya extraídos.

1. Este `main.py` realiza todo el proceso de extracción. Se encuentra en la ruta `src\extraccion`. Este script se encarga de realizar web-scraping de todas las fuentes de datos que utilizamos. Para ello se debe ejecutar incluyendo como parámetro los datos que queremos extraer que pueden ser "peleas", "peleadores" o "fechas". La ejecución del `main.py` es similar para los tres. Primero entramos a la carpeta donde se encuentra el script (se puede ejecutar también desde la raíz incluyendo el path).
```
cd src
cd extraccion
```
2. Después ejecutamos el main con el parámetro que queramos extraer que puede ser peleas, peleadores o fechas.
```
uv run main.py peleas
```
3. En caso de que se quiera se pueden añadir más parametros. Esos parámetros son diferentes en el caso de las diferentes fuentes, por ello explicamos para cada caso cuales son.
 * Peleas:
    * --pagina_inicio: Tipo entero, indica la página por la que queremos empezar a extraer.
    * --pagina_final: Tipo entero, indica la página en la que queremos parar de extraer.
 * Peleadores:
    * --pagina_inicio: Tipo entero, indica la página por la que queremos empezar a extraer.
    * --pagina_final: Tipo entero, indica la página en la que queremos parar de extraer.
  * Fechas:
    * --fila_inicio: Tipo entero, fila del dataset de peleadores por el que queremos empezar a extraer información sobre el peleador adicional.
    * --fila_final: Tipo, entero, fila del dataset de peleadores en el que acaba la extracción. Recomendamos extraer como mucho 200 filas cada tanda. Sino corremos el riesgo de que bloqueen la IP y no podamos continuar extrayendo durante un periodo de tiempo.

* Transformación:
1. Este `main.py` realiza la limpieza, transformación y creación de variables que usarán los modelos para predecir los resultados. Se encuentra en la ruta `src\transformacion`. Primero entramos a la carpeta donde se encuentra el script (se puede ejecutar también desde la raíz incluyendo el path).
```
cd src
cd transformacion
```
2. Después ejecutamos el main. Si no se añaden parámetros extraerá los datos `raw` de la carpeta `data`. En caso de que se quiera introducir un directorio de peleas o peleadores diferente se podría cambiar usando el parámetro `--dir_peleas` o `dir_peleadores`.
```
uv run main.py
``` 

### 5. Resultados y evaluación

* Modelo con datos de la pelea:

  En este caso, el modelo que obtuvo el mejor desempeño fue `XGBoost`, tras un ajuste de hiperparámetros utilizando `GridSearchCV`. A continuación, se presentan las métricas del mejor modelo en comparación con el baseline (que predice como ganador a quien da más golpes):
  | Modelo | Accuracy | F1-Score |
  | --- | --- | --- |
  | XGBoost| 0.954  | 0.944 |
  | Baseline | 0.70 | 0.65 |

  Los resultados finales fueron bastante buenos mejorando notablemente el baseline.

  En cuanto a la evaluación con nuevos datos, los cuales corresponden a los eventos ocurridos desde la última extración hasta la última fase del proyecto, también fueron buenos manteniendo un Accuracy y F1-Score prácticamente idénticos a los de la última evaluación. En este caso se obtuvo un Accuracy al rededor de 0.95 y un F1-Score de 0.945.

* Modelo con datos previos a la pelea:

  En cuánto al modelo que predice peleas futuras, los mejores resultados se obtuvieron con el modelo `XGBoost` con las variables representadas como diferencias entre los peleadores. En este caso también creamos un Baseline, el cual se basaba en que siempre ganaba el `Peleador_A` que es el favorito o que tiene un puesto superior en el ranking.

  | Modelo | Accuracy | F1-Score |
  | --- | --- | --- |
  | XGBoost| 0.6025 | 0.56 |
  | Baseline | 0.54 | 0.00 |

En este caso los resultados no son tan buenos. Aun así conseguimos mejorar el Accuracy del baseline más de un 6% y una clara mejora para predecir los combates en los que gana el Peleador_B, el cual suele ser no favorito.

Tras obtener nuevos datos volvimos a poner a prueba al modelo. Sorprendentemente, obtuvimos un mejor Accuracy con los nuevos datos, cercano a 64%. También mejoró el F1-Score llegando a 62%. 


### 6. Equipo de desarrollo
 -  Andrés Fernández Ortega
 -  Francisco José Pastor Ruiz
 -  Mario Granados Guerrero
 -  Telmo Aracama Docampo
 -  Carlos Vallejo Ros
 -  Mateo Turati Domínguez
   
Mención especial y agradecimientos a nuestro profesor Antonio Alejandro Sánchez Ruiz-Granados por su constante ayuda y supervisión a lo largo del desarrollo del proyecto.
