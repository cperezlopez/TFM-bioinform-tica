import pandas as pd
import Bio
from Bio import Entrez
import pymongo
from pymongo import MongoClient
from secuencias_PPI import secuencia_proteica

#En primer lugar importo los data frames del estudio una vez se han eliminado las secuencias repetidas y las poteinas que dan errores en la 
#busqueda de su secuencia
n_PPI_intact_negatome = pd.read_csv(r'cleaning_2/n_PPI_intact_negatome_c.csv')

#Le comunico al NCBI mi correo por si existiese algún problema con la consulta se pudiese poner en contacto conmigo
Entrez.email = "carpelo14.cpl@gmail.com"

#obtengo las secuencias de la Proteina A (relacionada con el Alzheimer)
proteinas_A = []
for n in range(len(n_PPI_intact_negatome['Proteina A'])):
    a = secuencia_proteica(n_PPI_intact_negatome['Proteina A'][n])
    proteinas_A.append(a)

#Y las secuencias de la B
proteinas_B = []
for n in range(len(n_PPI_intact_negatome['Proteina B'])):
    b = secuencia_proteica(n_PPI_intact_negatome['Proteina B'][n])
    proteinas_B.append(b)

#Una vez tengo las listas con las secuencias las adjunto al data frame 
n_PPI_intact_negatome['Secuencia A']= proteinas_A
n_PPI_intact_negatome['Secuencia B']= proteinas_B


#Ahora, lo introduzco en la base de datos mongo
mongo_uri = 'mongodb://localhost'  
client = MongoClient(mongo_uri)  #Lo llamamos client para poder conectarcon una db específica

db = client['estudio_de_proteinas']     #Se crea la base de datos

#Se crean las colecciones donde voy a guardar los datos
collection3 = db['n_PPI_intact_negatome']


for n in range(len(n_PPI_intact_negatome)):
    collection3.insert_one({'_id':n+1,'Proteina A': n_PPI_intact_negatome.iloc[n,0],'Proteina B': n_PPI_intact_negatome.iloc[n,1],'Secuencia A':n_PPI_intact_negatome.iloc[n,2],'Secuencia B':n_PPI_intact_negatome.iloc[n,3]})

