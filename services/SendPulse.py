import logging
import services.secrets as os
import requests
from datetime import datetime, timedelta

logging.basicConfig(level=logging.DEBUG)


CLIENT_ID = os.getenv("SP_CLIENT_ID")
CLIENT_SECRET = os.getenv("SP_CLIENT_SECRET")
BOT_ID = os.getenv("SP_BOT_ID")
DEFAULT_API_LINK = "https://api.sendpulse.com/telegram"


class SendPulse:
    def __init__(self) -> None:
        self.default_api_link = DEFAULT_API_LINK
        self.auth()

    def AuthDecorator(self, func):
        def wrapper(*args, **kwargs):
            if not self.authenticated():
                self.auth()
            result = func(*args, **kwargs)
            return result

        wrapper.__name__ = func.__name__
        return wrapper

    def authenticated(self):
        authKeyExists = bool(os.getenv("SP_AUTH_KEY"))
        authKeyExpired = (
            datetime.strptime(os.getenv("SP_AUTH_EXPIRE"), "%Y-%m-%d %H:%M:%S.%f")
            <= datetime.now()
        )

        if authKeyExists and not authKeyExpired:
            return True
        else:
            return False

    def auth(self):
        if not self.authenticated():
            authEndpoint = "https://api.sendpulse.com/oauth/access_token"
            data = {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            }

            request = requests.post(authEndpoint, data=data).json()

            authExpireTime = str(
                datetime.now() + timedelta(seconds=request["expires_in"] - 600)
            )
            os.setenv("SP_AUTH_KEY", request["access_token"])
            os.setenv("SP_AUTH_EXPIRE", authExpireTime)

    @AuthDecorator
    def headerUpdated(self):
        return {
            "Authorization": f"Bearer {os.getenv('SP_AUTH_KEY')}",
            "Content-Type": "application/json",
        }

    @AuthDecorator
    def getPreferencias(self, contactID: str):
        from services.sql.Preferencia_Usuarios import Preferencia_Usuarios

        prefEndpoint = self.default_api_link + "/contacts/get"
        params = {"id": contactID}
        headers = self.headerUpdated()
        request = requests.get(url=prefEndpoint, params=params, headers=headers)

        if request.status_code == 200:
            response = request.json()
            preferences = []

            for tag in response["data"]["tags"]:
                pref = Preferencia_Usuarios().confirm(Nome_Preferencia=tag)[0]
                preferences.append(pref)

        logging.info(response)

        return response

    @AuthDecorator
    def getContatos(self):
        contactsEndpoint = self.default_api_link + "/chats"
        params = {"bot_id": BOT_ID}
        headers = self.headerUpdated()

        request = requests.get(contactsEndpoint, params=params, headers=headers)
        response = request.json()

        if request.status_code == 200:
            contacts = []
            for chat in response["data"]:
                contact = chat["inbox_last_message"]["contact_id"]
                contacts.append(contact)

            return contacts

    @AuthDecorator
    def runFlowsByGroup(self, flowID: str, contactsGroup: list) -> None:
        runFlowEndpoint = self.default_api_link + "/flows/run"
        headers = self.headerUpdated()

        contactsRemaining = contactsGroup.copy()

        for contact in contactsGroup:
            params = {"contact_id": contact, "flow_id": flowID}
            request = requests.post(runFlowEndpoint, params=params, headers=headers)

            if request.status_code != 200:
                self.runFlowsByGroup(flowID=flowID, contactsGroup=contactsRemaining)
                break

            contactIndex = contactsRemaining.index(contact)
            contactsRemaining.pop(contactIndex)

    @AuthDecorator
    def syncFlows(self):
        flowsEndpoint = self.default_api_link + "/flows"
        headers = self.headerUpdated()
        params = {"bot_id": BOT_ID}

        request = requests.get(flowsEndpoint, params=params, headers=headers)
        response = request.json()

        if request.status_code == 200:
            from services.sql.SendPulse_Flows import SendPulse_Flows

            for flow in response["data"]:
                flowExists = SendPulse_Flows().confirm(ID_Flow_API=flow["id"])

                if not flowExists:
                    SendPulse_Flows().insert(
                        ID_Flow_API=flow["id"],
                        Nome_Flow=flow["name"],
                        Data_Registro=flow["created_at"],
                    )

                elif flowExists and flowExists[1] != flow["name"]:
                    SendPulse_Flows().update(
                        ID_Flow_API=flow["id"], Nome_Flow=flow["name"]
                    )
