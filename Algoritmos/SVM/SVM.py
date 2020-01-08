#Lo primero de todo es obtener las secuencias que se habian guardado en Mongodb
import pandas as pd
import pymongo
from pymongo import MongoClient

#Se accede a Mongodb
mongo_uri = 'mongodb://localhost'  
client = MongoClient(mongo_uri)  #Lo llamamos client para poder conectarcon una db específica

def obtener_df_mongo(database, coleccion):
    db = client[database]
    collection = db[coleccion]

    results = collection.find()

    df = pd.DataFrame()
    contador = 0
    for r in results:
        if r['_id'] == 1:
            for clave in r.keys():
                df[clave] = []
            for cla, val in zip(df.columns.tolist(),r.values()):
                df[cla] = [val]
        else:
            val = list(r.values())
            df.loc[contador] = val
        contador += 1
    return(df)

AAC_uniprot = obtener_df_mongo('estudio_de_proteinas', 'AAC_uniprot')
print(1)
AAC_intact_negatome = obtener_df_mongo ('estudio_de_proteinas','AAC_intact_negatome')
print(1)
CTD_uniprot = obtener_df_mongo('estudio_de_proteinas', 'CTD_uniprot')
print(1)
CDT_intact_negatome = obtener_df_mongo('estudio_de_proteinas', 'CTD_intact_negatome')
print(1)
DPC_uniprot = obtener_df_mongo('estudio_de_proteinas', 'DPC_uniprot')
print(1)
DPC_intact_negatome = obtener_df_mongo('estudio_de_proteinas', 'DPC_intact_negatome')
print(1)
PAAC_uniprot = obtener_df_mongo('estudio_de_proteinas', 'PAAC_uniprot')
print(1)
PAAC_intact_negatome = obtener_df_mongo('estudio_de_proteinas', 'PAAC_intact_negatome')

import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix

#Lo primero es crear una función que permita reducir los pasos que se van a repetir en todas las bases de datos, para crear
#los distintos modelos
def preparacion_datos(df):
    
    #Lo primero de todo va a ser barajar los datos ya que se encuentran las interacciones arriba y las no interacciones abajo
    df = shuffle(df, random_state = 0)
    
    #Ahora se separan las columnas, por una parte se cogen todos los indicativos menos el id y los nombres de las proteinas
    #como 'X' y por otra parte el reultado de la interacción como 'Y'
    X = df.iloc[:,3:-1]
    Y = df.iloc[:,-1]
    
    #A continuación, se separan los datos en datos de entrenamiento y datos de test donde el 75% de los datos serán de entrenamiento
    x_train,x_test,y_train,y_test = train_test_split(X,Y, test_size = 0.25, random_state = 0)
    
    return(x_train,x_test,y_train,y_test)
    
x_train,x_test,y_train,y_test = preparacion_datos(AAC_uniprot)

#Ahora se estudia cuales serán los mejores parámetros, dentro de unos dados, para generar el modelo
parameters = {
    'kernel':['rbf'],
    'gamma':[1e-3,1e-2,0.1,0.2,0.3,0.4,0.5,0.6,1],
    'C':[10,100,1000,10000,50000,100000]
}
#Se realiza un k-fold cross validaton con una k = 10
clf = GridSearchCV(svm.SVC(decision_function_shape = 'ovr'), param_grid=parameters, cv = 10)
clf.fit(x_train,y_train)
clf.best_params_
#Se observa que los valores que mejor se ajustan a los datos son C = 50000 y gamma =0.1
y_pred = clf.predict(x_test)
mat = confusion_matrix(y_test, y_pred)
mat
#Se asignan valores
TP1 = mat[1][1]
TN1 = mat[0][0]
FP1 = mat[1][0]
FN1 = mat[0][1]

#Se crea un data frame donde se meten los resultados
resultados = pd.DataFrame({'Model':[],'Database':[],'Features':[],'Accuracy':[],'Precision':[],'Sensitivity':[],'Specifity':[], 'Matthews correlation coefficient':[],'F1 score':[]})

def evaluacion(TP,TN,FP,FN, modelo, bd, caract):
    accuracy =(TP+TN)/(TP+TN+FN+FP)
    precision = TP/(TP+FP)
    sensitivity = TP/(TP+FN)
    specifity = TN/(TN+FP)
    Mat = (TP*TN-FP*FN)/np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    F1 = 2*TP/(2*TP+FP+FN)
    
    r = [modelo,bd,caract,accuracy,precision,sensitivity,specifity,Mat,F1]
    resultados.loc[resultados.shape[0]] = r

evaluacion(TP1,TN1,FP1,FN1,'SVM','Uniprot','AAC')
resultados

x_train,x_test,y_train,y_test = preparacion_datos(AAC_intact_negatome)
#Ahora se estudia cuales serán los mejores parámetros, dentro de unos dados, para generar el modelo
parameters = {
    'kernel':['rbf'],
    'gamma':[1e-3,1e-2,0.1,0.2,0.3,0.4,0.5,0.6,1],
    'C':[10,100,1000,10000,50000,100000]
}
clf = GridSearchCV(svm.SVC(decision_function_shape = 'ovr'), param_grid=parameters, cv = 10)
clf.fit(x_train,y_train)
clf.best_params_
#Se observa que los valores que mejor se ajustan a los datos son C = 1000y gamma =1

y_pred = clf.predict(x_test)
mat = confusion_matrix(y_test, y_pred)
mat
#Se asignan valores
TP2 = mat[1][1]
TN2 = mat[0][0]
FP2 = mat[1][0]
FN2 = mat[0][1]

evaluacion(TP2,TN2,FP2,FN2,'SVM','Intact/Negatome', 'ACC')
resultados

x_train,x_test,y_train,y_test = preparacion_datos(DPC_uniprot)
#Ahora se estudia cuales serán los mejores parámetros, dentro de unos dados, para generar el modelo
parameters = {
    'kernel':['rbf'],
    'gamma':[1e-3,1e-2,0.1,0.2,0.3,0.4,0.5,0.6,1],
    'C':[10,100,1000,10000,50000,100000]
}
clf = GridSearchCV(svm.SVC(decision_function_shape = 'ovr'), param_grid=parameters, cv = 10)

clf.fit(x_train,y_train)
clf.best_params_
#Se observa que los valores que mejor se ajustan a los datos son C = 100 y gamma =0.5
y_pred = clf.predict(x_test)
mat = confusion_matrix(y_test, y_pred)
mat
#Se asignan valores
TP3 = mat[1][1]
TN3 = mat[0][0]
FP3 = mat[1][0]
FN3 = mat[0][1]

evaluacion(TP3,TN3,FP3,FN3,'SVM','Uniprot','DPC')
resultados

x_train,x_test,y_train,y_test = preparacion_datos(DPC_intact_negatome)
#Ahora se estudia cuales serán los mejores parámetros, dentro de unos dados, para generar el modelo
parameters = {
    'kernel':['rbf'],
    'gamma':[1e-5,1e-4,1e-3,1e-2,0.1,0.2,0.3,0.4,0.5],
    'C':[10,100,1000,10000,50000,100000]
}
clf = GridSearchCV(svm.SVC(decision_function_shape = 'ovr'), param_grid=parameters, cv = 10)

clf.fit(x_train,y_train)
clf.best_params_
#Se observa que los valores que mejor se ajustan a los datos son C = 50000 y gamma =0.001
y_pred = clf.predict(x_test)
mat = confusion_matrix(y_test, y_pred)
mat
#Se asignan valores
TP4 = mat[1][1]
TN4 = mat[0][0]
FP4 = mat[1][0]
FN4 = mat[0][1]
evaluacion(TP4,TN4,FP4,FN4,'SVM','Intact/Negatome','DPC')
resultados

x_train,x_test,y_train,y_test = preparacion_datos(CTD_uniprot)
#Ahora se estudia cuales serán los mejores parámetros, dentro de unos dados, para generar el modelo
parameters = {
    'kernel':['rbf'],
    'gamma':[1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,0.1],
    'C':[1,5,10,100,1000]
}
clf = GridSearchCV(svm.SVC(decision_function_shape = 'ovr'), param_grid=parameters, cv = 10)

clf.fit(x_train,y_train)
clf.best_params_
#Se observa que los valores que mejor se ajustan a los datos son C = 100 y gamma =0.0001

y_pred = clf.predict(x_test)
mat = confusion_matrix(y_test, y_pred)
mat
#Se asignan valores
TP5 = mat[1][1]
TN5 = mat[0][0]
FP5 = mat[1][0]
FN5 = mat[0][1]
evaluacion(TP5,TN5,FP5,FN5,'SVM','Uniprot','CTD')
resultados

x_train,x_test,y_train,y_test = preparacion_datos(CDT_intact_negatome)
#Ahora se estudia cuales serán los mejores parámetros, dentro de unos dados, para generar el modelo
parameters = {
    'kernel':['rbf'],
    'gamma':[1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,0.1],
    'C':[0.5,1,5,10,100,1000]
}
clf = GridSearchCV(svm.SVC(decision_function_shape = 'ovr'), param_grid=parameters, cv = 10)

clf.fit(x_train,y_train)
clf.best_params_
#Se observa que los valores que mejor se ajustan a los datos son C = 5 y gamma =0.001

y_pred = clf.predict(x_test)
mat = confusion_matrix(y_test, y_pred)
mat
#Se asignan valores
TP6 = mat[1][1]
TN6 = mat[0][0]
FP6 = mat[1][0]
FN6 = mat[0][1]
evaluacion(TP6,TN6,FP6,FN6,'SVM','Intact/Negatome','CTD')
resultados  

x_train,x_test,y_train,y_test = preparacion_datos(PAAC_uniprot)
#Ahora se estudia cuales serán los mejores parámetros, dentro de unos dados, para generar el modelo
parameters = {
    'kernel':['rbf'],
    'gamma':[1e-5,1e-4,1e-3,1e-2,0.1,0.2,0.3],
    'C':[0.1,1,10,100,1000,10000]
}
clf = GridSearchCV(svm.SVC(decision_function_shape = 'ovr'), param_grid=parameters, cv = 10)

clf.fit(x_train,y_train)
clf.best_params_
#Se observa que los valores que mejor se ajustan a los datos son C = 10 y gamma =0.001

y_pred = clf.predict(x_test)
mat = confusion_matrix(y_test, y_pred)
mat
#Se asignan valores
TP7 = mat[1][1]
TN7 = mat[0][0]
FP7 = mat[1][0]
FN7 = mat[0][1]
evaluacion(TP7,TN7,FP7,FN7,'SVM','Uniprot','PAAC')
resultados

x_train,x_test,y_train,y_test = preparacion_datos(PAAC_intact_negatome)
#Ahora se estudia cuales serán los mejores parámetros, dentro de unos dados, para generar el modelo
parameters = {
    'kernel':['rbf'],
    'gamma':[1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,0.1,1],
    'C':[1,5,10,100]
}
clf = GridSearchCV(svm.SVC(decision_function_shape = 'ovr'), param_grid=parameters, cv = 10)

clf.fit(x_train,y_train)
clf.best_params_
#Se observa que los valores que mejor se ajustan a los datos son C = 1 y gamma =0.01
y_pred = clf.predict(x_test)
mat = confusion_matrix(y_test, y_pred)
mat
#Se asignan valores
TP8 = mat[0][0]
TN8 = mat[1][1]
FP8 = mat[0][1]
FN8 = mat[1][0]
evaluacion(TP8,TN8,FP8,FN8,'SVM','Intact/Negatome','PAAC')
resultados

#Por último, se exporta la tabla de resultados
export_csv = resultados.to_excel(r'resultados.xlsx', index = None, header=True)