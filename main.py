from modules import modules as md
import pandas as pd
import numpy as np
import requests
import bs4
from shapely.geometry import Point
import geopandas as gpd
import os
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    "--valor",
    dest = "valor",
    default = "EstacionMasCercana",
    help = "parametro para selecionar el tipo de ejecucion. Posibles valores: EstacionMasCercana , TodaslasEstaciones"
)

args = parser.parse_args(sys.argv[1:])

#transforma latitud/longitud en grados a coordinadas en metros
def to_mercator(lat, long):
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

#Función para sacar el json descargado de las estaciones de BiciMad
def read_json():
    bicimad = pd.read_json("Data/biciMad stations.json")
    long = [float(i.split(",")[0].replace("[", "")) for i in bicimad["geometry_coordinates"]]
    lat = [float(i.split(",")[1].replace("]", "")) for i in bicimad["geometry_coordinates"]]
    bicimad["LATITUD"] = lat
    bicimad["LONGITUD"] = long
    bicimad = bicimad.rename(index=str, columns={"LATITUD": "lat_finish", "LONGITUD": "long_finish"})
    bicimad = pd.DataFrame(bicimad[["name","address","lat_finish","long_finish"]])
    bicimad["DISTANCIA"] = bicimad.apply(lambda x: to_mercator(x["lat_finish"],x["long_finish"]), axis = 1)
    return bicimad

bicimad = read_json()

#Función para sacar los centros de la comunidad de Madrid y definir la distancia
def centros():
    centros = requests.get('https://datos.madrid.es/egob/catalogo/212769-0-atencion-medica.json')
    centros = centros.json()
    centros = pd.json_normalize(centros['@graph'])
    centros["TIPO DE LUGAR"] = "Sedes.Centros de atención médica"
    centros = centros.rename(index=str, columns={"location.latitude": "lat_start", "location.longitude": "long_start"})
    centros=pd.DataFrame(centros[["title", "TIPO DE LUGAR", "address.street-address", "lat_start", "long_start"]])
    centros["DISTANCIA"] = centros.apply(lambda x: to_mercator(x["lat_start"],x["long_start"]), axis = 1)
    return centros
centros = centros()

bicimad1 = pd.DataFrame(bicimad[["name","address","lat_finish","long_finish"]])
bicimad1["DISTANCIA"] = bicimad1.apply(lambda x: to_mercator(x["lat_finish"],x["long_finish"]), axis = 1)

centros1=pd.DataFrame(centros[["title", "TIPO DE LUGAR", "address.street-address", "lat_start", "long_start"]])
centros1["DISTANCIA"] = centros1.apply(lambda x: to_mercator(x["lat_start"],x["long_start"]), axis = 1)

#devuelve la distancia en metros entre dos latitudes/longitudes
def distance_meters(DISTANCIA_x, DISTANCIA_y):
    return DISTANCIA_x.distance(DISTANCIA_y)

#Función para hacer el merge entre los centros y las estaciones de biciMad
def bicis():
    df_bicis = pd.merge(bicimad1, centros1, how ='cross')
    df_bicis["DISTANCIA"] = df_bicis.apply(lambda x: distance_meters(x["DISTANCIA_x"],x["DISTANCIA_y"]), axis = 1)
    return df_bicis
df_bicis = bicis()


#Función para sacar el dataframe final desde el merge anterior
def final(): 
    df_final = pd.DataFrame(df_bicis[["title", "TIPO DE LUGAR", "address.street-address", "DISTANCIA", "name", "address"]])
    df_final = df_final.rename(index=str, columns={"title": "Place of Interest", "TIPO DE LUGAR": "Type of Place", "address.street-address": "Place Address", "name": "BiciMad Station", "address": "Station location"})
    return df_final
df_final = final()

#Función mediante la cual introduces el lugar y te devuelve la estación más cercana
def bicimad_station():
    i = str(input("Introduzca lugar "))
    x = df_final[df_final["Place of Interest"] == i]
    return x.sort_values(by = "DISTANCIA", ascending = True).head(1)
    

#Función mediante la cual te aparecen todos los centros y su estación BiciMad más cercana.
def bicimad():
    return df_final.sort_values(by = "DISTANCIA", ascending = True).groupby('Place of Interest')['Type of Place','Place Address', 'DISTANCIA','BiciMad Station', 'Station location'].nth(0).drop(["DISTANCIA"], axis = "columns")

if args.valor == "EstacionMasCercana":
    mas_cercana = bicimad_station()
    mas_cercana.to_csv("Data/Estación más cercana.csv", sep= ";")
    print("Guardado en Data")
elif args.valor == "TodaslasEstaciones":
    todas_ubicaciones = bicimad()
    todas_ubicaciones.to_csv("Data/Todas ubicaciones.csv", sep= ";")
    print("Guardado en Data")
else:
    print("Error, por favor, seleccione de entre EstacionMasCercana o TodaslasEstaciones")
