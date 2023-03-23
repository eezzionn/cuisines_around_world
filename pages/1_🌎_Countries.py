# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
from plotly.subplots import make_subplots
# bibliotecas necessárias
import folium
import pandas as pd
import numpy as np
import math
import inflection
import streamlit as st
import re
import csv
import math
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from PIL import Image
from datetime import datetime 
from itertools import count

from py_currency_converter import convert
from forex_python.converter import CurrencyRates

import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_data
from datetime import datetime, timedelta

st.set_page_config( page_title="Countries", page_icon=":earth_americas:", layout='wide' )

# ==========================================
#      Funções        
# ==========================================

# -------------- Limpeza dos dados ---------------

def rename_colunms(dataframe):
    """ Esta função tem a responsabilidade de limpar o dataframe
             Tipos de limpeza:
             1.todo nome de coluna serão em letras minusculas
             2.remoção de espaços nos titulos das colunas
     """
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def clean_dataframe(df1):


    # --- Preenchimento, Criação da coluna com nome dos países  ---------
    COUNTRIES = {1: "India", 14:"Australia", 30: "Brazil", 37: "Canada", 94: "Indonesia", 148: "New Zeland", 162:"Philippines", 166:"Qatar", 184:"Singapure", 189: "South Africa", 191: "Sri Lanka", 208: "Turkey", 214: "United Arab Emirates", 215: "England", 216: "United States of America"}

    def country_name(country_id, value):    
        return COUNTRIES[country_id]

    df1['country'] = df1['country_code'].apply(country_name, args =(COUNTRIES, )) 

    # ---- Criação da coluna do Tipo de Categoria de Comida ---------

    # criação da coluna tipo de preço
    def create_price_tye(price_range):
        if price_range == 1:
            return "cheap"
        elif price_range == 2:
            return "normal"
        elif price_range == 3:
            return "expencive"
        else:
            return "gourmet"    
    df1['price_tye'] = df1['price_range'].apply(lambda x: create_price_tye(x))

    # ----- criação da coluna tipo de cor ----------
    def color_name(rating_color, value):
        return COLORS[rating_color]

    COLORS = {'3F7E00':'darkgreen', '5BA829':'green', '9ACD32':'lightgreen', 'CDD614':'orange', 'FFBA00':'red', 'CBCBC8':'darkred', 'FF7800':'darkred',}

    df1['color_name'] = df1['rating_color'].apply(color_name, args =(COLORS, ))

    # --------- Conversao de texto/categoria/string (object) para object ('str') ------------------
    df1['cuisines'] = df1['cuisines'].astype( str )

    # --------- Remove as linhas vazias que tenham o conteudo igual a 'nan'----------------------------
    linhas_vazias = (df1['cuisines'] != 'nan')
    df1 = df1.loc[linhas_vazias, :].copy()

    # ----------- limpando e simplificando nomenclaturas da coluna do tipo de cozinha --------------------
    df1['cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: x.split(',')[0] )

    # ------------ eliminando valores duplicados no dataframe e renomeando Index ------------------------------------
    df1.drop_duplicates(subset="restaurant_id", inplace=True)


    # -------- Criando nova coluna código da moeda dos paises ----------------------

    MOEDA = {'Botswana Pula(P)':'BWP','Brazilian Real(R$)':'BRL','Dollar($)':'USD','Emirati Diram(AED)':'AED','Indian Rupees(Rs.)':'INR','Indonesian Rupiah(IDR)':'IDR','NewZealand($)':'NZD','Pounds(£)':'GBP','Qatari Rial(QR)':'QAR','Rand(R)':'ZAR','Sri Lankan Rupee(LKR)':'LKR','Turkish Lira(TL)':'TRY',}

    # criação da coluna codigo de nomenglatura da moeda
    def exchange(currency, value):
        return MOEDA[currency]
    df1['currency_cod'] = df1['currency'].apply(exchange, args =(MOEDA, ))

    # -------- correção do custo discrepante do resturante australiano ------------------
    df1.loc[385,'average_cost_for_two'] = 250.17


    # ---- Converção e cambio da moeda -------------------------------------
    # - https://theautomatic.net/yahoo_fin-documentation/
    # - https://finance.yahoo.com/currencies  ---  get_currencies()
    # ---get_data(ticker, start_date = None, end_date = None, index_as_date = True, interval = “1d”)

    def convert_currency_yahoofin(src, dst, amount):
         # construct the currency pair symbol
        symbol = f"{src}{dst}=X"
        # extract minute data of the recent 2 days
        latest_data = si.get_data(symbol, interval="1m", start_date=datetime.now() - timedelta(days=2))
        # get the latest datetime
        last_updated_datetime = latest_data.index[-1].to_pydatetime()
        # get the latest price
        latest_price = latest_data.iloc[-1].close
        # return the latest datetime with the converted amount
        return  latest_price * amount


    # ----------- chamada da tabela auxiliar para ter correção dos indices de cambio --------------
    moeda = pd.read_csv('dataset/cambio.csv')    

    # função de limpeza da variavel retorno indice de cambio py_currency_converter
    def limp(x):
        cotacao = x['USD']
        return cotacao

    # função de limpeza da variavel retorno indice de cambio py_currency_converter
    def limp_BRL(x):
        cotacao = x['BRL']
        return cotacao
    # # ----- ferramenta de converção online para dólar americano USD --------------
    # usd_BWP = convert(base='BWP', amount=1, to=['SGD', 'USD'])
    usd_BRL1 = convert(base='BRL', amount=1, to=['SGD', 'USD'])
    usd_USD1 = convert(base='USD', amount=1, to=['SGD', 'USD'])
    usd_AED1 = convert(base='AED', amount=1, to=['SGD', 'USD'])
    usd_INR1 = convert(base='INR', amount=1, to=['SGD', 'USD'])
    usd_IDR1 = convert(base='IDR', amount=1, to=['SGD', 'USD'])
    usd_NZD1 = convert(base='NZD', amount=1, to=['SGD', 'USD'])
    usd_GBP1 = convert(base='GBP', amount=1, to=['SGD', 'USD'])
    # usd_QAR = convert(base='QAR', amount=1, to=['SGD', 'USD'])
    usd_ZAR1 = convert(base='ZAR', amount=1, to=['SGD', 'USD'])
    # usd_LKR = convert(base='LKR', amount=1, to=['SGD', 'USD'])
    usd_TRY1 = convert(base='TRY', amount=1, to=['SGD', 'USD'])

    # ----- ferramenta de converção online do yahoo finance ---------
    camb_usd_BWP1 = convert_currency_yahoofin('BWP', 'USD', 1)
    camb_usd_QAR1 = convert_currency_yahoofin('QAR', 'USD', 1)
    camb_usd_LKR1 = convert_currency_yahoofin('LKR', 'USD', 1)

    # ----- função de limpeza dos dados -----------------
    camb_usd_BRL1 = limp(usd_BRL1)
    camb_usd_USD1 = limp(usd_USD1)
    camb_usd_AED1 = limp(usd_AED1)
    camb_usd_INR1 = limp(usd_INR1)
    camb_usd_IDR1 = limp(usd_IDR1)
    camb_usd_NZD1 = limp(usd_NZD1)
    camb_usd_GBP1 = limp(usd_GBP1)
    camb_usd_ZAR1 = limp(usd_ZAR1)
    camb_usd_TRY1 = limp(usd_TRY1)

    # função de calculo da vairavel average_cost_for_two para o cambio em dólares
    def calc_cambio1(currency_cod, ):
        if currency_cod == 'BWP':
            atual_USD = camb_usd_BWP1
            return atual_USD
        elif currency_cod == 'BRL':
            atual_USD = camb_usd_BRL1
            return atual_USD
        elif currency_cod == 'USD':
            atual_USD = camb_usd_USD1
            return atual_USD
        elif currency_cod == 'AED':
            atual_USD = camb_usd_AED1
            return atual_USD
        elif currency_cod == 'INR':
            atual_USD = camb_usd_INR1
            return atual_USD
        elif currency_cod == 'IDR':
            atual_USD = camb_usd_IDR1
            return atual_USD
        elif currency_cod == 'NZD':
            atual_USD = camb_usd_NZD1
            return atual_USD
        elif currency_cod == 'GBP':
            atual_USD = camb_usd_GBP1
            return atual_USD
        elif currency_cod == 'QAR':
            atual_USD = camb_usd_QAR1
            return atual_USD
        elif currency_cod == 'ZAR':
            atual_USD = camb_usd_ZAR1
            return atual_USD
        elif currency_cod == 'LKR':
            atual_USD = camb_usd_LKR1
            return atual_USD
        elif currency_cod == 'TRY':
            atual_USD = camb_usd_TRY1
            return atual_USD
        else:
            return None    
    moeda['atual_USD'] = moeda.apply(lambda x: calc_cambio1(x.currency_cod, ), axis=1)

    # ---- função de execução indice em Reais de cambio da py_currency_converter
    brl_BRL1 = convert(base='BRL', amount=1, to=['SGD', 'BRL'])
    brl_USD1 = convert(base='USD', amount=1, to=['SGD', 'BRL'])
    brl_AED1 = convert(base='AED', amount=1, to=['SGD', 'BRL'])
    brl_INR1 = convert(base='INR', amount=1, to=['SGD', 'BRL'])
    brl_IDR1 = convert(base='IDR', amount=1, to=['SGD', 'BRL'])
    brl_NZD1 = convert(base='NZD', amount=1, to=['SGD', 'BRL'])
    brl_GBP1 = convert(base='GBP', amount=1, to=['SGD', 'BRL'])
    brl_ZAR1 = convert(base='ZAR', amount=1, to=['SGD', 'BRL'])
    brl_TRY1 = convert(base='TRY', amount=1, to=['SGD', 'BRL'])

    # limpeza do valor retorno de indice Reais de cambio da py_currency_converter
    camb_brl_BRL1 = limp_BRL(brl_BRL1) 
    camb_brl_USD1 = limp_BRL(brl_USD1)
    camb_brl_AED1 = limp_BRL(brl_AED1) 
    camb_brl_INR1 = limp_BRL(brl_INR1)
    camb_brl_IDR1 = limp_BRL(brl_IDR1)
    camb_brl_NZD1 = limp_BRL(brl_NZD1)
    camb_brl_GBP1 = limp_BRL(brl_GBP1)
    camb_brl_ZAR1 = limp_BRL(brl_ZAR1)
    camb_brl_TRY1 = limp_BRL(brl_TRY1)

    # função de calculo da vairavel average_cost_for_two para o cambio em reais
    def calc_cambio_br1(currency_cod, ):
        if currency_cod == 'BWP':
            atual_BRL = camb_usd_BWP1*camb_brl_USD1
            return atual_BRL
        elif currency_cod == 'BRL':
            atual_BRL = camb_brl_BRL1
            return atual_BRL
        elif currency_cod == 'USD':
            atual_BRL = camb_brl_USD1
            return atual_BRL
        elif currency_cod == 'AED':
            atual_BRL = camb_brl_AED1
            return atual_BRL
        elif currency_cod == 'INR':
            atual_BRL = camb_brl_INR1
            return atual_BRL
        elif currency_cod == 'IDR':
            atual_BRL = camb_brl_IDR1
            return atual_BRL
        elif currency_cod == 'NZD':
            atual_BRL = camb_brl_NZD1
            return atual_BRL
        elif currency_cod == 'GBP':
            atual_BRL = camb_brl_GBP1
            return atual_BRL
        elif currency_cod == 'QAR':
            atual_BRL = camb_usd_QAR1*camb_brl_USD1
            return atual_BRL
        elif currency_cod == 'ZAR':
            atual_BRL = camb_brl_ZAR1
            return atual_BRL
        elif currency_cod == 'LKR':
            atual_BRL = camb_usd_LKR1*camb_brl_USD1
            return atual_BRL
        elif currency_cod == 'TRY':
            atual_BRL = camb_brl_TRY1
            return atual_BRL
        else:
            return None
    moeda['atual_BRL'] = moeda.apply(lambda x: calc_cambio_br1(x.currency_cod, ), axis=1)

    # função para preenchimento da coluna ult_USD com filtro da valores vazios "".
    
    def sem_cambio(ult_USD, atual_USD):       
        isNaN = math.isnan(atual_USD)

        if isNaN == True:
            return ult_USD
        elif atual_USD != isNaN:
             return atual_USD
        else:
            return ult_USD    
    moeda['ult_USD'] = moeda.apply(lambda x: sem_cambio(x['ult_USD'], x['atual_USD']), axis=1)

    # função para preenchimento da coluna ult_BRL com filtro da valores vazios "".
    def sem_cambio2(ult_BRL, atual_BRL):       
        isNaN = math.isnan(atual_BRL)

        if isNaN == True:
            return ult_BRL
        elif atual_BRL != isNaN:
             return atual_BRL
        else:
            return ult_BRL    
    moeda['ult_BRL'] = moeda.apply(lambda x: sem_cambio(x['ult_BRL'], x['atual_BRL']), axis=1) 

    # # chamada para salvar e atualizar os indices na tabela auxiliar
    moeda.to_csv("dataset/cambio.csv", index=False)

    # --------- Calculo de cambio em dólar para dataframe ------

    # função de execução indice de cambio da yahoo finance
    camb_usd_QAR = moeda.loc[8,'ult_USD']
    camb_usd_BWP = moeda.loc[0,'ult_USD']
    camb_usd_LKR = moeda.loc[10,'ult_USD']

    # limpeza do valor retorno de indice dólar de cambio da py_currency_converter
    camb_usd_BRL = moeda.loc[1,'ult_USD'] 
    camb_usd_USD = moeda.loc[2,'ult_USD']
    camb_usd_AED = moeda.loc[3,'ult_USD'] 
    camb_usd_INR = moeda.loc[4,'ult_USD']
    camb_usd_IDR = moeda.loc[5,'ult_USD']
    camb_usd_NZD = moeda.loc[6,'ult_USD']
    camb_usd_GBP = moeda.loc[7,'ult_USD']
    camb_usd_ZAR = moeda.loc[9,'ult_USD']
    camb_usd_TRY = moeda.loc[11,'ult_USD']

    # criação da coluna cost_USD ----
    # função de calculo da vairavel average_cost_for_two para o cambio em dólares
    def calc_cambio(currency_cod, average_cost_for_two):
        if currency_cod == 'BWP':
            cost_usd = average_cost_for_two*camb_usd_BWP
            return cost_usd
        elif currency_cod == 'BRL':
            cost_usd = average_cost_for_two*camb_usd_BRL
            return cost_usd
        elif currency_cod == 'USD':
            cost_usd = average_cost_for_two*camb_usd_USD
            return cost_usd
        elif currency_cod == 'AED':
            cost_usd = average_cost_for_two*camb_usd_AED
            return cost_usd
        elif currency_cod == 'INR':
            cost_usd = average_cost_for_two*camb_usd_INR
            return cost_usd
        elif currency_cod == 'IDR':
            cost_usd = average_cost_for_two*camb_usd_IDR
            return cost_usd
        elif currency_cod == 'NZD':
            cost_usd = average_cost_for_two*camb_usd_NZD
            return cost_usd
        elif currency_cod == 'GBP':
            cost_usd = average_cost_for_two*camb_usd_GBP
            return cost_usd
        elif currency_cod == 'QAR':
            cost_usd = average_cost_for_two*camb_usd_QAR
            return cost_usd
        elif currency_cod == 'ZAR':
            cost_usd = average_cost_for_two*camb_usd_ZAR
            return cost_usd
        elif currency_cod == 'LKR':
            cost_usd = average_cost_for_two*camb_usd_LKR
            return cost_usd
        elif currency_cod == 'TRY':
            cost_usd = average_cost_for_two*camb_usd_TRY
            return cost_usd
        else:
            return None    
    df1['cost_USD'] = round(df1.apply(lambda x: calc_cambio(x.currency_cod, x.average_cost_for_two), axis=1), 2) 

    # --------- Calculo cambio em Reais -------
    # limpeza do valor retorno de indice Reais de cambio da py_currency_converter
    camb_brl_BRL = moeda.loc[1,'ult_BRL'] 
    camb_brl_USD = moeda.loc[2,'ult_BRL']
    camb_brl_AED = moeda.loc[3,'ult_BRL'] 
    camb_brl_INR = moeda.loc[4,'ult_BRL']
    camb_brl_IDR = moeda.loc[5,'ult_BRL']
    camb_brl_NZD = moeda.loc[6,'ult_BRL']
    camb_brl_GBP = moeda.loc[7,'ult_BRL']
    camb_brl_ZAR = moeda.loc[9,'ult_BRL']
    camb_brl_TRY = moeda.loc[11,'ult_BRL']

    # ---- criação da coluna cost_BRL ----------
    # função de calculo da vairavel average_cost_for_two para o cambio em dólares
    def calc_cambio_br(currency_cod, average_cost_for_two):
        if currency_cod == 'BWP':
            cost_usd = average_cost_for_two*camb_usd_BWP*camb_brl_USD
            return cost_usd
        elif currency_cod == 'BRL':
            cost_usd = average_cost_for_two*camb_brl_BRL
            return cost_usd
        elif currency_cod == 'USD':
            cost_usd = average_cost_for_two*camb_brl_USD
            return cost_usd
        elif currency_cod == 'AED':
            cost_usd = average_cost_for_two*camb_brl_AED
            return cost_usd
        elif currency_cod == 'INR':
            cost_usd = average_cost_for_two*camb_brl_INR
            return cost_usd
        elif currency_cod == 'IDR':
            cost_usd = average_cost_for_two*camb_brl_IDR
            return cost_usd
        elif currency_cod == 'NZD':
            cost_usd = average_cost_for_two*camb_brl_NZD
            return cost_usd
        elif currency_cod == 'GBP':
            cost_usd = average_cost_for_two*camb_brl_GBP
            return cost_usd
        elif currency_cod == 'QAR':
            cost_usd = average_cost_for_two*camb_usd_QAR*camb_brl_USD
            return cost_usd
        elif currency_cod == 'ZAR':
            cost_usd = average_cost_for_two*camb_brl_ZAR
            return cost_usd
        elif currency_cod == 'LKR':
            cost_usd = average_cost_for_two*camb_usd_LKR*camb_brl_USD
            return cost_usd
        elif currency_cod == 'TRY':
            cost_usd = average_cost_for_two*camb_brl_TRY
            return cost_usd
        else:
            return None    
    df1['cost_BRL'] = round(df1.apply(lambda x: calc_cambio_br(x.currency_cod, x.average_cost_for_two), axis=1), 2) 

    return df1
    
# ---- Fim da limpeza dos dados e criação de colunas no dataframe ----------------



# ----- função criação do mapa em clusters dos restaurantes --------------------
def country_maps2( df2 ):
    
    cols = ['longitude','latitude','restaurant_name','city','cuisines','aggregate_rating','color_name']
    df_aux = (df2.loc[:, cols]).reset_index()

    map2 = folium.Map(location=[2.033333, 45.35], zoom_start=2)
    mc = MarkerCluster()

    for index, location_info in df_aux.iterrows():
        html = """ <ul>
              <li><b></b>{nome}</li>
              <li><b></b>{cuisines}</li>
              <li><b></b>{pontos}</li>
                    </ul> 
                        """.format(nome=location_info['restaurant_name'], cuisines=location_info['cuisines'], pontos=location_info['aggregate_rating'] )

        mc.add_child(folium.Marker( [location_info['latitude'],
                               location_info['longitude']], 
                              popup=html,
                                icon=folium.Icon(icon='cutlery', color=location_info['color_name']))).add_to(map2)        

    st_folium( map2,  width=1024, height=600 ) 

# ------ calculo da quantidade de paises -------
def calc_quant(df2):    
    df_aux = (df2.loc[:,['country','city']]
                 .groupby('country').nunique()
                 .sort_values('city', ascending=False) 
                 .head(6).reset_index())

    fig = (px.bar(df_aux, x="country", y="city", color="country",
                  color_discrete_sequence=["orange", "red", "green",
                  "blue", "purple", "lightgray",], title="Total de cidades por país"))
    return fig

# ------ calculo da quantidade de restaurantes registrados -------
def calc_quant_resta(df2):
    df_aux = (df2.loc[:,['country', 'restaurant_id']]
                .groupby('country').nunique()
                .sort_values('restaurant_id', ascending=False)
                .reset_index().head(6))

    fig = (px.bar(df_aux, x="country", y="restaurant_id",   
                   color="country", color_discrete_sequence= 
     ['blue','brown','burlywood','green','yellow','crimson','cyan'] , title="Total de restaurantes registrados por país"))
    return fig

# ------ calculo da quantidade de restaurantes gourmet ------------------
def nivel_gourmet(df2):
    gourmet = (df2.loc[:,'price_tye'] == "gourmet")
    df_aux = (df2.loc[gourmet,['country','restaurant_id']]
                .groupby('country').nunique()
                .sort_values('restaurant_id', ascending=False)
                .reset_index().head(7))

    fig = (px.bar(df_aux, x="country", y="restaurant_id",   
                   color="country", color_discrete_sequence= 
     ['blue','brown','burlywood','coral','yellow','crimson','cyan'] , title="Total de restaurantes por país"))
    return fig

# ------- calculo da quantidade de culinarias distintas nos paises -------------
def calc_quant_cuisines(df2):
    df_aux = (df2.loc[:,['country', 'cuisines']]
                 .groupby('country').nunique()
                 .sort_values(['cuisines'],ascending=False)
                 .reset_index().head(6))

    fig = (px.bar(df_aux, x="country", y='cuisines',   
                   color="country", color_discrete_sequence= 
     ['blue','orange','burlywood','coral','yellow','crimson','cyan'] , title="Total de tipos de culinarias por país"))       
    return fig

# ------ calculo do número de avaliações distintas ----------------------
def calc_quant_avaliações(df2):
    df_aux = (df2.loc[:,['country', 'votes']]
                 .groupby('country').sum()
                 .sort_values(['votes'],ascending=False)
                 .reset_index().head(7))
    fig = (px.bar(df_aux, x="country", y='votes',   
                   color="country", color_discrete_sequence= 
     ['blue','orange','burlywood','coral','yellow','crimson','cyan'] , title="Total de avaliações por país")) 
    return fig

# ------- calculo da quantidade de restaurantes que fazem entrega --------------------
def calc_rest_entregas(df2):
    delivery = (df2.loc[:, 'has_online_delivery'] == 1)
    df_aux = (df2.loc[delivery,['country', 'has_online_delivery']]
                .groupby('country').count()
                .sort_values(['has_online_delivery'],ascending=False)
                .reset_index())

    fig = (px.bar(df_aux, x="country", y='has_online_delivery',   
                   color="country", color_discrete_sequence= 
     ['blue','orange','burlywood','coral','yellow','crimson','cyan'] , title="Total de restaurantes por país"))
    return fig

# ------ calculo da quantidades de restaurantes que fazem reservas -------------------
def cal_quant_reservas(df2):
    table_booking = (df2.loc[:, 'has_table_booking'] == 1)
    df_aux = (df2.loc[table_booking,['country','has_table_booking']]
                 .groupby('country').count()
                 .sort_values('has_table_booking', ascending=False)
                 .reset_index().head(7))

    fig = (px.bar(df_aux, x='country', y='has_table_booking',   
                 color='country', 
                 color_discrete_sequence=['blue','orange','burlywood','coral','yellow','crimson','cyan'],
                  title="Total de restaurantes por país"))
    return fig

# ------- calculo da média de avaliações dos restaurantes por país ---------------------
def mean_avaliacoes(df2):
    df_aux = (df2.loc[:,['country','votes']]
                .groupby('country').mean()
                .round(2).sort_values('votes', ascending=False)
                .reset_index().head(7))  

    fig = (px.bar(df_aux, x='country', y='votes',   
                   color="country", 
    color_discrete_sequence= 
     ['blue','orange','burlywood','coral', 'yellow','crimson','cyan'] , title="Quantidades de avaliações resgistradas em média"))
    return fig

# ------- calculo da média de votos dos restaurantes registrados por país ------------------
def mean_votes(df2):
    df_aux = (df2.loc[:,['country', 'aggregate_rating']]
                 .groupby('country').mean()
                 .round(2).sort_values('aggregate_rating', ascending=False)
                 .reset_index().head(7))

    fig = (px.bar(df_aux, x='country', y='aggregate_rating',   
                   color="country", 
    color_discrete_sequence= 
     ['blue','orange','burlywood','coral', 'yellow','crimson','cyan'] , title="Maiores notas médias por país"))
    return fig


# ------- calculo da menor média dos restaurantes registrada por país -----------------------
def mean_min_votes(df2):
    df_aux = (df2.loc[:,['country', 'aggregate_rating']]
                 .groupby('country').mean()
                 .round(2).sort_values('aggregate_rating', ascending=True)
                 .reset_index().head(7))

    fig = (px.bar(df_aux, x='country', y='aggregate_rating',   
                   color="country", 
    color_discrete_sequence= 
     ['blue','orange','burlywood','coral', 'yellow','crimson','cyan'] , title="Menores notas médias por país"))
    return fig

# ------- média de preço do prato para duas pessoas por país ---------
def mean_prato(df2):
    df_aux = (df2.loc[:,['country','cost_USD','cost_BRL']]
                 .groupby('country').mean().round(2)
                 .sort_values('cost_USD', ascending=False)
                 .reset_index().head(7))

    fig = (px.bar(df_aux, x='country', y='cost_USD',   
                   color="country", 
    color_discrete_sequence= 
     ['blue','orange','burlywood','coral', 'yellow','crimson','cyan'] , title="Maiores médias de preços em dólares por prato para duas pessoas por país")) 
    return fig

# ==========================================
#      fim das Funções        
# ==========================================


# -------------------------- Início da Estrutura Lógica de código ---------------------------

# ----------------------------------------
# Import dataset
# ----------------------------------------
df = pd.read_csv('dataset/zomato.csv')

# ----------------------------------------
# Limpando os dados
# ----------------------------------------

df1 = rename_colunms(df)

df2 = clean_dataframe(df1)

# ============================================================
#         LAYOUT DO SIDEBAR STREAMLIT
# =============================================================

#image_path = '/Users/esiomds/documents/repos/FTC/Projeto_final/Projeto/'
image = Image.open('cuisines.png')
st.sidebar.image(image, use_column_width='auto')


st.sidebar.markdown("""---""")
# ---- seleção de paises--------- 

paises_options = st.sidebar.multiselect('PAÍSES SELECIONADOS', ['Philippines','Brazil','Australia','United States of America','Canada','Singapure','United Arab Emirates','India','Indonesia','New Zeland','England','Qatar','South Africa','Sri Lanka','Turkey'], default=['Philippines','Brazil','Australia','United States of America','Canada','Singapure','United Arab Emirates','India','Indonesia','New Zeland','England','Qatar','South Africa','Sri Lanka','Turkey'])

linhas_selecionadas = df2['country'].isin(paises_options)
df2 = df2.loc[linhas_selecionadas, :]

# ===================================================================
# --------   LAYOUT DO STREAMLIT -------------------
#====================================================================

with st.container():
    st.header('Restaurantes e Culinaria em Números')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        reg = df2['restaurant_id'].nunique()
        st.metric(label="Nº de Restaurantes", value=reg, delta=None,
    delta_color="normal")
        
    with col2:
        reg = df2['country'].nunique()
        st.metric(label="Nº de Paises", value=reg, delta=None,
    delta_color="normal")
        
    with col3:
        reg = df2['city'].nunique()
        st.metric(label="Nº de Cidades", value=reg, delta=None,
    delta_color="normal")
        
    with col4:
        reg = df2['votes'].count()
        st.metric(label="Total de avaliações", value=reg, delta=None,
    delta_color="normal")
        
    with col5:
        reg = df2['cuisines'].nunique()
        st.metric(label="Tipos de culinária", value=reg, delta=None,
    delta_color="normal")

        
# # ========= criação do Country map ===========        
with st.container():
    st.header('🗺️ Visão Geral dos Restaurantes e da Culinaria')
    st.markdown("""----""")

    country_maps2( df2 ) 
    st.markdown("""----""")

# # ========= Analise dos restaurantes nos países =========== 

st.header(':bar_chart: Análise dos Restaurantes nos Países')
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # calculo da quantidade de cidades em cada país  para criação do gráfico -------
        fig = calc_quant(df2)
        st.markdown('##### Qual país possui mais cidades registradas ?')   
        st.plotly_chart( fig, use_container_width=True)
        
    with col2:
        # calculo da quantidade de restaurantes registrados em cada país ---------
        fig = calc_quant_resta(df2)
        st.markdown('##### Qual país possui mais restaurantes registrados ?')   
        st.plotly_chart( fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # calculo da quantidade de restaurantes gourmet ---------------
        fig = nivel_gourmet(df2)
        st.markdown('##### Qual país possui mais restaurantes com nível de preço gourmet ?')   
        st.plotly_chart( fig, use_container_width=True)          
        
    with col2:
        # calculo da quantidade de culinarias distintas nos paises ---------------
        fig = calc_quant_cuisines(df2)
        st.markdown('##### Qual país possui a maior quantidade de tipos de culinárias distintas ?')
        st.plotly_chart( fig, use_container_width=True)
        
with st.container():
    col1, col2 = st.columns(2)
    with col1:
       # calculo do número de avaliações distintas ----------------------
        fig = calc_quant_avaliações(df2)
        st.markdown('##### Qual país possui a maior quantidade de avaliações realizadas ?')        
        st.plotly_chart( fig, use_container_width=True)        
        
        
    with col2: 
        # calculo da quantidade de restaurantes que fazem entrega --------------------
        fig = calc_rest_entregas(df2)
        st.markdown('##### Qual país possui a maior quantidade de restaurantes que fazem entregas ?')         
        st.plotly_chart( fig, use_container_width=True)          

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # calculo da quantidades de restaurantes que fazem reservas -------------------
        fig = cal_quant_reservas(df2)
        st.markdown('##### Qual país possui a maior quantidade de restaurantes que fazem reservas ?')       
        st.plotly_chart( fig, use_container_width=True)          
        
    with col2: 
       # calculo da média de avaliações dos restaurantes por país ---------------------
        fig = mean_avaliacoes(df2)
        st.markdown('##### Qual país possui, na média, a maior quantidade de avaliações registrada ?')               
        st.plotly_chart( fig, use_container_width=True)          
        
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # calculo da média de votos dos restaurantes registrados por país ------------------
        fig = mean_votes(df2)
        st.markdown('##### Qual país possui, na média, a maior nota média registrada ?')    
        st.plotly_chart( fig, use_container_width=True)          
        
    with col2: 
        # calculo da menor média dos restaurantes registrada por país ------------------
        fig = mean_min_votes(df2)
        st.markdown('##### Qual país possui, na média, a menor nota média registrada ?')        
        st.plotly_chart( fig, use_container_width=True)  
        
with st.container(): 
    # ------- média de preço do prato para duas pessoas por país ---------
    fig = mean_prato(df2)
    st.markdown('##### Qual a média de preço de um prato para dois por país ?')
    st.plotly_chart( fig, use_container_width=True)  
        