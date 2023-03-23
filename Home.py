import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon=":knife_fork_plate:",
    layout='wide'
)

#image_path = '/Users/esiomds/documents/repos/FTC/Projeto_final/Projeto/'
image = Image.open('cuisines.png')
st.sidebar.image(image, use_column_width='auto')


st.write("# 🗺️ Cuisine Around the World Dashboard")

st.markdown(
    """
    '*Cuisine Around the World*' foi feito para o usuário conhecer os tipos de culinária que existe nos países e em cidades pelo mundo.
    ### O que você vai encontrar em '*Cuisine Around the World*'  Dashboard. 
    - :earth_americas: Countries:
        - Restaurantes e culinarias em números;
        - Visão com geolocalização em mapa interativo dos restaurantes;
        - Análise gráfica de restaurantes e culináris em destaque.
    - :city_sunrise: Cities:
        - Restaurantes e culinarias em números;
        - Análise gráfica de tipos de serviços, qualidade e variedade culinária por cidade.
    - :knife_fork_plate: Cusines:
        - Restaurantes e culinarias em números;
        - Avaliação de restaurante e tipos de culinárias;
        - Avaliação dos melhores e piores restaurantes;
        - Avaliação dos preços por país e por cidade;
        - Comparativo de tipos de culinária em preço e avaliação.
        
    ### Ask for Help
    - email: eezzionn@gmail.com     
    
    """)