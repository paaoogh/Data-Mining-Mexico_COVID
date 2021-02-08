import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from mlxtend.preprocessing import TransactionEncoder
import mlxtend.frequent_patterns as fp
import sklearn
from sklearn.decomposition import PCA

estado_casos={ 1:"AGUASCALIENTES",2:"BAJA CALIFORNIA",3:"BAJA CALIFORNIA SUR",4:"CAMPECHE",5:"COAHUILA DE ZARAGOZA",6:"COLIMA",7:"CHIAPAS",8:"CHIHUAHUA",9:"CIUDAD DE MÉXICO",
            10:"DURANGO",11:"GUANAJUATO",12:"GUERRERO",13:"HIDALGO",14:"JALISCO",15:"MÉXICO",16:"MICHOACÁN DE OCAMPO",17:"MORELOS",18:"NAYARIT",19:"NUEVO LEÓN",
            20:"OAXACA",21:"PUEBLA",22:"QUERÉTARO",23:"QUINTANA ROO",24:"SAN LUIS POTOSÍ",25:"SINALOA",26:"SONORA", 27:"TABASCO",28:"TAMAULIPAS",29:"TLAXCALA",
            30:"VERACRUZ DE IGNACIO DE LA LLAVE",31:"YUCATÁN",32:"ZACATECAS",99:'No'}
#casos = pd.DataFrame(lista.values(), index=lista.keys(), columns=["Estado","Casos"]).to_csv("CasosMex.csv")

columnas2 = ["ORIGEN","SECTOR","ENTIDAD_UM","SEXO","ENTIDAD_NAC","ENTIDAD_RES",
            "MUNICIPIO_RES","TIPO_PACIENTE","FECHA_INGRESO","INTUBADO","NEUMONIA","EDAD",
            "NACIONALIDAD","EMBARAZO","HABLA_LENGUA_INDIG","INDIGENA","DIABETES","EPOC","ASMA","INMUSUPR",
            "HIPERTENSION","OTRA_COM","CARDIOVASCULAR","OBESIDAD","RENAL_CRONICA","TABAQUISMO","OTRO_CASO",
             "TOMA_MUESTRA_LAB","RESULTADO_LAB","TOMA_MUESTRA_ANTIGENO", "RESULTADO_ANTIGENO","CLASIFICACION_FINAL",
            "UCI"]
datos_hoy = pd.read_csv("210124COVID19MEXICO.csv", usecols = columnas2)
datos_hoy['FECHA_INGRESO'] = pd.to_datetime(datos_hoy['FECHA_INGRESO'])
X = datos_hoy[(datos_hoy['FECHA_INGRESO'] > '2020-12-20 00:00:00')]
X.drop(['FECHA_INGRESO'], axis=1,inplace=True)

Mor = X[X["ENTIDAD_UM"]==16]
CM = X[X["ENTIDAD_UM"]==9]

print("3d1")
pca = PCA(n_components=2, svd_solver='arpack', random_state=42)
Data = pca.fit_transform(X)
print("3d2")
pca2 = PCA(n_components=2, svd_solver='arpack', random_state=42)
data_CM = pca2.fit_transform(CM)
print("3d3")
pca3 = PCA(n_components=2, svd_solver='arpack', random_state=42)
data_mor = pca3.fit_transform(Mor)
df1 = pd.DataFrame(data=Data, columns=["x","y"]).to_csv("Mexico2d.csv")
df2 = pd.DataFrame(data=data_CM, columns=["x","y"]).to_csv("CDMX2d.csv")
df3 = pd.DataFrame(data=data_mor, columns=["x","y"]).to_csv("Morelia2d.csv")

print("2d1")
pca = PCA(n_components=3, svd_solver='arpack', random_state=42)
Data = pca.fit_transform(X)
print("2d2")
pca2 = PCA(n_components=3, svd_solver='arpack', random_state=42)
data_CM = pca2.fit_transform(CM)
print("2d3")
pca3 = PCA(n_components=3, svd_solver='arpack', random_state=42)
data_mor = pca3.fit_transform(Mor)
df1 = pd.DataFrame(data=Data, columns=["x","y","z"]).to_csv("Mexico3d.csv")
df2 = pd.DataFrame(data=data_CM, columns=["x","y","z"]).to_csv("CDMX3d.csv")
df3 = pd.DataFrame(data=data_mor, columns=["x","y","z"]).to_csv("Morelia3d.csv")
