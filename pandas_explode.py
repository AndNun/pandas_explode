# %%
import pandas as pd

import numpy as np

# %%
# Importando dados de exemplo
dados_transacao = pd.read_csv('transacao_cartao.txt', sep = ';')
dados_transacao.info()

# %%
# Tratando data da transação
dados_transacao['dt_transacao'] = pd.to_datetime(dados_transacao['dt_transacao'], format = '%d/%m/%Y')
dados_transacao['dt_transacao']

# %%
# Criando colunas com lista dos valor das parcelas
dados_transacao['valor_parcela'] = dados_transacao.apply(lambda row: [row['valor']/row['qtd_parcelas'] for i in range(row['qtd_parcelas'])], axis = 1)

# %%
# Aplicando função explode para explodir valor para parcela para cada transação a depender da quantidade de parcelas
dados_fatura = dados_transacao.explode('valor_parcela')

# Removendo colunas desnecessárias
dados_fatura = dados_fatura.drop(['valor', 'qtd_parcelas'], axis = 1)
dados_fatura

# %%
# Agora preciasamos andar alguns meses para frente, para que possamos trazer a data da fatura 
# Para isto iremos criar uma coluna auxiliar que diz quanto meses para frente devemos adicionar
dados_fatura['mes_add'] = dados_fatura.groupby('id_transacao')['dt_transacao']\
                                        .rank('first')\
                                        .astype(int)

dados_fatura

# %%
# Criando função para adicionar nova data que adciona um mês para frente
def add_meses(row):
    dias_por_mes = 31
    nova_data = row['dt_transacao'] + np.timedelta64(row['mes_add'] * dias_por_mes, 'D')
    dt_str = f'{nova_data.year}-{nova_data.month:02}'
    return dt_str

# %%
# Aplicando função add meses
dados_fatura['dt_fatura'] = dados_fatura.apply(add_meses, axis = 1)

dados_fatura

# %%
# Realizando o calculo da fatura do cliente
dados_fatura.groupby(['id_cliente', 'dt_fatura'])['valor_parcela'].sum().reset_index()
