import mysql.connector
import time


"""
- CRUD de todas as tabelas
- Principais selects
"""

DATABASE = "sql10642707"
HOST = "sql10.freesqldatabase.com"
USER = "sql10642707"
PASSWORD = "4HGIwWshhf"
FORMAT_DATA = "%Y-%M-%D"


class SendPulse_Flows:
    def __init__(self) -> None:
        self.connect_db()

    def connect_db(self):
        self.database = mysql.connector.connect(
            host=HOST, user=USER, password=PASSWORD, database=DATABASE
        )
        self.mysql_cursor = self.database.cursor()

    def disconnect_db(self):
        self.mysql_cursor.close()
        self.database.close()

    def executar_comando_sql(self, sql: str, values=None):
        if values == None:
            self.mysql_cursor.execute(sql)

        elif values != None and type(values) == tuple:
            self.mysql_cursor.execute(sql, values)

        else:
            print("Erro ao executar um comando")
            exit()

        if "SELECT" in sql or "select" in sql:
            result = self.mysql_cursor.fetchall()
            self.database.commit()
            return result

        self.database.commit()

    def insert(self, ID_FLOW_API: str, Nome_Flow: str, Data_Registro: str):
        """
        Formato Data_Registro = AAAA-MM-DD (2023-08-23)
        """

        if not Data_Registro:
            Data_Registro = time.strftime(FORMAT_DATA)

        if ID_FLOW_API and Nome_Flow:
            insert_into = "INSERT INTO SendPulse_Flows (ID_FLOW_API, Nome_Flow, Data_Registro) VALUES (%s,%s,%s)"
            values = (ID_FLOW_API, Nome_Flow, Data_Registro)
            self.executar_comando_sql(insert_into, values)

        else:
            print("Erro ao inserir um valor")

    def delete(self, confirmation_string: str):
        """Escreva = ID_FLOW_API/Nome_Flow"""

        confirmation_string = confirmation_string.split("/")

        if type(confirmation_string) == list and confirmation_string:
            delete_from = f"DELETE FROM SendPulse_Flows WHERE ID_FLOW_API = '{confirmation_string[0]}' AND Nome_Flow = '{confirmation_string[1]}'"
            self.executar_comando_sql(delete_from)

        else:
            exit()

    def confirm(self, ID_FLOW_API: str = None, ID_FLOW_DB: str = None):
        """Informe o ID_FLOW_API ou ID_FLOW_DB para confirmar"""
        if ID_FLOW_API:
            select_from = (
                f"SELECT * FROM SendPulse_Flows WHERE ID_FLOW_API = '{ID_FLOW_API}'"
            )
            return list(self.executar_comando_sql(select_from))

        elif ID_FLOW_DB:
            select_from = (
                f"SELECT * FROM SendPulse_Flows WHERE ID_FLOW_DB = '{ID_FLOW_DB}'"
            )
            return list(self.executar_comando_sql(select_from))

        else:
            return None
