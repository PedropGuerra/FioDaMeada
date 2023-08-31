"""
dadadas"""

import mysql.connector
import time
from typing import Any
import math

# """
# - CRUD de todas as tabelas
# - Principais selects
# """

MAIN_DATABASE = "sql10642707"
HOST = "sql10.freesqldatabase.com"
USER = "sql10642707"
PASSWORD = "4HGIwWshhf"
FORMAT_DATA = "%Y-%m-%d"


def connect_db() -> None:
    """a"""
    global database, mysql_cursor
    database = mysql.connector.connect(
        host=HOST, user=USER, password=PASSWORD, database=MAIN_DATABASE
    )
    mysql_cursor = database.cursor()
    return database, mysql_cursor


def disconnect_db() -> None:
    """a"""
    mysql_cursor.close()
    database.close()


def executar_comando_sql(sql: str, values=None):
    """a"""
    if values is None:
        mysql_cursor.execute(sql)

    elif values is not None:
        mysql_cursor.execute(sql, values)

    else:
        print("Erro ao executar um comando")
        exit()

    if "SELECT" in sql or "select" in sql:
        result = mysql_cursor.fetchall()
        database.commit()
        return result

    database.commit()


def transformar_valores_em_string(tipo: str, values: dict) -> str:
    """Coloque todos os valores em uma lista ordenada por como será enviado ao DB
    tipo = "insert"/"update"
    """
    value_string = ""

    match tipo:
        case "insert":
            for count, index in enumerate(values):
                if values[index] is not None:
                    values[index] = "null"

                values[
                    index
                ] = f"'{values[index]}'"  # todos os valores estão sendo inseridos como string
                if count != len(values) - 1:
                    values[index] = values[index] + ","

                value_string += values[index]

            return value_string

        case "update":
            set_string: str = ""

            for index in values:
                if values[index] is None:
                    continue

                value_string = f"{index} = '{values[index]}' "  # manter espaço
                set_string += value_string

            return set_string


class SendPulse_Flows:
    """a"""

    def __init__(self) -> None:
        pass

    def insert(self, ID_FLOW_API: str, Nome_Flow: str, Data_Registro: str):
        """
        Formato Data_Registro = AAAA-MM-DD (2023-08-23)
        """

        if not Data_Registro:
            Data_Registro = time.strftime(FORMAT_DATA)

        if ID_FLOW_API and Nome_Flow:
            insert_into = "INSERT INTO SendPulse_Flows (ID_FLOW_API, Nome_Flow, Data_Registro) VALUES (%s,%s,%s)"
            values = (ID_FLOW_API, Nome_Flow, Data_Registro)
            executar_comando_sql(insert_into, values)

        else:
            print("Erro ao inserir um valor")

    def delete(self, confirmation_string: str):
        """Escreva = ID_FLOW_API/Nome_Flow"""

        confirmation_string = confirmation_string.split("/")

        if type(confirmation_string) == list and confirmation_string:
            delete_from = f"DELETE FROM SendPulse_Flows WHERE ID_FLOW_API = '{confirmation_string[0]}' AND Nome_Flow = '{confirmation_string[1]}'"
            executar_comando_sql(delete_from)

        else:
            exit()

    def confirm(self, ID_FLOW_API: str = None, ID_FLOW_DB: str = None):
        """Informe o ID_FLOW_API ou ID_FLOW_DB para confirmar"""
        if ID_FLOW_API:
            select_from = (
                f"SELECT * FROM SendPulse_Flows WHERE ID_FLOW_API = '{ID_FLOW_API}'"
            )
            return list(executar_comando_sql(select_from))

        elif ID_FLOW_DB:
            select_from = (
                f"SELECT * FROM SendPulse_Flows WHERE ID_FLOW_DB = '{ID_FLOW_DB}'"
            )
            return list(executar_comando_sql(select_from))

        else:
            return None


class Metodo_Raspagem_Noticias:
    def __init__(self) -> None:
        pass

    def insert(self, Nome_Metodo_Coleta: str):
        """char(10)"""
        insert_into = (
            "INSERT INTO Metodo_Raspagem_Noticias (Nome_Metodo_Coleta) VALUES (%s)"
        )
        values = [Nome_Metodo_Coleta]
        executar_comando_sql(insert_into, values)

    def delete(self, confirmation_string: str):
        """Escreva = ID_Metodo_Coleta/Nome_Metodo_Coleta"""

        confirmation_string = confirmation_string.split("/")

        if type(confirmation_string) == list and confirmation_string:
            delete_from = f"DELETE FROM Metodo_Raspagem_Noticias WHERE ID_Metodo_Coleta = '{confirmation_string[0]}' AND Nome_Metodo_Coleta = '{confirmation_string[1]}'"
            executar_comando_sql(delete_from)

        else:
            exit()

    def confirm(self, ID_Metodo_Coleta: str = None, Nome_Metodo_Coleta: str = None):
        """Informe o ID_Metodo_Coleta ou Nome_Metodo_Coleta para confirmar"""
        if ID_Metodo_Coleta:
            select_from = f"SELECT * FROM Metodo_Raspagem_Noticias WHERE ID_Metodo_Coleta = '{ID_Metodo_Coleta}'"
            return list(executar_comando_sql(select_from))

        elif Nome_Metodo_Coleta:
            select_from = f"SELECT * FROM Metodo_Raspagem_Noticias WHERE Nome_Metodo_Coleta = '{Nome_Metodo_Coleta}'"
            return list(executar_comando_sql(select_from))

        else:
            return None


class Preferencia_Usuarios:
    def __init__(self) -> None:
        pass

    def insert(self, Nome_Preferencia: str):
        """char(15)"""
        insert_into = "INSERT INTO Preferencia_Usuarios (Nome_Preferencia) VALUES (%s)"
        values = [Nome_Preferencia]
        executar_comando_sql(insert_into, values)

    def delete(self, confirmation_string: str):
        """Escreva = ID_Pref_Usuario/Nome_Preferencia"""

        confirmation_string = confirmation_string.split("/")

        if type(confirmation_string) == list and confirmation_string:
            delete_from = f"DELETE FROM Preferencia_Usuarios WHERE ID_Pref_Usuario = '{confirmation_string[0]}' AND Nome_Preferencia = '{confirmation_string[1]}'"
            executar_comando_sql(delete_from)

        else:
            exit()

    def confirm(self, ID_Pref_Usuario: str = None, Nome_Preferencia: str = None):
        """Informe o ID_Pref_Usuario ou Nome_Preferencia para confirmar"""
        if ID_Pref_Usuario:
            select_from = f"SELECT * FROM Preferencia_Usuarios WHERE ID_Pref_Usuario = '{ID_Pref_Usuario}'"
            return list(executar_comando_sql(select_from))

        elif Nome_Preferencia:
            select_from = f"SELECT * FROM Preferencia_Usuarios WHERE Nome_Preferencia = '{Nome_Preferencia}'"
            return list(executar_comando_sql(select_from))

        else:
            return None


class Parceiros:
    def __init__(self) -> None:
        pass

    def insert(
        self,
        Nome_Parceiro: str,
        Link_Parceiro: str,
        ID_Metodo_Coleta: str,
        Tags_HTML_Raspagem: str,
        Data_Registro_DB: str = time.strftime(FORMAT_DATA),
        Nome_Responsavel: str = None,
        Contato_Responsavel: str = None,
        Licenca_Distrib: str = None,
        Ult_Raspagem: str = None,
        Status: bool = 1,
    ):
        """
        char(15)
        Formato Data= AAAA-MM-DD (2023-08-23) se vazio será o tempo atual
        ID_Metodo_Coleta = 1/2/3/4/5/n.....
        """
        values = {
            "Nome_Parceiro": Nome_Parceiro,
            "Data_Registro_DB": Data_Registro_DB,
            "Link_Parceiro": Link_Parceiro,
            "Nome_Responsavel": Nome_Responsavel,
            "Contato_Responsavel": Contato_Responsavel,
            "Licenca_Distrib": Licenca_Distrib,
            "ID_Metodo_Coleta": ID_Metodo_Coleta,
            "Tags_HTML_Raspagem": Tags_HTML_Raspagem,
            "Ult_Raspagem": Ult_Raspagem,
            "Status": Status,
        }

        value_string = transformar_valores_em_string("insert", values)
        insert_into = f"INSERT INTO Parceiros VALUES ({value_string})"
        executar_comando_sql(insert_into)

    def alterar_status(self, confirmation_string: str):
        """Escreva = ID_Parceiro/Nome_Parceiro/StatusDesejado"""

        confirmation_string = confirmation_string.split("/")

        if type(confirmation_string) == list and confirmation_string:
            update = f"UPDATE Parceiros SET Status = '{confirmation_string[2]}' WHERE ID_Parceiro = '{confirmation_string[0]}' AND Nome_Parceiro = '{confirmation_string[1]}'"
            executar_comando_sql(update)

        else:
            exit()

    def confirm(
        self, ID_Parceiro: str = None, Nome_Parceiro: str = None, Status: int = 1
    ):
        """Informe o ID_Parceiro ou Nome_Parceiro para confirmar"""
        if ID_Parceiro:
            select_from = f"SELECT * FROM Parceiros WHERE ID_Parceiro = '{ID_Parceiro}' AND Status = '{Status}'"
            return list(executar_comando_sql(select_from))

        elif Nome_Parceiro:
            select_from = f"SELECT * FROM Parceiros WHERE Nome_Parceiro = '{Nome_Parceiro}' AND Status = '{Status}'"
            return list(executar_comando_sql(select_from))

        else:
            return None

    def update(
        self,
        ID_Parceiro: str,
        Nome_Parceiro: str = None,
        Link_Parcerio: str = None,
        Nome_Responsavel: str = None,
        Contato_Responsavel: str = None,
        Licenca_Distrib: str = None,
        ID_Metodo_Coleta: str = None,
        Tags_HTML_Raspagem: str = None,
        Ult_Raspagem: str = None,
        Status: str = None,
    ):
        """
        1. Gerar uma string para tipo de update ("Nome", "Responsavel", "Contato"....)
        Formato = "coluna = 'valor'"
        """

        columns_dict = {
            "Nome_Parceiro": Nome_Parceiro,
            "Link_Parcerio": Link_Parcerio,
            "Nome_Responsavel": Nome_Responsavel,
            "Contato_Responsavel": Contato_Responsavel,
            "Licenca_Distrib": Licenca_Distrib,
            "ID_Metodo_Coleta": ID_Metodo_Coleta,
            "Tags_HTML_Raspagem": Tags_HTML_Raspagem,
            "Ult_Raspagem": Ult_Raspagem,
            "Status": Status,
        }

        set_string = transformar_valores_em_string("update", columns_dict)

        sql_string = (
            f"UPDATE Parceiros SET {set_string} WHERE ID_Parceiro = {ID_Parceiro}"
        )

        executar_comando_sql(sql_string)


class Noticias:
    def __init__(self) -> None:
        self.nome_tabela = "Noticias"

        # adicionar colunas para cada preferencia
        #

    def insert(
        self,
        ID_Parceiro: str,
        Link_Publicacao: str,
        Headline_Publicacao: str,
        Resumo_Publicacao: str,
        Tema_Publicacao: str,
        Data_Publicacao_Parceiro: str,
        Data_Registro_DB: str = time.strftime(FORMAT_DATA),
    ):
        """
        char(15)
        Formato Data= AAAA-MM-DD (2023-08-23) se vazio será o tempo atual
        ID_Pref_Usuario = 1/2/3/4/5/n.....
        Tema_P
        """
        values = {
            "ID_Parceiro": ID_Parceiro,
            "Link_Publicacao": Link_Publicacao,
            "Headline_Publicacao": Headline_Publicacao,
            "Resumo_Publicacao": Resumo_Publicacao,
            "Tema_Publicacao": Tema_Publicacao,
            "Data_Publicacao_Parceiro": Data_Publicacao_Parceiro,
            "Data_Registro_DB": Data_Registro_DB,
        }

        value_string = transformar_valores_em_string("insert", values)
        insert_into = f"INSERT INTO {self.nome_tabela} VALUES ({value_string})"
        executar_comando_sql(insert_into)

    def confirm_preferencia(self, ID_Pref_Usuario: str) -> list:
        """Informe o ID_Parceiro ou Nome_Parceiro para confirmar"""
        tabela_noticias_preferencia = "Noticias_Preferencias"

        confirm_sql = f"SELECT * FROM {tabela_noticias_preferencia} WHERE ID_Pref_Usuario = {ID_Pref_Usuario}"
        return executar_comando_sql(confirm_sql)

    def select(
        self,
        categorizacao: str,
        data_desde: str = None,
        data_ate: str = None,
        parceiro_id: str = None,
        tema: str = None,
        preferencia_id: str = None,
    ):
        """
        categorizacao = 'data' / 'parceiro' / 'tema' / 'preferencia'
        Formato Data = YYYY-MM-DD

        data_ate -> Se vazio então data atual
        """

        match categorizacao:
            case "data":
                if data_desde:
                    if data_ate is None:
                        data_ate = time.strftime(FORMAT_DATA)

                    data_desde = f"Data_Publicacao_Parceiro >= '{data_desde}'"
                    data_ate = f"AND Data_Publicacao_Parceiro <= '{data_ate}'"
                    select_from = f"SELECT * FROM {self.nome_tabela} Where {data_desde} {data_ate}"
                    return executar_comando_sql(select_from)

            case "parceiro":
                if parceiro_id:
                    parceiro_id = f"ID_Parceiro = '{parceiro_id}'"
                    select_from = (
                        f"SELECT * FROM {self.nome_tabela} Where {parceiro_id}"
                    )
                    return executar_comando_sql(select_from)

            case "tema":
                if tema:
                    tema = f"Tema_Publicacao = '{tema}'"
                    select_from = f"SELECT * FROM {self.nome_tabela} Where {tema}"
                    return executar_comando_sql(select_from)

            case "preferencia":
                if preferencia_id:
                    tabela_noticia_preferencia = self.confirm_preferencia(
                        preferencia_id
                    )
                    lista_noticias = list()
                    noticias_string = ""

                    for num_noticia in tabela_noticia_preferencia:
                        lista_noticias.append(num_noticia[1])

                    for i, num_noticia in enumerate(lista_noticias):
                        noticias_string += f"ID_Noticia = {num_noticia}"

                        if i != len(lista_noticias) - 1:
                            noticias_string += " AND "

                    select_from = (
                        f"SELECT * FROM {self.nome_tabela} Where {noticias_string}"
                    )
                    return executar_comando_sql(select_from)

    def update(
        self,
        ID_Noticia: str,
        ID_Parceiro: str = None,
        Link_Publicacao: str = None,
        Headline_Publicacao: str = None,
        Resumo_Publicacao: str = None,
        Tema_Publicacao: str = None,
        Data_Publicacao_Parceiro: str = None,
    ):
        """ """

        columns_dict = {
            "ID_Parceiro": ID_Parceiro,
            "Link_Publicacao": Link_Publicacao,
            "Headline_Publicacao": Headline_Publicacao,
            "Resumo_Publicacao": Resumo_Publicacao,
            "Tema_Publicacao": Tema_Publicacao,
            "Data_Publicacao_Parceiro": Data_Publicacao_Parceiro,
        }

        set_string = transformar_valores_em_string("update", columns_dict)

        sql_string = f"UPDATE {self.nome_tabela} SET {set_string} WHERE ID_Noticia = {ID_Noticia}"

        executar_comando_sql(sql_string)


class Envios:
    def __init__(self) -> None:
        self.nome_tabela = "Envios"

    def insert(
        self,
        ID_Envio: str,
        ID_Pref_Usuario: str,
        ID_Noticia: str,
        ID_Flow_DB: str,
        Data_Envio: str,
    ):
        """
        Formato Data= AAAA-MM-DD (2023-08-23)

        """
        values = {
            "ID_Envio": ID_Envio,
            "ID_Pref_Usuario": ID_Pref_Usuario,
            "ID_Noticia": ID_Noticia,
            "ID_Flow_DB": ID_Flow_DB,
            "Data_Envio": Data_Envio,
        }

        value_string = transformar_valores_em_string("insert", values)
        insert_into = f"INSERT INTO {self.nome_tabela} VALUES ({value_string})"
        executar_comando_sql(insert_into)


class Usuarios:
    def __init__(self) -> None:
        self.nome_tabela = "Usuarios"

    def insert(
        self,
        Primeiro_Nome: str,
        Ult_Nome: str = None,
        Data_Registro: str = time.strftime(FORMAT_DATA),
        DDD: str = None,
        Telefone_Celular: str = None,
        Tipo_WhatsApp: str = None,
        Status: str = "1",
        Data_Nasc: str = None,
    ):
        """ """
        Data_Ult_Interacao = None

        values = {
            "Primeiro_Nome": Primeiro_Nome,
            "Ult_Nome": Ult_Nome,
            "Data_Registro": Data_Registro,
            "DDD": DDD,
            "Telefone_Celular": Telefone_Celular,
            "Tipo_WhatsApp": Tipo_WhatsApp,
            "Data_Ult_Interacao": Data_Ult_Interacao,
            "Status": Status,
            "Data_Nasc": Data_Nasc,
        }

        value_string = transformar_valores_em_string("insert", values)
        insert_into = f"INSERT INTO {self.nome_tabela} VALUES ({value_string})"
        executar_comando_sql(insert_into)

    def confirm_status(self, ID_Usuario: str):
        """Informe o ID_Usuario para confirmar o status"""

        confirm_sql = (
            f"SELECT * FROM {self.nome_tabela} WHERE ID_Usuario = {ID_Usuario}"
        )
        return executar_comando_sql(confirm_sql)[-2]

    def select(
        self,
        categorizacao=str,
        ID_Usuario: str = None,
        Data_Registro_desde: str = None,
        Data_Registro_ate: str = None,
        DDD: str = None,
        Telefone_Celular: str = None,
        Tipo_WhatsApp: str = None,
        Status: str = None,
        Data_Nasc: str = None,
        Data_Ult_Interacao: str = None,
    ):
        """
        Categorização = 'ID', 'Data', 'DDD', 'Telefone', 'Tipo_WhatsApp', 'Status', 'Nasc', 'Ult_Interacao'
        """

        match categorizacao:
            case "data":
                if Data_Registro_desde:
                    if Data_Registro_ate is None:
                        Data_Registro_ate = time.strftime(FORMAT_DATA)

                    Data_Registro_desde = f"Data_Registro >= '{Data_Registro_desde}'"
                    Data_Registro_ate = f"AND Data_Registro <= '{Data_Registro_ate}'"
                    select_from = f"SELECT * FROM {self.nome_tabela} Where {Data_Registro_desde} {Data_Registro_ate}"
                    return executar_comando_sql(select_from)

            case "ID":
                if ID_Usuario:
                    ID_Usuario = f"ID_Usuario = '{ID_Usuario}'"
                    select_from = f"SELECT * FROM {self.nome_tabela} Where {ID_Usuario}"
                    return executar_comando_sql(select_from)

            case "DDD":
                if DDD:
                    DDD = f"DDD = '{DDD}'"
                    select_from = f"SELECT * FROM {self.nome_tabela} Where {DDD}"
                    return executar_comando_sql(select_from)

            case "Telefone":
                if Telefone_Celular:
                    Telefone_Celular = f"Telefone_Celular = '{Telefone_Celular}'"
                    select_from = (
                        f"SELECT * FROM {self.nome_tabela} Where {Telefone_Celular}"
                    )
                    return executar_comando_sql(select_from)

            case "Tipo_WhatsApp":
                if Tipo_WhatsApp:
                    Tipo_WhatsApp = f"Tipo_WhatsApp = '{Tipo_WhatsApp}'"
                    select_from = (
                        f"SELECT * FROM {self.nome_tabela} Where {Tipo_WhatsApp}"
                    )
                    return executar_comando_sql(select_from)

            case "Status":
                if Status:
                    Status = f"Status = '{Status}'"
                    select_from = f"SELECT * FROM {self.nome_tabela} Where {Status}"
                    return executar_comando_sql(select_from)

            case "Nasc":
                if Data_Nasc:
                    Data_Nasc = f"Data_Nasc = '{Data_Nasc}'"
                    select_from = f"SELECT * FROM {self.nome_tabela} Where {Data_Nasc}"
                    return executar_comando_sql(select_from)

            case "Ult_Interacao":
                if Data_Ult_Interacao:
                    Data_Ult_Interacao = f"Data_Ult_Interacao = '{Data_Ult_Interacao}'"
                    select_from = (
                        f"SELECT * FROM {self.nome_tabela} Where {Data_Ult_Interacao}"
                    )
                    return executar_comando_sql(select_from)

    def update(
        self,
        ID_Usuario: str,
        Primeiro_Nome: str = None,
        Ult_Nome: str = None,
        Data_Registro: str = None,
        DDD: str = None,
        Telefone_Celular: str = None,
        Tipo_WhatsApp: str = None,
        Data_Ult_Interacao: str = None,
        Status: str = "1",
        Data_Nasc: str = None,
    ):
        """ """

        columns_dict = {
            "ID_Usuario": ID_Usuario,
            "Primeiro_Nome": Primeiro_Nome,
            "Ult_Nome": Ult_Nome,
            "Data_Registro": Data_Registro,
            "DDD": DDD,
            "Telefone_Celular": Telefone_Celular,
            "Tipo_WhatsApp": Tipo_WhatsApp,
            "Data_Ult_Interacao": Data_Ult_Interacao,
            "Status": Status,
            "Data_Nasc": Data_Nasc,
        }

        set_string = transformar_valores_em_string("update", columns_dict)

        sql_string = f"UPDATE {self.nome_tabela} SET {set_string} WHERE ID_Usuario = {ID_Usuario}"

        executar_comando_sql(sql_string)
