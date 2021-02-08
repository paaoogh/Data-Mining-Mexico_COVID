import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import requests
import seaborn as sns
 
repo_url = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json" #archivo GeoJson

st.title("COVID-19 MEXICO DATA")
st.sidebar.title("Menu")

@st.cache(persist=True)

def load_data():
    data = pd.read_csv("210124COVID19MEXICO.csv")
    data['FECHA_INGRESO'] = pd.to_datetime(data['FECHA_INGRESO'])
    return data

#data = load_data()
st.markdown("Ésta es una aplicación de Streamlit donde se pueden observar varios datos acerca del COVID-19 en México. Los datos se encuentran en la página [oficial de datos abiertos del gobierno](https://datos.covid-19.conacyt.mx/#DownZCSV)")


#___________Casos por estado_________
st.subheader("Casos por estado")
st.sidebar.subheader("Casos por estado")
datos = pd.read_csv("CasosMex.csv")

@st.cache(persist=True)
def plot_casos(estado):
    df = datos[datos['Estado']==estado]
    count = df['Estado']
    casos = df["Casos"]
    count = pd.DataFrame({'Estado':count, 'Casos':casos})
    return count

estados = st.sidebar.multiselect("Selección de estados a desplegar", (datos.Estado))
elegidos = datos[datos.Estado.isin(estados)].drop(["latitude","longitude","CasosMex"],axis=1)
if len(estados)>0:
    breakdown_type = st.sidebar.selectbox('Tipo de visualización', ['Bar plot', 'Chart'], key='3')
    fig_3 = make_subplots(rows=1, cols=len(estados), subplot_titles=datos.Estado)
    if breakdown_type == 'Bar plot':
        for i in range(1):
            for j in range(len(estados)):
                fig_3.add_trace(
                    go.Bar(x=plot_casos(estados[j]).Estado, y=plot_casos(estados[j]).Casos, showlegend=False),
                    row=i+1, col=j+1
                )
        fig_3.update_layout(height=600, width=800)
        st.plotly_chart(fig_3)
    else:
        st.dataframe(elegidos)
    

#_____________Afectaciones de salud________________________-
st.subheader("Complicaciones de salud en México")
st.sidebar.subheader("Complicaciones y/o estados de salud nacionales")
st.sidebar.markdown("Situaciones que pueden poner en riesgo a la vida de las personas en caso de contraer virus.")
choice = st.sidebar.multiselect("Seleccionar afecciones o estados de salud",("NEUMONIA","EMBARAZO","DIABETES","EPOC","ASMA", 
                                                                            "INMUNOSUPR","HIPERTENSION","HIPERTENSION","OTRO_CASO",
                                                                           "CARDIOVASCULAR", "OBESIDAD", "TABAQUISMO","RENAL_CRONICA") )
afectaciones = {'NEUMONIA': [8.32, 82.9, 8.69],'EMBARAZO': [0.76, 50.9,48.3],
                'DIABETES': [9.62, 80.51, 9.85],'EPOC': [0.99, 97.77, 1.22],
                'ASMA': [2.45, 94.86, 2.67],
                'INMUNOSUPR': [0.9, 97.95, 1.14],'HIPERTENSION': [12.55, 74.68, 12.76],
                'OTRO_CASO': [31.42, 32.49, 36.08],'CARDIOVASCULAR': [1.47, 96.81, 1.70],
                'OBESIDAD': [11.28, 77.23, 11.48], 'TABAQUISMO': [7.60, 84.56, 7.82],
                'RENAL_CRONICA': [1.35, 97.05, 1.58]}
afecta = pd.DataFrame(afectaciones.values(), index = afectaciones.keys(), columns = ["positivo","negativo","otro"])

if len(choice)>0:
    breakdown_type = st.sidebar.selectbox('Tipo de visualización', ['Bar plot', 'Chart'], key='4')
    fig_4 = make_subplots(rows=1, cols=len(choice), subplot_titles=afecta.index)
    choice_data = afecta[afecta.index.isin(choice)]
    if breakdown_type == 'Bar plot':
        fig_choice = px.histogram(choice_data, x=choice_data.index, y=[choice_data.negativo,choice_data.positivo,choice_data.otro],
        barmode="group",height=500,width=800)
        fig_choice.update_layout(
            title_text='Afectaciones de salud', # title of plot
            xaxis_title_text='Enfermedades', # xaxis label
            yaxis_title_text='Casos', # yaxis label
            bargap=0.2, # gap between bars of adjacent location coordinates
            bargroupgap=0.1 # gap between bars of the same location coordinates
        )
        st.plotly_chart(fig_choice)

    elif breakdown_type == "Chart":
        st.dataframe(choice_data)



#_________________Visualizar datos________________
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.sidebar.subheader("Visualizar datos")
st.subheader("Visualizandod datos con reducción de dimensionalidad")
st.markdown("De poder tomar y plasmar los datos, se podrían ver algo así:")

breakdown_type = st.sidebar.selectbox('Dimensiones', [3, 2], key='5')
if breakdown_type==3:
    data_ = pd.read_csv("Mexico3d.csv")
    data_cm = pd.read_csv("CDMX3d.csv")
    data_mor = pd.read_csv("Morelia3d.csv")
    sns.set(style = "darkgrid")
    fig = plt.figure(figsize=(10,20),)
    ax = fig.add_subplot(311, projection = '3d')
    x = data_['x']
    y = data_['y']
    z = data_['z']
    ax.scatter(x, y, z)

    ax2 = fig.add_subplot(312, projection = '3d')
    x = data_cm['x']
    y = data_cm['y']
    z = data_cm['z']
    ax2.scatter(x, y, z)

    ax3 = fig.add_subplot(313, projection = '3d')
    x = data_mor['x']
    y = data_mor['y']
    z = data_mor['z']
    ax3.scatter(x, y, z)
    ax.title.set_text('México (país)')
    ax2.title.set_text('Ciudad de México')
    ax3.title.set_text('Morelia')
    st.pyplot(fig)

elif breakdown_type==2:
    data_ = pd.read_csv("Mexico2d.csv")
    data_cm = pd.read_csv("CDMX2d.csv")
    data_mor = pd.read_csv("Morelia2d.csv")
    sns.set(style = "darkgrid")
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(311)
    ax.scatter(x=data_['x'], y=data_['y'])

    ax2 = fig.add_subplot(312)
    ax2.scatter(x=data_mor['x'], y=data_mor['y'])

    ax3 = fig.add_subplot(313)
    ax3.scatter(x=data_cm['x'], y=data_cm['y'])
    ax.title.set_text('México (país)')
    ax2.title.set_text('Ciudad de México')
    ax3.title.set_text('Morelia')
    st.pyplot(fig)
