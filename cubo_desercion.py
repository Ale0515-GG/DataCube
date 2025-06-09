import pandas as pd
import plotly.express as px

# 1. Cargar archivos
tiempo_df = pd.read_excel('tiempo.xlsx')
estudiante_df = pd.read_excel('estudiante.xlsx')
escuela_df = pd.read_excel('escuelas.xlsx')
causa_df = pd.read_excel('causas.xlsx')

# 2. Generar ID para estudiante y tiempo
estudiante_df = estudiante_df.copy()
estudiante_df['id_estudiante'] = range(1, len(estudiante_df) + 1)

tiempo_df = tiempo_df.copy()
tiempo_df['id_tiempo'] = range(1, len(tiempo_df) + 1)

# 3. Renombrar columna de causa
causa_df = causa_df.rename(columns={'id_causa_desercion': 'id_causa'})

# 4. Asegurar que solo se usan los primeros N registros comunes
num_registros = min(len(tiempo_df), len(estudiante_df), len(escuela_df), len(causa_df))

hechos_df = pd.DataFrame({
    'id_hecho': range(1, num_registros + 1),
    'id_tiempo': tiempo_df['id_tiempo'][:num_registros].values,
    'id_estudiante': estudiante_df['id_estudiante'][:num_registros].values,
    'id_escuela': escuela_df['id_escuela'][:num_registros].values,
    'id_causa': causa_df['id_causa'][:num_registros].values,
})

# 5. Unir todo en el cubo
data_cube = hechos_df \
    .merge(tiempo_df, on='id_tiempo') \
    .merge(estudiante_df, on='id_estudiante') \
    .merge(escuela_df, on='id_escuela') \
    .merge(causa_df, on='id_causa')

# 6. Agregar columna de conteo
data_cube['conteo'] = 1

# 7. Mostrar columnas para verificar nombres
#print("Columnas del cubo:", data_cube.columns.tolist())

data_cube['dim_tiempo'] = data_cube['Año'].astype(str) + ' - ' + data_cube['Mes'].astype(str)
data_cube['dim_estudiante'] = data_cube['Nivel Educativo'].astype(str) + ' - ' + data_cube['Sexo']
data_cube['dim_escuela'] = data_cube['estado'].astype(str) + ' - ' + data_cube['nombre_escuela']
data_cube['dim_causa'] = data_cube['causa_principal']  # O agrega más columnas si quieres

# 8. Visualización 3D (ajusta los nombres según tus datos)
fig = px.scatter_3d(
    data_cube,
    x='dim_tiempo',
    y='dim_estudiante',
    z='dim_escuela',
    color='dim_causa',
    size='conteo',
    hover_data=['Año', 'Nivel Educativo', 'estado', 'causa_principal'],  # Más detalles al pasar el cursor
    title='Cubo de Datos 3D con Todas las Dimensiones'
)
fig.show()
