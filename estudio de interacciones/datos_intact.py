import pandas as pd

#Se importan los datos que se han descargado desde Intact
datos = pd.read_csv('intact/intact.txt', sep = '\t', encoding= 'utf8')

#Se cogen las 2 primeras columnas que corresponden a las asociaciones
intact = datos.iloc[:,0:2]
intact.columns = ['interactor A', 'interactor B']
#Se limpian los datos, ya que pone la base de datos de donde viene la proteina ejem -> uniprot:nombre y solo queremos el nombre
defi = []
for i in intact['interactor A']:
    lista = i.split(':')
    defi.append(lista[1])
intact['interactor A'] = defi

defi2 = []
for i in intact['interactor B']:
    lista = i.split(':')
    defi2.append(lista[-1])
intact['interactor B'] = defi2
#A partir de aqui se vuelve al script 'base de datos' para no tener que estar cargando la base de datos cada vez que se ejecuta, importaremos el 
#data frame 'intact' y así no ocupamos la RAM del Pc, pero primero se guarda en un archivo
export_csv = intact.to_csv (r'intact/intact.csv', index = None, header=True)






