import streamlit as st
import re
import pandas as pd
import sqlite3
from database import insert_clients_db
from database import list_clients_db
from database import remove_clients_db
from database import update_clients_db
from database import filter_clients_db
from database import insert_leads_db
from database import remove_leads_db
from database import update_leads_db
from database import list_leads_db
from database import filter_leads_db
from database import fetch_client_by_email
from database import update_faturacao_cliente
from read_validate_csv import validate_csv


# --------------------------- CLIENTES -------------------------------------------

# def adicionar clientes mais respetivas validacoes para os respetivos campos
def adicionar_clients(nome_client, empresa_client, email_client, telefone_client, faturacao_total_client):
    # validação para o nome
    if not nome_client.strip():
        st.error("O campo 'Nome' não pode ficar vazio")
        return

    # A-Z = Aceita intervalo de maiusculas
    # a-z = Aceita intervalo de minusculas
    # À-ÿ = Aceita intervalo de caracteres acentuados
    # ' = Aceita apóstrofo
    # + = Permite varios caracteres; sem este + validava nomes com um unico caracter
    if not re.fullmatch(r"[A-Za-zÀ-ÿ' ]+", nome_client):
        st.error("O campo 'nome' contém carateres inválidos e não pode conter elementos númericos")
        return

    # validação para a empresa
    if not empresa_client.strip():
        st.error("O campo 'empresa' não pode ficar vazio")
        return

    # validação para o email
    if not email_client.strip():
        st.error("O campo 'email' não pode ficar vazio")
        return

    if "@" not in email_client or "." not in email_client:
        st.error("O campo 'email' deve conter '@' e '.' ")
        return

    # validação para o telefone
    if not telefone_client.strip():
        st.error("O campo 'telefone' não pode ficar vazio")
        return

    # \+? = aceita '+' no início para números internacionais e pode aparecer até uma vez ou nenhuma
    if not re.fullmatch(r"\+?[0-9]+", telefone_client):
        st.error("O campo 'telefone' só deve conter digitos e, opcionalmente, '+' no ínicio")
        return

    try:
        # vamos buscar funcao da base de dados para inserir o novo cliente
        insert_clients_db(
            nome_client,
            empresa_client,
            email_client,
            telefone_client,
            faturacao_total_client
        )
        st.success("Cliente adicionado com sucesso!")

    except sqlite3.IntegrityError:
        st.error("Já existe um cliente com este email.")


# def para remover clientes
def remover_clients(remove_client_id):
    remove_clients_db(remove_client_id)

    st.success("Cliente removido com sucesso!")


# def para actualizar/editar clientes
def editar_clientes(client_id, nome_client, empresa_client, email_client, telefone_client, faturacao_total_client):
    # validação para o nome
    if not nome_client.strip():
        st.error("O campo 'Nome' não pode ficar vazio")
        return

    # A-Z = Aceita intervalo de maiusculas
    # a-z = Aceita intervalo de minusculas
    # À-ÿ = Aceita intervalo de caracteres acentuados
    # ' = Aceita apóstrofo
    # + = Permite varios caracteres; sem este + validava nomes com um unico caractere
    if not re.fullmatch(r"[A-Za-zÀ-ÿ' ]+", nome_client):
        st.error("O campo 'nome' contém carateres inválidos e não pode conter elementos númericos")
        return

    # validação para a empresa
    if not empresa_client.strip():
        st.error("O campo 'empresa' não pode ficar vazio")
        return

    # validação para o email
    if not email_client.strip():
        st.error("O campo 'email' não pode ficar vazio")
        return

    if "@" not in email_client or "." not in email_client:
        st.error("O campo 'email' deve conter '@' e '.' ")
        return

    # validação para o telefone
    if not telefone_client.strip():
        st.error("O campo 'telefone' não pode ficar vazio")
        return

    # \+? = aceita '+' no início para números internacionais e pode aparecer até uma vez ou nenhuma
    if not re.fullmatch(r"\+?[0-9]+", telefone_client):
        st.error("O campo 'telefone' só deve conter digitos e, opcionalmente, '+' no ínicio")
        return

    try:
        update_clients_db(
            client_id,
            nome_client,
            empresa_client,
            email_client,
            telefone_client,
            faturacao_total_client
        )

        st.success("Cliente atualizado com successo!")

    except sqlite3.IntegrityError:
        st.error("Já existe um cliente com este email.")


# def para a filtragem de clientes
def filtrar_clientes(filter_nome, filter_empresa, filter_email):
    resultados = filter_clients_db(filter_nome, filter_empresa, filter_email)
    return resultados


# Percorre o CSV e cria novos clientes no CRM(com insert_clients_db) ou se o cliente existir no CRM, atualiza a faturacao dos clientes atraves do email
def dados_cliente_faturacao_para_crm(df):
    for i in range(len(df)):
        nome = df["Cliente"][i]
        empresa = df["Empresa"][i]
        email = df["Email"][i]
        telefone = df["Telefone"][i]
        faturacao_total = df["Quantidade"][i] * df["Preço"][i]

        resultado = fetch_client_by_email(email)
        if resultado:
            update_faturacao_cliente(email, faturacao_total)
        else:
            insert_clients_db(nome, empresa, email, telefone, faturacao_total)


# -------------------------- LEADS -----------------------------------------


# def para adicionar leads
def adicionar_leads(nome_leads, empresa_leads, email_leads, telefone_leads, servico_leads, valor_leads, estado_leads):
    # validacao nome
    if not nome_leads.strip():
        st.error("O campo 'nome' não pode ficar vazio")
        return

    if not re.fullmatch(r"[A-Za-zÀ-ÿ' ]+", nome_leads):
        st.error("O campo 'nome' contém carateres inválidos e não pode conter elementos númericos")
        return

    # validacao empresa
    if not empresa_leads.strip():
        st.error("O campo 'empresa' não pode ficar vazio ")
        return

    # validacao email
    if not email_leads.strip():
        st.error("O campo 'email' não pode ficar vazio")
        return

    if "@" not in email_leads or "." not in email_leads:
        st.error("O campo 'email' deve conter '@' e '.' ")
        return

    # validacao telefone
    if not telefone_leads.strip():
        st.error("O campo 'telefone' não pode ficar vazio")
        return

    if not re.fullmatch(r"\+?[0-9]+", telefone_leads):
        st.error("O campo 'telefone' só deve conter digitos e, opcionalmente, '+' no ínicio")
        return

    # validacao servico
    if not servico_leads.strip():
        st.error("O campo 'servico' não pode ficar vazio")
        return

    try:
        # buscamos a def da base de dados(database.py) para inserir as leads
        insert_leads_db(
            nome_leads,
            empresa_leads,
            email_leads,
            telefone_leads,
            servico_leads,
            valor_leads,
            estado_leads
        )

        st.success("Lead adicionado com sucesso!")

    except sqlite3.IntegrityError:
        st.error("Já existe uma lead com este email.")


# def para remover leads
def remover_leads(remove_leads_id):
    remove_leads_db(remove_leads_id)

    st.success("Lead removida com sucesso")


# def para atualizar leads
def editar_leads(leads_id, nome_leads, empresa_leads, email_leads, telefone_leads, servico_leads, valor_leads,
                 estado_leads):
    if not nome_leads.strip():
        st.error("O campo 'nome' não pode ficar vazio")
        return

    if not re.fullmatch(r"[A-Za-zÀ-ÿ' ]+", nome_leads):
        st.error("O campo 'nome' contém carateres inválidos e não pode conter elementos numéricos")
        return

    # validacao empresa
    if not empresa_leads.strip():
        st.error("O campo 'empresa' não pode ficar vazio ")
        return

    # validacao email
    if not email_leads.strip():
        st.error("O campo 'email' não pode ficar vazio")
        return

    if "@" not in email_leads or "." not in email_leads:
        st.error("O campo 'email' deve conter '@' e '.' ")
        return

    # validacao telefone
    if not telefone_leads.strip():
        st.error("O campo 'telefone' não pode ficar vazio")
        return

    if not re.fullmatch(r"\+?[0-9]+", telefone_leads):
        st.error("O campo 'telefone' só deve conter digitos e, opcionalmente, '+' no ínicio")
        return

    # validacao servico
    if not servico_leads.strip():
        st.error("O campo 'servico' não pode ficar vazio")
        return

    try:
        update_leads_db(
            leads_id,
            nome_leads,
            empresa_leads,
            email_leads,
            telefone_leads,
            servico_leads,
            valor_leads,
            estado_leads
        )

        st.success("Lead atualizada com sucesso!")

    except sqlite3.IntegrityError:
        st.error("Já existe uma lead com este email.")


def filtrar_leads(filter_nome, filter_empresa, filter_email, filter_estado):
    return filter_leads_db(filter_nome, filter_empresa, filter_email, filter_estado)


def mostrar_crm():
    # ---- titulo Streamlit ----
    st.title("CRM Formadores Day Traders")

    opcoes = st.selectbox(
        "Por favor escolha uma opçao",
        ("Clientes", "Leads/Oportunidades")
    )

    # --------------------------------- clients ----------------------------------------------
    # ------------- criar clients ----------------------
    if opcoes == "Clientes":
        form_clients = st.form("Clientes", clear_on_submit=True)

        titulo_clientes = form_clients.title("Clientes")

        nome = form_clients.text_input("Nome")
        empresa = form_clients.text_input("Empresa")
        email = form_clients.text_input("Email")
        telefone = form_clients.text_input("Telefone")
        faturacao_total = form_clients.number_input("Faturação total", min_value=0)

        botao_clients = form_clients.form_submit_button("Criar cliente")
        if botao_clients:
            #
            adicionar_clients(nome, empresa, email, telefone, faturacao_total)


        # --------- importar clientes e faturação do CSV para serem adicionados ao formulario -----------

        st.divider()

        st.subheader("Importar clientes e faturação do CSV para o CRM")

        # upload do ficheiro
        file = st.file_uploader("Selecione um ficheiro CSV para importar novos clientes ou atualizar a faturação dos clientes já existentes", type="csv")
        if file is not None:
            st.success("Ficheiro carregado com sucesso")

            # enviamos o ficheiro carregado para a funcao que valida o CSV
            # e se o ficheiro for valido validate_csv() devolve um dataframe
            df = validate_csv(file)

            if df is None:
                return

            botao_importar = st.button("Importar cliente do CSV")
            if botao_importar:
                dados_cliente_faturacao_para_crm(df)

        # subtitulo para a tabela de clientes
        st.subheader("Lista de Clientes")

        st.caption("Selecione um cliente para editar ou remover.")


        # ---------------- remover clients -----------------------------
        # vamos buscar todos os clientes a base de dados
        listar_clientes = list_clients_db()

        # criamos um dataframe com pandas para poder mostrar nomes nas colunas… sem isto o Streamlit mostra so cabecalhos numerados
        dataframe_clientes = pd.DataFrame(
            listar_clientes,
            columns=["ID", "Nome", "Empresa", "Email", "Telefone", "Faturação Total"]
        )

        # mostra todos os clientes numa tabela
        # selection_mode permite selecionar uma linha na tabela
        # faz o streamlit reagir à seleção
        tabela_clientes = st.dataframe(dataframe_clientes, on_select="rerun", selection_mode="single-row")

        # verifica se foi selecionada uma linha na tabela
        if tabela_clientes.selection.rows:

            # guarda o indice da linha selecionada
            indice = tabela_clientes.selection.rows[0]

            # usa o indice da linha anterior para ir buscar o cliente correspondente a lista
            cliente_selecionado = listar_clientes[indice]

            # o primeiro elemento do tuplo do cliente é o seu id
            id_cliente = cliente_selecionado[0]

            # criar o botao para remover o cliente selecionado
            botao_remover_clients = st.button("Remover cliente")

            # se o botao for clicado...
            if botao_remover_clients:
                # ...chama a funcao de remocao de clientes
                remover_clients(id_cliente)

            # ------------------- atualizar clients ------------------------

            atualizar_nome = cliente_selecionado[1]
            atualizar_empresa = cliente_selecionado[2]
            atualizar_email = cliente_selecionado[3]
            atualizar_telefone = cliente_selecionado[4]
            atualizar_faturacao_total = cliente_selecionado[5]

            # criamos um novo formulario, agora para atualizar/editar os clientes
            form_atualizar_clients = st.form("Atualizar Clientes")

            # titulo do formulario
            titulo_atualizar_clientes = form_atualizar_clients.title("Atualizar Clientes")

            # 'value' mostra os dados atuais do cliente
            nome = form_atualizar_clients.text_input("Nome", value=atualizar_nome)
            empresa = form_atualizar_clients.text_input("Empresa", value=atualizar_empresa)
            email = form_atualizar_clients.text_input("Email", value=atualizar_email)
            telefone = form_atualizar_clients.text_input("Telefone", value=atualizar_telefone)
            faturacao_total = form_atualizar_clients.number_input("Faturação total",
                                                                  value=float(atualizar_faturacao_total),
                                                                  min_value=float(0))

            botao_atualizar_clients = form_atualizar_clients.form_submit_button("Atualizar Cliente")
            if botao_atualizar_clients:
                editar_clientes(id_cliente, nome, empresa, email, telefone, faturacao_total)

        # ---------------- filtrar clients -----------------------

        # Criamos um novo formulario para o processo de filtragem
        form_filtrar_clients = st.form("Filtrar Clientes")

        # Titulo do formulario
        titulo_filtrar_clientes = form_filtrar_clients.title("Filtrar Clientes")

        filtro_nome = form_filtrar_clients.text_input("Nome")
        filtro_empresa = form_filtrar_clients.text_input("Empresa")
        filtro_email = form_filtrar_clients.text_input("Email")

        # botao filtrar clientes
        botao_filtrar_clients = form_filtrar_clients.form_submit_button("Filtrar Clientes")
        if botao_filtrar_clients:
            filtro = filtrar_clientes(filtro_nome, filtro_empresa, filtro_email)

            # criamos um dataframe com pandas para poder mostrar nomes nas colunas… sem isto o Streamlit mostra so cabecalhos numerados
            dataframe_filtro = pd.DataFrame(
                filtro,
                columns=["ID", "Nome", "Empresa", "Email"]
            )

            st.dataframe(dataframe_filtro)

    # ------------------------------- leads ----------------------------------------------
    # --------- criar leads -------------------
    if opcoes == "Leads/Oportunidades":
        form_leads = st.form("Leads", clear_on_submit=True)

        # titulo
        titulo_leads = form_leads.title("Leads")

        nome = form_leads.text_input("Nome")
        empresa = form_leads.text_input("Empresa")
        email = form_leads.text_input("Email")
        telefone = form_leads.text_input("Telefone")
        servico = form_leads.text_input("Serviço")
        valor = form_leads.number_input("Valor", min_value=0)
        estado = form_leads.selectbox("Selecione uma opção", ("Novo", "Contactado", "Proposta", "Ganho", "Perdido"))

        # botao leads
        botao_criar_leads = form_leads.form_submit_button("Criar Lead")
        if botao_criar_leads:
            adicionar_leads(nome, empresa, email, telefone, servico, valor, estado)

        st.subheader("Lista de Leads")

        st.caption("Selecione uma lead para editar ou remover")

        # ---------- remover leads ------------------
        listar_leads = list_leads_db()

        # criamos um dataframe com pandas para poder mostrar nomes nas colunas… sem isto o Streamlit mostra so cabecalhos numerados
        dataframe_leads = pd.DataFrame(
            listar_leads,
            columns=["ID", "Nome", "Empresa", "Email", "Telefone", "Serviço", "Valor", "Estado"]
        )

        # criamos a tabela para listar as leads
        tabela_leads = st.dataframe(dataframe_leads, on_select="rerun", selection_mode="single-row")

        # verificamos se foi selecionada uma linha na tabela
        if tabela_leads.selection.rows:

            # guardamos o indice para identificar o ID
            indice = tabela_leads.selection.rows[0]

            # usa o indice da linha anterior para ir buscar a lead correspondente a lista
            lead_selecionada = listar_leads[indice]

            # o primeiro elemento do tuplo da lead é o seu id
            id_lead = lead_selecionada[0]

            # criamos um botao para remover a lead
            botao_remover_lead = st.button("Remover lead")

            if botao_remover_lead:
                remover_leads(id_lead)

            # --------- atualizar leads -----------
            atualizar_lead_nome = lead_selecionada[1]
            atualizar_lead_empresa = lead_selecionada[2]
            atualizar_lead_email = lead_selecionada[3]
            atualizar_lead_telefone = lead_selecionada[4]
            atualizar_lead_servico = lead_selecionada[5]
            atualizar_lead_valor = lead_selecionada[6]
            atualizar_lead_estado = lead_selecionada[7]

            # logica para, ao abrir o selectbox, mostrar o estado atual da lead
            # index() serve para descobrir a posicao de um valor em uma lista
            estados_leads = ["Novo", "Contactado", "Proposta", "Ganho", "Perdido"]
            indice_estados = estados_leads.index(atualizar_lead_estado)

            # criamos um novo formulario para atualizar/editar as leads
            form_atualizar_leads = st.form("Atualizar Leads")

            # criamos um título para a tabela
            form_atualizar_leads_titulo = form_atualizar_leads.title("Atualizar Leads")

            lead_nome = form_atualizar_leads.text_input("Nome", value=atualizar_lead_nome)
            lead_empresa = form_atualizar_leads.text_input("Empresa", value=atualizar_lead_empresa)
            lead_email = form_atualizar_leads.text_input("Email", value=atualizar_lead_email)
            lead_telefone = form_atualizar_leads.text_input("Telefone", value=atualizar_lead_telefone)
            lead_servico = form_atualizar_leads.text_input("Serviço", value=atualizar_lead_servico)
            lead_valor = form_atualizar_leads.number_input("Valor", value=float(atualizar_lead_valor),
                                                           min_value=float(0))
            lead_estado = form_atualizar_leads.selectbox("Selecione uma opção",
                                                         ("Novo", "Contactado", "Proposta", "Ganho", "Perdido"),
                                                         index=indice_estados)

            # criamos o botao para atualizar as leads
            botao_atualizar_leads = form_atualizar_leads.form_submit_button("Atualizar Lead")
            if botao_atualizar_leads:
                editar_leads(id_lead, lead_nome, lead_empresa, lead_email, lead_telefone, lead_servico, lead_valor,
                             lead_estado)

        # ---------- filtrar leads ------------

        # Criamos um novo formulario para o processo de filtragem
        form_filtrar_leads = st.form("Filtrar Leads")

        # criamos um título para o formulario de filtragem
        form_filtrar_leads_titulo = form_filtrar_leads.title("Filtrar Leads")

        filtro_nome_lead = form_filtrar_leads.text_input("Nome")
        filtro_empresa_lead = form_filtrar_leads.text_input("Empresa")
        filtro_email_lead = form_filtrar_leads.text_input("Email")
        filtro_estado_lead = form_filtrar_leads.selectbox("Estado",
                                                          ("", "Novo", "Contactado", "Proposta", "Ganho", "Perdido"))

        # criamos o botao para filtrar as leads
        botao_filtrar_leads = form_filtrar_leads.form_submit_button("Filtrar Lead")
        if botao_filtrar_leads:
            filtro_leads = filtrar_leads(filtro_nome_lead, filtro_empresa_lead, filtro_email_lead, filtro_estado_lead)

            # criamos um dataframe com pandas para poder mostrar nomes nas colunas… sem isto o Streamlit mostra so cabecalhos numerados
            dataframe_filtro_leads = pd.DataFrame(
                filtro_leads,
                columns=["ID", "Nome", "Empresa", "Email", "Estado"]
            )

            st.dataframe(dataframe_filtro_leads)
