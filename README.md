# Análise de entregas realizadas nas cidades

![icons8-numpy-48](https://github.com/user-attachments/assets/c065f2b2-6afc-44fd-8e76-5585356ab023)
![icons8-pandas-logo-48](https://github.com/user-attachments/assets/092de3ff-0722-4e5d-b066-1f144a79a94b)
![icons8-python-48](https://github.com/user-attachments/assets/91d530a0-e841-45ce-a5fe-ca52dac31918)
![image](https://github.com/user-attachments/assets/3e86e878-4eb5-4059-8c1e-31d37a168b63)
#
## Observação!!
Esta análise somente é focada nas informações referentes ao comportamento das entregas, para obter insights e entender a dinâmica das entregas, com objetivo para somar com outras análises.  
#
Objetivo:

Analisar o impacto das condições nas rotas de entrega, identificando padrões e propondo soluções para otimizar as operações em diferentes cenários e climáticos.

# 

Dados:

Dados de pedidos: Data, hora, origem, destino, tipo da entrega, localidade dos pedidos.

Dados meteorológicos: Temperatura, condições do tempo.

Dados de frota: Tipo  e condições dos veículos.

Dados dos restaurantes: localidade dos restaurantes.



#

Ferramentas:

Bibliotecas: Pandas, Streamlit, Haversine, Plotly.

Python: Para extração, limpeza e manipulação do dataset.


    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    df1['Time_Orderd'] = pd.to_datetime(df1['Time_Orderd'])

    df1['Time_Order_picked'] = pd.to_datetime(df1['Time_Order_picked'])

    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

#

Limpeza e preparação dos dados:

Remoção e verificação de valores faltantes no dataset .

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

#
Análise exploratória:

Visualização da distribuição das entregas por dia, semana, horário, cidades por tráfego e por lacalização central das cidades.

    df_aux1 = df1.loc[:,['ID', 'week_of_year']].groupby(['week_of_year']).count().reset_index()
    df_aux2 = df1.loc[:,['Delivery_person_ID', 'week_of_year']].groupby(['week_of_year']).nunique().reset_index()
    
    df_aux = pd.merge(df_aux1, df_aux2, how='inner', on='week_of_year')
    df_aux['Orde_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    
    px.line( df_aux, x='week_of_year', y='Orde_by_deliver')
    
![image](https://github.com/user-attachments/assets/e088032d-1fff-4d1f-8d9c-36bfb8145627)

Análise da correlação entre as variáveis climáticas e o tempo de entrega.
#

Descobertas:

Os pedidos sofrem diretamente sobre a influência do aumeno do trânsito nos centros.

Os pedidos apresentam altas variações no início do mês.

A temperatura influencia diretamente no consumo de combustível dos veículos.

Visualizações:

Mapa mostrando as regiões, com as localidades onde os pedidos foram realizados.

![image](https://github.com/user-attachments/assets/99da7c1e-eae3-4c0f-a334-8929f2190087)

Gráfico de pizza comparando a porcentagem de entrega de acordo com o tráfego.

![image](https://github.com/user-attachments/assets/029f6072-3134-4ba3-b9a6-2fb914fb131f)

#
Recomendações:

Desenvolver rotas alternativas para evitar áreas com alta probabilidade de trânsito.
    
Utilização de sistema de alerta para notificar os motoristas sobre condições de tráfego intenso.

Otimizar a capacidade dos veículos para reduzir o consumo de combustível e agilizar as entregas.


#
Próximos passos:

Verificação de sazonalidades para realizar uma previsão de entregas.
    
Incorporar dados históricos de acidentes para identificar rotas mais seguras.

Explorar técnicas de machine learning mais avançadas para melhorar a precisão das previsões.

#
Para uma visão mais detalhada dos gráficos, sugiro colar o link abaixo no URL do navegador, pois apresento outros gráficos construidos. 

    http://192.168.0.28:8502
