"""
@Luis Alejandro Vejarano Gutierrez
@Johan Sebastián Miranda

PROYECTO COVID 19 COLOMBIA
"""

#### LIBRERIAS #####
import pandas as pd #Uso de DataFrame
from sodapy import Socrata #Petición HTTP
import numpy as np #Manejo de Vectores
import matplotlib.pyplot as plt #Uso de Gráficas
import time #Manejo del tiempo actual

def ColReg():
    # Se obtiene la fecha actual para el nombre del PNG generado por cada gráfica
    hoy=time.strftime("%d-%m-%y")
    ### PETICIONES HTTP ###
    #Uso de Socrata Para Acceder a Datos Abiertos de Colombia con Token Único
    client = Socrata("www.datos.gov.co", "GJekEiJhbhkJ8pr6c4tjbMBYq")

    ### Conversión de Respuesta HTTP en pandas DataFrame
    cd = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT departamento_nom as depa, count(departamento_nom) as cantidad GROUP BY departamento_nom ORDER BY departamento_nom"))
    se = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT sexo, departamento_nom as depa, count(sexo) as ctdGenero GROUP BY sexo,departamento_nom ORDER BY sexo,departamento_nom"))
    mt = pd.DataFrame.from_records(client.get("gt2j-8ykr", query="SELECT estado, departamento_nom as depa, count(estado) as cont GROUP BY estado, departamento_nom ORDER BY estado, departamento_nom"))

    depa=[]
    cantidad=[]

    #Clasificación de Casos Por Regiones Principales
    for x in range(len(cd['depa'])):
        if(int(cd['cantidad'][x])>13000):
            depa.append(cd['depa'][x])
            cantidad.append(cd['cantidad'][x])

    #Gráfico de Torta Casos Por Departamento
    fig1, ax1 = plt.subplots(figsize=(20,10))
    plt.title("CASOS CONFIRMADOS POR LOCALIDAD DE COVID-19 EN COLOMBIA\n", fontdict={'fontsize':15})

    ax1.pie(cantidad, labels=depa, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')
    fig1.tight_layout()

    fig1.tight_layout()
    fname="GraficoCircular_Departamento_Covid_Colombia_"+hoy+".png"
    plt.savefig(fname, bbox_inches='tight')

    #Arreglos de Género por localidades
    mujeres=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    hombres=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for x in range(len(depa)):
        for k in range(len(se['sexo'])):
            if (se['depa'][k] == depa[x]):
                if(se['sexo'][k] == 'M' or se['sexo'][k] == 'm'):
                    hombres[x]+=int(se['ctdGenero'][k])
                elif(se['sexo'][k] == 'F' or se['sexo'][k] == 'f'):
                    mujeres[x]+=int(se['ctdGenero'][k])

    x = np.arange(len(depa))
    width = 0.35
    fig, ax = plt.subplots(figsize=(20,10))
    rects1 = ax.bar(x , mujeres, width, label='Mujeres')
    rects2 = ax.bar(x + width, hombres, width, label='Hombres')

    #Gráfica de barras por Regiones y Género
    ax.set_ylabel('Cantidad de Casos')
    ax.set_title('Casos Por Género En Los Departamentos Más Afectados de Colombia')
    ax.set_xticks(x)
    ax.set_xticklabels(depa,rotation='vertical')
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
    fname="GraficaBarras_Genero_Covid_Departamento_Colombia_"+hoy+".png"
    plt.savefig(fname, bbox_inches='tight')

    #Arreglos de Estado Por Localidades
    leve=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    mode=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    grave=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    falle=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for x in range(len(depa)):
        for k in range(len(mt['estado'])):
            if (mt['depa'][k] == depa[x]):
                aux = mt['estado'][k]
                aux2 = int(mt['cont'][k])
                if (aux == "leve" or aux == "Leve" or aux == "LEVE"):
                    leve[x] += aux2
                elif (aux == "Moderado" or aux == "moderado"):
                    mode[x] += aux2
                elif (aux == "Grave"):
                    grave[x] += aux2
                elif (aux == "Fallecido"):
                    falle[x] += aux2

    #Gráfico de Barras Por Estado en Localidades
    x = np.arange(len(depa))
    width = 0.35
    fig, ax = plt.subplots(figsize=(20,10))
    rects2 = ax.bar(x, leve, width, label='Leve')
    rects3 = ax.bar(x + width/2+0.2, mode, width, label='Moderado')
    rects4 = ax.bar(x + width/2 +0.4, grave, width, label='Grave')
    rects5 = ax.bar(x + width/2, falle, width, label='Fallecido')

    ax.set_ylabel('Cantidad de Casos')
    ax.set_title('Casos Por Estado En Los Departamentos Más Afectados de Colombia')
    ax.set_xticks(x)
    ax.set_xticklabels(depa,rotation='vertical')
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
    fname="GraficaBarras_Estado_Covid_Departamento_Colombia_"+hoy+".png"
    plt.savefig(fname, bbox_inches='tight')

    # Muestra todos los gráficos
    plt.show()
