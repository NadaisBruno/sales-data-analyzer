import sqlite3


# ======================
# Clients
# ======================

def create_clients_db():
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        empresa TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telefone TEXT NOT NULL,
        faturacao_total REAL NOT NULL
        )
        """)
        con.commit()


def insert_clients_db(nome, empresa, email, telefone, faturacao_total):
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()
        cursor.execute("""
        INSERT INTO clients (nome, empresa, email, telefone, faturacao_total) VALUES (?, ?, ?, ?, ?)
        """, (nome, empresa, email, telefone, faturacao_total))
        con.commit()


def remove_clients_db(remove_client_id):
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()
        cursor.execute("""DELETE FROM clients WHERE id = ?""", (remove_client_id,))
        con.commit()


def list_clients_db():
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM clients")
        return cursor.fetchall()


def update_clients_db(client_id, nome, empresa, email, telefone, faturacao_total):
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()
        cursor.execute("""
        UPDATE clients SET nome = ?, empresa = ?, email = ?, telefone = ?, faturacao_total = ? WHERE id = ?
        """, (nome, empresa, email, telefone, faturacao_total, client_id))
        con.commit()


# esta def permite devolver o registo completo do cliente atraves do seu email do CSV e adiciona-o no CRM
def fetch_client_by_email(email):
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM clients WHERE email = ?", (email,))
        return cursor.fetchone()


# atualiza a faturacao total do cliente no crm atraves e-mail(aqui adicionamos apenas a faturacao no crm a um cliente ja existente)
def update_faturacao_cliente(email, faturacao_total):
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()
        cursor.execute("UPDATE clients set faturacao_total = ? WHERE email = ?", (faturacao_total, email))
        con.commit()


def filter_clients_db(nome="", empresa="", email=""):
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()

        query = """
        SELECT id, nome, empresa, email FROM clients WHERE 1=1
        """

        parametros = []
        # filtro por nome
        if nome:
            query += " AND nome LIKE ?"
            parametros.append(f"%{nome}%")

        # filtro por empresa
        if empresa:
            query += " AND empresa LIKE ?"
            parametros.append(f"%{empresa}%")

        # filtro por email
        if email:
            query += " AND email LIKE ?"
            parametros.append(f"%{email}%")

        cursor.execute(query, parametros)

        return cursor.fetchall()


# ===================
# Leads/Oportunidades
# ===================


def create_leads_db():
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        empresa TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telefone TEXT NOT NULL,
        servico TEXT NOT NULL,
        valor REAL NOT NULL,
        estado TEXT NOT NULL
        )
        """)
        con.commit()


def insert_leads_db(nome, empresa, email, telefone, servico, valor, estado):
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()
        cursor.execute("""
        INSERT INTO leads (nome, empresa, email, telefone, servico, valor, estado) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nome, empresa, email, telefone, servico, valor, estado))
        con.commit()


def remove_leads_db(remove_leads_id):
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()
        cursor.execute("""DELETE FROM leads WHERE id = ? """, (remove_leads_id,))
        con.commit()


def list_leads_db():
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()
        cursor.execute("""SELECT * FROM leads""")
        return cursor.fetchall()


def update_leads_db(leads_id, nome, empresa, email, telefone, servico, valor, estado):
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()
        cursor.execute("""
        UPDATE leads SET nome = ?, empresa = ?, email = ?, telefone = ?, servico = ?, valor = ?,  estado = ? WHERE id = ?
        """, (nome, empresa, email, telefone, servico, valor, estado, leads_id))
        con.commit()


def filter_leads_db(nome="", empresa="", email="", estado=""):
    with sqlite3.connect("tss_crm.db") as con:
        cursor = con.cursor()

        query = """
        SELECT id, nome, empresa, email, estado FROM leads WHERE 1=1
        """

        parametros = []  # guardamos aqui os valores que vao substituir os ? da consulta
        # filtro por nome
        if nome:
            query += " AND nome LIKE ?"
            parametros.append(f"%{nome}%")

        # filtro por empresa
        if empresa:
            query += " AND empresa LIKE ?"
            parametros.append(f"%{empresa}%")

        # filtro por email
        if email:
            query += " AND email LIKE ?"
            parametros.append(f"%{email}%")

        # filtro por estado
        if estado:
            query += " AND estado LIKE ?"
            parametros.append(f"%{estado}%")

        cursor.execute(query, parametros)

        return cursor.fetchall()


create_clients_db()
list_clients_db()
create_leads_db()
list_leads_db()


