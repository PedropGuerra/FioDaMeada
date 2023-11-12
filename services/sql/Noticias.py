import time
import logging
from services.sql.connection import executar_comando_sql
from tools.timeManipulate import FORMAT_DATA
from tools.stringManipulate import sanitize, valuesToDatabaseString

logging.basicConfig(level=logging.INFO)


class Noticias:
    def __init__(self) -> None:
        self.nome_tabela = "Noticias"
        self.tabela_noticias_preferencia = "Noticias_Preferencias"
        self.tabela_noticias_usuarios = "Noticias_Usuarios"

        # adicionar colunas para cada preferencia
        #

    def insert(
        self,
        ID_Parceiro: str,
        Link_Publicacao: str,
        Headline_Publicacao: str,
        Resumo_Publicacao: str,
        Data_Publicacao_Parceiro: str,
        Data_Registro_DB: str = time.strftime(FORMAT_DATA),
        Status: str = "0",
        Fake: str = "0",
        Fake_Local: str = None,
    ) -> None:
        """
        char(15)
        Formato Data= AAAA-MM-DD (2023-08-23) se vazio será o tempo atual
        ID_Pref_Usuario = 1/2/3/4/5/n.....
        Tema_P
        """
        values = {
            "ID_Noticia": None,
            "ID_Parceiro": ID_Parceiro,
            "Link_Publicacao": sanitize(Link_Publicacao, url=True),
            "Headline_Publicacao": sanitize(Headline_Publicacao),
            "Resumo_Publicacao": sanitize(Resumo_Publicacao),
            "Data_Publicacao_Parceiro": Data_Publicacao_Parceiro,
            "Data_Registro_DB": Data_Registro_DB,
            "Status": Status,
            "Fake": Fake,
            "Fake_Local": Fake_Local,
        }

        values_string = valuesToDatabaseString("insert", values)
        insert_into = f"INSERT INTO {self.nome_tabela} VALUES ({values_string})"
        try:
            executar_comando_sql(insert_into)
        except Exception as e:
            logging.error(e)

    def confirm_preferencia(self, ID_Pref_Usuario: str) -> list:
        """Informe o ID_Parceiro ou Nome_Parceiro para confirmar"""

        confirm_sql = f"SELECT * FROM {self.tabela_noticias_preferencia} WHERE ID_Pref_Usuario = {ID_Pref_Usuario}"
        return executar_comando_sql(confirm_sql)

    def insert_preferencia(self, ID_Pref_Usuario: str, ID_Noticia: str) -> None:
        values = {
            "ID_Pref_Usuario": ID_Pref_Usuario,
            "ID_Noticia": ID_Noticia,
        }

        values_string = valuesToDatabaseString("insert", values)
        insert_into = (
            f"INSERT INTO {self.tabela_noticias_preferencia} VALUES ({values_string})"
        )
        executar_comando_sql(insert_into)

    def noticias_usuario(self, ID_Contato: str, IDs_Noticia) -> None:
        values = {}
        for index, idNoticia in enumerate(IDs_Noticia):
            values[index] = {"idNoticia": idNoticia, "idContato": ID_Contato}

        values_string = valuesToDatabaseString("insertMultiple", values)

        insert_into = (
            f"INSERT INTO {self.tabela_noticias_usuarios} VALUES {values_string}"
        )

        logging.info(insert_into)
        executar_comando_sql(insert_into)

    def select(
        self,
        formato: str = None,
        data_desde: str = None,
        data_ate: str = None,
        # parceiro_id: str = None,
        # tema: str = None,
        preferencias_id: tuple = None,
        # IDs_Noticias: list = None,
        contact_id: str = None,
        qtd_noticias: int = None,
        qtd_fakenews: int = None,
        valoresUnicos: bool = True,
    ):
        """
        formato = 'associacao', 'qtd_noticias' , 'qtd_fakenews'
        Formato Data = YYYY-MM-DD

        data_ate -> Se vazio então data atual
        """

        if formato != "associacao":
            col_pref = "ID_Pref_Usuario"

            where = f"Status = 0 AND NOT ID_Contato = '{contact_id}'"
            where += f" AND ({col_pref} = {preferencias_id[0][0]} or {col_pref} = {preferencias_id[1][0]} or {col_pref} = {preferencias_id[2][0]})"
            where_noticia = " AND Fake = 0"
            where_fake = " AND Fake = 1"

            limit_random_noticia = f" ORDER BY RAND() LIMIT {qtd_noticias}"
            limit_random_fake = f" ORDER BY RAND() LIMIT {qtd_fakenews}"

            distinct = "DISTINCT" if valoresUnicos else ""

            cols_to_select = "n.ID_Noticia, n.ID_Parceiro, n.Link_Publicacao, n.Headline_Publicacao, n.Resumo_Publicacao, n.Fake, n.Fake_Local"
            select_from = (
                f"SELECT {distinct} {cols_to_select} from {self.nome_tabela} as n"
            )
            select_from += f" INNER JOIN {self.tabela_noticias_preferencia} as np on n.ID_Noticia = np.ID_Noticia"
            select_from += f" CROSS JOIN {self.tabela_noticias_usuarios}"
            select_from += f" WHERE {where}"

        match formato:
            case "associacao":
                selectCols = "nt.ID_Noticia, nt.Link_Publicacao, nt.Headline_Publicacao, nt.Resumo_Publicacao"
                leftJoin = "LEFT JOIN Noticias_Preferencias as np on nt.ID_Noticia = np.ID_Noticia"
                where = "np.ID_Pref_Usuario IS NULL"
                select_from = f"SELECT DISTINCT {selectCols} FROM {self.nome_tabela} as nt {leftJoin} WHERE {where}"
                return executar_comando_sql(select_from)

            case "qtd_noticias":
                if qtd_noticias:
                    # loggin.info(select_from + where_noticia + limit_random_noticia)
                    return executar_comando_sql(
                        select_from + where_noticia + limit_random_noticia
                    )

                else:
                    return None

            case "qtd_fakenews":
                if qtd_fakenews:
                    # loggin.info(select_from + where_fake + limit_random_fake)
                    return executar_comando_sql(
                        select_from + where_fake + limit_random_fake
                    )

                else:
                    return None

    def update(
        self,
        ID_Noticia: str,
        ID_Parceiro: str = None,
        Link_Publicacao: str = None,
        Headline_Publicacao: str = None,
        Resumo_Publicacao: str = None,
        Data_Publicacao_Parceiro: str = None,
        Status: str = None,
    ):
        """
        Status = 0 (Não Enviada)
        Status = 1 (Enviada)
        Status = 2 (Inutilizada)
        Status = 3 (Programada)
        """

        if int(Status) < 0 or int(Status) > 2:
            # logging.error("Status de Notícias {Status} inválido")
            return None

        columns_dict = {
            "ID_Parceiro": ID_Parceiro,
            "Link_Publicacao": sanitize(Link_Publicacao, url=True),
            "Headline_Publicacao": sanitize(Headline_Publicacao),
            "Resumo_Publicacao": sanitize(Resumo_Publicacao),
            "Data_Publicacao_Parceiro": Data_Publicacao_Parceiro,
            "Status": Status,
        }

        set_string = valuesToDatabaseString("update", columns_dict)

        sql_string = f"UPDATE {self.nome_tabela} SET {set_string} WHERE ID_Noticia = {ID_Noticia}"

        executar_comando_sql(sql_string)

    def confirm_noticia(self, link_Publicacao: str):
        confirm_sql = f"SELECT ID_Noticia FROM {self.nome_tabela} WHERE link_Publicacao = '{link_Publicacao}'"
        return executar_comando_sql(confirm_sql)
