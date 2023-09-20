from time import strftime
from random import choices
from datetime import date
import requests
from SCRIPTS.sql_fiodameada import *


CLIENT_ID = "ee842a8007e7a34e290dc77fc984df78"
CLIENT_SECRET = "2ef059710b021d02111b97b8a28c044f"
BOT_ID = "6500e98627d2d8922a07a065"


class Auth_SendPulse:
    def __init__(self) -> None:
        self.default_api_link = "https://api.sendpulse.com/telegram"
        self.access_token = ""
        self.header = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

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
        request = requests.get(
            self.default_api_link + "/contacts/get",
            params={"id": contact_id},
            headers=self.header,
        ).json()

        if len(request["data"]["tags"]) >= 1:
            return map(
                lambda tag: Preferencia_Usuarios().confirm(Nome_Preferencia=tag),
                request["data"]["tags"],
            )

        else:
            return None

    def get_contatos(self):
        preferencias = map(lambda pref : pref[1],Preferencia_Usuarios().select())
        url = self.default_api_link + "/contacts/getByTag"
        contatos = []

        for pref in preferencias:
            request = requests.get(url, params={"tag" : pref}, headers = self.header)
            contatos_temp = map(lambda contact : contatos.append(contact["id"]), request["data"])

        return contatos


    def run_flows(self, flow_id: str, contacts: list) -> None:
        url = self.default_api_link + "/flows/run"

        for contact in contacts:
            params = {"contact_id" : contact_id,"flow_id" : flow_id}
            requests.post(url, params=params, headers=self.header)

    def sync_formatos(self):
        url = self.default_api_link + "/flows"

        request_flows = requests.get(url, params={"bot_id" : BOT_ID}, headers=self.header).json()

        db_sendpulse = SendPulse_Flows()
        flows_db = db_sendpulse.select(categorizacao="todos")

        for flow in request_flows["data"]:

            confirm = db_sendpulse.confirm(ID_FLOW_API = flow["id"])
            if confirm[1] != flow["name"]:
                db_sendpulse.update(ID_FLOW_API=flow["id"], Nome_Flow=flow["name"])

            elif len(confirm) == 0:
                db_sendpulse.insert(
                    ID_FLOW_API=flow["id"],
                    Nome_Flow = flow["name"],
                    Data_Registro = flow["created_at"],)