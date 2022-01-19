
OBJECTIVES
- Get a table with every Medical Attention Center and its nearest BiciMad Station. This table would be saved in our folder(Data) by csv.
- Introducing a Medical Attention Center, we have to find the closest BiciMad Station. This table would be saved in our folder too (Data) by csv.

ENV
We have created a new environment (project1) and installed and import (import + "name of the library) therein the following library:
- Python 3.7 (conda install python == 3.7)
- Pandas (conda install pandas)
- Numpy (conda install numpy)
- BeautifulSoup (pip install BeautifulSoup)
- Shapely.geometry
- Geopandas (conda install geopandas)
- Requests(conda install requests)
- Argparse
- Sys 
- Json (conda install json)

CODE
- Import databases:
     - bicimad(from Azure Data Studio, downloading into our local repo).
     - centros: with requests we get the json from the website and work with it.
In order to clean the data, we have to create dataframes.
Once imported, we have to clean the database, in order to drop the columns that we are not goint to use and separate latitude and longitude in two differents columns. We have created a new column for the distance, using to mercator () to get a point between latitude and longitude.
For this step, we have used the functions read_json() and centros().

- Using distance_meters() we get the distances between two addresses.

- After getting the distance, we have to merge both tables, so we use bicis() in order to have a table with every distance, stations and centres.

- Naturally, we have to clean that table, so we use final() in order to get a table only with the data we would use.

- The final steps of our project are use a function to create a Dataframe with the closest biciMad Stations, that's why we use bicimad_station(). If we want to get every center with its closest station, we would use bicimad().

- For making it more intuitive for the user, we have introduce the argparse function. With this function, the user can introduce a string on terminal (EstacionMasCercana or TodaslasEstaciones) and depends on them decision, the terminal run the right code. Also, if the customer doesn't introduce anything, it would get a csv with the closest bicimad Station.

- Finally, in order to run it on Terminal, it has to be used the following command: python main.py followed by the type of table we want to get. If is there any question about the options, please, introduce python main.py --help.

CSV SAVED
--------------------------------------
- Documents/ironhack/ih_datamadpt1121_project_m1/Data/Estación más cercana.csv)
- Documents/ironhack/ih_datamadpt1121_project_m1/Data/Todas ubicaciones.csv) 


## **Project Main Stack**

- [Azure SQL Database](https://portal.azure.com/)

- [SQL Alchemy](https://docs.sqlalchemy.org/en/13/intro.html) (alternatively you can use _Azure Data Studio_)

- [Requests](https://requests.readthedocs.io/)

- [Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/index.html)

- Module `geo_calculations.py`

- [Argparse](https://docs.python.org/3.7/library/argparse.html)












 


 

