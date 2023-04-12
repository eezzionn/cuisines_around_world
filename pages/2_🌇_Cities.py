# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
from plotly.subplots import make_subplots
# bibliotecas necessárias
import pandas as pd
import numpy as np
import math
import inflection
import streamlit as st
import folium
import re
import csv
import math
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from PIL import Image
from datetime import datetime 
from itertools import count

from py_currency_converter import convert
from forex_python.converter import CurrencyRates

import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_data
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Cities",
    page_icon=":city_sunrise:",
    layout='wide', )


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

# ------ geração de gráfico Treecamp ---------------------
def grafico(df_aux, flag):    
    fig1 = px.treemap(df_aux, path=[px.Constant('country'),'country', 'city', flag], values=flag,
                  color=flag, 
                  color_continuous_scale='spectral', title='')
    fig1.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig1.update_traces(hovertemplate='<b>%{label}</b><br>%{value}</br>')
    return fig1

# ------ geração de gráfico Treecamp ---------------------
def grafico2(df_aux, flag):    
    fig1 = px.treemap(df_aux, path=[px.Constant('country'),'country', 'city', flag], values=flag,
                  color=flag, 
                  color_continuous_scale='sunset', title='')
    fig1.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig1.update_traces(hovertemplate='<b>%{label}</b><br>%{value}</br>')
    return fig1

# ------ cidades com mais restaurantes ------
def city_resta(df2):
    df_aux = (df2.loc[:,['country','city', 'restaurant_id']]
                 .groupby(['country','city']).count()
                 .sort_values('restaurant_id', ascending=False)
                 .reset_index().head(100) )    

    fig = grafico(df_aux, df_aux.restaurant_id)
    fig.layout.update({'title': 'Total de Restaurantes por cidade'})
    return fig

# ------ restaurantes com restaurantes com nota média acima de 4 ------
def rest_mean(df2):
    df_aux = (df2.loc[:,['country','city', 'aggregate_rating']]
                 .groupby(['country','city']).mean().round(2)
                 .sort_values('aggregate_rating', ascending=False)
                 .reset_index().head(80))
    fig = go.Figure(data=[go.Table(name='tetet',
        header=dict(values=list(df_aux.columns), 
                    fill_color='darkblue',
                    align='left' ),
        cells=dict(values=[df_aux.country, df_aux.city, df_aux.aggregate_rating],
                   fill_color='orange',
                   align='center'))]) 
    fig.layout.update({'title': 'Ranking de restaurantes com média acima de 4'})
    return fig

# ------ restaurantes com restaurantes com nota média menor que 2.5 ------
def rest_mean_menor(df2):
    df_aux = (df2.loc[:,['country','city', 'aggregate_rating']]
                 .groupby(['country','city']).mean().round(2)
                 .sort_values('aggregate_rating', ascending=True)
                 .reset_index().head(5))

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df_aux.columns),
                    fill_color='darkblue', align='left'),
        cells=dict(values=[df_aux.country, df_aux.city, df_aux.aggregate_rating],
                   fill_color='mediumaquamarine',
                   align='center'))])
    fig.layout.update({'title': 'Ranking de restaurantes com média abaixo de 2,5'})
    return fig

# ------ cidade com custo médio do prato para duas pessoas ----------------
def rest_maior_custo(df2):
    df_aux = (df2.loc[:,['country','city','cost_USD']]
                 .groupby(['country','city']).mean().round(2)
                 .sort_values('cost_USD', ascending=False)
                 .reset_index().head(30))
    
    fig = grafico(df_aux, df_aux.cost_USD)
    fig.layout.update({'title': 'Preço médio em dólares do prato para duas pessoas por cidade'})
    return fig

# ------ cidades com maior quantidade de tipos de culinaria ----------------
def maior_quant_cuisines(df2):
    df_aux = (df2.loc[:,['country','city', 'cuisines']]
                 .groupby(['country','city']).nunique()
                 .sort_values('cuisines', ascending=False)
                 .reset_index().head(60) )
    
    fig = grafico(df_aux, df_aux.cuisines)
    fig.layout.update({'title': 'Quantidade de tipos de culinária por cidade'})
    return fig

# ------ calculo de cidades com maior quantidade de reservas --------------
def quant_reservas(df2):
    table_booking = (df2.loc[:, 'has_table_booking'] == 1)
    df_aux = (df2.loc[table_booking,['country','city', 'has_table_booking']]
                 .groupby(['country','city']).sum()
                 .sort_values('has_table_booking', ascending=False)
                 .reset_index().head(20))
    
    fig = grafico2(df_aux, df_aux.has_table_booking)
    fig.layout.update({'title': 'Quantidade de Restaurantes que aceitam reservas por cidade'})
    return fig

# ------ calculo das cidades com maior quantidade de restaurantes que fazem entregas ------------------
def quant_entregas(df2):
    delivering_now = (df2.loc[:, 'is_delivering_now'] == 1)
    df_aux = (df2.loc[delivering_now,['country','city','is_delivering_now']]
                 .groupby(['country','city']).sum()
                 .sort_values('is_delivering_now', ascending=False)
                 .reset_index().head(150))
    
    fig = grafico(df_aux, df_aux.is_delivering_now)
    fig.layout.update({'title': 'Quantidade de Restaurantes que fazem entregas por cidade'})
    return fig


# ------ calculo das cidades com maior quantidade de restaurantes que aceitam pedidos online -------------
def quant_pedidos_online(df2):
    online_delivery = (df2.loc[:,'has_online_delivery'] == 1)
    df_aux = (df2.loc[online_delivery,['country','city','has_online_delivery']]
                 .groupby(['country','city']).sum()
                 .sort_values('has_online_delivery', ascending=False)
                 .reset_index().head(50))
    
    fig = grafico2(df_aux, df_aux.has_online_delivery)
    fig.layout.update({'title': 'Quantidade de Restaurantes que aceitam pedidos online por cidade'})
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

image = Image.open('cuisines.png')
st.sidebar.image(image, use_column_width='auto')

st.sidebar.markdown("""---""")
# ---- seleção de paises--------- 

paises_options = st.sidebar.multiselect('PAÍSES SELECIONADOS', ['Philippines','Brazil','Australia','United States of America','Canada','Singapure','United Arab Emirates','India','Indonesia','New Zeland','England','Qatar','South Africa','Sri Lanka','Turkey'], default=['United States of America','India'])

linhas_selecionadas = df2['country'].isin(paises_options)
df2 = df2.loc[linhas_selecionadas, :]


cidades = list(df2.loc[:,'city'].unique())
cidades_options = st.sidebar.multiselect('CIDADES SELECIONADAS', cidades, default=cidades)
linhas_selecionadas = df2['city'].isin(cidades_options)
df2 = df2.loc[linhas_selecionadas, :]


# ===================================================================
# --------   LAYOUT DO STREAMLIT -------------------
#====================================================================

with st.container():
    
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


st.header(':chart_with_upwards_trend: Avaliação dos Restaurantes por Cidades')
st.markdown("""----""")

with st.container():
    # cidades com mais restaurantes ------
    fig = city_resta(df2)
    st.markdown('##### Qual o nome da cidade que possui mais restaurantes registrados ?')
    st.plotly_chart( fig, use_container_width=True)
    
with st.container():    
    col1, col2 = st.columns(2)
    
    with col1: 
        # restaurantes com restaurantes com nota média acima de 4 ------
        fig = rest_mean(df2)        
        st.markdown('##### Qual o nome da cidade que possui mais restaurantes com nota média acima de 4 ?')
        st.plotly_chart( fig, use_container_width=True)
    
    with col2:   
        # restaurantes com restaurantes com nota média menor que 2.5 ------
        fig = rest_mean_menor(df2)
        st.markdown('##### Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5 ?')
        st.plotly_chart( fig, use_container_width=True)   
    
with st.container(): 
    # cidade com custo médio do prato para duas pessoas ----------------
    fig = rest_maior_custo(df2)
    st.markdown('##### Qual o nome da cidade que possui o maior valor médio de um prato para dois ?')
    st.plotly_chart( fig, use_container_width=True)
    
with st.container():    
    # cidades com maior quantidade de tipos de culinaria ----------------
    fig = maior_quant_cuisines(df2)
    st.markdown('##### Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?')
    st.plotly_chart( fig, use_container_width=True)  

with st.container(): 
    # calculo de cidades com maior quantidade de reservas --------------
    fig = quant_reservas(df2)
    st.markdown('##### Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?')
    st.plotly_chart( fig, use_container_width=True)      
    
with st.container():  
    # calculo das cidades com maior quantidade de restaurantes que fazem entregas ------------------
    fig = quant_entregas(df2)
    st.markdown('##### Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?')
    st.plotly_chart( fig, use_container_width=True)      
    
    
with st.container():    
    # calculo das cidades com maior quantidade de restaurantes que aceitam pedidos online -------------
    fig = quant_pedidos_online(df2)
    st.markdown('##### Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online ?')
    st.plotly_chart( fig, use_container_width=True)      
    