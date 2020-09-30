"""
@Luis Alejandro Vejarano Gutierrez
@Johan Sebastián Miranda
@Manuel Alberto Torres

PROYECTO COVID 19 COLOMBIA
"""
#!/usr/bin/env python
# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import requests as rq
import pandas as pd
from sodapy import Socrata
import numpy as ny
import matplotlib.pyplot as pt


client = Socrata("www.datos.gov.co", "GJekEiJhbhkJ8pr6c4tjbMBYq")

results = client.get("gt2j-8ykr",query="SELECT ciudad_de_ubicaci_n as ciudad, count(ciudad_de_ubicaci_n) as cantidad GROUP BY ciudad_de_ubicaci_n ORDER BY ciudad_de_ubicaci_n")

# Convert to pandas DataFrame
df = pd.DataFrame.from_records(results)
se = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT sexo, count(sexo) as ctdGenero GROUP BY sexo ORDER BY sexo"))
#print(se.columns)

#print(df.dtypes)
ciudad=[]
cantidad=[]
valGenero=[0,0]
sexo=['Masculino','Femenino']

for x in range(len(df['ciudad'])):
    if(int(df['cantidad'][x])>10000):
        ciudad.append(df['ciudad'][x])
        cantidad.append(df['cantidad'][x])

for x in range(len(se['sexo'])):
    if(se['sexo'][x] == 'M' or se['sexo'][x] == 'm'):
        valGenero[0]+= int(se['ctdGenero'][x])
    else:
        valGenero[1]+= int(se['ctdGenero'][x])

print(valGenero[0]," ",valGenero[1])


ny.random.seed(19680801)
pt.rcdefaults()
fig, ax = pt.subplots(figsize=(11, 5))

y_pos = ny.arange(2)

ax.barh(y_pos, valGenero, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(sexo)
ax.invert_yaxis()
ax.set_xlabel('Número de Personas Contagiadas')
ax.set_title('Contagios Covid-19 Colombia')


labels = ciudad
sizes = cantidad
  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = pt.subplots(figsize=(10,7))
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.











pt.grid() #Activa la cuadricula
pt.show() #Muestra la gráfica
