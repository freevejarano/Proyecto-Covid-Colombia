import numpy as np #Manejo de Vectores
import matplotlib.pyplot as plt #Uso de Gráficas
import requests
import plotly
import plotly.express as px
import geopandas as gpd
import unidecode as un

def MapBog():
    #URL API Datos Abiertos de Bogotá
    urlDatos = 'https://datosabiertos.bogota.gov.co/api/3/action/datastore_search_sql?'

    #Consulta SQL a la API
    urlDatosSQL1 = 'sql=SELECT "LOCALIDAD_ASIS" as localidad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "LOCALIDAD_ASIS" order by "LOCALIDAD_ASIS"'

    #Petición de datos, conversión de json a lista de diccionarios
    req1 = requests.get(url=urlDatos+urlDatosSQL1)
    reqJson1 = req1.json()
    ndict1=reqJson1['result']['records']

    #Organización de localidades, correción de los casos "sin dato"
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


    repo_url = 'data/bogota_localidades.geojson' #Archivo GeoJSON
    mx_regions_geo = gpd.read_file(repo_url)

    casosLocalidades=np.array(cantloca)
    nombresLocalidades=np.array(localidad)


    fig = px.choropleth(data_frame=ndict1,
                    geojson=mx_regions_geo,
                    locations=nombresLocalidades,
                    featureidkey='properties.NOMBRE',
                    labels={'color':'Casos'},
                    color=casosLocalidades,
                    color_continuous_scale="burg",
                   )

    fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")

    fig.update_layout(
        title_text = '\t\tCasos de Covid-19 en Bogotá',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
            )
        )
    plotly.offline.plot(fig)
