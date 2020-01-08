import pandas as pd

#Se crea una función para cambiar el nombre de las columnas y poner que pertenecen a la secuenca A o B para así poder 
#distinguirlas cuando se junten
def nombre_cols(df,nom):
    col = df.columns.tolist()
    columna = []
    for i in col:
        columna.append(i+nom)
    columna[0] = 'Secuencia'+ nom
    df.columns = columna
    return(df)

#Se crea una función que permita unir las filas, que se sabe que tienen las mismas columnas y así unir las parejas de proteinas con sus caracteristicas
def union_df(final, df_A,df_B):

    A = df_A.columns.tolist()
    B = df_B.columns.tolist()

    final['Secuancia A'] = df_A[A[0]]
    final['Secuencia B'] = df_B[B[0]]

    for nombre in A[1:]:
        final[nombre] = df_A[nombre]
    for nombre in B[1:]:
        final[nombre] = df_B[nombre]
    return(final)

#Se crea una función que permita insertar colecciones en mongo dado un data frame, las columnas de este y el nombre de la
#colección
def insertar_mongo(df,columnas,colecc):
    for n in range(len(df)):
        dic = {}
        contador = 0
        dic['_id'] = n+1
        for a in columnas[:len(columnas)-1]:
            dic[a]=df.iloc[n,contador]
            contador += 1
        dic['Interacción'] = int(df.iloc[n,len(columnas)-1]) #Se pone por separado al final la columna que se ha añadido
        colecc.insert_one(dic)


#Primero se obtienen las bases de datos finales de AAC
AAC_PPI_A = pd.read_csv(r'caracteristicas/ACC/PPI_A/descriptors.tsv', sep = '\t')
AAC_PPI_B = pd.read_csv(r'caracteristicas/ACC/PPI_B/descriptors.tsv', sep = '\t')
AAC_n_PPI_uniprot_A = pd.read_csv(r'caracteristicas/ACC/n_PPI_uniprot_A/descriptors.tsv',sep= '\t')
AAC_n_PPI_uniprot_B = pd.read_csv(r'caracteristicas/ACC/n_PPI_uniprot_B/descriptors.tsv',sep= '\t')
AAC_n_PPI_intact_negatome_A = pd.read_csv(r'caracteristicas/ACC/n_PPI_intact_negatome_A/descriptors.tsv', sep = '\t')
AAC_n_PPI_intact_negatome_B = pd.read_csv(r'caracteristicas/ACC/n_PPI_intact_negatome_B/descriptors.tsv', sep = '\t')

#Se ejectuta la función y se les cambian los nombres a las columnas, permitiendo distinguirlas
AAC_PPI_A = nombre_cols(AAC_PPI_A,'(A)')
AAC_PPI_B = nombre_cols(AAC_PPI_B,'(B)') 
AAC_n_PPI_uniprot_A = nombre_cols(AAC_n_PPI_uniprot_A, '(A)')
AAC_n_PPI_uniprot_B = nombre_cols(AAC_n_PPI_uniprot_B, '(B)')
AAC_n_PPI_intact_negatome_A =nombre_cols(AAC_n_PPI_intact_negatome_A, '(A)')
AAC_n_PPI_intact_negatome_B = nombre_cols(AAC_n_PPI_intact_negatome_B, '(B)')

#Se crean data frames vacios donde se incluirán los datos de cada pareja de proteinas y así poder juntar los datasets 
#que contienen la proteina A y la B
AAC_PPI = pd.DataFrame()
AAC_n_PPI_uniprot = pd.DataFrame()
AAC_n_PPI_intact_negatome = pd.DataFrame()

#Se aplica la función
AAC_PPI = union_df(AAC_PPI,AAC_PPI_A,AAC_PPI_B)
AAC_n_PPI_uniprot = union_df(AAC_n_PPI_uniprot, AAC_n_PPI_uniprot_A,AAC_n_PPI_uniprot_B)
AAC_n_PPI_intact_negatome = union_df(AAC_n_PPI_intact_negatome, AAC_n_PPI_intact_negatome_A,AAC_n_PPI_intact_negatome_B)

#Una vez que ya están listos los datasets que interaccionan y que no (con propiedades incluidas), se añade una nueva columna
#categorica donde el 1 significa que interaccionan las proteinas y el 0 que no interaccionan. De esta forma, se pueden mezclar
#sin perder de vista las que interaccionan  y las que no
AAC_PPI['Interaccion'] = 1
AAC_n_PPI_uniprot['Interaccion'] = 0
AAC_n_PPI_intact_negatome['Interaccion'] = 0

#Ahora se unen en 2 datasets, uno con las que interaccionan y el dataset que no interacciona sacado de uniprot y otro formado
#por los que interacionan y el data set sacado de la unión de Intact y Negatome que no interaccionan
AAC_uniprot = pd.concat([AAC_PPI,AAC_n_PPI_uniprot])
AAC_intact_negatome = pd.concat([AAC_PPI,AAC_n_PPI_intact_negatome])
columnas_uniprot = AAC_uniprot.columns.tolist()
columnas_intact_negatome = AAC_intact_negatome.columns.tolist()

#Se pasan a csv y se vuelven a cargar para así resetear los ids ya que los necesitamos para introducir los datasets en Mongo
export_csv = AAC_uniprot.to_csv (r'Datasets_finales/AAC_uniprot.csv', index = None, header=True)
export_csv = AAC_intact_negatome.to_csv (r'Datasets_finales/AAC_intact_negatome.csv', index = None, header=True)

AAC_uniprot = pd.read_csv(r'Datasets_finales/AAC_uniprot.csv')
AAC_intact_negatome = pd.read_csv(r'Datasets_finales/AAC_intact_negatome.csv')

#Se añade a Mongodb como ya se ha hecho en otras ocasiones
import pymongo
from pymongo import MongoClient

mongo_uri = 'mongodb://localhost'  
client = MongoClient(mongo_uri)  

db = client['estudio_de_proteinas']    

#Se crean las colecciones donde voy a guardar los datos
collection = db['AAC_uniprot']
collection2 = db['AAC_intact_negatome']

insertar_mongo(AAC_uniprot,columnas_uniprot,collection)
insertar_mongo(AAC_intact_negatome,columnas_intact_negatome,collection2)