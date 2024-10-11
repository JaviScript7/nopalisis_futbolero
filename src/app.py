import streamlit as st
import pandas as pd
import json

# Título de la aplicación
st.title("Subir archivos ")

# Cargar archivo
uploaded_file = st.file_uploader("Elige un archivo", type=["csv", "json"])

if uploaded_file is not None:
    # Leer el archivo según su tipo
    if uploaded_file.name.endswith('.csv'):
        # Leer el archivo CSV
        df = pd.read_csv(uploaded_file)
        st.write("Contenido del archivo CSV:")
        st.dataframe(df)
    elif uploaded_file.name.endswith('.json'):
        # Leer el archivo JSON
        data = json.load(uploaded_file)
        st.write("Contenido del archivo JSON:")
        st.json(data)

st.info("Sube un archivo CSV o JSON para ver su contenido.")
1