## Pacotes 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st 




st.set_page_config(page_title="Dados do atividade",
                   page_icon="🏙️", 
                   layout="wide")



custom_css = """
body {
    background-color: #f0f2f6; /* cor de fundo geral */
    color: #333333; /* cor do texto principal */
    font-family: Arial, sans-serif; /* fonte padrão */
}

.stButton {
    background-color: #007BFF !important; /* cor dos botões */
    color: white !important; /* cor do texto nos botões */
}

.stTextInput {
    border-color: #007BFF !important; /* cor da borda dos inputs */
}
"""

st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

## Importação dos Dados 

df = pd.read_excel("C:\Users\vinicius.valenca\Documents\GitHub\streamlit_revista_deploy\dataset\prodepe_2.xlsx")

df.columns = df.columns.str.strip() ## Espaços em branco 

meses = {
    'JANEIRO': '01',
    'FEVEREIRO': '02',
    'MARÇO': '03',
    'ABRIL': '04',
    'MAIO': '05',
    'JUNHO': '06',
    'JULHO': '07',
    'AGOSTO': '08',
    'SETEMBRO': '09',
    'OUTUBRO': '10',
    'NOVEMBRO': '11',
    'DEZEMBRO': '12'
}

## Tratando a data 

df['MÊS_NUM'] = df['MÊS REUNIÃO'].map(meses)


if df['MÊS_NUM'].isna().any():
    print("Existem meses inválidos:")
    print(df[df['MÊS_NUM'].isna()][['ANO', 'MÊS REUNIÃO']])


df['data'] = df['ANO'].astype(str) + '-' + df['MÊS_NUM']


df['data'] = pd.to_datetime(df['data'], format='%Y-%m', errors='coerce')

if df['data'].isna().any():
    print("Existem datas inválidas:")
    print(df[df['data'].isna()][['ANO', 'MÊS REUNIÃO', 'MÊS_NUM']])


df = df[['data'] + [col for col in df.columns if col != 'data']]
df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace(r'[^a-zA-Z0-9_]', '', regex=True)

df['trimestre'] = pd.PeriodIndex(df['data'], freq='Q')

df = df[['data', 'trimestre', 'ano', 'ms_reunio', 'tipo_de_projeto', 'setor_de_atividade', 'rd', 'investimentos_r', 'empregos', 'ms_num']]



## TRATAMENTO 

## Seleconando 
colunas_sel = ['trimestre', 'tipo_de_projeto', 'setor_de_atividade', 'rd', 'investimentos_r',
               'empregos']


df_sel = df[colunas_sel]

## Convertendo as colunas 



df_sel['empregos'].isnull().sum()
df_sel['empregos'] = df_sel['empregos'].fillna(0).astype(int)
df_sel['empregos'] = pd.to_numeric(df_sel['empregos'], errors='coerce')

df_sel.isna().sum()
df_sel.fillna(value='0', inplace=True)


# Algumas tabelas 

## Projetos por RD
#projetos_rd = df_sel.groupby('rd').size().reset_index(name='total_projetos')

## Empregos por setor
#empregos_por_setor = df.groupby('setor_de_atividade')['empregos'].sum().reset_index(name='total_empregos')


# Merge dos dados 

## Adicionando as tabelas Prohetos por RD e empregos por total por setor 

#df_sel = df_sel.merge(projetos_rd, on='rd', how='left')
#df_sel = df_sel.merge(empregos_por_setor, on='setor_de_atividade', how='left')


df_sel.rename(columns={
    'trimestre': 'data',
    'tipo_de_projeto': 'projetos',
    'setor_de_atividade': 'atividade',
    'rd': 'RD',
    'investimentos_r': 'investimento',
    'empregos': 'empregos',
    'total_projetos': 'total_projetos_rd',
    'total_empregos': 'total_emprego_setor'
}, inplace=True)


df_sel['investimento'] = pd.to_numeric(df_sel['investimento'], errors='coerce')

## Agrupando os Dados 

# Padronizando nomes dos setores de atividade
mapping = {
    'METALMECÂNICA': 'METALMECÂNICA',
    'METALMECÂNICA E DE MATERIAL DE TRANSPORTE': 'METALMECÂNICA E DE MATERIAL DE TRANSPORTE',
    'MINERAIS NÃO METÁLICOS': 'MINERAIS NÃO METÁLICOS',
    'PLÁSTICOS': 'PLÁSTICOS',
    'AGROINDÚSTRIA': 'AGROINDÚSTRIA',
    'BEBIDAS': 'BEBIDAS',
    'COMÉRCIO ATACADISTA': 'COMÉRCIO ATACADISTA',
    'COMÉRCIO IMPORTADOR ATACADISTA': 'COMÉRCIO IMPORTADOR ATACADISTA',
    'ELETROELETRÔNICA': 'ELETROELETRÔNICA',
    'FARMACOQUÍMICA': 'FARMACOQUÍMICA',
    'MÓVEIS': 'MÓVEIS'
}

# Padronização Projetos 

mapping_projetos = {
    'CENTRAL DE DISTRIBUIÇÃO': 'CENTRAL DE DISTRIBUIÇÃO',
    'IMPORTAÇÃO': 'IMPORTAÇÃO',
    'INDÚSTRIA': 'INDÚSTRIA',
    # Adicione outros mapeamentos conforme necessário
}

# Padronozação RD 

# Padronização dos nomes de RD
mapping_rd = {
    'AGRESTE CENTRAL': 'AGRESTE CENTRAL',
    'SERTÃO DO PAJEÚ': 'SERTÃO DO PAJEÚ',
    'METROPOLITANA': 'METROPOLITANA',
    'SERTÃO DO ARARIPE': 'SERTÃO DO ARARIPE',
    'MATA SUL': 'MATA SUL',
    'SERTÃO DO SÃO FRANCISCO': 'SERTÃO DO SÃO FRANCISCO',
    'AGRESTE MERIDIONAL': 'AGRESTE MERIDIONAL',
    'SERTÃO DO MOXOTÓ': 'SERTÃO DO MOXOTÓ',
    'AGRESTE SETENTRIONAL': 'AGRESTE SETENTRIONAL',
}





# Aplicando o mapeamento

df_sel['atividade'] = df_sel['atividade'].replace(mapping)

df_sel['projetos'] = df_sel['projetos'].replace(mapping_projetos)

df_sel['RD'] = df_sel['RD'].replace(mapping_rd)

## Coluna data trimestral 



# Agrupando os dados conforme solicitado

df_agrupado = df_sel.groupby(['data', 'projetos', 'RD', 'atividade'], as_index=False).agg({
    'investimento': 'sum',
    'empregos': 'sum',
})

#df_agrupado.set_index('data', inplace=True)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
#df_agrupado = df_agrupado[df_agrupado['data'] > '2020-01-01']


#df_agrupado['investimento'] = pd.to_numeric(df_agrupado['investimento'], errors='coerce')

# Adicionando a coluna 'ano' com base na data
# Salvando os dados para o Streamlit carregar

st.session_state["df_agrupado"] = df_agrupado


# Calcular os totais para o value Box 
total_empregos = df_agrupado['empregos'].sum()
total_investimento = df_agrupado['investimento'].sum()
total_projetos = df_agrupado['projetos'].nunique()
total_atividade = df_agrupado['atividade'].nunique()
investimento_medio = df_agrupado['investimento'].mean()
emprego_medio = df_agrupado['empregos'].mean()

# Função para simplificar os números grandes
def format_large_numbers(number):
    if abs(number) >= 1_000_000_000:
        return f'R${number / 1_000_000_000:.2f}B'
    elif abs(number) >= 1_000_000:
        return f'R${number / 1_000_000:.2f}M'
    elif abs(number) >= 1_000:
        return f'R${number / 1_000:.2f}K'
    else:
        return f'R${number:.2f}'


# CSS para adicionar contornos
 
# CSS para adicionar contornos
st.markdown("""
    <style>
    .metric-box {
        border: 1px solid #ddd; /* cor do contorno */
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-box.total-empregos {
        background-color: #f8d7da; /* fundo vermelho claro */
    }
    .metric-box.total-investimento {
        background-color: #d4edda; /* fundo verde claro */
    }
    .metric-box.total-projetos {
        background-color: #d1ecf1; /* fundo azul claro */
    }
    .metric-box.total-atividade {
        background-color: #fff3cd; /* fundo amarelo claro */
    }
    .metric-label {
        font-size: 16px;
        font-weight: bold;
    }
    .metric-value {
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# Visualização com Streamlit
st.title("Prodepe 2024")

# Adicionando filtros adicionais
st.sidebar.header("selecione o trimestre, RD, Tipos de Projetos, Setor de Atividade")

# Filtros Gerais 

trimestre =  ["Todos"] + list(df_agrupado['data'].unique())

RD = ["Todos"] + list(df_agrupado['RD'].unique())

projetos = ["Todos"] + list(df_agrupado['projetos'].unique())

empregos = ["Todos"] + list(df_agrupado['empregos'].unique())

atividade = ["Todos"] + list(df_agrupado['atividade'].unique())


# Seleção de filtros na barra lateral

trimestre_selecionado = st.sidebar.selectbox("Selecione o Trimestre", trimestre)

RD_selecionado = st.sidebar.selectbox("Selecione o RD", RD)

projeto_selecionado = st.sidebar.selectbox("Selecione o Tipo de Projeto", projetos)

atividade_selecionado = st.sidebar.selectbox("Selecione a atividade", atividade)

# Aplicando filtros

df_filtrado = df_agrupado.copy()


if trimestre_selecionado != "Todos": 
    df_filtrado = df_filtrado[df_filtrado["data"] == trimestre_selecionado]

if RD_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["RD"] == RD_selecionado]

if projeto_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["projetos"] == projeto_selecionado]

if atividade_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["atividade"] == atividade_selecionado]



 # Mostra uma mensagem no corpo principal da aplicação
st.markdown('### Metricas')


col1, col2, col3, col4 = st.columns(4)
col5, col6 = st.columns(2)


with col1:
    st.markdown(f"""
    <div class="metric-box total-empregos">
        <div class="metric-label">Total de Empregos</div>
        <div class="metric-value">{total_empregos}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box total-investimento">
        <div class="metric-label">Total de Investimento</div>
        <div class="metric-value">{format_large_numbers(total_investimento)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box total-projetos">
        <div class="metric-label">Tipo de Projetos</div>
        <div class="metric-value">{total_projetos}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-box total-atividade">
        <div class="metric-label">Total de Atividade</div>
        <div class="metric-value">{total_atividade}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-box total-projetos">
        <div class="metric-label">Investimento Médio</div>
        <div class="metric-value">{format_large_numbers(investimento_medio)}</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="metric-box total-atividade">
        <div class="metric-label">Emprego Médio</div>
        <div class="metric-value">{format_large_numbers(emprego_medio)}</div>
    </div>
    """, unsafe_allow_html=True)


# Cores no PX 
#colors = px.colors.qualitative.swatches()
#colors.show()

st.divider()

# Criação de colunas para a visualização dos gráficos
col1, col2, col3  = st.columns(3)
col4, col5, col6 = st.columns(3)   
col7,  col8 = st.columns(2)
col9, col10 = st.columns(2)
col11, col12 = st.columns(2)
col13, col14  = st.columns(2)
col15, col16 = st.columns(2)





# Gráfico de barra de investimentos por Rd

df_filtrado = df_filtrado.sort_values(by='investimento', ascending=False)

fig_setor = px.bar(df_filtrado, x="RD", y="investimento",
                   title="Investimento por RD", color="RD", orientation='v', 
                   color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
#fig_setor.update_yaxes(showticklabels=False)


col1.plotly_chart(fig_setor, use_container_width=True)


## maiores investimentos por RD pizza e ToP 3 

investimentos_por_rd = df_filtrado.groupby('RD')['investimento'].sum().reset_index(name='investimentos_por_rd')

top_3_rd = investimentos_por_rd.nlargest(3, 'investimentos_por_rd')


fig_pizza_rd = px.pie(investimentos_por_rd, names='RD', values='investimentos_por_rd',
                   title="investimentos por RD", color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
col2.plotly_chart(fig_pizza_rd, use_container_width=True)

## Top 3 maiores investimentos por RD

top3_fig = px.pie(top_3_rd, names='RD', values='investimentos_por_rd',
                   title="top 3 investimentos por RD", color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
col3.plotly_chart(top3_fig, use_container_width=True)



# Empregos Por RD 

df_filtrado = df_filtrado.sort_values(by='empregos', ascending=False)

fig_empregos = px.bar(df_filtrado, x = 'RD', y='empregos',
                      title="Empregos por RD", color="RD", orientation='v',  color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
col4.plotly_chart(fig_empregos, use_container_width=True)


## top 5 empregos 

empregos_rd = df_filtrado.groupby('RD')['empregos'].sum().reset_index(name='empregos_rd')
top_3_emp = empregos_rd.nlargest(3, 'empregos_rd')

## Emprego Pizza 

fig_pizza_emprego = px.pie(empregos_rd, names='RD', values='empregos_rd',
                   title="empregos por rd",  color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
col5.plotly_chart(fig_pizza_emprego, use_container_width=True)



## Top 3 Empregos por RD
fig_top_emprego = px.pie(top_3_emp, names='RD', values='empregos_rd',
                   title="maiores empregos por rd",  color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
col6.plotly_chart(fig_top_emprego, use_container_width=True)


## separar Interior e Regiao metropolitana 

# Definindo uma função para categorizar os valores de RD
def categorizar_rd(valor):
    if "METROPOLITANA" in valor:
        return "Região Metropolitana"
    else:
        return "Interior"

# Aplicando a função para criar uma nova coluna 'categoria'
df_filtrado['categoria'] = df_filtrado['RD'].apply(categorizar_rd)

# Contando a quantidade de cada categoria
contagem_categoria = df_filtrado['categoria'].value_counts().reset_index(name='quantidade')
contagem_categoria.columns = ['categoria', 'quantidade']

cores = ['#1f77b4', '#ff7f0e'] 

fig = px.pie(contagem_categoria, values='quantidade', names='categoria',
             title='projetos por RMR e interior',  color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
col7.plotly_chart(fig, use_container_width=True)




## Atividade por RD pie

atividade_rd = df_filtrado.groupby('atividade')['RD'].value_counts().reset_index(name='atividade_rd')

atividade_pie = px.pie(atividade_rd, names='RD', values='atividade_rd',
                   title="atividade por RD",  color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
col8.plotly_chart(atividade_pie, use_container_width=True)


## Contagem atividade Pizza 


atividade_soma = df_filtrado.groupby('atividade').size().reset_index(name='contagem_setores')


atividade_fig = px.pie(atividade_soma, names='atividade', values='contagem_setores',
                       title='projeto por setores',color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white' )
col9.plotly_chart(atividade_fig, use_container_width=True)


## Porjetos por atividade Barra 

atividade_soma = atividade_soma.sort_values(by='contagem_setores', ascending=False)
atividade_soma['atividade'] = atividade_soma['atividade'].replace('METALMECÂNICA E DE MATERIAL DE TRANSPORTE', 'TRANSPORTE')

fig_ativ = px.bar(atividade_soma, x = 'atividade', y='contagem_setores',
                  title='projeto por setores',color='atividade', color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white',
                  orientation='v',
                   labels={'atividade': 'Setores de Atividade', 'contagem_setores': 'Contagem de Projetos'})
col10.plotly_chart(fig_ativ, use_container_width=True)


## Interior e Metropolitana Investimento 
def categorizar_rd(valor):
    if "METROPOLITANA" in valor:
        return "Região Metropolitana"
    else:
        return "Interior"

# Aplicando a função para criar uma nova coluna 'categoria'
df_filtrado['categoria'] = df_filtrado['RD'].apply(categorizar_rd)

# Agrupar os dados pela categoria e somar os investimentos
investimento_categoria = df_filtrado.groupby('categoria')['investimento'].sum().reset_index()
empregos_categoria = df_filtrado.groupby('categoria')['empregos'].sum().reset_index()

# Criar o gráfico de pizza
fig = px.pie(investimento_categoria, values='investimento', names='categoria',
             title='Investimento por Região Metropolitana e Interior', 
             color_discrete_sequence=['#1f77b4', '#ff7f0e'], template='plotly_white')
col11.plotly_chart(fig, use_container_width=True)


# Criar o gráfico de pizza para empregos
fig_empregos = px.pie(empregos_categoria, values='empregos', names='categoria',
                      title='Empregos por Região Metropolitana e Interior', 
                      color_discrete_sequence=['#1f77b4', '#ff7f0e'], template='plotly_white')
col12.plotly_chart(fig_empregos, use_container_width=True)


#Investimento por Setor de Atividade 

# Gráfico de barra de investimentos por Rd

df_filtrado = df_filtrado.sort_values(by='investimento', ascending=False)

fig_setor = px.bar(df_filtrado, x="atividade", y="investimento",
                   title="Investimento por atividade", color="RD", orientation='v', 
                   color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')

#col13.plotly_chart(fig_setor, use_container_width=True)


## maiores investimentos por RD pizza e ToP 3 

investimentos_por_setor = df_filtrado.groupby('atividade')['investimento'].sum().reset_index(name='investimentos_por_atividade')

top_3_ativ = investimentos_por_setor.nlargest(3, 'investimentos_por_atividade')


fig_pizza_ativ = px.pie(investimentos_por_setor, names='atividade', values='investimentos_por_atividade',
                   title="investimentos por atividade", color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
col14.plotly_chart(fig_pizza_ativ, use_container_width=True)

## Top 3 maiores investimentos por RD

top3_fig = px.pie(top_3_ativ, names='atividade', values='investimentos_por_atividade',
                   title="top 3 investimentos por atividade", color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
col13.plotly_chart(top3_fig, use_container_width=True)


## Empregos por Atividade 


df_filtrado = df_filtrado.sort_values(by='atividade', ascending=False)

fig_empregos = px.bar(df_filtrado, x = 'atividade', y='empregos',
                      title="Empregos por Atividade", color="atividade", orientation='v',  color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
#col15.plotly_chart(fig_empregos, use_container_width=True)


## top 5 empregos 

empregos_ativ = df_filtrado.groupby('atividade')['empregos'].sum().reset_index(name='empregos_atividade')
top_3_emp = empregos_ativ.nlargest(3, 'empregos_atividade')

## Emprego Pizza 

fig_pizza_emprego = px.pie(empregos_ativ, names='atividade', values='empregos_atividade',
                   title="empregos por atividade",  color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
col16.plotly_chart(fig_pizza_emprego, use_container_width=True)



empregos_ativ = empregos_ativ.sort_values(by='empregos_atividade', ascending=False)

fig_empregos = px.bar(empregos_ativ, x = 'atividade', y='empregos_atividade',
                      title="Empregos por Atividade", color="atividade", orientation='v',  color_discrete_sequence=px.colors.qualitative.Vivid, template='plotly_white')
fig_empregos.update_layout(
    xaxis_title="Setor",
    yaxis_title="Empregos por Atividade"
)
col15.plotly_chart(fig_empregos, use_container_width=True)




