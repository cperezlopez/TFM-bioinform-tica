#Se sigue el mismo codigo que en 'datos_intact'
import pandas as pd

datos = pd.read_csv('intact/intact_negative.txt', sep = '\t', encoding= 'utf8')

#Se cogen las 2 primeras columnas y se les pone ese nombre
intact = datos.iloc[:,0:2]
intact.columns = ['Proteina A', 'Proteina B']

#Se limpian los datos, ya que pone la base de datos de donde viene la proteina ejem -> uniprot:nombre y solo queremos el nombre
defi = []
for i in intact['Proteina A']:
    lista = i.split(':')
    defi.append(lista[1])
intact['Proteina A'] = defi

defi2 = []
for i in intact['Proteina B']:
    lista = i.split(':')
    defi2.append(lista[-1])
intact['Proteina B'] = defi2

#A partir de aqui se vuelve al script 'base de datos' para no tener que estar cargando la base de datos cada vez que se ejecuta, importaremos el 
#data frame 'intact' y así no ocupamos la RAM del Pc, pero primero se guarda en un archivo
export_csv = intact.to_csv (r'interacciones_ninteracciones/n_PPI_intact.csv', index = None, header=True)