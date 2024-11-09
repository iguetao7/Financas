import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance


data_inicial = datetime.now() - timedelta(days=360)
data_final = datetime.now()

#Ativo que vai ter o preço buscado
df_ibov = yfinance.download("^BVSP", data_inicial, data_final)["Adj Close"]
print(df_ibov)

#Retorno Ibov
retotno_ibov = df_ibov.iloc[-1] / df_ibov.iloc[0] - 1
retotno_ibov = float(retotno_ibov)
print(f"Retorno do IBOV é de {retotno_ibov:.2%}")

#Média móvel
media_movel = df_ibov.rolling(21).mean()

#Gráfico e legendas
plt.plot(df_ibov, label="IBOV")
plt.plot(media_movel, label="Média móvel 21")
plt.legend()
plt.show()

#Ánalise de carteira
df_carteira = pd.read_excel("Carteira.xlsx")
print(df_carteira)

#Cotação dos ativos
ativos = list(df_carteira["Ativos"].astype(str) + ".SA")
df_cotacoes = yfinance.download(ativos, data_inicial, data_final)["Adj Close"]
print(df_cotacoes)

#Preenchendo celulas vazias
df_cotacoes = df_cotacoes.ffill()
print(df_cotacoes.info())

#Gráfico da carteira
df_cotacoes_norm = df_cotacoes /df_cotacoes.iloc[0]
df_cotacoes_norm.plot(figsize=(15, 5))
plt.legend(loc="upper left")
plt.show()

#Total investido na carteira
df_valor_investido = pd.DataFrame()
for ativo in df_carteira["Ativos"]:
    qtde_acoes = df_carteira.loc[df_carteira["Ativos"] == ativo, "Qtde"].values[0]
    df_valor_investido[ativo] = qtde_acoes * df_cotacoes[f"{ativo}.SA"]
df_valor_investido["Total"] = df_valor_investido.sum(axis=1)
print(df_valor_investido)

#Comparando carteira com índice
df_ibov_norm = df_ibov / df_ibov.iloc[0]
df_valor_investido_norm = df_valor_investido / df_valor_investido.iloc[0]
plt.plot(df_valor_investido_norm["Total"], label="Carteira")
plt.plot(df_ibov_norm, label="IBOV")
plt.legend()
plt.show()

#Retorno da carteira e do IBOV
retorno_ibov = df_ibov_norm.iloc[-1] - 1
retorno_carteira = df_valor_investido_norm["Total"].iloc[-1] - 1
retorno_ibov = float(retotno_ibov)
retorno_carteira = float(retorno_carteira)
print(f"Retorno do IBOV é de {retorno_ibov:.2%}")
print(f"Retorno da carteira é de {retorno_carteira:.2%}")


