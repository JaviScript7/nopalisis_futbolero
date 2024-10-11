#Esto es un Dockerfile para entorno de produccion

#Elgimos nuestra imagen base con su version respectiva
FROM python:3.12

#Inidicamos quien es el responsable de mantener el contenedor
LABEL Maintainer = "JaviScript"

#Creamos el directorio de la aplicacion
RUN mkdir -p /home/app

#Instalacion de paquetes necesarios para correr Streamlit
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

#Copiar los archivos la aplicacion
COPY . /home/app

#Establecemos el espacio de trabajo
WORKDIR /home/app

#Exponemos el puerto en este caso para streamlit
EXPOSE 8501

#Instalamos las dependencias necesarios para correr el programa
RUN pip install --no-cache-dir -r /home/app/requirements.txt

#Con esto comprobamos que esta funcionando correctamente, comprobamos las salud de nuestra aplicacion
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

#Definimos lo que se ejecutara cuando el contenedor se inicie 
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
