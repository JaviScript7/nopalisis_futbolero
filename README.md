# nopalisis_futbolero

## Análisis de Fútbol con Dijkstra

Para este proyecto usaremos el algoritmo de Dijkstra en el análisis de fútbol. El fútbol se basa en estrategias y movimientos optimizados, y Dijkstra puede ayudar a descubrir rutas óptimas en el campo, algo que podría tener aplicaciones tanto para la defensa como para el ataque.


## Análisis de Fútbol con Clustering con K-Means o DBSCAN

La idea es poder implementar esta opcion para identificar agrupamientos de jugadores o patrones de movimiento en el campo. Esto te ayudaría a ver las zonas del campo donde un equipo se concentra más o detectar formaciones y huecos. Este proceso esta pendiente

# Estructura del Proyecto
<pre>
Nopalisis_Futbolero/
├── 📂 data/
│   ├── data.json
│   └── ...
├── 📂 src/
│   ├── 📂 algorithms/
│   │   ├── dijkstra.py
│   │   └── ...
│   ├── 📂 analisis/
│   │   ├── data_processing.py
│   │   ├── clustering.py
│   │   └── visualization.py
│   ├── app.py
│   └── utils.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── main.py
</pre>

 ## 🚀 Despegar APP con Docker

 ### 🏗️ Vamos a construir el contenedor 📦

 ### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/JaviScript7/nopalisis_futbolero.git
```

### Paso 2: Navegar al directorio del proyecto
```bash
cd nopalisis_futbolero
```
### Paso 3: Ejecutar el contenedor Docker
```bash
docker-compose -f docker-compose.yml up -d --build 
```
### Paso 4: Verificar que los contenedores esten corriendo
```bash
docker ps 
```
### Paso 5: Verificar los logs 
```bash
docker logs <nombre del contenedor> 
```
### Paso 6: Si todo esta bien, abrir el navegador e ingresar la siguiente ruta 
```bash
http://localhost:8501/
```
### Paso 7: Para detener 
```bash
docker-compose -f docker-compose.yml down 
```

