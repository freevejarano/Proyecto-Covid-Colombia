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

results = client.get("gt2j-8ykr",query="SELECT ciudad_de_ubicaci_n, count(ciudad_de_ubicaci_n) as cantidad GROUP BY ciudad_de_ubicaci_n ORDER BY ciudad_de_ubicaci_n")

# Convert to pandas DataFrame
df = pd.DataFrame.from_records(results)

print(df)















""""
ciudad= df.columns
casoxC=[len(df.columns)]

    

print(casoxC)
#c= df.groupby('ciudad_de_ubicaci_n')['id_de_caso'].count()['Villavicencio']
#print(c)
#print(df['ciudad_de_ubicaci_n'].describe())



pt.rcdefaults()
fig, ax = pt.subplots(figsize=(11, 5))

y_pos = ny.arange(len(Ciudad))

ax.barh(y_pos, len(idCaso), align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(Ciudad)
ax.invert_yaxis()
ax.set_xlabel('Número de Personas Contagiadas')
ax.set_title('Contagios Covid-19 Bogotá')

pt.grid() #Activa la cuadricula
pt.show() #Muestra la gráfica

print(idCaso)"""