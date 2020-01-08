#Se sigue el mismo codigo que en 'datos_intact'
import pandas as pd

datos = pd.read_csv('negatome/negatome.txt', sep = '\t', encoding= 'utf8')

#Se cogen las 2 primeras columnas y se les pone ese nombre
negatome = datos.iloc[:,0:2]
negatome.columns = ['interactor A', 'interactor B']

#En este caso no sale la referencia de la base de datos de donde se ha obtenido la proteina, por lo que el siguiente paso no es necesario
#A partir de aqui se vuelve al script 'base de datos' para no tener que estar cargando la base de datos cada vez que se ejecuta, importaremos el 
#data frame 'negatome' y así no ocupamos la RAM del Pc, pero primero se guarda en un archivo
export_csv = negatome.to_csv (r'negatome/negatome.csv', index = None, header=True)