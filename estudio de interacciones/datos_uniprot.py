import numpy as np
import pandas as pd


#En este caso, debido a la naturaleza de los datos descargados, se lleva a cabo un trtamiento distinto para
#obtener los nombres de las proteinas
datos = pd.read_csv(r'Uniprot/pdbtosp.txt', sep ='\t')
datos = datos.iloc[:,-1]
datos = datos.str.split()

#Cojo 3000 numeros al azar que se corresponderan con las posiciones de las proteinas que cogeré, se cogen tantos para luego
#poder filtrar
np.random.seed(12345)
col_A = np.random.randint(0,142000,3000)
col_B = np.random.randint(0,142000,3000)
#Como hay valores que les faltan datos, filtro aquellos que no tengan las 6 columnas que necesito
columna_a = []
for i in range(0,len(col_A)):
    if len(datos[col_A[i]]) == 6:
        columna_a.append(col_A[i])

columna_b = []
for i in range(0,len(col_B)):
    if len(datos[col_B[i]]) == 6:
        columna_b.append(col_B[i])

#Ahora aislo los nombres de las proteinas
Proteina_A = []
Proteina_B = []
for i,j in zip(columna_a,columna_b):
    Proteina_A.append(datos[i][5])
    Proteina_B.append(datos[j][5])

#Ahora se eliminan aquellos datos que la columna no se correspondía al valor del nombre de la proteina
for a,b in zip(Proteina_A,Proteina_B):
    if len(a) < 4:
        Proteina_A.remove(a)
    if len(b) < 4:
        Proteina_B.remove(b)
#Ahora se eliminan los parentesis de los nombres de las proteinas
for n1,n2 in zip(range(len(Proteina_A)),range(len(Proteina_B))):
    Proteina_A[n1]= Proteina_A[n1].replace('(','').replace(')','')
    Proteina_B[n2]= Proteina_B[n2].replace('(','').replace(')','')

#Se cogen 1450 de cada lista para que coincidan
Proteina_A = Proteina_A[:1450]
Proteina_B = Proteina_B[:1450]

#Por último, se emparejan, asumiendo que como se han cogido de forma aleatoria, no van a interaccionar
n_PPI_uniprot = pd.DataFrame()
n_PPI_uniprot['Proteina A']=Proteina_A
n_PPI_uniprot['Proteina B']=Proteina_B
export_csv = n_PPI_uniprot.to_csv (r'uniprot/uniprot.csv', index = None, header=True)
