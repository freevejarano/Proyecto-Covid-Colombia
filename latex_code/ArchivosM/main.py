﻿"""
@Luis Alejandro Vejarano Gutierrez
@Johan Sebastián Miranda
@Manuel Alberto Torres

PROYECTO COVID 19 COLOMBIA
"""

#### LIBRERIAS #####
import pandas as pd #Uso de DataFrame
from sodapy import Socrata #Petición HTTP
import numpy as ny #Manejo de Números
import matplotlib.pyplot as pt #Uso de Gráficas
import time #Manejo del tiempo actual

### PETICIONES HTTP ###

#Uso de Socrata Para Acceder a Datos Abiertos de Colombia con Token Único
client = Socrata("www.datos.gov.co", "GJekEiJhbhkJ8pr6c4tjbMBYq")


### Conversión de Respuesta HTTP en pandas DataFrame
cd = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT ciudad_de_ubicaci_n as ciudad, count(ciudad_de_ubicaci_n) as cantidad GROUP BY ciudad_de_ubicaci_n ORDER BY ciudad_de_ubicaci_n"))
se = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT sexo, count(sexo) as ctdGenero GROUP BY sexo ORDER BY sexo"))
ed = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT edad, count(edad) as cont GROUP BY edad ORDER BY edad"))
mt = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT estado, count(estado) as cont GROUP BY estado ORDER BY estado"))


### MANEJO DE DATOS / GRÁFICOS ###


#Se obtiene la fecha actual para el nombre del PNG generado por cada gráfica
hoy=time.strftime("%d-%m-%y")


#Solución problema de BD por género en mayúscula y minúsucula
valGenero=[0,0]
sexo=['Hombres','Mujeres']

for x in range(len(se['sexo'])):
    if(se['sexo'][x] == 'M' or se['sexo'][x] == 'm'):
        valGenero[0]+= int(se['ctdGenero'][x])
    else:
        valGenero[1]+= int(se['ctdGenero'][x])


#Gráfica de Torta de Casos Por Género
fig1, ax1 = pt.subplots(figsize=(10,7))
pt.title("CASOS CONFIRMADOS POR GÉNERO DE COVID-19 EN COLOMBIA\n", fontdict={'fontsize':15})
ax1.pie(valGenero, labels=sexo, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
fname="GraficoTorta_Genero_Covid_Colombia_"+hoy+".png"
pt.savefig(fname, bbox_inches='tight')

#Clasificación de Casos Por Ciudades Principales
ciudad=[]
cantidad=[]

for x in range(len(cd['ciudad'])):
    if(int(cd['cantidad'][x])>10000):
        ciudad.append(cd['ciudad'][x])
        cantidad.append(cd['cantidad'][x])


#Diagrama de Torta por Ciudades

fig1, ax1 = pt.subplots(figsize=(10,7))
pt.title("CASOS CONFIRMADOS DE COVID-19 EN LAS PRINCIPALES CIUDADES DE COLOMBIA\n", fontdict={'fontsize':15})
ax1.pie(cantidad, labels=ciudad, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
fname="GraficoTorta_Casos_Ciudad_Covid_Colombia_"+hoy+".png"
pt.savefig(fname, bbox_inches='tight')



#Clasificación de Edades Por Segmentos
agecant=[0,0,0,0,0]
age=['NIÑOS\n0-12\naños','ADOLESCENTES\n13-18\naños', 'JOVENES\n19-26\naños', 'ADULTOS\n26-59\naños', 'ANCIANOS\n60+\naños']

for x in range(len(ed['edad'])):
    aux= int(ed['edad'][x])
    aux2= int(ed['cont'][x])
    if aux<12:
        agecant[0]+=aux2
    elif (aux>=12 and aux<=18):
        agecant[1]+=aux2
    elif (aux>18 and aux<=26):
        agecant[2]+=aux2
    elif (aux>26 and aux<=59):
        agecant[3] += aux2
    else :
        agecant[4]+=aux2


#Gráfica de Barras de Casos Por Edad
fig, ax = pt.subplots()
ax.set_ylabel('Número de Casos')
ax.set_title('CASOS CONFIRMADOS DE COVID-19 EN COLOMBIA POR EDADES')
pt.bar(age, agecant)
fname="GraficoBarras_Edad_Covid_Colombia_"+hoy+".png"
pt.savefig(fname, bbox_inches='tight')


#Solución Problema Mayúscula En Estado
estado=['Asintomático','Leve','Moderado','Grave','Fallecido']
estCant=[0,0,0,0,0]

#
for x in range(len(mt['estado'])):
    aux=mt['estado'][x]
    aux2=int(mt['cont'][x])
    if(aux=="Asintomático"):
        estCant[0]+=aux2
    elif (aux=="leve" or aux=="Leve" or aux=="LEVE"):
        estCant[1]+=aux2
    elif (aux=="Moderado"):
        estCant[2]+=aux2
    elif (aux=="Grave"):
        estCant[3]+=aux2
    elif (aux=="Fallecido"):
        estCant[4]+=aux2

#Gráfica de Barras de Estado de Casos confirmados
fig, ax = pt.subplots()
ax.set_ylabel('Número de Casos')
ax.set_title('ESTADO DE CASOS CONFIRMADOS DE COVID-19 EN COLOMBIA')
pt.bar(estado, estCant)
fname="GraficoBarras_Estado_Covid_Colombia_"+hoy+".png"
pt.savefig(fname, bbox_inches='tight')


#Muestra todas las gráficas almacenadas
pt.show()
