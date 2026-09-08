import streamlit as st
from read_validate_csv import validate_csv
from csv_metrics import metrics
from html_report import relatorio_html
from graficos import graphics
from crm_tss import mostrar_crm


def open_file():

    # upload do ficheiro
    file = st.file_uploader("Selecione um ficheiro CSV para analizar dados de vendas e gerar relatório em HTML", type="csv")
    if file is not None:
        st.success("Ficheiro carregado.")

        # enviamos o ficheiro carregado para a funcao que valida o CSV
        # e se o ficheiro for valido validate_csv() devolve um dataframe
        df = validate_csv(file)

        # se a validacao falhar para o programa e devolve None e assim nao calcula as metricas com um ficheiro invalido
        if df is None:
            return

        # calculo de todas as metricas do csv
        dict_metrics = metrics(df)

        # gera relatorio de HTML
        relatorio_html(dict_metrics)

        # gera o grafico utilizando os totais por produto
        graphics(dict_metrics["totais_produto"])


# ---- logo da empresa ----
# criacao de uma tabela com tres colunas so para poder centrar o logo da empresa
col1, col2, col3 = st.columns(3)
with col2:
    st.image("Formadores_Day_Traders.png", width=300)


opcoes = st.selectbox(
    "Por favor escolha uma opção",
    ("Análise CSV", "CRM")
    )

if opcoes == "Análise CSV":
    open_file()

if opcoes == "CRM":
    mostrar_crm()
