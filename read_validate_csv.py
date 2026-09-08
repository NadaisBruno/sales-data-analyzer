import streamlit as st
import pandas as pd
import re


def validate_csv(file):

    # validacao para o caso de um csv completamente vazio
    try:
        df = pd.read_csv(file, encoding="utf-8", sep=";")
        print(df)

    except pd.errors.EmptyDataError:
        st.error("Erro - CSV está vazio!")
        return None


    # se o df estiver vazio(ou seja o dataframe/tabela esta criada, mas está sem valores) mostra erro
    if df.empty:
        st.error("Erro - O ficheiro contém cabeçalhos mas não contém registos de dados!")
        return None

    # verificamos se o CSV contem as colunas obrigatorias
    colunas_obrigatorias = ["Cliente", "Empresa", "Email", "Telefone", "Produto", "Quantidade", "Preço", "Data"]
    for coluna in colunas_obrigatorias:
        if coluna not in df.columns:
            st.error("Erro - O ficheiro deve conter as colunas: Cliente, Empresa, Email, Telefone, Produto, Quantidade, Preço e Data")
            return None

    # data -----
    # converter a coluna data para o tipo datetime
    # qualquer valor que nao seja uma data valida é tranformado em NAT(not a time)
    # com coerce o program apresenta erro imediato e transforma esse valor numa data invalida(NaT)
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
    if df["Data"].isna().any():
        st.error("Erro - Certifique-se que as datas estão no formato válido(DD-MM-AAAA ou AAAA-MM-DD)")
        return None

    # preço -----
    df["Preço"] = pd.to_numeric(df["Preço"], errors="coerce")
    if df["Preço"].isna().any():
        st.error("Erro - Certifique-se que todos os valores desta coluna são numeros válidos, usando ponto como separador")
        return None

    if (df["Preço"] <= 0).any():
        st.error("Erro - Existem valores negativos ou nulos/zero na coluna Preço")
        return None

    # quantidade -----
    df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
    if df["Quantidade"].isna().any():
        st.error("Erro - Certifique-se que os valores desta coluna são numeros inteiros")
        return None


    if (df["Quantidade"] <= 0).any():
        st.error("Erro - Existem valores negativos ou nulos na coluna 'Quantidade'")
        return None

    if (df["Quantidade"] % 1 != 0).any():
        st.error("Erro - A coluna 'Quantidade' não pode conter valores decimais")
        return None

    # produto -----
    if df["Produto"].isna().any():
        st.error("Erro - A coluna 'Produto' contem valores em falta.Preencha todas as celulas antes de continuar")
        return None

    if (df["Produto"].str.strip() == "").any():
        st.error("Erro - A coluna 'Produto' contem valores vazios ou apenas espaços em branco")
        return None

    # cliente -----
    if df["Cliente"].isna().any():
        st.error("Erro - A coluna 'Cliente' contem valores em falta. Preencha todas as celulas antes de continuar")
        return None

    if (df["Cliente"].str.strip() == "").any():
        st.error("Erro - A coluna 'Cliente' contem valores vazios ou apenas espaços em branco")
        return None

    # Empresa ----
    if df["Empresa"].isna().any():
        st.error("Erro - A coluna 'Empresa' contem valores em falta. Preencha todas as celulas antes de continuar")
        return None

    if (df["Empresa"].str.strip() == "").any():
        st.error("Erro - A coluna 'Empresa' contem valores vazios ou apenas espaços em branco")
        return None

    # Email ----
    if df["Email"].isna().any():
        st.error("Erro - A coluna 'Email' contem valores em falta. Preencha todas as celulas antes de continuar")
        return None

    if (df["Email"].str.strip() == "").any():
        st.error("Erro - A coluna 'Email' contem valores vazios ou apenas espaços em branco")
        return None

    for email in df["Email"]:
        if "@" not in email or "." not in email:
            st.error("O campo 'Email' deve conter '@' e '.' ")
            return None

    # Telefone ----
    if df["Telefone"].isna().any():
        st.error("Erro - A coluna 'Telefone' contem valores em falta. Preencha todas as celulas antes de continuar")
        return None

    # essencial para nao dar erro: converte os valores desta coluna para texto antes das validacoes string
    df["Telefone"] = df["Telefone"].astype(str)

    if (df["Telefone"].str.strip() == "").any():
        st.error("Erro - A coluna 'Telefone' contem valores vazios ou apenas espaços em branco")
        return None

    for telefone in df["Telefone"]:
        if not re.fullmatch(r"\+?[0-9]+", telefone):
            st.error("O campo 'telefone' só deve conter digitos e, opcionalmente, '+' no ínicio")
            return None

    print(df.shape)

    # se o df nao estiver vazio devolve-o com os dados
    return df


