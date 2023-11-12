import logging
from services.sql.connection import executar_comando_sql
from tools.stringManipulate import valuesToDatabaseString
from tools.timeManipulate import FORMAT_DATA
import time

logging.basicConfig(level=logging.INFO)


class Envios:
    def __init__(self) -> None:
        self.nome_tabela = "Envios"

    def insert(
        self,
        ID_Flow_API: str = None,
        Dia_Semana: int = None,
        Data_Envio: str = time.strftime(FORMAT_DATA),
    ):
        """
        Formato Data= AAAA-MM-DD (2023-08-23)
        Status = 0 (Pendente)
        Status = 1 (Enviado)
        Status = 2 (Confirmado)
        """
        values = {
            "ID_Envio": None,
            "Dia_Semana": Dia_Semana,
            "Data_Envio": Data_Envio,
            "ID_Flow_API": ID_Flow_API,
        }

        value_string = valuesToDatabaseString("insert", values)
        insert_into = f"INSERT INTO {self.nome_tabela} VALUES ({value_string})"
        logging.info(insert_into)
        executar_comando_sql(insert_into)

        select_from = f"SELECT MAX(ID_Envio) FROM {self.nome_tabela}"
        return executar_comando_sql(select_from)
