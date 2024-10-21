'''
Aquí implementaremos el algoritmo de Dijkstra utilizando coordenadas reales 
obtenidas de los eventos de pases de los datos de STATSBOMB.

'''
import networkx as nx
import random

# Función para sugerir jugadas usando Dijkstra
def obtener_jugadas_sugeridas(posiciones):
    # Crear un grafo basado en las posiciones de los jugadores
    G = nx.Graph()

    # Añadir nodos (jugadores)
    for idx, pos in enumerate(posiciones):
        G.add_node(idx + 1, pos=pos)

    # Añadir aristas (pases posibles)
    for i in range(len(posiciones)):
        for j in range(len(posiciones)):
            if i != j:
                dist = ((posiciones[i][0] - posiciones[j][0])**2 + (posiciones[i][1] - posiciones[j][1])**2)**0.5
                G.add_edge(i + 1, j + 1, weight=dist)

    # Seleccionar aleatoriamente un jugador de origen y los destinos posibles
    origen = 1
    destinos = list(G.nodes())
    destinos.remove(origen)
    
    jugadas_sugeridas = []
    
    for _ in range(3):
        if not destinos:  # Verificar que hay destinos disponibles
            break
        
        destino = random.choice(destinos)
        
        try:
            path = nx.dijkstra_path(G, source=origen, target=destino)
            jugadas_sugeridas.append(path)
        except nx.NetworkXNoPath:
            st.error(f"No hay camino disponible entre el jugador {origen} y el jugador {destino}.")
            continue  # Si no hay camino, sigue a la siguiente iteración

    return jugadas_sugeridas
