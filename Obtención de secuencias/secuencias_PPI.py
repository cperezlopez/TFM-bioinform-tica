import pandas as pd
import Bio
from Bio import Entrez
import pymongo
from pymongo import MongoClient

#En primer lugar importo los data frames del estudio una vez se han eliminado las secuencias repetidas y las poteinas que dan errores en la 
#busqueda de su secuencia
PPI = pd.read_csv(r'cleaning_2/PPI_c.csv')

#Le comunico al NCBI mi correo por si existiese algún problema con la consulta se pudiese poner en contacto conmigo
Entrez.email = "carpelo14.cpl@gmail.com"

#Creo una función de consulta y obtención de secuencias primarias de proteinas a partir de un identificador
def secuencia_proteica(identificador):
    handle = Entrez.efetch(db="protein", id=identificador,rettype="FASTA", term="terminase large")
    record = handle.read()
    record = record.split('\n')
    record = record[:-2]
    seq = ''
    for line in record:
        if line[0] == '>':
            pass
        else:
            seq = seq +line
    return(seq)

#obtengo las secuencias de la Proteina A (relacionada con el Alzheimer)
proteinas_A = []
for n in range(len(PPI['Proteina A'])):
    a = secuencia_proteica(PPI['Proteina A'][n])
    proteinas_A.append(a)

#Y las secuencias de la B
proteinas_B = []
for n in range(len(PPI['Proteina B'])):
    b = secuencia_proteica(PPI['Proteina B'][n])
    proteinas_B.append(b)

#Una vez tengo las listas con las secuencias las adjunto al data frame 
PPI['Secuencia A']= proteinas_A
PPI['Secuencia B']= proteinas_B

#Ahora, lo introduzco en la base de datos mongo
mongo_uri = 'mongodb://localhost'  
client = MongoClient(mongo_uri)  #Lo llamamos client para poder conectarcon una db específica

db = client['estudio_de_proteinas']     #Se crea la base de datos

#Se crean las colecciones donde voy a guardar los datos
collection = db['PPI']

for n in range(len(PPI)):
    collection.insert_one({'_id': n+1,'Proteina A': PPI.iloc[n,0],'Proteina B': PPI.iloc[n,1],'Secuencia A':PPI.iloc[n,2],'Secuencia B':PPI.iloc[n,3]})