from SQL.sql_fiodameada import *
from SQL.app import app
import requests
import json
import threading


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


if __name__ == "__main__":
    # REST_API_ID = "ee842a8007e7a34e290dc77fc984df78"
    # REST_API_SECRET = "2ef059710b021d02111b97b8a28c044f"

    # SendPulse_Api = Auth_SendPulse(REST_API_ID, REST_API_SECRET)

    # Noticias().select()
