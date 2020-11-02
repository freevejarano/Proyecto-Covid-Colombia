"""
@Luis Alejandro Vejarano Gutierrez
@Johan Sebastián Miranda

PROYECTO COVID 19 COLOMBIA
"""
# Importa las clases
import Colombia
import ColombiaRegiones
import MapaColombia
import Bogota
import BogotaLocalidades
import MapaBogota

# Se hace el llamado a cada clase
# Se ejecuta la siguiente clase una vez que se cierran todas las ventanas de la actual

Colombia.Col() #Gráficas de Colombia

ColombiaRegiones.ColReg() #Gráficas de Colombia por Departamentos

Bogota.Bog() #Gráficas de Bogotá

BogotaLocalidades.BogLoc() #Gráficas de Bogotá por Localidades

MapaColombia.MapCol() #Mapa de Colombia Por Departamentos Con Los Casos de Covid

MapaBogota.MapBog() #Mapa de Calor de Bogotá Por Localidades Con Los Casos de Covid