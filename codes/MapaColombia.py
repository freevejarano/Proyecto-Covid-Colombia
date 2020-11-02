"""
@Luis Alejandro Vejarano Gutierrez
@Johan Sebastián Miranda

PROYECTO COVID 19 COLOMBIA
"""

import requests #Petición
import os
import geopandas as gpd #Uso de GeoDataFrame
import numpy as np #Manejo de Vectores
import plotly
import plotly.express as px #Permite graficar el mapa
import pandas as pd #Uso de Panda DataFrame
from sodapy import Socrata #Petición HTTP

def MapCol():
    # Ingresar al sitio y descargar el CSV con los datos de Colombia
    url = "https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD&bom=true&format=true"
    response = requests.get(url)
    with open(os.path.join("data", "CasosCol.csv"), "wb") as f:
        f.write(response.content)

    #Abrir Archivo csv con los datos
    data = pd.read_csv('data/CasosCol.csv')
    data.head()

    #Especificar las columnas del DataFrame
    data.columns = ['Fecha', 'ID', 'Fecha2', 'Código DIVIPOLA', 'Departamento', 'Código DIVIPOLA2', 'Ciudad', 'Edad',
                    'Unnidad', 'Sexo', 'Tipo', 'Ubicacion', 'Atencion', 'Código ISO del país', 'Nombre del país',
                    'Recuperado', 'Fecha de inicio de síntomas', 'Fecha de muerte', 'Fecha de diagnóstico',
                    'Fecha de recuperación', 'Tipo de recuperación', 'Pertenencia étnica', 'Nombre del grupo étnico']

    #Abrir Archivo GEOJson
    repo_url = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
    mix_depa = requests.get(repo_url).json()
    extra = np.array(data.Departamento.value_counts())
    #Ajuste de la lista del número de casos por departamentos
    cantidad = np.array(
        [extra[1], extra[6], extra[0], extra[24], extra[17], extra[19], extra[21], extra[18], extra[9], extra[7],
         extra[3], extra[28], extra[12], extra[22], extra[25], extra[10], extra[11], extra[13], extra[23], extra[15],
         extra[4], extra[16], extra[14], extra[2], extra[29], extra[26], extra[27], extra[30], extra[33], extra[32],
         extra[34], extra[35], extra[31]])
    #Ajuste de los nombres de los Departamentos
    depa = np.array(
        ["ANTIOQUIA", "ATLANTICO", "SANTAFE DE BOGOTA D.C", "BOLIVAR", "BOYACA", "CALDAS", "CAQUETA", "CAUCA", "CESAR",
         "CORDOBA", "CUNDINAMARCA", "CHOCO", "HUILA", "LA GUAJIRA", "MAGDALENA", "META", "NARIÑO", "NORTE DE SANTANDER",
         "QUINDIO", "RISARALDA", "SANTANDER", "SUCRE", "TOLIMA", "VALLE DEL CAUCA", "ARAUCA", "CASANARE", "PUTUMAYO",
         "AMAZONAS", "GUAINIA", "GUAVIARE", "VAUPES", "VICHADA",
         "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA"])

    # Ajuste interno del mapa
    fig = px.choropleth(data_frame=data,  #Dataframe
                        geojson=mix_depa,  #GEOJson de Colombia
                        locations=depa,  #Lista de Departamentos
                        featureidkey='properties.NOMBRE_DPT',  #Acceso a la propiedad de Departamento del archivo GEOJson
                        labels={'color': 'Número de Casos'},  # Ajuste para la etiqueta lateral
                        color=cantidad,  # Varia según la cantidad
                        color_continuous_scale="burg",  #Escala de color
                        )

    # Ajustes externos del mapa
    fig.update_geos(showcountries=False, showcoastlines=False, showland=True, fitbounds="locations")

    # Ajuste del titulo
    fig.update_layout(
        title_text='\t\tCASOS DE COVID-19 EN COLOMBIA',
        font=dict(
            size=22,
            color="#FF0000"
        )
    )

    # Muestra el mapa en el navegador
    plotly.offline.plot(fig)


