import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao BD SQlite

conn = sqlite3.connect('../data/quotes.db')

# Carregar os dados da table 'ML_items' em um DataFrame do Pandas

df = pd.read_sql_query("SELECT * FROM ML_items", conn)

# Fechar o BD SQlite

conn.close()

# Título da Aplicação

st.title('Pesquisa de Mercado - Tênis Esportivos no ML')

# Melhorar o layout com colunas para KPIs

st.subheader('KPIs principais do sistema')
col1, col2, col3 = st.columns(3)

# KPI 1: Número Total de Itens

total_items = df.shape[0]
col1.metric('Total de Itens', total_items)

# KPI 2: Número de Marcas Únicas

unique_brands = df['brand'].nunique()
col2.metric('Marcas Únicas', unique_brands)

# KPI 3: Preço Médio dos Preços Novos

avg_new_price = df['new_price'].mean()
col3.metric('Preço Médio dos Preços Novos', f'R$ {avg_new_price:.2f}')

# Quais marcas são as mais encontradas até a 10ª página

st.subheader('Marcas mais encontradas até a 10ª página')
col1, col2 = st.columns([4, 2])
top_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_brands)
col2.write(top_brands)

# Qual o preço médio por marca

st.subheader('Preço Médio por Marca')
col1, col2 = st.columns([4, 2])
df_non_zero_prices = df[df['new_price'] > 0]
avg_prices_by_brand = df_non_zero_prices.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(avg_prices_by_brand)
col2.write(avg_prices_by_brand)

# Satisfação por Marca

st.subheader('Satisfação por Marca')
col1, col2 = st.columns([4, 2])
df_non_zero_ratings = df[df['reviews_rating_number'] > 0]
avg_rating_by_brand = df_non_zero_ratings.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(avg_rating_by_brand)
col2.write(avg_rating_by_brand)