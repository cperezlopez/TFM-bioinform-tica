import pandas as pd
from datasets_finales(AAC) import nombre_cols
from datasets_finales(AAC) import union_df
from datasets_finales(AAC) import insertar_mongo
import pymongo
from pymongo import MongoClient

CTD_PPI_A = pd.read_csv(r'caracteristicas/CTD/PPI_A/descriptors.tsv', sep = '\t')
CTD_PPI_B = pd.read_csv(r'caracteristicas/CTD/PPI_B/descriptors.tsv', sep = '\t')
CTD_n_PPI_uniprot_A = pd.read_csv(r'caracteristicas/CTD/n_PPI_uniprot_A/descriptors.tsv',sep= '\t')
CTD_n_PPI_uniprot_B = pd.read_csv(r'caracteristicas/CTD/n_PPI_uniprot_B/descriptors.tsv',sep= '\t')
CTD_n_PPI_intact_negatome_A = pd.read_csv(r'caracteristicas/CTD/n_PPI_intact_negatome_A/descriptors.tsv', sep = '\t')
CTD_n_PPI_intact_negatome_B = pd.read_csv(r'caracteristicas/CTD/n_PPI_intact_negatome_B/descriptors.tsv', sep = '\t')

#Se ejectuta la función y se les cambian los nombres a las columnas, permitiendo distinguirlas
CTD_PPI_A = nombre_cols(CTD_PPI_A,'(A)')
CTD_PPI_B = nombre_cols(CTD_PPI_B,'(B)') 
CTD_n_PPI_uniprot_A = nombre_cols(CTD_n_PPI_uniprot_A, '(A)')
CTD_n_PPI_uniprot_B = nombre_cols(CTD_n_PPI_uniprot_B, '(B)')
CTD_n_PPI_intact_negatome_A =nombre_cols(CTD_n_PPI_intact_negatome_A, '(A)')
CTD_n_PPI_intact_negatome_B = nombre_cols(CTD_n_PPI_intact_negatome_B, '(B)')

#Se crean data frames vacios donde se incluirán los datos de cada pareja de proteinas y así poder juntar los datasets 
#que contienen la proteina A y la B
CTD_PPI = pd.DataFrame()
CTD_n_PPI_uniprot = pd.DataFrame()
CTD_n_PPI_intact_negatome = pd.DataFrame()

#Se aplica la función
CTD_PPI = union_df(CTD_PPI,CTD_PPI_A,CTD_PPI_B)
CTD_n_PPI_uniprot = union_df(CTD_n_PPI_uniprot, CTD_n_PPI_uniprot_A,CTD_n_PPI_uniprot_B)
CTD_n_PPI_intact_negatome = union_df(CTD_n_PPI_intact_negatome, CTD_n_PPI_intact_negatome_A,CTD_n_PPI_intact_negatome_B)

#En este caso hay que efectuar un paso mas, ya que los nombres de las columnas poseen el caracter '.', y esto produce 
#errores al insertar los datos en Mongo. La solución será cambiar esos '.' por '_'

#Para ello, se crea una función
def sustituir_nombres_cols(df):
    col = df.columns.tolist()
    columna=[]
    for a in col:
        a = a.replace('.','_')
        columna.append(a)
    df.columns = columna

#Y se aplica dicha función
sustituir_nombres_cols(CTD_PPI)
sustituir_nombres_cols(CTD_n_PPI_uniprot)
sustituir_nombres_cols(CTD_n_PPI_intact_negatome)

#Una vez que ya están listos los datasets que interaccionan y que no (con propiedades incluidas), se añade una nueva columna
#categorica donde el 1 significa que interaccionan las proteinas y el 0 que no interaccionan. De esta forma, se pueden mezclar
#sin perder de vista las que interaccionan  y las que no
CTD_PPI['Interaccion'] = 1
CTD_n_PPI_uniprot['Interaccion'] = 0
CTD_n_PPI_intact_negatome['Interaccion'] = 0

#Ahora se unen en 2 datasets, uno con las que interaccionan y el dataset que no interacciona sacado de uniprot y otro formado
#por los que interacionan y el data set sacado de la unión de Intact y Negatome que no interaccionan
CTD_uniprot = pd.concat([CTD_PPI,CTD_n_PPI_uniprot])
CTD_intact_negatome = pd.concat([CTD_PPI,CTD_n_PPI_intact_negatome])
columnas_uniprot = CTD_uniprot.columns.tolist()
columnas_intact_negatome = CTD_intact_negatome.columns.tolist()

#Se pasan a csv y se vuelven a cargar para así resetear los ids ya que los necesitamos para introducir los datasets en Mongo
export_csv = CTD_uniprot.to_csv (r'Datasets_finales/CTD_uniprot.csv', index = None, header=True)
export_csv = CTD_intact_negatome.to_csv (r'Datasets_finales/CTD_intact_negatome.csv', index = None, header=True)

CTD_uniprot = pd.read_csv(r'Datasets_finales/CTD_uniprot.csv')
CTD_intact_negatome = pd.read_csv(r'Datasets_finales/CTD_intact_negatome.csv')

mongo_uri = 'mongodb://localhost'  
client = MongoClient(mongo_uri)  

db = client['estudio_de_proteinas']    

#Se crean las colecciones donde voy a guardar los datos
collection5 = db['CTD_uniprot']
collection6 = db['CTD_intact_negatome']

#Se aplica la funcion
insertar_mongo(CTD_uniprot,columnas_uniprot,collection5)

insertar_mongo(CTD_intact_negatome,columnas_intact_negatome,collection6)