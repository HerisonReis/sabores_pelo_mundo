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

st.set_page_config(page_title="Culinárias",layout="wide",page_icon="🍽️")

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

st.sidebar.markdown("""___""")

#======================= Quantidade de restaurantes visualizados =================================


restaurant_slider = st.sidebar.slider('Até quantos restaurantes?',0,20,10)
                                
st.write(restaurant_slider)


st.sidebar.markdown("""___""")

# Filtro Culinárias Escolhas ===============================================
cuisines_filtros = df['Cuisines'].unique()
cuisines_options = st.sidebar.multiselect('Escolha os Tipos de Culinária',cuisines_filtros, default='Brazilian')

                                                                                                                                                  
                                                                           

linhas_selecionadas3 = df['Cuisines'].isin( cuisines_options )
df3 = df.loc[linhas_selecionadas3, :]





#cópia do dataframe
df1 = df.copy()

# =============================================
# Layout no streamlit
# =============================================
        
with st.container():
    st.markdown('<h3 style="font-size:17px;">Melhores restaurantes dos principais tipos culinários</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        culinaria_maior_nota = df.loc[:, ['Cuisines','Aggregate rating']].groupby('Cuisines').mean().reset_index().sort_values(by='Aggregate rating',ascending=False )
        
       
        culinaria_maior_nota.iloc[0,0]
        st.markdown(f'{culinaria_maior_nota.iloc[0,1]}/5.0')
       
    
    with col2:
      
        culinaria_maior_nota.iloc[1,0]
        st.markdown(f'{round(culinaria_maior_nota.iloc[1,1],2)}/5.0')
    
    with col3:
        
        culinaria_maior_nota.iloc[2,0]
        st.markdown(f'{round(culinaria_maior_nota.iloc[2,1],2)}/5.0')
        
        
    with col4:
        
        culinaria_maior_nota.iloc[3,0]
        st.markdown(f'{round(culinaria_maior_nota.iloc[3,1],2)}/5.0')
        
    with col5:
        
        culinaria_maior_nota.iloc[4,0]
        st.markdown(f'{round(culinaria_maior_nota.iloc[4,1],2)}/5.0')
        
        

with st.container():
    
    restaurant_text = f' Top {restaurant_slider} Restaurantes'
    
    
    st.markdown(f'<h3 style="font-size:17px;">{restaurant_text}</h3>', unsafe_allow_html=True)

    maior_nota_restaurante = df.loc[:,['Aggregate rating','Restaurant Name','Restaurant ID','Country Code','City','Cuisines','Average Cost for two','Votes']].groupby('Restaurant Name').mean().reset_index().sort_values(by='Aggregate rating', ascending=False)

          
    restaurante10_maior_nota = maior_nota_restaurante.head(restaurant_slider)
        
    restaurante10_maior_nota
        
with st.container():
    col1, col2 = st.columns(2)
        
    with col1:
        
        culinaria_maior_nota = df.loc[:, ['Cuisines','Aggregate rating','Country Code']].groupby(['Cuisines','Country Code']).mean().reset_index().sort_values(by='Aggregate rating',ascending=False)
            
        culinaria_top10 = culinaria_maior_nota.head(restaurant_slider)
            
        fig = px.bar( culinaria_top10, x='Cuisines', y='Aggregate rating', color='Country Code', color_discrete_map=color_map, title= f' Top {restaurant_slider} Melhores Tipos de Culinárias')
        
            # Remove títulos dos eixos no layout
        fig.update_layout(
            xaxis_title=None,  # Remove o título do eixo X
            #yaxis_title=None   # Remove o título do eixo Y
        )
        
        st.plotly_chart( fig, use_container_width=True )
                  
                
    with col2:
        
        culinaria_menor_nota = df.loc[:, ['Cuisines','Aggregate rating','Country Code']].groupby(['Cuisines','Country Code']).mean().reset_index().sort_values(by='Aggregate rating',ascending=True)
            
        culinaria_top10_menos = culinaria_menor_nota.head(restaurant_slider)
            
        fig = px.bar( culinaria_top10_menos, x='Cuisines' ,y='Aggregate rating', color='Country Code', color_discrete_map=color_map, title= f' Top {restaurant_slider} Piores Tipos de Culinárias')
        
        # Remove títulos dos eixos no layout
        fig.update_layout(
            xaxis_title=None,  # Remove o título do eixo X
            #yaxis_title=None   # Remove o título do eixo Y
        )
            
        st.plotly_chart( fig, use_container_width=True )