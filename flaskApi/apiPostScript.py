import tools.flaskSupportTools as apiTools
from flask import request, Response


def apiPostScript():
    from services.Script_Crawl import FioDaMeada_Script_Crawling as Crawl

    apiTools.apiKeyValidate(request.args.get("API_KEY"))
    Crawl()
    return Response(status=200)
