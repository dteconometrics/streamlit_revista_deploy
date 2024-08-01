import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Configuração da Tela 

st.set_page_config(page_title="Tabelas",
                page_icon="🛠" ,
                layout="wide")

## Carregando os Dados 

df_agrupado = st.session_state["df_agrupado"]

# Calcular os totais para o value Box 

total_empregos = df_agrupado['empregos'].sum()
total_investimento = df_agrupado['investimento'].sum()
investimento_medio = df_agrupado['investimento'].mean()
emprego_medio = df_agrupado['empregos'].mean()

# Função para simplificar os números grandes e formatar com duas casas decimais
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
# Value Box
col1, col2, col3, col4 = st.columns(4)

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
        <div class="metric-label">Investimento Médio</div>
        <div class="metric-value">{format_large_numbers(investimento_medio)}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-box total-atividade">
        <div class="metric-label">Emprego Médio</div>
        <div class="metric-value">{format_large_numbers(emprego_medio)}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()


## Tabelas 

# Adicionar colunas calculadas

## Investimento e Empregos por RD
investimento_por_rd = df_agrupado.groupby('RD')['investimento'].sum().reset_index().rename(columns={'investimento': 'investimento_por_rd'})
empregos_por_rd = df_agrupado.groupby('RD')['empregos'].sum().reset_index().rename(columns={'empregos': 'empregos_por_rd'})

## iNVESTIMENTO, Emprego por setor e contagem por atividade 

investimento_por_atividade = df_agrupado.groupby('atividade')['investimento'].sum().reset_index().rename(columns={'investimento': 'investimento_por_atividade'})
emprego_por_atividade = df_agrupado.groupby('atividade')['empregos'].sum().reset_index().rename(columns={'empregos': 'emprego_por_atividade'})



# Merge com o dataframe original
#df_agrupado = df_agrupado.merge(investimento_por_rd, on='RD', how='left')
#df_agrupado = df_agrupado.merge(empregos_por_rd, on='RD', how='left')

# Converter a coluna 'data' para string
df_agrupado['data'] = df_agrupado['data'].astype(str)

# Agrupar e calcular os totais
df_agrupado2 = df_agrupado.groupby(['data', 'RD'])[['investimento', 'empregos']].sum().reset_index().rename(columns={'investimento': 'investimento_por_rd', 'empregos': 'empregos_por_rd'})
df_agrupado3 = df_agrupado.groupby(['data', 'atividade'])[['investimento', 'empregos']].sum().reset_index().rename(columns={'investimento': 'investimento_por_atividade', 'empregos': 'empregos_por_atividade'})

df_agrupado4 = df_agrupado.groupby(['data', 'atividade', 'RD']).agg(
    investimento_por_atividade=('investimento', 'sum'),
    empregos_por_atividade=('empregos', 'sum'),
    contagem_atividade=('atividade', 'size')
).reset_index()




# Função para adicionar a linha de totais
# Função para adicionar a linha de totais
def add_total_row(df, groupby_columns, sum_columns):
    totals = df[sum_columns].sum().to_dict()
    total_row = pd.DataFrame({**{col: 'Total' if col in groupby_columns else '' for col in df.columns}, **totals}, index=[0])
    total_row[groupby_columns[0]] = 'Total'
    return pd.concat([df, total_row], ignore_index=True)

# Função para converter DataFrame em Excel
def convert_df_to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer._save()  # Use _save() instead of save() to save the file
    processed_data = output.getvalue()
    return processed_data

# Função para exibir a tabela df_agrupado com filtros e totais
def mostra_tabela_agrupado():
    st.sidebar.divider()
    st.sidebar.markdown('### Filtrar tabela df_agrupado')
    colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas da tabela:',
                                                  list(df_agrupado.columns),
                                                  list(df_agrupado.columns))
    col1, col2 = st.sidebar.columns(2)
    filtro_selecionada = col1.selectbox('Filtrar coluna',
                                        list(df_agrupado.columns))
    valores_unicos_coluna = list(df_agrupado[filtro_selecionada].unique())
    valor_filtro = col2.selectbox('Valor do filtro',
                                  valores_unicos_coluna)
    filtrar = col1.button('Filtrar')
    limpar = col2.button('Limpar')

    if filtrar:
        df_filtrado = df_agrupado.loc[df_agrupado[filtro_selecionada] == valor_filtro, colunas_selecionadas]
        df_filtrado_com_total = add_total_row(df_filtrado, groupby_columns=['data', 'RD'], sum_columns=['investimento', 'empregos'])
        st.dataframe(df_filtrado_com_total, height=800)
    elif limpar:
        df_com_total = add_total_row(df_agrupado[colunas_selecionadas], groupby_columns=['data', 'RD'], sum_columns=['investimento', 'empregos'])
        st.dataframe(df_com_total, height=800)
    else:
        df_com_total = add_total_row(df_agrupado[colunas_selecionadas], groupby_columns=['data', 'RD'], sum_columns=['investimento', 'empregos'])
        st.dataframe(df_com_total, height=800)
    
    # Download button for Excel
    df_download = df_com_total if not filtrar and not limpar else df_filtrado_com_total
    excel_data = convert_df_to_excel(df_download)
    st.sidebar.download_button(label="Download tabela df_agrupado em Excel", data=excel_data, file_name='df_agrupado.xlsx')

# Função para exibir a tabela df_agrupado2 com filtros e totais
def mostra_tabela_agrupado2():
    st.sidebar.divider()
    st.sidebar.markdown('### Filtrar tabela df_agrupado2')
    colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas da tabela:',
                                                  list(df_agrupado2.columns),
                                                  list(df_agrupado2.columns))
    col1, col2 = st.sidebar.columns(2)
    filtro_selecionada = col1.selectbox('Filtrar coluna',
                                        list(df_agrupado2.columns))
    valores_unicos_coluna = list(df_agrupado2[filtro_selecionada].unique())
    valor_filtro = col2.selectbox('Valor do filtro',
                                  valores_unicos_coluna)
    filtrar = col1.button('Filtrar')
    limpar = col2.button('Limpar')

    if filtrar:
        df_filtrado = df_agrupado2.loc[df_agrupado2[filtro_selecionada] == valor_filtro, colunas_selecionadas]
        df_filtrado_com_total = add_total_row(df_filtrado, groupby_columns=['data', 'RD'], sum_columns=['investimento_por_rd', 'empregos_por_rd'])
        st.dataframe(df_filtrado_com_total, height=800)
    elif limpar:
        df_com_total = add_total_row(df_agrupado2[colunas_selecionadas], groupby_columns=['data', 'RD'], sum_columns=['investimento_por_rd', 'empregos_por_rd'])
        st.dataframe(df_com_total, height=800)
    else:
        df_com_total = add_total_row(df_agrupado2[colunas_selecionadas], groupby_columns=['data', 'RD'], sum_columns=['investimento_por_rd', 'empregos_por_rd'])
        st.dataframe(df_com_total, height=800)
    
    # Download button for Excel
    df_download = df_com_total if not filtrar and not limpar else df_filtrado_com_total
    excel_data = convert_df_to_excel(df_download)
    st.sidebar.download_button(label="Download tabela df_agrupado2 em Excel", data=excel_data, file_name='df_agrupado2.xlsx')

def mostra_tabela_agrupado3():
    st.sidebar.divider()
    st.sidebar.markdown('### Filtrar tabela df_agrupado3')
    colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas da tabela:',
                                                  list(df_agrupado3.columns),
                                                  list(df_agrupado3.columns))
    col1, col2 = st.sidebar.columns(2)
    filtro_selecionada = col1.selectbox('Filtrar coluna',
                                        list(df_agrupado3.columns))
    valores_unicos_coluna = list(df_agrupado3[filtro_selecionada].unique())
    valor_filtro = col2.selectbox('Valor do filtro',
                                  valores_unicos_coluna)
    filtrar = col1.button('Filtrar')
    limpar = col2.button('Limpar')

    if filtrar:
        df_filtrado = df_agrupado3.loc[df_agrupado3[filtro_selecionada] == valor_filtro, colunas_selecionadas]
        df_filtrado_com_total = add_total_row(df_filtrado, groupby_columns=['data', 'atividade'], sum_columns=['investimento_por_atividade', 'empregos_por_atividade'])
        st.dataframe(df_filtrado_com_total, height=800)
    elif limpar:
        df_com_total = add_total_row(df_agrupado3[colunas_selecionadas], groupby_columns=['data', 'atividade'], sum_columns=['investimento_por_atividade', 'empregos_por_atividade'])
        st.dataframe(df_com_total, height=800)
    else:
        df_com_total = add_total_row(df_agrupado3[colunas_selecionadas], groupby_columns=['data', 'atividade'], sum_columns=['investimento_por_atividade', 'empregos_por_atividade'])
        st.dataframe(df_com_total, height=800)
    
    # Botão de download para Excel
    df_download = df_com_total if not filtrar and not limpar else df_filtrado_com_total
    excel_data = convert_df_to_excel(df_download)
    st.sidebar.download_button(label="Download tabela df_agrupado3 em Excel", data=excel_data, file_name='df_agrupado3.xlsx')

def mostra_tabela_agrupado4():
    st.sidebar.divider()
    st.sidebar.markdown('### Filtrar tabela df_agrupado4')
    colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas da tabela:',
                                                  list(df_agrupado4.columns),
                                                  list(df_agrupado4.columns))
    col1, col2 = st.sidebar.columns(2)
    filtro_selecionada = col1.selectbox('Filtrar coluna',
                                        list(df_agrupado4.columns))
    valores_unicos_coluna = list(df_agrupado4[filtro_selecionada].unique())
    valor_filtro = col2.selectbox('Valor do filtro',
                                  valores_unicos_coluna)
    filtrar = col1.button('Filtrar')
    limpar = col2.button('Limpar')

    if filtrar:
        df_filtrado = df_agrupado4.loc[df_agrupado4[filtro_selecionada] == valor_filtro, colunas_selecionadas]
        df_filtrado_com_total = add_total_row(df_filtrado, groupby_columns=['data', 'atividade'], sum_columns=['investimento_por_atividade', 'empregos_por_atividade', 'contagem_atividade'])
        st.dataframe(df_filtrado_com_total, height=800)
    elif limpar:
        df_com_total = add_total_row(df_agrupado4[colunas_selecionadas], groupby_columns=['data', 'atividade'], sum_columns=['investimento_por_atividade', 'empregos_por_atividade', 'contagem_atividade'])
        st.dataframe(df_com_total, height=800)
    else:
        df_com_total = add_total_row(df_agrupado4[colunas_selecionadas], groupby_columns=['data', 'atividade'], sum_columns=['investimento_por_atividade', 'empregos_por_atividade', 'contagem_atividade'])
        st.dataframe(df_com_total, height=800)
    
    # Botão de download para Excel
    df_download = df_com_total if not filtrar and not limpar else df_filtrado_com_total
    excel_data = convert_df_to_excel(df_download)
    st.sidebar.download_button(label="Download tabela df_agrupado4 em Excel", data=excel_data, file_name='df_agrupado4.xlsx')

# Interface da barra lateral para seleção de tabela
st.sidebar.markdown('## Seleção de Tabelas')
tabelas_selecionada = st.sidebar.selectbox('Selecione a tabela que você deseja ver:',
                                           ['Agrupado', 'Agrupado2', 'Agrupado3', 'Agrupado4'])

# Mostrar a tabela selecionada
if tabelas_selecionada == 'Agrupado':
    mostra_tabela_agrupado()
elif tabelas_selecionada == 'Agrupado2':
    mostra_tabela_agrupado2()
elif tabelas_selecionada == 'Agrupado3':
    mostra_tabela_agrupado3()
elif tabelas_selecionada == 'Agrupado4':
    mostra_tabela_agrupado4()