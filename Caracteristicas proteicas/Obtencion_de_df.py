#Lo primero de todo es obtener las secuencias que se habian guardado en Mongodb
import pandas as pd
import pymongo
from pymongo import MongoClient

#Se accede a Mongodb
mongo_uri = 'mongodb://localhost'  
client = MongoClient(mongo_uri)  #Lo llamamos client para poder conectarcon una db específica

#Se crea una función que permita generar dataframes a partir de los datos que hemos guardado en Mongodb
def obtener_dataframe_coleccion(datab,colle): 
    db = client[datab]
    collection = db[colle]

    # se guardan los datos de la colección en una variable
    results = collection.find()#Ahora results tiene todos los resultados

    #Ahora se crean listas para meter la información de Mongodb y posteriormente crear un data frame con el que trabajar
    Proteina_A =[]
    Secuencia_A = []
    Proteina_B = []
    Secuencia_B = []

    #Se llenan las listas
    for r in results:
        Proteina_A.append(r['Proteina A'])
        Proteina_B.append(r['Proteina B'])
        Secuencia_A.append(r['Secuencia A'])
        Secuencia_B.append(r['Secuencia B'])

    #Se crea el data frame
    df = pd.DataFrame()
    df['Proteina A'] = Proteina_A
    df['Proteina B'] = Proteina_B
    df['Secuencia A'] = Secuencia_A
    df['Secuencia B'] = Secuencia_B
    return(df)

#Ahora se obtienen los data frames
PPI = obtener_dataframe_coleccion('estudio_de_proteinas','PPI')
n_PPI_uniprot = obtener_dataframe_coleccion('estudio_de_proteinas','n_PPI_uniprot')
n_PPI_intact_negatome = obtener_dataframe_coleccion('estudio_de_proteinas','n_PPI_intact_negatome')
print(len(PPI))
print(len(n_PPI_uniprot))
print(len(n_PPI_intact_negatome))