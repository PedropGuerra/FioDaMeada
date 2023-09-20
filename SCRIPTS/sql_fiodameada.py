"""
dadadas"""

import mysql.connector
import time
import json
import bleach

# """
# - CRUD de todas as tabelas
# - Principais selects
# """

MAIN_DATABASE = "fiodameada"
HOST = "34.134.108.235"
USER = "pedro"
PASSWORD = "959538698gbP@"
FORMAT_DATA = "%Y-%m-%d"


def sanitizar_input(input):
    if input != None:
        return bleach.clean(input)

    else:
        return input


def connect_db(user: str = None, password: str = None) -> None:
    """a"""
    global database, mysql_cursor
    if user == None or password == None:
        user = USER
        password = PASSWORD

    database = mysql.connector.connect(
        host=HOST, user=user, password=password, database=MAIN_DATABASE
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
        return resultlocal = random.choice(["contexto", "introducao", "conclusao"])

    database.commit()


def transformar_valores_em_string(tipo: str, values: dict) -> str:
    """Coloque todos os valores em uma lista ordenada por como será enviado ao DB
    tipo = "insert"/"update"
    """
    value_string = ""

    match tipo:
        case "insert":
            for count, index in enumerate(values):
                if values[index] is None or values[index] == "":
                    values[index] = "null"

                values[index] = (
                    f"'{values[index]}'" if values[index] != "null" else "null"
                )

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


def dict_to_json(objeto: dict) -> str:
    return json.dumps(objeto)


def json_to_dict(objeto: str) -> dict:
    return json.loads(objeto)


class SendPulse_Flows:
    """a"""

    def __init__(self) -> None:
        self.nome_tabela = "SendPulse_Flows"

    def insert(
        self, ID_Flow_API: str, Nome_Flow: str, Data_Registro:str, Dia_Semana: int = None
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

        values_string = transformar_valores_em_string("insert", values)
        insert_into = f"INSERT INTO {self.nome_tabela} VALUES ({values_string})"

        executar_comando_sql(insert_into)

    def select(self, categorizacao: str, ID_Flow_API:str = None, Dia_Semana:int = None):
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
                    select_from = f"SELECT * FROM {self.nome_tabela} WHERE {where}"
                    return executar_comando_sql(select_from)

                else:
                    print("Dias da Semana apenas 1/2/3/4/5/6/7")
                    return None

            case "todos":
                select_from = f"SELECT * FROM {self.nome_tabela}"
                return executar_comando_sql(select_from)


    def update(self, ID_Flow_API: str, Nome_Flow:str = None, Dia_Semana: int = None):
        columns_dict = {
            "ID_Flow_API": ID_Flow_API,
            "Nome_Flow": Nome_Flow,
            "Dia_Semana": Dia_Semana,
        }

        set_string = transformar_valores_em_string("update", columns_dict)
        where = f"ID_Flow_API = {ID_Flow_API}"
        sql_string = f"UPDATE {self.nome_tabela} SET {set_string} WHERE {where}"

        executar_comando_sql(sql_string)

    def confirm(self, ID_FLOW_API:str = None, Nome_Flow:str = None):
        if ID_Flow_API:
            where = f"ID_Flow_API = {ID_Flow_API}"

        elif Nome_Flow:
            where = f"Nome_Flow = {Nome_Flow}"

        select_from = f"SELECT ID_Flow_API, Nome_Flow from {self.nome_tabela} WHERE {where}"
        return executar_comando_sql(select_from)


class Preferencia_Usuarios:
    def __init__(self) -> None:
        self.nome_tabela = "Preferencia_Usuarios"

    def insert(self, Nome_Preferencia: str):
        """char(15)"""
        insert_into = "INSERT INTO {self.nome_tabela} (Nome_Preferencia) VALUES (%s)"
        values = [Nome_Preferencia]
        executar_comando_sql(insert_into, values)

    def delete(self, confirmation_string: str):
        """Escreva = ID_Pref_Usuario/Nome_Preferencia"""

        confirmation_string = confirmation_string.split("/")

        if type(confirmation_string) == list and confirmation_string:
            delete_from = f"DELETE FROM {self.nome_tabela} WHERE ID_Pref_Usuario = '{confirmation_string[0]}' AND Nome_Preferencia = '{confirmation_string[1]}'"
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

    def select(self):
        select_from = f"SELECT * FROM {self.nome_tabela}"
        return executar_comando_sql(select_from)


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
            select_from = f"SELECT Nome_Parceiro FROM Parceiros WHERE ID_Parceiro = '{ID_Parceiro}' AND Status = '{Status}'"
            return executar_comando_sql(select_from)[0][0]

        elif Nome_Parceiro:
            select_from = f"SELECT ID_Parceiro FROM Parceiros WHERE Nome_Parceiro = '{Nome_Parceiro}' AND Status = '{Status}'"
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

        set_string = transformar_valores_em_string("update", columns_dict)

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
                where_script = f"Ult_Raspagem < '{time.strftime(FORMAT_DATA)}' or Ult_Raspagem is NULL"
                select_from = f"SELECT {tabelas_script} FROM {self.nome_tabela} WHERE {where_script}"

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
            "ID_Noticia": "null",
            "ID_Parceiro": ID_Parceiro,
            "Link_Publicacao": sanitizar_input(Link_Publicacao),
            "Headline_Publicacao": sanitizar_input(Headline_Publicacao),
            "Resumo_Publicacao": sanitizar_input(Resumo_Publicacao),
            "Data_Publicacao_Parceiro": Data_Publicacao_Parceiro,
            "Data_Registro_DB": Data_Registro_DB,
            "Status": Status,
            "Fake" : Fake,
            "Fake_Local" : Fake_Local,
        }

        values_string = transformar_valores_em_string("insert", values)
        insert_into = f"INSERT INTO {self.nome_tabela} VALUES ({values_string})"
        # print(insert_into)
        try:
            executar_comando_sql(insert_into)
        except:
            pass

    def confirm_preferencia(self, ID_Pref_Usuario: str) -> list:
        """Informe o ID_Parceiro ou Nome_Parceiro para confirmar"""

        confirm_sql = f"SELECT * FROM {self.tabela_noticias_preferencia} WHERE ID_Pref_Usuario = {ID_Pref_Usuario}"
        return executar_comando_sql(confirm_sql)

    def insert_preferencia(self, ID_Pref_Usuario: str, ID_Noticia: str) -> None:
        values = {
            "ID_Pref_Usuario": ID_Pref_Usuario,
            "ID_Noticia": ID_Noticia,
        }

        values_string = transformar_valores_em_string("insert", values)
        insert_into = (
            f"INSERT INTO {self.tabela_noticias_preferencia} VALUES ({values_string})"
        )
        executar_comando_sql(insert_into)


    def noticias_usuario(self, ID_Contato: str, IDs_Noticia) -> None:
        values = {
            "ID_Contato": ID_Contato,
            "IDs_Noticia": IDs_Noticia,
        }

        values_string = transformar_valores_em_string("insert", values)

        insert_into = (
            f"INSERT INTO {self.tabela_noticias_usuarios} VALUES ({values_string})"
        )

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
    ):
        """
        formato = 'associacao', 'qtd_noticias' , 'qtd_fakenews'
        Formato Data = YYYY-MM-DD

        data_ate -> Se vazio então data atual
        """

        if formato != "associacao":
            if preferencias_id and contact_id and len(preferencias_id) == 3:
                col_pref = "ID_Pref_Usuario"
                where = f"Status = 0 AND NOT ID_Contato = {contact_id}"
                where += f" AND ({col_pref} = {preferencias_id[0]} or {col_pref} = {preferencias_id[1]} or {col_pref} = {preferencias_id[2]})"
                where_noticia = " AND Fake = 0"
                where_fake = " AND Fake = 1"
                limit_random_noticia = f" ORDER BY RAND() LIMIT {qtd_noticias}"
                limit_random_fake = f" ORDER BY RAND() LIMIT {qtd_fakenews}"

                cols_to_select = "n.ID_Noticia, n.ID_Parceiro, n.Link_Publicacao, n.Headline_Publicacao, n.Resumo_Publicacao, n.Fake, n.Fake_Local"
                select_from = (
                    f"SELECT DISTINCT {cols_to_select} from {self.nome_tabela} as n"
                )
                select_from += f" INNER JOIN {self.tabela_noticias_preferencia} as np on n.ID_Noticia = np.ID_Noticia"
                select_from += f" CROSS JOIN {self.tabela_noticias_usuarios}"
                select_from += f" WHERE {where}"

        match formato:
            case "associacao":
                if data_desde and data_ate:
                    data_desde = f"Data_Publicacao_Parceiro >= '{data_desde}'"
                    data_ate = f"AND Data_Publicacao_Parceiro <= '{data_ate}'"
                    select_from = f"SELECT * FROM {self.nome_tabela} as nt INNER JOIN Noticias_Preferencias as np on NOT nt.ID_Noticia = np.ID_Noticia WHERE {data_desde} {data_ate}"
                    return executar_comando_sql(select_from)

            case "qtd_noticias":
                return executar_comando_sql(
                    select_from + where_noticia + limit_random_noticia
                )

            case "qtd_fakenews":
                return executar_comando_sql(
                    select_from + where_fake + limit_random_fake
                )

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
            print("Status de Notícias apenas 0/1/2")
            return None

        columns_dict = {
            "ID_Parceiro": ID_Parceiro,
            "Link_Publicacao": sanitizar_input(Link_Publicacao),
            "Headline_Publicacao": sanitizar_input(Headline_Publicacao),
            "Resumo_Publicacao": sanitizar_input(Resumo_Publicacao),
            "Tema_Publicacao": sanitizar_input(Tema_Publicacao),
            "Data_Publicacao_Parceiro": Data_Publicacao_Parceiro,
            "Status": Status,
        }

        set_string = transformar_valores_em_string("update", columns_dict)

        sql_string = f"UPDATE {self.nome_tabela} SET {set_string} WHERE ID_Noticia = {ID_Noticia}"

        executar_comando_sql(sql_string)


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
            "ID_Envio": "null",
            "Dia_Semana": Dia_Semana,
            "Data_Envio": Data_Envio,
            "ID_Flow_API" : ID_Flow_API
        }

        value_string = transformar_valores_em_string("insert", values)
        insert_into = f"INSERT INTO {self.nome_tabela} VALUES ({value_string})"
        executar_comando_sql(insert_into)

        select_from = f"SELECT MAX(ID_Envio) FROM {self.nome_tabela}"
        return executar_comando_sql(select_from)
