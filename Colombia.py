"""
@Luis Alejandro Vejarano Gutierrez
@Johan Sebastián Miranda

PROYECTO COVID 19 COLOMBIA
"""

#### LIBRERIAS #####
import pandas as pd #Uso de DataFrame
from sodapy import Socrata #Petición HTTP
import numpy as ny #Manejo de Vectores Extensos
import matplotlib.pyplot as pt #Uso de Gráficas
import time #Manejo del tiempo

def Col():
    # Se obtiene la fecha actual para el nombre del PNG generado por cada gráfica
    hoy = time.strftime("%d-%m-%y")
    ### PETICIONES HTTP ###
    #Uso de Socrata Para Acceder a Datos Abiertos de Colombia con Token Único
    client = Socrata("www.datos.gov.co", "GJekEiJhbhkJ8pr6c4tjbMBYq")

    ### Conversión de Respuesta HTTP en pandas DataFrame
    cd = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT ciudad_municipio_nom as ciudad, count(ciudad_municipio_nom) as cantidad GROUP BY ciudad_municipio_nom ORDER BY ciudad_municipio_nom"))
    se = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT sexo, count(sexo) as ctdGenero GROUP BY sexo ORDER BY sexo"))
    ed = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT edad, count(edad) as cont GROUP BY edad ORDER BY edad"))
    mt = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT estado, count(estado) as cont GROUP BY estado ORDER BY estado"))
    fe = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT fecha_de_notificaci_n as fecha, count(fecha_de_notificaci_n) as cantidad GROUP BY fecha_de_notificaci_n ORDER BY fecha_de_notificaci_n"))

    ### MANEJO DE DATOS / GRÁFICOS ###

    #Solución problema de BD por género en mayúscula y minúsucula
    valGenero=[0,0]
    sexo=['Hombres','Mujeres']

    for x in range(len(se['sexo'])):
        if(se['sexo'][x] == 'M' or se['sexo'][x] == 'm'):
            valGenero[0]+= int(se['ctdGenero'][x])
        else:
            valGenero[1]+= int(se['ctdGenero'][x])


    #Gráfica de Torta de Casos Por Género
    fig1, ax1 = pt.subplots(figsize=(20,10))
    pt.title("CASOS CONFIRMADOS POR GÉNERO DE COVID-19 EN COLOMBIA\n", fontdict={'fontsize':15})
    ax1.pie(valGenero, labels=sexo, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')
    fig1.tight_layout()
    fname="GraficoTorta_Genero_Covid_Colombia_"+hoy+".png"
    pt.savefig(fname, bbox_inches='tight')

    #Clasificación de Casos Por Ciudades Principales
    ciudad=[]
    cantidad=[]

    for x in range(len(cd['ciudad'])):
        if(int(cd['cantidad'][x])>15000):
            ciudad.append(cd['ciudad'][x])
            cantidad.append(cd['cantidad'][x])


    #Diagrama de Torta por Ciudades
    fig1, ax1 = pt.subplots(figsize=(20,10))
    pt.title("CASOS CONFIRMADOS DE COVID-19 EN LAS CIUDADES MÁS INFECTADAS DE COLOMBIA\n", fontdict={'fontsize':15})
    ax1.pie(cantidad, labels=ciudad, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')
    fig1.tight_layout()
    fname="GraficoTorta_Casos_Ciudad_Covid_Colombia_"+hoy+".png"
    pt.savefig(fname, bbox_inches='tight')


    #Clasificación de Edades Por Segmentos
    agecant=[0,0,0,0,0]
    age=['NIÑOS\n0-12\naños','ADOLESCENTES\n13-18\naños','JOVENES\n19-35\naños','ADULTOS\n36-59\naños','ANCIANOS\n60+\naños']

    for x in range(len(ed['edad'])):
        aux= int(ed['edad'][x])
        aux2= int(ed['cont'][x])
        if aux<12:
            agecant[0]+=aux2
        elif (aux>=12 and aux<=18):
            agecant[1]+=aux2
        elif (aux>18 and aux<=35):
            agecant[2]+=aux2
        elif (aux>35 and aux<=59):
            agecant[3] += aux2
        else :
            agecant[4]+=aux2


    #Gráfica de Barras de Casos Por Edad
    fig,ax = pt.subplots(figsize=(20,10))
    ax.set_ylabel('Número de Casos')
    ax.set_title('CASOS CONFIRMADOS DE COVID-19 EN COLOMBIA POR EDADES')
    pt.bar(age, agecant)
    fig1.tight_layout()
    fname="GraficoBarras_Edad_Covid_Colombia_"+hoy+".png"
    pt.savefig(fname, bbox_inches='tight')


    #Solución Problema Mayúscula En Estado
    estado=['Leve','Moderado','Grave','Fallecido']
    estCant=[0,0,0,0]
    for x in range(len(mt['estado'])):
        aux=mt['estado'][x]
        aux2=int(mt['cont'][x])
        if (aux=="leve" or aux=="Leve" or aux=="LEVE"):
            estCant[0]+=aux2
        elif (aux=="Moderado" or aux=="moderado"):
            estCant[1]+=aux2
        elif (aux=="Grave"):
            estCant[2]+=aux2
        elif (aux=="Fallecido"):
            estCant[3]+=aux2

    #Gráfica de Barras de Casos Por Estado
    fig, ax = pt.subplots(figsize=(20,10))
    ax.set_ylabel('Número de Casos')
    ax.set_title('ESTADO DE CASOS CONFIRMADOS DE COVID-19 EN COLOMBIA')
    pt.bar(estado, estCant)
    fig1.tight_layout()
    fname="GraficoBarras_Estado_Covid_Colombia_"+hoy+".png"
    pt.savefig(fname, bbox_inches='tight')

    #Solución fecha sin formato
    for x in range(len(fe['fecha'])):
        aux=fe['fecha'][x]
        aux=aux[0:10]
        demo = aux.split("/")
        fe['fecha'][x]=int(demo[1])
        fe['cantidad'][x]=int(fe['cantidad'][x])

    #Organización casos por día en casos por mes
    cant=[0,0,0,0,0,0,0,0,0]
    fech=[]
    meses=['Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre']

    for x in range(len(fe['fecha'])):
        if (fe['fecha'][x] == 3):
            cant[0] += fe['cantidad'][x]
        elif (fe['fecha'][x] == 4):
            cant[1] += fe['cantidad'][x]
        elif (fe['fecha'][x] == 5):
            cant[2] += fe['cantidad'][x]
        elif (fe['fecha'][x] == 6):
            cant[3] += fe['cantidad'][x]
        elif (fe['fecha'][x] == 7):
            cant[4] += fe['cantidad'][x]
        elif (fe['fecha'][x] == 8):
            cant[5] += fe['cantidad'][x]
        elif (fe['fecha'][x] == 9):
            cant[6] += fe['cantidad'][x]
        elif (fe['fecha'][x] == 10):
            cant[7] += fe['cantidad'][x]
        elif (fe['fecha'][x] == 11):
            cant[8] += fe['cantidad'][x]

    #Gráfica de Barras Casos Por Mes
    fig, ax = pt.subplots(figsize=(20,10))
    ax.set_ylabel('NÚMERO DE CASOS')
    ax.set_title('CASOS CONFIRMADOS DE COVID-19 EN COLOMBIA POR MESES')
    pt.bar(meses, cant)
    fig1.tight_layout()
    fname="GraficoBarras_Mes_Covid_Colombia_"+hoy+".png"
    pt.savefig(fname, bbox_inches='tight')


    #Muestra todas las gráficas almacenadas
    pt.show()
