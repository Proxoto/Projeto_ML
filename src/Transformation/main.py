# Importar o Pandas
import pandas as pd
import sqlite3
from datetime import datetime


# Ler o arquivo CSV
df = pd.read_csv('../data/data.csv')

# Adicionar Coluna da fonte de dados

df['_source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

# Adicionar Coluna do dia da raspagem
df['_scraping_date'] = datetime.now()

# Tratando valores NaN
df['old_price_int'] = df['old_price_int'].fillna(0)
df['old_price_cents'] = df['old_price_cents'].fillna(0)
df['new_price_int'] = df['new_price_int'].fillna(0)
df['new_price_cent'] = df['new_price_cent'].fillna(0)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0)

# Remover os parênteses da coluna 'review_amount'

df['reviews_amount'] = df['reviews_amount'].str.replace('(', '').str.replace(')', '')
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Tratar os preços

df['old_price'] = df['old_price_int'] + df['old_price_cents'] / 100
df['new_price'] = df['new_price_int'] + df['new_price_cent'] / 100

# Remover as Colunas antigas dos preços

df = df.drop(['old_price_int', 'old_price_cents', 'new_price_int', 'new_price_cent'], axis=1)

# Conectar ao banco de dados SQLite

conn = sqlite3.connect('../data/quotes.db')

# Exportar para o BD SQLite

df.to_sql('ML_items', conn, if_exists='append', index=False)

# Fechar a conexão com o BD

conn.close()

print(df.info())
