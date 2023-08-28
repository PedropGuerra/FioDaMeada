import mysql.connector
import time

# """
# - CRUD de todas as tabelas
# - Principais selects
# """

DATABASE = "sql10642707"
HOST = "sql10.freesqldatabase.com"
USER = "sql10642707"
PASSWORD = "4HGIwWshhf"
FORMAT_DATA = "%Y-%M-%D"

database = mysql.connector.connect(
    host=HOST, user=USER, password=PASSWORD, database=DATABASE
)
mysql_cursor = database.cursor()


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
        Data_Registro_DB: str,
        Link_Parceiro: str,
        ID_Metodo_Coleta: str,
        Tags_HTML_Raspagem: str,
        Nome_Responsavel: str = None,
        Contato_Responsavel: str = None,
        Licenca_Distrib: str = None,
        Ult_Raspagem: str = None,
        Status: bool = 1,
    ):
        """
        char(15)
        Formato Data= AAAA-MM-DD (2023-08-23) ou será substituida
        ID_Metodo_Coleta = 1/2/3/4/5/n.....
        """
        values = [
            Nome_Parceiro,
            Data_Registro_DB,
            Link_Parceiro,
            Nome_Responsavel,
            Contato_Responsavel,
            Licenca_Distrib,
            ID_Metodo_Coleta,
            Tags_HTML_Raspagem,
            Ult_Raspagem,
            Status,
        ]

        for i, value in enumerate(values):
            if value == None:
                values.pop(values.index(value))

            value = f"{value}"
            if i != value - 1:
                value = value + ","

        insert_into = f"INSERT INTO Parceiros VALUES ()"
        # executar_comando_sql(insert_into, values)

    def delete(self, confirmation_string: str):
        """Escreva = ID_Pref_Usuario/Nome_Preferencia"""

        confirmation_string = confirmation_string.split("/")

        if type(confirmation_string) == list and confirmation_string:
            delete_from = f"DELETE FROM Parceiros WHERE ID_Pref_Usuario = '{confirmation_string[0]}' AND Nome_Preferencia = '{confirmation_string[1]}'"
            executar_comando_sql(delete_from)

        else:
            exit()

    def confirm(self, ID_Pref_Usuario: str = None, Nome_Preferencia: str = None):
        """Informe o ID_Pref_Usuario ou Nome_Preferencia para confirmar"""
        if ID_Pref_Usuario:
            select_from = (
                f"SELECT * FROM Parceiros WHERE ID_Pref_Usuario = '{ID_Pref_Usuario}'"
            )
            return list(executar_comando_sql(select_from))

        elif Nome_Preferencia:
            select_from = (
                f"SELECT * FROM Parceiros WHERE Nome_Preferencia = '{Nome_Preferencia}'"
            )
            return list(executar_comando_sql(select_from))

        else:
            return None

    def update(self):
        pass
