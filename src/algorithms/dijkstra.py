'''
Aquí implementaremos el algoritmo de Dijkstra utilizando coordenadas reales 
obtenidas de los eventos de pases de los datos de STATSBOMB.

'''
import numpy as np
import pandas as pd
import heapq

def dijkstra(graph, start):
    # Inicializar distancias y prioridad
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Verificar si la distancia actual es mayor que la guardada
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # Solo considerar este nuevo camino si es mejor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

# Ejemplo de uso
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

start_node = 'A'
distances = dijkstra(graph, start_node)
print("Distancias desde el nodo de inicio:", distances)
