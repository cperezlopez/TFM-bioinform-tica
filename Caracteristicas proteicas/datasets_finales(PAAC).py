import pandas as pd
from datasets_finales(AAC) import nombre_cols
from datasets_finales(AAC) import union_df
from datasets_finales(AAC) import insertar_mongo
from datasets_finales(CTD) import sustituir_nombres_cols
import pymongo
from pymongo import MongoClient

PAAC_PPI_A = pd.read_csv(r'caracteristicas/PAAC/PPI_A/descriptors.tsv', sep = '\t')
PAAC_PPI_B = pd.read_csv(r'caracteristicas/PAAC/PPI_B/descriptors.tsv', sep = '\t')
PAAC_n_PPI_uniprot_A = pd.read_csv(r'caracteristicas/PAAC/n_PPI_uniprot_A/descriptors.tsv',sep= '\t')
PAAC_n_PPI_uniprot_B = pd.read_csv(r'caracteristicas/PAAC/n_PPI_uniprot_B/descriptors.tsv',sep= '\t')
PAAC_n_PPI_intact_negatome_A = pd.read_csv(r'caracteristicas/PAAC/n_PPI_intact_negatome_A/descriptors.tsv', sep = '\t')
PAAC_n_PPI_intact_negatome_B = pd.read_csv(r'caracteristicas/PAAC/n_PPI_intact_negatome_B/descriptors.tsv', sep = '\t')

#Se ejectuta la función y se les cambian los nombres a las columnas, permitiendo distinguirlas
PAAC_PPI_A = nombre_cols(PAAC_PPI_A,'(A)')
PAAC_PPI_B = nombre_cols(PAAC_PPI_B,'(B)') 
PAAC_n_PPI_uniprot_A = nombre_cols(PAAC_n_PPI_uniprot_A, '(A)')
PAAC_n_PPI_uniprot_B = nombre_cols(PAAC_n_PPI_uniprot_B, '(B)')
PAAC_n_PPI_intact_negatome_A =nombre_cols(PAAC_n_PPI_intact_negatome_A, '(A)')
PAAC_n_PPI_intact_negatome_B = nombre_cols(PAAC_n_PPI_intact_negatome_B, '(B)')

#Se crean data frames vacios donde se incluirán los datos de cada pareja de proteinas y así poder juntar los datasets 
#que contienen la proteina A y la B
PAAC_PPI = pd.DataFrame()
PAAC_n_PPI_uniprot = pd.DataFrame()
PAAC_n_PPI_intact_negatome = pd.DataFrame()

#Se aplica la función
PAAC_PPI = union_df(PAAC_PPI,PAAC_PPI_A,PAAC_PPI_B)
PAAC_n_PPI_uniprot = union_df(PAAC_n_PPI_uniprot, PAAC_n_PPI_uniprot_A,PAAC_n_PPI_uniprot_B)
PAAC_n_PPI_intact_negatome = union_df(PAAC_n_PPI_intact_negatome, PAAC_n_PPI_intact_negatome_A,PAAC_n_PPI_intact_negatome_B)

#En este caso hay que efectuar un paso mas, ya que los nombres de las columnas poseen el caracter '.', y esto produce 
#errores al insertar los datos en Mongo. La solución será cambiar esos '.' por '_'
sustituir_nombres_cols(PAAC_PPI)
sustituir_nombres_cols(PAAC_n_PPI_uniprot)
sustituir_nombres_cols(PAAC_n_PPI_intact_negatome)

#Una vez que ya están listos los datasets que interaccionan y que no (con propiedades incluidas), se añade una nueva columna
#categorica donde el 1 significa que interaccionan las proteinas y el 0 que no interaccionan. De esta forma, se pueden mezclar
#sin perder de vista las que interaccionan  y las que no
PAAC_PPI['Interaccion'] = 1
PAAC_n_PPI_uniprot['Interaccion'] = 0
PAAC_n_PPI_intact_negatome['Interaccion'] = 0

#Ahora se unen en 2 datasets, uno con las que interaccionan y el dataset que no interacciona sacado de uniprot y otro formado
#por los que interacionan y el data set sacado de la unión de Intact y Negatome que no interaccionan
PAAC_uniprot = pd.concat([PAAC_PPI,PAAC_n_PPI_uniprot])
PAAC_intact_negatome = pd.concat([PAAC_PPI,PAAC_n_PPI_intact_negatome])
columnas_uniprot = PAAC_uniprot.columns.tolist()
columnas_intact_negatome = PAAC_intact_negatome.columns.tolist()

#Se pasan a csv y se vuelven a cargar para así resetear los ids ya que los necesitamos para introducir los datasets en Mongo
export_csv = PAAC_uniprot.to_csv (r'Datasets_finales/PAAC_uniprot.csv', index = None, header=True)
export_csv = PAAC_intact_negatome.to_csv (r'Datasets_finales/PAAC_intact_negatome.csv', index = None, header=True)
PAAC_uniprot = pd.read_csv(r'Datasets_finales/PAAC_uniprot.csv')
PAAC_intact_negatome = pd.read_csv(r'Datasets_finales/PAAC_intact_negatome.csv')

#Se añade a Mongodb como ya se ha hecho en otras ocasiones
import pymongo
from pymongo import MongoClient

mongo_uri = 'mongodb://localhost'  
client = MongoClient(mongo_uri)  

db = client['estudio_de_proteinas']    

#Se crean las colecciones donde voy a guardar los datos
collection7 = db['PAAC_uniprot']
collection8 = db['PAAC_intact_negatome']

#Se aplica la funcion
insertar_mongo(PAAC_uniprot,columnas_uniprot,collection7)

insertar_mongo(PAAC_intact_negatome,columnas_intact_negatome,collection8)