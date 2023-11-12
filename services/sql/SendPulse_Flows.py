from services.sql.connection import executar_comando_sql
from tools.stringManipulate import valuesToDatabaseString


class SendPulse_Flows:
    """a"""

    def __init__(self) -> None:
        self.nome_tabela = "SendPulse_Flows"

    def insert(
        self,
        ID_Flow_API: str,
        Nome_Flow: str,
        Data_Registro: str,
        Dia_Semana: int = None,
    ) -> None:
        """
        Dia_Semana = 1 (Domingo)
        Dia_Semana = 2 (Segunda)
        Dia_Semana = 3 (Terça)
        Dia_Semana = 4 (Quarta)
        Dia_Semana = 5 (Quinta)
        Dia_Semana = 6 (Sexta)
        Dia_Semana = 7 (Sábado)
        """

        values = {
            "ID_Flow_API": ID_Flow_API,
            "Nome_Flow": Nome_Flow,
            "Data_Registro": Data_Registro,
            "Dia_Semana": Dia_Semana,
        }

        values_string = valuesToDatabaseString("insert", values)
        insert_into = f"INSERT INTO {self.nome_tabela} VALUES ({values_string})"

        executar_comando_sql(insert_into)

    def select(
        self, categorizacao: str, ID_Flow_API: str = None, Dia_Semana: int = None
    ):
        """
        categorizacao = 'id', 'dia', 'todos'
        Dia_Semana = 1 (Domingo)
        Dia_Semana = 2 (Segunda)
        Dia_Semana = 3 (Terça)
        Dia_Semana = 4 (Quarta)
        Dia_Semana = 5 (Quinta)
        Dia_Semana = 6 (Sexta)
        Dia_Semana = 7 (Sábado)
        """

        match categorizacao:
            case "id":
                if ID_Flow_API:
                    where = f"ID_Flow_API = {ID_Flow_API}"
                    select_from = f"SELECT * FROM {self.nome_tabela} WHERE {where}"
                    return executar_comando_sql(select_from)

            case "dia":
                if Dia_Semana and Dia_Semana <= 7 and Dia_Semana >= 1:
                    where = f"Dia_Semana = {Dia_Semana}"
                    select_from = (
                        f"SELECT ID_Flow_API FROM {self.nome_tabela} WHERE {where}"
                    )
                    return executar_comando_sql(select_from)

                else:
                    return None

            case "todos":
                select_from = f"SELECT * FROM {self.nome_tabela}"
                return executar_comando_sql(select_from)

    def update(self, ID_Flow_API: str, Nome_Flow: str = None, Dia_Semana: int = None):
        columns_dict = {
            "ID_Flow_API": ID_Flow_API,
            "Nome_Flow": Nome_Flow,
            "Dia_Semana": Dia_Semana,
        }

        set_string = valuesToDatabaseString("update", columns_dict)
        where = f"ID_Flow_API = {ID_Flow_API}"
        sql_string = f"UPDATE {self.nome_tabela} SET {set_string} WHERE {where}"

        executar_comando_sql(sql_string)

    def confirm(self, ID_Flow_API: str = None, Nome_Flow: str = None):
        if ID_Flow_API:
            where = f"ID_Flow_API = '{ID_Flow_API}'"

        elif Nome_Flow:
            where = f"Nome_Flow = '{Nome_Flow}'"

        select_from = (
            f"SELECT ID_Flow_API, Nome_Flow from {self.nome_tabela} WHERE {where}"
        )
        return executar_comando_sql(select_from)[0]
