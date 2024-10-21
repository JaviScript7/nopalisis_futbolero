import warnings
import pandas as pd
from statsbombpy import sb
import streamlit as st  # Asegúrate de importar Streamlit

# Suprimir advertencias de StatsBomb
warnings.filterwarnings("ignore", category=UserWarning, module='statsbombpy.api_client')

def load_statbomb_data(competition_name="Copa America", season_id=282):
    # Obtener las competiciones
    competitions = sb.competitions()
    st.write("Competiciones disponibles:", competitions)  # Mostrar competiciones en Streamlit

    # Filtrar por la competición deseada
    competition_id_row = competitions[competitions['competition_name'] == competition_name]
    st.write("Fila de competición seleccionada:", competition_id_row)  # Mostrar fila seleccionada

    # Verificar si la competición existe
    if competition_id_row.empty:
        raise ValueError(f"La competición '{competition_name}' no se encontró en los datos.")
    
    competition_id = competition_id_row["competition_id"].values[0]
    st.write("ID de competición:", competition_id)  # Mostrar ID de competición

    # Intentar obtener los partidos de la competición seleccionada
    try:
        matches = sb.matches(competition_id=competition_id, season_id=season_id)
        st.write("Partidos obtenidos:", matches)  # Mostrar partidos obtenidos
        
        # Asegurarse de que hay partidos disponibles
        if matches is None or matches.empty:
            raise ValueError(f"No se encontraron partidos para la competición con ID {competition_id} y temporada {season_id}.")
    
    except Exception as e:
        st.error(f"Error al obtener datos de STATSBOMB: {e}")
        raise ValueError("No se pudo obtener la información.")

    # Selecciona el primer partido como ejemplo
    match_id = matches.iloc[0]['match_id']
    st.write("ID de partido seleccionado:", match_id)  # Mostrar ID de partido

    # Obtener eventos del partido
    events = sb.events(match_id=match_id)
    st.write("Eventos obtenidos:", events)  # Mostrar eventos obtenidos

    # Verificar que events no sea None y que tenga datos
    if events is None or events.empty:
        raise ValueError(f"No se encontraron eventos para el partido con ID {match_id}.")
    
    # Verificar la estructura de los eventos
    if 'type' in events.columns and 'name' in events['type'].dtype.names:
        passes = events[events['type']['name'] == 'Pass']
    else:
        raise ValueError("La estructura de eventos no es la esperada. Verifica los datos obtenidos.")
    
    return passes