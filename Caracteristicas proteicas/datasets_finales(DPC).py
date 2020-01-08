import pandas as pd
from datasets_finales(AAC) import *
import datasets_finales(AAC)
import datasets_finales(AAC)
import pymongo
from pymongo import MongoClient

#Se sigue el mismo procedimiento que en la obtención de AAC
DPC_PPI_A = pd.read_csv(r'caracteristicas/DPC/PPI_A/descriptors.tsv', sep = '\t')
DPC_PPI_B = pd.read_csv(r'caracteristicas/DPC/PPI_B/descriptors.tsv', sep = '\t')
DPC_n_PPI_uniprot_A = pd.read_csv(r'caracteristicas/DPC/n_PPI_uniprot_A/descriptors.tsv',sep= '\t')
DPC_n_PPI_uniprot_B = pd.read_csv(r'caracteristicas/DPC/n_PPI_uniprot_B/descriptors.tsv',sep= '\t')
DPC_n_PPI_intact_negatome_A = pd.read_csv(r'caracteristicas/DPC/n_PPI_intact_negatome_A/descriptors.tsv', sep = '\t')
DPC_n_PPI_intact_negatome_B = pd.read_csv(r'caracteristicas/DPC/n_PPI_intact_negatome_B/descriptors.tsv', sep = '\t')

#Se ejectuta la función y se les cambian los nombres a las columnas, permitiendo distinguirlas
DPC_PPI_A = nombre_cols(DPC_PPI_A,'(A)')
DPC_PPI_B = nombre_cols(DPC_PPI_B,'(B)') 
DPC_n_PPI_uniprot_A = nombre_cols(DPC_n_PPI_uniprot_A, '(A)')
DPC_n_PPI_uniprot_B = nombre_cols(DPC_n_PPI_uniprot_B, '(B)')
DPC_n_PPI_intact_negatome_A =nombre_cols(DPC_n_PPI_intact_negatome_A, '(A)')
DPC_n_PPI_intact_negatome_B = nombre_cols(DPC_n_PPI_intact_negatome_B, '(B)')

#Se crean data frames vacios donde se incluirán los datos de cada pareja de proteinas y así poder juntar los datasets 
#que contienen la proteina A y la B
DPC_PPI = pd.DataFrame()
DPC_n_PPI_uniprot = pd.DataFrame()
DPC_n_PPI_intact_negatome = pd.DataFrame()

#Se aplica la función
DPC_PPI = union_df(DPC_PPI,DPC_PPI_A,DPC_PPI_B)
DPC_n_PPI_uniprot = union_df(DPC_n_PPI_uniprot, DPC_n_PPI_uniprot_A,DPC_n_PPI_uniprot_B)
DPC_n_PPI_intact_negatome = union_df(DPC_n_PPI_intact_negatome, DPC_n_PPI_intact_negatome_A,DPC_n_PPI_intact_negatome_B)

#Una vez que ya están listos los datasets que interaccionan y que no (con propiedades incluidas), se añade una nueva columna
#categorica donde el 1 significa que interaccionan las proteinas y el 0 que no interaccionan. De esta forma, se pueden mezclar
#sin perder de vista las que interaccionan  y las que no
DPC_PPI['Interaccion'] = 1
DPC_n_PPI_uniprot['Interaccion'] = 0
DPC_n_PPI_intact_negatome['Interaccion'] = 0

#Ahora se unen en 2 datasets, uno con las que interaccionan y el dataset que no interacciona sacado de uniprot y otro formado
#por los que interacionan y el data set sacado de la unión de Intact y Negatome que no interaccionan
DPC_uniprot = pd.concat([DPC_PPI,DPC_n_PPI_uniprot])
DPC_intact_negatome = pd.concat([DPC_PPI,DPC_n_PPI_intact_negatome])
columnas_uniprot = DPC_uniprot.columns.tolist()
columnas_intact_negatome = DPC_intact_negatome.columns.tolist()

#Se pasan a csv y se vuelven a cargar para así resetear los ids ya que los necesitamos para introducir los datasets en Mongo
export_csv = DPC_uniprot.to_csv (r'Datasets_finales/DPC_uniprot.csv', index = None, header=True)
export_csv = DPC_intact_negatome.to_csv (r'Datasets_finales/DPC_intact_negatome.csv', index = None, header=True)

DPC_uniprot = pd.read_csv(r'Datasets_finales/DPC_uniprot.csv')
DPC_intact_negatome = pd.read_csv(r'Datasets_finales/DPC_intact_negatome.csv')

#Por ultimo, se introduce en Mongodb
mongo_uri = 'mongodb://localhost'  
client = MongoClient(mongo_uri)  

db = client['estudio_de_proteinas']    

#Se crean las colecciones donde voy a guardar los datos
collection3 = db['DPC_uniprot']
collection4 = db['DPC_intact_negatome']

#Se aplica la funcion
insertar_mongo(DPC_uniprot,columnas_uniprot,collection3)

insertar_mongo(DPC_intact_negatome,columnas_intact_negatome,collection4)