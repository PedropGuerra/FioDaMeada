from services.sql.connection import executar_comando_sql
from tools.stringManipulate import valuesToDatabaseString
from tools.timeManipulate import FORMAT_DATA
import time


class Parceiros:
    def __init__(self) -> None:
        self.nome_tabela = "Parceiros"

    def insert(
        self,
        Nome_Parceiro: str,
        Link_Parceiro: str,
        ID_Metodo_Coleta: str,
        Tags_HTML_Raspagem: str = None,
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
            "ID_Parceiro": "null",
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

        value_string = valuesToDatabaseString("insert", values)
        insert_into = f"INSERT INTO Parceiros VALUES ({value_string})"
        executar_comando_sql(insert_into)

    def alterar_status(self, confirmation_string: str):
        """Escreva = ID_Parceiro/Nome_Parceiro/StatusDesejado"""

        confirmation_string = confirmation_string.split("/")

        if type(confirmation_string) == list and confirmation_string:
            update = f"UPDATE Parceiros SET Status = '{confirmation_string[2]}' WHERE ID_Parceiro = '{confirmation_string[0]}' AND Nome_Parceiro = '{confirmation_string[1]}'"
            executar_comando_sql(update)

        else:
            return None

    def confirm(
        self, ID_Parceiro: str = None, Nome_Parceiro: str = None, Status: int = 1
    ):
        """Informe o ID_Parceiro ou Nome_Parceiro para confirmar"""
        if ID_Parceiro:
            select_from = f"SELECT Nome_Parceiro FROM Parceiros WHERE ID_Parceiro = '{ID_Parceiro}' AND Status = '{Status}'"
            print(select_from)
            return executar_comando_sql(select_from)[0][0]

        elif Nome_Parceiro:
            select_from = f"SELECT ID_Parceiro FROM Parceiros WHERE Nome_Parceiro = '{Nome_Parceiro}' AND Status = '{Status}'"
            print(select_from)
            return executar_comando_sql(select_from)[0][0]

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

        set_string = valuesToDatabaseString("update", columns_dict)

        sql_string = (
            f"UPDATE Parceiros SET {set_string} WHERE ID_Parceiro = {ID_Parceiro}"
        )

        executar_comando_sql(sql_string)

    def update_ult_raspagem(self, ID_Parceiro: str):
        update_set = f"UPDATE Parceiros SET Ult_Raspagem = '{time.strftime(FORMAT_DATA)}' WHERE ID_Parceiro = {ID_Parceiro}"
        executar_comando_sql(update_set)

    def select(
        self,
        categorizacao: str,
        status: str = 1,
        ult_raspagem_desde: str = None,
        ult_raspagem_ate: str = None,
    ):
        """
        categorizacao = todos / status / ult_raspagem / script
        """

        match categorizacao:
            case "todos":
                select_from = f"SELECT * FROM {self.nome_tabela}"

            case "status":
                if status:
                    status = f"Status = '{status}'"
                    select_from = f"SELECT * FROM {self.nome_tabela} WHERE {status}"

            case "ult_raspagem":
                if ult_raspagem_desde:
                    if ult_raspagem_ate is None:
                        ult_raspagem_ate = time.strftime(FORMAT_DATA)

                    ult_raspagem_desde = f"Ult_Raspagem >= '{ult_raspagem_desde}'"
                    ult_raspagem_ate = f"AND Ult_Raspagem <= '{ult_raspagem_ate}'"

                    select_from = f"SELECT * FROM {self.nome_tabela} WHERE {ult_raspagem_desde} {ult_raspagem_ate}"

            case "script":
                tabelas_script = (
                    "ID_Parceiro, ID_Metodo_Coleta, Tags_HTML_Raspagem, Link_Parceiro"
                )
                # where_script = f"Ult_Raspagem < '{time.strftime(FORMAT_DATA)}' or Ult_Raspagem is NULL"
                # select_from = f"SELECT {tabelas_script} FROM {self.nome_tabela} WHERE {where_script}"
                select_from = f"SELECT {tabelas_script} FROM {self.nome_tabela}"

        return executar_comando_sql(select_from)

    def confirm_tags(self, parse):
        import feedparser

        tags_entries = [
            "content",
            "link",
            "links",
            "published",
            "publisher",
            "summary",
            "tags",
            "title",
            "updated",
        ]

        for tag in tags_entries:
            try:
                v_test = getattr(parse.entries[0], tag)

            except:
                tags_entries.remove(tag)

        return tags_entries
