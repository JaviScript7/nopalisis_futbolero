import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsbombpy import sb
from analisis.data_processing import load_statbomb_data

# Añadir la carpeta 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Configuración de estilo para las gráficas
sns.set(style="whitegrid")

# Título de la aplicación
st.title("Análisis de Datos de Fútbol")

# Cargar Font Awesome
st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """,
    unsafe_allow_html=True,
)

# Inicializa la variable de sesión para la página seleccionada
if 'page' not in st.session_state:
    st.session_state.page = "Inicio"  # Página por defecto

# Mostrar botones de navegación en la parte superior
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Inicio'):
        st.session_state.page = "Inicio"
        st.markdown('<i class="fa fa-home"></i> Inicio', unsafe_allow_html=True)

with col2:
    if st.button('Dijkstra'):
        st.session_state.page = "Dijkstra"
        st.markdown('<i class="fa fa-road"></i> Dijkstra', unsafe_allow_html=True)

with col3:
    if st.button('Análisis de Clustering'):
        st.session_state.page = "Análisis de Clustering"
        st.markdown('<i class="fa fa-chart-bar"></i> Análisis de Clustering', unsafe_allow_html=True)

# Menú de navegación lateral para parámetros y funciones
st.sidebar.title("Parámetros y Funciones")

# Obtener competiciones
competitions = pd.DataFrame(sb.competitions())

# Seleccionar competición
competition_name = st.sidebar.selectbox("Selecciona la Competición", competitions['competition_name'])

# Botón de cargar datos
load_data_button = st.sidebar.button("Cargar Datos")

# Función para cargar datos de la competición
def load_competition_data(competition_name):
    # Asignar automáticamente el ID de temporada según la competición seleccionada
    season_id = competitions.loc[competitions['competition_name'] == competition_name, 'season_id'].values[0]
    # Cargar datos desde STATSBOMB
    return load_statbomb_data(competition_name=competition_name, season_id=season_id)

# Código dentro de la página de inicio
if st.session_state.page == "Inicio":
    st.subheader("Bienvenido al Análisis de Datos de Fútbol")

    if load_data_button:
        passes = None  # Inicializar la variable para los datos

        # Cargar datos desde STATSBOMB
        try:
            passes = load_competition_data(competition_name)
            if passes is not None and not passes.empty:
                st.write(passes)
            else:
                st.error("No se encontraron datos para la competición seleccionada.")
        except ValueError as ve:
            st.error(str(ve))
        except Exception as e:
            print(f"Error al cargar datos de la competición: {str(e)}")

        # Gráficas de ejemplo
        if passes is not None and 'match_id' in passes.columns and not passes.empty:
            # Contar partidos por fecha
            match_counts = passes['match_id'].value_counts().reset_index()
            match_counts.columns = ['match_id', 'count']

            # Crear gráfico
            plt.figure(figsize=(10, 6))
            sns.barplot(data=match_counts, x='match_id', y='count', palette='viridis')
            plt.title('Cantidad de Eventos por Partido')
            plt.xlabel('ID del Partido')
            plt.ylabel('Cantidad de Eventos')
            st.pyplot(plt)  # Mostrar la gráfica en Streamlit
        else:
            print("No se encontraron datos para graficar.")

# Página para Dijkstra
elif st.session_state.page == "Dijkstra":
    st.subheader("Análisis de Rutas con Dijkstra")
    # Aquí iría tu lógica para el algoritmo de Dijkstra

# Página para Análisis de Clustering
elif st.session_state.page == "Análisis de Clustering":
    st.subheader("Análisis de Fútbol con Clustering")
    # Aquí iría tu lógica para el análisis de clustering
