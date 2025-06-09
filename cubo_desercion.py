import pandas as pd
import plotly.express as px

# Cargar dimensiones desde archivos separados
tiempo_df = pd.read_excel('tiempo.xlsx')
estudiante_df = pd.read_excel('estudiante.xlsx')
escuela_df = pd.read_excel('escuela.xlsx')
causa_df = pd.read_excel('causa_desercion.xlsx')

# Simular hechos uniendo por índices
num_registros = min(len(tiempo_df), len(estudiante_df), len(escuela_df), len(causa_df))
hechos_df = pd.DataFrame({
    'id_hecho': range(1, num_registros + 1),
    'id_tiempo': range(1, num_registros + 1),
    'id_estudiante': range(1, num_registros + 1),
    'id_escuela': range(1, num_registros + 1),
    'id_causa': range(1, num_registros + 1),
})

# Unir todas las dimensiones al hecho
data_cube = hechos_df \
    .merge(tiempo_df.reset_index().rename(columns={'index': 'id_tiempo'}), on='id_tiempo') \
    .merge(estudiante_df.reset_index().rename(columns={'index': 'id_estudiante'}), on='id_estudiante') \
    .merge(escuela_df.reset_index().rename(columns={'index': 'id_escuela'}), on='id_escuela') \
    .merge(causa_df.reset_index().rename(columns={'index': 'id_causa'}), on='id_causa')

# Agrega columna de conteo para la medida
data_cube['conteo'] = 1

# Visualización 3D con Plotly (usa Año, Nivel educativo y Estado como ejes)
fig = px.scatter_3d(
    data_cube,
    x='Año',
    y='Nivel educativo',
    z='Estado',
    color='conteo',
    size='conteo',
    title='Cubo de Datos 3D - Deserción Escolar'
)

fig.show()
