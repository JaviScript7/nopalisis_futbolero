import statsbombpy as sb
import pandas as pd

def list_competitions():
    # Obtener competiciones desde el repositorio abierto
    competitions = sb.get_competitions()
    
    # Mostrar todas las columnas
    pd.set_option('display.max_columns', None)  # Esto permite mostrar todas las columnas
    print(competitions)

list_competitions()
