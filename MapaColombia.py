import requests
import pandas as px #Uso de DataFrame
import numpy as np #Manejo de Vectores
import plotly
import plotly.express as px
#### LIBRERIAS #####
import pandas as pd #Uso de DataFrame
from sodapy import Socrata #Petición HTTP
import time #Manejo del tiempo actual
### PETICIONES HTTP ###

#Uso de Socrata Para Acceder a Datos Abiertos de Colombia con Token Único
client = Socrata("www.datos.gov.co", "GJekEiJhbhkJ8pr6c4tjbMBYq")
data = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT departamento_nom as departamento, count(departamento_nom) as cantidad GROUP BY departamento_nom ORDER BY departamento_nom"))

#//////////////////MAPA DE CALOR COLOMBIA//////////////////////////
repo_url = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json' #Archivo GeoJSON
mx_regions_geo = requests.get(repo_url).json()
depa=[]
casoDep=[]
nombresDepartamentos=["ANTIOQUIA", "ATLANTICO", "SANTAFE DE BOGOTA D.C", "BOLIVAR", "BOYACA", "CALDAS", "CAQUETA", "CAUCA", "CESAR", "CORDOBA", "CUNDINAMARCA", "CHOCO", "HUILA", "LA GUAJIRA", "MAGDALENA", "META", "NARIÑO", "NORTE DE SANTANDER", "QUINDIO", "RISARALDA", "SANTANDER", "SUCRE", "TOLIMA", "VALLE DEL CAUCA", "ARAUCA", "CASANARE", "PUTUMAYO", "AMAZONAS", "GUAINIA", "GUAVIARE", "VAUPES", "VICHADA", "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA"]

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

casosDepartamentos=np.array(casoDep)
nombresDepartamentos=np.array(depa)

fig = px.choropleth(data_frame=data,
                    geojson=mx_regions_geo,
                    locations=nombresDepartamentos, # nombre de la columna del Dataframe
                    featureidkey='properties.NOMBRE_DPT',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                    labels={'color':'Número de Casos'},
                    color=casosDepartamentos, #El color depende de las cantidades
                    color_continuous_scale="burg", #greens
                   )

fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")

fig.update_layout(
    title_text = '\tCasos Covid-19 en Colombia',
    font=dict(
        family="Courier New, monospace",
       # family="Ubuntu",
        size=18,
        color="#7f7f7f"
    )
)
plotly.offline.plot(fig)

