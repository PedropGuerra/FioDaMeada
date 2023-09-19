from time import strftime
from random import choices
from datetime import date
import requests
from SCRIPTS.sql_fiodameada import *

"""
Definir preferências por notícias (Web App HTML)
Definir formatos das notícias (Web App HTML)


1. Importar Notícias
2. Importar Noticias_Preferencia
3. Importar Noticias_Formatadas
4. Armazenar noticias+format+pref no Banco de Dados Envios (Adicionar Status)
5. Request SendPulse -> Contatos por Pref
6. Importar Envios -> Request_SendPulse(Enviar + Contatos)

"""

CLIENT_ID = "ee842a8007e7a34e290dc77fc984df78"
CLIENT_SECRET = "2ef059710b021d02111b97b8a28c044f"


def replace_space(text: str, replacements: dict):
    for to_replace in replacements:
        old = to_replace
        new = replacements[to_replace]
        text = text.replace(old, new)

    return text


# def formatacao_html(noticias, html_format) -> dict:
#     replacements = {"{data}": strftime("%d/%m/%Y")}
#     for i, noticia in enumerate(noticias):
#         i += 1
#         replacements[f"noticia{i}"] = noticia[3]
#         replacements[f"link{i}"] = noticia[2]
#     return replace_space(html_format, replacements)


class Auth_SendPulse:
    def __init__(self) -> None:
        self.default_api_link = "https://api.sendpulse.com/telegram"
        self.access_token = ""
        self.auth()

    def auth(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        request = requests.post(
            "https://api.sendpulse.com/oauth/access_token", data=data
        ).json()

        self.access_token = request["access_token"]

    def get_preferencias(self, contact_id: str):
        header = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        request = requests.get(
            self.default_api_link + "/contacts/get",
            params={"id": contact_id},
            headers=header,
        ).json()

        if len(request["data"]["tags"]) >= 1:
            return map(
                lambda tag: Preferencia_Usuarios().confirm(Nome_Preferencia=tag),
                request["data"]["tags"],
            )

        else:
            return None


class Envio:
    def __init__(self, formato: str, preferencia_usuarios: dict):
        self.formato: str = formato
        self.preferencia_usuarios: str = preferencia_usuarios
        self.mensage_dict: dict = {}
        self.noticias: list = []
        self.dia_semana_envio: int = None
        self.id_envio = Envios().insert()
        self.requisicao: dict = {}
        self.flow: str = ""

    def criar(self) -> None:
        self.gerar_requisicao()
        self.salvar_info_db()

    def importar_noticias(self) -> list:
        return Noticias().select(
            categorizacao="preferencia", preferencia_id=self.preferencia_usuarios
        )

    def importar_info_formatos(self) -> str:
        formatos_info = Formatos().select(categorizacao="id", ID_Formato=self.formato)
        self.dia_semana_envio = formatos_info[3]
        self.flow = formatos_info[4]
        return formatos_info[2]

    # def atualizar_status_noticias(self) -> None:
    #     for id_noticia in self.noticias:
    #         Noticias().update(ID_Noticia=id_noticia, Status=1)  # status programado

    def selecionar_noticias(self, qtd: int):
        noticias = self.importar_noticias()
        selecao = choices(noticias, k=qtd)

        for noticia in selecao:
            id_noticia = noticia[0]
            self.noticias.append(id_noticia)

        return selecao

    def requisicao_external_data(self) -> dict:
        external_data = {}
        html_format = self.importar_info_formatos()
        noticias = self.selecionar_noticias(html_format.count("{noticia"))
        for i, noticia in enumerate(noticias):
            i += 1
            external_data[f"noticia{i}"] = noticia[3]
            external_data[f"link{i}"] = noticia[2]

        return external_data

    # def exp_formatacao_manual(self):
    #     if len(self.message_dict) != 0:
    #         return Response(self.message_dict["text"], mimetype="text/html", headers="Content-Disposition":"attachment;filename=msg_format.html")

    #     else:
    #         return "Não foi possível exportar, a mensagem pode ainda não ter sido formada"
    #     #exporta um json

    # def imp_formatacao_manual(self, html_string: str):
    #     if len(self.message_dict) != 0:
    #         self.message_dict["text"] = html_string

    #     else:
    #         return "Não foi possível importar, a mensagem pode ainda não ter sido formada"
    #     #importa o json para envio

    def salvar_info_db(self):
        Envios().update(
            ID_Envio=self.id_envio,
            ID_Pref_Usuario=self.preferencia_usuarios,
            IDs_Noticia=dict_to_json(self.noticias),
            ID_Formato=self.formato,
            ID_Flow_DB=self.flow,
            Dia_Semana=self.dia_semana_envio,
            Data_Criacao=str(date.today()),
            Requisicao_JSON=dict_to_json(self.requisicao),
        )

    def gerar_requisicao(self):
        """
        {
            "contact_id": "string",
            "flow_id": "string",
            "external_data": {
                "noticia": string,
                "noticia": string,
                "noticia": string
            }
        }
        """
        # contatos = self.importar_contatos()
        external_data = self.requisicao_external_data()

        self.requisicao = {
            "contact_id": "null",
            "flow_id": self.flow,
            "external_data": external_data,
        }

        # if __name__ == "__main__":
        #     # REST_API_ID = "ee842a8007e7a34e290dc77fc984df78"
        #     # REST_API_SECRET = "2ef059710b021d02111b97b8a28c044f"
        # BOT_ID = "6500e98627d2d8922a07a065"


#     # SendPulse_Api = Auth_SendPulse(REST_API_ID, REST_API_SECRET)

#     # Noticias().select()

#     #Classe Envio (1 classe por envio)
#     #Classe Auth_SendPulse faz a autenticacao e envio ao telegram
