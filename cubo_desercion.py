import pandas as pd
import plotly.express as px

# Leer los datos desde el archivo Excel
df = pd.read_excel('educacion.xlsx')

# Mostrar la tabla original
print("== Datos del archivo Excel ==")
print(df)

# Cubo 3D con Plotly
fig = px.scatter_3d(
    df,
    x='anio',               # Eje X: Año
    y='nivel_educativo',    # Eje Y: Nivel educativo
    z='causa',              # Eje Z: Causa de deserción
    color='casos',          # Color: número de casos
    size='casos',           # Tamaño del punto según número de casos
    symbol='sexo',          # Diferenciar por sexo
    title='Cubo de Datos 3D - Deserción Escolar'
)

# Mostrar el gráfico interactivo
fig.show()
