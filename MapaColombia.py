"""
@Luis Alejandro Vejarano Gutierrez
@Johan Sebastián Miranda

PROYECTO COVID 19 COLOMBIA
"""

import geopandas as gpd #Uso de GeoDataFrame
import numpy as np #Manejo de Vectores
import plotly
import plotly.express as px #Permite graficar el mapa
import pandas as pd #Uso de Panda DataFrame
from sodapy import Socrata #Petición HTTP

def MapCol():
    #Uso de Socrata Para Acceder a Datos Abiertos de Colombia con Token Único
    client = Socrata("www.datos.gov.co", "GJekEiJhbhkJ8pr6c4tjbMBYq")
    data = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT departamento_nom as departamento, count(departamento_nom) as cantidad GROUP BY departamento_nom ORDER BY departamento_nom"))

    #MAPA DE COLOMBIA

    #Lectura del archivo GEOJson
    repo_url = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json' #Archivo GeoJSON
    mx_regions_geo = gpd.read_file(repo_url)
    depa=[]
    casoDep=[]

    #Ajuste de los arreglos según el GEOJson
    nomatch=['STA MARTA D.E.','CARTAGENA','BARRANQUILLA']
    for x in range(len(data['departamento'])):
        if not (data['departamento'][x] in nomatch):
            if data['departamento'][x]=='BOGOTA':
                depa.append('SANTAFE DE BOGOTA D.C')
            elif data['departamento'][x]=='GUAJIRA':
                depa.append('LA GUAJIRA')
            elif data['departamento'][x]=='NORTE SANTANDER':
                depa.append('NORTE DE SANTANDER')
            elif data['departamento'][x]=='VALLE':
                depa.append('VALLE DEL CAUCA')
            else:
                depa.append(data['departamento'][x])

            casoDep.append(data['cantidad'][x])

    #Numpy array para el manejo de los arreglos
    casosDepartamentos=np.array(casoDep)
    nombresDepartamentos=np.array(depa)

    #Ajuste interno del mapa
    fig = px.choropleth(data_frame=data,
                        geojson=mx_regions_geo,#GEOJson de Colombia
                        locations=nombresDepartamentos,#Lista de Departamentos ajustada al GEOJson
                        featureidkey='properties.NOMBRE_DPT',  #Ruta al campo del archivo GeoJSON
                        labels={'color':'Número de Casos'}, #Ajuste para la etiqueta lateral
                        color=casoDep, #El color depende de las cantidades
                        color_continuous_scale="burg",
                       )

    #Ajustes externos del mapa
    fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")

    #Ajuste del titulo
    fig.update_layout(
        title_text = '\tCasos Covid-19 en Colombia',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
            )
        )

    #Muestra el mapa en el navegador
    plotly.offline.plot(fig)


