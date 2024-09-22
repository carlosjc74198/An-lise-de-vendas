import pandas as pd
import numpy as np	
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
from PIL import Image


#========================
# Importing the dataset
#========================

df = pd.read_csv('C:/Users/carlo/Desktop/Machine Learning/Machine Learning/train2.csv')

#================================
# criando uma cópia do dataframe
# Create a copy of the dataframe
#================================

df1 = df.copy()

#=================================
# limpa a coluna que contém 'NaN'
# Clean the column that contains 'NaN'
#=================================

linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN ' 
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = df1['Road_traffic_density'] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = df1['City'] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = df1['Festival'] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
df1 = df1.loc[linhas_selecionadas, :].copy()

#====================================
# Convertendo o formato das colunas
# Convert the format of the columns
#====================================

df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

df1['Time_Orderd'] = pd.to_datetime(df1['Time_Orderd'])

df1['Time_Order_picked'] = pd.to_datetime(df1['Time_Order_picked'])

df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

#===================================================
# Removendo espaços dentro dos dados da tabela.
# Removing spaces inside the data table.
#===================================================

df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[: , 'City'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

# Cleaning time taken column
#Limpando a coluna de Time_taken
df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
df1['Time_taken(min)'] =df1['Time_taken(min)'].str.strip(int)

#===============================
# Barra lateral no Streamlit
# Sidebat on Streamlit
#===============================

st.header(' Markplace - Visão Empresa', divider=True)

image_path = 'C:/Users/carlo/Pictures/streamlit-logo-primary-lightmark-lighttext.png'
image = Image.open(image_path)
st.sidebar.image(image, width=200)


st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## (Ifood Índia)')
st.sidebar.markdown('## Entrega mais rápida na cidade')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

# Filter by date
# filtro de data
date_slider = st.sidebar.slider(
    'Até qual data deseja analisar?',
    value = dt.datetime(2022, 4, 13),
    min_value = dt.datetime(2022, 2, 11), # Data minima do dataframe
    max_value = dt.datetime(2022, 4, 6), # Data maxima do dataframe
	format="DD/MM/YYYY",
)
st.write("Data: " , date_slider)

st.header(date_slider, divider=True)
st.sidebar.markdown("""---""")

# Filter by traffic
# Filtra por transito
traffic_options = st.sidebar.multiselect('Quais as condições do trânsito',
                                         ['Low', 'Medium', 'High', 'Jam'],
                                         default=['Low', 'Medium', 'High', 'Jam',])

st.sidebar.markdown("""---""") 
st.sidebar.markdown('### By José Carlos Carneiro')

# Filtering date
# Filtro por data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtering traffic
# Filtro por transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#================================
# Layout no Streamlit
#Lauyout on Streamlit
#================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])
#--------------------------------------
# Primeira aba
# First tab
#--------------------------------------
with tab1:
    with st.container():
        st.markdown('''## :blue[Pedidos por Data]''') # criando um título com cor azul
        coluna = ['ID', 'Order_Date']
        #Seleção de linhas
        df_aux = df1.loc[:, coluna].groupby('Order_Date').count().reset_index()        # Desenhando o gráfico de linhas
        fig = px.bar(df_aux, x = 'Order_Date', y = 'ID')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""---""")

    with st.container():
        #Quantidade pedidos por semana
        with st.container():
            st.header(''' :blue[Pedidos por Semana]''')
            df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
            df_aux = df1.loc[:,['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
            fig = px.line(df_aux, x = 'week_of_year', y = 'ID')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""---""")

    with st.container():
        st.header(''':blue[Pedidos por Tipo de Tráfego]''')
        #Distribuição dos pedidos por tipo de tráfego.
        df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby(['Road_traffic_density']).count().reset_index()
        df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
        fig = px.pie(df_aux, values= 'entregas_perc', names='Road_traffic_density', color='Road_traffic_density',
             color_discrete_map={'Low':'lightblue',
                                 'Jam': 'cyan', 
                                 'Medium': 'royalblue',
                                 'High': 'darkblue'})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""---""")

    with st.container():
    # Comparação do volme de pedidos por cidade e tipo de tráfego.
        st.header(''' :blue[Pedidos por Cidade e Tipo de Tráfego]''')
        df_aux = (df1.loc [:, ['ID', 'City', 'Road_traffic_density']].groupby([ 'City', 'Road_traffic_density'])
                                                                     .count()
                                                                     .reset_index())
        fig = px.scatter(df_aux, x= 'City', y= 'Road_traffic_density', 
                         size='ID', 
                        symbol='City')
        fig.update_traces(marker_size=30)
        fig.update_layout(scattermode ="group")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("""---""")

#--------------------------------
# Segunda aba
# Second tab
#--------------------------------
with tab2:
    with st.container():
        st.header(''' :blue[Pedidos por Cidade]''')
        df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')

        df_aux = df1.loc[:,['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
        fig = px.line(df_aux, x = 'week_of_year', y = 'ID')
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("""---""")
    with st.container():
        st.header(''' :blue[Pedidos por Semana]''')
        df_aux1 = df1.loc[:,['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
        df_aux2 = df1.loc[:,['Delivery_person_ID', 'week_of_year']].groupby(['week_of_year']).nunique().reset_index()
        df_aux = pd.merge(df_aux1, df_aux2, how='inner', on='week_of_year')
        df_aux['Orde_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

        fig = px.line( df_aux, x='week_of_year', y='Orde_by_deliver')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")
#--------------------------------
# Terceira aba
# Third tab
#--------------------------------
with tab3:
    with st.container():
        st.header(''' :blue[Pedidos por Cidade]''')
        fig = px.scatter_mapbox(df1, 
                        lat="Delivery_location_latitude", 
                        lon="Delivery_location_longitude",
                        hover_name="City",
                        hover_data=["Road_traffic_density"],
                        zoom=3,
                        height=500)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
st.markdown("""---""")




# Para abrir o streamlit, basta executar o seguinte comando.
# streamlit run "C:\Users\carlo\Desktop\Python_piva\visao_empresa.py"
