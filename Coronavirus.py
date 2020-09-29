import requests as rq
import numpy as ny
import matplotlib.pyplot as pt

tiempo=[]
casos=[]
localidad=[]
L_Estado=[]
L_Localidad=[]
L_Valor=[]

urlDatosAbiertos= 'https://datosabiertos.bogota.gov.co/api/3/action/datastore_search_sql?'
urlDatosSQL = 'sql=SELECT  "Localidad de residencia", count(*) as Cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" GROUP BY "Localidad de residencia" ORDER BY "Localidad de residencia"'



