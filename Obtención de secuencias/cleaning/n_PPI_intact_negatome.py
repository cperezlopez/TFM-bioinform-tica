import pandas as pd

#En primer lugar cargo los datos
n_PPI_intact_negatome = pd.read_csv(r'../../estudio de interacciones/interacciones_ninteracciones/n_PPI_intact_negatome.csv')

#A continuacion, elimino aquellos que tengan un guión, ya que producen problemas en las busquedas
lista =[]
for n in range(len(n_PPI_intact_negatome)):
    for l in n_PPI_intact_negatome.iloc[n,1]:
        if l == '-':
            lista.append(n)
for n in range(len(n_PPI_intact_negatome)):
    for l in n_PPI_intact_negatome.iloc[n,0]:
        if l == '-':
            lista.append(n)
lista = set(lista)
n_PPI_intact_negatome = n_PPI_intact_negatome.drop(lista, axis = 0)

#Genero un csv con el resultado
n_PPI_intact_negatome.to_csv(r'n_PPI_intact_negatome.csv', index = None, header=True)

#Ahora lo vuelvo a cargar para que se reseteen los id y no de error al correrlo
n_PPI_intact_negatome = pd.read_csv(r'n_PPI_intact_negatome.csv')

#Se eliminan una serie de ids que dan error, algunos de los que se eliminan no dan error, pero se encuentran en zonas donde muchos si dan error
eliminar = [24, 38,  121,  186,  250,  294,  297,  345,  347,  370,  373,  392,  431,  447,  448,  457,  506,  518,  1124,  1133,  1138,  1139,  1185,  1186,  224,  253,  277,  297,  378,  398,  402,  406,  447,  448,  466,  545,  564,  697,  731,  941, 1048,  1049,  1050,  1051,  1052,  1053,  1054,  1055,  1056,  1057,  1058,  1059,  1060,  1061,  1062,  1063,  1064,  1065,  1066,  1067,  1068,  1069,  1070,  1071,  1072,  1073,  1074,  1075,  1076,  1077,  1078,  1079,  1080,  1081,  1082,  1083,  1084,  1085,  1086,  1087,  1088,  1089,  1090,  1091,  1092,  1093,  1094,  1095,  1096,  1097,  1098,  1099,  1100,  1101,  1102,  1103,  1104,  1105,  1106,  1107,  1108,  1109,  1110,  1111,  1112,  1113,  1114,  1115,  1116,  1117,  1118,  1119,  1120,  1121,  1122,  1123,  1124,  1125,  1126,  1127,  1128,  1129,  1130,  1131,  1132,  1133,  1134,  1135,  1136,  1137,  1138,  1139,  1140,  1141,  1142,  1143,  1144,  1145,  1146,  1147,  1148,  1149,  1150,  1151,  1152,  1153,  1154,  1155,  1156,  1157,  1158,  1159,  1160,  1161,  1162,  1163,  1164,  1165,  1166,  1167,  1168,  1169,  1170,  1171,  1172,1173]
n_PPI_intact_negatome = n_PPI_intact_negatome.drop(eliminar, axis = 0)

#Se vuelve a guardar ya con todos los datos de consulta correctos
n_PPI_intact_negatome.to_csv(r'../cleaning_2/n_PPI_intact_negatome_c.csv', index = None, header=True) #Se queda en 1033 datos, suficientes