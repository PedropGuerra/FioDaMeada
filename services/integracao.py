from datetime import datetime, timedelta
import requests
from services.sql_fiodameada import *
import services.secrets as os
import logging
from flask import abort

logging.basicConfig(level=logging.DEBUG)


CLIENT_ID = os.getenv("SP_CLIENT_ID")
CLIENT_SECRET = os.getenv("SP_CLIENT_SECRET")
BOT_ID = os.getenv("SP_BOT_ID")


class Auth_SendPulse:
    def __init__(self) -> None:
        self.default_api_link = "https://api.sendpulse.com/telegram"
        self.auth()

    def auth(self):
        if (
            not os.getenv("SP_AUTH_KEY")
            or datetime.strptime(os.getenv("SP_AUTH_EXPIRE"), "%Y-%m-%d %H:%M:%S.%f")
            <= datetime.now()
        ):
            data = {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            }

            request = requests.post(
                "https://api.sendpulse.com/oauth/access_token", data=data
            ).json()

            os.setenv("SP_AUTH_KEY", request["access_token"])
            os.setenv(
                "SP_AUTH_EXPIRE",
                str(datetime.now() + timedelta(seconds=request["expires_in"] - 600)),
            )
            logging.info(f"{os.getenv('SP_AUTH_KEY')} - {os.getenv('SP_AUTH_EXPIRE')}")

    def define_header(self):
        return {
            "Authorization": f"Bearer {os.getenv('SP_AUTH_KEY')}",
            "Content-Type": "application/json",
        }

    def get_preferencias(self, contact_id: str, continuar=1):
        url = self.default_api_link + "/contacts/get"
        params = {"id": contact_id}
        headers = self.define_header()
        request = requests.get(url=url, params=params, headers=headers)

        if request.status_code == 401:
            continuar = 0

        if continuar:
            request = request.json()
            conditions = ("data" in request, len(request["data"]["tags"]) >= 1)
            request = (
                [
                    Preferencia_Usuarios().confirm(Nome_Preferencia=tag)[0]
                    for tag in request["data"]["tags"]
                ]
                if all(conditions)
                else abort(400, "Problemas com API SendPulse")
            )

            logging.info(request)

            return request

        self.retry_auth(self.get_preferencias, contact_id=contact_id)

    def get_contatos(self, continuar=1):
        url = self.default_api_link + "/chats"

        request = requests.get(
            url, params={"bot_id": BOT_ID}, headers=self.define_header()
        )

        if request.status_code == 401:
            continuar = 0

        if continuar:
            contatos = list(
                map(
                    lambda chat: chat["inbox_last_message"]["contact_id"],
                    request.json()["data"],
                )
            )
            return contatos

        self.retry_auth(self.get_contatos)

    def run_flows(self, flow_id: str, contacts: list, continuar=1) -> None:
        url = self.default_api_link + "/flows/run"

        keep_contacts = contacts.copy()

        for contact in contacts:
            params = {"contact_id": contact, "flow_id": flow_id}
            logging.info(params)
            request = requests.post(url, params=params, headers=self.define_header())
            logging.info(request.json())

            if request.status_code == 401:
                continuar = 0
                break

            keep_contacts.pop(keep_contacts.index(contact))

        if not continuar:
            self.retry_auth(self.run_flows, flow_id=flow_id, contacts=keep_contacts)

    def sync_formatos(self, continuar=1) -> None:
        url = self.default_api_link + "/flows"

        request_flows = requests.get(
            url, params={"bot_id": BOT_ID}, headers=self.define_header()
        )

        if request_flows.status_code == 401:
            continuar = 0

        if continuar:
            db_sendpulse = SendPulse_Flows()
            request_flows = request_flows.json()

            for flow in request_flows["data"]:
                confirm = db_sendpulse.confirm(ID_Flow_API=flow["id"])

                if len(confirm) == 0:
                    db_sendpulse.insert(
                        ID_Flow_API=flow["id"],
                        Nome_Flow=flow["name"],
                        Data_Registro=flow["created_at"],
                    )

                elif confirm[1] != flow["name"]:
                    db_sendpulse.update(ID_Flow_API=flow["id"], Nome_Flow=flow["name"])

            return

        self.retry_auth(self.sync_formatos)

    def retry_auth(self, func, *args, **kwargs) -> None:
        self.auth()
        func(*args, **kwargs)
