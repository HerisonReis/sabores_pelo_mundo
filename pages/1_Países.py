# Libraries

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import folium

# Bibliotecas necessárias
import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_folium import folium_static
from datetime import datetime

# import dataset

df = pd.read_csv('zomato.csv')

# Funções

#Tamanho da página

st.set_page_config(page_title="Países",layout="wide",page_icon="🌍")


#Preenchimento dos nomes dos países
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]

#Criação do Tipo de Categoria de Comida

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

    
# Definindo um mapeamentode cores fixo para os países
color_map = {
    'India': '#636EFA',             # Azul
    'United States of America': '#EF553B',     # Vermelho
    'Brazil': '#00CC96',            # Verde
    'Australia': '#AB63FA',         # Roxo
    'Canada': '#FFA15A',            # Laranja
    'United Kingdom': '#19D3F3',    # Azul claro
    'South Africa': '#FF6692',      # Rosa
    'New Zeland': '#B6E880',        # Verde limão
    'England': '#FFB400',           # Amarelo dourado
    'United Arab Emirates': '#00C2C7', # Azul turquesa
    'Turkey': '#F95D6A',            # Vermelho coral
    'Sri Lanka': '#9C88FF',         # Lavanda
    'Qatar': '#D4A5A5',             # Rosa antigo
    'Philippines': '#E76F51',       # Laranja queimado
    'Indonesia': '#2A9D8F'          # Verde escuro
}


# Criação do nome das cores
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]


#Remover as linhas duplicadas
df = df.drop_duplicates().reset_index(drop=True)

#Remover na
df = df.dropna()


# Incluindo coluna de nome de país
df['Country Code'] = df['Country Code'].map(COUNTRIES)

# CATEGORIZAR
df['Cuisines'] = df.loc[:, 'Cuisines'].apply(lambda x: x.split(',')[0])

# =============================================
# Barra lateral
# =============================================


image_path = 'sabores_pelo_mundo.png'
image = Image.open(image_path)
st.sidebar.image( image, width=150)

st.sidebar.markdown("""___""")

#================= Filtros utilizando o Country Code ========
country_options = st.sidebar.multiselect('Escolha o(s) país(es) abaixo', ['India','United States of America','England','South Africa','United Arab Emirates','New Zeland','Brazil','Australia', 'Canada','Turkey','Sri Lanka','Qatar','Philippines','Indonesia'], default=['Brazil','India','Canada','United States of America'])
                                                                                      

#Filtro de Códigos dos países
linhas_selecionadas = df['Country Code'].isin( country_options )
df = df.loc[linhas_selecionadas, :]


#cópia do dataframe
df1 = df.copy()


# =============================================
# Layout no streamlit
# =============================================
    
with st.container():
    restaurant_for_country = (df.loc[:, ['Restaurant Name', 'Country Code']].groupby('Country Code')
                                .nunique()
                                .reset_index()
                                .sort_values(by='Restaurant Name', ascending=False))

        
    fig = px.bar(restaurant_for_country, x='Country Code', y='Restaurant Name', color='Country Code', color_discrete_map=color_map, title='Quantidade de Restaurantes Registrados por País')
    
    fig.update_layout(
            xaxis_title=None,  # Remove o título do eixo X
            yaxis_title=None   # Remove o título do eixo Y
        )
        
    st.plotly_chart( fig, use_container_width=True )
        
    
with st.container():
    city_countries = df.loc[:,['Country Code','City']].groupby('Country Code').nunique().reset_index().sort_values(by='City',ascending=False)

        
    fig = px.bar(city_countries, x='Country Code', y='City', color='Country Code', color_discrete_map=color_map, title='Quantidade de Cidades Registradas por País')
    
    fig.update_layout(
            xaxis_title=None,  # Remove o título do eixo X
            yaxis_title=None   # Remove o título do eixo Y
        )
        
    st.plotly_chart( fig, use_container_width=True )
        
        
    
with st.container():
    col1, col2 = st.columns(2)
        
    with col1:
        rating_country_mean = df.loc[:, ['Country Code','Votes']].groupby('Country Code').mean().reset_index().sort_values(by='Votes', ascending=False)
            
                
        fig = px.bar(rating_country_mean, x='Country Code', y='Votes', color='Country Code', color_discrete_map=color_map, title= 'Média de Avaliações feitas por País')
        
        fig.update_layout(
            xaxis_title=None,  # Remove o título do eixo X
            #yaxis_title=None   # Remove o título do eixo Y
        )
            
        st.plotly_chart( fig, use_container_width=True )
            
    with col2:
        avarage_country = df.loc[:,['Country Code','Average Cost for two']].groupby('Country Code').mean().reset_index().sort_values(by= 'Average Cost for two', ascending=False)
            
            
        fig = px.bar( avarage_country , x='Country Code', y='Average Cost for two', color='Country Code', color_discrete_map=color_map, title='Média de Preço de um prato para duas pessoas por País')
        
        fig.update_layout(
            xaxis_title=None,  # Remove o título do eixo X
            #yaxis_title=None   # Remove o título do eixo Y
        )
            
        st.plotly_chart( fig, use_container_width=True )
            