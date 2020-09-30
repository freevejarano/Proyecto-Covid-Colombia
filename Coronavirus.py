"""
@Luis Alejandro Vejarano Gutierrez
@Johan Sebastián Miranda
@Manuel Alberto Torres

PROYECTO COVID 19 COLOMBIA
"""
import requests as rq #Se usa para hacer las peticiones a la página de datos abiertos
import numpy as ny #Facilita el manejo de vectores de gran tamaño
import matplotlib.pyplot as pt #Permite graficar los datos obtenidos

#Se declaran los arreglos que se van a emplear
tiempo=[]
casos=[]
localidad=[]
L_Estado=[]
L_Localidad=[]
L_Valor=[]

#Se asigna la dirección de datos abiertos
urlDatosAbiertos= 'https://datosabiertos.bogota.gov.co/api/3/action/datastore_search_sql?'

#Asignación de la consulta a la base de datos sql
urlDataSQL = 'sql=SELECT  "Localidad de residencia", count(*) as Cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" GROUP BY "Localidad de residencia" ORDER BY "Localidad de residencia"'

#Se hace la petición a la página de datos abiertos
requ= rq.get(url=urlDatosAbiertos+urlDataSQL)

#Organiza los datos obtendios como Json en un arreglo
requJson= requ.json()
Data= requJson['result']['records']

#Asignación en los arreglos
i=0
for f in Data:
    L_Valor.append(int(f["cantidad"]))
    L_Localidad.append(f["Localidad de residencia"])
    i=i+1

#Se hace un gráfico de barras con los datos por localidad
ny.random.seed(19680801)
pt.rcdefaults()
fig, ax = pt.subplots(figsize=(11, 5))

y_pos = ny.arange(len(L_Localidad))

ax.barh(y_pos, L_Valor, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(L_Localidad)
ax.invert_yaxis()
ax.set_xlabel('Número de Personas Contagiadas')
ax.set_title('Contagios Covid-19 Bogotá')

pt.grid() #Activa la cuadricula
pt.show() #Muestra la gráfica

