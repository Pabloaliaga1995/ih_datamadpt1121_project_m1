import pandas as pd
import numpy as np
import requests
import bs4
from shapely.geometry import Point
import geopandas as gpd
import os
def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

bicimad = pd.read_json("Data/biciMad stations.json")
long = [float(i.split(",")[0].replace("[", "")) for i in bicimad["geometry_coordinates"]]
lat = [float(i.split(",")[1].replace("]", "")) for i in bicimad["geometry_coordinates"]]
bicimad["LATITUD"] = lat
bicimad["LONGITUD"] = long
bicimad = bicimad.rename(index=str, columns={"LATITUD": "lat_finish", "LONGITUD": "long_finish"})
bicimad = pd.DataFrame(bicimad[["name","address","lat_finish","long_finish"]])
bicimad["DISTANCIA"] = bicimad.apply(lambda x: to_mercator(x["lat_finish"],x["long_finish"]), axis = 1)

centros = requests.get('https://datos.madrid.es/egob/catalogo/212769-0-atencion-medica.json')
centros = centros.json()
centros = pd.json_normalize(centros['@graph'])
centros["TIPO DE LUGAR"] = "Sedes.Centros de atención médica"
centros = centros.rename(index=str, columns={"location.latitude": "lat_start", "location.longitude": "long_start"})
centros=pd.DataFrame(centros[["title", "TIPO DE LUGAR", "address.street-address", "lat_start", "long_start"]])
centros["DISTANCIA"] = centros.apply(lambda x: to_mercator(x["lat_start"],x["long_start"]), axis = 1)

bicimad1 = pd.DataFrame(bicimad[["name","address","lat_finish","long_finish"]])
bicimad1["DISTANCIA"] = bicimad1.apply(lambda x: to_mercator(x["lat_finish"],x["long_finish"]), axis = 1)

centros1=pd.DataFrame(centros[["title", "TIPO DE LUGAR", "address.street-address", "lat_start", "long_start"]])
centros1["DISTANCIA"] = centros1.apply(lambda x: to_mercator(x["lat_start"],x["long_start"]), axis = 1)


def distance_meters(DISTANCIA_x, DISTANCIA_y):
    return DISTANCIA_x.distance(DISTANCIA_y)

df_bicis = pd.merge(bicimad1, centros1, how ='cross')
df_bicis["DISTANCIA"] = df_bicis.apply(lambda x: distance_meters(x["DISTANCIA_x"],x["DISTANCIA_y"]), axis = 1)

df_final = pd.DataFrame(df_bicis[["title", "TIPO DE LUGAR", "address.street-address", "DISTANCIA", "name", "address"]])
df_final = df_final.rename(index=str, columns={"title": "Place of Interest", "TIPO DE LUGAR": "Type of Place", "address.street-address": "Place Address", "name": "BiciMad Station", "address": "Station location"})



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


def centros():
    centros = requests.get('https://datos.madrid.es/egob/catalogo/212769-0-atencion-medica.json')
    centros = centros.json()
    centros = pd.json_normalize(centros['@graph'])
    centros["TIPO DE LUGAR"] = "Sedes.Centros de atención médica"
    centros = centros.rename(index=str, columns={"location.latitude": "lat_start", "location.longitude": "long_start"})
    centros=pd.DataFrame(centros[["title", "TIPO DE LUGAR", "address.street-address", "lat_start", "long_start"]])
    centros["DISTANCIA"] = centros.apply(lambda x: to_mercator(x["lat_start"],x["long_start"]), axis = 1)
    return centros


def bicis():
    df_bicis = pd.merge(bicimad1, centros1, how ='cross')
    df_bicis["DISTANCIA"] = df_bicis.apply(lambda x: distance_meters(x["DISTANCIA_x"],x["DISTANCIA_y"]), axis = 1)
    return df_bicis

def final(): 
    df_final = pd.DataFrame(df_bicis[["title", "TIPO DE LUGAR", "address.street-address", "DISTANCIA", "name", "address"]])
    df_final = df_final.rename(index=str, columns={"title": "Place of Interest", "TIPO DE LUGAR": "Type of Place", "address.street-address": "Place Address", "name": "BiciMad Station", "address": "Station location"})
    return df_final


def bicimad_station():
    i = str(input("Introduzca lugar "))
    x = df_final[df_final["Place of Interest"] == i]
    return x.sort_values(by = "DISTANCIA", ascending = True).head(1)

def bicimad():
    return df_final.sort_values(by = "DISTANCIA", ascending = True).groupby('Place of Interest')['Type of Place','Place Address', 'DISTANCIA','BiciMad Station', 'Station location'].nth(0).drop(["DISTANCIA"], axis = "columns")
