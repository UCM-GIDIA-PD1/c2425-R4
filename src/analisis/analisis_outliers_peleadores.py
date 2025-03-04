import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
from IPython.display import display

df = pd.read_csv("peleadores.csv")
df.head()

print("Columnas del DataFrame:")
print(df.columns)

df= df.drop(columns=['Unnamed: 0'])

# Mostrar los tipos de datos después de la conversión
print(df.dtypes)
print("\nTipos de datos:")
print(df.dtypes.to_string())

"""SUB (Sumisiones): Tiene una distribución altamente sesgada a la derecha, con la mayoría de los valores concentrados 
en los niveles más bajos y algunos valores extremadamente altos, 
lo que indica que la mayoría de los peleadores consiguen pocas sumisiones en sus carreras."""

print("\nResumen estadístico de columnas numéricas:")
pd.set_option('display.max_columns', None)
print(df.describe(include='all'))

numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns
print(numerical_columns)


plt.figure(figsize=(10, 5 * len(numerical_columns)))
for i, col in enumerate(numerical_columns):
    plt.subplot(len(numerical_columns), 1, i + 1)
    sns.boxplot(x=df[col])
    plt.title(f"Distribución de {col}")

plt.tight_layout()
plt.show()
"""Distribución sesgada a la derecha: La mayoría de los valores están concentrados 
en la parte baja de la escala, mientras que hay una gran cantidad de valores atípicos (outliers) hacia 
la derecha. Esto indica que la mayoría de los peleadores conectan pocos golpes significativos, 
pero hay algunos casos excepcionales donde se conectan muchos. Para mejorar eso deberíamos estudiar realizar ciertas transformaciones."""


# Identificación de valores atípicos usando IQR
outliers = {}
for col in numerical_columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers[col] = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)][col]

# Mostrar las columnas con sus respectivos outliers
for col, outlier_values in outliers.items():
    print(f"{col} tiene {len(outlier_values)} outliers")
    print(outlier_values.head(5))  # Muestra solo los primeros 5 valores atípicos para cada columna


df.hist(figsize=(14, 10))
plt.suptitle("Histogramas de las variables", fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()

"""Como vemos en los histogramas las variables no siguen distribuciones normales
y predomina, como ya habíamos visto con los boxplots las colas hacía la derecha."""


# Calcular el Z-score para todas las columnas numéricas
z_scores = df[numerical_columns].apply(zscore)

# Identificar valores con Z-score mayor a 3 o menor a -3
outliers_z = (z_scores.abs() > 3)

# Mostrar cuántos outliers hay en cada columna
outliers_count = outliers_z.sum()
print("\nNúmero de outliers detectados con Z-score:")
print(outliers_count[outliers_count > 0])