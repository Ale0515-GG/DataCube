import pandas as pd
import plotly.express as px

# Leer el Excel saltando metadatos
df = pd.read_excel('Educacion.xlsx', skiprows=5)

# Reorganizar a formato largo
df_long = df.melt(
    id_vars=['Entidad federativa', 'Nivel educativo'],
    var_name='anio',
    value_name='casos'
)

# Convertir casos a numérico, errores como NaN
df_long['casos'] = pd.to_numeric(df_long['casos'], errors='coerce')

# Eliminar valores nulos
df_long.dropna(subset=['casos'], inplace=True)

# Eliminar o ajustar valores negativos
df_long = df_long[df_long['casos'] >= 0]

# Convertir año a texto
df_long['anio'] = df_long['anio'].astype(str)

# Escalar los tamaños si los valores son muy pequeños
df_long['tamano'] = df_long['casos'] * 5  # ajusta el multiplicador según visualización

# Crear gráfico 3D
fig = px.scatter_3d(
    df_long,
    x='anio',
    y='Nivel educativo',
    z='Entidad federativa',
    color='casos',
    size='tamano',
    title='Cubo 3D - Tasa de Abandono Escolar'
)

fig.show()
