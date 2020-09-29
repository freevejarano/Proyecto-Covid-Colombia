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
requJson= rq.json()
Data= requJson['result']['records']

#Asignción en los arreglos
i=0
for f in Data:
    L_Valor.append(int(f["Cantidad"]))
    L_Localidad.append(f["Residencia"])
    i=i+1




