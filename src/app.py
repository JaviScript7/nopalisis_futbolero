import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from statsbombpy import sb
from analisis.data_processing import load_statbomb_data
import networkx as nx
import random
from algorithms.dijkstra import obtener_jugadas_sugeridas

# Añadir la carpeta 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
# Configuración de estilo para las gráficas
sns.set(style="white")

# Función para dibujar el campo de fútbol
def dibujar_campo(ax=None,campo_color='#0e6b0e'):
    if ax is None:
        ax = plt.gca()

    # Parámetros del campo
    ancho_campo = 100
    alto_campo = 100

    # Dibujar el fondo del campo
    ax.set_facecolor(campo_color)  # Establece el color de fondo del campo

    # Dibujar el borde del campo
    plt.plot([0, 0], [0, alto_campo], color="white")
    plt.plot([0, ancho_campo], [alto_campo, alto_campo], color="white")
    plt.plot([ancho_campo, ancho_campo], [alto_campo, 0], color="white")
    plt.plot([ancho_campo, 0], [0, 0], color="white")

    # Dibujar el medio campo
    plt.plot([ancho_campo / 2, ancho_campo / 2], [0, alto_campo], color="white")

    # Dibujar el círculo central
    circulo_central = plt.Circle((ancho_campo / 2, alto_campo / 2), 10, color="white", fill=False)
    ax.add_patch(circulo_central)

    # Dibujar las áreas
    plt.plot([0, 16.5], [75, 75], color="white")
    plt.plot([16.5, 16.5], [75, 25], color="white")
    plt.plot([16.5, 0], [25, 25], color="white")

    plt.plot([ancho_campo, ancho_campo - 16.5], [75, 75], color="white")
    plt.plot([ancho_campo - 16.5, ancho_campo - 16.5], [75, 25], color="white")
    plt.plot([ancho_campo - 16.5, ancho_campo], [25, 25], color="white")

    # Dibujar los arcos
    plt.plot([0, -2], [60, 60], color="white")
    plt.plot([0, -2], [40, 40], color="white")
    plt.plot([ancho_campo, ancho_campo + 2], [60, 60], color="white")
    plt.plot([ancho_campo, ancho_campo + 2], [40, 40], color="white")

    return ax

# Almacenar las conexiones de pases en una lista
if 'pases' not in st.session_state:
    st.session_state.pases = []  # Inicializa una lista vacía para almacenar los pases

# Mostrar campo de fútbol con posiciones de jugadores y pases
def mostrar_campo_con_jugadores_y_pases(posiciones, pases):
    fig, ax = plt.subplots(figsize=(10, 7))
    # Dibujar el campo de fútbol
    ax = dibujar_campo(ax)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Colocar los jugadores en el campo según las posiciones de la formación
    for idx, (x, y) in enumerate(posiciones):
        ax.plot(x, y, 'bo', markersize=15)
        ax.text(x, y, str(idx + 1), color='white', fontsize=12, ha='center', va='center')

    # Dibujar los pases almacenados en la lista
    for pase in pases:
        jugador_origen, jugador_destino = pase
        x_origen, y_origen = posiciones[jugador_origen - 1]
        x_destino, y_destino = posiciones[jugador_destino - 1]
        ax.annotate('', xy=(x_destino, y_destino), xytext=(x_origen, y_origen),
                    arrowprops=dict(facecolor='blue', shrink=0.05))

    st.pyplot(fig)


# Función para construir la secuencia de jugadas
def construir_secuencia_jugada(jugada):
    return ' pasa '.join(map(str, jugada)) + ' y gol'

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



# Función para cargar datos de la competición
def load_competition_data(competition_name):
    # Asignar automáticamente el ID de temporada según la competición seleccionada
    season_id = competitions.loc[competitions['competition_name'] == competition_name, 'season_id'].values[0]
    # Cargar datos desde STATSBOMB
    return load_statbomb_data(competition_name=competition_name, season_id=season_id)

# Código dentro de la página de inicio
if st.session_state.page == "Inicio":
    st.subheader("Bienvenido al Análisis de Datos de Fútbol")
    # Obtener competiciones
    competitions = pd.DataFrame(sb.competitions())

    # Seleccionar competición
    competition_name = st.sidebar.selectbox("Selecciona la Competición", competitions['competition_name'])

    # Botón de cargar datos
    load_data_button = st.sidebar.button("Cargar Datos")

    if load_data_button:
        passes, matches_df = None, None  # Inicializar las variables para los datos

        # Cargar datos desde STATSBOMB
        try:
            passes, matches_df = load_competition_data(competition_name)
            if passes is not None and not passes.empty:
                st.write("Datos de Pases Cargados:")
                st.write(passes)  # Mostrar la tabla de eventos

                st.write("Datos de Partidos Cargados:")
                st.write(matches_df)  # Mostrar la tabla de partidos
            else:
                st.error("No se encontraron datos para la competición seleccionada.")
        except ValueError as ve:
            st.error(str(ve))
        except Exception as e:
            print(f"Error al cargar datos de la competición: {str(e)}")

        # Gráficas de ejemplo
        if passes is not None and 'match_id' in passes.columns and not passes.empty:
            st.subheader("Gráfica de Pases por Partido")
            fig, ax = plt.subplots()
            sns.countplot(data=passes, x='match_id', ax=ax)
            ax.set_title("Pases por Partido")
            st.pyplot(fig)

# Código dentro de la página de Dijkstra
elif st.session_state.page == "Dijkstra":
    st.subheader("Análisis de Jugadas con Dijkstra")

    # Elegir la formación
    formacion = st.sidebar.selectbox("Selecciona la Formación", ['4-4-2', '4-3-3', '3-5-2'])
    
    # Inicializar las posiciones de los jugadores según la formación seleccionada
    if formacion == '4-4-2':
        posiciones = [(5, 50), (20, 50), (30, 80), (30, 60), (30, 40), 
                      (30, 20), (50, 80), (50, 60), (50, 40), (50, 20), (80, 60), (80, 40)]
    elif formacion == '4-3-3':
        posiciones = [(5, 50), 
                      (20, 50), 
                      (30, 80), (30, 60), (30, 40),(30, 20), 
                      (50, 80), (50, 50), (50, 20),
                      (70, 70), (70, 50), (70, 30)]
    elif formacion == '3-5-2':
        posiciones = [(5, 50), 
                      (20, 50), 
                      (30, 80), (30, 50), (30, 20),
                      (50, 80), (50, 60), (50, 40), (50, 20),
                      (70, 70), (70, 30), 
                      (80, 50)]

    # Mostrar el campo con los jugadores
    mostrar_campo_con_jugadores_y_pases(posiciones, st.session_state.pases)

    # Modificar el código para mostrar las jugadas sugeridas
    if st.sidebar.button("Sugerir Jugadas"):
        jugadas_sugeridas = obtener_jugadas_sugeridas(posiciones)
        st.session_state.pases = []  # Reiniciar los pases

        # Mostrar las jugadas sugeridas en el campo
        for jugada in jugadas_sugeridas:
            # Guardar los pases
            for i in range(len(jugada) - 1):
                st.session_state.pases.append((jugada[i], jugada[i + 1]))

            # Formatear la salida de la jugada
            jugada_str = " pasa ".join(map(str, jugada)) + " y gol"
            st.write(f"Sugerencia de Jugada: {jugada_str}")

    # Mostrar el campo con jugadores
    mostrar_campo_con_jugadores_y_pases(posiciones, st.session_state.pases)

# Código dentro de la página de Análisis de Clustering
elif st.session_state.page == "Análisis de Clustering":
    st.subheader("Análisis de Clustering")
    # Aquí puedes agregar tu código para el análisis de clustering
