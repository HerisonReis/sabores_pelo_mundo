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
st.set_page_config(page_title="Início",layout="wide",page_icon="🏠")


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

#Criação do Tipo de Categoaria de Comida
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

#st.dataframe( df )

#cópia do dataframe
df1 = df.copy()


st.sidebar.markdown("""___""")

st.sidebar.title('Dados tratados')


@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.sidebar.download_button(
    label=" Download ",
    data=csv,
    file_name='zomato.csv',
    mime="csv")
    


# =============================================
# Layout no streamlit
# =============================================

with st.container():
    st.header('O melhor lugar para encontrar seu mais novo restaurante favorito! ')
#    st.markdown('Temos as seguintes marcas dentro da nossa plataforma:')
    
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        #st.markdown('Restaurantes Cadastrados')
        restaurant_unique = len(df.loc[:,'Restaurant ID'].unique())
        #restaurant_unique
        st.metric(label='Restaurantes Cadastrados',value=restaurant_unique)
            
    with col2:
        countries_unique = len(df.loc[:,'Country Code'].unique())
        st.metric(label='Países Cadastrados',value=countries_unique)
        
            
        
    with col3:
        city_unique = len(df.loc[:,'City'].unique())
        st.metric(label='Cidades Cadastradas',value=city_unique)
            
    with col4:
        rating_total = df.loc[:, 'Votes'].sum()
        st.metric(label='Total de Avaliações',value=rating_total)
        
    with col5:
        cuisines_total = len(df.loc[:, 'Cuisines'].unique())
        st.metric(label='Total de Culinárias',value=cuisines_total)

            

with st.container():
    maps_restaurant = df.groupby('Country Code', as_index=False).median()
    map = folium.Map(zoom_start=2, tiles="CartoDB dark_matter")

    # Adicionando marcadores com cores personalizadas
    for index, location_info in maps_restaurant.iterrows():
        country = location_info['Country Code']
        color = color_map.get(country, '#FFFFFF')  # Preto se não houver cor definida

        folium.CircleMarker(
            location=[location_info['Latitude'], location_info['Longitude']],
            radius=6,  # Tamanho do marcador
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=folium.Popup(f"{country}", parse_html=True)
        ).add_to(map)

    folium_static(map, width=1024, height=600)