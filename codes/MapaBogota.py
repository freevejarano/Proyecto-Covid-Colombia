"""
@Luis Alejandro Vejarano Gutierrez
@Johan Sebastián Miranda

PROYECTO COVID 19 COLOMBIA
"""

import numpy as np #Manejo de Vectores
import matplotlib.pyplot as plt #Uso de Gráficas
import requests #Permite la petición a la API
import plotly
import plotly.express as px #Permite graficar el mapa
import geopandas as gpd #Uso de GeoDataFrame
import unidecode as un #Permite eliminar las tildes de un String

def MapBog():
    #Consulta SQL a la API
    urlDatos = 'https://datosabiertos.bogota.gov.co/api/3/action/datastore_search_sql?'
    urlDatosSQL1 = 'sql=SELECT "LOCALIDAD_ASIS" as localidad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "LOCALIDAD_ASIS" order by "LOCALIDAD_ASIS"'

    #Petición de datos, conversión de json a lista de diccionarios
    req1 = requests.get(url=urlDatos+urlDatosSQL1)
    reqJson1 = req1.json()
    ndict1=reqJson1['result']['records']

    #Organización de localidades, correción de los casos "sin dato" y emparejamiento con los datos del GEOJson
    localidad=[]
    cantloca=[]
    for x in ndict1:
        if x['localidad']!=None and x['localidad'] != 'Sin dato':
            auxloca=un.unidecode(x['localidad'].upper())
            if auxloca=='LA CANDELARIA':
                localidad.append('CANDELARIA')
            elif auxloca=='ANTONIO NARINO':
                localidad.append('ANTONIO NARIÑO')
            else:
                localidad.append(auxloca)

            cantloca.append(int(x['cantidad']))

    #Lectura del archivo GEOJson
    repo_url = 'data/bogota_localidades.geojson' #Archivo GeoJSON
    mx_regions_geo = gpd.read_file(repo_url)

    # Numpy array para el manejo de los arreglos
    casosLocalidades=np.array(cantloca)
    nombresLocalidades=np.array(localidad)

    # Ajuste interno del mapa
    fig = px.choropleth(data_frame=ndict1,
                    geojson=mx_regions_geo,
                    locations=nombresLocalidades,
                    featureidkey='properties.NOMBRE',#Ruta al campo del archivo GeoJSON
                    labels={'color':'Número de Casos'},#Ajuste para la etiqueta lateral
                    color=casosLocalidades,#El color depende de las cantidades
                    color_continuous_scale="burg",
                   )

    # Ajustes externos del mapa
    fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")

    # Ajuste del titulo
    fig.update_layout(
        title_text = '\t\tCasos de Covid-19 en Bogotá',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
            )
        )

    # Muestra el mapa en el navegador
    plotly.offline.plot(fig)
