import pandas as pd
import plotly.express as px

# 1. Cargar archivos
tiempo_df = pd.read_excel('tiempo.xlsx')
estudiante_df = pd.read_excel('estudiante.xlsx')
escuela_df = pd.read_excel('escuelas.xlsx')
causa_df = pd.read_excel('causas.xlsx')

# 2. Generar ID para estudiante y tiempo
estudiante_df['id_estudiante'] = range(1, len(estudiante_df) + 1)
tiempo_df['id_tiempo'] = range(1, len(tiempo_df) + 1)

# 🔁 Convertir mes y año en fecha real para orden correcto
meses_map = {
    'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
    'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
    'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
}
tiempo_df['fecha'] = pd.to_datetime({
    'year': tiempo_df['anio'],
    'month': tiempo_df['mes'].map(meses_map),
    'day': 1
})

# 3. Renombrar columna de causa
causa_df = causa_df.rename(columns={'id_causa_desercion': 'id_causa'})

# 4. Asegurar mismo número de registros
num_registros = min(len(tiempo_df), len(estudiante_df), len(escuela_df), len(causa_df))

hechos_df = pd.DataFrame({
    'id_hecho': range(1, num_registros + 1),
    'id_tiempo': tiempo_df['id_tiempo'][:num_registros].values,
    'id_estudiante': estudiante_df['id_estudiante'][:num_registros].values,
    'id_escuela': escuela_df['id_escuela'][:num_registros].values,
    'id_causa': causa_df['id_causa'][:num_registros].values,
})

# 5. Unir tablas
data_cube = hechos_df \
    .merge(tiempo_df, on='id_tiempo') \
    .merge(estudiante_df, on='id_estudiante') \
    .merge(escuela_df, on='id_escuela') \
    .merge(causa_df, on='id_causa')

# 6. Agregar conteo
data_cube['conteo'] = 1

# 7. Crear dimensiones amigables
data_cube['dim_tiempo'] = data_cube['fecha'].dt.strftime('%Y-%m')

# Abreviar sexo y construir etiqueta corta para estudiantes
data_cube['sexo_abbr'] = data_cube['sexo'].map({'Masculino': 'M', 'Femenino': 'F'})
data_cube['dim_estudiante'] = data_cube['nivel_educativo'].astype(str) + ' (' + data_cube['sexo_abbr'] + ')'

# Asegurar que todos los estados están presentes
data_cube['dim_escuela'] = data_cube['estado'].astype(str)

# Causa
data_cube['dim_causa'] = data_cube['causa_principal']

# 8. Visualización 3D
fig = px.scatter_3d(
    data_cube.sort_values('fecha'),
    x='dim_tiempo',
    y='dim_estudiante',
    z='dim_escuela',
    color='dim_causa',
    size='conteo',
    hover_data=['anio', 'nivel_educativo', 'estado', 'causa_principal','nombre_escuela'],  # Más detalles al pasar el cursor
    title='Cubo de Datos 3D con Todas las Dimensiones'
)

fig.show()

#Número de casos por año y causa de deserción
pivot_1 = pd.pivot_table(
    data_cube,
    values='conteo',
    index='anio',           # filas
    columns='causa_principal',  # columnas
    aggfunc='sum',          # función de agregación
    fill_value=0            # reemplaza NaNs con 0
)

print(pivot_1)

#Deserciones por estado y nivel educativo
pivot_2 = pd.pivot_table(
    data_cube,
    values='conteo',
    index='estado',
    columns='nivel_educativo',
    aggfunc='sum',
    fill_value=0
)

print(pivot_2)

