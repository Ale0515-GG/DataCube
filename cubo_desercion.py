import pandas as pd
import plotly.express as px


# Datos simulados del modelo estrella
data = {
    'anio': [2021, 2021, 2022, 2022, 2023],
    'mes': ['Enero', 'Febrero', 'Enero', 'Febrero', 'Marzo'],
    'nivel_educativo': ['Secundaria', 'Media Superior', 'Media Superior', 'Superior', 'Superior'],
    'edad': [14, 17, 16, 20, 21],
    'sexo': ['F', 'M', 'F', 'F', 'M'],
    'etnia': ['No', 'Sí', 'Sí', 'No', 'No'],
    'comunidad': ['Rural', 'Urbana', 'Rural', 'Urbana', 'Rural'],
    'estado': ['Oaxaca', 'CDMX', 'Chiapas', 'CDMX', 'Oaxaca'],
    'servicios': ['Agua,Internet', 'Baños', 'Baños,Internet', 'Agua', 'Agua,Baños'],
    'causa': ['Económica', 'Personal', 'Institucional', 'Económica', 'Contextual'],
    'casos': [5, 10, 7, 4, 3]
}

df = pd.DataFrame(data)

# Mostrar tabla original
print("== Datos originales ==")
print(df)


# Usamos solo 3 dimensiones para simplificar
fig = px.scatter_3d(
    df,
    x='anio',
    y='nivel_educativo',
    z='causa',
    color='casos',
    size='casos',
    symbol='sexo',
    title='Cubo de Datos 3D - Deserción Escolar'
)

fig.show()