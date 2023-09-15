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
            return executar_comando_sql(select_from)

        elif Nome_Parceiro:
            select_from = f"SELECT ID_Parceiro FROM Parceiros WHERE Nome_Parceiro = '{Nome_Parceiro}' AND Status = '{Status}'"
            return executar_comando_sql(select_from)

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
        self.tabela_noticias_formato = "Noticias_Formatos"

        # adicionar colunas para cada preferencia
        #

    def insert(
        self,
        ID_Parceiro: str,
        Link_Publicacao: str,
        Headline_Publicacao: str,
        Resumo_Publicacao: str,
        Data_Publicacao_Parceiro: str,
        Tema_Publicacao: str = None,
        Data_Registro_DB: str = time.strftime(FORMAT_DATA),
        Status: str = "0",
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
            "Tema_Publicacao": sanitizar_input(Tema_Publicacao),
            "Data_Publicacao_Parceiro": Data_Publicacao_Parceiro,
            "Data_Registro_DB": Data_Registro_DB,
            "Status": Status,
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

    def insert_formato(self, ID_Formato: str, ID_Noticia: str) -> None:
        values = {
            "ID_Formato": ID_Formato,
            "ID_Noticia": ID_Noticia,
        }

        values_string = transformar_valores_em_string("insert", values)
        insert_into = (
            f"INSERT INTO {self.tabela_noticias_formato} VALUES ({values_string})"
        )
        executar_comando_sql(insert_into)

    def select(
        self,
        categorizacao: str,
        data_desde: str = None,
        data_ate: str = None,
        parceiro_id: str = None,
        tema: str = None,
        preferencia_id: str = None,
        IDs_Noticias: list = None,
    ):
        """
        categorizacao = 'data' / 'parceiro' / 'tema' / 'preferencia / associacao' / 'IDs/
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
                    where = f"ID_Pref_Usuario = {preferencia_id}"
                    select_from = f"select * from {self.nome_tabela} as n INNER JOIN {self.tabela_noticia_preferencias} as np on n.ID_Noticia = np.ID_Noticia INNER JOIN {self.tabela_noticias_formato} as nf on n.ID_Noticia = nf.ID_Noticia WHERE {where}"
                    return executar_comando_sql(select_from)

            case "associacao":
                if data_desde and data_ate:
                    data_desde = f"Data_Publicacao_Parceiro >= '{data_desde}'"
                    data_ate = f"AND Data_Publicacao_Parceiro <= '{data_ate}'"
                    select_from = f"SELECT * FROM {self.nome_tabela} as nt INNER JOIN Noticias_Preferencias as np on NOT nt.ID_Noticia = np.ID_Noticia WHERE {data_desde} {data_ate}"
                    return executar_comando_sql(select_from)

            case "IDs":
                if IDs_Noticias:
                    where = ""
                    for i, id in enumerate(IDs_Noticias):
                        where += "ID_Noticia = {id}"
                        if i != len(IDs_Noticias) - 1:
                            where += " OR "
                    select_from = f"SELECT * FROM {self.nome_tabela} WHERE {where}"

    def update(
        self,
        ID_Noticia: str,
        ID_Parceiro: str = None,
        Link_Publicacao: str = None,
        Headline_Publicacao: str = None,
        Resumo_Publicacao: str = None,
        Tema_Publicacao: str = None,
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
        ID_Pref_Usuario: str = None,
        IDs_Noticia: str = None,
        ID_Formato: str = None,
        ID_Flow_DB: str = None,
        Dia_Semana: int = None,
        Data_Envio: str = None,
        Data_Criacao: str = None,
        Status: str = None,
        Requisicao_JSON=None,
    ):
        """
        Formato Data= AAAA-MM-DD (2023-08-23)

        """
        values = {
            "ID_Envio": "null",
            "ID_Pref_Usuario": ID_Pref_Usuario,
            "IDs_Noticia": IDs_Noticia,
            "ID_Formato": ID_Formato,
            "ID_Flow_DB": ID_Flow_DB,
            "Dia_Semana": Dia_Semana,
            "Data_Envio": Data_Envio,
            "Data_Criacao": Data_Criacao,
            "Status": Status,
            "Requisicao_JSON": Requisicao_JSON,
        }

        value_string = transformar_valores_em_string("insert", values)
        insert_into = f"INSERT INTO {self.nome_tabela} VALUES ({value_string})"
        executar_comando_sql(insert_into)

        select_from = f"SELECT MAX(ID_Envio) FROM {self.nome_tabela}"
        return executar_comando_sql(select_from)

    def update(
        self,
        ID_Envio: str,
        ID_Pref_Usuario: str = None,
        IDs_Noticia: str = None,
        ID_Formato: str = None,
        ID_Flow_DB: str = None,
        Dia_Semana: int = None,
        Data_Envio: str = None,
        Data_Criacao: str = None,
        Status: str = None,
        Requisicao_JSON=None,
    ):
        columns_dict = {
            "ID_Pref_Usuario": ID_Pref_Usuario,
            "IDs_Noticia": IDs_Noticia,
            "ID_Formato": ID_Formato,
            "ID_Flow_DB": ID_Flow_DB,
            "Dia_Semana": Dia_Semana,
            "Data_Envio": Data_Envio,
            "Data_Criacao": Data_Criacao,
            "Status": Status,
            "Requisicao_JSON": Requisicao_JSON,
        }

        set_string = transformar_valores_em_string("update", columns_dict)
        where = f"ID_Envio = {ID_Envio}"
        sql_string = f"UPDATE {self.nome_tabela} SET {set_string} WHERE {where}"

        executar_comando_sql(sql_string)

    def select(
        self,
    ):
        from datetime import date
        from dateutil.relativedelta import relativedelta

        today = date.today()
        prim_dia = today + relativedelta(day=1)
        ult_dia = today + relativedelta(day=31)
        where = f"Data_Criacao >= {prim_dia} AND Data_Criacao <= {ult_dia}"
        select_from = f"SELECT * FROM {self.nome_tabela} WHERE {where}"
        return executar_comando_sql(select_from)


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


class Formatos:
    def __init__(self) -> None:
        self.nome_tabela = "Formatos"

    def insert(
        self, Nome_Formato: str, HTML_Formato: str, Dia_Semana: int, ID_Flow_DB: str
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
            "ID_Formato": "null",
            "Nome_Formato": Nome_Formato,
            "HTML_Formato": HTML_Formato,
            "Dia_Semana": Dia_Semana,
            "ID_Flow_DB": ID_Flow_DB,
        }

        values_string = transformar_valores_em_string("insert", values)
        insert_into = f"INSERT INTO {self.nome_tabela} VALUES ({values_string})"

        executar_comando_sql(insert_into)

    def select(
        self,
        categorizacao: str,
        ID_Formato: str = None,
        Dia_Semana: int = None,
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
                if ID_Formato:
                    where = f"ID_Formato = {ID_Formato}"
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

    def update(
        self,
        ID_Formato: str,
        Nome_Formato: str = None,
        HTML_Formato: str = None,
        Dia_Semana: int = None,
    ):
        """
        Dia_Semana = 1 (Domingo)
        Dia_Semana = 2 (Segunda)
        Dia_Semana = 3 (Terça)
        Dia_Semana = 4 (Quarta)
        Dia_Semana = 5 (Quinta)
        Dia_Semana = 6 (Sexta)
        Dia_Semana = 7 (Sábado)
        """

        columns_dict = {
            "ID_Formato": ID_Formato,
            "Nome_Formato": Nome_Formato,
            "HTML_Formato": HTML_Formato,
            "Dia_Semana": Dia_Semana,
        }

        set_string = transformar_valores_em_string("update", columns_dict)
        where = f"ID_Formato = {ID_Formato}"
        sql_string = f"UPDATE {self.nome_tabela} SET {set_string} WHERE {where}"

        executar_comando_sql(sql_string)