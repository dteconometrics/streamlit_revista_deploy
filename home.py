import streamlit as st
import webbrowser

st.set_page_config(page_title="Dados do Prodepe",
                   page_icon="🏙️", 
                   layout="wide")




st.markdown("# Dados do Prodepe 🏙️")
st.sidebar.markdown("Desenvolvido por [DGFIAP](https://www.adepe.pe.gov.br/invista-em-pernambuco/incentivos-fiscais/prodepe/)")

st.markdown('## Analise dos Dados Prodepe 2024')

st.divider()

btn = st.button("Acesse os dados tratados na planilha")
if btn:
    webbrowser.open_new_tab("https://docs.google.com/spreadsheets/d/1dlgpf5cgYNmnb4Cmcx7_ElF54R2nrjx8/edit?gid=1203425085#gid=1203425085")

st.divider()

st.markdown(
    '''
    O Programa de Desenvolvimento do Estado de Pernambuco (Prodepe) compreende um conjunto de incentivos fiscais 
    direcionados para alguns setores da atividade econômica, entre os quais se destacam: Indústrias, Centrais de distribuição e Importadores atacadistas.
    O pacote destina-se à atração de novos investimentos para Pernambuco e consolidação dos já existentes, sendo necessária a apresentação de projetos por linha de produtos 
    pelos interessados, e posterior análise e aprovação pelo Conselho Estadual de Políticas Industrial, Comercial e de Serviços (Condic)
    

    ''' 
)

