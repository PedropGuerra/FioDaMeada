from time import strftime
from random import choices
from datetime import date
import requests
from SCRIPTS.sql_fiodameada import *
import os


CLIENT_ID = os.getenv("SP_CLIENT_ID")
CLIENT_SECRET = os.getenv("SP_CLIENT_SECRET")
BOT_ID = os.getenv("SP_BOT_ID")


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
        print(request)

        self.access_token = request["access_token"]

    def define_header(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def get_preferencias(self, contact_id: str):
        request = requests.get(
            self.default_api_link + "/contacts/get",
            params={"id": contact_id},
            headers=self.define_header(),
        ).json()

        print(f"request pref: {request}")
        if len(request["data"]["tags"]) >= 1:
            response = list(
                map(
                    lambda tag: Preferencia_Usuarios().confirm(Nome_Preferencia=tag),
                    request["data"]["tags"],
                )
            )

            response = list(map(lambda x: x[0], response))

            return response

        else:
            return None

    def get_contatos(self):
        preferencias = map(lambda pref: pref[1], Preferencia_Usuarios().select())
        url = self.default_api_link + "/contacts/getByTag"
        contatos = []

        for pref in preferencias:
            request = requests.get(
                url, params={"tag": pref}, headers=self.define_header()
            )
            contatos_temp = map(
                lambda contact: contatos.append(contact["id"]), request["data"]
            )

        return contatos

    def run_flows(self, flow_id: str, contacts: list) -> None:
        url = self.default_api_link + "/flows/run"

        for contact in contacts:
            params = {"contact_id": contact_id, "flow_id": flow_id}
            requests.post(url, params=params, headers=self.define_header())

    def sync_formatos(self):
        url = self.default_api_link + "/flows"

        request_flows = requests.get(
            url, params={"bot_id": BOT_ID}, headers=self.define_header()
        ).json()

        db_sendpulse = SendPulse_Flows()
        flows_db = db_sendpulse.select(categorizacao="todos")

        for flow in request_flows["data"]:
            confirm = db_sendpulse.confirm(ID_FLOW_API=flow["id"])
            if confirm[1] != flow["name"]:
                db_sendpulse.update(ID_FLOW_API=flow["id"], Nome_Flow=flow["name"])

            elif len(confirm) == 0:
                db_sendpulse.insert(
                    ID_FLOW_API=flow["id"],
                    Nome_Flow=flow["name"],
                    Data_Registro=flow["created_at"],
                )
