"""
@Luis Alejandro Vejarano Gutierrez
@Johan Sebastián Miranda

PROYECTO COVID 19 COLOMBIA
"""

import requests #Permite las peticiones a la API
import numpy as np #Manejo de Vectores
import matplotlib.pyplot as plt #Uso de Gráficas
import time #Manejo del tiempo

def BogLoc():
    #Se obtiene la fecha actual para el nombre del PNG generado por cada gráfica
    hoy=time.strftime("%d-%m-%y")

    #Consulta SQL a la API
    urlDatos = 'https://datosabiertos.bogota.gov.co/api/3/action/datastore_search_sql?'
    urlDatosSQL1 = 'sql=SELECT "LOCALIDAD_ASIS" as localidad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "LOCALIDAD_ASIS" order by "LOCALIDAD_ASIS"'
    urlDatosSQL2 = 'sql=SELECT "FECHA_DIAGNOSTICO" as fecha, "LOCALIDAD_ASIS" as localidad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "FECHA_DIAGNOSTICO","LOCALIDAD_ASIS" order by "FECHA_DIAGNOSTICO","LOCALIDAD_ASIS"'
    urlDatosSQL3 = 'sql=SELECT "SEXO" as gen, "LOCALIDAD_ASIS" as localidad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "SEXO","LOCALIDAD_ASIS" order by "SEXO","LOCALIDAD_ASIS"'
    urlDatosSQL4 = 'sql=SELECT "EDAD" as edad, "LOCALIDAD_ASIS" as localidad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "EDAD","LOCALIDAD_ASIS" order by "EDAD","LOCALIDAD_ASIS"'
    urlDatosSQL5 = 'sql=SELECT "ESTADO" as estado, "LOCALIDAD_ASIS" as localidad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "ESTADO","LOCALIDAD_ASIS" order by "ESTADO","LOCALIDAD_ASIS"'

    #Petición de datos, conversión de json a lista de diccionarios
    req1 = requests.get(url=urlDatos+urlDatosSQL1)
    reqJson1 = req1.json()
    ndict1=reqJson1['result']['records']

    #Organización de localidades, correción de los casos "sin dato"
    localidad=[]
    cantloca=[]

    for x in ndict1:
        if x['localidad']!=None:
            localidad.append(x['localidad'])
            cantloca.append(int(x['cantidad']))
        else:
            aux=localidad.index('Sin dato')
            cantloca[aux]+=int(x['cantidad'])


    #Gráfico de Torta Casos Por Localidad
    fig1, ax1 = plt.subplots(figsize=(20,10))
    plt.title("CASOS CONFIRMADOS DE COVID-19 POR LOCALIDAD EN BOGOTÁ\n", fontdict={'fontsize':15})

    ax1.pie(cantloca, labels=localidad, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')

    fig1.tight_layout()
    fname="GraficoCircular_Covid_Localidad_Bogota_"+hoy+".png"
    plt.savefig(fname, bbox_inches='tight')

    #Petición de datos, conversión de json a lista de diccionarios
    req3 = requests.get(url=urlDatos+urlDatosSQL3)
    reqJson3 = req3.json()
    ndict3=reqJson3['result']['records']

    #Organización de Datos por Género en Localidades
    genero=['Mujeres','Hombres']
    mujeres=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    hombres=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for k in range(len(localidad)):
        for x in ndict3:
            if(x['localidad']==localidad[k]):
                if(x['gen']=='F'):
                    mujeres[k]+=int(x['cantidad'])
                if(x['gen']=='M'):
                    hombres[k]+=int(x['cantidad'])

    x = np.arange(len(localidad))
    width = 0.35
    fig, ax = plt.subplots(figsize=(20,10))
    rects1 = ax.bar(x , mujeres, width, label='Mujeres')
    rects2 = ax.bar(x + width, hombres, width, label='Hombres')

    #Gráfica de Barras Por Género en Localidades
    ax.set_ylabel('Cantidad de Casos')
    ax.set_title('Casos Por Género En Las Localidades de Bogotá')
    ax.set_xticks(x)
    ax.set_xticklabels(localidad,rotation='vertical')
    ax.legend()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),
                        textcoords="offset points",
                        ha='center', va='bottom')

    fig.tight_layout()
    fname="GraficaBarras_Genero_Covid_Localidad_Bogota_"+hoy+".png"
    plt.savefig(fname, bbox_inches='tight')


    #Petición de datos, conversión de json a lista de diccionarios
    req5 = requests.get(url=urlDatos+urlDatosSQL5)
    reqJson5 = req5.json()
    ndict5=reqJson5['result']['records']


    #Clasificación del estado de los casos de Covid en Las Localidades de Bogotá
    recu=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    leve=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    mode=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    grave=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    falle=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    falleNo=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for k in range(len(localidad)):
        for x in ndict5:
            if(x['localidad']==localidad[k]):
                if(x['estado']=='Recuperado'):
                    recu[k]+=int(x['cantidad'])
                elif (x['estado']=='Leve'):
                    leve[k]+=int(x['cantidad'])
                elif (x['estado']=='Moderado'):
                    mode[k]+=int(x['cantidad'])
                elif (x['estado']=='Grave'):
                    grave[k]+=int(x['cantidad'])
                elif (x['estado']=='Fallecido'):
                    falle[k]+=int(x['cantidad'])
                elif (x['estado']=='Fallecido No aplica No Causa Directa'):
                    falleNo[k]+=int(x['cantidad'])

    #Gráfica de Barras por Estado en Localidades de Bogotá
    x = np.arange(len(localidad))
    width = 0.35
    estado=['Recuperado','Leve','Moderado','Grave','Fallecido','Fallecido No Aplica No Causa Directa']
    fig, ax = plt.subplots(figsize=(20,10))
    rects1 = ax.bar(x, recu, width, label='Recuperado')
    rects2 = ax.bar(x + width/2+0.1, leve, width, label='Leve')
    rects3 = ax.bar(x + width/2+0.2, mode, width, label='Moderado')
    rects4 = ax.bar(x + width/2+0.2, grave, width, label='Grave')
    rects5 = ax.bar(x + width/2+0.3, falle, width, label='Fallecido')
    rects6 = ax.bar(x + width/2+0.4, falleNo, width, label='Fallecido No Causa Directa')

    ax.set_ylabel('Cantidad de Casos')
    ax.set_title('Casos Por Estado En Las Localidades de Bogotá')
    ax.set_xticks(x)
    ax.set_xticklabels(localidad,rotation='vertical')
    ax.legend()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom')

    fig.tight_layout()
    fname="GraficaBarras_Estado_Covid_Localidad_Bogota_"+hoy+".png"
    plt.savefig(fname, bbox_inches='tight')


    #Petición de datos, conversión de json a lista de diccionarios
    req2 = requests.get(url=urlDatos+urlDatosSQL2)
    reqJson2 = req2.json()
    ndict2=reqJson2['result']['records']

    #Organización casos por día en casos por mes
    mar=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    abr=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    may=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    jun=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    jul=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ago=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    sep=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    oct=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    nov=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    #Correción formato de fecha
    for k in range(len(localidad)):
        for x in ndict2:
            if(isinstance(x['fecha'],str) and x['localidad']==localidad[k]):
                aux = x['fecha']
                aux = aux[0:10]
                demo = aux.split("-")
                e=int(demo[1])
                if (e == 3):
                    mar[k] += int(x['cantidad'])
                elif (e == 4):
                    abr[k] += int(x['cantidad'])
                elif (e == 5):
                    may[k] += int(x['cantidad'])
                elif (e == 6):
                    jun[k] += int(x['cantidad'])
                elif (e == 7):
                    jul[k] += int(x['cantidad'])
                elif (e == 8):
                    ago[k] += int(x['cantidad'])
                elif (e == 9):
                    sep[k] += int(x['cantidad'])
                elif (e == 10):
                    oct[k] += int(x['cantidad'])
                elif (e == 11):
                    nov[k] += int(x['cantidad'])

    #Gráfica de barras por meses en Localidades de Bogotá
    x = np.arange(len(localidad))
    width = 0.35
    meses=['Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre']

    fig, ax = plt.subplots(figsize=(20,10))
    rects1 = ax.bar(x, mar, width, label='Marzo')
    rects2 = ax.bar(x + 0.05, abr, width, label='Abril')
    rects3 = ax.bar(x + 0.1, may, width, label='Mayo')
    rects4 = ax.bar(x + 0.15, jun, width, label='Junio')
    rects5 = ax.bar(x + 0.2, jul, width, label='Julio')
    rects6 = ax.bar(x + 0.25, ago, width, label='Agosto')
    rects7 = ax.bar(x + 0.3, sep, width, label='Septiembre')
    rects8 = ax.bar(x + 0.35, oct, width, label='Octubre')
    rects9 = ax.bar(x + 0.4, nov, width, label='Noviembre')

    ax.set_ylabel('Cantidad de Casos')
    ax.set_title('Casos Por Meses En Las Localidades de Bogotá')
    ax.set_xticks(x)
    ax.set_xticklabels(localidad,rotation='vertical')
    ax.legend()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 5, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom')
    fig.tight_layout()
    fname="GraficaBarras_Mes_Covid_Localidad_Bogota_"+hoy+".png"
    plt.savefig(fname, bbox_inches='tight')


    #Petición de datos, conversión de json a lista de diccionarios
    req4 = requests.get(url=urlDatos+urlDatosSQL4)
    reqJson4 = req4.json()
    ndict4=reqJson4['result']['records']
    #Clasificación de Edades Por Segmentos
    menores=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    jovenes=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    adultos=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ancianos=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for k in range(len(localidad)):
        for x in ndict4:
            if (isinstance(x['edad'], str) and (x['localidad']==localidad[k])):
                aux= int(x['edad'])
                aux2= int(x['cantidad'])
                if aux<=18:
                    menores[k]+=aux2
                elif (aux>=19 and aux<=35):
                    jovenes[k]+=aux2
                elif (aux>35 and aux<=59):
                    adultos[k]+=aux2
                else :
                    ancianos[k]+=aux2

    #Gráfica de Barras Por Edades en Localidades de Bogotá
    x = np.arange(len(localidad))
    width = 0.35

    fig, ax = plt.subplots(figsize=(20,10))
    rects1 = ax.bar(x , menores, width, label='Menores de Edad (0-18 años)')
    rects2 = ax.bar(x + width/2+0.1, jovenes, width, label='Jóvenes (19-35 años)')
    rects3 = ax.bar(x + width/2+0.2, adultos, width, label='Adultos (36-59 años)')
    rects4 = ax.bar(x + width/2+0.3, ancianos, width, label='Ancianos (60+ años)')

    ax.set_ylabel('Cantidad de Casos')
    ax.set_title('Casos Por Edades En Las Localidades de Bogotá')
    ax.set_xticks(x)
    ax.set_xticklabels(localidad,rotation='vertical')
    ax.legend()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom')

    fname="GraficaBarras_Edad_Covid_Bogota_"+hoy+".png"
    plt.savefig(fname, bbox_inches='tight')
    fig.tight_layout()

    # Muestra todos los gráficos
    plt.show()