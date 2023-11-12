import tools.flaskSupportTools as apiTools
from flask import request, Response


def apiPostMensagens():
    from services.integracao import Auth_SendPulse
    from threading import Thread
    from tools.timeManipulate import weekday_sun_first
    from datetime import date

    # HTML Arguments Passed in URL
    argsConfig = {"API_KEY": str, "producao": int}
    argsRequired = ("API_KEY",)
    args = apiTools.apiArgsNoticiasTransform(request.args, argsConfig, argsRequired)

    # API KEY VALIDATION
    apiTools.apiKeyValidate(args["API_KEY"])

    # GET TODAY FLOW -- OR ABORT
    weekday = weekday_sun_first(date.today())
    todayFlow = apiTools.apiTodayFlow(weekday)

    if todayFlow:
        # BUILD CONTACTS GROUPS
        contacts = Auth_SendPulse().get_contatos()
        groups = apiTools.threadGroups4(contacts)

        # SEND FLOWS TO CONTACTS
        for group in groups.values():
            Thread(target=Auth_SendPulse().run_flows, args=(todayFlow, group)).start()

        # REGISTER SEND IN DB
        apiTools.apiRegisterSend(weekday, todayFlow[0][0])

        return Response("Sucess", status=200)
