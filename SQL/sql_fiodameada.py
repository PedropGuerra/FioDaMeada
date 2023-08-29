import mysql.connector
import time
from typing import Any

# """
# - CRUD de todas as tabelas
# - Principais selects
# """

MAIN_DATABASE = "sql10642707"
HOST = "sql10.freesqldatabase.com"
USER = "sql10642707"
PASSWORD = "4HGIwWshhf"
FORMAT_DATA = "%Y-%M-%D"


def connect_db() -> None:
    global database, mysql_cursor
    database = mysql.connector.connect(
        host=HOST, user=USER, password=PASSWORD, database=MAIN_DATABASE
    )
    mysql_cursor = database.cursor()
    return database, mysql_cursor


def disconnect_db() -> None:
    mysql_cursor.close()
    database.close()


def executar_comando_sql(sql: str, values=None):
    if values == None:
        mysql_cursor.execute(sql)

    elif values != None:
        mysql_cursor.execute(sql, values)

    else:
        print("Erro ao executar um comando")
        exit()

    if "SELECT" in sql or "select" in sql:
        result = mysql_cursor.fetchall()
        database.commit()
        return result

    database.commit()


def transformar_valores_em_string(type: str, values: dict) -> str:
    """Coloque todos os valores em uma lista ordenada por como será enviado ao DB
    type = "insert"/"update"
    """
    value_string = ""

    match type:
        case "insert":
            for count, index in enumerate(values):
                if values[index] == None:
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
                if values[index] == None:
                    continue

                value_string = f"{index} = '{values[index]}' "  # o espaço ao final garante a separação
                set_string += value_string

            return set_string


class SendPulse_Flows:
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
        categorização: str,
        data_desde: str = None,
        data_ate: str = None,
        parceiro_id: str = None,
        tema: str = None,
        preferencia_id: str = None,
    ):
        """
        Categorização = 'data' / 'parceiro' / 'tema' / 'preferencia'
        Formato Data = YYYY-MM-DD

        data_ate -> Se vazio então data atual
        """

        match categorização:
            case "data":
                if data_desde:
                    if data_ate == None:
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

                    for item in tabela_noticia_preferencia:
                        lista_noticias.append(item[1])

                    return list(lista_noticias)

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
