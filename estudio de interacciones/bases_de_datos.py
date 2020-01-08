#Se descarga a partir del apartado ‘summary of gen-disease associations’ de la página http://www.disgenet.org los datos y se guardan como 
import pandas as pd

descarga = pd.read_excel('Genes_Alzheimer.xlsx')

#Una vez se tienen cargados los datos, se procede a obtener una lista con el nombre de todas las proteinas involucradas

prot = descarga['UniProt'] 

print(len(prot))
print(prot.describe())
#tras una primera observación de los datos, se observa que existen datos omitidos ('prot' presenta 1981 elementos, mientras que 1979 son valores)
#que se corresponen con RNAs no codificantes (microRNA, lncodRNAs) y genes que no se han obtenido proteina todavía. Por lo tanto, se eliminan los ausentes
#y los repetidos

prot = prot.dropna().unique().tolist()

#Se observa que existen varias proteinas dentro de un mismo elemento dentro de la lista y estos se separan con el caracter ';' por lo que se 
#separan y despues de meten en una lista definitiva

proteinas= []
for p in prot:
    p = p.split(';')
    for i in p:
        proteinas.append(i)

#Ahora se tiene una lista con el nombre de todas las proteinas relacionadas con el Alzheimer

#Se importa el archivo de datos intact que previamente se ha obtenido en el script 'datos_inctat' para rellenar el diccionario PPI
intact = pd.read_csv('intact/intact.csv', sep = ',')

#Se eliminan las filas donde se repiten las proteinas de la 1 columna de las obtenidas en la base de datos intact
intact.drop_duplicates(subset ="interactor A", inplace = True)

#Se crea un diccionario donde se meterán las proteinas del data frame 'intact' que coincidan con elementos de la lista 'proteinas', siendo 
#las claves aquellas proteinas relacionadas con la enfermedad y los valores las proteinas con las que interaccionan.

PPI_dic = {}

for a, b in zip(intact['interactor A'], intact['interactor B']):
    for val in proteinas:
        if val == a:
            PPI_dic[a]=b
#El diccionario PPI contiene las proteinas que interaccionan
#El siguiente paso es seguir el mismo procedimiento para aquellas proteinas que no interaccionan.

#Ahora se realiza el mismo procedimiento en 'datos_intact_nppi' para las proteinas que no interaccionan. En este caso se cogen todas y no se
#eliminan las repetidas ya que hay poco mas de 950 registros entonces de los cuales solo 50 coinciden con nuestras proteinas de interés
intact_nppi = pd.read_csv('intact/intact_nppi.csv', sep = ',')

n_PPI_intact_dic ={} #finalmente se quedan en 430 ya que no pueden haber elementos repetidos en las claves del diccionario

for p1, p2 in zip(intact_nppi['interactor A'],intact_nppi['interactor B']): 
    n_PPI_intact_dic[p1]=p2

#Ahora se cargan los datos de la otra base de datos de interaccion negativa, es decir, descargada de negatome
negatome = pd.read_csv('negatome/negatome.csv', sep=',')

n_PPI_negatome_dic = {}

for p1, p2 in zip(negatome['interactor A'],negatome['interactor B']):
    n_PPI_negatome_dic[p1]=p2

#A continuación se vuelve a repetir el proceso con la base de datos de Uniprot, de esta forma se eliminan posibles elementos repetidos
uniprot = pd.read_csv('uniprot/uniprot.csv', sep=',')

n_PPI_uniprot_dic = {}

for p1, p2 in zip(uniprot['Proteina A'],uniprot['Proteina B']):
    n_PPI_uniprot_dic[p1]=p2 #Una vez eliminadas las proteinas repetidas se nos quedan un total de 1101 proteinas que no interaccionan

#por último, se va a generar un diccionario para filtrar que no se repitan claves a la hora de juntar los datos de negatome y de intact que son negativos
#Para así tener 4 variables a comparar en el futuro modelo
n_PPI_intact_negatome_dic ={} #finalmente se quedan en 430 ya que no pueden haber elementos repetidos en las claves del diccionario

for p1, p2 in zip(negatome['interactor A'],negatome['interactor B']):
    n_PPI_intact_negatome_dic[p1]=p2 #Se añaden primero los datos de negatome al diccionario
    
for p1, p2 in zip(intact_nppi['interactor A'],intact_nppi['interactor B']): 
    n_PPI_intact_negatome_dic[p1]=p2 #Y después los de negatome



#Para poder manejar los datos, se pasan a data frame, este data frame constará de una columna llamada 'Proteina A' y otra 'Proteina B'
def dic_df_exportar(diccionario,ruta):
    df= pd.DataFrame(columns=['Proteina A','Proteina B'])
    df['Proteina A'] = diccionario.keys()
    df['Proteina B'] = diccionario.values()
    df.to_csv(ruta, index = None, header=True)



dic_df_exportar(PPI_dic,r'interacciones_ninteracciones/PPI.csv')
dic_df_exportar(n_PPI_intact_dic,r'interacciones_ninteracciones/n_PPI_intact.csv')
dic_df_exportar(n_PPI_negatome_dic,r'interacciones_ninteracciones/n_PPI_negatome.csv')
dic_df_exportar(n_PPI_intact_negatome_dic,r'interacciones_ninteracciones/n_PPI_intact_negatome.csv')
dic_df_exportar(n_PPI_uniprot_dic,r'interacciones_ninteracciones/n_PPI_uniprot.csv')