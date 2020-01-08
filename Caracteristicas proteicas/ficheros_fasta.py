#Para poder trabajar con iFeatures, hay que transformar la información que se tiene de las proteinas a formato fasta
from Obtencion_de_df import PPI
from Obtencion_de_df import n_PPI_uniprot
from Obtencion_de_df import n_PPI_intact_negatome
import pandas as pd

#Una vez se tienen las librerias, se crea una función que permita crear estos ficheros de texto en formato fasta
def crear_fasta(archivo,df,a,b):
    f = open(archivo,'w')

    for i in range(len(df)):
        f.write('>'+df.iloc[i,a]+'\n')
        f.write(df.iloc[i,b]+'\n')
    f.close()

#Antes de comenzar a aplicar la función y conseguir la librería hay que ajustar las proporciones de las librerías de interacciones
#En primer lugar, barajo el data frame, para que se escojan las filas al azar a la hora de seleccionar
n_PPI_uniprot = n_PPI_uniprot.sample(frac=1)
n_PPI_intact_negatome = n_PPI_intact_negatome.sample(frac=1)

#Ahora que están barajadas, se limita el data frame a 785 elementos, para obtener una misma proporción de datos entre ellas y el data frame PPI
# esta proporción será 1:2 con respecto a PPI que tiene 1570 elementos
n_PPI_uniprot = n_PPI_uniprot.iloc[0:785,]
n_PPI_intact_negatome = n_PPI_intact_negatome.iloc[0:785,]


#Ahora se crean 6 archivos, 2 para cada uno de los archivos con proteina y secuencia en formato fasta para poder llevar a cabo las consultas 
crear_fasta('PPI_A.txt',PPI,0,2)
crear_fasta('PPI_B.txt',PPI,1,3)
crear_fasta('n_PPI_uniprot_A.txt',n_PPI_uniprot,0,2)
crear_fasta('n_PPI_uniprot_B.txt',n_PPI_uniprot,1,3)
crear_fasta('n_PPI_intact_negatome_A.txt',n_PPI_intact_negatome,0,2)
crear_fasta('n_PPI_intact_negatome_B.txt',n_PPI_intact_negatome,1,3)

print(len(n_PPI_intact_negatome),len(n_PPI_uniprot))