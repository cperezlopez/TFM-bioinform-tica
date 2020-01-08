#Al hacer las consultas de secuencias, se ha visto que algunas proteinas dan error, tanto las que tienen el caracter '-' como algunas que no 
#encuentran consulta. Por ello, se lleva un proceso de cleaning de todas estas proteinas
import pandas as pd 

#Se cargan los datos PPI 
PPI = pd.read_csv(r'../../estudio de interacciones/interacciones_ninteracciones/PPI.csv')

#En primer, se eliminan determinadas posiciones que dan error de busqueda
eliminar = [269-2,270-2,708-2,938-2,1040-2,1071-2,1072-2,1074-2,1076-2,1079-2,1083-2,1084-2,1087-2,1088-2,1090-2,1091-2,1094-2,1096-2,1097-2,1098-2,1103-2,1105-2,1107-2,1118-2,1120-2,1123-2,1124-2,1130-2,1131-2,1133-2,1136-2,1176-2,1311-2,1397-2]

PPI = PPI.drop(eliminar, axis = 0)
PPI.to_csv('PPI.csv', index = None, header=True)

#Ahora se vuelven a cargar los datos para que se reseteen los 'id' y poder seguir con el cleaning
PPI = pd.read_csv('PPI.csv')
lista =[]
for n in range(len(PPI)):
    for l in PPI.iloc[n,1]:
        if l == '-':
            lista.append(n)
for n in range(len(PPI)):
    for l in PPI.iloc[n,0]:
        if l == '-':
            lista.append(n)
lista = set(lista)
PPI = PPI.drop(lista, axis = 0)

PPI.to_csv(r'../cleaning_2/PPI_c.csv', index = None, header=True)