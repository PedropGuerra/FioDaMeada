import tools.flaskSupportTools as apiTools
from flask import request, Response


def apiPostScript():
    import services.crawler.main as Crawl

    apiTools.apiKeyValidate(request.args.get("API_KEY"))
    Crawl()
    return Response(status=200)
