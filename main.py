from SQL.sql_fiodameada import *
from SQL.app import app
import requests
import json
import threading
import time
import random


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


class Auth_SendPulse:
    def __init__(self, client_id, client_secret) -> None:
        self.auth(client_id, client_secret)

    def auth(self, client_id, client_secret):
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }

        return requests.post(
            "https://api.sendpulse.com/oauth/access_token", data=data
        ).json()

    def enviar_mensagem(self, contatos: list, mensagem: str) -> None:
        pass


class Envio:
    def __init__(self, formato: dict, preferencia_usuarios: dict):
        self.formato: dict = formatos
        self.preferencia_usuarios: str = preferencia_usuario
        self.mensage_dict: dict = {}
        

    def replace_space(text:str, replacements:dict):
        for to_replace in replacements:
            old = to_replace
            new = replacements[to_replace]
            text = text.replace(old,new)

        return text

    def importar_noticias(self):
        return Noticias().select(categorizacao="preferencia", preferencia_id = self.preferencia_usuarios)

    
    def importar_info_formatos(self):
        pass
        #Formatos().select(ID_Formato = self.formato)
    

    def selecionar_noticias(self, qtd: int):
        from random import choices
        noticias = self.importar_noticias()
        return choices(noticias, k=qtd)

    
    def formatacao_html(self) -> dict:
        replacements = {"{data}" : time.strftime("%d/%m/%Y")}
        html_format = self.importar_info_formatos()
        noticias = selecionar_noticias(html_format.count("{headline"))
        for i, noticia in enumerate(noticias):
            i+=1
            replacements[f"headline{i}"] = noticia[h3]
            replacements[f"link{i}"] = noticia[2]

        self.message_dict = {
            "text": self.replace_space(html_format, replacements),
            "parse_mode" : "html"
        }
        return self.message_dict

    def exp_formatacao_manual(self):
        if len(self.message_dict) != 0:
            return Response(self.message_dict["text"], mimetype="text/html", headers="Content-Disposition":"attachment;filename=msg_format.html")
        
        else:
            return "Não foi possível exportar, a mensagem pode ainda não ter sido formada"
        #exporta um json
    
    def imp_formatacao_manual(self, html_string: str):
        if len(self.message_dict) != 0:
            self.message_dict["text"] = html_string

        else:
            return "Não foi possível importar, a mensagem pode ainda não ter sido formada"
        #importa o json para envio

if __name__ == "__main__":
    # REST_API_ID = "ee842a8007e7a34e290dc77fc984df78"
    # REST_API_SECRET = "2ef059710b021d02111b97b8a28c044f"

    # SendPulse_Api = Auth_SendPulse(REST_API_ID, REST_API_SECRET)

    # Noticias().select()


    #Classe Envio (1 classe por envio)
    #Flask precisa ter um rota para a execução
    #A lógica será importar o calendário (json) com os formatos
    #Definição da formatação de cada dia e quantidade de noticias
    #Classe Auth_SendPulse faz a autenticacao e envio ao telegram
    #Adicionar ao banco de dados (dia da semana/formato)