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



#print(df.dtypes)
ciudad=[]
cantidad=[]

for x in range(len(df['ciudad'])):
    if(int(df['cantidad'][x])>10000):
        ciudad.append(df['ciudad'][x])
        cantidad.append(df['cantidad'][x])

ny.random.seed(19680801)
pt.rcdefaults()
fig, ax = pt.subplots(figsize=(11, 5))

y_pos = ny.arange(len(ciudad))

ax.barh(y_pos, cantidad, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(ciudad)
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


fig, ax = pt.subplots(figsize=(15, 10), subplot_kw=dict(aspect="equal"))

recipe = ciudad

data = cantidad

wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = ny.sin(ny.deg2rad(ang))
    x = ny.cos(ny.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(ny.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*ny.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

ax.set_title("Contagios Covid-19 Bogotá")



t = ny.arange(22)
s = ny.array(cantidad)

fig, ax = pt.subplots()
ax.plot(t, s)

ax.grid(True, linestyle='-.')
ax.tick_params(labelcolor='r', labelsize='medium', width=3)




pt.grid() #Activa la cuadricula
pt.show() #Muestra la gráfica
