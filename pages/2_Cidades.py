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

st.set_page_config(page_title="Cidades",layout="wide",page_icon="🌆")


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
    'Singapure': '#8A2BE2',                     # Azul violeta
    'Turkey': '#F95D6A',                        # Vermelho coral
    'Sri Lanka': '#9C88FF',                     # Lavanda
    'Qatar': '#D4A5A5',                         # Rosa antigo
    'Philippines': '#E76F51',                   # Laranja queimado
    'Indonesia': '#2A9D8F'                      # Verde escuro
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
country_options = st.sidebar.multiselect('Escolha o(s) país(es) abaixo', ['India','United States of America','England','South Africa','United Arab Emirates','New Zeland','Brazil','Singapure','Australia', 'Canada','Turkey','Sri Lanka','Qatar','Philippines','Indonesia'], default=[])                                                                                  


if country_options:
    df = df[df['Country Code'].isin( country_options )]

#st.dataframe( df )

#cópia do dataframe
df1 = df.copy()


# =============================================
# Layout no streamlit
# =============================================
    
    
with st.container():
 
    restaurant_city = df.loc[:, ['Restaurant ID', 'City', 'Country Code']] \
                        .groupby(['City', 'Country Code']) \
                        .nunique() \
                        .reset_index() \
                        .sort_values(by='Restaurant ID', ascending=False)
    
    r_city = restaurant_city.head(10)
     
    # Mapeando a cor do país para a cidade usando a coluna 'Country Code'
    r_city['Country Name'] = r_city['Country Code'].map(COUNTRIES)
    r_city['Color'] = r_city['Country Code'].map(color_map)
    
    # Tratando possíveis valores ausentes (NaN)
    r_city['Color'] = r_city['Color'].fillna('#808080')  # Usando cor cinza para NaN
    
    # Criando o gráfico
    fig = px.bar(r_city, x='City', y='Restaurant ID', color='Country Code', color_discrete_map=color_map, title='Top 10 Cidades com mais Restaurantes')
    
    # Remove títulos dos eixos no layout
    fig.update_layout(
        xaxis_title=None,  # Remove o título do eixo X
        yaxis_title=None   # Remove o título do eixo Y
    )
        
    # Exibindo o gráfico
    st.plotly_chart(fig, use_container_width=True)

    
with st.container():
    col1, col2 = st.columns(2)
    with col1: 
        
        acima4 = df['Aggregate rating'] >= 4
        df1 = df.loc[acima4, :]
        acima4_city = df1.loc[:,['City','Aggregate rating','Restaurant ID','Country Code']].groupby(['City', 'Country Code']).nunique().reset_index().sort_values(by='Aggregate rating',ascending=False)
            
        acima4_c = acima4_city.head(7)
        
        # **Ordena o DataFrame em ordem decrescente**
        acima4_c = acima4_c.sort_values(by='Restaurant ID', ascending=False)
        
            
        fig = px.bar( acima4_c , x='City', y='Restaurant ID', color='Country Code', color_discrete_map=color_map, title='Top 7 Cidades com Mais Restaurantes Avaliados')
        
           # Remove títulos dos eixos no layout
        fig.update_layout(
            xaxis_title=None,  # Remove o título do eixo X
            yaxis_title=None   # Remove o título do eixo Y
        )
            
        st.plotly_chart( fig, use_container_width=True )
            
    with col2:
        
        abaixo_2_5 = df['Aggregate rating'] <= 2.5

        df2 = df.loc[abaixo_2_5, :]

        abaixo_2_5_city = df2.loc[:,['City','Aggregate rating','Restaurant ID','Country Code']].groupby(['City', 'Country Code']).nunique().reset_index().sort_values(by='Aggregate rating',ascending=False)
            
        
        abaixo2_5city = abaixo_2_5_city.head(7)
            
            
        fig = px.bar( abaixo2_5city , x='City', y='Restaurant ID', color='Country Code', color_discrete_map=color_map, title= 'Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2,5')
        
           # Remove títulos dos eixos no layout
        fig.update_layout(
            xaxis_title=None,  # Remove o título do eixo X
            yaxis_title=None   # Remove o título do eixo Y
        )
            
        st.plotly_chart( fig, use_container_width=True )
            
            
with st.container():
    
    culinaria_city = df.loc[:, ['Cuisines','City','Country Code']].groupby(['City', 'Country Code']).nunique().reset_index().sort_values(by='Cuisines',ascending=False)
        
    top10_culinaria_city = culinaria_city.head(10)
        
    fig = px.bar( top10_culinaria_city, x='City', y='Cuisines', color='Country Code', color_discrete_map=color_map, title= 'Top 10 Cidades com mais restaurantes com tipo culinários distintos' )
    
     # Remove títulos dos eixos no layout
    fig.update_layout(
        xaxis_title=None,  # Remove o título do eixo X
        yaxis_title=None   # Remove o título do eixo Y
    )
        
    st.plotly_chart( fig, use_container_width=True )
