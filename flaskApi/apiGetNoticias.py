import tools.flaskSupportTools as apiTools
from flask import request


def apiGetNoticias():
    # HTML Arguments Passed in URL
    argsConfig = {
        "qtd_noticias": int,
        "qtd_fakenews": int,
        "qtd_rodadas": int,
        "producao": int,
        "contact_id": str,
        "API_KEY": str,
    }
    argsRequired = ("contact_id", "API_KEY")
    args = apiTools.apiArgsTransform(request.args, argsConfig, argsRequired)

    # API KEY VALIDATION
    apiTools.apiKeyValidate(args["API_KEY"])

    # GET CONTACT PREFERENCES ID
    preferecias = apiTools.contactPreferences(args["contact_id"])

    # SELECTING NEWS
    dbNoticias = None
    if args["qtd_noticias"]:
        dbNoticias = apiTools.dbSelectNoticias(
            {
                "formato": "qtd_noticias",
                "qtd_noticias": args["qtd_noticias"],
                "contact_id": args["contact_id"],
                "preferencias_id": preferecias,
            }
        )
        dbNoticias = apiTools.apiFormatNoticias(dbNoticias)

    dbFakeNews = None
    if args["qtd_fakenews"]:
        dbFakeNews = apiTools.dbSelectNoticias(
            {
                "formato": "qtd_fakenews",
                "qtd_fakenews": args["qtd_fakenews"],
                "contact_id": args["contact_id"],
                "preferencias_id": preferecias,
            }
        )
        dbFakeNews = apiTools.apiFormatNoticias(dbFakeNews)

    # UPDATING CONTACT NEWS VIEWS
    if args["producao"]:
        threadArgs = (args["contact_id"], dbNoticias, dbFakeNews)

        # from threading import Thread
        from threading import Thread

        Thread(target=apiTools.dbAtualizarNoticiasContatos, args=threadArgs).start()

    # BUILD JSON RESPONSE
    return apiTools.apiResponseNoticias(
        qtd_noticias=args["qtd_noticias"],
        qtd_fakenews=args["qtd_fakenews"],
        qtd_rodadas=args["qtd_rodadas"],
        db_noticias=dbNoticias,
        db_fakenews=dbFakeNews,
    )
